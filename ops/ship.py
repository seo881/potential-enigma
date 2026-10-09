"""ship.py: the launch pipeline, page by page (Divit, 2026-10-08 LAUNCH RUN, Part 3.3). Called through hubctl.

  hubctl ship BATCH_FILE                  advance every page of the batch as far as code can take it; print what waits on whom
  hubctl ship-done BATCH_FILE URL STAGE --by ID [--fail TEXT]   an agent finished a stage (writer | review | rework)
  hubctl ship-cms BATCH_FILE READBACK.json   after the orchestrator's create/update call: verify the read-back, record the drafts
  hubctl ship-qc URL                      QC as a normal page (the 4 originals are frozen in plain QC; launch brings them to standard)
  hubctl ship-cost BATCH_FILE             tokens per page and per role logged for the batch (hubctl usage-log)
  hubctl readiness                        write status/readiness.md (one row per page, template blockers in the header)

Order per page: autofix (code) -> writer (agent: FAQ replacements from approved secondaries and gate-passing AlsoAsked
questions only, answer-first, no AlsoAsked answer text; remaining A5/A6/C4/C5 and other QC flags; 4 chip prompts for T1)
-> check (code: QC TOTAL 0, PAA gate 10/10, chip prompts) -> images (the render Action, only if the brief changed)
-> review (batch reviewer, blocking findings only) -> [rework (a different writer) -> check -> images -> hubctl ready]
-> payload (link-to-live applied) -> cms (orchestrator: create or update the DRAFT, read back) -> done.
A page that fails the same stage twice is stopped, never forced, and listed. Ledger: status/ship/<batch>.json (public:
no question text, no SERP data). Writer briefs go to .cache/ship/ (git-ignored: they quote FAQ questions).
"""
import json, os, re, sys, glob, hashlib, subprocess, datetime, csv
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc", "pipeline"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H, guards as G, render_changed as RC

LEDGER_DIR = os.path.join(ROOT, "status", "ship"); BRIEFS = os.path.join(ROOT, ".cache", "ship")
ORIGINALS = {"/ai-landing-page-builder/thank-you-page", "/ai-form-builder/creator-application",
             "/ai-automation-builder/approval-workflow", "/ai-survey-and-quiz-builder/customer-satisfaction"}
AGENT = {"writer", "review", "rework", "images", "cms"}       # stages that wait on someone other than code
MAX_FAILS = 2
def now(): return H.now()

# ---------- ledger
def batch_name(bf): return os.path.splitext(os.path.basename(bf))[0]
def batch_urls(bf): return [l.split("#")[0].strip() for l in open(bf) if l.split("#")[0].strip()]
def lpath(bf): return os.path.join(LEDGER_DIR, batch_name(bf) + ".json")
def load_ledger(bf):
    p = lpath(bf)
    L = json.load(open(p)) if os.path.exists(p) else {"batch": batch_name(bf), "file": os.path.relpath(bf, ROOT), "pages": {}}
    for u in batch_urls(bf): L["pages"].setdefault(u, {"stage": "autofix", "fails": {}, "history": [], "stopped": None})
    return L
def save_ledger(bf, L):
    os.makedirs(LEDGER_DIR, exist_ok=True); json.dump(L, open(lpath(bf), "w"), indent=1, sort_keys=True)
def note(P, stage, ok, msg=""):
    P["history"].append({"t": now(), "stage": stage, "ok": ok, "note": msg[:300]})
def fail(P, stage, msg, back_to):
    P["fails"][stage] = P["fails"].get(stage, 0) + 1; note(P, stage, False, msg)
    if P["fails"][stage] >= MAX_FAILS: P["stopped"] = f"{stage} failed twice: {msg}"[:300]; P["stage"] = "stopped"
    else: P["stage"] = back_to; P["last_fail"] = msg[:500]

# ---------- checks
def spec(url): s = json.load(open(H.spath(url))); s["_path"] = H.spath(url); return s
def qc_issues(url):
    """Strict QC: the originals are checked as normal pages (status 'spec'); everything else as plain QC does."""
    import qc_hub as Q
    every = Q.load_specs(sorted(glob.glob(os.path.join(ROOT, "specs", "*", "*.json"))))
    s = next(x for x in every if x["url"] == url)
    if url in ORIGINALS: s = dict(s, status="spec")
    return [i for i in Q.check(s, every) if i["sev"] in ("P0", "P1")]
