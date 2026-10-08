"""hubctl.py: the one tool every build-hub chat uses. Run from the repo root.

  status [HUB]                      queue and state counts (all hubs, or one)
  claim HUB N --by CHAT             claim the next N unclaimed pages of HUB in queue order
  brief URL                         keyword brief for a page (needs plan/keyword_map.json)
  init URL --by WRITER-ID           create the spec skeleton specs/<dir>/<slug>.json, recording who writes it
  qc URL                            run qc/qc_hub.py on that page's spec
  state URL STATE [--note TEXT] [--by ID]   move a page to a new state; writers set qc_pass with --by so no agent reviews its own page (qc_pass runs QC: refused unless TOTAL 0)
  release URL [--note TEXT]         return a claimed/spec page to the planned queue (status entry removed, spec file kept, logged)
  paa-resource URL                  write AlsoAsked provenance into FAQ items matching the pull (no copy changes)
  paa-synonyms URL...               propose PA3 synonym candidates with safety counts -> rules/paa_synonym_candidates.json (not applied)
  paa URL [--spec] [--cand]   PAA gate PA1-PA12 (qc/paa_gate.py): AlsoAsked pull or the spec's FAQ; verdicts to private/alsoasked/verdicts/
  verified URL                      Divit approved the page as rendered in the real Webflow template: it joins the width calibration
  review URL RUBRIC.json --by ID    record the reviewer's rubric and rule-cited findings (state images); blocking -> rework, notes -> spec.review_notes
  ready URL --by ID                 after the one rework: QC 0 and images rendered -> reviewed (ready for Divit); no second review
  export-csv HUB                    one row per page (every CMS field, image paths, alt text) -> .cache/review/<hub>.csv
  challenge                         retired (Divit, 2026-10-07)
  payload URL --sha SHA             write ops/out/<slug>.payload.json: the exact data_cms_tool action
  verify URL READBACK.json          diff a stored CMS read-back against the spec (exit 1 on mismatch)
  record URL --item-id ID [--file-id FIELD=ID ...]   store Webflow IDs after a create/import
  bulk-payload HUB --sha SHA        create_collection_items actions (100 items per action) for every approved page without an item ID
  bulk-verify HUB READBACK.json     verify every page of HUB found in a stored read-back; records item IDs and file IDs
  next STATE [HUB]                  list pages waiting in a state (for orchestrators and reviewers)
  table URL --vs A,B,C --rows id[=Label],... [--variant CAT]   build the comparison table from the vetted library (rules/competitors/)
  library HUB                       list the library: competitors, categories, dimensions, fact ages
  serp-save URL RAW.json [KEYWORD]  normalise a DataForSEO SERP result into private/serp/ (PAA, related, top 10, features)
  serp-keywords URL RAW.json       add DataForSEO keyword ideas (related keywords) to the page's SERP capture
  serp-status [HUB]                 claimed or in-progress pages that still need a live SERP
  images URL                        render the page's image_brief into its 6 images + contact sheet (engine), state -> images
  images-batch STATE [HUB]          render every page in STATE (normally 'reviewed'); prints a summary
  cms-check HUB READBACK.json       record which queued slugs already exist in Webflow (required within the hour before creating)
  plan-check URL                    compare the page's plan and tab headings with the hub's other specs (run before writing prose)
  pack URL --role writer|reviewer   one compact file for that agent: brief, the rules it needs, catalogue summary, exemplar
  sources-check URL|--all            link-check every spec.domain_sources URL (cached for QC P3)
  usage-log URL TOKENS --role R     record an agent's token usage for a page (metrics reports tokens per page)
  metrics | sample [STATE] | links HUB | links --relink | lookahead HUB [N] | serp-budget | ranks-save URL RAW | ranks-report | recheck [--states a,b] | image-regress | verify-live URL [--html F]
  publish-payload HUB               publish_collection_items actions (100 per call) for every verified cms_draft page (only after Divit's go)
  log HUB TEXT                      append a dated line to logs/<hub>.md

HUB is one of LP, Form, Auto, SurveyQuiz. Status lives in status/<hub>.json; each hub chat writes only its own.
"""
import json, os, sys, re, glob, datetime, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))
STATES = ["claimed", "spec", "qc_pass", "images", "reviewed", "challenged", "approved", "rework", "cms_draft", "published", "parked"]
# pipeline (Divit, 2026-10-07): claimed -> spec -> qc_pass (code QC = 0) -> images (rendered + gated) -> one review (rules/SEVERITY.md)
#   -> reviewed (no blocking) or rework -> one rework -> qc_pass -> images -> `hubctl ready` -> reviewed -> approved (Divit) -> cms_draft -> published.
# The writer and the reviewer must be different agents. "challenged" is kept only for pages that passed the retired challenger pass.
REPO_RAW = "https://raw.githubusercontent.com/seo881/potential-enigma"

def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
def kmap():
    p = os.path.join(ROOT, "plan", "keyword_map.json")
    if not os.path.exists(p): sys.exit("plan/keyword_map.json missing. Run: python3 plan/build_map.py /mnt/project/Emergent_Hub_Child_Pages_Final_v3.xlsx")
    return json.load(open(p))
def hub_of(url):
    for k, h in CFG["hubs"].items():
        if url.startswith(h["path"] + "/"): return k
    sys.exit(f"no hub owns {url}")
def spath(url):
    h = CFG["hubs"][hub_of(url)]; return os.path.join(ROOT, "specs", h["repo_dir"], url.rsplit("/", 1)[1] + ".json")
def st_path(hub): return os.path.join(ROOT, "status", f"{CFG['hubs'][hub]['repo_dir']}.json")
def load_st(hub):
    p = st_path(hub)
    return json.load(open(p)) if os.path.exists(p) else {"hub": hub, "pages": {}}
def save_st(hub, st): json.dump(st, open(st_path(hub), "w"), indent=1, sort_keys=True)
def set_state(url, state, note=None, via=None, by=None, **extra):
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    hub = hub_of(url)
    with G.lock("status-" + hub):
        st = load_st(hub); e = st["pages"].setdefault(url, {})
        e.update({"state": state, "updated": now(), **extra})
        if note: e["note"] = note
        save_st(hub, st)
    sp = spath(url)
    if os.path.exists(sp):
        with G.lock("spec-" + url.rsplit("/", 1)[1]):
            s = json.load(open(sp)); s.setdefault("history", []).append({"t": now(), "state": state, "via": via, "by": by, "note": (note or "")[:300]})
            json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)

