"""hubctl.py: the one tool every build-hub chat uses. Run from the repo root.

  status [HUB]                      queue and state counts (all hubs, or one)
  claim HUB N --by CHAT             claim the next N unclaimed pages of HUB in queue order
  brief URL                         keyword brief for a page (needs plan/keyword_map.json)
  init URL --by WRITER-ID           create the spec skeleton specs/<dir>/<slug>.json, recording who writes it
  qc URL                            run qc/qc_hub.py on that page's spec
  state URL STATE [--note TEXT]     move a page to a new state (see STATES); 'reviewed' needs a passing rubric
  verified URL                      Divit approved the page as rendered in the real Webflow template: it joins the width calibration
  review URL RUBRIC.json --by ID    record the reviewer's scored rubric (page must be in state images); all pass -> reviewed, any fail -> rework
  challenge URL FINDINGS.json --by ID   record the adversarial pass (page must be reviewed); no defects -> challenged, any -> rework
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
  publish-payload HUB               publish_collection_items actions (100 per call) for every verified cms_draft page (only after Divit's go)
  log HUB TEXT                      append a dated line to logs/<hub>.md

HUB is one of LP, Form, Auto, SurveyQuiz. Status lives in status/<hub>.json; each hub chat writes only its own.
"""
import json, os, sys, re, glob, datetime, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))
STATES = ["claimed", "spec", "qc_pass", "images", "reviewed", "challenged", "approved", "rework", "cms_draft", "published", "parked"]
# pipeline: claimed -> spec -> qc_pass (code QC = 0) -> images (rendered + gated) -> reviewed (independent reviewer, rubric 10/10)
#   -> challenged (independent adversarial pass, zero defects) -> approved (Divit) -> cms_draft -> published. rework sends a page back to its writer.
# The writer, the reviewer and the challenger must be three different agents (enforced here and in QC R1/R2).
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
def set_state(url, state, note=None, **extra):
    hub = hub_of(url); st = load_st(hub); e = st["pages"].setdefault(url, {})
    e.update({"state": state, "updated": now(), **extra})
    if note: e["note"] = note
    save_st(hub, st)

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
    return subprocess.call([sys.executable, os.path.join(ROOT, "qc", "qc_hub.py"), spath(args[0])])

def cmd_payload(args):
    url = args[0]; sha = args[args.index("--sha") + 1]; hub = hub_of(url); h = CFG["hubs"][hub]
    s = json.load(open(spath(url))); fd = {}
    for k, v in s["fields"].items():
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
    for k, v in s["fields"].items():
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

def cmd_review(args):
    url, rf = args[0], args[1]; by = args[args.index("--by") + 1] if "--by" in args else "reviewer"
    rub = json.load(open(rf)); RUB = json.load(open(os.path.join(ROOT, "rules", "rubric.json")))["criteria"]
    missing = [c["id"] for c in RUB if c["id"] not in rub]
    if missing: sys.exit(f"rubric incomplete, score every criterion: {missing}")
    for k, v in rub.items():
        if v.get("result") not in ("pass", "fail") or not v.get("evidence"): sys.exit(f'"{k}" needs result pass|fail and one line of evidence')
    sp = spath(url); s = json.load(open(sp))
    st_now = load_st(hub_of(url))["pages"].get(url, {}).get("state")
    if st_now != "images": sys.exit(f"review needs the page in state 'images' (QC passed and images rendered); it is '{st_now}'")
    if by == s.get("written_by"): sys.exit("the reviewer cannot be the agent that wrote the page")
    s["review"] = {"by": by, "date": now(), "rubric": rub}; s.pop("challenge", None); json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)
    fails = [f"{k}: {v['evidence']}" for k, v in rub.items() if v["result"] == "fail"]
    if fails: set_state(url, "rework", note=" | ".join(fails)); print("REWORK:\n  " + "\n  ".join(fails))
    else: set_state(url, "reviewed", note=f"rubric 10/10 by {by}"); print("REVIEWED: rubric 10/10")

