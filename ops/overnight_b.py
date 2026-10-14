"""overnight_b.py: code-first state for B's overnight run (ruling 20, Divit 2026-10-14). No Claude session, no tokens, no Webflow.

    python3 ops/overnight_b.py preflight   exit 1 (reasons listed) unless: this is B's clone (~/emergent-hubs-a), CLAUDE_CONFIG_DIR is
                                           ~/.claude (account B), .hub is B:LP,Form,Auto,SurveyQuiz, and there is no STOP file
    python3 ops/overnight_b.py next        what the next iteration should do, in plan order (plan/overnight-run-b.md); exit 3 when
                                           nothing is left (after re-checking the ranked queue every 30 min until 08:00 IST), 4 on STOP
"""
import datetime, json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H

ALL_HUBS = {"LP", "Form", "Auto", "SurveyQuiz"}
QUIZ_CANARY = os.path.join(ROOT, "status", "quiz-canary.json")   # {"result": "pass"} once A's quiz canary passed (DECISIONS 2026-10-14)
RECHECK_SECS, IDLE_UNTIL = 1800, (8, 0)
LOG = os.path.expanduser("~/Library/Logs/emergent-overnight-run-b.log")

def stop(): return os.path.exists(os.path.join(ROOT, "STOP"))
def held_by_a(e): return bool(e.get("hold")) and H.hold_account(e["hold"]) == "A"
def is_quiz(u): return "quiz" in u.rsplit("/", 1)[1]
def quiz_ok():
    try: return json.load(open(QUIZ_CANARY)).get("result") == "pass"
    except (OSError, ValueError): return False
def quiz_canary_pages():
    try: return set(json.load(open(QUIZ_CANARY)).get("canary_pages") or [])
    except (OSError, ValueError): return set()

def work():
    st = {u: e for h in H.CFG["hubs"] for u, e in H.load_st(h)["pages"].items()}
    ok = lambda u, e: not held_by_a(e) and (quiz_ok() or not is_quiz(u) or u in quiz_canary_pages())
    rework = [u for u, e in st.items() if e.get("state") == "rework" and ok(u, e)]
    inflight = [u for u, e in st.items() if e.get("state") in ("claimed", "spec") and ok(u, e)
                and ((e.get("by") or "").startswith("B-") or (e.get("hold") and H.hold_account(e["hold"]) == "B"))]
    render = [u for u, e in st.items() if e.get("state") == "qc_pass" and ok(u, e)]
    review = [u for u, e in st.items() if e.get("state") == "images" and ok(u, e)]
    import queue_rank as Q
    claim = [u for _r, _h, u, c, _f in (Q.ranked() or []) if c in ("ready", "syn-pending") and u not in st and (quiz_ok() or not is_quiz(u) or u in quiz_canary_pages())]
    return [("1 reworks first (blocking findings only; one rework per page)", rework), ("2 in-flight B pages to finish", inflight),
            ("3 render images", render), ("4 full review by an independent B-r agent (never a page it wrote)", review),
            ("5 claim from the top of plan/queue-ranked.txt (all 4 hubs)", claim)]

def cmd_next(a):
    from zoneinfo import ZoneInfo
    while True:
        if stop(): print("STOP"); sys.exit(4)
        order = work()
        if sum(len(us) for _, us in order): break
        now = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
        if (now.hour, now.minute) >= IDLE_UNTIL: break
        with open(LOG, "a") as fh: fh.write(f"{now:%Y-%m-%d %H:%M:%S} nothing to do: re-checking the ranked queue in 30 min (until 08:00 IST)\n")
        for _ in range(RECHECK_SECS // 60):
            if stop(): print("STOP"); sys.exit(4)
            time.sleep(60)
    left = 0
    for name, us in order:
        print(f"{name}: {len(us)}" + (": " + ", ".join(u.rsplit('/', 1)[1] for u in us[:10]) if us else "")); left += len(us)
    sys.exit(0 if left else 3)

def cmd_preflight(a):
    bad = []
    if os.path.basename(ROOT.rstrip("/")) != "emergent-hubs-a": bad.append(f"this is {ROOT}, not B's clone ~/emergent-hubs-a")
    if os.environ.get("CLAUDE_CONFIG_DIR", "") != os.path.expanduser("~/.claude"): bad.append("CLAUDE_CONFIG_DIR is not ~/.claude (account B); refusing any other config dir")
    acct, hubs = H.clone_pin()
    if acct != "B" or set(hubs) != ALL_HUBS: bad.append(f".hub is {acct}:{','.join(hubs)}; ruling 20 needs B:LP,Form,Auto,SurveyQuiz")
    if stop(): bad.append("STOP file present (~/emergent-hubs-a/STOP)")
    for b in bad: print("PREFLIGHT FAIL: " + b)
    if not bad: print("preflight ok")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    a = sys.argv[1:]
    {"next": cmd_next, "preflight": cmd_preflight}.get(a[0] if a else "", lambda _: sys.exit(__doc__))(a[1:])
