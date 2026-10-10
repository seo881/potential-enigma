"""weekend.py: the weekend run's state machine (Divit, 2026-10-10). Code decides what comes next; the headless session does the
agent work. Plan, rules and position: plan/weekend-run.md. Loop: ops/schedule/weekend_run.sh. No Webflow calls anywhere.

  weekend.py init                 build plan/batches/wk-rework-<dir>.txt once (written pages that are not live, held, parked or in Webflow)
  weekend.py next                 the next work unit (claims new pages itself, canary per hub); exit 0 work, 3 exhausted, 4 STOP file
  weekend.py add-new URL --by ID [--fail TEXT]   a new page's writer returned: into plan/batches/wk-new-<dir>.txt (ledger at check)
  weekend.py aa URL [--fresh]     AlsoAsked pull for one page within the weekend cap (300 credits, 2 per page) via ops/alsoasked_pull.py
  weekend.py render [SLUG..]      render queued pages locally now and commit them (default: the render queue); wait-render is an alias
  weekend.py commit URL MESSAGE   commit and push one page (spec, status, batch files) through ops/sync.sh, under a git lock
  weekend.py tick [--final]       park pages stopped twice, readiness board, position in plan/weekend-run.md, a report every 10 pages
  weekend.py credits              AlsoAsked credits used this weekend
  weekend.py block-new REASON | unblock-new   hold or release the new-page phase (e.g. DataForSEO MCP not authenticated)
Public state (no question text, no SERP data): status/weekend-run.json.
"""
import contextlib, datetime, glob, io, json, os, re, subprocess, sys, time
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ops")); sys.path.insert(0, os.path.join(ROOT, "qc")); sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import hubctl as H, guards as G, ship as S

ORDER = ["LP", "Auto", "SurveyQuiz", "Form"]                       # Divit: LP, Automation, SurveyQuiz, then Form
HELD = {"consultation-form", "checkout-form", "conference-registration-form", "summer-camp-registration-form", "contact-form",
        "thank-you-page", "creator-application", "approval-workflow", "customer-satisfaction"}   # DECISIONS 2026-10-09 and the 4 originals
CREDIT_CAP, PER_PAGE = 300, 2
STATE = os.path.join(ROOT, "status", "weekend-run.json")
PLAN = os.path.join(ROOT, "plan", "weekend-run.md")
STOP = os.path.join(ROOT, "STOP")
CREDITS_LOG = os.path.join(ROOT, "private", "alsoasked", "credits.log")
TERMINAL = {"payload", "done", "stopped"}
WRITTEN = {"qc_pass", "images", "reviewed", "rework"}
CANARY, INFLIGHT_MAX, CLAIM_STEP = 3, 8, 4

def now(): return datetime.datetime.now(datetime.timezone.utc)
def ts(): return now().strftime("%Y-%m-%d %H:%M UTC")
def load():
    if os.path.exists(STATE): return json.load(open(STATE))
    return {"started": now().isoformat(timespec="seconds"), "new": {}, "reported": [], "reports": 0, "holds": {}}
def save(W): json.dump(W, open(STATE, "w"), indent=1, sort_keys=True)
def hdir(hub): return H.CFG["hubs"][hub]["repo_dir"]
def bfile(kind, hub): return os.path.join(ROOT, "plan", "batches", f"wk-{kind}-{hdir(hub)}.txt")
def slug(u): return u.rsplit("/", 1)[1]
def sync(msg, paths):
    with G.lock("git"):
        r = subprocess.run(["bash", os.path.join(ROOT, "ops", "sync.sh"), msg, *paths], cwd=ROOT, capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-400:]); return r.returncode