def cmd_verified(args):
    url = args[0]; sp = spath(url); s = json.load(open(sp)); s["render_verified"] = now(); json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)
    sys.path.insert(0, os.path.join(ROOT, "ops")); import typeset as TS; TS.calibrate()
    print(f"{url} marked as verified in the template; width ceilings recalibrated with it")

def cmd_challenge(args):
    url, ff = args[0], args[1]; by = args[args.index("--by") + 1] if "--by" in args else "challenger"
    sp = spath(url); s = json.load(open(sp)); f = json.load(open(ff))
    st_now = load_st(hub_of(url))["pages"].get(url, {}).get("state")
    if st_now != "reviewed": sys.exit(f"challenge needs the page in state 'reviewed'; it is '{st_now}'")
    if by in (s.get("written_by"), (s.get("review") or {}).get("by")): sys.exit("the challenger must be a different agent from the writer and the reviewer")
    if not isinstance(f.get("defects"), list) or not f.get("checked"): sys.exit('findings need "defects": [...] (empty if none) and "checked": [what was examined, section by section]')
    defects = [f"{d.get('field', '?')}: {d.get('issue', '')} -> {d.get('fix', '')}" for d in f["defects"]]
    s["challenge"] = {"by": by, "date": now(), "result": "fail" if defects else "pass", "defects": defects, "checked": f["checked"]}
    json.dump(s, open(sp, "w"), indent=1, ensure_ascii=False)
    if defects: set_state(url, "rework", note=" | ".join(defects)); print("REWORK:\n  " + "\n  ".join(defects))
    else: set_state(url, "challenged", note=f"no defects found by {by}"); print("CHALLENGED: no defects found")

def cmd_state(args):
    url, state = args[0], args[1]
    if state not in STATES: sys.exit(f"state must be one of {STATES}")
    if state in ("reviewed", "challenged"): sys.exit(f"'{state}' is set only by hubctl {'review' if state == 'reviewed' else 'challenge'}, never by hand")
    if state == "approved":
        cur = load_st(hub_of(url))["pages"].get(url, {}).get("state")
        if cur != "challenged": sys.exit(f"only a challenged page can be approved (this one is '{cur}')")
    note = args[args.index("--note") + 1] if "--note" in args else None
    set_state(url, state, note); print(f"{url} -> {state}")

def _field_data(url, sha):
    hub = hub_of(url); h = CFG["hubs"][hub]; s = json.load(open(spath(url))); fd = {}
    for k, v in s["fields"].items():
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
    for url, e in sorted(st["pages"].items(), key=lambda x: x[1].get("queue_rank", 0)):
        if e.get("state") != "approved": continue
        s, fd = _field_data(url, sha)
        if s.get("item_id"): continue
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
        for k, v in s["fields"].items():
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
    print(f"saved {os.path.relpath(p, ROOT)}: {len(n['paa'])} PAA questions, {len(n['related'])} related searches, {len(n['organic'])} organic, features {n['features']}")

def cmd_serp_keywords(args):
    sys.path.insert(0, os.path.join(ROOT, "plan")); import serp as S
    try: rawj = json.load(open(args[1]))
    except ValueError: rawj = open(args[1]).read()
    p, n = S.save(args[0], rawj, merge=True); print(f"added {len(n['keywords'])} keyword ideas to {os.path.relpath(p, ROOT)}")

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
        "verify": cmd_verify, "record": cmd_record, "state": cmd_state, "publish-payload": cmd_publish_payload, "log": cmd_log,
        "bulk-payload": cmd_bulk_payload, "bulk-verify": cmd_bulk_verify, "next": cmd_next, "images": cmd_images, "images-batch": cmd_images_batch, "serp-save": cmd_serp_save, "serp-status": cmd_serp_status, "table": cmd_table, "library": cmd_library, "serp-keywords": cmd_serp_keywords, "review": cmd_review, "verified": cmd_verified, "challenge": cmd_challenge}
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS: print(__doc__); sys.exit(0)
    try:
        sys.exit(CMDS[sys.argv[1]](sys.argv[2:]) or 0)
    except (IndexError, ValueError):
        print(f"usage error for '{sys.argv[1]}'.\n" + __doc__); sys.exit(2)