def qc_total(url): return len(qc_issues(url))
def paa(url):
    """PAA gate on the spec's FAQ (qc/paa_gate.py, PA1-PA12): (items not rejected, items, page-level problems, flagged items)."""
    import paa_gate as P
    items, page = P.run_spec(P.Gate(url))
    return sum(i["verdict"] != "reject" for i in items), len(items), [r for r, _ in page], [i["n"] for i in items if i["verdict"] == "flag"]
def gate_ok(url):
    ok, n, page, _ = paa(url); return ok == 10 and n == 10 and not page
def chips_ok(s): c = s.get("chip_prompts") or []; return len(c) == 4 and all(isinstance(x, str) and len(x.strip()) > 20 for x in c)
def images_current(s):
    return bool(s.get("image_brief")) and RC.current(s)

# ---------- autofix (deterministic, guarded exactly like ops/autofix.py: kept only if no P0/P1 gets worse)
def autofix(url):
    import autofix as AF, qc_hub as Q
    every = Q.load_specs(sorted(glob.glob(os.path.join(ROOT, "specs", "*", "*.json"))))
    s = next(x for x in every if x["url"] == url); chk = (lambda: Q.check(dict(s, status="spec"), every)) if url in ORIGINALS else (lambda: Q.check(s, every))
    raw = open(s["_path"]).read(); F = s["fields"]; base = AF.blocking(chk()); n = 0
    for name, (gen, _code) in AF.GEN.items():
        for k in list(F):
            if not isinstance(F[k], str) or k in AF.SKIP_FIELDS: continue
            for a, b, cands in sorted(gen(k, F[k]), key=lambda x: -x[0]):
                old = F[k]
                for c in cands:
                    F[k] = old[:a] + c + old[b:]; after = AF.blocking(chk())
                    if not AF.worse(base, after): base = after; n += 1; break
                else: F[k] = old
    if n:
        with open(s["_path"], "w") as fh: fh.write(json.dumps({k: v for k, v in s.items() if k != "_path"}, indent=1, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""))
    return n

