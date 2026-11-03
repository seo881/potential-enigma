"""redirect_check.py: the daily 843-row redirect check (Divit 2026-10-26, handback item 0). Plain Python, no Claude dependency.

Every row of reports/2026-10-23/redirects-final.csv (source,target): the source URL on the live site must answer a SINGLE-HOP 301
whose Location is exactly its target, and the target itself must return HTTP 200. It runs inside the live audit's score phase on
BOTH runners (ops/schedule/live_audit_checks.sh: the Mac launchd job and the GitHub Actions matrix run the same script), so the
findings land in audits/live/DATE/findings.json BEFORE the digest and last_success.json: digest.txt, ops/audit_status.py
real_counts and the watchdog see them like any other Layer A finding. Read-only toward the site (HEAD, GET fallback). It only
ADDS checks; it never pauses, weakens or replaces an existing one (permanent rule, Divit 2026-10-23).

  redirect_check.py run [--date RDATE] [--base URL] [--csv PATH] [--workers N] [--min-rows N]
      checks every row, writes .cache/live/RDATE/redirects.json, appends the findings to audits/live/RDATE/findings.json
      (ids in the audit's format) and prints the summary plus every failure. Exit 0 when the check COMPLETED (findings or not),
      1 when it could not run (CSV missing or truncated below --min-rows, findings.json missing).
  redirect_check.py check [--base URL] [--csv PATH] [--workers N] [--min-rows N]
      the same checks without touching findings.json (ad-hoc). Exit 3 when any row fails, 0 clean, 1 could not run.

Codes (REAL findings, never in known_open_issues; severities per Divit 2026-10-26):
  A11-redirect   P0  the source does not return a single-hop 301 to exactly its target (missing, changed, 302/307/308, a chain)
  A11-target     P1  the redirect target does not return HTTP 200 (one finding per failing target, however many rows point at it)
  A11-transport  P1  not checked: transport error after a retry (like A1-transport; a re-run clears it)
"""
import concurrent.futures, csv, datetime, json, os, sys, time
import urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "reports", "2026-10-23", "redirects-final.csv")
CANON = "https://emergent.sh"
MIN_ROWS = 843   # Divit 2026-10-26: the full 843-row set, every day; a truncated CSV must fail the run, never pass quietly
UA = "Mozilla/5.0 (emergent-redirect-check; +https://emergent.sh)"


def load_rows(path):
    with open(path, newline="") as fh:
        rd = csv.DictReader(fh)
        if rd.fieldnames != ["source", "target"]: sys.exit(f"{path}: expected header source,target, got {rd.fieldnames}")
        rows = [(r["source"].strip(), r["target"].strip()) for r in rd if (r.get("source") or "").strip()]
    bad = [s for s, t in rows if not s.startswith("/") or not t.startswith("/")]
    if bad: sys.exit(f"{path}: {len(bad)} row(s) whose source or target is not a site-absolute path (e.g. {bad[0]})")
    return rows


# ---------------------------------------------------------------- HTTP (redirects never followed)
class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None

_OPENER = urllib.request.build_opener(_NoRedirect)

def _once(url, method, timeout):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    try:
        with _OPENER.open(req, timeout=timeout) as r:
            return {"status": r.status, "location": r.headers.get("Location")}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "location": e.headers.get("Location")}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"[:160]}

def fetch(url, timeout=30):
    """One status for one URL, no redirect followed: HEAD, then GET when HEAD is not allowed; one retry on a transport error."""
    r = _once(url, "HEAD", timeout)
    if r.get("status") in (405, 501): r = _once(url, "GET", timeout)
    if r.get("error"):
        time.sleep(2); r = _once(url, "HEAD", timeout)
        if r.get("status") in (405, 501): r = _once(url, "GET", timeout)
    return r


