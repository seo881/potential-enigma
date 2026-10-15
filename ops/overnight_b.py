"""overnight_b.py: code-first state for B's overnight run (ruling 20, Divit 2026-10-14; tonight's rulings: DECISIONS 2026-10-15 night).
No Claude session, no tokens, no Webflow.

    python3 ops/overnight_b.py preflight   exit 1 (reasons listed) unless: this is B's clone (~/emergent-hubs-a), CLAUDE_CONFIG_DIR is
                                           ~/.claude (account B), .hub is B:LP,Form,Auto,SurveyQuiz, the ruling-19 lift file exists
                                           (.cache/overnight-b/ruling19-lift-2026-10-15), the AlsoAsked keychain status is recorded
                                           (ok or failed; failed is not fatal), the live count is under the cap, and there is no STOP file
    python3 ops/overnight_b.py next        what the next iteration should do, in plan order (plan/overnight-run-b.md); exit 3 when
                                           nothing is left (after re-checking the ranked queue every 30 min until 08:00 IST), 4 on STOP,
                                           6 when status/live.json counts 200 live child pages (the cap: the loop stops)
    python3 ops/overnight_b.py cap         exit 6 at the live cap, else 0; prints live, room and the next ship batch size
    python3 ops/overnight_b.py tokens OUT.json OUT.txt   one session's usage from claude's JSON output -> .cache/overnight-b/tokens.jsonl;
                                           writes the result text (plus stderr) to OUT.txt for the limit checks; prints the night's
                                           total; exit 5 at TOKEN_CAP (the loop touches STOP)
    python3 ops/overnight_b.py aa-keychain the AlsoAsked keychain item is reachable from a headless-like env: prints ok or failed only
    python3 ops/overnight_b.py snapshot    the night's starting point (state counts, live count) -> .cache/overnight-b/start.json
    python3 ops/overnight_b.py report WHY  the morning report from code (no tokens): reports/<date>/0800-overnight.md (under 15
                                           lines) + a line in reports/INDEX.md, committed with ops/sync.sh; WHY = why the loop ended
"""
import datetime, json, os, subprocess, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H, guards as G

ALL_HUBS = {"LP", "Form", "Auto", "SurveyQuiz"}
QUIZ_CANARY = os.path.join(ROOT, "status", "quiz-canary.json")   # {"result": "pass"} once A's quiz canary passed (DECISIONS 2026-10-14)
RECHECK_SECS, IDLE_UNTIL = 1800, (8, 0)
LOG = os.path.expanduser("~/Library/Logs/emergent-overnight-run-b.log")
RUN = G.OVERNIGHT_DIR
TOKENS = os.path.join(RUN, "tokens.jsonl")
AA_STATUS = os.path.join(RUN, "aa-keychain")
TOKEN_CAP = 24_000_000          # DECISIONS 2026-10-15 night: weekly usage at most 70%, about 24M tokens
AA_RUN, AA_CAP = "night-r1015", 60

def stop(): return os.path.exists(os.path.join(ROOT, "STOP"))
def held_by_a(e): return bool(e.get("hold")) and H.hold_account(e["hold"]) == "A"
def is_quiz(u): return "quiz" in u.rsplit("/", 1)[1]
def quiz_ok():
    try: return json.load(open(QUIZ_CANARY)).get("result") == "pass"
    except (OSError, ValueError): return False
def quiz_canary_pages():
    try: return set(json.load(open(QUIZ_CANARY)).get("canary_pages") or [])
    except (OSError, ValueError): return set()
def live_count(): return len(G.live_child_urls())
def has_pull(u):   # existence only (the pull itself is never read here)
    return os.path.exists(os.path.join(ROOT, "private", "alsoasked", u.rsplit("/", 1)[1] + ".json"))

def aa_keychain(env=None):
    """True when `security` finds the AlsoAsked item (service alsoasked, account $USER) from a minimal env. No -w: the key is
    never even written to a pipe; only the exit status is used."""
    e = env if env is not None else {"HOME": os.path.expanduser("~"), "PATH": "/usr/bin:/bin"}
    try:
        return subprocess.run(["security", "find-generic-password", "-s", "alsoasked", "-a", os.environ.get("USER", "")],
                              env=e, capture_output=True, timeout=15).returncode == 0
    except Exception: return False
def aa_status():
    try: return open(AA_STATUS).read().strip()
    except OSError: return "unknown"

