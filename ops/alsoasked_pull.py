"""alsoasked_pull.py: one synchronous AlsoAsked API search, saved raw to private/alsoasked/<slug>.json (git-ignored).

  .venv/bin/python3 ops/alsoasked_pull.py <slug> "<term>" [--depth 2] [--region us] [--language en] [--fresh]

API (alsoasked.com/llms.txt, developers.alsoasked.com): base https://alsoaskedapi.com/v1, X-Api-Key header,
POST /search, GET /account. Depth 2 costs 1 credit, depth 3 costs 4 (PA2 never needs level 3).
The key comes from ALSOASKED_API_KEY and is never printed; neither is the response body. Prints only the HTTP status,
credits used (account before/after, also appended to private/alsoasked/credits.log) and question counts per depth.
fresh:false first; fresh:true only if that returns no_results (or with --fresh); --no-retry: one call only (the caller decides).
Callers: only `ops/weekend.py aa` (2 credits per page in total) and `ops/alsoasked_batch.py` (balance ceiling), which set
ALSOASKED_VIA_AA=1; a direct run refuses, so no tool can bypass the caps (Divit 2026-10-10). By hand: ALSOASKED_VIA_AA=1 ... .
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
    except (TimeoutError, urllib.error.URLError):
        return 0, {"_error": "timeout", "status": "timeout"}

PENDING = ("pending", "processing", "queued", "running")

def poll(sid):
    """GET /search/{id} until it leaves a pending state (free; up to 10 minutes)."""
    import time
    for _ in range(30):
        s, r = call("GET", "/search/" + sid)
        if s != 200 or r.get("status") not in PENDING: return s, r
        time.sleep(20)
    return s, r

def from_history(term, depth, region, language):
    """A finished search for the same term and settings already in the history (fetched free, no new billing)."""
    s, h = call("GET", "/search")
    hit = next((x for x in (h.get("results") or []) if x.get("terms") == [term] and x.get("depth") == depth and x.get("region") == region
                and x.get("language") == language and x.get("status") == "success"), None) if s == 200 else None
    return poll(hit["id"]) if hit else (None, None)

def recover(term, depth, region, language):
    """A synchronous search that timed out still runs (and is billed) server-side: find it in the search history
    (GET /search) and fetch it with GET /search/{id}, polling up to 10 minutes while it is pending."""
    import time
    for _ in range(30):
        s, h = call("GET", "/search")
        hit = next((x for x in (h.get("results") or []) if x.get("terms") == [term] and x.get("depth") == depth
                    and x.get("region") == region and x.get("language") == language), None) if s == 200 else None
        if hit and hit.get("status") not in PENDING:
            return call("GET", "/search/" + hit["id"])
        time.sleep(20)
    return 0, {"_error": "timeout; not recovered from history", "status": "timeout"}

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
    if os.environ.get("ALSOASKED_VIA_AA") != "1": sys.exit("refused: pull through ops/weekend.py aa <url> (it enforces the per-page credit cap)")
    if "ALSOASKED_API_KEY" not in os.environ: sys.exit("ALSOASKED_API_KEY is not set")
    slug, term = argv[0], argv[1]
    opt = lambda k, d: argv[argv.index(k) + 1] if k in argv else d
    depth = int(opt("--depth", "2"))
    if depth > 2: sys.exit("PA2: depth 3+ is never required; refusing (costs 4 credits)")
    body = {"terms": [term], "language": opt("--language", "en"), "region": opt("--region", "us"), "depth": depth, "async": False}
    fresh = "--fresh" in argv
    while True:  # fresh:false first (a cache hit may be free); fresh:true only when that returns no_results
        s0, a0 = call("GET", "/account")
        recovered = False
        hs, hr = (None, None) if fresh else from_history(term, depth, body["region"], body["language"])
        if hs == 200 and hr.get("status") == "success": status, res, recovered = hs, hr, "history"
        else: status, res = call("POST", "/search", {**body, "fresh": fresh})
        if res.get("status") == "timeout": status, res = recover(term, depth, body["region"], body["language"]); recovered = True
        elif res.get("status") in PENDING and res.get("id"): status, res = poll(res["id"]); recovered = "polled"
        s1, a1 = call("GET", "/account")
        b, a = (credits(a0), credits(a1)) if s0 == 200 and s1 == 200 else ({}, {})
        used = {k: b[k] - a.get(k, b[k]) for k in b}
        print(f"HTTP {status} fresh={fresh} recovered={recovered} status={res.get('status')} cached={res.get('cached')}" + (f" ({res['_error']})" if "_error" in res else ""))
        print("credits used: " + ", ".join(f"{k} {v}" for k, v in used.items()) + " | remaining: " + ", ".join(f"{k} {v}" for k, v in a.items()))
        os.makedirs(os.path.join(ROOT, "private", "alsoasked"), exist_ok=True)
        with open(os.path.join(ROOT, "private", "alsoasked", "credits.log"), "a") as f:
            f.write(json.dumps({"t": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(timespec="seconds"), "slug": slug,
                                "term": term, "depth": depth, "fresh": fresh, "recovered": recovered, "post": recovered != "history", "http": status, "status": res.get("status"), "cached": res.get("cached"),
                                "before": b, "after": a, "used": used}) + "\n")
        if status == 200 and res.get("status") == "no_results" and not fresh and "--no-retry" not in argv: fresh = True; continue
        break
    if status != 200 or "_error" in res: return 1
    out = os.path.join(ROOT, "private", "alsoasked"); os.makedirs(out, exist_ok=True)
    meta = {"tool": "alsoasked-api", "query": term, "depth": depth, "fresh": fresh, "status": res.get("status"), "region": opt("--region", "us"), "language": opt("--language", "en"),
            "fetched": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%d")}
    json.dump({"_meta": meta, "response": res}, open(os.path.join(out, slug + ".json"), "w"), indent=1, ensure_ascii=False)
    print("nodes per depth: " + ", ".join(f"d{k}={v}" for k, v in sorted(depth_counts(res).items())))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
