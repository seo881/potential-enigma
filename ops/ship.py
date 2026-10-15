"""ship.py: the launch pipeline, page by page (Divit, 2026-10-08 LAUNCH RUN, Part 3.3). Called through hubctl.

  hubctl ship BATCH_FILE                  advance every page of the batch as far as code can take it; print what waits on whom
  hubctl ship-done BATCH_FILE URL STAGE --by ID [--fail TEXT]   an agent finished a stage (writer | review | rework)
  hubctl ship-cms BATCH_FILE READBACK.json [--learn LEARN.json]   after the orchestrator's create/update call: verify the read-back, record the drafts
  hubctl ship-qc URL                      QC as a normal page (the 4 originals are frozen in plain QC; launch brings them to standard)
  hubctl ship-update BATCH READBACK [--before-only]   changed fields only for pages already in the CMS (before-values committed first; status kept)
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
              "The explore CTA is at most 34 characters (QC D3; shorten the display name). "
              "In 2-3 general answers (items 3-10) add one subtle sentence on the question-specific Emergent moat, approved claims only, no hard sell, no competitor names (QC F9). "
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
        qb = H.quiz_ship_block(url, json.load(open(H.spath(url))))
        if qb: print(f"  HOLD {url}: {qb}"); continue
        hub = H.hub_of(url); h = H.CFG["hubs"][hub]; s, fd = H._field_data(url, sha)
        e0 = H.load_st(H.hub_of(url))["pages"].get(url, {})   # ruling 6: only reviewed pages, never over the other account's hold
        if not s.get("item_id") and e0.get("state") not in ("reviewed", "approved"): print(f"  REFUSED {url}: state {e0.get('state')}, not reviewed"); continue
        if e0.get("hold") and H.hold_account(e0["hold"]) != H.clone_account(): print(f"  REFUSED {url}: held by account {H.hold_account(e0['hold'])}"); continue
        ok_r, why_r = G.review_ok(s)   # ruling 1 (Divit 2026-10-13): only reviewed text ships
        if not ok_r: print(f"  REFUSED {url}: {why_r}"); continue
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
    learn = H.learn_index(_arg(args, "--learn")) if "--learn" in args else None
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
        diff += H.learn_problems(hub, it, learn)   # Divit 2026-10-16: 3 published Learn refs
        if diff: bad += 1; fail(P, "cms", "read-back mismatch: " + ", ".join(diff), "payload"); print(f"MISMATCH {url}: {diff}"); continue
        s["item_id"] = it["id"]; s["cms_draft"] = {"fingerprint": G.fingerprint(s), "sha": P.get("payload_sha"), "date": now(), "verified": True}
        json.dump(s, open(H.spath(url), "w"), indent=1, ensure_ascii=False)
        P["stage"] = "done"; P["item_id"] = it["id"]; note(P, "cms", True, f"draft {it['id']} verified"); ok += 1
    save_ledger(bf, L); write_readiness(); print(f"drafts verified {ok}; mismatched {bad}. {H.learn_note(learn)}")

def cmd_update(args):
    """hubctl ship-update BATCH READBACK [--before-only]: changed fields only, for batch pages already in the CMS (staged or draft).
    Diffs each page's export against a fresh read-back; saves the CMS before-values to childedits/<date>/<slug>.<batch>.before.json
    and refuses to write the payload until those files are committed and pushed (Divit 2026-10-10). Image fields go only when the
    file changed since the create commit (spec.cms_draft.sha) or the alt changed. isDraft is omitted, so the item's status is kept."""
    import live_audit as LA
    bf, rb = args[0], args[1]; L = load_ledger(bf); name = L["batch"]; items = {it["id"]: it for it in H._items_from_readback(rb)}
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    day = datetime.date.today().isoformat(); out = {}; befores = []; changed_pages = []
    if "--verify" in args: return update_verify(bf, name, items, day, H.learn_index(_arg(args, "--learn")) if "--learn" in args else None)
    for url in batch_urls(bf):
        s = spec(url); h = H.CFG["hubs"][H.hub_of(url)]; it = items.get(s.get("item_id"))
        if not it: sys.exit(f"{url}: item {s.get('item_id')} not in {rb}")
        fd = it["fieldData"]; ex = H.export_fields(url, s)[0]; ch = {}
        for k, v in ex.items():
            if k == "slug" or (v in (None, "") and k in H.CFG["optional_fields"]): continue
            if fd.get(h["fields"][k]) != v: ch[h["fields"][k]] = v
        base = (s.get("cms_draft") or {}).get("sha")
        for k, im in s["images"].items():
            cur = fd.get(h["fields"][k]) or {}
            moved = base and subprocess.run(["git", "diff", "--quiet", base, "HEAD", "--", im["path"]], cwd=ROOT).returncode != 0
            if moved: ch[h["fields"][k]] = {"url": f"{H.REPO_RAW}/{sha}/{im['path']}", "alt": im["alt"]}
            elif (im.get("alt") or "") != (cur.get("alt") or ""): ch[h["fields"][k]] = {"fileId": cur.get("fileId"), "url": cur.get("url"), "alt": im["alt"]}
        if not ch: continue
        if "slug" in ch: sys.exit(f"{url}: slug would change")
        bp = os.path.join(ROOT, "childedits", day, f"{url.rsplit('/', 1)[1]}.{name}.before.json")
        before = {"id": it["id"], "collection": h["collection_id"], "isDraft": it.get("isDraft"), "lastUpdated": it.get("lastUpdated"), "fieldData": {k: fd.get(k) for k in ch}}
        if not os.path.exists(bp) or json.load(open(bp)) != before:
            os.makedirs(os.path.dirname(bp), exist_ok=True); json.dump(before, open(bp, "w"), indent=1, ensure_ascii=False)
        befores.append(bp); changed_pages.append((url, sorted(ch)))
        out.setdefault(h["collection_id"], []).append({"id": it["id"], "fieldData": ch})
    for url, keys in changed_pages: print(f"  {url}: {len(keys)} field(s): {', '.join(keys)}")
    if "--before-only" in args: print(f"{len(befores)} before-value file(s) written; commit and push them, then rerun without --before-only"); return
    bad = [os.path.relpath(b, ROOT) + ": " + LA.before_committed(b)[1] for b in befores if not LA.before_committed(b)[0]]
    if bad: sys.exit("before-values not committed and pushed:\n  " + "\n  ".join(bad))
    if subprocess.run(["git", "status", "-sb"], cwd=ROOT, capture_output=True, text=True).stdout.splitlines()[0].find("ahead") >= 0: sys.exit("push first: image URLs are pinned to a pushed commit")
    os.makedirs(os.path.join(ROOT, "ops", "out", "ship"), exist_ok=True)
    for cid, its in out.items():
        p = os.path.join(ROOT, "ops", "out", "ship", f"{name}-update-{cid}.json")
        json.dump([{"label": f"update {name}: {len(its)} item(s), changed fields only, status kept", "update_collection_items": {"collection_id": cid, "request": {"items": its}}}], open(p, "w"), indent=1, ensure_ascii=False)
        print(f"  wrote {os.path.relpath(p, ROOT)}: {len(its)} item(s)")