def cmd_status(args):
    m = kmap(); hubs = [args[0]] if args else list(CFG["hubs"])
    for hub in hubs:
        st = load_st(hub)["pages"]; queue = [p for p in m.values() if p["hub"] == hub and p["status"] == "planned"]
        counts = {}
        for p in queue: counts[st.get(p["url"], {}).get("state", "queued")] = counts.get(st.get(p["url"], {}).get("state", "queued"), 0) + 1
        print(f"{hub:10s} {len(queue):3d} planned | " + " ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        for url, e in sorted(st.items(), key=lambda x: x[1].get("updated", "")):
            if e.get("state") not in ("queued", "published"): print(f"    {e['state']:9s} {url}  ({e.get('by','')}, {e.get('updated','')}) {e.get('note','')}")

def cmd_claim(args):
    hub, n = args[0], int(args[1]); by = args[args.index("--by") + 1] if "--by" in args else "unknown"
    pin = os.path.join(ROOT, ".hub")
    if os.path.exists(pin) and open(pin).read().strip() != hub: sys.exit(f"this worktree works only hub {open(pin).read().strip()} (ops/worktrees.sh); claim {hub} from its own worktree")
    if n > 50: sys.exit("claim at most 50 pages at a time")
    m = kmap(); st = load_st(hub)
    queue = sorted([p for p in m.values() if p["hub"] == hub and p["status"] == "planned"], key=lambda p: p["queue_rank"])
    got = []
    for p in queue:
        if p["url"] in st["pages"]: continue
        st["pages"][p["url"]] = {"state": "claimed", "by": by, "updated": now(), "queue_rank": p["queue_rank"]}
        got.append(p)
        if len(got) == n: break
    save_st(hub, st)
    for p in got: print(f"claimed #{p['queue_rank']:<4} {p['url']}  ({p['primary']}, {p['total_msv']} total MSV, wave {p['wave']})")
    print("Commit and push status now so other chats see the claim.")

def cmd_brief(args):
    m = kmap(); p = m.get(args[0]) or sys.exit("not in keyword map")
    print(f"URL        {p['url']}   (queue #{p.get('queue_rank')}, wave {p.get('wave')}, {p.get('tier')})")
    print(f"PRIMARY    {p['primary']}  | MSV {p['primary_msv']} | KD {p['kd']} | intent {p['intent']} | cluster {p['cluster']}")
    print(f"TOTAL MSV  {p['total_msv']}")
    print(f"VERDICT    {p.get('verdict')}  | top-10 mix: {p.get('top10_mix')}")
    if p.get("angle"): print(f"ANGLE      {p['angle']}")
    if p.get("amber_evidence"): print(f"AMBER      {p['amber_evidence']}")
    if p.get("serp_features"): print(f"SERP FEAT  {p['serp_features']}")
    if p.get("pass3_action"): print(f"SHEET NOTE {p['pass3_action']}")
    if p.get("notes"): print(f"NOTES      {p['notes']}")
    for o in p.get("overrides", []): print(f"OVERRIDE   {o}")
    for w in p.get("watch", []): print(f"WATCH      {w}")
    print("SECONDARIES (use each naturally, once; never as a heading if it is another page's primary):")
    for s in p["secondaries"]: print(f"   {s['msv']:>6}  {s['kw']}")
    if p.get("top10"):
        print("TOP 10 (Semrush US, Oct 2026): build the comparison table and the angle from these, not from memory")
        for i, u in enumerate(p["top10"], 1): print(f"   {i:>2}. {u}")
    else:
        print("TOP 10 not pulled (Wave 3): get the live top 10 before writing and apply the cut rules (plan/ISSUES.md).")
    sys.path.insert(0, os.path.join(ROOT, "plan")); import serp as S
    live = S.load(p["url"]); prims = {q["primary"].lower(): q["url"] for q in m.values() if q["url"] != p["url"] and q.get("status") != "live-off-plan"}
    if live:
        print(f"LIVE SERP  DataForSEO, Google US, {live['fetched']} | features: {', '.join(live['features'])}")
        print("PEOPLE ALSO ASK (source every FAQ question from these first; mirror the phrasing; answer in your own words):")
        ok, skip = S.eligible(live, p, prims)
        for it in ok: print(f"   - {it['q']}")
        for q_, why in skip: print(f"   x {q_}   [skip: {why}]")
        if live.get("keywords"): print("KEYWORD IDEAS (DataForSEO; more FAQ sources once PAA and secondaries are used):\n   " + " | ".join(f"{k['kw']} ({k['msv']})" for k in live["keywords"][:25]))
        if live["related"]: print("RELATED SEARCHES (fill remaining FAQ slots and secondaries from these):\n   " + " | ".join(live["related"]))
        if not p.get("top10") and live["organic"]: print("TOP 10 (live):\n" + "\n".join(f"   {o['rank']:>2}. {o['url']}" for o in live["organic"]))
    else:
        print("LIVE SERP  not captured yet. Pull it first (DataForSEO, Google organic live advanced, United States, English,")
        print("           people_also_ask_click_depth 2) and save it: python3 ops/hubctl.py serp-save <url> <raw.json>")
    if p.get("wave3_evidence"): print(f"WAVE 3     {p['wave3_evidence']}")
    try:
        sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
        nl = [(u, n) for u, n in G.needs_links(p["hub"], 10) if u != p["url"]]
        if nl: print("LINK THESE (live or approved siblings with the fewest inbound links; exact-match anchors in FAQ answers):\n" + "\n".join(f"   {n} inbound  {u}" for u, n in nl[:6]))
    except Exception: pass
    sib = [q for q in m.values() if q["hub"] == p["hub"] and q["url"] != p["url"] and q["cluster"] == p["cluster"]]
    if sib:
        print("SIBLINGS IN THE SAME CLUSTER (do not use their primaries as headings; link to them where natural):")
        for q in sorted(sib, key=lambda q: -q["total_msv"])[:12]: print(f"   {q['primary']:40s} {q['url']}")

def cmd_init(args):
    url = args[0]; hub = hub_of(url); h = CFG["hubs"][hub]; m = kmap(); p = m.get(url) or sys.exit("not in keyword map")
    path = spath(url)
    if os.path.exists(path): sys.exit(f"{path} exists; edit it instead")
    slug = url.rsplit("/", 1)[1]; d = f"images/{h['repo_dir']}/{slug}"
    fields = {k: "" for k in h["fields"] if k not in CFG["image_fields"]}
    for k in CFG["optional_fields"]: fields[k] = None
    fields["slug"] = slug; fields["category"] = CFG["category_option_ids"][hub]
    by = args[args.index("--by") + 1] if "--by" in args else (load_st(hub)["pages"].get(url, {}).get("by") or "unknown-writer")
    spec = {"url": url, "hub": hub, "item_id": None, "status": "spec", "written_by": by,
            "keywords": {"primary": p["primary"], "secondaries_used": []},
            "vendor_facts_checked": None,
            "fields": fields,
            "images": {"tab_image_1": {"path": f"{d}/uc-1.svg", "alt": ""}, "tab_image_2": {"path": f"{d}/uc-2.svg", "alt": ""},
                       "tab_image_3": {"path": f"{d}/uc-3.svg", "alt": ""}, "tab_image_4": {"path": f"{d}/uc-4.svg", "alt": ""},
                       "cover_image": {"path": f"{d}/cover.svg", "alt": ""}, "share_image": {"path": f"{d}/og.png", "alt": ""}},
            "image_spec": None}
    os.makedirs(os.path.dirname(path), exist_ok=True); json.dump(spec, open(path, "w"), indent=1, ensure_ascii=False)
    set_state(url, "spec"); print(f"created {os.path.relpath(path, ROOT)}")

def cmd_qc(args):
    rc = subprocess.call([sys.executable, os.path.join(ROOT, "qc", "qc_hub.py"), spath(args[0])])
    if rc == 0:
        sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
        sp = spath(args[0]); s = json.load(open(sp)); s["qc_passed"] = {"rules_version": G.rules_version(), "date": now()}
        json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)
    return rc

def _record_pending(url, pend):
    sp = spath(url); s = json.load(open(sp))
    if s.get("pending_links") != pend:
        s["pending_links"] = pend; json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)
    if pend: print(f"{url}: {len(pend)} link(s) to non-live pages sent as plain text: " + ", ".join(p["target"] for p in pend))

