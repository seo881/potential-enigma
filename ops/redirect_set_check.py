"""redirect_set_check.py: pre-import verification of a whole redirect CSV (B-redir-3, Divit 2026-11-17: "prepare the final CSV
(843 rows plus the 30 fixes, all targets 200) and a pre-publish checklist for my site publish this week").

ops/redirect_check.py checks what the LIVE site serves for each row (source 301 -> target, target 200). Before an import the
sources still answer with the OLD targets, so that check cannot pass yet. This script checks the FILE itself, read-only:

  S1-header     the header is exactly `source,target`
  S2-path       source and target are site-absolute paths (start with "/", no host, no query, no fragment)
  S3-dup        a source appears more than once (after trailing-slash and case normalisation)
  S4-self       a row redirects to itself
  S5-chain      a target is itself a source in the file (a 2-hop chain after import)
  S6-shadow     a source is a live child page (status/live.json) or one of the 4 hub paths: the redirect would hide a live page
  S7-notlive    a target under a hub path is not a live child page in status/live.json (renamed or unpublished slug)
  T1-target     the target does not return HTTP 200 directly (HEAD, GET fallback, redirects NOT followed); 5xx is re-fetched
                up to 3 times with a pause (Webflow serves an occasional transient 500), the status after the retries counts

  redirect_set_check.py verify --csv PATH [--old PATH] [--base URL] [--workers N] [--out PATH.md]
      every check above; --old lists each row whose target differs from that file (the fixes) with both targets' status.
      Exit 0 when no finding, 3 when any finding, 1 when it could not run.

The pure part (static_issues) is driven by the golden suite (kind redirect-set). Read-only toward the site; no Webflow call.
"""
import concurrent.futures, csv, datetime, json, os, sys, time, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import redirect_check as RC  # noqa: E402  (fetch without redirect follow, the daily check's HTTP)

HUB_PATHS = ("/ai-landing-page-builder", "/ai-form-builder", "/ai-automation-builder", "/ai-survey-and-quiz-builder")


def norm(p):
    return (p or "").strip().rstrip("/").lower() or "/"


def read_csv(path):
    with open(path, newline="") as fh:
        rd = csv.reader(fh)
        header = next(rd, None)
        rows = [(r[0].strip(), r[1].strip() if len(r) > 1 else "") for r in rd if r and r[0].strip()]
    return header, rows


def live_child_paths(path=os.path.join(ROOT, "status", "live.json")):
    d = json.load(open(path))
    return {norm(u) for u, v in d["pages"].items() if isinstance(v, dict) and v.get("live")}


def _is_path(p):
    if not p.startswith("/") or p.startswith("//"): return False
    u = urllib.parse.urlsplit(p)
    return not (u.scheme or u.netloc or u.query or u.fragment)


def static_issues(header, rows, live_paths, hub_paths=HUB_PATHS):
    """Pure: [(code, source, target, msg)] for the file checks S1-S7. [] = the file is clean."""
    out = []
    if header != ["source", "target"]:
        out.append(("S1-header", "", "", f"header is {header}, expected ['source', 'target']"))
    hubs = {norm(h) for h in hub_paths}
    seen, srcs = {}, {norm(s) for s, _t in rows}
    for s, t in rows:
        if not _is_path(s) or not _is_path(t):
            out.append(("S2-path", s, t, "source or target is not a site-absolute path")); continue
        ns, nt = norm(s), norm(t)
        if ns in seen: out.append(("S3-dup", s, t, f"duplicate source (also row {seen[ns]})"))
        seen.setdefault(ns, len(seen) + 1)
        if ns == nt: out.append(("S4-self", s, t, "row redirects to itself"))
        elif nt in srcs: out.append(("S5-chain", s, t, "target is itself a source: a 2-hop chain after import"))
        if ns in live_paths or ns in hubs:
            out.append(("S6-shadow", s, t, "source is a live child page or hub URL: the redirect would hide it"))
        hub = next((h for h in hubs if nt.startswith(h + "/")), None)
        if hub and nt not in live_paths:
            out.append(("S7-notlive", s, t, "target is under a hub path but not a live child page in status/live.json"))
    return out


