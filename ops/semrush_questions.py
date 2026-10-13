"""semrush_questions.py: Semrush phrase_questions (database us) as a keyword-sourced FAQ source (Divit 2026-10-13, pilot first).

Semrush data stays out of git: raw responses, the call ledger and the per-page results live in private/semrush/questions/.
Calls go through the Semrush MCP (execute_report phrase_questions); this script plans them, caches each response once, and filters.

    python3 ops/semrush_questions.py plan URL...          the phrases per page (head phrase + top 2 secondaries) and which are cached
    python3 ops/semrush_questions.py balance              read the API unit balance (free endpoint; key from the macOS keychain, service semrush)
    python3 ops/semrush_questions.py fetch URL... [--limit 30] [--cap N]   call phrase_questions for each uncached phrase of the pages,
                                                          one at a time, cache the raw response, log real units (balance before/after)
    python3 ops/semrush_questions.py save PHRASE FILE [--limit N]   cache one MCP response (rows: keyword, volume) for PHRASE; refuses a repeat
    python3 ops/semrush_questions.py derive URL...        filter the cached rows into usable questions per page -> private/.../derived/<slug>.json
    python3 ops/semrush_questions.py report URL...        per page: rows, usable, feasibility now, units (counts only; safe for a report)

Filter (Divit 2026-10-13): keep a question only if it contains the page's full head phrase or an approved multi-word variant
(rules/paa_synonyms.json), contiguous and in order; drop political, personal-finance advice, salary, best/top-N listicle and
competitor-brand questions; it must pass the PAA gate as a keyword source with 0 rejects; dedupe against the page's existing
candidates (FAQ, AlsoAsked pull, secondaries) and against each other. Keyword-sourced: the writer may reword into a natural question
only if the head phrase stays (backlog line 91); provenance records the source keyword and its volume.
Budget (Divit 2026-10-13): never repeat a call for the same phrase and database; display_limit 30 first; pilot cap 35 calls.
"""
import contextlib, datetime, io, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H, paa_gate as P

BASE = os.path.join(ROOT, "private", "semrush", "questions")
RAW, DER, LEDGER = os.path.join(BASE, "raw"), os.path.join(BASE, "derived"), os.path.join(BASE, "ledger.jsonl")
DB = "us"
UNITS_PER_ROW = 40   # estimate from Semrush's published API price list for phrase_questions; the balance read is the truth
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
def key(phrase): return DB + "__" + re.sub(r"[^a-z0-9]+", "-", phrase.lower()).strip("-")
def raw_path(phrase): return os.path.join(RAW, key(phrase) + ".json")
def quiet(f, *a):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a)

def phrases(url):
    """The page's head phrase plus its top 2 secondaries by MSV (PA15-allowed, not the primary in another inflection)."""
    m = H.kmap().get(url) or {}; prim = m.get("primary") or ""; out = [prim]
    fm = json.load(open(os.path.join(ROOT, "rules", "paa_blocklist.json"))).get("pa15_formats", [])
    seen = {frozenset(P.content(prim))}
    for x in sorted(m.get("secondaries") or [], key=lambda x: -(x.get("msv") or 0)):
        k = P.norm(x.get("kw") or ""); c = frozenset(P.content(k))
        if not k or c in seen or any(P.has(f, k) for f in fm): continue
        seen.add(c); out.append(x["kw"])
        if len(out) == 3: break
    return out

def calls_made():
    return [json.loads(l) for l in open(LEDGER)] if os.path.exists(LEDGER) else []

def _key():
    import subprocess
    k = subprocess.run(["security", "find-generic-password", "-a", os.environ.get("USER", ""), "-s", "semrush", "-w"], capture_output=True, text=True).stdout.strip()
    if not k: sys.exit("no Semrush key in the keychain (service semrush)")
    return k
def _get(u, timeout=60):
    """GET with backoff on HTTP 429/5xx (shared API key: the discovery agent runs too)."""
    import urllib.request, urllib.error, time
    for k in range(6):
        try: return urllib.request.urlopen(u, timeout=timeout).read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and k < 5: time.sleep(15 * (k + 1)); continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if k < 5: time.sleep(15 * (k + 1)); continue
            raise
def balance():
    return int(_get("https://www.semrush.com/users/countapiunits.html?key=" + _key(), timeout=30).strip())