def relink_plan(items, live, specs=None, targets=None, day=None, write=True):
    """The relink plan behind relink-payload and the automatic relink after api-publish: for live pages whose pending links now
    point at live pages (only `targets` when given), the fields whose CMS value differs from the export by exactly the restored
    <a> tags (anything else in the field is drift and is refused). Returns (upd, pub, befores, refused, rows); before-values go to
    childedits/<date>/<slug>.relink.before.json (write=False: nothing written)."""
    import guards as G
    day = day or datetime.date.today().isoformat(); upd = {}; pub = {}; befores = []; refused = []; rows = []
    for s in (G.all_specs() if specs is None else specs):
        url = s["url"]; ready = sorted({p["target"] for p in s.get("pending_links") or [] if p["target"] in live and (targets is None or p["target"] in targets)})
        if not ready or url not in live: continue
        it = items.get(s.get("item_id"))
        if not it: refused.append(f"{url}: item {s.get('item_id')} not in the read-back"); continue
        h = H.CFG["hubs"][H.hub_of(url)]; fd = it["fieldData"]; ex = H.export_fields(url, {k: v for k, v in s.items() if k != "_path"}, live)[0]; ch = {}
        for k, v in ex.items():
            cur = fd.get(h["fields"][k])
            if k == "slug" or cur == v or not isinstance(v, str) or not isinstance(cur, str): continue
            strip = lambda t: re.sub(r"<a href=(\\?[\"'])https://emergent\.sh(" + "|".join(map(re.escape, ready)) + r")/?\1[^>]*>(.*?)</a>", r"\3", t)
            if strip(v) == strip(cur): ch[h["fields"][k]] = v
            else: refused.append(f"{url}: {h['fields'][k]} differs by more than the restored links (drift; not sent)")
        if not ch: continue
        bp = os.path.join(ROOT, "childedits", day, f"{url.rsplit('/', 1)[1]}.relink.before.json")
        before = {"id": it["id"], "collection": h["collection_id"], "isDraft": it.get("isDraft"), "lastPublished": it.get("lastPublished"), "fieldData": {k: fd.get(k) for k in ch}}
        if write and (not os.path.exists(bp) or json.load(open(bp)) != before):
            os.makedirs(os.path.dirname(bp), exist_ok=True); json.dump(before, open(bp, "w"), indent=1, ensure_ascii=False)
        befores.append(bp); upd.setdefault(h["collection_id"], []).append({"id": it["id"], "fieldData": ch}); pub.setdefault(h["collection_id"], []).append({"id": it["id"]})
        rows.append((url, sorted(ch), ready))
    return upd, pub, befores, refused, rows

def relink_actions(upd, pub):
    acts = [{"label": f"relink: {len(v)} item(s), changed fields only, status kept", "update_collection_items": {"collection_id": c, "request": {"items": v}}} for c, v in upd.items()]
    return acts + [{"label": f"relink: item publish {len(v)} item(s)", "publish_collection_items": {"collection_id": c, "request": {"items": v}}} for c, v in pub.items()]