def fetch_target(base, path, tries=3, pause=4):
    """Status of one target, redirects not followed; a 5xx or transport error is re-fetched up to `tries` more times."""
    r = RC.fetch(base + path); n = 0
    while (r.get("error") or (r.get("status") or 0) >= 500) and n < tries:
        time.sleep(pause); r = RC.fetch(base + path); n += 1
    r["retries"] = n
    return r


def main(argv):
    if not argv or argv[0] != "verify": sys.exit(__doc__)
    a = argv[1:]
    get = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    path = get("--csv"); old = get("--old"); base = get("--base", RC.CANON).rstrip("/")
    workers = int(get("--workers", "12")); out = get("--out")
    if not path or not os.path.exists(path): sys.exit(f"--csv {path}: missing")
    header, rows = read_csv(path)
    live = live_child_paths()
    issues = static_issues(header, rows, live)
    targets = sorted({t for _s, t in rows})
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        res = dict(zip(targets, ex.map(lambda t: fetch_target(base, t), targets)))
    for s, t in rows:
        r = res[t]
        if r.get("status") != 200:
            issues.append(("T1-target", s, t, f"target returns {r.get('status') or r.get('error')}"
                           + (f" -> {r.get('location')}" if r.get("location") else "") + ", expected 200 directly"))
    fixes = []
    if old:
        _oh, orows = read_csv(old); od = dict(orows)
        missing = [s for s in od if s not in dict(rows)]
        added = [s for s, _t in rows if s not in od]
        for s, t in rows:
            if s in od and od[s] != t: fixes.append((s, od[s], t))
        old_t = sorted({o for _s, o, _t in fixes})
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
            old_res = dict(zip(old_t, ex.map(lambda t: RC.fetch(base + t), old_t)))
    secs = round(time.time() - t0, 1)
    retried = {t: r["retries"] for t, r in res.items() if r.get("retries")}
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = [f"# Redirect CSV verification: {os.path.relpath(path, ROOT)}", "",
         f"Run {now} by `ops/redirect_set_check.py verify` against {base} (read-only HEAD, GET fallback, redirects not followed), {secs}s.", "",
         "## Totals", "",
         f"- Rows: {len(rows)} (+ header `{','.join(header or [])}`); distinct sources {len({norm(s) for s, _ in rows})}; distinct targets {len(targets)}",
         f"- Live child pages checked against (status/live.json): {len(live)}; hub paths: {len(HUB_PATHS)}",
         f"- Targets returning 200 directly: {sum(1 for r in res.values() if r.get('status') == 200)} of {len(targets)}"
         + (f" ({len(retried)} needed a re-fetch after a 5xx/transport error: {', '.join(f'{k} x{v}' for k, v in sorted(retried.items()))})" if retried else ""),
         ]
    if old:
        L.append(f"- Against {os.path.relpath(old, ROOT)}: sources kept {len(rows) - len(added)}, added {len(added)}, dropped {len(missing)}; targets changed {len(fixes)}")
    by = {}
    for c, *_ in issues: by[c] = by.get(c, 0) + 1
    codes = ["S1-header", "S2-path", "S3-dup", "S4-self", "S5-chain", "S6-shadow", "S7-notlive", "T1-target"]
    L.append("- Findings: " + "; ".join(f"{c} {by.get(c, 0)}" for c in codes) + f"; **total {len(issues)}**")
    if fixes:
        L += ["", f"## Changed rows ({len(fixes)})", "", "| # | source | old target (status today) | new target (status today) |", "|---|---|---|---|"]
        for i, (s, o, t) in enumerate(fixes, 1):
            os_ = old_res[o].get("status") or old_res[o].get("error")
            loc = RC.norm_location(old_res[o].get("location"), base) if old_res[o].get("location") else ""
            L.append(f"| {i} | {s} | {o} ({os_}{' -> ' + loc if loc else ''}) | {t} ({res[t].get('status') or res[t].get('error')}) |")
    L += ["", "## Findings", ""]
    L += [f"- {c} {s} -> {t}: {m}" for c, s, t, m in issues] or ["None: 0 failures."]
    text = "\n".join(L) + "\n"
    if out:
        with open(out, "w") as fh: fh.write(text)
    print(text)
    sys.exit(3 if issues else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
