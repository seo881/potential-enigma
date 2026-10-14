"""The keyword map every tool reads: the clone's git-ignored plan/keyword_map.json, plus the approved additions it lacks.

plan/additions.json (tracked; written by plan/build_map.py) names each page added outside the workbook (ruling 13 new keywords,
Divit 2026-10-14) with url, hub, primary, status, wave and queue_rank only: no Semrush data. A clone whose own map predates the
additions (B's, ~/emergent-hubs-a) gets those pages after a plain git pull, so `hubctl claim` can hand them out. The Semrush fields
(secondaries, MSV, top 10) come from private/semrush/plan-additions-*.json when that file is present (Divit's local rsync);
without it the page carries empty secondaries and no MSV instead of crashing, marked plan_source "additions" (not "+private").
The local map always wins for a URL it already has.

Test hooks (golden cases, simulating B's clone in A's): HUB_KMAP_SIM=no-additions drops the tracked additions from the local map
before merging; HUB_KMAP_SIM=no-additions,no-private also ignores the private additions file.
"""
import glob, json, os

TRACKED = os.path.join("plan", "additions.json")
DEFAULTS = {"tier": None, "display_name": None, "primary_msv": None, "kd": None, "intent": None, "cluster": None, "secondaries": [],
            "total_msv": 0, "verdict": None, "top10_mix": None, "angle": None, "amber_evidence": None, "serp_features": None,
            "top10": [], "pass3_action": None, "notes": None}
FIELDS = ("hub", "primary", "status", "wave", "queue_rank")   # the only per-page fields plan/additions.json may hold

def tracked(root):
    p = os.path.join(root, TRACKED)
    return (json.load(open(p)).get("pages") or {}) if os.path.exists(p) else {}

def private_additions(root):
    add = {}
    for f in sorted(glob.glob(os.path.join(root, "private", "semrush", "plan-additions-*.json"))): add.update(json.load(open(f)))
    return add

def merge(m, root):
    """Add every tracked addition the map lacks (in place); returns m."""
    sim = {s.strip() for s in os.environ.get("HUB_KMAP_SIM", "").split(",") if s.strip()}
    tr = tracked(root)
    if "no-additions" in sim:
        for u in tr: m.pop(u, None)
    priv = {} if "no-private" in sim or not tr else private_additions(root)
    try: held = {h["url"]: h.get("reason") for h in (json.load(open(os.path.join(root, "plan", "overrides.json"))).get("additions") or {}).get("held", [])}
    except (OSError, ValueError): held = {}
    for u, t in tr.items():
        if u in m: continue
        base = priv.get(u) or {}
        e = {**DEFAULTS, **base, **{k: t.get(k) for k in FIELDS}, "url": u, "plan_source": "additions" + ("+private" if base else "")}
        if e.get("secondaries") is None: e["secondaries"] = []
        if e["status"] != "planned": e.pop("queue_rank", None)
        if e["status"] == "parked-short" and u in held: e["park_reason"] = held[u]
        m[u] = e
    return m

def load(root):
    """The merged map, or None when plan/keyword_map.json is missing."""
    p = os.path.join(root, "plan", "keyword_map.json")
    return merge(json.load(open(p)), root) if os.path.exists(p) else None

def write_tracked(root, pages, ov):
    """plan/additions.json from the full plan: the approved additions (overrides.json additions.urls) with FIELDS only."""
    want = set((ov.get("additions") or {}).get("urls") or []); urls = sorted(want & set(pages))
    if want - set(pages):   # a clone without private/semrush/plan-additions-*.json: never shrink the tracked file
        print(f"plan/additions.json left as is: {len(want - set(pages))} approved addition(s) not in this plan (no private additions file)")
        return 0
    out = {"_note": "Approved additions outside the workbook (ruling 13 new keywords, Divit 2026-10-14): url, hub, primary, status, wave, "
                    "queue_rank only, so every clone's hubctl sees them (plan/kmap_load.py). No Semrush data: secondaries and MSV stay in "
                    "private/semrush/plan-additions-*.json. Written by plan/build_map.py; do not edit by hand.",
           "pages": {u: {k: pages[u].get(k) for k in FIELDS if k != "queue_rank" or pages[u].get("status") == "planned"} for u in urls}}
    json.dump(out, open(os.path.join(root, TRACKED), "w"), indent=1, ensure_ascii=False, sort_keys=False)
    return len(urls)