def cmd_balance(a): print(f"{now()} Semrush API units: {balance()}")
def cmd_fetch(a):
    import urllib.request, urllib.parse
    lim = int(a[a.index("--limit") + 1]) if "--limit" in a else 30; cap = int(a[a.index("--cap") + 1]) if "--cap" in a else None
    urls = [x for x in a if x.startswith("/")]; made = 0
    if "--urls-file" in a: urls += [l.strip() for l in open(a[a.index("--urls-file") + 1]) if l.strip().startswith("/")]
    pct = float(a[a.index("--budget-pct") + 1]) if "--budget-pct" in a else 25.0   # Divit 2026-10-13: stop at 25% of the balance read
    start = json.load(open(os.path.join(BASE, "balance-start.json")))["balance_read"]; limit = start * pct / 100
    for u in urls:
        for p in phrases(u):
            if os.path.exists(raw_path(p)): continue
            if cap is not None and made >= cap: print(f"call cap {cap} reached"); return
            b0 = balance()
            if start - b0 >= limit: print(f"budget line reached: {start - b0} of {int(limit)} units ({pct}% of {start}); stop and ask Divit"); return
            q = urllib.parse.urlencode({"type": "phrase_questions", "key": _key(), "phrase": p, "database": DB, "display_limit": lim, "export_columns": "Ph,Nq"})
            txt = _get("https://api.semrush.com/?" + q)
            b1 = balance(); made += 1
            rows = []
            if not txt.startswith("ERROR"):
                for line in txt.strip().splitlines()[1:]:
                    parts = line.split(";")
                    if len(parts) >= 2: rows.append({"keyword": parts[0], "volume": int(parts[1] or 0)})
            os.makedirs(RAW, exist_ok=True)
            json.dump({"phrase": p, "database": DB, "display_limit": lim, "fetched": now(), "rows": rows, "api_note": txt[:60] if txt.startswith("ERROR") else ""}, open(raw_path(p), "w"), indent=1)
            with open(LEDGER, "a") as fh:
                fh.write(json.dumps({"t": now(), "url": u, "phrase": p, "database": DB, "display_limit": lim, "rows": len(rows), "units": b0 - b1, "balance_after": b1}) + "\n")
            print(f"{u.rsplit('/', 1)[1]}: {len(rows)} rows, {b0 - b1} units" + (" (" + txt[:40].strip() + ")" if txt.startswith("ERROR") else ""), flush=True)

HUB_PATH = {"LP": "/ai-landing-page-builder", "Form": "/ai-form-builder", "Auto": "/ai-automation-builder", "Automation": "/ai-automation-builder",
            "SurveyQuiz": "/ai-survey-and-quiz-builder", "Survey": "/ai-survey-and-quiz-builder"}
def _fetch_one(phrase, lim, label):
    import urllib.request, urllib.parse
    if os.path.exists(raw_path(phrase)): return 0
    start = json.load(open(os.path.join(BASE, "balance-start.json")))["balance_read"]; b0 = balance()
    if start - b0 >= start * 0.25: sys.exit(f"budget line reached ({start - b0} units); stop and ask Divit")
    q = urllib.parse.urlencode({"type": "phrase_questions", "key": _key(), "phrase": phrase, "database": DB, "display_limit": lim, "export_columns": "Ph,Nq"})
    txt = _get("https://api.semrush.com/?" + q); b1 = balance()
    rows = [] if txt.startswith("ERROR") else [{"keyword": l.split(";")[0], "volume": int(l.split(";")[1] or 0)} for l in txt.strip().splitlines()[1:] if ";" in l]
    os.makedirs(RAW, exist_ok=True)
    json.dump({"phrase": phrase, "database": DB, "display_limit": lim, "fetched": now(), "rows": rows}, open(raw_path(phrase), "w"), indent=1)
    with open(LEDGER, "a") as fh:
        fh.write(json.dumps({"t": now(), "url": label, "phrase": phrase, "database": DB, "display_limit": lim, "rows": len(rows), "units": b0 - b1, "balance_after": b1}) + "\n")
    return b0 - b1

