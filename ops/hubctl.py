"""hubctl.py: the one tool every build-hub chat uses. Run from the repo root.

  status [HUB]                      queue and state counts (all hubs, or one)
  claim HUB N --by CHAT             claim the next N unclaimed pages of HUB in queue order
  brief URL                         keyword brief for a page (needs plan/keyword_map.json)
  init URL                          create the spec skeleton specs/<dir>/<slug>.json
  qc URL                            run qc/qc_hub.py on that page's spec
  state URL STATE [--note TEXT]     move a page to a new state (see STATES)
  payload URL --sha SHA             write ops/out/<slug>.payload.json: the exact data_cms_tool action
  verify URL READBACK.json          diff a stored CMS read-back against the spec (exit 1 on mismatch)
  record URL --item-id ID [--file-id FIELD=ID ...]   store Webflow IDs after a create/import
  bulk-payload HUB --sha SHA        create_collection_items actions (100 items per action) for every approved page without an item ID
  bulk-verify HUB READBACK.json     verify every page of HUB found in a stored read-back; records item IDs and file IDs
  next STATE [HUB]                  list pages waiting in a state (for orchestrators and reviewers)
  publish-payload HUB               publish_collection_items actions (100 per call) for every verified cms_draft page (only after Divit's go)
  log HUB TEXT                      append a dated line to logs/<hub>.md

HUB is one of LP, Form, Auto, SurveyQuiz. Status lives in status/<hub>.json; each hub chat writes only its own.
"""
import json, os, sys, re, glob, datetime, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))
STATES = ["claimed", "spec", "qc_pass", "reviewed", "rework", "images", "approved", "cms_draft", "published", "parked"]
# content-first pipeline: claimed -> spec -> qc_pass (code QC = 0) -> reviewed (independent reviewer) -> images (rendered + gated)
#   -> approved (Divit: calibration batch in full, then daily sample) -> cms_draft (bulk create) -> published (bulk publish). rework sends a page back to its writer.
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
    spec = {"url": url, "hub": hub, "item_id": None, "status": "spec",
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

def cmd_state(args):
    url, state = args[0], args[1]
    if state not in STATES: sys.exit(f"state must be one of {STATES}")
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

def cmd_publish_payload(args):
    hub = args[0]; h = CFG["hubs"][hub]; st = load_st(hub); ids = []
    for url, e in st["pages"].items():
        if e.get("state") == "cms_draft":          # created as drafts after Divit's approval, verified
            s = json.load(open(spath(url)))
            if s.get("item_id"): ids.append(s["item_id"])
    if not ids: sys.exit("no verified cms_draft pages to publish")
    for i in range(0, len(ids), 100):
        print(json.dumps([{"label": f"publish {hub} batch {i//100+1}", "publish_collection_items": {"collection_id": h["collection_id"], "request": {"items": [{"id": x} for x in ids[i:i+100]]}}}], indent=1))

def cmd_log(args):
    hub, text = args[0], " ".join(args[1:]); p = os.path.join(ROOT, "logs", f"{CFG['hubs'][hub]['repo_dir']}.md")
    with open(p, "a") as f: f.write(f"- {now()}: {text}\n")
    print(f"logged to {os.path.relpath(p, ROOT)}")

CMDS = {"status": cmd_status, "claim": cmd_claim, "brief": cmd_brief, "init": cmd_init, "qc": cmd_qc, "payload": cmd_payload,
        "verify": cmd_verify, "record": cmd_record, "state": cmd_state, "publish-payload": cmd_publish_payload, "log": cmd_log,
        "bulk-payload": cmd_bulk_payload, "bulk-verify": cmd_bulk_verify, "next": cmd_next}
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS: print(__doc__); sys.exit(0)
    sys.exit(CMDS[sys.argv[1]](sys.argv[2:]) or 0)