# ---------- writer brief (git-ignored: it quotes questions)
def writer_brief(url, P, role="writer"):
    import paa_gate as PG
    s = spec(url); g = PG.Gate(url); items, page = PG.run_spec(g)
    bad = [i for i in items if i["verdict"] == "reject"]
    pull = []
    if os.path.exists(PG.pull_path(g.slug)):
        have = {PG.norm(i["q"]) for i in items}
        pull = [i["q"] for i in PG.run_pull(g)[0] if i["verdict"] == "pass" and PG.norm(i["q"]) not in have]
    secs = (s.get("keywords") or {}).get("secondaries_used") or []
    faqtxt = " ".join(PG.norm(i["q"]) for i in items)
    unused = [k for k in secs if not PG.content(k) <= PG.content(faqtxt)]
    issues = qc_issues(url); slug = url.rsplit("/", 1)[1]
    L = [f"# Launch {role} brief: {url}", "",
         f"Spec: `{os.path.relpath(H.spath(url), ROOT)}`. Read `python3 ops/hubctl.py pack {url} --role writer` first (rules, catalogue, exemplar).",
         "This is ONE combined pass (DECISIONS 2026-10-08). Rules are frozen for launch: never edit rules, QC or shared code. Fix only what this brief lists; leave everything else as it is.", ""]
    if role == "rework":
        L += ["## Blocking review findings (fix these only; notes never trigger edits)", "",
              *[f"- {x}" for x in (load_status_note(url) or "see spec.review.findings (severity blocking)").split(" | ")], ""]
    else:
        L += ["## 1. FAQ items to replace (PAA gate rejects)", ""]
        L += [f"- Q{i['n']}: {i['q']}  (rules: {', '.join(sorted({r[0] for r in i['reasons'] if r[1] == 'reject'}))})" for i in bad] or ["- none"]
        if page: L += ["", "Page-level gate problems: " + "; ".join(f"{r} {m}" for r, m in page)]
        L += ["", "Replacement questions may come ONLY from these sources (no other PAA, no invented questions):",
              "- gate-passing AlsoAsked questions not yet in the FAQ:", *([f"  - {q}" for q in pull] or ["  - none"]),
              "- approved secondaries not yet carried by a question:", *([f"  - {k}" for k in unused] or ["  - none"]),
              "Keep exactly 10 items; item 1 the definition, item 2 how-to-build with the hub link (QC K4). Answers lead with the answer (first words answer the question). "
              "No question may name a brand or product (PA14) or ask for a file format or download (PA15) (Divit 2026-10-09). "
              "Never reuse AlsoAsked answer text (PA1b blocks any 6-word run). Record each new item in faq_sources with its source "
              "(alsoasked with prov, or secondary). Build the FAQ embed in Python so quoting is exact.", ""]
        L += ["## 2. QC issues still open (strict QC; fix the class across the page)", ""]
        L += [f"- {i['sev']} {i['code']} {i['field']}: {i['msg'][:220]}" for i in issues] or ["- none"]
        L += ["", "## 3. Chip prompts for the hero (template edit T1)", "",
              "Write `spec.chip_prompts`: a list of exactly 4 strings, in the order of the chip labels "
              + ", ".join(f'"{s["fields"].get(f"prompt_chip_{i}", "")}"' for i in range(1, 5)) + ". Each is what this page's reader would type into the "
              "builder when they click that chip: first person, one or two sentences, 60-220 characters, specific to the page and the chip, "
              "and consistent with the default prompt (`fields.hero_prompt`, unchanged). Same voice rules as the page (HUB_RULES 2a, 2b; US spelling; serial comma); "
              "no claims beyond rules/capabilities.json.", ""]
        if s["fields"].get("h1") and (s.get("image_brief") or {}).get("og", {}).get("headline") and og_stale(s):
            L += ["## 4. Factual fix: the share image", "", "The share image headline (`image_brief.og.headline`) is an older H1 of this page. "
                  "Rewrite it as a short sentence-case form of the current H1 (max 3 lines at the 480px column; the engine checks it) and update `og.alt` to match.", ""]
    if url in ORIGINALS and role == "writer":
        ref = {"thank-you-page": "lp_thankyou", "creator-application": "form_creators", "approval-workflow": "aab_approvals", "customer-satisfaction": "sqb_csat"}[slug]
        L += ["## 5. This is one of the 4 original pages (Divit, 2026-10-08: brought to the same standard)", "",
              "Slug, primary keyword and H1 intent stay unchanged. Plain `hubctl qc` treats this page as frozen, so use `hubctl ship-qc` as the gate. "
              f"Image brief: start from `pipeline/briefs/{ref}.json` (it rebuilds the page's approved scenes in the engine) and keep each tab's `story` "
              "pairs true to the tab copy you end with. Table: generate it with `hubctl table` from the library (V1/V2). Write `spec.plan` and run "
              "`hubctl plan-check`. If F1 is listed, pull the live SERP first (writer steps 0-1). Remove every claim QC marks C2 (not approved) rather than rewording it.", ""]
    if P.get("last_fail"): L += ["## Previous attempt failed", "", P["last_fail"], ""]
    L += ["## Done when", "",
          f"`python3 ops/hubctl.py ship-qc {url}` prints TOTAL 0 and `python3 ops/hubctl.py paa {url} --spec` reports 10 items with no reject. "
          f"Then `python3 ops/hubctl.py state {url} qc_pass --by <your id>` (for the 4 originals plain QC is frozen, ship-qc is the gate) and return a 3-line summary."]
    os.makedirs(BRIEFS, exist_ok=True); p = os.path.join(BRIEFS, f"{slug}.{role}.md"); open(p, "w").write("\n".join(L) + "\n")
    return os.path.relpath(p, ROOT)
def load_status_note(url): return H.load_st(H.hub_of(url))["pages"].get(url, {}).get("note")
def og_stale(s):
    """The og headline equals an earlier H1 of this page (git history) but not the current one: a stale share image."""
    og = re.sub(r"\W+", " ", s["image_brief"]["og"]["headline"].lower()).strip()
    cur = re.sub(r"\W+", " ", re.sub(r"<[^>]+>", "", s["fields"]["h1"]).lower()).strip()
    if og == cur: return False
    rel = os.path.relpath(s["_path"], ROOT); olds = set()
    for sha in subprocess.run(["git", "log", "--format=%H", "--", rel], cwd=ROOT, capture_output=True, text=True).stdout.split()[:40]:
        try: olds.add(re.sub(r"\W+", " ", re.sub(r"<[^>]+>", "", json.loads(subprocess.run(["git", "show", f"{sha}:{rel}"], cwd=ROOT, capture_output=True, text=True).stdout)["fields"]["h1"]).lower()).strip())
        except Exception: pass
    return og in olds

