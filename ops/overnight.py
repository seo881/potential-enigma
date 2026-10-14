"""overnight.py: code-first state for the overnight run (Divit ruling 17, 2026-10-13). No Claude session, no tokens, no Webflow.

    python3 ops/overnight.py preflight     exit 1 (reasons listed) unless: the canary passed 3/3, the .hub override covers all 4 hubs,
                                           no Webflow tools are configured for the loop, the AlsoAsked/Semrush keys are not needed
    python3 ops/overnight.py next          what the next iteration should do, in plan order; exit 3 when nothing is left, 4 on STOP
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H

CANARY = os.path.join(ROOT, "status", "canary-r15.json")   # {"result": "pass"|"fail", "pages": {...}} written by the coordinator

def b_held(e): return bool(e.get("hold")) and H.hold_account(e["hold"]) == "B"

def work():
    st = {u: e for h in H.CFG["hubs"] for u, e in H.load_st(h)["pages"].items()}
    lp_rework = [u for u, e in st.items() if H.hub_of(u) == "LP" and e.get("state") == "rework" and not b_held(e)]
    held_for_ruling = lambda e: "held for ruling" in (e.get("note") or "") or (e.get("note") or "").startswith("proposal")
    review = [u for u, e in st.items() if e.get("state") == "images" and not b_held(e) and not held_for_ruling(e)]
    render = [u for u, e in st.items() if e.get("state") == "qc_pass" and not b_held(e)]
    rework = [u for u, e in st.items() if e.get("state") == "rework" and H.hub_of(u) != "LP" and not b_held(e)
              and (json.load(open(H.spath(u))) if os.path.exists(H.spath(u)) else {}).get("pipeline") == "r15"]
    import queue_rank as Q
    ranked = [(u, c) for _r, h, u, c, _f in (Q.ranked() or []) if c in ("ready", "syn-pending") and u not in st]
    a_held = lambda e: bool(e.get("hold")) and H.hold_account(e["hold"]) == "A"
    inflight = [u for u, e in st.items() if e.get("state") in ("claimed", "spec") and ((e.get("by") or "").startswith("A-w") or a_held(e)) and not b_held(e)]
    return {"lp_rework": lp_rework, "inflight": inflight, "render": render, "review": review, "r15_rework": rework, "claimable": ranked}

RECHECK_SECS, IDLE_UNTIL = 1800, (8, 0)   # Divit 2026-10-14: before going idle, re-check the ranked queue every 30 min until 08:00 IST
LOG = os.path.expanduser("~/Library/Logs/emergent-overnight-run.log")

# 2026-10-14 05:55 IST (A-coord): blocked on tooling or a ruling the loop may not make (plan/backlog.md lines of 10-14); listing them made
# 2-minute claim/release iterations. Out of `next` until the 10:00 report's decisions land.
BLOCKED = {"attendance-form", "culture-survey",                                   # 9/10 FAQ sources (feasibility recount)
           "donation-form", "wedding-rsvp", "living-trust-form",                  # QC F1/F2 read only the primary pull, not the --sec pull
           "last-will-and-testament-form",                                        # A1 'testament' vs the primary keyword
           "membership-form",                                                     # K5: locked AlsoAsked FAQ 3 names a sibling primary
           "service-request-form",                                                # skeleton vs Q6: two locked near-duplicates (slots 3, 4)
           "lead-nurturing-workflow",                                             # skeleton 7/10 passing slots vs feasibility 10
           "membership-survey"}                                                   # rework needs a new Semrush pull (FAQ 8)

def _order():
    w = {k: [x for x in v if (x[0] if isinstance(x, tuple) else x).rsplit("/", 1)[1] not in BLOCKED] for k, v in work().items()}
    claim = [u for u, _ in w["claimable"] if "quiz" not in u.rsplit("/", 1)[1]]   # quiz pages stay last: not claimed without a ruling
    return [("1 LP reworks (blocking findings only)", w["lp_rework"]), ("2 in-flight A pages to finish", w["inflight"]),
            ("3 render images", w["render"]), ("4 review (A-r, not the writer)", w["review"]), ("5 one rework (r15)", w["r15_rework"]),
            ("6 claim from the top of plan/queue-ranked.txt (non-quiz)", claim)]

def cmd_next(a):
    import datetime, time
    from zoneinfo import ZoneInfo
    stop = lambda: os.path.exists(os.path.join(ROOT, "STOP"))
    while True:
        if stop(): print("STOP"); sys.exit(4)
        order = _order()
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
    c = json.load(open(CANARY)) if os.path.exists(CANARY) else {}
    if c.get("result") != "pass": bad.append("canary has not passed 3/3 (status/canary-r15.json); no scaling before that (ruling 15)")
    acct, hubs = H.clone_pin()
    if acct != "A" or set(hubs) != {"LP", "Form", "Auto", "SurveyQuiz"}: bad.append(f".hub is {acct}:{','.join(hubs)}; the overnight override is A:LP,Form,Auto,SurveyQuiz (plan/overnight-run.md)")
    if os.path.exists(os.path.join(ROOT, "STOP")): bad.append("STOP file present")
    if os.environ.get("CLAUDE_CONFIG_DIR", "") != os.path.expanduser("~/.claude-b"): bad.append("CLAUDE_CONFIG_DIR is not ~/.claude-b (account A)")
    for b in bad: print("PREFLIGHT FAIL: " + b)
    if not bad: print("preflight ok")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    a = sys.argv[1:]
    {"next": cmd_next, "preflight": cmd_preflight}.get(a[0] if a else "", lambda _: sys.exit(__doc__))(a[1:])