def work():
    st = {u: e for h in H.CFG["hubs"] for u, e in H.load_st(h)["pages"].items()}
    ok = lambda u, e: not held_by_a(e) and (quiz_ok() or not is_quiz(u) or u in quiz_canary_pages())
    rework = [u for u, e in st.items() if e.get("state") == "rework" and ok(u, e)]
    inflight = [u for u, e in st.items() if e.get("state") in ("claimed", "spec") and ok(u, e)
                and ((e.get("by") or "").startswith("B-") or (e.get("hold") and H.hold_account(e["hold"]) == "B"))]
    render = [u for u, e in st.items() if e.get("state") == "qc_pass" and ok(u, e)]
    review = [u for u, e in st.items() if e.get("state") == "images" and ok(u, e)]
    def slim_due(u, e):   # A-coord 2026-10-14: a rework's changed fields need a B-s slim review before the page can ship (review_ok)
        if e.get("state") != "reviewed" or not ok(u, e) or not os.path.exists(H.spath(u)): return False
        sp = json.load(open(H.spath(u)))
        return not sp.get("item_id") and bool(G.review_changed(sp))
    slim = [u for u, e in st.items() if slim_due(u, e)]
    # tonight (DECISIONS 2026-10-15 night): ship under the standing go while the lift holds and shipping is not stopped
    ship = []
    if G.ruling19_lifted() and not G.ship_stopped():
        live = G.live_child_urls()
        for u, e in st.items():
            if e.get("state") not in ("reviewed", "approved", "cms_draft") or not ok(u, e) or u in live: continue
            if not os.path.exists(H.spath(u)): continue
            sp = json.load(open(H.spath(u)))
            if G.flags_pending(sp) or (e.get("state") == "reviewed" and G.review_changed(sp) != []): continue   # flags: morning packet; slim first
            ship.append(u)
    import queue_rank as Q
    rows = Q.ranked() or []
    claim = [u for _r, _h, u, c, _f in rows if c in ("ready", "syn-pending") and u not in st and (quiz_ok() or not is_quiz(u) or u in quiz_canary_pages())]
    if aa_status() != "ok": claim.sort(key=lambda u: not has_pull(u))   # no keychain: pages with a saved pull first (stable)
    pull = []
    if aa_status() == "ok":
        try:
            import weekend as WK; left = AA_CAP - WK.run_spent(AA_RUN)
        except Exception: left = 0
        if left >= 2: pull = [u for _r, _h, u, c, _f in rows if c == "no-pull" and u not in st][:min(5, left // 2)]
    return [("0 ship (standing go, batches of 10, verify-live; flagged pages -> morning packet)", ship),
            ("1 reworks first (blocking findings only; one rework per page)", rework), ("2 in-flight B pages to finish", inflight),
            ("2b slim review (hubctl slim-review, an independent B-s agent) of fields changed after review", slim), ("3 render images", render), ("4 full review by an independent B-r agent (never a page it wrote)", review),
            ("5 claim from the top of plan/queue-ranked.txt (all 4 hubs; relevance-checked)", claim),
            (f"6 AlsoAsked pulls (weekend.py aa URL --run {AA_RUN}; {AA_CAP} credits max) for the top no-pull rows, then queue_rank.py", pull)]

def cmd_cap(a):
    n = live_count(); room = G.LIVE_CAP - n
    print(f"live {n} of {G.LIVE_CAP}; room {max(room, 0)}; next ship batch at most {max(0, min(room, 10))}")
    sys.exit(6 if room <= 0 else 0)

def cmd_next(a):
    from zoneinfo import ZoneInfo
    while True:
        if stop(): print("STOP"); sys.exit(4)
        if live_count() >= G.LIVE_CAP: print(f"CAP: {live_count()} live child pages (cap {G.LIVE_CAP}); no more shipping, writing or reviewing tonight"); sys.exit(6)
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
    print(f"live {live_count()} of {G.LIVE_CAP}; shipping " + ("STOPPED (ship-stop)" if G.ship_stopped() else "on" if G.ruling19_lifted() else "off (no lift file)")
          + f"; AlsoAsked keychain {aa_status()}")
    sys.exit(0 if left else 3)

def usage_of(d):
    """{input, output, cache_creation, cache_read} summed over modelUsage (every model, subagents included) or usage."""
    out = {"input": 0, "output": 0, "cache_creation": 0, "cache_read": 0}
    mu = d.get("modelUsage") or {}
    if mu:
        for m in mu.values():
            out["input"] += int(m.get("inputTokens") or 0); out["output"] += int(m.get("outputTokens") or 0)
            out["cache_creation"] += int(m.get("cacheCreationInputTokens") or 0); out["cache_read"] += int(m.get("cacheReadInputTokens") or 0)
        return out
    u = d.get("usage") or {}
    out.update(input=int(u.get("input_tokens") or 0), output=int(u.get("output_tokens") or 0),
               cache_creation=int(u.get("cache_creation_input_tokens") or 0), cache_read=int(u.get("cache_read_input_tokens") or 0))
    return out
def counted(u):
    """Tokens counted against the night's budget: input + output + cache writes; cache reads too when OVERNIGHT_COUNT_CACHE_READ=1."""
    return u["input"] + u["output"] + u["cache_creation"] + (u["cache_read"] if os.environ.get("OVERNIGHT_COUNT_CACHE_READ") == "1" else 0)
def night_total(path=None):
    t = 0
    try:
        for l in open(path or TOKENS):
            try: t += int(json.loads(l).get("counted") or 0)
            except ValueError: pass
    except OSError: pass
    return t
def parse_json_out(raw):
    """The last JSON object in claude's --output-format json stdout (None if none parses)."""
    i = raw.rfind('{"type"')
    while i >= 0:
        try: return json.loads(raw[i:])
        except ValueError: i = raw.rfind('{"type"', 0, i)
    try: return json.loads(raw)
    except ValueError: return None

def cmd_tokens(a, path=None):
    src, txt = a[0], a[1]; raw = open(src, errors="ignore").read() if os.path.exists(src) else ""
    err = open(src + ".err", errors="ignore").read() if os.path.exists(src + ".err") else ""
    d = parse_json_out(raw)
    open(txt, "w").write(((d or {}).get("result") or ("" if d else raw)) + ("\n" + err if err else ""))
    row = {"t": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "file": os.path.basename(src)}
    if d:
        u = usage_of(d); row.update(u, counted=counted(u), session=d.get("session_id"), is_error=d.get("is_error"), turns=d.get("num_turns"))
    else: row.update(counted=0, note="no JSON result (crash or limit before output)")
    os.makedirs(os.path.dirname(path or TOKENS), exist_ok=True)
    with open(path or TOKENS, "a") as f: f.write(json.dumps(row) + "\n")
    tot = night_total(path)
    print(f"tokens: session {row['counted']}, night {tot} of {TOKEN_CAP}")
    sys.exit(5 if tot >= TOKEN_CAP else 0)

START = os.path.join(RUN, "start.json")
def counts():
    from collections import Counter
    st = G.all_status(); c = Counter(e.get("state") for e in st.values())
    return {"states": dict(c), "live": live_count(), "standing_go": sum(1 for e in st.values() if (e.get("by") or "").startswith("standing-go")),
            "t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
def cmd_snapshot(a):
    os.makedirs(RUN, exist_ok=True); s = counts(); json.dump(s, open(START, "w"), indent=1); print(f"snapshot: live {s['live']}, states {s['states']}")

def report_lines(start, end, why, tokens, limits, credits, packet_rows, ship_stop, restored):
    d = lambda k: end["states"].get(k, 0) - start["states"].get(k, 0)
    return ["# Overnight run B, 2026-10-15 night (morning report)", "",
            f"- Ended: {why}. Ruling 19 restored at exit ({restored}).",
            f"- Live child pages: {start['live']} -> {end['live']} (cap {G.LIVE_CAP}); published tonight {end['live'] - start['live']}.",
            f"- States now: " + ", ".join(f"{k} {v}" for k, v in sorted(end["states"].items())) + ".",
            f"- Change since start: reviewed {d('reviewed'):+d}, approved {d('approved'):+d}, cms_draft {d('cms_draft'):+d}, published {d('published'):+d}, parked {d('parked'):+d}, rework {d('rework'):+d}.",
            f"- Approved by the standing go (status by): {end['standing_go'] - start.get('standing_go', 0)}.",
            f"- Holds: morning packet {packet_rows} flagged row(s) (.cache/review/morning-packet-<date>.md); ship stop: {ship_stop or 'none'}.",
            f"- Tokens counted {tokens:,} of {TOKEN_CAP:,} (.cache/overnight-b/tokens.jsonl); 5-hour session limits hit: {limits}.",
            f"- AlsoAsked: run {AA_RUN} spent {credits} of {AA_CAP} credits (credits.log).",
            "- Details: the commits since the start, ~/Library/Logs/emergent-overnight-run-b.log. The coordinator records the ruling-19 restore in DECISIONS.md."]

def cmd_report(a):
    why = " ".join(x for x in a if x != "--no-commit") or "loop ended"
    try: start = json.load(open(START))
    except (OSError, ValueError): start = {"states": {}, "live": live_count(), "standing_go": 0}
    end = counts()
    try: limits = int(open(os.path.join(RUN, "session-limits")).read().strip() or 0)
    except (OSError, ValueError): limits = 0
    try:
        import weekend as WK; credits = WK.run_spent(AA_RUN)
    except Exception: credits = "unknown"
    rows = 0
    for p in __import__("glob").glob(os.path.join(H.PACKET_DIR, "morning-packet-*.md")):
        rows += sum(1 for l in open(p) if l.startswith("| /"))
    ss = open(G.SHIP_STOP).read().strip().splitlines()[-1][:160] if G.ship_stopped() else ""
    try: restored = open(os.path.join(RUN, "ruling19-restored")).read().strip()
    except OSError: restored = "now"
    L = report_lines(start, end, why, night_total(), limits, credits, rows, ss, restored)
    day = datetime.date.today().isoformat(); rel = f"reports/{day}/0800-overnight.md"; p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write("\n".join(L) + "\n")
    idx = os.path.join(ROOT, "reports", "INDEX.md"); lines = open(idx).read().split("\n")
    entry = f"- {day} · [0800-overnight]({day}/0800-overnight.md) · B overnight (standing go): live {start['live']} -> {end['live']}; {why}; tokens {night_total():,}; AlsoAsked {credits}/{AA_CAP} · (this commit)"
    if not any(f"[0800-overnight]({day}/" in l for l in lines):
        at = next((i for i, l in enumerate(lines) if l.startswith("- ")), len(lines)); lines.insert(at, entry); open(idx, "w").write("\n".join(lines))
    print("\n".join(L))
    if "--no-commit" not in a:
        r = subprocess.run(["bash", os.path.join(ROOT, "ops", "sync.sh"), f"overnight B morning report: {why}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>", rel, "reports/INDEX.md"],
                           cwd=ROOT, capture_output=True, text=True)
        print("committed" if r.returncode == 0 else "commit failed: " + (r.stdout + r.stderr)[-300:])

def cmd_aa_keychain(a):
    ok = aa_keychain(); os.makedirs(RUN, exist_ok=True); open(AA_STATUS, "w").write("ok" if ok else "failed")
    print("ok" if ok else "failed")

def cmd_preflight(a):
    bad, notes = [], []
    if os.path.realpath(ROOT) != os.path.realpath(os.path.expanduser("~/emergent-hubs-a")): bad.append(f"this is {ROOT}, not B's clone ~/emergent-hubs-a")
    if os.environ.get("CLAUDE_CONFIG_DIR", "") != os.path.expanduser("~/.claude"): bad.append("CLAUDE_CONFIG_DIR is not ~/.claude (account B); refusing any other config dir")
    acct, hubs = H.clone_pin()
    if acct != "B" or set(hubs) != ALL_HUBS: bad.append(f".hub is {acct}:{','.join(hubs)}; ruling 20 needs B:LP,Form,Auto,SurveyQuiz")
    if not G.ruling19_lifted(): bad.append("no ruling-19 lift file (.cache/overnight-b/ruling19-lift-2026-10-15, under 18 hours old): the coordinator creates it at start")
    if stop(): bad.append("STOP file present (~/emergent-hubs-a/STOP)")
    n = live_count()
    if n >= G.LIVE_CAP: bad.append(f"{n} live child pages: the cap of {G.LIVE_CAP} is reached")
    ok = aa_keychain(); os.makedirs(RUN, exist_ok=True); open(AA_STATUS, "w").write("ok" if ok else "failed")
    notes.append("AlsoAsked keychain: " + ("ok" if ok else "failed (writers take queued pages with a saved pull first; no pulls tonight)"))
    shared = os.path.realpath(os.path.expanduser("~/emergent-hubs/private/alsoasked"))
    if os.path.realpath(os.path.join(ROOT, "private", "alsoasked")) != shared: notes.append("private/alsoasked is not the shared store: weekend.py aa will refuse pulls")
    if G.ship_stopped(): notes.append("ship-stop present: shipping stays off (writing and reviewing continue)")
    notes.append(f"live {n} of {G.LIVE_CAP}; night tokens so far {night_total()} of {TOKEN_CAP}")
    for b in bad: print("PREFLIGHT FAIL: " + b)
    for x in notes: print("preflight note: " + x)
    if not bad: print("preflight ok")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    a = sys.argv[1:]
    {"next": cmd_next, "preflight": cmd_preflight, "cap": cmd_cap, "tokens": cmd_tokens, "aa-keychain": cmd_aa_keychain,
     "snapshot": cmd_snapshot, "report": cmd_report}.get(a[0] if a else "", lambda _: sys.exit(__doc__))(a[1:])