def cmd_screen(a):
    """New-keyword screening (Divit 2026-10-13, ruling 13): FAQ supply first. For each candidate row (replacement sheets), Semrush
    questions for the primary and its top 2 secondaries (cached, budgeted), the same filter, plus distinct secondaries and the 2
    template slots. Only candidates projecting to 10 with 0 rejects (flags allowed) go to Divit's sheet."""
    import csv, synonyms as SY, park_rescue as R
    rows = []
    for r in csv.DictReader(open(os.path.join(ROOT, ".cache", "review", "replacements-2026-10-13.csv"))):
        rows.append((r["hub"], r["proposed_url"], r["primary"], r["top secondaries"], "passed screen", r))
    for r in csv.DictReader(open(os.path.join(ROOT, ".cache", "review", "replacements-2026-10-13-dropped.csv"))):
        if r["verdict"] == "unconfirmed":
            u = HUB_PATH.get(r["hub"], "/ai-form-builder") + "/" + re.sub(r"[^a-z0-9]+", "-", r["primary"].lower()).strip("-")
            rows.append((r["hub"], u, r["primary"], "", "unconfirmed (intent)", r))
    out = []; units = 0
    for hub, u, prim, secs_txt, status, raw in rows:
        secs = [x.strip().rsplit("(", 1)[0].strip() for x in (secs_txt or "").split(";") if x.strip()]
        phr = [prim] + secs[:2]
        for p_ in phr: units += _fetch_one(p_, 30, u)
        g = P.Gate(u); heads = [P.phrase_re(prim)]; have = []; usable_ = []; flags = 0
        for p_ in phr:
            for q in sorted(json.load(open(raw_path(p_)))["rows"], key=lambda x: -x["volume"]):
                nq = P.norm(q["keyword"])
                if not any(h.search(nq) for h in heads) or SY.drop_class(q["keyword"]): continue
                if any(re.search(r"(?<![a-z0-9])" + re.escape(b) + r"(?![a-z0-9])", nq) for b in _brands(u)): continue
                rs = g.judge({"q": q["keyword"], "source": "keyword", "n": 5})
                if any(x[1] == "reject" for x in rs) or R.dup(q["keyword"], have): continue
                have.append(q["keyword"]); flags += any(x[1] == "flag" for x in rs)
        sec_n = len({frozenset(P.content(x)) for x in secs if x and not R.dup(x, have)})
        proj = len(have) + sec_n + 2
        out.append({"hub": hub, "url": u, "primary": prim, "status": status, "semrush_usable": len(have), "flags": flags, "secondaries": sec_n,
                    "projected": proj, "reaches_10": proj >= 10, "msv": raw.get("msv", "")})
    p = os.path.join(ROOT, ".cache", "review", "replacements-screened-2026-10-13.csv")
    with open(p, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()) + ["divit"]); w.writeheader()
        for o in sorted(out, key=lambda o: (not o["reaches_10"], -(int(o["msv"] or 0)))): w.writerow(dict(o, divit=""))
    for o in out: print(f"{o['status']:22s} usable {o['semrush_usable']:2d} (flags {o['flags']}) secs {o['secondaries']} -> projected {o['projected']:2d}" + (" REACHES 10" if o["reaches_10"] else ""))
    print(f"units this screen: {units}; sheet {os.path.relpath(p, ROOT)} (only rows that reach 10 go to Divit)")

def cmd_plan(urls):
    todo = 0
    for u in urls:
        ps = phrases(u); st = ["cached" if os.path.exists(raw_path(p)) else "to call" for p in ps]; todo += st.count("to call")
        print(f"{u}: " + "; ".join(f"[{s}] {p}" for p, s in zip(ps, st)))
    print(f"calls needed: {todo}; calls made so far: {len(calls_made())}")

def cmd_save(a):
    phrase, f = a[0], a[1]; lim = int(a[a.index("--limit") + 1]) if "--limit" in a else 30
    if os.path.exists(raw_path(phrase)): sys.exit(f"refused: {phrase!r} ({DB}) is already cached; never repeat a call (Divit 2026-10-13)")
    data = json.load(open(f)); rows = data.get("rows") if isinstance(data, dict) else data
    rows = [{"keyword": r.get("keyword") or r.get("Keyword"), "volume": int(r.get("volume") or r.get("Search Volume") or 0)} for r in rows]
    os.makedirs(RAW, exist_ok=True)
    json.dump({"phrase": phrase, "database": DB, "display_limit": lim, "fetched": now(), "rows": rows}, open(raw_path(phrase), "w"), indent=1)
    with open(LEDGER, "a") as fh:
        fh.write(json.dumps({"t": now(), "phrase": phrase, "database": DB, "display_limit": lim, "rows": len(rows), "units_est": len(rows) * UNITS_PER_ROW}) + "\n")
    print(f"cached {len(rows)} rows for {phrase!r}; ledger: {len(calls_made())} call(s)")

def _brands(url):
    bl = json.load(open(os.path.join(ROOT, "rules", "paa_blocklist.json")))
    names = set(bl.get("tool_brands", [])) | set(bl.get("retail_brands", [])) | set(bl.get("pa14_brands", []))
    lib = os.path.join(ROOT, "rules", "competitors", H.CFG["hubs"][H.hub_of(url)]["repo_dir"] + ".json")
    if os.path.exists(lib): names |= set(json.load(open(lib)).get("competitors", {}))
    return {P.norm(n) for n in names if n and len(n) > 2}