# ---------- advance
def state_of(url): return H.load_st(H.hub_of(url))["pages"].get(url, {}).get("state")
def advance(url, P, queue):
    """Run code stages until the page waits on an agent, the Action or the orchestrator. Returns the waiting label."""
    for _ in range(12):
        st = P["stage"]
        if st in ("stopped", "done"): return st
        if st == "autofix":
            n = autofix(url); note(P, "autofix", True, f"{n} deterministic edit(s)"); P["stage"] = "writer"; continue
        if st in ("writer", "rework"):
            fresh = P.get("brief_for") == f"{st}:{P['fails'].get('check' if st == 'writer' else 'check2', 0)}"
            if not (fresh and P.get("brief") and os.path.exists(os.path.join(ROOT, P["brief"]))):   # never rewrite a brief an agent is reading
                P["brief"] = writer_brief(url, P, st); P["brief_for"] = f"{st}:{P['fails'].get('check' if st == 'writer' else 'check2', 0)}"
            return st
        if st in ("check", "check2"):
            s = spec(url); probs = []
            t = qc_total(url)
            if t: probs.append(f"QC TOTAL {t}: " + ", ".join(sorted({i['code'] for i in qc_issues(url)})))
            ok, n, page, _ = paa(url)
            if not (ok == 10 and n == 10 and not page): probs.append(f"PAA gate {ok}/{n}" + (f" ({', '.join(page)})" if page else ""))
            if not chips_ok(s): probs.append("chip_prompts missing or not 4")
            if probs: fail(P, st, "; ".join(probs), "writer" if st == "check" else "rework"); continue
            note(P, st, True, "QC 0, PAA 10/10, chips"); P["stage"] = "images" if st == "check" else "images2"; continue
        if st in ("images", "images2"):
            s = spec(url)
            if not images_current(s):
                queue.add(url.rsplit("/", 1)[1]); return "images"
            if state_of(url) != "images":   # hubctl review and hubctl ready both need state images
                H.set_state(url, "images", note="launch: QC 0, PAA 10/10, images current", via="ship")
            note(P, st, True, "images current")
            if st == "images": P["stage"] = "review"; return "review"
            P["stage"] = "ready"; continue
        if st == "review": return "review"
        if st == "ready":
            r = subprocess.run([sys.executable, os.path.join(ROOT, "ops", "hubctl.py"), "ready", url, "--by", P.get("rework_by", "orchestrator")], capture_output=True, text=True)
            if r.returncode: fail(P, "ready", r.stdout[-300:] + r.stderr[-300:], "rework"); continue
            note(P, "ready", True); P["stage"] = "payload"; continue
        if st == "payload": return "payload"
        if st == "cms": return "cms"
    return P["stage"]

def cmd_ship(args):
    bf = args[0]; L = load_ledger(bf); queue = set(); waits = Counter(); lines = []
    for url in batch_urls(bf):
        P = L["pages"][url]
        try: w = advance(url, P, queue)
        except SystemExit as e: fail(P, P["stage"], f"error: {e}", P["stage"]); w = P["stage"]
        except Exception as e: fail(P, P["stage"], f"{type(e).__name__}: {e}", P["stage"]); w = P["stage"]
        waits[w] += 1; lines.append(f"  {w:8s} {url}" + (f"  [{P['stopped']}]" if P.get("stopped") else "") + (f"  brief {P.get('brief')}" if w in ("writer", "rework") else ""))
        save_ledger(bf, L)
    if queue:
        q = os.path.join(ROOT, "status", "render-queue.txt"); have = set(l.strip() for l in open(q)) if os.path.exists(q) else set()
        open(q, "w").write("".join(x + "\n" for x in sorted(have | queue)))
    if "--payload" in args: build_payloads(bf, L, args[args.index("--payload") + 1])
    save_ledger(bf, L); write_readiness()
    print("\n".join(lines)); print("waiting:", dict(waits) | ({"render-queue": len(queue)} if queue else {}))

