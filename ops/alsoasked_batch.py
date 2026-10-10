"""alsoasked_batch.py: pull AlsoAsked for every written page with a credit ceiling (Divit, 2026-10-08).

  .venv/bin/python3 ops/alsoasked_batch.py --ceiling 200 --max-per-page 2 --start-balance 998 [--workers 3] [--skip slug,slug]

Written pages: state images or later, plus rework (live-draft specs excluded). Pages already pulled are skipped.
Workers run ops/alsoasked_pull.py in parallel. Before every launch the account balance is read under a lock and the
page is started only if spent + max-per-page x (pages in flight + 1) stays within the ceiling, so concurrency cannot
cross it. Per-page cost is counted from billed POSTs (account deltas mix under concurrency): over max-per-page stops
the run. A 429 or rate-limit error drops the run to 1 worker (the page is requeued). A failed page is retried once.
Prints one summary line per page, never the response.
"""
import json, os, subprocess, sys, threading, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G, alsoasked_pull as A
LOG = os.path.join(ROOT, "private", "alsoasked", "credits.log")
WRITTEN = {"images", "reviewed", "challenged", "approved", "rework", "cms_draft", "published"}

def log_rows():
    return [json.loads(l) for l in open(LOG)] if os.path.exists(LOG) else []

def main(argv):
    opt = lambda k, d: argv[argv.index(k) + 1] if k in argv else d
    ceiling, maxp, workers = int(opt("--ceiling", "200")), int(opt("--max-per-page", "2")), int(opt("--workers", "1"))
    skip = set(opt("--skip", "").split(",")) - {""}
    start = int(opt("--start-balance", log_rows()[-1]["after"]["credits"]))
    st = G.all_status(); queue = []
    for s in G.all_specs():
        slug = s["url"].rsplit("/", 1)[1]
        if s.get("status") == "live-draft" or st.get(s["url"], {}).get("state") not in WRITTEN or slug in skip: continue
        if os.path.exists(os.path.join(ROOT, "private", "alsoasked", slug + ".json")): continue
        queue.append((slug, (s.get("keywords") or {}).get("primary")))
    print(f"start balance {start}; ceiling {ceiling}; {len(queue)} pages to pull; {workers} workers", flush=True)
    lock = threading.Lock(); state = {"inflight": 0, "stop": None, "single": workers == 1, "done": 0}
    retried, failed = set(), []

    def worker(wid):
        while True:
            with lock:
                if state["stop"] or not queue: return
                if state["single"] and wid != 0: return
                s0, acc = A.call("GET", "/account")
                if s0 != 200: state["stop"] = f"account read failed (HTTP {s0})"; return
                spent = start - acc["credits"]
                if spent + maxp * (state["inflight"] + 1) > ceiling:
                    if state["inflight"] == 0: state["stop"] = f"ceiling: spent {spent}, next page could cross {ceiling}"
                    return
                slug, term = queue.pop(0); state["inflight"] += 1
            t0 = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
            r = subprocess.run([sys.executable, os.path.join(ROOT, "ops", "alsoasked_pull.py"), slug, term, "--depth", "2"], capture_output=True, text=True, env={**os.environ, "ALSOASKED_VIA_AA": "1"})
            with lock:
                state["inflight"] -= 1; state["done"] += 1
                rows = [x for x in log_rows() if x["slug"] == slug and x["t"][:19] >= t0]
                cost = sum(1 for x in rows if x.get("post", True) and x.get("status") != "no_results")
                last = rows[-1] if rows else {}
                print(f"{slug}: rc {r.returncode}, est credits {cost}, calls {len(rows)}, status {last.get('status')}, via {last.get('recovered')}, worker {wid}", flush=True)
                limited = any(x.get("http") == 429 for x in rows) or "rate limit" in (r.stdout + r.stderr).lower() or "too many requests" in (r.stdout + r.stderr).lower()
                if limited:
                    queue.insert(0, (slug, term))
                    if not state["single"]: state["single"] = True; print("RATE LIMITED: dropping to 1 worker", flush=True)
                    continue
                if cost > maxp: state["stop"] = f"{slug} cost {cost} credits (> {maxp})"; return
                if r.returncode != 0 or last.get("status") not in ("success", "no_results"):
                    if slug in retried: failed.append(slug); print(f"FAILED twice: {slug} (skipped)", flush=True)
                    else: retried.add(slug); queue.append((slug, term)); print(f"retry later: {slug}", flush=True)

    ts = [threading.Thread(target=worker, args=(i,)) for i in range(workers)]
    for t in ts: t.start()
    for t in ts: t.join()
    if not state["stop"] and queue and state["single"]: worker(0)  # rate-limited tail: finish on one worker
    s1, acc = A.call("GET", "/account")
    end = acc.get("credits") if s1 == 200 else None
    print(f"{'STOP: ' + state['stop'] + '; ' if state['stop'] else ''}done {state['done']} pulls; left {len(queue)}; failed {len(failed)} {failed}; "
          f"spent {start - end if end is not None else '?'}; balance {end}", flush=True)

if __name__ == "__main__":
    main(sys.argv[1:])