def cmd_payload(args):
    url = args[0]; sha = args[args.index("--sha") + 1]; hub = hub_of(url); h = CFG["hubs"][hub]
    s = json.load(open(spath(url))); fd = {}
    ex, pend = export_fields(url, s); _record_pending(url, pend)
    for k, v in ex.items():
        if v is None or v == "" and k in CFG["optional_fields"]: continue
        fd[h["fields"][k]] = v
    for k, im in s["images"].items():
        if im.get("path"):
            full = os.path.join(ROOT, im["path"])
            if not os.path.exists(full): sys.exit(f"image missing on disk: {im['path']}")
            fd[h["fields"][k]] = {"url": f"{REPO_RAW}/{sha}/{im['path']}", "alt": im["alt"]}
    assert fd.get("name") and fd.get("slug"), "name (h1) and slug are required"
    if s.get("item_id"):
        action = {"label": f"update {fd['slug']}", "update_collection_items": {"collection_id": h["collection_id"],
                  "request": {"items": [{"id": s["item_id"], "isDraft": True, "fieldData": fd}]}}}
    else:
        action = {"label": f"create {fd['slug']}", "create_collection_items": {"collection_id": h["collection_id"],
                  "request": {"items": [{"isDraft": True, "fieldData": fd}]}}}
    os.makedirs(os.path.join(ROOT, "ops", "out"), exist_ok=True)
    out = os.path.join(ROOT, "ops", "out", f"{fd['slug']}.payload.json"); json.dump([action], open(out, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {os.path.relpath(out, ROOT)}: pass its content as the `actions` of data_cms_tool (isDraft is always true)")

def _items_from_readback(path):
    raw = json.load(open(path)); txt = "".join(b.get("text", "") for b in raw) if isinstance(raw, list) else json.dumps(raw)
    dec = json.JSONDecoder(); i = 0; items = []
    while i < len(txt):
        while i < len(txt) and txt[i] in " \n\r\t": i += 1
        if i >= len(txt): break
        o, j = dec.raw_decode(txt, i); i = j
        res = o.get("result", {}) if isinstance(o, dict) else {}
        items += res.get("items", [])
    return items

def cmd_verify(args):
    url, rb = args[0], args[1]; hub = hub_of(url); h = CFG["hubs"][hub]; s = json.load(open(spath(url)))
    slug = url.rsplit("/", 1)[1]
    items = [it for it in _items_from_readback(rb) if it.get("fieldData", {}).get("slug") == slug]
    if not items: sys.exit(f"no item with slug {slug} in {rb}")
    it = items[0]; fd = it["fieldData"]; bad = []
    for k, v in export_fields(url, s)[0].items():
        if v in (None, "") and k in CFG["optional_fields"]: continue
        if fd.get(h["fields"][k]) != v: bad.append(k)
    for k, im in s["images"].items():
        got = fd.get(h["fields"][k]) or {}
        if not got.get("fileId"): bad.append(f"{k} (no fileId)")
        elif got.get("alt") != im.get("alt"): bad.append(f"{k} (alt differs)")
    print(f"item {it['id']} isDraft={it.get('isDraft')} | mismatched: {bad or 'none'}")
    sys.exit(1 if bad else 0)

def cmd_record(args):
    url = args[0]; s = json.load(open(spath(url)))
    if "--item-id" in args: s["item_id"] = args[args.index("--item-id") + 1]
    for i, a in enumerate(args):
        if a == "--file-id":
            k, v = args[i + 1].split("=", 1); s["images"][k]["file_id"] = v
    json.dump(s, open(spath(url), "w"), indent=1, ensure_ascii=False)
    set_state(url, "cms_draft", item_id=s.get("item_id")); print("recorded")

def _rubric_ok(url):
    RUB = json.load(open(os.path.join(ROOT, "rules", "rubric.json")))["criteria"]
    rv = (json.load(open(spath(url))).get("review") or {}).get("rubric", {})
    return [c["id"] for c in RUB if rv.get(c["id"], {}).get("result") != "pass"]

def _authors(s):
    """Every agent that wrote this page (first writer and each rework writer that set qc_pass with --by)."""
    return {s.get("written_by")} | set(s.get("writers", []))
def _reviewers(s): return {h.get("by") for h in s.get("reviews", [])} | {(s.get("review") or {}).get("by")}
def _keep_notes(s, findings, by, via):
    for f in findings:
        if f["severity"] == "note": s.setdefault("review_notes", []).append({**{k: f.get(k) for k in ("criterion", "rule", "field", "issue", "fix")}, "by": by, "via": via, "date": now()})

def cmd_review(args):
    """RUBRIC.json: {"rubric": {criterion: {result, evidence}}, "findings": [{criterion, rule, field, quote, issue, fix, severity}]}.
    Every finding cites the HUB_RULES section or CONTENT_DEFECTS row it breaks and is blocking or a note. Only blocking findings
    send the page to rework; notes are kept in spec.review_notes (hubctl metrics proposes a rule when one recurs on 3+ pages)."""
    url, rf = args[0], args[1]; by = args[args.index("--by") + 1] if "--by" in args else "reviewer"
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    raw = json.load(open(rf)); rub = raw.get("rubric", raw); findings = raw.get("findings", [])
    RUB = json.load(open(os.path.join(ROOT, "rules", "rubric.json")))["criteria"]; ids = {c["id"] for c in RUB}
    missing = [c for c in ids if c not in rub]
    if missing: sys.exit(f"rubric incomplete, score every criterion: {sorted(missing)}")
    for k in ids:
        v = rub[k]
        if v.get("result") not in ("pass", "fail") or not v.get("evidence"): sys.exit(f'"{k}" needs result pass|fail and one line of evidence')
    errs = G.validate_findings(findings, ids, need_class=True)
    if errs: sys.exit("findings rejected (a defect is a rule violation: cite the rule, name its class from rules/SEVERITY.md):\n  " + "\n  ".join(errs))
    blocking = [f for f in findings if f["severity"] == "blocking"]
    for k in ids:
        hit = [f for f in blocking if f["criterion"] == k]
        if rub[k]["result"] == "fail" and not hit: sys.exit(f'"{k}" is scored fail but no blocking finding cites it: add the finding with its rule, or score it pass')
        if rub[k]["result"] == "pass" and hit: sys.exit(f'"{k}" is scored pass but {len(hit)} blocking finding(s) cite it: score it fail, or mark them notes')
    sp = spath(url); s = json.load(open(sp))
    st_now = load_st(hub_of(url))["pages"].get(url, {}).get("state")
    if st_now != "images": sys.exit(f"review needs the page in state 'images' (QC passed and images rendered); it is '{st_now}'")
    if by in _authors(s): sys.exit("the reviewer cannot be an agent that wrote the page")
    if s.get("review") and "--legacy" not in args: sys.exit("one review per page (Divit, 2026-10-07): after the one rework, run hubctl ready <url> --by <id>; the page then goes to Divit")
    if s.get("review"): s.setdefault("reviews", []).append({k: v for k, v in s["review"].items() if k not in ("rubric", "findings")} | {"result": "pass" if all(v.get("result") == "pass" for v in s["review"]["rubric"].values()) else "fail", "blocking": len([f for f in s["review"].get("findings", []) if f.get("severity") == "blocking"]), "notes": len([f for f in s["review"].get("findings", []) if f.get("severity") == "note"])})
    ch_ = s.pop("challenge", None)
    if ch_ and not any(c.get("by") == ch_.get("by") and c.get("date") == ch_.get("date") for c in s.get("challenges", [])):
        s.setdefault("challenges", []).append({"by": ch_.get("by"), "date": ch_.get("date"), "result": ch_.get("result"), "defects": len(ch_.get("defects", []))})
    s["review"] = {"by": by, "date": now(), "rubric": rub, "findings": findings}; _keep_notes(s, findings, by, "review")
    json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)
    notes = len(findings) - len(blocking)
    if blocking: set_state(url, "rework", note=" | ".join(G.fmt_finding(f) for f in blocking), via="review", by=by); print(f"REWORK: {len(blocking)} blocking, {notes} notes\n  " + "\n  ".join(G.fmt_finding(f) for f in blocking))
    else: set_state(url, "reviewed", note=f"rubric 10/10 by {by}; {notes} notes", via="review", by=by); print(f"REVIEWED: rubric 10/10, {notes} notes kept in spec.review_notes")

def cmd_verified(args):
    url = args[0]; sp = spath(url); s = json.load(open(sp)); s["render_verified"] = now(); json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)
    sys.path.insert(0, os.path.join(ROOT, "ops")); import typeset as TS; TS.calibrate()
    print(f"{url} marked as verified in the template; width ceilings recalibrated with it")