def cmd_done(args):
    bf, url, stage = args[0], args[1], args[2]; by = args[args.index("--by") + 1] if "--by" in args else None
    L = load_ledger(bf); P = L["pages"][url]
    if "--fail" in args: fail(P, stage, args[args.index("--fail") + 1], stage); save_ledger(bf, L); print(f"{url}: {stage} failed ({P['fails'][stage]}x)"); return
    if stage == "writer": P["writer_by"] = by; P["stage"] = "check"
    elif stage == "rework": P["rework_by"] = by; P["stage"] = "check2"
    elif stage == "review":
        stt = state_of(url); P["reviewer_by"] = by
        if stt == "reviewed": P["stage"] = "payload"
        elif stt == "rework": P["stage"] = "rework"
        else: sys.exit(f"{url}: review not recorded (state {stt}); run hubctl review first")
    else: sys.exit("stage must be writer, review or rework")
    note(P, stage, True, f"by {by}"); save_ledger(bf, L); print(f"{url}: {stage} done -> {P['stage']}")

# ---------- payloads and CMS
def build_payloads(bf, L, sha):
    """One data_cms_tool action list per collection: updates for pages with an item, creates for new slugs (after cms-check)."""
    out = {}; os.makedirs(os.path.join(ROOT, "ops", "out", "ship"), exist_ok=True)
    for url in batch_urls(bf):
        P = L["pages"][url]
        if P["stage"] != "payload": continue
        hub = H.hub_of(url); h = H.CFG["hubs"][hub]; s, fd = H._field_data(url, sha)
        e = H.load_st(hub)["pages"].get(url, {})
        if not s.get("item_id"):
            if e.get("cms_exists"): fail(P, "payload", f"slug already in Webflow ({e.get('cms_item_id')}); record it first", "payload"); continue
            chk = e.get("cms_checked")
            if not chk or (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.strptime(chk, "%Y-%m-%d %H:%M UTC").replace(tzinfo=datetime.timezone.utc)).total_seconds() > 3600:
                print(f"  HOLD {url}: no slug check in the last hour (hubctl cms-check {hub} <readback>)"); continue
            out.setdefault((hub, "create"), []).append({"isDraft": True, "fieldData": fd})
        else:
            out.setdefault((hub, "update"), []).append({"id": s["item_id"], "isDraft": True, "fieldData": fd})
        P["payload_sha"] = sha; P["payload_fp"] = G.fingerprint(s); P["stage"] = "cms"; note(P, "payload", True, f"{'update' if s.get('item_id') else 'create'} at {sha[:7]}")
    for (hub, kind), items in out.items():
        h = H.CFG["hubs"][hub]
        for i in range(0, len(items), 25):
            chunk = items[i:i + 25]; key = "update_collection_items" if kind == "update" else "create_collection_items"
            p = os.path.join(ROOT, "ops", "out", "ship", f"{L['batch']}-{h['repo_dir']}-{kind}-{i // 25 + 1}.json")
            slugs = [it["fieldData"]["slug"] for it in chunk]
            json.dump([{"label": f"{kind} {hub} {L['batch']} {i + 1}-{i + len(chunk)}", key: {"collection_id": h["collection_id"], "request": {"items": chunk}}},
                       {"label": "read back", "list_collection_items": {"collection_id": h["collection_id"], "request": {"filter": {"slug": {"in": slugs}}, "limit": 100}}}],
                      open(p, "w"), indent=1, ensure_ascii=False)
            print(f"  wrote {os.path.relpath(p, ROOT)}: {len(chunk)} {kind}(s) + read-back")

def cmd_cms(args):
    """Verify a stored read-back against the specs for every page waiting in stage cms; record item and file IDs and the draft fingerprint."""
    bf, rb = args[0], args[1]; L = load_ledger(bf); items = H._items_from_readback(rb); ok = bad = 0
    by = {(it.get("fieldData") or {}).get("slug"): it for it in items}
    for url in batch_urls(bf):
        P = L["pages"][url]
        if P["stage"] != "cms": continue
        it = by.get(url.rsplit("/", 1)[1])
        if not it: continue
        hub = H.hub_of(url); h = H.CFG["hubs"][hub]; s = json.load(open(H.spath(url))); fd = it["fieldData"]; diff = []
        for k, v in H.export_fields(url, s)[0].items():
            if v in (None, "") and k in H.CFG["optional_fields"]: continue
            if fd.get(h["fields"][k]) != v: diff.append(k)
        for k, im in s["images"].items():
            got = fd.get(h["fields"][k]) or {}
            if not got.get("fileId"): diff.append(f"{k} (no fileId)")
            else: im["file_id"] = got["fileId"]; im["cdn_url"] = got.get("url")
        if not it.get("isDraft"): diff.append("isDraft is not true")
        if diff: bad += 1; fail(P, "cms", "read-back mismatch: " + ", ".join(diff), "payload"); print(f"MISMATCH {url}: {diff}"); continue
        s["item_id"] = it["id"]; s["cms_draft"] = {"fingerprint": G.fingerprint(s), "sha": P.get("payload_sha"), "date": now(), "verified": True}
        json.dump(s, open(H.spath(url), "w"), indent=1, ensure_ascii=False)
        P["stage"] = "done"; P["item_id"] = it["id"]; note(P, "cms", True, f"draft {it['id']} verified"); ok += 1
    save_ledger(bf, L); write_readiness(); print(f"drafts verified {ok}; mismatched {bad}")