# ---------------------------------------------------------------- init
def cmd_init(args):
    st = G.all_status(); m = H.kmap(); made = []
    for hub in ORDER:
        p = bfile("rework", hub)
        if os.path.exists(p): continue
        urls = []
        for u, e in st.items():
            if H.hub_of(u) != hub or e.get("state") not in WRITTEN or slug(u) in HELD: continue
            try: s = json.load(open(H.spath(u)))
            except FileNotFoundError: continue
            if s.get("item_id"): continue                             # in Webflow already: live or held draft, never touched here
            urls.append(u)
        urls.sort(key=lambda u: (m.get(u) or {}).get("queue_rank", 9999))
        open(p, "w").write(f"# Weekend run rework, {hub} (Divit 2026-10-10): written pages, not live, held, parked or in Webflow; queue order\n" + "".join(u + "\n" for u in urls))
        made.append(f"{os.path.relpath(p, ROOT)}: {len(urls)} pages")
    W = load(); save(W); print("\n".join(made) or "batch files already exist")

# ---------------------------------------------------------------- next
def ledger(bf): return S.load_ledger(bf) if os.path.exists(bf) else {"pages": {}}
def ship_quiet(bf, want=4):
    """hubctl ship for one batch, bounded: pages already under way advance; untouched pages start (autofix + brief) only while
    fewer than `want` pages wait on a writer, so one call never autofixes a whole hub. The readiness board is left to tick."""
    L = S.load_ledger(bf); queue = set()
    for u in S.batch_urls(bf):
        P = L["pages"][u]
        if P["stage"] in TERMINAL: continue
        if P["stage"] == "autofix" and sum(Q["stage"] in ("writer", "rework") for Q in L["pages"].values()) >= want: continue
        try: S.advance(u, P, queue)
        except SystemExit as e: S.fail(P, P["stage"], f"error: {e}", P["stage"])
        except Exception as e: S.fail(P, P["stage"], f"{type(e).__name__}: {e}", P["stage"])
        S.save_ledger(bf, L)
    if queue:
        q = os.path.join(ROOT, "status", "render-queue.txt"); have = set(l.strip() for l in open(q)) if os.path.exists(q) else set()
        open(q, "w").write("".join(x + "\n" for x in sorted(have | queue)))
    return L
def planned_left(hub):
    st = H.load_st(hub)["pages"]
    return [p for p in H.kmap().values() if p["hub"] == hub and p["status"] == "planned" and p["url"] not in st]

PARALLEL_NEW = ["LP", "Auto", "SurveyQuiz"]   # Divit 2026-10-10: canaries for these 3 hubs at once (9 pages); Form new pages only when they are idle
MAX_UNITS = 4                                 # writer/review units handed out per next, across hubs

def new_units(hub, waits, holds):
    """New-page units for one hub, claiming its canary (or the next step) when allowed. Canary rule per hub: no 4th page until
    the first 3 are through review (TERMINAL stage)."""
    W = load(); mine = W["new"].setdefault(hub, []); bf = bfile("new", hub)
    L = ship_quiet(bf) if os.path.exists(bf) and S.batch_urls(bf) else {"pages": {}}
    unwritten = [u for u in mine if u not in L["pages"] and H.load_st(hub)["pages"].get(u, {}).get("state") in ("claimed", "spec", None)]
    out = [f"WRITE-NEW {u}" for u in unwritten[:4]] + (unit(hub, bf, L, waits) if L["pages"] else [])
    if out: return out
    stage = lambda u: (L["pages"].get(u) or {}).get("stage", "writer")
    inflight = [u for u in mine if stage(u) not in TERMINAL]
    if len(mine) < CANARY: n = CANARY - len(mine)
    elif any(stage(u) not in TERMINAL for u in mine[:CANARY]): holds[hub] = "canary: first 3 new pages not through review yet"; return []
    elif sum(stage(u) == "stopped" for u in mine[:CANARY]) >= 2: holds[hub] = "canary failed: 2 of the first 3 new pages parked; no more claims for this hub"; return []
    elif len(inflight) >= INFLIGHT_MAX: return []
    else: n = CLAIM_STEP
    if not planned_left(hub): return []
    r = subprocess.run([sys.executable, os.path.join(ROOT, "ops", "hubctl.py"), "claim", hub, str(n), "--by", "weekend"], cwd=ROOT, capture_output=True, text=True)
    got = re.findall(r"^claimed #\S+\s+(\S+)", r.stdout, re.M)
    if not got: holds[hub] = f"claim failed: {(r.stdout + r.stderr).strip()[-200:]}"; return []
    W = load(); W["new"].setdefault(hub, []).extend(got); save(W)
    sync(f"weekend: claim {len(got)} new {hub} page(s)", ["status/"])
    return [f"WRITE-NEW {u}" for u in got]