def cmd_ready(args):
    """After the one rework: QC TOTAL 0 and images rendered (state images), the page has its one review -> reviewed, ready for Divit."""
    url = args[0]; by = args[args.index("--by") + 1] if "--by" in args else "orchestrator"
    s = json.load(open(spath(url))); st_now = load_st(hub_of(url))["pages"].get(url, {}).get("state")
    if st_now != "images": sys.exit(f"ready needs the page in state 'images' (reworked, QC passed, images re-rendered); it is '{st_now}'")
    if not s.get("review"): sys.exit("this page has not had its review yet: spawn a page-reviewer (hubctl review)")
    q = subprocess.run([sys.executable, os.path.join(ROOT, "ops", "hubctl.py"), "qc", url], capture_output=True, text=True).stdout
    if "TOTAL (P0+P1) = 0" not in q: sys.exit("QC is not at zero:\n" + q[-1500:])
    src = s.get("challenge") or s["review"]   # legacy pages: the challenger's findings counted as their one review (Divit, 2026-10-07)
    nb = len([f for f in src.get("findings", []) if f.get("severity") == "blocking"])
    set_state(url, "reviewed", note=f"one rework applied by {by} after {src['by']} ({nb} findings marked blocking then, fixed per rules/SEVERITY.md); ready for Divit", via="ready", by=by)
    print(f"{url} -> reviewed (ready for Divit's preview review)")

def cmd_export_csv(args):
    """One row per page ready for Divit or later (or every spec with --all): every CMS field under its Webflow slug,
    each image as its repo path plus an alt-text column. Written to .cache/review/<hub>.csv for review in a spreadsheet."""
    import csv
    hub = args[0]; h = CFG["hubs"][hub]; st = load_st(hub)
    keep = None if "--all" in args else ("reviewed", "challenged", "approved", "cms_draft", "published")
    imgs = [k for k in h["fields"] if k.startswith(("tab_image_", "cover_image", "share_image"))]
    cols = ["url", "state"]
    for k, slug in h["fields"].items(): cols += [slug, slug + " (alt)"] if k in imgs else [slug]
    rows = []
    for url, e in sorted(st["pages"].items(), key=lambda x: x[1].get("queue_rank", 0)):
        if keep and e.get("state") not in keep or not os.path.exists(spath(url)): continue
        s = json.load(open(spath(url))); r = {"url": url, "state": e.get("state")}
        for k, slug in h["fields"].items():
            if k in imgs: im = s.get("images", {}).get(k, {}); r[slug] = im.get("path", ""); r[slug + " (alt)"] = im.get("alt", "")
            else: v = s["fields"].get(k); r[slug] = "" if v is None else v
        rows.append(r)
    out = os.path.join(ROOT, ".cache", "review", f"{h['repo_dir']}.csv"); os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print(f"{os.path.relpath(out, ROOT)}: {len(rows)} page(s), {len(cols)} columns")

def cmd_challenge(args):
    sys.exit("the challenger pass is retired (Divit, 2026-10-07): one review with rules/SEVERITY.md, one rework, then Divit")
def _cmd_challenge_retired(args):
    """FINDINGS.json: {"defects": [{criterion, rule, field, quote, issue, fix, severity}], "checked": [...]}. Same citation rule as review."""
    url, ff = args[0], args[1]; by = args[args.index("--by") + 1] if "--by" in args else "challenger"
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    sp = spath(url); s = json.load(open(sp)); f = json.load(open(ff))
    st_now = load_st(hub_of(url))["pages"].get(url, {}).get("state")
    if st_now != "reviewed": sys.exit(f"challenge needs the page in state 'reviewed'; it is '{st_now}'")
    if by in _authors(s) | _reviewers(s): sys.exit("the challenger must be a different agent from every writer and reviewer of this page")
    if by in {h.get("by") for h in s.get("challenges", [])} | {(s.get("challenge") or {}).get("by")}: sys.exit("every cycle needs a new challenger agent; this one has challenged the page before")
    if not isinstance(f.get("defects"), list) or not f.get("checked"): sys.exit('findings need "defects": [...] (empty if none) and "checked": [what was examined, section by section]')
    ids = {c["id"] for c in json.load(open(os.path.join(ROOT, "rules", "rubric.json")))["criteria"]}
    errs = G.validate_findings(f["defects"], ids)
    if errs: sys.exit("findings rejected (a defect is a rule violation: cite the rule):\n  " + "\n  ".join(errs))
    blocking = [d for d in f["defects"] if d["severity"] == "blocking"]; notes = len(f["defects"]) - len(blocking)
    s["challenge"] = {"by": by, "date": now(), "result": "fail" if blocking else "pass", "defects": [G.fmt_finding(d) for d in blocking], "findings": f["defects"], "checked": f["checked"]}
    s.setdefault("challenges", []).append({"by": by, "date": s["challenge"]["date"], "result": s["challenge"]["result"], "defects": len(blocking), "notes": notes})
    _keep_notes(s, f["defects"], by, "challenge")
    json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)
    if blocking: set_state(url, "rework", note=" | ".join(G.fmt_finding(d) for d in blocking), via="challenge", by=by); print(f"REWORK: {len(blocking)} blocking, {notes} notes\n  " + "\n  ".join(G.fmt_finding(d) for d in blocking))
    else: set_state(url, "challenged", note=f"no blocking defects found by {by}; {notes} notes", via="challenge", by=by); print(f"CHALLENGED: no blocking defects, {notes} notes")

def cmd_state(args):
    url, state = args[0], args[1]
    if state not in STATES: sys.exit(f"state must be one of {STATES}")
    if state in ("reviewed", "challenged"): sys.exit(f"'{state}' is set only by hubctl review or hubctl ready, never by hand")
    if state == "approved":
        cur = load_st(hub_of(url))["pages"].get(url, {}).get("state")
        if cur not in ("reviewed", "challenged"): sys.exit(f"only a reviewed page can be approved (this one is '{cur}')")
        sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
        sp = spath(url); s = json.load(open(sp)); s["approval"] = {"fingerprint": G.fingerprint(s), "date": now(), "rules_version": G.rules_version()}
        json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)
        ex = os.path.join(os.path.dirname(sp), "_exemplar.md")
        if not os.path.exists(ex):
            import review as RV
            open(ex, "w").write(f"# Hub exemplar: {url}\n\nThe first page in this hub to pass review and be approved by Divit ({now()}). "
                                "Writers read it before writing: match its standard, not its words (QC D1/D2 block copied sentences).\n\n" + RV.page(url) + "\n")
            print(f"hub exemplar written: {os.path.relpath(ex, ROOT)}")
    note = args[args.index("--note") + 1] if "--note" in args else None
    by = args[args.index("--by") + 1] if "--by" in args else None
    if state == "qc_pass":
        # code QC must be TOTAL 0 before a page can enter qc_pass (handover 2026-10-08 3.8: a writer set it at TOTAL 1); no bypass
        if not os.path.exists(spath(url)): sys.exit(f"no spec for {url}: cannot set qc_pass")
        r = subprocess.run([sys.executable, os.path.join(ROOT, "qc", "qc_hub.py"), spath(url)], capture_output=True, text=True)
        if r.returncode != 0:
            ids = sorted({m.group(2) for m in re.finditer(r"^  (P0|P1) (\S+)", r.stdout, re.M)})
            sys.exit(f"refused: QC TOTAL is not 0 for {url}; failing checks: {', '.join(ids) or 'unknown (run hubctl qc)'}")
    if state == "qc_pass" and by:
        sp = spath(url); s = json.load(open(sp))
        if by not in s.setdefault("writers", []): s["writers"].append(by); json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)
    set_state(url, state, note, by=by); print(f"{url} -> {state}")