def cmd_qc(args):
    url = args[0]; iss = qc_issues(url)
    for i in iss: print(f"  {i['sev']} {i['code']} {i['field']}: {i['msg'][:200]}")
    print(f"TOTAL (P0+P1) = {len(iss)}"); sys.exit(1 if iss else 0)

def cmd_cost(args):
    bf = args[0]; urls = set(batch_urls(bf)); per = {}
    for l in open(G.usage_path()):
        r = json.loads(l)
        if r["url"] in urls and r.get("agent", "").startswith("launch"): per.setdefault(r["url"], Counter())[r["role"]] += r["tokens"]
    for u in sorted(per): print(f"  {u}: " + ", ".join(f"{k} {v}" for k, v in per[u].items()))
    for role in ("writer", "reviewer"):
        v = [c[role] for c in per.values() if c.get(role)]
        if v: print(f"{role}: {len(v)} pages, mean {sum(v) // len(v)} tokens/page, total {sum(v)}")

# ---------- readiness board (public: counts and IDs only)
def write_readiness():
    T = json.load(open(os.path.join(ROOT, "plan", "template-status.json")))
    ledgers = {}
    for p in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.json"))):
        L = json.load(open(p))
        for u, P in L["pages"].items(): ledgers[u] = (L["batch"], P)
    st = G.all_status(); rows = []
    for u in sorted(ledgers, key=lambda x: (ledgers[x][0], list(json.load(open(os.path.join(LEDGER_DIR, ledgers[x][0] + ".json")))["pages"]).index(x))):
        b, P = ledgers[u]
        try: s = spec(u)
        except FileNotFoundError: continue
        ok, n, page, flags = paa(u)
        rv = s.get("review") or {}
        launch_rev = bool(P.get("reviewer_by")) and rv.get("by") == P.get("reviewer_by")
        cd = s.get("cms_draft") or {}; synced = bool(cd) and cd.get("fingerprint") == G.fingerprint(s)
        rows.append([b, u, str(qc_total(u)), f"{ok}/{n}", ("yes, " + rv.get("by", "")) if launch_rev else "no",
                     "yes" if images_current(s) else "no", "yes" if (s.get("pa13") or {}).get("approved") else "no",
                     str(len(s.get("pending_links") or [])), s.get("item_id") or "-", "yes" if synced else "no",
                     "yes" if st.get(u, {}).get("state") == "published" else "no", P["stage"] + (" (stopped)" if P.get("stopped") else "")])
    out = ["# Readiness board", "", f"Regenerated {now()} by `hubctl readiness` (also after every `hubctl ship` step). Public: counts and IDs only.", "",
           "## Template blockers (plan/template-edits-2026-10-08.md)", "", "| # | Edit | Blocks first publish | Status |", "|---|---|---|---|"]
    out += [f"| {k} | {v['edit']} | {v['blocks']} | {v['status']} |" for k, v in T.items() if not k.startswith("_")]
    hdr = ["Batch", "Page", "QC TOTAL", "PAA gate", "Review (launch)", "Images current", "PA13 approved", "Pending links", "CMS item", "Draft synced", "Published", "Ship stage"]
    out += ["", "## Pages", "", "| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)] + ["| " + " | ".join(r) + " |" for r in rows]
    c = Counter(r[-1].split(" ")[0] for r in rows)
    out += ["", "Stages: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())) + f" ({len(rows)} pages)"]
    open(os.path.join(ROOT, "status", "readiness.md"), "w").write("\n".join(out) + "\n")
def cmd_readiness(args): write_readiness(); print("wrote status/readiness.md")

CMDS = {"ship": cmd_ship, "ship-done": cmd_done, "ship-cms": cmd_cms, "ship-qc": cmd_qc, "ship-cost": cmd_cost, "readiness": cmd_readiness}
