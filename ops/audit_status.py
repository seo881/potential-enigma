"""audit_status.py: post-live QC bookkeeping (Divit 2026-10-23: post-live QC never stops and is never skipped).

  audit_status.py success DATE RUNNER     after a FULL run: audits/live/last_success.json {time, runner, date, pages, hubs, fails, p0, p1}
                                          (kept only if newer than what is there)
  audit_status.py line                    one line: "AUDIT: last full run <time UTC>, <n> pages, <n> fail" (STALE if older than 26 h)
  audit_status.py watchdog [--runner R]   writes status/audit_watchdog.json; exit 3 (and the caller alerts) when the last full run is
                                          stale or missing, OR the GitHub Actions backup (live-audit.yml) did not succeed: its newest
                                          completed run failed/was cancelled/timed out, or no run succeeded in the last 26 h (A 2026-10-26:
                                          runs #10-#18 timed out daily and nobody was alerted). Public API, no token.
`hubctl audit-status` prints the line. "fail" = pages (and hubs) with a P0 or P1 finding.
"""
import datetime, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAST = os.path.join(ROOT, "audits", "live", "last_success.json")
WATCH = os.path.join(ROOT, "status", "audit_watchdog.json")
STALE_H = 26

def utcnow(): return datetime.datetime.now(datetime.timezone.utc)
def fmt(t): return t.strftime("%Y-%m-%d %H:%M UTC")

def success(date, runner):
    d = json.load(open(os.path.join(ROOT, "audits", "live", date, "findings.json")))
    F = d["findings"]; bad = {f["url"] for f in F if f["severity"] in ("P0", "P1")}
    rec = {"time": fmt(utcnow()), "epoch": int(utcnow().timestamp()), "runner": runner, "date": date, "base": d.get("base"),
           "pages": len(d["pages"]), "hubs": len(d["hubs"]), "fails": len(bad),
           "p0": sum(f["severity"] == "P0" for f in F), "p1": sum(f["severity"] == "P1" for f in F),
           "findings": f"audits/live/{date}/findings.json"}
    old = json.load(open(LAST)) if os.path.exists(LAST) else {}
    if old.get("epoch", 0) > rec["epoch"]: return old
    os.makedirs(os.path.dirname(LAST), exist_ok=True); json.dump(rec, open(LAST, "w"), indent=1); return rec

RAW_LAST = "https://raw.githubusercontent.com/seo881/potential-enigma/main/audits/live/last_success.json"

def state():
    """The newest of the local last_success.json and the one on origin/main (public raw URL): the watchdog stays right whichever clone
    it runs from and whether or not that clone has pulled (A 2026-10-26, stable shim)."""
    recs = []
    if os.path.exists(LAST):
        try: recs.append(json.load(open(LAST)))
        except ValueError: pass
    if os.environ.get("AUDIT_STATUS_OFFLINE") != "1":
        try:
            import urllib.request
            recs.append(json.load(urllib.request.urlopen(urllib.request.Request(RAW_LAST, headers={"User-Agent": "emergent-audit-watchdog"}), timeout=20)))
        except Exception: pass
    if not recs: return None, None
    r = max(recs, key=lambda x: x.get("epoch", 0)); age = (utcnow().timestamp() - r.get("epoch", 0)) / 3600
    return r, age

def line():
    r, age = state()
    if r is None: return "AUDIT: STALE: no full run recorded (audits/live/last_success.json missing)"
    return f"AUDIT: last full run {r['time']}, {r['pages']} pages, {r['fails']} fail" + (f" ({r['runner']})" if r.get("runner") else "") \
        + (f"  STALE ({age:.0f} h old, limit {STALE_H} h)" if age > STALE_H else "")

GH_RUNS = "https://api.github.com/repos/seo881/potential-enigma/actions/workflows/live-audit.yml/runs?per_page=20"

def backup(runs=None):
    """(ok, line) for the GitHub Actions backup audit. runs: the API's workflow_runs list (tests pass it in)."""
    if runs is None:
        import urllib.request
        try: runs = json.load(urllib.request.urlopen(urllib.request.Request(GH_RUNS, headers={"User-Agent": "emergent-audit-watchdog"}), timeout=30))["workflow_runs"]
        except Exception as e: return False, f"BACKUP AUDIT: status unknown (GitHub API unreachable: {type(e).__name__})"
    done = [r for r in runs if r.get("status") == "completed"]
    if not done: return False, "BACKUP AUDIT: no completed run"
    last = done[0]; ts = lambda r: datetime.datetime.fromisoformat(r["updated_at"].replace("Z", "+00:00"))
    ok_runs = [r for r in done if r.get("conclusion") == "success"]
    if last.get("conclusion") != "success":
        return False, f"BACKUP AUDIT FAILED: run #{last['run_number']} {last.get('conclusion')} at {fmt(ts(last))}" + \
            (f"; last success #{ok_runs[0]['run_number']} {fmt(ts(ok_runs[0]))}" if ok_runs else "; no successful run on record")
    if (utcnow() - ts(ok_runs[0])).total_seconds() / 3600 > STALE_H:
        return False, f"BACKUP AUDIT STALE: last success #{ok_runs[0]['run_number']} {fmt(ts(ok_runs[0]))}"
    return True, f"BACKUP AUDIT: run #{last['run_number']} success {fmt(ts(last))}"

def watchdog(runner, runs=None):
    r, age = state(); stale = r is None or age > STALE_H
    bok, bline = backup(runs)
    rec = {"checked": fmt(utcnow()), "checked_by": runner, "stale": stale, "limit_hours": STALE_H,
           "age_hours": None if age is None else round(age, 1), "last_success": r, "line": line(),
           "backup_ok": bok, "backup_line": bline}
    os.makedirs(os.path.dirname(WATCH), exist_ok=True); json.dump(rec, open(WATCH, "w"), indent=1)
    print(rec["line"]); print(bline); return 3 if (stale or not bok) else 0

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["success"]: print(json.dumps(success(a[1], a[2] if len(a) > 2 else "unknown")))
    elif a[:1] == ["line"] or not a: print(line())
    elif a[:1] == ["watchdog"]: sys.exit(watchdog(a[a.index("--runner") + 1] if "--runner" in a else "unknown"))
    else: sys.exit(__doc__)