def cmd_next(args):
    if os.path.exists(STOP): print("STOP: ~/emergent-hubs/STOP exists; finish nothing new, exit"); sys.exit(4)
    W = load(); waits = []; holds = {}; lanes = []   # one lane per hub and phase; units are dealt round-robin so every hub stays busy
    # 1. rework phase, every hub
    for hub in ORDER:
        bf = bfile("rework", hub)
        if not os.path.exists(bf) or not S.batch_urls(bf): continue
        u_ = unit(hub, bf, ship_quiet(bf), waits)
        if u_: lanes.append(u_)
    # 2. new pages, canary per hub; LP, Automation and SurveyQuiz in parallel, Form only when those three have nothing to do
    if W.get("block_new"): holds["new pages"] = W["block_new"]
    else:
        par = [u_ for u_ in (new_units(h, waits, holds) for h in PARALLEL_NEW) if u_]
        lanes += par
        if not par:
            for h in [h for h in ORDER if h not in PARALLEL_NEW]:
                u_ = new_units(h, waits, holds)
                if u_: lanes.append(u_)
    out = []
    while lanes and len(out) < MAX_UNITS:
        for l in list(lanes):
            if len(out) >= MAX_UNITS: break
            out.append(l.pop(0))
            if not l: lanes.remove(l)
    W = load(); W["holds"] = holds; save(W)
    if out:
        print("\n".join(out)); sync("weekend: ship ledgers, autofix, render queue", ["status/", "plan/batches/", "specs/"]); return
    if waits:
        print("WAIT-RENDER " + " ".join(sorted(set(waits)))); sync("weekend: ship ledgers, autofix, render queue", ["status/", "plan/batches/", "specs/"]); return
    print("EXHAUSTED: no actionable page in any rework batch or new-page queue" + (f" (holds: {holds})" if holds else "")); sys.exit(3)

def unit(hub, bf, L, waits):
    """Actions for one batch: up to 4 writer and 4 rework passes, review groups of 4 (fewer only when no page of the batch can still join)."""
    rel = os.path.relpath(bf, ROOT); out = []
    by = {}
    for u, P in L["pages"].items(): by.setdefault(P["stage"], []).append(u)
    out += [f"WRITER {rel} {u} brief {L['pages'][u].get('brief')}" for u in by.get("writer", [])[:4]]
    out += [f"REWORK {rel} {u} brief {L['pages'][u].get('brief')}" for u in by.get("rework", [])[:4]]
    rv = by.get("review", []); upstream = sum(len(by.get(k, [])) for k in ("autofix", "writer", "check", "images"))
    groups = [rv[i:i + 4] for i in range(0, len(rv), 4)]
    if groups and len(groups[-1]) < 4 and upstream: groups.pop()
    out += [f"REVIEW {rel} " + " ".join(g) for g in groups[:2]]
    waits += [slug(u) for u in by.get("images", []) + by.get("images2", [])]
    return out

# ---------------------------------------------------------------- new pages, AlsoAsked, renders, commits
def cmd_add_new(args):
    url = args[0]; by = args[args.index("--by") + 1]; hub = H.hub_of(url); bf = bfile("new", hub)
    have = S.batch_urls(bf) if os.path.exists(bf) else []
    if url not in have:
        fresh = not os.path.exists(bf)
        with open(bf, "a") as fh:
            if fresh: fh.write(f"# Weekend run new pages, {hub} (Divit 2026-10-10): claim order\n")
            fh.write(url + "\n")
    L = S.load_ledger(bf); P = L["pages"][url]
    if "--fail" in args: S.fail(P, "writer", args[args.index("--fail") + 1], "writer")
    elif P["stage"] in ("autofix", "writer"): P["writer_by"] = by; P["stage"] = "check"; S.note(P, "writer", True, f"new page by {by}")
    S.save_ledger(bf, L); print(f"{url}: {P['stage']}")

