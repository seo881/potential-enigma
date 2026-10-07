"""Live SERP data per page, captured through the DataForSEO MCP server (Google, United States, English, desktop).

Stored at private/serp/<dir>/<slug>.json, git-ignored: third-party data never goes into the public repo.
`normalize()` accepts the raw tool result in any of DataForSEO's shapes (the MCP text wrapper, the full API response,
or a bare `items` list) and keeps what the writers use:
  paa       People Also Ask questions (with the source URL; answer text is kept only for reference, never copied)
  related   related searches
  organic   the top 10 (rank, url, domain, title)
  features  SERP feature types present (ai_overview, featured_snippet, people_also_ask, video, ...)
"""
import json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def path(url):
    cfg = json.load(open(os.path.join(ROOT, "config", "collections.json")))
    for h in cfg["hubs"].values():
        if url.startswith(h["path"] + "/"):
            return os.path.join(ROOT, "private", "serp", h["repo_dir"], url.rsplit("/", 1)[1] + ".json")
    raise ValueError(f"no hub owns {url}")

def load(url):
    p = path(url)
    return json.load(open(p)) if os.path.exists(p) else None

def _walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values(): yield from _walk(v)
    elif isinstance(o, list):
        for v in o: yield from _walk(v)

def _parse_text(raw):
    """The MCP tool result may arrive as text blocks containing JSON."""
    if isinstance(raw, (dict, list)) and not (isinstance(raw, list) and raw and isinstance(raw[0], dict) and "text" in raw[0] and len(raw[0]) <= 2):
        return raw
    txt = "".join(b.get("text", "") for b in raw) if isinstance(raw, list) else str(raw)
    out, dec, i = [], json.JSONDecoder(), 0
    while i < len(txt):
        j = txt.find("{", i) if txt.find("{", i) != -1 else len(txt)
        k = txt.find("[", i) if txt.find("[", i) != -1 else len(txt)
        i = min(j, k)
        if i >= len(txt): break
        try:
            o, e = dec.raw_decode(txt, i); out.append(o); i = e
        except ValueError:
            i += 1
    return out

def normalize(raw, keyword=None):
    data = _parse_text(raw)
    paa, related, organic, features, seen_q = [], [], [], set(), set()
    for d in _walk(data):
        t = d.get("type")
        if not t: continue
        features.add(t)
        if t == "people_also_ask_element":
            q = (d.get("title") or "").strip()
            if q and q.lower() not in seen_q:
                seen_q.add(q.lower())
                ex = (d.get("expanded_element") or [{}])[0] or {}
                paa.append({"q": q, "url": ex.get("url"), "answer_ref": (ex.get("description") or "")[:300]})
        elif t == "related_searches":
            for it in d.get("items") or []:
                s = it if isinstance(it, str) else (it.get("title") or it.get("keyword") if isinstance(it, dict) else None)
                if s and s not in related: related.append(s)
        elif t == "organic":
            if d.get("url") and len(organic) < 10:
                organic.append({"rank": d.get("rank_group") or d.get("rank_absolute"), "url": d["url"], "domain": d.get("domain"), "title": d.get("title")})
    kw = keyword
    if not kw:
        for d in _walk(data):
            if isinstance(d.get("keyword"), str): kw = d["keyword"]; break
    features.discard("people_also_ask_element")
    keywords, seen_k = [], set()
    for d in _walk(data):                      # DataForSEO Labs related keywords / keyword suggestions
        kd = d.get("keyword_data") if isinstance(d.get("keyword_data"), dict) else d
        k_ = kd.get("keyword") if isinstance(kd, dict) else None
        info = (kd.get("keyword_info") or {}) if isinstance(kd, dict) else {}
        vol = info.get("search_volume", kd.get("search_volume") if isinstance(kd, dict) else None)
        if isinstance(k_, str) and vol is not None and k_.lower() not in seen_k:
            seen_k.add(k_.lower()); keywords.append({"kw": k_, "msv": vol})
    return {"keyword": kw, "source": "dataforseo", "engine": "google", "location": "United States", "language": "en",
            "fetched": datetime.date.today().isoformat(), "paa": paa, "related": related, "organic": organic, "keywords": sorted(keywords, key=lambda x: -(x["msv"] or 0))[:60],
            "features": sorted(f for f in features if f not in ("organic",))}

def save(url, raw, keyword=None, merge=False):
    n = normalize(raw, keyword)
    if merge:                                   # add keyword ideas to an existing SERP capture
        old = load(url) or {}
        if not old: raise ValueError("capture the SERP first (hubctl serp-save), then add keyword ideas")
        old["keywords"] = n["keywords"]; n = old
    elif not n["organic"] and not n["paa"]:
        raise ValueError("no organic results or PAA questions found in the raw SERP; check the tool call (Google organic, live advanced, United States, en)")
    p = path(url); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(n, open(p, "w"), indent=1, ensure_ascii=False)
    return p, n

TOK = re.compile(r"[a-z0-9]+")
STOP = {"a", "an", "the", "is", "are", "do", "does", "how", "what", "can", "i", "you", "to", "of", "for", "in", "on", "and", "or", "my", "your", "with", "it"}
def tokens(s): return {t for t in TOK.findall((s or "").lower()) if t not in STOP}
GENERIC = {"ai", "seo", "automation", "automate", "automated", "app", "apps", "software", "tool", "tools", "builder", "online", "free", "best",
           "template", "templates", "form", "forms", "page", "pages", "survey", "surveys", "quiz", "quizzes", "workflow", "workflows", "example", "examples"}
def similar(a, b):
    ta, tb = tokens(a), tokens(b)
    return len(ta & tb) / max(1, len(ta | tb))

def topic_tokens(page):
    """Meaningful tokens of the page's primary and secondaries, plus common abbreviations."""
    toks = set()
    for k in [page.get("primary", "")] + [x["kw"] for x in page.get("secondaries", [])]:
        toks |= tokens(k)
    abbr = {"accounts payable": "ap", "accounts receivable": "ar", "customer satisfaction": "csat", "net promoter": "nps", "search engine optimization": "seo", "human resources": "hr"}
    for full, ab in abbr.items():
        if full in page.get("primary", "").lower(): toks.add(ab)
    return toks - {"form", "page", "template", "free", "online", "best", "software", "tool", "tools", "builder"}

def eligible(live, page, prims=None):
    """Split captured PAA questions into (eligible, skipped[(q, reason)]).
    Skipped: questions that drift off topic (deeper PAA expansions often do) and questions that name another page's primary."""
    want = topic_tokens(page); ok, skip = [], []
    for it in live.get("paa", []):
        q = it["q"]; ql = q.lower()
        owner = None
        for k, u in (prims or {}).items():
            if len(k.split()) > 1 and k in ql and k not in page.get("primary", "").lower(): owner = u; break
        if owner: skip.append((q, f"belongs to {owner}")); continue
        # a shared generic word ("ai", "seo", "automation") is not enough: "How to use AI to make $10,000 a month?" is not
        # on topic for sales automation (Divit, 2026-10-07: 10 on-topic FAQ items, never padded with drift)
        specific = (want - GENERIC) or want
        if not (tokens(q) & specific): skip.append((q, "off topic (PAA expansion drift)")); continue
        ok.append(it)
    return ok, skip