def cmd_release(args):
    url = args[0]; note = args[args.index("--note") + 1] if "--note" in args else None
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    hub = hub_of(url)
    with G.lock("status-" + hub):
        st = load_st(hub); cur = st["pages"].get(url, {}).get("state")
        if cur not in ("claimed", "spec"): sys.exit(f"refused: release is allowed only from claimed or spec; {url} is '{cur or 'queued'}'")
        del st["pages"][url]; save_st(hub, st)
    cmd_log([hub, f"released {url} (was {cur}) to the planned queue; spec file left in place" + (f": {note}" if note else "")])
    print(f"{url}: {cur} -> queued")

def cmd_paa(args):
    sys.path.insert(0, os.path.join(ROOT, "qc")); import paa_gate
    return paa_gate.main(args)

def cmd_paa_synonyms(args):
    sys.path.insert(0, os.path.join(ROOT, "qc")); import paa_gate
    return paa_gate.synonym_candidates(args)

def cmd_paa_resource(args):
    sys.path.insert(0, os.path.join(ROOT, "qc")); import paa_gate
    return paa_gate.resource(args[0])

ZW = re.compile("[\u200b\u200c\u200d\u2060\ufeff]|&zwj;|&#8205;|&zwnj;")
EMPTY_P = re.compile(r"<p[^>]*>\s*(?:&nbsp;|\s)*</p>")
def live_urls():
    """Hub pages are live (Divit, 2026-10-08); a child page is live once published."""
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    live = {h["path"] for h in CFG["hubs"].values()} | set(CFG.get("live_child_urls", []))
    live |= {u for u, e in G.all_status().items() if e.get("state") == "published"}
    return live
def export_fields(url, s, live=None):
    """What reaches Webflow: zero-width characters and empty paragraphs stripped (QC S10); links to child pages that are not live
    become plain text and are listed as pending (DECISIONS 2026-10-08). The hub link (K4) is never stripped."""
    live = live_urls() if live is None else live; out = {}; pending = []
    hubs = tuple(h["path"] for h in CFG["hubs"].values())
    a_re = re.compile(r"<a\s+href=(\\?['\"])(?:https?://(?:www\.)?emergent\.sh)?(/[a-z0-9/-]*)\1[^>]*>(.*?)</a>", re.S)
    for k, v in s["fields"].items():
        if not isinstance(v, str): out[k] = v; continue
        v = EMPTY_P.sub("", ZW.sub("", v))
        def _sub(m):
            path = m.group(2).rstrip("/")
            if path in hubs or path in live or not path.startswith(hubs): return m.group(0)
            pending.append({"field": k, "target": path, "anchor": re.sub(r"<[^>]+>", "", m.group(3))}); return m.group(3)
        out[k] = a_re.sub(_sub, v)
    return out, pending

def _field_data(url, sha):
    hub = hub_of(url); h = CFG["hubs"][hub]; s = json.load(open(spath(url))); fd = {}
    ex, pend = export_fields(url, s); _record_pending(url, pend)
    for k, v in ex.items():
        if v is None or (v == "" and k in CFG["optional_fields"]): continue
        fd[h["fields"][k]] = v
    for k, im in s["images"].items():
        if im.get("path"):
            if not os.path.exists(os.path.join(ROOT, im["path"])): sys.exit(f"image missing on disk: {im['path']}")
            fd[h["fields"][k]] = {"url": f"{REPO_RAW}/{sha}/{im['path']}", "alt": im["alt"]}
    assert fd.get("name") and fd.get("slug"), f"{url}: name (h1) and slug are required"
    return s, fd

def cmd_bulk_payload(args):
    hub = args[0]; sha = args[args.index("--sha") + 1]; h = CFG["hubs"][hub]; st = load_st(hub); items = []
    sys.path.insert(0, os.path.join(ROOT, "ops")); sys.path.insert(0, os.path.join(ROOT, "plan")); import guards as G, serp as S, datetime as _dt
    for url, e in sorted(st["pages"].items(), key=lambda x: x[1].get("queue_rank", 0)):
        if e.get("state") != "approved": continue
        s, fd = _field_data(url, sha)
        if s.get("item_id"): continue
        if not s.get("approval") or G.fingerprint(s) != s["approval"]["fingerprint"]:
            sys.exit(f"{url}: content or images changed after Divit approved it. Re-run review and approval.")
        chk = e.get("cms_checked")
        if not chk or (_dt.datetime.now(_dt.timezone.utc) - _dt.datetime.strptime(chk, "%Y-%m-%d %H:%M UTC").replace(tzinfo=_dt.timezone.utc)).total_seconds() > 3600:
            sys.exit(f"{url}: no slug check in the last hour. Read the collection to disk and run hubctl cms-check {hub} <readback.json> first.")
        if e.get("cms_exists"): sys.exit(f"{url}: an item with this slug already exists in Webflow ({e.get('cms_item_id')}); it would be duplicated. Record it with hubctl record, or delete the stray item first.")
        live = S.load(url)
        if live and (_dt.date.today() - _dt.date.fromisoformat(live["fetched"])).days > 60: sys.exit(f"{url}: SERP data is older than 60 days; re-pull it and re-run QC before creating")
        items.append({"isDraft": True, "fieldData": fd})
    if not items: sys.exit("no approved pages without an item ID")
    os.makedirs(os.path.join(ROOT, "ops", "out"), exist_ok=True)
    for i in range(0, len(items), 100):
        out = os.path.join(ROOT, "ops", "out", f"{h['repo_dir']}-create-{i//100+1}.json")
        json.dump([{"label": f"create {hub} {i+1}-{i+len(items[i:i+100])}", "create_collection_items": {"collection_id": h["collection_id"], "request": {"items": items[i:i+100]}}}], open(out, "w"), indent=1, ensure_ascii=False)
        print(f"wrote {os.path.relpath(out, ROOT)} ({len(items[i:i+100])} drafts)")

def cmd_bulk_verify(args):
    hub, rb = args[0], args[1]; h = CFG["hubs"][hub]; st = load_st(hub); by_slug = {it["fieldData"].get("slug"): it for it in _items_from_readback(rb)}
    ok = bad = 0
    for url, e in st["pages"].items():
        if e.get("state") not in ("approved", "cms_draft"): continue
        it = by_slug.get(url.rsplit("/", 1)[1])
        if not it: continue
        s = json.load(open(spath(url))); fd = it["fieldData"]; diff = []
        for k, v in export_fields(url, s)[0].items():
            if v in (None, "") and k in CFG["optional_fields"]: continue
            if fd.get(h["fields"][k]) != v: diff.append(k)
        for k, im in s["images"].items():
            got = fd.get(h["fields"][k]) or {}
            if not got.get("fileId"): diff.append(f"{k} (no fileId)")
            else: im["file_id"] = got["fileId"]; im["cdn_url"] = got.get("url")
        if diff: bad += 1; print(f"MISMATCH {url}: {diff}"); continue
        s["item_id"] = it["id"]; json.dump(s, open(spath(url), "w"), indent=1, ensure_ascii=False)
        set_state(url, "cms_draft", item_id=it["id"]); ok += 1
    print(f"verified and recorded {ok}; mismatched {bad}"); sys.exit(1 if bad else 0)

