"""Safeguards shared by hubctl and QC (decided 2026-10-07; see DECISIONS.md).

  lock()                 file lock around every status read-modify-write (parallel agents never overwrite each other)
  fingerprint(spec)      content + image hash frozen at approval; creation refuses anything changed since
  rules_version()        hash of every rule and check; pages record which version they passed
  shingle similarity     phrase-level near-duplicate detection across every page in a hub
  sample()               risk-based selection of pages for Divit's review
  metrics()              pass rates, rework causes, challenger-after-review hit rate
  link_graph()           inbound FAQ links per page; pages that need links
  lookahead()            competitor-library gaps for the next pages in the queue
  serp budget, ranks     DataForSEO call budget per day; position history and refresh queue
"""
import os, json, glob, hashlib, re, random, datetime, contextlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))
PRIVATE = os.path.join(ROOT, "private")

@contextlib.contextmanager
def lock(name="status"):
    """Exclusive lock (fcntl) for read-modify-write of shared files. Works across processes on one machine."""
    import fcntl
    os.makedirs(os.path.join(ROOT, ".locks"), exist_ok=True)
    with open(os.path.join(ROOT, ".locks", name + ".lock"), "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try: yield
        finally: fcntl.flock(fh, fcntl.LOCK_UN)

def _canon(obj): return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
def fingerprint(spec):
    """Hash of everything that will reach Webflow: all fields, image files on disk, alt texts, table and FAQ sources."""
    h = hashlib.sha256(_canon({"fields": spec.get("fields"), "table": spec.get("table"), "faq_sources": spec.get("faq_sources")}).encode())
    for k in sorted(spec.get("images", {})):
        im = spec["images"][k]; h.update(k.encode()); h.update((im.get("alt") or "").encode())
        p = os.path.join(ROOT, im.get("path", "") or "")
        h.update(open(p, "rb").read() if im.get("path") and os.path.exists(p) else b"missing")
    return h.hexdigest()

def rules_version():
    files = sorted(glob.glob(os.path.join(ROOT, "rules", "**", "*"), recursive=True)) + [os.path.join(ROOT, "qc", "qc_hub.py"), os.path.join(ROOT, "config", "typography.json"),
             os.path.join(ROOT, "pipeline", "engine.py"), os.path.join(ROOT, "pipeline", "engine_blocks.py")]
    h = hashlib.sha256()
    for f in files:
        if os.path.isfile(f): h.update(os.path.relpath(f, ROOT).encode()); h.update(open(f, "rb").read())
    return h.hexdigest()[:12]

# ---------------------------------------------------------------- near-duplicates
def _norm_words(t): return re.findall(r"[a-z0-9']+", re.sub(r"<[^>]+>", " ", (t or "").lower()))
def shingles(text, n=5):
    w = _norm_words(text); return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}
def sections(spec):
    F = spec.get("fields", {}); out = {}
    out["features"] = " ".join(F.get(f"feature_{i}", "") for i in range(1, 7))
    out["tabs"] = " ".join(F.get(f"tab_content_{i}", "") for i in range(1, 5))
    out["howto"] = " ".join(F.get(f"howto_step_{i}_des", "") for i in range(1, 8))
    m = re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;\s*</script>", F.get("faq", ""), re.S)
    out["faq"] = " ".join(i.get("a", "") for i in json.loads(m.group(1)).get("items", [])) if m else ""
    out["hero"] = " ".join([F.get("hero_description", ""), F.get("features_subheading", ""), F.get("why_description", "")])
    return out
def similarity(spec, others, n=5):
    """[(section, other_url, containment)] : share of this page's 5-word phrases that also appear on another page."""
    mine = {k: shingles(v, n) for k, v in sections(spec).items()}; res = []
    for o in others:
        if o.get("url") == spec.get("url") or o.get("hub") != spec.get("hub"): continue
        theirs = {k: shingles(v, n) for k, v in sections(o).items()}
        for k, sh in mine.items():
            if len(sh) >= 20 and theirs.get(k):
                res.append((k, o["url"], len(sh & theirs[k]) / len(sh)))
    return res

# ---------------------------------------------------------------- history, metrics, sampling
def all_specs():
    return [dict(json.load(open(p)), _path=p) for p in sorted(glob.glob(os.path.join(ROOT, "specs", "*", "*.json")))]
def all_status():
    out = {}
    for h in CFG["hubs"].values():
        p = os.path.join(ROOT, "status", f"{h['repo_dir']}.json")
        if os.path.exists(p): out.update(json.load(open(p))["pages"])
    return out
def metrics():
    st = all_status(); specs = {s["url"]: s for s in all_specs()}
    counts = {}
    for e in st.values(): counts[e.get("state", "?")] = counts.get(e.get("state", "?"), 0) + 1
    rework_causes, challenged_after_review, challenge_fail = {}, 0, 0
    for url, s in specs.items():
        for ev in s.get("history", []):
            if ev.get("state") == "rework":
                cause = "challenge" if "challenge" in (ev.get("via") or "") else ("review" if "review" in (ev.get("via") or "") else "other")
                rework_causes[cause] = rework_causes.get(cause, 0) + 1
                if cause == "challenge": challenge_fail += 1
            if ev.get("via") == "challenge": challenged_after_review += 1
    hit = challenge_fail / challenged_after_review if challenged_after_review else None
    return {"states": counts, "rework_causes": rework_causes, "challenges_run": challenged_after_review,
            "challenger_hit_rate": hit, "alert": (hit is not None and challenged_after_review >= 10 and hit > 0.15)}