def cmd_relink(args):
    """hubctl relink-payload READBACK [--before-only] [--targets URL,URL]: for live pages whose pending links now point at live pages
    (hubctl links --relink), send only the fields whose CMS value differs from the export by exactly the restored <a> tags (anything
    else in the field is drift and is refused). Before-values go to childedits/<date>/<slug>.relink.before.json and must be committed
    and pushed first; the payload is update_collection_items (status kept) plus publish_collection_items for exactly those items.
    api-publish --live --verify-live runs this itself for the pages it just published (auto relink)."""
    import live_audit as LA
    rb = args[0]; items = {it["id"]: it for it in H._items_from_readback(rb)}; day = datetime.date.today().isoformat()
    tg = set(_arg(args, "--targets").split(",")) if _arg(args, "--targets") else None
    upd, pub, befores, refused, rows = relink_plan(items, H.live_urls(), targets=tg, day=day)
    for url, ch, ready in rows: print(f"  {url}: {', '.join(ch)} (links to {', '.join(ready)})")
    for r in refused: print("  REFUSED " + r)
    if "--before-only" in args: print(f"{len(befores)} before-value file(s); commit and push them, then rerun without --before-only"); return
    bad = [os.path.relpath(b, ROOT) + ": " + LA.before_committed(b)[1] for b in befores if not LA.before_committed(b)[0]]
    if bad: sys.exit("before-values not committed and pushed:\n  " + "\n  ".join(bad))
    p = os.path.join(ROOT, "ops", "out", "ship", f"relink-{day}.json")
    os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(relink_actions(upd, pub), open(p, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {os.path.relpath(p, ROOT)}: {sum(len(v) for v in upd.values())} item(s)")

def update_verify(bf, name, items, day, learn=None):
    """ship-update ... --verify: after the update, every text field and alt matches the read-back, and every image field sent
    (from the payloads in ops/out/ship) now holds a different CDN file than its committed before-value. On a pass, cms_draft.sha
    moves to the payload commit so the next ship-update compares images from there."""
    sent = {}
    for p in glob.glob(os.path.join(ROOT, "ops", "out", "ship", f"{name}-update-*.json")):
        for it in json.load(open(p))[0]["update_collection_items"]["request"]["items"]: sent[it["id"]] = it["fieldData"]
    bad = []; ok = 0; psha = None
    for url in batch_urls(bf):
        s = spec(url); h = H.CFG["hubs"][H.hub_of(url)]; it = items.get(s.get("item_id"))
        if not it: bad.append(f"{url}: item not in read-back"); continue
        fd = it["fieldData"]; ex = H.export_fields(url, s)[0]
        for k, v in ex.items():
            if k == "slug" or (v in (None, "") and k in H.CFG["optional_fields"]): continue
            if fd.get(h["fields"][k]) != v: bad.append(f"{url}: {h['fields'][k]} differs")
        for k, im in s["images"].items():
            if (im.get("alt") or "") != ((fd.get(h["fields"][k]) or {}).get("alt") or ""): bad.append(f"{url}: {h['fields'][k]} alt differs")
        bad += [f"{url}: {p}" for p in H.learn_problems(H.hub_of(url), it, learn)]   # Divit 2026-10-16
        bp = os.path.join(ROOT, "childedits", day, f"{url.rsplit('/', 1)[1]}.{name}.before.json")
        for f, v in (sent.get(it["id"]) or {}).items():
            if not (isinstance(v, dict) and "/potential-enigma/" in (v.get("url") or "")): continue
            psha = v["url"].split("/potential-enigma/")[1].split("/")[0]
            old = ((json.load(open(bp))["fieldData"].get(f) if os.path.exists(bp) else None) or {}).get("fileId")
            if not (fd.get(f) or {}).get("fileId") or fd[f]["fileId"] == old: bad.append(f"{url}: {f} still the old file")
        ok += 1
    for b in bad: print("  MISMATCH " + b)
    print(f"{ok - len({b.split(':')[0] for b in bad})}/{ok} pages match the read-back. {H.learn_note(learn)}")
    if bad: sys.exit(1)
    for url in batch_urls(bf):
        s = json.load(open(H.spath(url))); it = items[s["item_id"]]; h = H.CFG["hubs"][H.hub_of(url)]
        for k, im in s["images"].items():
            got = it["fieldData"].get(h["fields"][k]) or {}
            if got.get("fileId"): im["file_id"] = got["fileId"]; im["cdn_url"] = got.get("url")
        cd = s.get("cms_draft") or {}
        s["cms_draft"] = {**cd, "fingerprint": G.fingerprint(s), "sha": psha if it["id"] in sent and psha else cd.get("sha"), "date": now(), "verified": True}
        json.dump(s, open(H.spath(url), "w"), indent=1, ensure_ascii=False)
    print(f"cms_draft refreshed on {ok} page(s); image base sha {psha[:8] if psha else 'unchanged'} on {len(sent)}")

def cmd_qc(args):
    url = args[0]; iss = qc_issues(url)
    for i in iss: print(f"  {i['sev']} {i['code']} {i['field']}: {i['msg'][:200]}")
    print(f"TOTAL (P0+P1) = {len(iss)}"); sys.exit(1 if iss else 0)

def cmd_cost(args):
    bf = args[0]; urls = set(batch_urls(bf)); per = {}
    for r in G.usage_rows():
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
    st = G.all_status(); live = G.live_child_urls(); rows = []
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
                     "yes" if u in live else "no", P["stage"] + (" (stopped)" if P.get("stopped") else "")])
    out = ["# Readiness board", "", f"Regenerated {now()} by `hubctl readiness` (also after every `hubctl ship` step). Public: counts and IDs only.", "",
           "## Template blockers (plan/template-edits-2026-10-08.md)", "", "| # | Edit | Blocks first publish | Status |", "|---|---|---|---|"]
    out += [f"| {k} | {v['edit']} | {v['blocks']} | {v['status']} |" for k, v in T.items() if not k.startswith("_")]
    hdr = ["Batch", "Page", "QC TOTAL", "PAA gate", "Review (launch)", "Images current", "PA13 approved", "Pending links", "CMS item", "Draft synced", "Published", "Ship stage"]
    out += ["", "## Pages", "", "| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)] + ["| " + " | ".join(r) + " |" for r in rows]
    c = Counter(r[-1].split(" ")[0] for r in rows)
    out += ["", "Stages: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())) + f" ({len(rows)} pages)"]
    open(os.path.join(ROOT, "status", "readiness.md"), "w").write("\n".join(out) + "\n")
def cmd_readiness(args): write_readiness(); print("wrote status/readiness.md")

# ---------- direct Webflow Data API v2 (Divit 2026-10-14): CMS item writes from the next batch on go through ops/webflow_api.py,
# not the connector. Dry run is the default; --live is required for every network write. Before-values are committed and pushed
# before every write; every write is read back and diffed against the spec; rollback files go to childedits/<date>/; one JSON line
# per request goes to logs/api/<date>.jsonl and one line per write to logs/<dir>.md. The token never reaches any output.
RB_DIR = os.path.join(ROOT, ".cache", "readback")
def _W():
    import webflow_api as W; return W
def _arg(args, k, d=None): return args[args.index(k) + 1] if k in args and args.index(k) + 1 < len(args) else d
def _mode(args):
    live, dry, bo = "--live" in args, "--dry-run" in args, "--before-only" in args
    if live + dry + bo > 1: sys.exit("choose one of --dry-run (the default), --before-only, --live")
    return "live" if live else "before" if bo else "dry"
def _stamp(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
def _day(): return datetime.date.today().isoformat()
def _hub(args):
    if not args or args[0] not in H.CFG["hubs"]: sys.exit(f"HUB must be one of {', '.join(H.CFG['hubs'])}")
    return args[0], H.CFG["hubs"][args[0]]
def _apilog(rec):
    p = os.path.join(ROOT, "logs", "api", f"{_day()}.jsonl"); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a") as f: f.write(json.dumps({"t": now(), **rec}, ensure_ascii=False) + "\n")
def _hublog(hub, text):
    with open(os.path.join(ROOT, "logs", f"{H.CFG['hubs'][hub]['repo_dir']}.md"), "a") as f: f.write(f"- {now()}: {text}\n")
def _rel(p): return os.path.relpath(p, ROOT)
def _pushed(sha):
    """sha is on origin/main (image URLs are pinned to it; Webflow fetches them from GitHub)."""
    subprocess.run(["git", "fetch", "-q", "origin", "main"], cwd=ROOT, capture_output=True)
    return subprocess.run(["git", "merge-base", "--is-ancestor", sha, "origin/main"], cwd=ROOT, capture_output=True).returncode == 0
def require_before(paths):
    """The before-value gate shared by every API write: each file exists, is committed, unchanged since, and pushed. Returns failures."""
    import live_audit as LA
    out = []
    for b in paths:
        if not os.path.exists(b): out.append(f"{_rel(b)}: missing"); continue
        ok, why = LA.before_committed(b)
        if not ok: out.append(f"{_rel(b)}: {why}")
    return out

def api_read(hub, out=None):
    """Full paginated read of a child collection (staged, drafts included) to .cache/readback/ in the read-back shape every
    hubctl command parses (cms-check, bulk-verify, ship-update, relink-payload)."""
    W = _W(); h = H.CFG["hubs"][hub]; items, _ = W.list_items(h["collection_id"], dry=False)
    p = out or os.path.join(RB_DIR, f"{h['repo_dir']}-api-{_stamp()}.json")
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    json.dump({"_meta": {"hub": hub, "collection": h["collection_id"], "read_at": now(), "count": len(items), "via": "hubctl api-read (Data API v2, staged)"},
               "result": {"items": items}}, open(p, "w"), ensure_ascii=False)
    _apilog({"op": "list", "hub": hub, "collection": h["collection_id"], "count": len(items), "file": _rel(p) if p.startswith(ROOT) else os.path.basename(p)})
    G.live_record(hub, items, json.load(open(p))["_meta"]["read_at"], os.path.basename(p))   # Webflow publish state -> status/live.json (Divit 2026-10-15)
    return items, p
def api_read_learn(out=None):
    """Read the Learn collection (GET list only; the client refuses every other request on it) to .cache/readback/learn-api-<time>.json,
    in the read-back shape learn-check, bulk-verify --learn and ship-cms --learn read (Divit 2026-10-16)."""
    W = _W(); items, _ = W.list_learn(dry=False)
    p = out or os.path.join(RB_DIR, f"learn-api-{_stamp()}.json"); os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    json.dump({"_meta": {"collection": W.LEARN, "read_at": now(), "count": len(items), "via": "hubctl api-read-learn (Data API v2, staged, read only)"},
               "result": {"items": items}}, open(p, "w"), ensure_ascii=False)
    _apilog({"op": "list", "hub": "Learn", "collection": W.LEARN, "count": len(items), "file": _rel(p) if p.startswith(ROOT) else os.path.basename(p)})
    return items, p
def _learn_live():
    """{id: item} from a fresh Learn read for the read-back checks of a live write, or None (count only) if the read fails."""
    W = _W()
    try: items, p = api_read_learn(); return {i["id"]: i for i in items}
    except (W.ApiError, W.Refused) as e: print(f"  Learn read failed ({str(e)[:120]}): Learn refs checked by count only"); return None
def cmd_api_read_learn(args):
    """hubctl api-read-learn [--out FILE]: the Learn collection to disk (read only); prints the count and the file."""
    items, p = api_read_learn(_arg(args, "--out"))
    print(f"Learn: {len(items)} item(s) read (staged, drafts included) -> {_rel(p) if os.path.abspath(p).startswith(ROOT) else p}")

def latest_readback(hub):
    fs = sorted(glob.glob(os.path.join(RB_DIR, f"{H.CFG['hubs'][hub]['repo_dir']}-api-*.json")))
    return fs[-1] if fs else None
def cmd_api_read(args):
    """hubctl api-read HUB [--out FILE]: read the whole collection to disk; prints the item count and the file only."""
    hub, _h = _hub(args); items, p = api_read(hub, _arg(args, "--out"))
    print(f"{hub}: {len(items)} item(s) read (staged, drafts included) -> {_rel(p) if os.path.abspath(p).startswith(ROOT) else p}")

def plan_create(cands, live_items, limit=None):
    """(to_create, skipped): never a slug that already exists in the collection (idempotent re-runs); duplicate slugs refused."""
    live = {(it.get("fieldData") or {}).get("slug"): it.get("id") for it in live_items}; seen = set(); go, skip = [], []
    for url, it in cands:
        sl = it["fieldData"]["slug"]
        if sl in seen: sys.exit(f"refused: slug {sl} twice in the create list")
        seen.add(sl)
        (skip.append((url, live[sl])) if sl in live else go.append((url, it)))
    return (go[:limit] if limit is not None else go), skip

def cmd_api_create(args):
    """hubctl api-create HUB --sha SHA [--limit N] [--readback FILE] [--dry-run | --before-only | --live]
    The bulk-payload list (approved, no item ID, review hash current, approval fingerprint, slug check within the hour). --before-only
    reads the live collection and writes the before-value (the slugs to create, absent in that read) to childedits/<date>/; commit and
    push it. --live re-reads the collection, skips every slug that exists, POSTs drafts in batches of 100 (429: Retry-After/backoff),
    writes the rollback file (IDs created) after each batch, reads the collection back and runs bulk-verify on the batch (state cms_draft)."""
    W = _W(); hub, h = _hub(args); mode = _mode(args); sha = _arg(args, "--sha"); cid = h["collection_id"]
    if not sha: sys.exit("--sha SHA required (the pushed commit the image URLs are pinned to)")
    lim = int(_arg(args, "--limit")) if "--limit" in args else None
    cands = H._create_candidates(hub, sha); held = []
    for url, _it in list(cands):
        e = H.load_st(hub)["pages"].get(url, {})
        if e.get("hold") and H.hold_account(e["hold"]) != H.clone_account(): held.append(url)
    cands = [c for c in cands if c[0] not in held]
    for u in held: print(f"  REFUSED {u}: held by the other account")
    if not cands: sys.exit("no approved pages without an item ID")
    if mode == "dry":
        rb = _arg(args, "--readback") or latest_readback(hub)
        live_items = H._items_from_readback(rb) if rb else []
        src = f"stored read-back {os.path.basename(rb)} ({len(live_items)} items)" if rb else "no stored read-back (the live run re-reads the collection)"
    else:
        live_items, rb = api_read(hub); src = f"live read {os.path.basename(rb)} ({len(live_items)} items)"
    go, skip = plan_create(cands, live_items, lim)
    slug_url = {it["fieldData"]["slug"]: u for u, it in go}
    bp = os.path.join(ROOT, "childedits", _day(), f"{h['repo_dir']}.api-create.{sha[:7]}.before.json")
    for u, iid in skip: print(f"  SKIP {u}: slug already in Webflow as {iid} (never created twice)")
    if mode == "dry":
        print(f"DRY RUN api-create {hub}: {len(go)} draft(s) to create, {len(skip)} skipped; slug check against {src}")
        for r, ch in zip(W.create_items(cid, [it for _, it in go], dry=True), W.chunks(go)):
            print(f"  {r['method']} {r['path']}  {r['count']} item(s), isDraft true: {', '.join(it['fieldData']['slug'] for _, it in ch)}")
        print(f"  then GET /collections/{cid}/items (full read-back, {max(1, -(-(len(live_items) + len(go)) // 100))} call(s)), bulk-verify, state cms_draft")
        if H.learn_from_item(hub): print(f"  and GET /collections/{W.LEARN}/items (Learn, read only): every draft needs exactly 3 published acrm---learn refs (Divit 2026-10-16)")
        print(f"  before-value {_rel(bp)}: " + ("present" if os.path.exists(bp) else "not written yet (--before-only)") + ". Nothing was sent.")
        return
    if not go: print("nothing to create: every slug already exists (run hubctl bulk-verify on a read-back to record them)"); return
    before = {"op": "create", "hub": hub, "collection": cid, "sha": sha, "read": {"file": os.path.basename(rb), "items": len(live_items)},
              "slugs_absent": sorted(slug_url), "note": "these slugs were absent from the collection when read; the write creates them as drafts"}
    if mode == "before":
        cur = json.load(open(bp)) if os.path.exists(bp) else None
        if not cur or cur.get("slugs_absent") != before["slugs_absent"] or cur.get("collection") != cid:
            os.makedirs(os.path.dirname(bp), exist_ok=True); json.dump(before, open(bp, "w"), indent=1)
        print(f"before-value {_rel(bp)}: {len(go)} slug(s) absent in {src}. Commit and push it (ops/sync.sh), then rerun with --live.")
        return
    if not os.path.exists(bp): sys.exit(f"refused: no before-value {_rel(bp)}; run --before-only, commit and push it first")
    B = json.load(open(bp)); extra = sorted(set(slug_url) - set(B.get("slugs_absent") or []))
    if B.get("collection") != cid or extra: sys.exit(f"refused: before-value {_rel(bp)} does not cover {extra or 'this collection'}; rerun --before-only, commit and push")
    bad = require_before([bp])
    if bad: sys.exit("refused: before-values not committed and pushed:\n  " + "\n  ".join(bad))
    if not _pushed(sha): sys.exit(f"refused: {sha[:7]} is not on origin/main (image URLs are pinned to it); push first")
    rp = os.path.join(ROOT, "childedits", _day(), f"{h['repo_dir']}.api-create.{sha[:7]}.{_stamp()}.rollback.json"); created = []
    def on_batch(ch, resp):
        got = {(x.get("fieldData") or {}).get("slug"): x.get("id") for x in W.created_of(resp)}
        for it in ch: sl = it["fieldData"]["slug"]; created.append({"url": slug_url[sl], "slug": sl, "id": got.get(sl)})
        json.dump({"op": "create", "hub": hub, "collection": cid, "sha": sha, "before": _rel(bp), "created": created,
                   "rollback": "drafts created by hubctl api-create; to roll back, delete these items in the Webflow CMS on Divit's go (the API script never deletes)"},
                  open(rp, "w"), indent=1)
        _apilog({"op": "create", "hub": hub, "collection": cid, "count": len(ch), "slugs": [it["fieldData"]["slug"] for it in ch], "ids": [got.get(it["fieldData"]["slug"]) for it in ch]})
    os.makedirs(os.path.dirname(rp), exist_ok=True); err = None; t0 = datetime.datetime.now()
    try: W.create_items(cid, [it for _, it in go], dry=False, on_batch=on_batch)
    except (W.ApiError, W.Refused) as e: err = str(e); print(f"STOPPED: {err}")
    items2, rb2 = api_read(hub); learn = _learn_live() if H.learn_from_item(hub) else None
    ok, nbad, lines = H._bulk_verify(hub, items2, only={u for u, _ in go} | {u for u, _ in skip}, need_draft=True, learn=learn)
    if H.learn_from_item(hub): print(f"  {H.learn_note(learn)}")
    for l in lines: print(l)
    _hublog(hub, f"api-create: {len(created)} draft(s) created via Data API at {sha[:7]} ({', '.join(c['slug'] for c in created)}); read back {len(items2)} items; verified {ok}, mismatched {nbad}; before {_rel(bp)}; rollback {_rel(rp)}" + (f"; stopped: {err[:200]}" if err else ""))
    print(f"created {len(created)} in {(datetime.datetime.now() - t0).total_seconds():.0f}s; read back {len(items2)}; verified and recorded {ok}; mismatched {nbad}; rollback {_rel(rp)}")
    if err or nbad: sys.exit(1)

def _before_index():
    idx = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "childedits", "*", "*.before.json"))):
        try: d = json.load(open(p))
        except ValueError: continue
        if isinstance(d, dict) and d.get("id") and isinstance(d.get("fieldData"), dict): idx.setdefault(d["id"], []).append((p, d))
    return idx