def cmd_next(args):
    state = args[0]; hubs = [args[1]] if len(args) > 1 else list(CFG["hubs"])
    for hub in hubs:
        for url, e in sorted(load_st(hub)["pages"].items(), key=lambda x: x[1].get("queue_rank", 0)):
            if e.get("state") == state: print(f"{hub:10s} #{e.get('queue_rank','-'):<4} {url}  {e.get('note','')}")

def cmd_serp_save(args):
    url, raw = args[0], args[1]; kw = args[2] if len(args) > 2 else None
    sys.path.insert(0, os.path.join(ROOT, "plan")); import serp as S
    try: rawj = json.load(open(raw))
    except ValueError: rawj = open(raw).read()
    p, n = S.save(url, rawj, kw)
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G; used = G.budget_use()
    print(f"(DataForSEO calls today: {used})")
    print(f"saved {os.path.relpath(p, ROOT)}: {len(n['paa'])} PAA questions, {len(n['related'])} related searches, {len(n['organic'])} organic, features {n['features']}")

def cmd_serp_keywords(args):
    sys.path.insert(0, os.path.join(ROOT, "plan")); import serp as S
    try: rawj = json.load(open(args[1]))
    except ValueError: rawj = open(args[1]).read()
    p, n = S.save(args[0], rawj, merge=True)
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G; used = G.budget_use()
    print(f"(DataForSEO calls today: {used})")
    print(f"added {len(n['keywords'])} keyword ideas to {os.path.relpath(p, ROOT)}")

def cmd_serp_status(args):
    sys.path.insert(0, os.path.join(ROOT, "plan")); import serp as S
    hubs = [args[0]] if args else list(CFG["hubs"]); n = 0
    for hub in hubs:
        for url, e in load_st(hub)["pages"].items():
            if e.get("state") in ("claimed", "spec", "rework") and not S.load(url): print(f"needs SERP  {url}"); n += 1
    print(f"{n} page(s) need a live SERP")

def cmd_table(args):
    url = args[0]; vs = [x.strip() for x in args[args.index("--vs") + 1].split(",")]; rows = [x.strip() for x in args[args.index("--rows") + 1].split(",")]
    sys.path.insert(0, os.path.join(ROOT, "ops")); import table as TB
    variant = args[args.index("--variant") + 1] if "--variant" in args else None
    d = CFG["hubs"][hub_of(url)]["repo_dir"]; html = TB.render(d, vs, rows, variant)
    sp = spath(url); s = json.load(open(sp)); s["fields"]["why_table"] = html; s["table"] = {"vs": vs, "rows": rows, "variant": variant}
    json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)
    old = TB.stale(d, vs, rows)
    print(f"table written to {os.path.relpath(sp, ROOT)}: Emergent vs {', '.join(vs)}; rows {', '.join(rows)}")
    for o in old: print("  STALE (re-check before use):", o)

def cmd_library(args):
    sys.path.insert(0, os.path.join(ROOT, "ops")); import table as TB, datetime
    d = CFG["hubs"][args[0]]["repo_dir"]; L = TB.lib(d)
    print(f"{args[0]} library, updated {L['updated']}. Dimensions: " + "; ".join(f"{k} ({' / '.join(v)})" for k, v in L["dimensions"].items()))
    for name, c in L["competitors"].items():
        ages = [(datetime.date.today() - datetime.date.fromisoformat(f["checked"])).days for f in c["facts"].values()]
        print(f"  {name:36s} {','.join(c['categories']):28s} facts: {', '.join(c['facts'])}  (oldest check {max(ages)} days)")

def cmd_cms_check(args):
    """Record, from a stored read-back of the whole collection, whether each queued page's slug already exists in Webflow."""
    hub, rb = args[0], args[1]; items = _items_from_readback(rb)
    by_slug = {it.get("fieldData", {}).get("slug"): it for it in items}
    if not items: sys.exit("no items found in the read-back; read the full collection (list_collection_items, all pages) to disk first")
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    with G.lock("status-" + hub):
        st = load_st(hub); n = 0
        for url, e in st["pages"].items():
            it = by_slug.get(url.rsplit("/", 1)[1])
            e["cms_checked"] = now(); e["cms_exists"] = bool(it); e["cms_item_id"] = it["id"] if it else None; n += 1
        save_st(hub, st)
    print(f"slug check recorded for {n} pages against {len(items)} Webflow items; existing: {[u for u, e in st['pages'].items() if e.get('cms_exists')]}")

def cmd_usage_log(args):
    url, tokens = args[0], args[1]; role = args[args.index("--role") + 1] if "--role" in args else "agent"
    agent = args[args.index("--agent") + 1] if "--agent" in args else ""
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G; G.usage_log(url, tokens, role, agent); print(f"logged {tokens} tokens ({role}) for {url}")

FUNC_WORDS = {"a", "an", "the", "that", "which", "with", "for", "to", "of", "in", "on", "by", "and", "or", "before", "after", "every", "each",
              "your", "its", "it", "from", "into", "when", "who", "one", "all", "any", "no"}
def heading_shape(h):
    out = []
    for w in re.findall(r"[a-z0-9']+", re.sub(r"<[^>]+>", " ", h or "").lower())[:7]:
        t = "a" if w in ("a", "an") else (w if w in FUNC_WORDS else "X")
        if not (t == "X" and out and out[-1] == "X"): out.append(t)
    return " ".join(out[:4])   # the opening shape is what a reader hears as a formula
def cmd_plan_check(args):
    """Compare this page's plan and tab headings with every other spec in the hub: shared heading shapes, near-identical tab stories."""
    url = args[0]; s = json.load(open(spath(url))); hub = hub_of(url); plan = s.get("plan") or {}
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    mine_h = [re.search(r"<h3[^>]*>(.*?)</h3>", s["fields"].get(f"tab_content_{i}", "") or "", re.S) for i in range(1, 5)]
    mine_h = [m.group(1) for m in mine_h if m]
    shapes = [heading_shape(x) for x in mine_h] + [heading_shape(x) for x in plan.get("heading_shapes", [])]
    def words(t): return {w for w in re.findall(r"[a-z]+", (t or "").lower()) if w not in FUNC_WORDS and len(w) > 3}
    issues = 0
    if len(set(heading_shape(x) for x in mine_h)) < len(mine_h): print(f"WARN own tab headings share a shape: {[heading_shape(x) for x in mine_h]}"); issues += 1
    for o in G.all_specs():
        if o["url"] == url or o.get("hub") != hub: continue
        oh = [re.search(r"<h3[^>]*>(.*?)</h3>", o["fields"].get(f"tab_content_{i}", "") or "", re.S) for i in range(1, 5)]
        osh = {heading_shape(m.group(1)) for m in oh if m}
        same = sorted(set(shapes) & osh)
        if same: print(f"WARN heading shape shared with {o['url']}: {same}"); issues += 1
        for i, st_ in enumerate(plan.get("tab_stories", []), 1):
            for j, ost in enumerate((o.get("plan") or {}).get("tab_stories", []), 1):
                a, b = words(st_), words(ost)
                if a and b and len(a & b) / len(a | b) > 0.4: print(f"WARN tab story {i} is close to {o['url']} tab {j}: {sorted(a & b)[:8]}"); issues += 1
        print(f"sibling {o['url']}: angle={((o.get('plan') or {}).get('angle') or '-')[:90]} | tab H3 shapes={sorted(osh)}")
    print(f"plan-check {url}: {issues} warning(s)"); sys.exit(1 if issues else 0)