def credits_rows(since):
    if not os.path.exists(CREDITS_LOG): return []
    rows = []
    for l in open(CREDITS_LOG):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get("t", "") >= since: rows.append(r)
    return rows
def spent(r): return sum(v for v in (r.get("used") or {}).values() if isinstance(v, (int, float)) and v > 0) or (1 if r.get("post") and not (r.get("used") or {}) else 0)
def cmd_credits(args):
    W = load(); rows = credits_rows(W["started"]); per = Counter()
    for r in rows: per[r.get("slug")] += spent(r)
    print(f"weekend credits used {sum(per.values())} of {CREDIT_CAP} on {len(per)} page(s); max per page {max(per.values()) if per else 0}")
    return sum(per.values()), per
def cmd_aa(args):
    url = args[0]; s = slug(url); total, per = cmd_credits([])
    if per[s] >= PER_PAGE: sys.exit(f"{s}: already {per[s]} credits this weekend (cap {PER_PAGE} per page); write from the sources you have or fail the page")
    if total + PER_PAGE > CREDIT_CAP: sys.exit(f"weekend AlsoAsked cap reached ({total}/{CREDIT_CAP}); no more pulls")
    primary = (H.kmap().get(url) or {}).get("primary") or sys.exit("not in the keyword map")
    cmd = [sys.executable, os.path.join(ROOT, "ops", "alsoasked_pull.py"), s, primary, "--depth", "2"] + (["--fresh"] if "--fresh" in args else [])
    sys.exit(subprocess.call(cmd, cwd=ROOT))

def cmd_render(args):
    """Render queued pages on this Mac now (no wait on the Action; Divit 2026-10-10), then commit only those pages' images and specs."""
    import render_changed as RC
    with G.lock("render"):
        q = os.path.join(ROOT, "status", "render-queue.txt")
        slugs = list(args) or ([l.strip() for l in open(q) if l.strip() and not l.startswith("#")] if os.path.exists(q) else [])
        urls = {slug(u): u for u in G.all_status()}
        bp = os.path.join(ROOT, ".cache", "weekend", "render_blocked.json"); blocked = json.load(open(bp)) if os.path.exists(bp) else {}
        spec_of = lambda s_: dict(json.load(open(H.spath(urls[s_]))), _path=H.spath(urls[s_]))
        todo = [s_ for s_ in slugs if s_ in urls and not RC.current(spec_of(s_)) and blocked.get(s_) != RC.brief_hash(spec_of(s_))]   # a brief that already failed waits for its fix
        if not todo: print(f"rendered 0 of {len(slugs)}; all current or blocked"); return
        r = subprocess.run([sys.executable, os.path.join(ROOT, "ops", "render_changed.py"), "--pages", ",".join(todo), "--no-commit"], cwd=ROOT, capture_output=True, text=True)
        print((r.stdout + r.stderr).strip()[-1500:])
        for s_ in todo:
            if not RC.current(spec_of(s_)): blocked[s_] = RC.brief_hash(spec_of(s_))
        os.makedirs(os.path.dirname(bp), exist_ok=True); json.dump(blocked, open(bp, "w"), indent=1)
        paths = ["status/render-queue.txt"]
        for s_ in todo:
            sp = H.spath(urls[s_]); paths += [os.path.relpath(sp, ROOT), os.path.relpath(RC.render_dir(dict(json.load(open(sp)), _path=sp)), ROOT)]
        sync(f"weekend: render {len(todo)} page(s) locally", [p for p in paths if os.path.exists(os.path.join(ROOT, p))])
cmd_wait_render = cmd_render   # old name kept for sessions that still call it: it renders now instead of waiting

def cmd_commit(args):
    url, msg = args[0], args[1]
    sys.exit(sync(f"weekend: {slug(url)}: {msg}", [os.path.relpath(H.spath(url), ROOT), "status/", "plan/batches/"]))

