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
    return {"keyword": kw, "source": "dataforseo", "engine": "google", "location": "United States", "language": "en",
            "fetched": datetime.date.today().isoformat(), "paa": paa, "related": related, "organic": organic,
            "features": sorted(f for f in features if f not in ("organic",))}

def save(url, raw, keyword=None):
    n = normalize(raw, keyword)
    if not n["organic"] and not n["paa"]:
        raise ValueError("no organic results or PAA questions found in the raw SERP; check the tool call (Google organic, live advanced, United States, en)")
    p = path(url); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(n, open(p, "w"), indent=1, ensure_ascii=False)
    return p, n

TOK = re.compile(r"[a-z0-9]+")
STOP = {"a", "an", "the", "is", "are", "do", "does", "how", "what", "can", "i", "you", "to", "of", "for", "in", "on", "and", "or", "my", "your", "with", "it"}
def tokens(s): return {t for t in TOK.findall((s or "").lower()) if t not in STOP}
def similar(a, b):
    ta, tb = tokens(a), tokens(b)
    return len(ta & tb) / max(1, len(ta | tb))