def cmd_sources_check(args):
    """Check every spec.domain_sources URL of a page (or --all in-progress pages) and cache the result for QC P3."""
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    specs = [json.load(open(spath(args[0])))] if args and args[0] != "--all" else [s for s in G.all_specs() if s.get("status") not in ("live-draft", "published")]
    bad = 0
    for s in specs:
        urls = sorted({d["source_url"] for d in s.get("domain_sources", []) if d.get("source_url")})
        for u, r in G.check_links(urls).items():
            if r["status"] != "ok": print(f"{r['status'].upper():8s} {r.get('code')} {u}" + (f" -> {r['final']}" if r["status"] == "moved" else "")); bad += r["status"] in ("dead", "moved")
        print(f"{s['url']}: {len(urls)} sources checked")
    sys.exit(1 if bad else 0)

PACK_RULES = {"writer": ["2", "2a", "2b", "5", "6", "8"], "reviewer": ["2a", "2b", "5", "6", "8"]}
def cmd_pack(args):
    """One compact file per role: the brief, the rules that role needs, a one-line catalogue, the exemplar excerpt."""
    url = args[0]; role = args[args.index("--role") + 1] if "--role" in args else "writer"
    if role not in PACK_RULES: sys.exit(f"role must be one of {list(PACK_RULES)}")
    hub = hub_of(url); d = CFG["hubs"][hub]["repo_dir"]; slug = url.rsplit("/", 1)[1]
    brief = subprocess.run([sys.executable, os.path.join(ROOT, "ops", "hubctl.py"), "brief", url], capture_output=True, text=True).stdout
    hr = open(os.path.join(ROOT, "rules", "HUB_RULES.md")).read()
    secs = re.split(r"(?m)^(?=## )", hr); keep = [x for x in secs if re.match(r"## (\d+[a-z]?)\.", x) and re.match(r"## (\d+[a-z]?)\.", x).group(1) in PACK_RULES[role]]
    cat = []
    for row in re.findall(r"(?m)^\| (\d+) \| ([^|]+)\|[^|]*\|[^|]*\| ([^|]+)\| ([^|]+)\|", open(os.path.join(ROOT, "rules", "CONTENT_DEFECTS.md")).read()):
        cat.append(f"- #{row[0]} {row[1].strip()} ({row[2].strip()}; {row[3].strip()})")
    ex = os.path.join(ROOT, "specs", d, "_exemplar.md"); exc = open(ex).read() if os.path.exists(ex) else ""
    exc = (" ".join(exc.split()[:900]) + " ...") if exc else "(no exemplar yet for this hub)"
    out = [f"# {role.title()} pack: {url}", "", "Read this pack and the spec (`" + os.path.relpath(spath(url), ROOT) + "`). It replaces the full rulebook for this task.", ""]
    if role == "writer":
        out += ["## Your job", "Plan first (spec.plan, `hubctl plan-check`), then write. At most 8 domain_sources, primary sources, from search snippets where they suffice; `hubctl sources-check <url>` verifies the links. On rework, fix BLOCKING findings only, each as a class across the page; notes never trigger edits. Run `hubctl qc` to TOTAL 0, then `hubctl state <url> qc_pass --by <id>`.", ""]
    else:
        rub = json.load(open(os.path.join(ROOT, "rules", "rubric.json")))["criteria"]
        out += ["## Rubric", *[f"- **{c['id']}**: {c['test']}" for c in rub], "",
                "## Findings", "Each finding: criterion, rule (HUB_RULES section or CONTENT_DEFECTS row), field, quote, issue, fix, severity. A defect is a rule violation; taste is not a finding.",
                "Every finding also names its `class` from the severity table below; the class decides blocking or note. Notes ship and never trigger rework; they feed the proposed-rules queue. There is one review per page.", "",
                open(os.path.join(ROOT, "rules", "SEVERITY.md")).read(),
                "Source liveness is the automated link check (`hubctl sources-check`); do not re-open sources to test them, only to check what a stretched claim says.", ""]
    out += ["## Brief", "```", brief.strip(), "```", "", "## Rules (HUB_RULES, the sections this role needs)", *[x.strip() + "\n" for x in keep],
            "## Defect catalogue (one line per row; full rows in rules/CONTENT_DEFECTS.md)", *cat, "", "## Hub exemplar (excerpt)", exc, ""]
    if role == "writer":
        out += ["## Image brief", open(os.path.join(ROOT, "docs", "IMAGE_BRIEF.md")).read()]
    p = os.path.join(ROOT, ".cache", "packs", f"{slug}.{role}.md"); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write("\n".join(out))
    print(f"{os.path.relpath(p, ROOT)}  ({len(chr(10).join(out).split())} words)")

def cmd_metrics(args):
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    m = G.metrics(); print(json.dumps(m, indent=1))

def cmd_sample(args):
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    state = args[0] if args else "reviewed"
    urls = [u for u, e in G.all_status().items() if e.get("state") == state]
    for u, why in G.sample(urls): print(f"{u}  <- {', '.join(why)}")

def cmd_links(args):
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    if "--relink" in args:
        live = live_urls(); n = 0
        for s in G.all_specs():
            ready = sorted({p["target"] for p in s.get("pending_links") or [] if p["target"] in live})
            if ready: n += 1; print(f"  {s['url']}: re-link {', '.join(ready)} (rebuild its payload; the link is now live)")
        print(f"pages to update: {n}"); return
    hub = args[0]; g = G.link_graph(); print("Pages needing inbound links (fewest first):")
    for u, n in G.needs_links(hub, 15): print(f"  {n} inbound  {u}")

def cmd_lookahead(args):
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    hub, n = args[0], int(args[1]) if len(args) > 1 else 50
    for url, have, missing in G.lookahead(hub, n, kmap()):
        if len(have) < 3: print(f"{url}: library has {have or 'none'} of its top 10; research: {missing}")

def cmd_serp_budget(args):
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    left, cap = G.budget_left(); print(f"DataForSEO calls left today: {left} of {cap}"); sys.exit(0 if left > 0 else 1)

def cmd_ranks_save(args):
    url, raw = args[0], args[1]; sys.path.insert(0, os.path.join(ROOT, "ops")); sys.path.insert(0, os.path.join(ROOT, "plan")); import guards as G, serp as S
    try: data = json.load(open(raw))
    except ValueError: data = open(raw).read()
    items = [d for d in S._walk(S._parse_text(data)) if isinstance(d, dict) and d.get("type") == "organic"]
    pos, purl = G.rank_from_serp(items); d = os.path.join(ROOT, "private", "ranks"); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, url.strip("/").replace("/", "__") + ".jsonl"), "a") as f: f.write(json.dumps({"date": now(), "position": pos, "url": purl}) + "\n")
    G.budget_use(); print(f"{url}: position {pos or 'not in the top 100'}")

def cmd_ranks_report(args):
    import datetime as _dt
    d = os.path.join(ROOT, "private", "ranks"); refresh = []
    for s in glob.glob(os.path.join(ROOT, "specs", "*", "*.json")):
        sp = json.load(open(s)); pub = next((ev["t"] for ev in sp.get("history", []) if ev.get("state") == "published"), None)
        if not pub: continue
        age = (_dt.datetime.now(_dt.timezone.utc) - _dt.datetime.strptime(pub, "%Y-%m-%d %H:%M UTC").replace(tzinfo=_dt.timezone.utc)).days
        f = os.path.join(d, sp["url"].strip("/").replace("/", "__") + ".jsonl")
        pos = [json.loads(l)["position"] for l in open(f)] if os.path.exists(f) else []
        best = min([p for p in pos if p] or [999])
        if age >= 56 and best > 20: refresh.append((sp["url"], age, best if best < 999 else None))
    for u, age, best in refresh: print(f"REFRESH {u}: live {age} days, best position {best or 'none in top 100'}")
    print(f"{len(refresh)} page(s) for the refresh queue")

