"""alsoasked_pull.py: one synchronous AlsoAsked API search, saved raw to private/alsoasked/<slug>.json (git-ignored).

  .venv/bin/python3 ops/alsoasked_pull.py <slug> "<term>" [--depth 2] [--region us] [--language en] [--fresh]

API (alsoasked.com/llms.txt, developers.alsoasked.com): base https://alsoaskedapi.com/v1, X-Api-Key header,
POST /search, GET /account. Depth 2 costs 1 credit, depth 3 costs 4 (PA2 never needs level 3).
The key comes from ALSOASKED_API_KEY and is never printed; neither is the response body. Prints only the HTTP status,
credits used (account before/after) and question counts per depth.
"""
import json, os, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://alsoaskedapi.com/v1"

def call(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"X-Api-Key": os.environ["ALSOASKED_API_KEY"], "Accept": "application/json", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as f: return f.status, json.load(f)
    except urllib.error.HTTPError as e:
        try: msg = json.load(e).get("message", "")
        except Exception: msg = ""
        return e.code, {"_error": str(msg)[:200]}

def credits(acc): return {k: v for k, v in acc.items() if "credit" in k.lower() and isinstance(v, (int, float))}

def depth_counts(o, d=0, out=None):
    """Count question nodes per nesting level: a dict with a 'question' string is a node; its children are one level deeper."""
    out = {} if out is None else out
    if isinstance(o, dict):
        isq = isinstance(o.get("question"), str)
        if isq: out[d + 1] = out.get(d + 1, 0) + 1
        for v in o.values(): depth_counts(v, d + 1 if isq else d, out)
    elif isinstance(o, list):
        for v in o: depth_counts(v, d, out)
    return out

def main(argv):
    if "ALSOASKED_API_KEY" not in os.environ: sys.exit("ALSOASKED_API_KEY is not set")
    slug, term = argv[0], argv[1]
    opt = lambda k, d: argv[argv.index(k) + 1] if k in argv else d
    depth = int(opt("--depth", "2"))
    if depth > 2: sys.exit("PA2: depth 3+ is never required; refusing (costs 4 credits)")
    s0, a0 = call("GET", "/account")
    status, res = call("POST", "/search", {"terms": [term], "language": opt("--language", "en"), "region": opt("--region", "us"),
                                          "depth": depth, "fresh": "--fresh" in argv, "async": False})
    s1, a1 = call("GET", "/account")
    print(f"HTTP {status}" + (f" ({res['_error']})" if "_error" in res else ""))
    if s0 == 200 and s1 == 200:
        b, a = credits(a0), credits(a1)
        print("credits used: " + ", ".join(f"{k} {b[k] - a.get(k, b[k])}" for k in b) + " | remaining: " + ", ".join(f"{k} {v}" for k, v in a.items()))
    if status != 200 or "_error" in res: return 1
    out = os.path.join(ROOT, "private", "alsoasked"); os.makedirs(out, exist_ok=True)
    meta = {"tool": "alsoasked-api", "query": term, "depth": depth, "fresh": "--fresh" in argv, "status": res.get("status"), "region": opt("--region", "us"), "language": opt("--language", "en"),
            "fetched": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%d")}
    json.dump({"_meta": meta, "response": res}, open(os.path.join(out, slug + ".json"), "w"), indent=1, ensure_ascii=False)
    print("nodes per depth: " + ", ".join(f"d{k}={v}" for k, v in sorted(depth_counts(res).items())))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