# ---------------------------------------------------------------- pure classification (golden kind redirect-row)
def norm_location(location, base):
    """A Location header as a comparable site path: absolute URLs on the site's own host (or the canonical host) become their
    path without the trailing slash; anything else (other host, query, fragment, empty) is returned as-is and will not match."""
    if not location: return ""
    u = urllib.parse.urlsplit(location)
    hosts = {urllib.parse.urlsplit(base).hostname, "emergent.sh", "www.emergent.sh"}
    if u.query or u.fragment or (u.hostname and u.hostname.lower() not in hosts): return location
    return (u.path or "/").rstrip("/") or "/"

def classify(source, target, first, tgt, base=CANON):
    """Findings for one CSV row given the source response `first` and the target response `tgt` ({status, location} or {error}).
    Returns [{code, severity, url, msg, snippet}]; [] = the row passes. Pure: the golden suite drives it with synthetic responses."""
    out = []
    src, want = source.rstrip("/") or "/", target.rstrip("/") or "/"
    if first.get("error"):
        out.append({"code": "A11-transport", "severity": "P1", "url": src, "snippet": "",
                    "msg": f"redirect row not checked: transport error after a retry ({first['error'][:120]})"})
    else:
        st, loc = first.get("status"), norm_location(first.get("location"), base)
        if st != 301:
            out.append({"code": "A11-redirect", "severity": "P0", "url": src, "snippet": first.get("location") or "",
                        "msg": f"missing or changed redirect: source returns {st}"
                               + (f" to {first.get('location')}" if first.get("location") else " (no redirect)")
                               + f", expected a single-hop 301 to {want}"})
        elif loc != want:
            out.append({"code": "A11-redirect", "severity": "P0", "url": src, "snippet": first.get("location") or "",
                        "msg": f"changed redirect: 301 to {first.get('location') or 'nothing'}, expected exactly {want}"
                               + " (a chain or a different target)"})
    if tgt is not None:
        if tgt.get("error"):
            out.append({"code": "A11-transport", "severity": "P1", "url": want, "snippet": "",
                        "msg": f"redirect target not checked: transport error after a retry ({tgt['error'][:120]})"})
        elif tgt.get("status") != 200:
            out.append({"code": "A11-target", "severity": "P1", "url": want, "snippet": tgt.get("location") or "",
                        "msg": f"redirect target returns {tgt.get('status')}, expected 200"})
    return out


# ---------------------------------------------------------------- run over the CSV
def check_all(base, rows, workers):
    """Fetch every source and every distinct target once, classify, and dedupe the per-target findings.
    Returns (findings, results) where results is the public-safe per-row record for .cache."""
    base = base.rstrip("/")
    targets = sorted({t.rstrip("/") or "/" for _s, t in rows})
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        src_f = {s: ex.submit(fetch, base + s) for s, _t in rows}
        tgt_f = {t: ex.submit(fetch, base + t) for t in targets}
        src_r = {s: f.result() for s, f in src_f.items()}
        tgt_r = {t: f.result() for t, f in tgt_f.items()}
    findings, results, seen_tgt = [], [], set()
    n_tgt_sources = {}
    for s, t in rows: n_tgt_sources[t.rstrip("/") or "/"] = n_tgt_sources.get(t.rstrip("/") or "/", 0) + 1
    for s, t in rows:
        tk = t.rstrip("/") or "/"
        fs = classify(s, t, src_r[s], tgt_r[tk], base)
        row_fs = []
        for f in fs:
            if f["code"] in ("A11-target",) or (f["code"] == "A11-transport" and f["url"] == tk != s.rstrip("/")):
                if tk in seen_tgt: continue   # one finding per failing target, however many rows point at it
                seen_tgt.add(tk)
                if n_tgt_sources[tk] > 1: f["msg"] += f" (target of {n_tgt_sources[tk]} redirect rows)"
            row_fs.append(f)
        findings += row_fs
        results.append({"source": s, "target": t, "source_status": src_r[s].get("status"), "location": src_r[s].get("location"),
                        "source_error": src_r[s].get("error"), "target_status": tgt_r[tk].get("status"), "target_error": tgt_r[tk].get("error"),
                        "ok": not classify(s, t, src_r[s], tgt_r[tk], base)})
    return findings, results, round(time.time() - t0, 1)