def cmd_recheck(args):
    """Ratchet: re-run QC on every page that passed under an older version of the rules; failures go to rework (or the fix queue if live)."""
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G
    cur = G.rules_version(); fixq = []; n = ok = 0
    only = set(args[args.index("--states") + 1].split(",")) if "--states" in args else None  # e.g. images,reviewed,...: parked pages stay parked
    for s in G.all_specs():
        if s.get("status") == "live-draft" or not s.get("qc_passed") or s["qc_passed"].get("rules_version") == cur: continue
        st_ = G.all_status().get(s["url"], {}).get("state")
        if only is not None and st_ not in only: continue
        r = subprocess.run([sys.executable, os.path.join(ROOT, "qc", "qc_hub.py"), s["_path"]], capture_output=True, text=True); rc = r.returncode; n += 1
        if rc: print(f"  FAIL {s['url']} ({st_}): " + ",".join(sorted({m.group(2) for m in re.finditer(r"^  (P0|P1) (\S+)", r.stdout, re.M)})))
        else: ok += 1
        if rc == 0:
            sp = json.load(open(s["_path"])); sp["qc_passed"] = {"rules_version": cur, "date": now()}; json.dump(sp, open(s["_path"], "w"), indent=1, ensure_ascii=False)
        elif st_ in ("published", "cms_draft"): fixq.append(s["url"])
        else: set_state(s["url"], "rework", note=f"rules changed ({cur}); QC now fails", via="recheck")
    json.dump({"rules_version": cur, "date": now(), "pages": fixq}, open(os.path.join(ROOT, "status", "fix_queue.json"), "w"), indent=1)
    print(f"recheck done at rules {cur}: {n} pages re-checked, {ok} at TOTAL 0; live pages needing a fix: {len(fixq)}")

def cmd_image_regress(args):
    """Approved and live pages must re-render byte-identically with the current engine."""
    sys.path.insert(0, os.path.join(ROOT, "ops")); sys.path.insert(0, os.path.join(ROOT, "pipeline")); import guards as G, engine
    bad = 0; n = 0
    for s in G.all_specs():
        if not s.get("approval"): continue
        out, issues, _ = engine.build_all(s); n += 1
        for rel, content in out:
            if rel.endswith(".svg") and os.path.exists(os.path.join(ROOT, rel)) and open(os.path.join(ROOT, rel)).read() != content:
                bad += 1; print(f"CHANGED {rel}")
    print(f"image regression: {n} approved page(s) checked, {bad} file(s) would change"); sys.exit(1 if bad else 0)

def cmd_verify_live(args):
    sys.path.insert(0, os.path.join(ROOT, "ops")); import verify_live as V
    url = args[0]; html = open(args[args.index("--html") + 1]).read() if "--html" in args else None
    ok, report = V.verify(json.load(open(spath(url))), html, check_links=("--html" not in args)); print("\n".join(report))
    if ok: set_state(url, "published", note="live page verified", via="verify-live")
    sys.exit(0 if ok else 1)

def _engine():
    sys.path.insert(0, os.path.join(ROOT, "pipeline")); import engine; return engine

def _hold():
    h = CFG.get("images_on_hold")
    if h: sys.exit(f"images are on hold since {h['since']}: {h['why']}")

def cmd_images(args):
    _hold(); url = args[0]; ok = _engine().render_spec(spath(url))
    if ok: set_state(url, "images")
    sys.exit(0 if ok else 1)

def cmd_images_batch(args):
    _hold(); state = args[0]; hubs = [args[1]] if len(args) > 1 else list(CFG["hubs"]); eng = _engine(); done = bad = 0
    for hub in hubs:
        for url, e in sorted(load_st(hub)["pages"].items(), key=lambda x: x[1].get("queue_rank", 0)):
            if e.get("state") != state: continue
            if eng.render_spec(spath(url)): set_state(url, "images"); done += 1
            else: set_state(url, "rework", note="image brief blocked: see engine output"); bad += 1
    print(f"rendered {done}; sent back to rework {bad}")

def cmd_publish_payload(args):
    hub = args[0]; h = CFG["hubs"][hub]; st = load_st(hub); ids = []
    for url, e in st["pages"].items():
        if e.get("state") == "cms_draft":          # created as drafts after Divit's approval, verified
            s = json.load(open(spath(url)))
            if s.get("item_id"): ids.append(s["item_id"])
    if not ids: sys.exit("no verified cms_draft pages to publish")
    # FAQ links must never point at a page that is not live (or publishing in this batch)
    batch = {url for url, e in st["pages"].items() if e.get("state") == "cms_draft"}
    live = set()
    for hk in CFG["hubs"]:
        live |= {u for u, e in load_st(hk)["pages"].items() if e.get("state") == "published"}
    live |= {json.load(open(f)).get("url") for f in glob.glob(os.path.join(ROOT, "specs", "*", "*.json")) if json.load(open(f)).get("status") == "live-draft"}
    for url in sorted(batch):
        s_ = json.load(open(spath(url))); bad = []
        for u in re.findall(r"<a href=(?:\\?\"|')https://emergent\.sh([^\"'\\]+)", s_["fields"].get("faq", "")):
            u = u.rstrip("/")
            if u in {v["path"] for v in CFG["hubs"].values()}: continue
            if u not in live and u not in batch: bad.append(u)
        if bad: print(f"WARNING {url} links to pages not live yet: {bad}. Hold it, or publish those first.", file=sys.stderr)
    for i in range(0, len(ids), 100):
        print(json.dumps([{"label": f"publish {hub} batch {i//100+1}", "publish_collection_items": {"collection_id": h["collection_id"], "request": {"items": [{"id": x} for x in ids[i:i+100]]}}}], indent=1))

def cmd_log(args):
    hub, text = args[0], " ".join(args[1:]); p = os.path.join(ROOT, "logs", f"{CFG['hubs'][hub]['repo_dir']}.md")
    with open(p, "a") as f: f.write(f"- {now()}: {text}\n")
    print(f"logged to {os.path.relpath(p, ROOT)}")

CMDS = {"status": cmd_status, "claim": cmd_claim, "brief": cmd_brief, "init": cmd_init, "qc": cmd_qc, "payload": cmd_payload,
        "verify": cmd_verify, "record": cmd_record, "state": cmd_state, "release": cmd_release, "paa": cmd_paa, "paa-resource": cmd_paa_resource, "paa-synonyms": cmd_paa_synonyms, "publish-payload": cmd_publish_payload, "log": cmd_log,
        "bulk-payload": cmd_bulk_payload, "bulk-verify": cmd_bulk_verify, "next": cmd_next, "images": cmd_images, "images-batch": cmd_images_batch, "serp-save": cmd_serp_save, "serp-status": cmd_serp_status, "table": cmd_table, "library": cmd_library, "serp-keywords": cmd_serp_keywords, "review": cmd_review, "verified": cmd_verified, "challenge": cmd_challenge, "ready": cmd_ready, "export-csv": cmd_export_csv, "cms-check": cmd_cms_check, "metrics": cmd_metrics, "usage-log": cmd_usage_log, "sources-check": cmd_sources_check, "pack": cmd_pack, "plan-check": cmd_plan_check, "sample": cmd_sample, "links": cmd_links,
        "lookahead": cmd_lookahead, "serp-budget": cmd_serp_budget, "ranks-save": cmd_ranks_save, "ranks-report": cmd_ranks_report,
        "recheck": cmd_recheck, "image-regress": cmd_image_regress, "verify-live": cmd_verify_live}
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS: print(__doc__); sys.exit(0)
    try:
        sys.exit(CMDS[sys.argv[1]](sys.argv[2:]) or 0)
    except (IndexError, ValueError):
        print(f"usage error for '{sys.argv[1]}'.\n" + __doc__); sys.exit(2)