def _same_image(sent, got, before):
    g = got or {}
    if (sent.get("alt") or "") != (g.get("alt") or ""): return False
    if sent.get("fileId"): return g.get("fileId") == sent["fileId"]
    return bool(g.get("fileId")) and g.get("fileId") != ((before or {}).get("fileId"))

def cmd_api_update(args):
    """hubctl api-update PAYLOAD.json [--dry-run | --live]: run the item updates (and the item publishes of exactly those items) in a
    payload written by ship-update or relink-payload (ops/out/ship/*.json). Every item needs a committed and pushed before-value in
    childedits/ covering its fields; the rollback payload (the before-values) is written before the write; the collection is read
    back and every sent field diffed; a mismatch stops before any publish."""
    W = _W(); pf = args[0]; mode = _mode(args)
    if mode == "before": sys.exit("api-update takes its before-values from hubctl ship-update / relink-payload --before-only")
    upd, pub = {}, {}
    for a in json.load(open(pf)):
        if "update_collection_items" in a: x = a["update_collection_items"]; upd.setdefault(x["collection_id"], []).extend(x["request"]["items"])
        elif "publish_collection_items" in a: x = a["publish_collection_items"]; pub.setdefault(x["collection_id"], []).extend(i["id"] for i in x["request"]["items"])
        else: sys.exit(f"refused: action {a.get('label')!r} is neither an item update nor an item publish")
    if not upd: sys.exit("refused: the payload has no item updates")
    for c in set(upd) | set(pub):
        if c not in W.CHILD: sys.exit(f"refused: collection {c} is not a child collection")
    for c, ids in pub.items():
        extra = set(ids) - {it["id"] for it in upd.get(c, [])}
        if extra: sys.exit(f"refused: publish of {len(extra)} item(s) not updated by this payload")
    idx = _before_index(); bfile = {}; missing = []
    for c, its in upd.items():
        for it in its:
            if "isDraft" in it and it["isDraft"] is not True: sys.exit(f"refused: {it['id']} sets isDraft {it['isDraft']}")
            cov = [(p, d) for p, d in idx.get(it["id"], []) if set(it["fieldData"]) <= set(d["fieldData"]) and d.get("collection", c) == c]
            if cov: bfile[it["id"]] = cov[-1]
            else: missing.append(it["id"])
    if missing: sys.exit(f"refused: no before-value in childedits/ covers {len(missing)} item(s): {', '.join(missing[:5])} (run ship-update / relink-payload --before-only, commit, push)")
    n = sum(len(v) for v in upd.values()); name = os.path.splitext(os.path.basename(pf))[0]
    if mode == "dry":
        print(f"DRY RUN api-update {os.path.basename(pf)}: {n} item(s)")
        for c, its in upd.items():
            for r in W.update_items(c, its, dry=True): print(f"  {r['method']} {r['path']}  {r['count']} item(s), fields: {', '.join(sorted({k for it in its for k in it['fieldData']}))}")
            print(f"  then GET /collections/{c}/items (read-back) and a diff of every sent field" + (f"; GET /collections/{W.LEARN}/items (Learn, read only) and 3 published acrm---learn refs per item" if H.learn_from_item(W.CHILD[c]) else ""))
        for c, ids in pub.items():
            for r in W.publish_items(c, ids, dry=True): print(f"  {r['method']} {r['path']}  {r['count']} item(s) (only if the diff is clean)")
        bad = require_before(sorted({p for p, _ in bfile.values()}))
        print(f"  before-values: {len(set(p for p, _ in bfile.values()))} file(s), " + (f"{len(bad)} not committed and pushed" if bad else "all committed and pushed") + ". Nothing was sent.")
        return
    bad = require_before(sorted({p for p, _ in bfile.values()}))
    if bad: sys.exit("refused: before-values not committed and pushed:\n  " + "\n  ".join(bad))
    rp = os.path.join(ROOT, "childedits", _day(), f"{name}.{_stamp()}.rollback.json"); os.makedirs(os.path.dirname(rp), exist_ok=True)
    json.dump([{"label": f"rollback of {os.path.basename(pf)}: before-values, changed fields only", "update_collection_items": {"collection_id": c, "request": {"items": [
        {"id": it["id"], "fieldData": {k: bfile[it["id"]][1]["fieldData"].get(k) for k in it["fieldData"]}} for it in its]}}} for c, its in upd.items()], open(rp, "w"), indent=1, ensure_ascii=False)
    diffs = []; err = None; learn = False
    for c, its in upd.items():
        try: W.update_items(c, its, dry=False, on_batch=lambda ch, r, c=c: _apilog({"op": "update", "collection": c, "count": len(ch), "ids": [i["id"] for i in ch], "payload": os.path.basename(pf)}))
        except (W.ApiError, W.Refused) as e: err = str(e); print(f"STOPPED: {err}")
        got = {it["id"]: it for it in W.list_items(c, dry=False)[0]}
        for it in its:
            g = (got.get(it["id"]) or {}).get("fieldData") or {}; bfd = bfile[it["id"]][1]["fieldData"]
            for k, v in it["fieldData"].items():
                same = _same_image(v, g.get(k), bfd.get(k)) if isinstance(v, dict) else g.get(k) == v
                if not same: diffs.append(f"{it['id']}: {k}")
            hb = W.CHILD[c]
            if H.learn_from_item(hb):   # Divit 2026-10-16: every updated item keeps exactly 3 published Learn refs
                if learn is False: learn = _learn_live(); print(f"  {H.learn_note(learn)}")
                diffs += [f"{it['id']}: {p}" for p in H.learn_problems(hb, got.get(it["id"]) or {"fieldData": {}}, learn)]
    hub = W.CHILD[next(iter(upd))]
    _hublog(hub, f"api-update {os.path.basename(pf)}: {n} item(s) updated via Data API; read back; {len(diffs)} field mismatch(es); rollback {_rel(rp)}" + (f"; stopped: {err[:200]}" if err else ""))
    for d in diffs: print(f"  MISMATCH {d}")
    if err or diffs: sys.exit("not published: fix the mismatches first" if pub else 1)
    for c, ids in pub.items():
        res = W.publish_items(c, ids, dry=False, on_batch=lambda ch, r, c=c: _apilog({"op": "publish", "collection": c, "count": len(ch), "ids": ch, "published": len(r.get("publishedItemIds") or []), "errors": len(r.get("errors") or [])}))
        done = {i for r in res for i in (r.get("publishedItemIds") or [])}
        if set(ids) - done: print(f"  NOT PUBLISHED {len(set(ids) - done)} item(s): {', '.join(sorted(set(ids) - done)[:5])}")
    print(f"updated {n} item(s); read back clean" + (f"; item-published {sum(len(v) for v in pub.values())}" if pub else "") + f"; rollback {_rel(rp)}")