def summary_lines(rows, findings, results, base, secs, workers):
    ok = sum(1 for r in results if r["ok"])
    by = lambda c: [f for f in findings if f["code"] == c]
    L = [f"redirects: {len(rows)} rows at {base} in {secs}s ({workers} workers, {len(rows) + len({r['target'] for r in results})} requests)",
         f"  rows ok {ok} of {len(rows)}; P0 A11-redirect {len(by('A11-redirect'))}; P1 A11-target {len(by('A11-target'))}; P1 A11-transport {len(by('A11-transport'))}"]
    for f in findings[:200]:
        L.append(f"  {f['severity']} {f['code']} {f['url']}: {f['msg']}")
    if len(findings) > 200: L.append(f"  ... and {len(findings) - 200} more finding(s)")
    return L


# ---------------------------------------------------------------- findings.json append (the audit's shape and id format)
def slug_of(u): return u.rstrip("/").rsplit("/", 1)[1] if u.rstrip("/").count("/") > 1 else "hub" + u.rstrip("/").replace("/", "-")

def append_findings(date, findings, n_rows, csv_path, base):
    fp = os.path.join(ROOT, "audits", "live", date, "findings.json")
    if not os.path.exists(fp): sys.exit(f"{fp} missing: run the audit's score phase first (redirect findings join that file)")
    d = json.load(open(fp)); ids = {f.get("id") for f in d["findings"]}
    for f in findings:
        k = f"{date[:10].replace('-', '')}-{slug_of(f['url'])}-{f['code']}"; n = 1
        while f"{k}-{n}" in ids: n += 1
        ids.add(f"{k}-{n}")
        f.update(id=f"{k}-{n}", field="redirect", layer="A", fix="rerun" if f["code"] == "A11-transport" else "proposed", action="proposed")
        d["findings"].append(f)
    d["redirects"] = {"rows": n_rows, "csv": os.path.relpath(csv_path, ROOT), "base": base, "failing": len(findings),
                      "checked": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
    json.dump(d, open(fp, "w"), indent=1, ensure_ascii=False)
    return fp


def main(argv):
    if not argv or argv[0] not in ("run", "check"): sys.exit(__doc__)
    a = argv[1:]
    get = lambda k, d: a[a.index(k) + 1] if k in a else d
    base = get("--base", CANON).rstrip("/"); csv_path = get("--csv", CSV)
    workers = int(get("--workers", "24")); min_rows = int(get("--min-rows", str(MIN_ROWS)))
    date = get("--date", datetime.date.today().isoformat())
    if not os.path.exists(csv_path): sys.exit(f"{csv_path} missing: the 843-row redirect set is required (Divit 2026-10-26)")
    rows = load_rows(csv_path)
    if len(rows) < min_rows: sys.exit(f"{csv_path}: only {len(rows)} rows (expected at least {min_rows}): refusing a shrunken redirect set")
    findings, results, secs = check_all(base, rows, workers)
    for l in summary_lines(rows, findings, results, base, secs, workers): print(l)
    if argv[0] == "check": sys.exit(3 if findings else 0)
    cdir = os.path.join(ROOT, ".cache", "live", date); os.makedirs(cdir, exist_ok=True)
    json.dump({"base": base, "date": date, "rows": len(rows), "results": results},
              open(os.path.join(cdir, "redirects.json"), "w"), indent=1)
    fp = append_findings(date, findings, len(rows), csv_path, base)
    print(f"appended {len(findings)} finding(s) to {os.path.relpath(fp, ROOT)}; per-row results in .cache/live/{date}/redirects.json")


if __name__ == "__main__":
    main(sys.argv[1:])