# ---------------------------------------------------------------- tick: park, readiness, position, reports
def all_ledgers():
    out = {}
    for hub in ORDER:
        for kind in ("rework", "new"):
            bf = bfile(kind, hub)
            if os.path.exists(bf) and S.batch_urls(bf):
                for u, P in S.load_ledger(bf)["pages"].items(): out[u] = (kind, hub, P)
    return out
def usage_by_page(urls):
    per = {}
    p = G.usage_path()
    if os.path.exists(p):
        for l in open(p):
            r = json.loads(l)
            if r["url"] in urls and str(r.get("agent", "")).startswith("wk-"): per.setdefault(r["url"], Counter())[r["role"]] += int(r["tokens"])
    return per

def cmd_tick(args):
    W = load(); Ls = all_ledgers(); parked = []
    for u, (kind, hub, P) in Ls.items():
        if P["stage"] == "stopped" and H.load_st(hub)["pages"].get(u, {}).get("state") != "parked":
            H.set_state(u, "parked", note=f"weekend run: {P.get('stopped')}", via="weekend", by="weekend"); parked.append(u)
    S.write_readiness()
    fin = [u for u, (_, _, P) in Ls.items() if P["stage"] in TERMINAL and u not in W["reported"]]
    paths = ["status/", "plan/weekend-run.md"]
    if len(fin) >= 10 or (args[:1] == ["--final"] and fin):
        paths.append(write_report(W, fin, Ls, final=args[:1] == ["--final"])); W["reported"] += fin; W["reports"] += 1
    save(W); write_position(W, Ls)
    if len(paths) > 2: paths.append("reports/")
    sync("weekend: tick" + (f", {len(parked)} parked" if parked else "") + (", report" if len(paths) > 2 else ""), paths)

def counts(Ls):
    c = Counter()
    for u, (kind, hub, P) in Ls.items(): c[(kind, hub, "ready" if P["stage"] in ("payload", "done") else P["stage"])] += 1
    return c
def write_position(W, Ls):
    c = counts(Ls); rows = []
    for kind in ("rework", "new"):
        for hub in ORDER:
            n = sum(v for (k, h, _), v in c.items() if k == kind and h == hub)
            if n: rows.append(f"| {kind} | {hub} | {n} | " + ", ".join(f"{s} {v}" for (k, h, s), v in sorted(c.items()) if k == kind and h == hub) + " |")
    total, _ = cmd_credits([]) if os.path.exists(CREDITS_LOG) else (0, None)
    pos = ["<!-- position:start (written by ops/weekend.py tick; do not edit by hand) -->", f"Updated {ts()}. Started {W['started']}.", "",
           "| Phase | Hub | Pages | Stages |", "|---|---|---|---|", *(rows or ["| - | - | 0 | not started |"]), "",
           f"New pages claimed this weekend: " + (", ".join(f"{h} {len(v)}" for h, v in W["new"].items() if v) or "none") + ".",
           f"Holds: " + ("; ".join(f"{h}: {v}" for h, v in (W.get("holds") or {}).items()) or "none") + ".",
           f"AlsoAsked credits this weekend: {total} of {CREDIT_CAP}. Reports written: {W['reports']}.",
           "Next step: run `.venv/bin/python3 ops/weekend.py next` and do what it prints.", "<!-- position:end -->"]
    txt = open(PLAN).read()
    txt = re.sub(r"<!-- position:start.*?<!-- position:end -->", "\n".join(pos), txt, flags=re.S)
    open(PLAN, "w").write(txt)

