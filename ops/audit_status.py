"""audit_status.py: post-live QC bookkeeping (Divit 2026-10-23: post-live QC never stops and is never skipped).

  audit_status.py success DATE RUNNER     after a FULL run: audits/live/last_success.json {time, runner, date, pages, hubs, fails, p0, p1}
                                          (kept only if newer than what is there)
  audit_status.py line                    one line: "AUDIT: last full run <time UTC>, <n> pages, <n> fail" (STALE if older than 26 h)
  audit_status.py watchdog [--runner R]   writes status/audit_watchdog.json; exit 3 (and the caller alerts) when stale or missing
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

def state():
    if not os.path.exists(LAST): return None, None
    r = json.load(open(LAST)); age = (utcnow().timestamp() - r.get("epoch", 0)) / 3600
    return r, age

def line():
    r, age = state()
    if r is None: return "AUDIT: STALE: no full run recorded (audits/live/last_success.json missing)"
    return f"AUDIT: last full run {r['time']}, {r['pages']} pages, {r['fails']} fail" + (f" ({r['runner']})" if r.get("runner") else "") \
        + (f"  STALE ({age:.0f} h old, limit {STALE_H} h)" if age > STALE_H else "")

def watchdog(runner):
    r, age = state(); stale = r is None or age > STALE_H
    rec = {"checked": fmt(utcnow()), "checked_by": runner, "stale": stale, "limit_hours": STALE_H,
           "age_hours": None if age is None else round(age, 1), "last_success": r, "line": line()}
    os.makedirs(os.path.dirname(WATCH), exist_ok=True); json.dump(rec, open(WATCH, "w"), indent=1)
    print(rec["line"]); return 3 if stale else 0

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["success"]: print(json.dumps(success(a[1], a[2] if len(a) > 2 else "unknown")))
    elif a[:1] == ["line"] or not a: print(line())
    elif a[:1] == ["watchdog"]: sys.exit(watchdog(a[a.index("--runner") + 1] if "--runner" in a else "unknown"))
    else: sys.exit(__doc__)