def keep_reason(url, q, have=()):
    """Why a Semrush question is dropped (or None when it is usable): no_head | drop_class | brand | gate_reject | duplicate."""
    import synonyms as SY, park_rescue as R
    s = url.rsplit("/", 1)[1]; g = P.Gate(url); nq = P.norm(q)
    heads = [P.phrase_re(g.primary)] + [P.phrase_re(x) for x in (json.load(open(os.path.join(ROOT, "rules", "paa_synonyms.json")))["pages"].get(s) or []) if len(x.split()) >= 2]
    if not any(h.search(nq) for h in heads): return "no_head"
    if SY.drop_class(q): return "drop_class"
    if any(re.search(r"(?<![a-z0-9])" + re.escape(b) + r"(?![a-z0-9])", nq) for b in _brands(url)): return "brand"
    if any(x[1] == "reject" for x in g.judge({"q": q, "source": "keyword", "n": 5})): return "gate_reject"
    if R.dup(q, list(have)): return "duplicate"
    return None

def derive(url):
    import synonyms as SY, park_rescue as R
    s = url.rsplit("/", 1)[1]; g = P.Gate(url)
    heads = [P.phrase_re(g.primary)] + [P.phrase_re(x) for x in (json.load(open(os.path.join(ROOT, "rules", "paa_synonyms.json")))["pages"].get(s) or []) if len(x.split()) >= 2]
    brands = _brands(url)
    # existing candidates: FAQ items the gate does not reject, passing pull questions, the page's secondaries
    have = []   # never the page's own FAQ: a re-derive after assembly would drop its locked questions as duplicates (canary 2026-10-14)
    if P.pulls(s):
        items, _ = quiet(P.run_pull, g); have += [i["q"] for i in items if i["verdict"] != "reject"]
    have += [x["kw"] for x in (H.kmap().get(url) or {}).get("secondaries") or []]
    out, why = [], {"no_head": 0, "drop_class": 0, "brand": 0, "gate_reject": 0, "duplicate": 0}
    rows = []
    for p in phrases(url):
        if os.path.exists(raw_path(p)): rows += [dict(r, phrase=p) for r in json.load(open(raw_path(p)))["rows"]]
    for r in sorted(rows, key=lambda r: -r["volume"]):
        q = r["keyword"]; nq = P.norm(q)
        if not any(h.search(nq) for h in heads): why["no_head"] += 1; continue
        if SY.drop_class(q): why["drop_class"] += 1; continue
        if any(re.search(r"(?<![a-z0-9])" + re.escape(b) + r"(?![a-z0-9])", nq) for b in brands): why["brand"] += 1; continue
        rs = g.judge({"q": q, "source": "keyword", "n": 5})
        if any(x[1] == "reject" for x in rs): why["gate_reject"] += 1; continue
        noyear = lambda t: re.sub(r"\b(19|20)\d\d\b", " ", t)   # "...workflow 2025 2026" is the same question (A-r-8, 2026-10-14)
        if R.dup(noyear(q), [noyear(x) for x in have + [o["q"] for o in out]]): why["duplicate"] += 1; continue
        out.append({"q": q, "verdict": "flag" if any(x[1] == "flag" for x in rs) else "pass",
                    "prov": {"tool": "semrush-phrase_questions", "query": r["phrase"], "database": DB, "volume": r["volume"], "fetched": now()[:10]}})
    os.makedirs(DER, exist_ok=True)
    json.dump({"url": url, "derived": now(), "rows": len(rows), "usable": out, "dropped": why}, open(os.path.join(DER, s + ".json"), "w"), indent=1)
    return len(rows), out, why

def usable(slug):
    """Usable Semrush questions for a page (the feasibility count and QC F2 read this)."""
    p = os.path.join(DER, slug + ".json")
    return json.load(open(p))["usable"] if os.path.exists(p) else []

def cmd_derive(urls):
    for u in urls:
        n, out, why = derive(u)
        print(f"{u}: rows {n}, usable {len(out)} (flags {sum(o['verdict'] == 'flag' for o in out)}); dropped " + ", ".join(f"{k} {v}" for k, v in why.items() if v))

def cmd_report(urls):
    import park_rescue as R
    led = calls_made(); per = {}
    for c in led: per[c["phrase"]] = c
    tot = 0
    for u in urls:
        ps = phrases(u); units = sum(per[p].get("units", per[p].get("units_est", 0)) for p in ps if p in per); tot += units
        f = quiet(R.feasibility, u)
        print(f"{u}: calls {sum(p in per for p in ps)}, usable {len(usable(u.rsplit('/', 1)[1]))}, feasibility {f['total']}/10" + (" REACHES 10" if f["feasible"] else "") + f", units est {units}")
    print(f"calls total {len(led)}; units total {sum(c.get('units', c.get('units_est', 0)) for c in led)} (this set {tot})")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    {"plan": cmd_plan, "save": cmd_save, "derive": cmd_derive, "report": cmd_report, "balance": cmd_balance, "fetch": cmd_fetch, "screen": cmd_screen}[a[0]](a[1:])