def write_report(W, fin, Ls, final=False):
    d = now().astimezone(); day = d.strftime("%Y-%m-%d"); n = W["reports"] + 1
    name = f"{d.strftime('%H%M')}-weekend-run-{n}"; rel = f"reports/{day}/{name}.md"; os.makedirs(os.path.join(ROOT, "reports", day), exist_ok=True)
    ready = [u for u in fin if Ls[u][2]["stage"] in ("payload", "done")]; stopped = [u for u in fin if Ls[u][2]["stage"] == "stopped"]
    use = usage_by_page(set(fin)); total, _ = cmd_credits([]) if os.path.exists(CREDITS_LOG) else (0, None)
    tok = [sum(c.values()) for c in use.values()]
    L = [f"# Weekend run report {n}" + (" (final)" if final else ""), "",
         "## Request", "", "Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: \"Continue the weekend run per plan/weekend-run.md\".", "",
         "**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.", "",
         "## Actions and results", "",
         f"{len(fin)} pages finished since the last report: {len(ready)} reviewed and ready for Divit, {len(stopped)} parked.", ""]
    L += [f"- ready: {u} ({Ls[u][0]})" for u in ready] + [f"- parked: {u} ({Ls[u][0]}): {Ls[u][2].get('stopped')}" for u in stopped]
    c = counts(Ls)
    L += ["", "## Numbers", "", f"- Weekend totals: " + ", ".join(f"{k} {h} {s} {v}" for (k, h, s), v in sorted(c.items())),
          f"- Tokens per finished page (logged agents): " + (f"median {sorted(tok)[len(tok) // 2]}, mean {sum(tok) // len(tok)}, pages with a log {len(tok)}" if tok else "none logged"),
          *[f"  - {u}: " + ", ".join(f"{r} {v}" for r, v in use[u].items()) for u in sorted(use)],
          f"- AlsoAsked credits used this weekend: {total} of {CREDIT_CAP}", "",
          "## Decisions", "", "- Rules applied: DECISIONS 2026-10-09 (PA14, PA15, D1, D2, F9) and 2026-10-10 (D3, serial comma H3); HUB_RULES section 5; rules/SEVERITY.md for review.",
          "- One review per page (batch of up to 4), one rework; a page failing a stage twice is parked (ops/ship.py MAX_FAILS, DECISIONS 2026-10-07).",
          "- New pages: canary of 3 per hub through review before more claims (Divit 2026-10-10).", "",
          "## Files changed and commits", "", "- specs/, status/ (ledgers status/ship/wk-*.json, status/weekend-run.json, status/readiness.md), plan/batches/wk-*.txt, plan/weekend-run.md; SHAs: `git log --grep '^weekend:'`.", "",
          "## Webflow calls", "", "None (weekend run: no Webflow tools).", "",
          "## Not done", "", "- Nothing created or published in Webflow; Divit's preview review and the Monday staging canary come first.", "",
          "## Open questions for Divit", "", "- Parked pages above: rescue or drop (default: leave parked until after the Monday canary)."]
    open(os.path.join(ROOT, rel), "w").write("\n".join(L) + "\n")
    idx = os.path.join(ROOT, "reports", "INDEX.md"); lines = open(idx).read().split("\n")
    at = next(i for i, l in enumerate(lines) if l.startswith("- "))
    lines.insert(at, f"- {day} · [{name}]({day}/{name}.md) · Weekend run: {len(ready)} pages reviewed, {len(stopped)} parked; {total} AlsoAsked credits so far; no Webflow calls · this commit")
    open(idx, "w").write("\n".join(lines)); return rel

def cmd_block_new(args):
    W = load(); W["block_new"] = (" ".join(args) or "blocked") + f" ({ts()})"; save(W); print("new-page phase held:", W["block_new"])
    sync("weekend: new-page phase held", ["status/weekend-run.json"])
def cmd_unblock_new(args):
    W = load(); W.pop("block_new", None); save(W); print("new-page phase released")
    sync("weekend: new-page phase released", ["status/weekend-run.json"])

CMDS = {"block-new": cmd_block_new, "unblock-new": cmd_unblock_new, "init": cmd_init, "next": cmd_next, "add-new": cmd_add_new, "aa": cmd_aa, "wait-render": cmd_wait_render, "render": cmd_render,
        "commit": cmd_commit, "tick": cmd_tick, "credits": cmd_credits}
if __name__ == "__main__":
    os.chdir(ROOT)
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS: sys.exit(__doc__)
    CMDS[sys.argv[1]](sys.argv[2:])