def cmd_api_publish(args):
    """hubctl api-publish HUB [--ids-from-state cms_draft] [--limit N] [--dry-run | --before-only | --live] [--verify-live] [--no-relink]
    Item publish (never a site publish) of exactly the verified cms_draft pages' item IDs, 100 per call. --before-only writes their
    before-state from a fresh read (isDraft, lastPublished, lastUpdated) to childedits/<date>/; --live refuses unless it is committed,
    pushed and still current. --verify-live then runs verify-live per URL (state published on a pass), then the automatic relink
    (auto_relink) for the pages that passed; --no-relink skips it (then run relink-payload by hand)."""
    import guards as G
    W = _W(); hub, h = _hub(args); mode = _mode(args); cid = h["collection_id"]
    if _arg(args, "--ids-from-state", "cms_draft") != "cms_draft": sys.exit("refused: only verified cms_draft pages are item-published")
    pairs, warn = H._publish_ids(hub)
    if "--limit" in args: pairs = pairs[:int(_arg(args, "--limit"))]
    if not pairs: sys.exit("no verified cms_draft pages to publish")
    for url, _ in pairs:
        s = spec(url); fp = G.fingerprint(s)
        if fp not in {(s.get("approval") or {}).get("fingerprint"), (s.get("cms_draft") or {}).get("fingerprint")}:
            sys.exit(f"refused: {url} changed after approval / draft verification (fingerprint); re-verify before publishing")
    for w in warn: print(w, file=sys.stderr)
    ids = [i for _, i in pairs]; key = hashlib.sha1(",".join(sorted(ids)).encode()).hexdigest()[:8]
    bp = os.path.join(ROOT, "childedits", _day(), f"{h['repo_dir']}.api-publish.{key}.before.json")
    if mode == "dry":
        print(f"DRY RUN api-publish {hub}: {len(ids)} item(s) (item publish only; no site publish)")
        for r, ch in zip(W.publish_items(cid, ids, dry=True), W.chunks(pairs)):
            print(f"  {r['method']} {r['path']}  {r['count']} item(s): {', '.join(u.rsplit('/', 1)[1] for u, _ in ch)}")
        print(f"  then verify-live per URL ({len(ids)} page fetch(es) plus their FAQ link checks)" if "--verify-live" in args else "  (add --verify-live to check every live URL after)")
        if "--verify-live" in args and "--no-relink" not in args:
            for l in auto_relink({u: True for u, _ in pairs}, "dry")[1]: print(l)
        print(f"  before-value {_rel(bp)}: " + ("present" if os.path.exists(bp) else "not written yet (--before-only)") + ". Nothing was sent.")
        return
    items, rb = api_read(hub); by = {it["id"]: it for it in items}
    lost = [u for u, i in pairs if i not in by or (by[i].get("fieldData") or {}).get("slug") != u.rsplit("/", 1)[1]]
    if lost: sys.exit(f"refused: not in the collection under their slug: {', '.join(lost[:5])}")
    before = [{"id": i, "slug": u.rsplit("/", 1)[1], **{k: by[i].get(k) for k in ("isDraft", "isArchived", "lastPublished", "lastUpdated")}} for u, i in pairs]
    if mode == "before":
        if not os.path.exists(bp) or json.load(open(bp)) != before:
            os.makedirs(os.path.dirname(bp), exist_ok=True); json.dump(before, open(bp, "w"), indent=1)
        print(f"before-value {_rel(bp)}: {len(ids)} item(s). Commit and push it (ops/sync.sh), then rerun with --live."); return
    if not os.path.exists(bp): sys.exit(f"refused: no before-value {_rel(bp)}; run --before-only, commit and push it first")
    if json.load(open(bp)) != before: sys.exit(f"refused: the items changed since {_rel(bp)} was written; rerun --before-only, commit and push")
    bad = require_before([bp])
    if bad: sys.exit("refused: before-values not committed and pushed:\n  " + "\n  ".join(bad))
    rp = os.path.join(ROOT, "childedits", _day(), f"{h['repo_dir']}.api-publish.{key}.{_stamp()}.rollback.json"); os.makedirs(os.path.dirname(rp), exist_ok=True)
    json.dump({"op": "publish", "hub": hub, "collection": cid, "items": before, "before": _rel(bp),
               "rollback": "unpublish is not on the API allowlist: unpublish these items in the Webflow CMS on Divit's go; their before-state is in the before file"}, open(rp, "w"), indent=1)
    t0 = datetime.datetime.now(); err = None; done = set(); errs = 0
    try:
        for r in W.publish_items(cid, ids, dry=False, on_batch=lambda ch, r: _apilog({"op": "publish", "hub": hub, "collection": cid, "count": len(ch), "ids": ch, "published": len(r.get("publishedItemIds") or []), "errors": len(r.get("errors") or [])})):
            done |= set(r.get("publishedItemIds") or []); errs += len(r.get("errors") or [])
    except (W.ApiError, W.Refused) as e: err = str(e); print(f"STOPPED: {err}")
    miss = [u for u, i in pairs if i not in done]
    for u, i in pairs:
        if i in done: G.live_mark(u, i, now(), "api-publish")   # item-published: live in Webflow (status/live.json), whatever its workflow state
    _hublog(hub, f"api-publish: {len(done)} item(s) item-published via Data API (no site publish); errors {errs}; not published {len(miss)}; before {_rel(bp)}; rollback {_rel(rp)}" + (f"; stopped: {err[:200]}" if err else ""))
    print(f"item-published {len(done)}/{len(ids)} in {(datetime.datetime.now() - t0).total_seconds():.0f}s; errors {errs}")
    for u in miss: print(f"  NOT PUBLISHED {u}")
    if "--verify-live" in args and done:
        import verify_live as V, time as _t
        _t.sleep(int(_arg(args, "--wait", "15"))); fails = []
        for u, i in pairs:
            if i not in done: continue
            t1 = _t.time(); ok, rep = V.verify(spec(u))
            if not ok: _t.sleep(30); ok, rep = V.verify(spec(u))   # one retry: the CDN can lag an item publish
            if ok: H.set_state(u, "published", note="live page verified", via="api-publish")
            else: fails.append(u)
            print(f"  {'PASS' if ok else 'FAIL'} {u} ({_t.time() - t1:.1f}s)" + ("" if ok else ": " + "; ".join(l for l in rep if l.startswith("FAIL"))[:300]))
        print(f"verify-live: {len(done) - len(fails)}/{len(done)} pass")
        rok = True
        if "--no-relink" not in args:
            rok, rl = auto_relink({u: u not in fails for u, i in pairs if i in done}, "live")
            for l in rl: print(l)
        if fails or not rok: sys.exit(1)
    if err or miss: sys.exit(1)

