"""pull_wave.py: ruling 12 part 1 (Divit 2026-10-13). Account A runs every AlsoAsked pull; B uses saved pulls only.

    python3 ops/pull_wave.py plan                 list what the wave would pull (no calls)
    python3 ops/pull_wave.py run [--run wave-r12] pull it, one page at a time, through weekend.py aa (the only AlsoAsked path)

Wave: (1) every queued page (planned, no status entry) with no saved pull, in queue-rank order across hubs; (2) then each LP page
whose primary pull returned no_results and whose feasibility is under 10 gets one --kw secondary pull. weekend.py aa enforces
2 credits per page and the run cap (AUTH_RUNS: wave-r12 = 400); the wave stops at the first cap refusal or unexpected cost.
Output is slugs and credit counts only (no question text): safe for a report.
"""
import io, contextlib, json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H, paa_gate as P

def saved_status(name):
    try: return json.load(open(os.path.join(ROOT, "private", "alsoasked", name + ".json")))["_meta"].get("status") or "success"
    except (OSError, ValueError, KeyError): return None

def queued():
    m = H.kmap(); st = {h: H.load_st(h)["pages"] for h in H.CFG["hubs"]}
    return sorted([p for p in m.values() if p["status"] == "planned" and p["url"] not in st[p["hub"]]], key=lambda p: p["queue_rank"])

def primaries():
    return [p for p in queued() if saved_status(p["url"].rsplit("/", 1)[1]) is None]

def lp_secondaries():
    import park_rescue as R
    out = []
    for p in queued():
        s = p["url"].rsplit("/", 1)[1]
        if p["hub"] != "LP" or saved_status(s) != "no_results" or saved_status(s + "--sec") is not None: continue
        with contextlib.redirect_stdout(io.StringIO()): f = R.feasibility(p["url"])
        if not f["feasible"]: out.append(p)
    return out

def aa(url, run, sec=False):
    cmd = [sys.executable, os.path.join(ROOT, "ops", "weekend.py"), "aa", url, "--run", run] + (["--kw", "secondary"] if sec else [])
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    print(f"{'sec ' if sec else ''}{url}: rc {r.returncode}: " + " | ".join(out[-2:]), flush=True)
    return r.returncode, " ".join(out)

def main(a):
    if not a or a[0] not in ("plan", "run"): sys.exit(__doc__)
    if H.clone_account() != "A": sys.exit("refused: pulls run in Account A only (ruling 12)")
    run = a[a.index("--run") + 1] if "--run" in a else "wave-r12"
    if a[0] == "plan":
        pr = primaries(); print(f"primary pulls: {len(pr)} queued pages with no pull")
        for p in pr: print(f"  #{p['queue_rank']:<4} {p['hub']:10s} {p['url']}")
        print("LP --kw secondary pulls (after the primaries): decided after the primary wave, from feasibility"); return
    stop = ("cap reached", "no more pulls", "not set", "HTTP 40")
    for p in primaries():
        rc, out = aa(p["url"], run)
        if rc == 5 or any(x in out for x in stop): print("wave stopped: " + out[-200:]); return
    for p in lp_secondaries():
        rc, out = aa(p["url"], run, sec=True)
        if rc == 5 or any(x in out for x in stop): print("wave stopped: " + out[-200:]); return
    print("wave complete")

if __name__ == "__main__":
    main(sys.argv[1:])