def sample(urls, seed=None, pct=0.10):
    """Risk-based: always the first page of each recipe or table category, pages with accepted P2s or with challenge defects
    in their history, pages using new ledger entries; then a random share of the rest."""
    specs = {s["url"]: s for s in all_specs()}; must, rest = [], []
    seen_recipe, seen_cat = set(), set()
    for s in sorted(all_specs(), key=lambda x: x.get("history", [{}])[0].get("t", "")):
        if s.get("status") in ("live-draft",): continue
        for t in (s.get("image_brief") or {}).get("tabs", []): seen_recipe.add(t.get("recipe")) if s["url"] not in urls else None
        if s["url"] not in urls and s.get("table"): seen_cat.add((s.get("table") or {}).get("variant"))
    for u in urls:
        s = specs.get(u, {}); why = []
        recipes = {t.get("recipe") for t in (s.get("image_brief") or {}).get("tabs", [])}
        if recipes - seen_recipe: why.append(f"first use of recipe {sorted(recipes - seen_recipe)}"); seen_recipe |= recipes
        cat = (s.get("table") or {}).get("variant")
        if cat not in seen_cat: why.append(f"first page of table category {cat or 'hub default'}"); seen_cat.add(cat)
        if any(ev.get("via") == "challenge" and ev.get("state") == "rework" for ev in s.get("history", [])): why.append("challenger found defects earlier")
        if s.get("accepted_p2"): why.append("accepted P2s")
        if s.get("new_ledger_entries"): why.append("uses new ledger entries")
        (must if why else rest).append((u, why))
    rnd = random.Random(seed or datetime.date.today().isoformat())
    k = max(1, round(len(rest) * pct)) if rest else 0
    return must + [(u, ["random sample"]) for u, _ in rnd.sample(rest, k)]

# ---------------------------------------------------------------- internal links
LINK = re.compile(r"<a href=(?:\\\\?\"|')https://emergent\.sh([^\"'\\\\]+)")
def link_graph():
    inbound = {}
    for s in all_specs():
        for u in set(LINK.findall(s.get("fields", {}).get("faq", ""))):
            inbound.setdefault(u.rstrip("/"), set()).add(s["url"])
    return inbound
def needs_links(hub, k=8):
    """Live or approved sibling pages with the fewest inbound links: suggestions for the writer."""
    st = all_status(); g = link_graph(); live = {u for u, e in st.items() if e.get("state") in ("approved", "cms_draft", "published")}
    live |= {s["url"] for s in all_specs() if s.get("status") == "live-draft"}
    path = CFG["hubs"][hub]["path"]
    cands = sorted((len(g.get(u, ())), u) for u in live if u.startswith(path + "/"))
    return [(u, n) for n, u in cands[:k]]

# ---------------------------------------------------------------- look-ahead, budgets, ranks
def lookahead(hub, n, kmap):
    lib = json.load(open(os.path.join(ROOT, "rules", "competitors", f"{CFG['hubs'][hub]['repo_dir']}.json")))
    sites = {c.get("site", "").split("/")[0]: name for name, c in lib["competitors"].items()}
    st = all_status(); queue = sorted([p for p in kmap.values() if p["hub"] == hub and p["status"] == "planned" and p["url"] not in st], key=lambda p: p["queue_rank"])[:n]
    out = []
    for p in queue:
        doms = [re.sub(r"^www\.", "", re.sub(r"https?://([^/]+).*", r"\1", u)) for u in p.get("top10", [])]
        have = [sites[d] for d in doms if d in sites]
        out.append((p["url"], have, [d for d in doms if d not in sites][:6]))
    return out
def budget_path(): return os.path.join(PRIVATE, "serp", "_usage.json")
def budget_use(n=1):
    os.makedirs(os.path.dirname(budget_path()), exist_ok=True)
    with lock("budget"):
        u = json.load(open(budget_path())) if os.path.exists(budget_path()) else {}
        d = datetime.date.today().isoformat(); u[d] = u.get(d, 0) + n; json.dump(u, open(budget_path(), "w"))
        return u[d]
def budget_left():
    cap = CFG.get("dataforseo_daily_cap", 600)
    u = json.load(open(budget_path())) if os.path.exists(budget_path()) else {}
    return cap - u.get(datetime.date.today().isoformat(), 0), cap
def rank_from_serp(raw_items, domain="emergent.sh"):
    for it in raw_items:
        if it.get("type") == "organic" and domain in (it.get("domain") or it.get("url") or ""):
            return it.get("rank_group") or it.get("rank_absolute"), it.get("url")
    return None, None