# ---------- automatic relink (Divit 2026-10-15): when api-publish ships a page and verify-live passes, every pending link that
# targets it is restored: relink plan from a fresh read -> before-values committed and pushed (ops/sync.sh, those files only) ->
# api-update --live (update, read-back diff, item publish of exactly the relinked items) -> verify-live on every relinked page.
# A target that failed verify-live (or was not published) triggers nothing. Dry run prints the plan only, no network.
def relink_holders(targets, specs=None, live=None):
    """[(holder url, [targets])]: live pages holding pending links to any of `targets` (the dry-run plan; no network)."""
    import guards as G
    live = H.live_urls() if live is None else live; tg = set(targets); out = []
    for s in (G.all_specs() if specs is None else specs):
        hit = sorted({p["target"] for p in s.get("pending_links") or [] if p["target"] in tg})
        if hit: out.append((s["url"], hit, s["url"] in live))
    return out

def _commit_befores(paths, msg):
    r = subprocess.run(["bash", os.path.join(ROOT, "ops", "sync.sh"), msg + "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"] + [_rel(p) for p in paths],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()[-300:]

def auto_relink(results, mode, specs=None, read=None, commit=None, update=None, verify=None, live=None):
    """results {target url: verify-live passed}. Returns (ok, lines). The steps are injectable for the golden cases."""
    import guards as G
    passed = sorted(u for u, ok in results.items() if ok); failed = sorted(u for u, ok in results.items() if not ok); L = []
    specs = G.all_specs() if specs is None else specs
    if mode == "dry":
        hs = relink_holders(list(results), specs, live)
        L.append(f"  relink plan (after verify-live passes; a target that fails triggers none): {len(hs)} page(s)")
        for u, tg, lv in hs: L.append(f"    {u} -> restores link(s) to {', '.join(tg)}" + ("" if lv else " (holder not live: skipped)"))
        return True, L
    for u in failed: L.append(f"  relink: none for {u} (verify-live failed)")
    if not passed: return True, L
    live = H.live_urls() if live is None else live
    hs = [h for h in relink_holders(passed, specs, live) if h[2]]
    if not hs: L.append(f"  relink: no pending links target {len(passed)} published page(s)"); return True, L
    read = read or (lambda hub: api_read(hub)[0]); commit = commit or _commit_befores
    update = update or (lambda pf: cmd_api_update([pf, "--live"])); verify = verify or (lambda u: __import__("verify_live").verify(spec(u)))
    items = {}
    for hub in sorted({H.hub_of(u) for u, _, _ in hs}): items.update({it["id"]: it for it in read(hub)})
    upd, pub, befores, refused, rows = relink_plan(items, live, specs=specs, targets=set(passed))
    for r in refused: L.append("  relink REFUSED " + r)
    if not upd: L.append("  relink: nothing to send (fields already linked or refused)"); return not refused, L
    for u, ch, ready in rows: L.append(f"  relink {u}: {', '.join(ch)} (links to {', '.join(ready)})")
    ok, out = commit(befores, f"relink before-values (auto, after api-publish): {', '.join(u.rsplit('/', 1)[1] for u, _, _ in rows)}")
    if not ok: L.append("  relink STOPPED: before-values not committed and pushed: " + out); return False, L
    pf = os.path.join(ROOT, "ops", "out", "ship", f"relink-auto-{_stamp()}.json"); os.makedirs(os.path.dirname(pf), exist_ok=True)
    json.dump(relink_actions(upd, pub), open(pf, "w"), indent=1, ensure_ascii=False)
    try: update(pf)
    except SystemExit as e: L.append(f"  relink STOPPED in api-update ({_rel(pf)}): {e}"); return False, L
    good = True
    for u, _, _ in rows:
        v, rep = verify(u)
        if v:
            s = next(x for x in specs if x["url"] == u); H._record_pending(u, H.export_fields(u, {k: x for k, x in s.items() if k != "_path"}, live)[1])
        good = good and v
        L.append(f"  relink verify-live {'PASS' if v else 'FAIL'} {u}" + ("" if v else ": " + "; ".join(l for l in rep if l.startswith("FAIL"))[:300]))
    return good and not refused, L

# ---------- golden cases for the API path (tests/golden/run.py kind "webflow-api"); dry run and stubs only, never the network
def api_golden(c):
    import io, contextlib, copy as _cp
    W = _W(); t = c["test"]; cid = next(iter(W.CHILD))
    def synth(n, draft=True): return [{"isDraft": draft, "fieldData": {"name": f"Golden {i}", "slug": f"golden-{i}"}} for i in range(n)]
    def body_of(b):
        if not isinstance(b, dict) or "synth" not in b: return b
        s = b["synth"]
        if s["op"] == "create": return {"items": synth(s["n"], s.get("isDraft", True))}
        if s["op"] == "update": return {"items": [{"id": f"{i:024x}", "fieldData": dict(s.get("fieldData") or {"name": "x"}), **({"isDraft": s["isDraft"]} if "isDraft" in s else {})} for i in range(s["n"])]}
        return {"itemIds": [f"{i:024x}" for i in range(s["n"])]}
    real = (W.TRANSPORT, W.TOKEN, W.SLEEP); calls = []
    def no_net(*a, **k): calls.append(a[:2]); raise AssertionError("network call in a dry run")
    try:
        if t == "refuse":
            path = c["path"].replace("{child}", cid)
            try: W.check(c["method"], path, body_of(c.get("body")), c.get("query")); refused = False
            except W.Refused: refused = True
            return refused == c["expect_refused"]
        if t == "dry-no-network":
            W.TRANSPORT = no_net; W.TOKEN = lambda: (_ for _ in ()).throw(AssertionError("token read in a dry run"))
            W.create_items(cid, synth(250)); W.update_items(cid, body_of({"synth": {"op": "update", "n": 3}})["items"]); W.publish_items(cid, [f"{i:024x}" for i in range(3)])
            return not calls
        if t == "batching":
            fn = {"create": lambda n: W.create_items(cid, synth(n)), "update": lambda n: W.update_items(cid, body_of({"synth": {"op": "update", "n": n}})["items"]),
                  "publish": lambda n: W.publish_items(cid, [f"{i:024x}" for i in range(n)])}[c["op"]]
            return [r["count"] for r in fn(c["n"])] == c["expect"]
        if t == "slug-skip":
            cands = [(f"/x/{s}", {"isDraft": True, "fieldData": {"name": s, "slug": s}}) for s in c["cands"]]
            live = [{"id": f"{i:024x}", "fieldData": {"slug": s}} for i, s in enumerate(c["live"])]
            go, skip = plan_create(cands, live, c.get("limit"))
            return [it["fieldData"]["slug"] for _, it in go] == c["expect_create"] and [u.rsplit("/", 1)[1] for u, _ in skip] == c["expect_skip"]
        if t == "create-cmd-skip":   # the command in dry run: a stored read-back holding one slug -> SKIP, no network, plan printed
            rb = os.path.join(ROOT, ".cache", "golden-api-readback.json"); os.makedirs(os.path.dirname(rb), exist_ok=True)
            json.dump({"result": {"items": [{"id": "0" * 24, "fieldData": {"slug": c["live"][0]}}]}}, open(rb, "w"))
            real_c = H._create_candidates; W.TRANSPORT = no_net; W.TOKEN = lambda: (_ for _ in ()).throw(AssertionError("token read"))
            H._create_candidates = lambda hub, sha: [(f"{H.CFG['hubs'][hub]['path']}/{s}", {"isDraft": True, "fieldData": {"name": s, "slug": s}}) for s in c["cands"]]
            out = io.StringIO()
            try:
                with contextlib.redirect_stdout(out): cmd_api_create([W.CHILD[cid], "--sha", "0" * 40, "--readback", rb])
            finally: H._create_candidates = real_c
            o = out.getvalue()
            return not calls and "DRY RUN" in o and f"SKIP" in o and c["live"][0] in o.split("DRY RUN")[0] and "Nothing was sent" in o
        if t == "live-before-gate":  # --live with no committed before-value: refused, and no write request ever leaves
            sent = []
            def stub(method, url, headers, data, timeout):
                sent.append(method)
                return 200, {}, json.dumps({"items": [], "pagination": {"total": 0}}).encode()
            real_c, real_rb = H._create_candidates, globals()["RB_DIR"]
            W.TRANSPORT = stub; W.TOKEN = lambda: "golden-token"; globals()["RB_DIR"] = os.path.join(ROOT, ".cache", "golden-readback")
            H._create_candidates = lambda hub, sha: [(f"{H.CFG['hubs'][hub]['path']}/golden-gate-{i}", {"isDraft": True, "fieldData": {"name": "g", "slug": f"golden-gate-{i}"}}) for i in range(2)]
            real_log, real_api = globals()["_apilog"], None; globals()["_apilog"] = lambda rec: None
            try:
                with contextlib.redirect_stdout(io.StringIO()): cmd_api_create([W.CHILD[cid], "--sha", "f" * 40, "--live"]); return False
            except SystemExit as e: return "before-value" in str(e) and all(m == "GET" for m in sent)
            finally: H._create_candidates = real_c; globals()["RB_DIR"] = real_rb; globals()["_apilog"] = real_log
        if t in ("relink-dry-plan", "relink-target-fails", "relink-chain"):   # Divit 2026-10-15: automatic relink after api-publish
            hub = c.get("hub", "Form"); h = H.CFG["hubs"][hub]; base = h["path"]; T = f"{base}/golden-target"; HU = f"{base}/golden-holder"
            a = f'<a href="https://emergent.sh{T}">golden target</a>'
            sp = [{"url": HU, "hub": hub, "item_id": "a" * 24, "fields": {"faq": f"<p>See the {a} page.</p>"},
                   "pending_links": [{"field": "faq", "target": T, "anchor": "golden target"}]}]
            item = {"id": "a" * 24, "isDraft": False, "lastPublished": "2026-10-15T00:00:00Z", "fieldData": {h["fields"]["faq"]: "<p>See the golden target page.</p>"}}
            steps = []; W.TRANSPORT = no_net; W.TOKEN = lambda: (_ for _ in ()).throw(AssertionError("token read"))
            real_rec = H._record_pending; H._record_pending = lambda u, pend: steps.append(("record", u, len(pend)))
            sent = {}
            def upd(pf): steps.append(("update", os.path.basename(pf))); sent["acts"] = json.load(open(pf)); os.remove(pf)
            kw = dict(specs=sp, read=lambda hb: (steps.append(("read", hb)), [item])[1], commit=lambda b, m: (steps.append(("commit", len(b))), (True, ""))[1],
                      update=upd, verify=lambda u: (steps.append(("verify", u)), (True, []))[1])
            try:
                if t == "relink-dry-plan":
                    ok, L = auto_relink({T: True}, "dry", live={HU}, **kw)
                    return ok and not steps and not calls and any(HU in l and T in l for l in L)
                if t == "relink-target-fails":
                    ok, L = auto_relink({T: False}, "live", live={HU}, **kw)
                    return not steps and not calls and any("verify-live failed" in l for l in L)
                ok, L = auto_relink({T: True}, "live", live={HU, T}, **kw)
                bps = glob.glob(os.path.join(ROOT, "childedits", _day(), "golden-holder.relink.before.json"))
                for b in bps: os.remove(b)
                u = (sent.get("acts") or [{}])[0].get("update_collection_items", {}).get("request", {}).get("items", [{}])[0]
                pubs = [x for x in sent.get("acts") or [] if "publish_collection_items" in x]
                return (ok and [s[0] for s in steps] == ["read", "commit", "update", "verify", "record"] and len(bps) == 1
                        and u.get("fieldData") == {h["fields"]["faq"]: f"<p>See the {a} page.</p>"} and len(pubs) == 1 and not calls)
            finally: H._record_pending = real_rec
        if t == "before-gate":
            return (not require_before([os.path.join(ROOT, c["path"])])) == c["expect_ok"]
        if t == "backoff":
            seq = list(c["statuses"]); slept = []
            def stub(method, url, headers, data, timeout):
                st = seq.pop(0); return st, ({"Retry-After": str(c.get("retry_after", 3))} if st == 429 else {}), b'{"items": [], "pagination": {"total": 0}}'
            W.TRANSPORT = stub; W.TOKEN = lambda: "golden-token"; W.SLEEP = slept.append
            try: W.request("GET", f"/collections/{cid}/items", query={"offset": 0, "limit": 100}, dry=False); ok = True
            except W.ApiError: ok = False
            return ok == c["expect_ok"] and slept == c["expect_sleeps"]
        if t == "no-token":   # a sentinel token never reaches stdout, stderr (debug on) or an exception, even if the server echoes it
            SENT = "wfGOLDENsentinel0123456789abcdef"; out, errb = io.StringIO(), io.StringIO(); msgs = []
            def stub(method, url, headers, data, timeout): return 401, {}, ("bad token " + headers.get("Authorization", "")).encode()
            W.TRANSPORT = stub; W.TOKEN = lambda: SENT; os.environ["WEBFLOW_API_DEBUG"] = "1"
            try:
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(errb):
                    for m, p, b in (("GET", f"/collections/{cid}/items", None), ("POST", f"/collections/{cid}/items/publish", {"itemIds": ["a" * 24]})):
                        try: W.request(m, p, b, query={"offset": 0, "limit": 100} if b is None else None, dry=False)
                        except Exception as e: msgs.append(str(e)); msgs.append(repr(e))
                    print(W.request("GET", f"/collections/{cid}/items", dry=True))
            finally: os.environ.pop("WEBFLOW_API_DEBUG", None)
            allout = out.getvalue() + errb.getvalue() + " ".join(msgs)
            return SENT not in allout and "Bearer [redacted]" in errb.getvalue() and len(msgs) == 4
    finally: W.TRANSPORT, W.TOKEN, W.SLEEP = real
    return None

CMDS = {"api-read": cmd_api_read, "api-read-learn": cmd_api_read_learn, "api-create": cmd_api_create, "api-update": cmd_api_update, "api-publish": cmd_api_publish,
        "ship-update": cmd_update, "relink-payload": cmd_relink, "ship": cmd_ship, "ship-done": cmd_done, "ship-cms": cmd_cms, "ship-qc": cmd_qc, "ship-cost": cmd_cost, "readiness": cmd_readiness}
