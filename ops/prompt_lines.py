"""prompt_lines.py: rendered line counts of the hero prompt box (rule L13, Divit 2026-10-15).

Divit's rule: at 1440 px the DEFAULT prompt (no chip selected) renders in at most 2 lines in the prompt box, and each CHIP prompt
(the default plus that chip's "add" clause, composed exactly as the template's hero-chips script does it) in at most 3 lines.
Character counts are not enough, so the text is rendered in headless Chromium (ops/prompt_lines.mjs) into a <textarea> with the
live box's computed style (width, font, size, weight, letter-spacing, padding, line-height, wrapping), cached per hub in
rules/prompt_box.json with the font files in rules/fonts/, so QC needs no network. 390 px is measured and reported, not judged.

    .venv/bin/python3 ops/prompt_lines.py profile [URL ...]       re-read the live box style (one page per hub) -> rules/prompt_box.json
    .venv/bin/python3 ops/prompt_lines.py validate URL ...        live line counts (real page, real chip clicks) vs the local measurer
    .venv/bin/python3 ops/prompt_lines.py sweep [--states a,b] [--out FILE]   every spec in those states: page | state | prompt | lines
    .venv/bin/python3 ops/prompt_lines.py text HUB "prompt text"  lines of one text at 1440 and 390

Composition (ops/template/hero-chips.html, live since 2026-10-09): default = the hero_prompt field's text (tags stripped,
entities unescaped, trimmed: hubctl.prompt_embed); chip i = default (trailing space trimmed) + " " + chip_adds[i]. One chip at a
time is what the rule judges (several chips at once are the visitor's choice). Specs with only the legacy chip_prompts (no
chip_adds) get the default measured; their chips are not composed by the live script.
Results are cached in .cache/prompt_lines.json, keyed by the profile, the width and the text.
"""
import hashlib, html, json, os, re, subprocess, sys, tempfile, glob, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE = os.path.join(ROOT, "rules", "prompt_box.json")
CACHE = os.path.join(ROOT, ".cache", "prompt_lines.json")
MJS = os.path.join(ROOT, "ops", "prompt_lines.mjs")
CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))
LIMITS = {"default": 2, "chip": 3}     # Divit 2026-10-15, at 1440 px
JUDGED_WIDTH = "1440"
WIDTHS = ("1440", "390")
DEFAULT_PAGES = {"LP": "/ai-landing-page-builder/app-landing-page", "Form": "/ai-form-builder/ach-form",
                 "Auto": "/ai-automation-builder/accounting-automation", "SurveyQuiz": "/ai-survey-and-quiz-builder/culture-survey"}

class MeasureError(RuntimeError): pass

def hub_of(url):
    for k, h in CFG["hubs"].items():
        if url.startswith(h["path"] + "/"): return k
    return None

def default_text(v):
    v = re.sub(r"<div data-rt-embed-type.*", "", v or "", flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", v)).strip()

def compose(spec):
    """[(key, text)]: the default and, with chip_adds, one prompt per chip as the live script builds it."""
    d = default_text((spec.get("fields") or {}).get("hero_prompt", ""))
    if not d: return []
    out = [("default", d)]
    for i, a in enumerate(spec.get("chip_adds") or [], 1):
        if isinstance(a, str) and a.strip(): out.append((f"chip {i}", re.sub(r"\s+$", "", d) + " " + a))
    return out

def _node(mode, job):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f: json.dump(job, f); jp = f.name
    try:
        r = subprocess.run(["node", MJS, mode, jp], cwd=os.path.join(ROOT, "ops"), capture_output=True, text=True, timeout=600)
    except (OSError, subprocess.TimeoutExpired) as e: raise MeasureError(f"node/Playwright unavailable: {e}")
    finally: os.unlink(jp)
    if r.returncode: raise MeasureError((r.stderr or r.stdout).strip()[-400:])
    return json.loads(r.stdout)

def profile():
    if not os.path.exists(PROFILE): raise MeasureError("rules/prompt_box.json missing: run ops/prompt_lines.py profile")
    return json.load(open(PROFILE))

def _key(prof_hash, style, text):
    return hashlib.sha1(json.dumps([prof_hash, style, text], sort_keys=True).encode()).hexdigest()

def measure(pairs):
    """pairs: [(hub, text)] -> {(hub, text): {"1440": n, "390": n}}; one Chromium launch for every cache miss."""
    P = profile(); ph = hashlib.sha1(json.dumps(P, sort_keys=True).encode()).hexdigest()[:12]
    try: cache = json.load(open(CACHE))
    except Exception: cache = {}
    items, out = [], {}
    for hub, text in pairs:
        hp = P["hubs"].get(hub)
        if not hp: raise MeasureError(f"no prompt box profile for hub {hub!r} in rules/prompt_box.json")
        res = {}
        for w in WIDTHS:
            st = hp["viewports"][w]["style"]; k = _key(ph, st, text)
            if k in cache: res[w] = cache[k]
            else: items.append({"id": k, "style": st, "text": text})
        out[(hub, text)] = res
    if items:
        uniq = list({i["id"]: i for i in items}.values())
        r = _node("local", {"fonts": P["fonts"], "items": uniq})
        if r.get("missing_fonts"): raise MeasureError(f"fonts not loaded locally: {r['missing_fonts']}")
        for k, v in r["lines"].items(): cache[k] = v["lines"]
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        tmp = CACHE + f".{os.getpid()}"; json.dump(cache, open(tmp, "w")); os.replace(tmp, CACHE)
        for hub, text in pairs:
            hp = P["hubs"][hub]
            for w in WIDTHS: out[(hub, text)][w] = cache[_key(ph, hp["viewports"][w]["style"], text)]
    return out

def spec_lines(spec, pre=None):
    """[{key, text, "1440": n, "390": n, limit, ok}] for one spec (pre: a measure() result to reuse)."""
    hub = spec.get("hub") or hub_of(spec.get("url", ""))
    comp = compose(spec)
    m = pre if pre is not None and all((hub, t) in pre for _, t in comp) else measure([(hub, t) for _, t in comp])
    rows = []
    for k, t in comp:
        lim = LIMITS["default" if k == "default" else "chip"]; n = m[(hub, t)]
        rows.append({"key": k, "text": t, "1440": n["1440"], "390": n["390"], "limit": lim, "ok": n[JUDGED_WIDTH] <= lim})
    return rows

def qc_issues(spec, pre=None):
    """L13 for qc_hub.check: P1 per prompt over its line limit at 1440 px; P1 when the measurer cannot run (fail closed)."""
    if not compose(spec): return []
    try: rows = spec_lines(spec, pre)
    except MeasureError as e: return [("P1", "L13", "hero_prompt", f"prompt line measurer did not run ({e}); the rule needs a rendered count, not characters")]
    I = []
    for r in rows:
        if r["ok"]: continue
        if r["key"] == "default":
            I.append(("P1", "L13", "hero_prompt", f"default prompt renders in {r['1440']} lines in the 1440 px prompt box (max 2; {r['390']} at 390 px): shorten it"))
        else:
            I.append(("P1", "L13", "chip_adds", f"{r['key']} prompt (default + its add clause) renders in {r['1440']} lines at 1440 px (max 3; {r['390']} at 390 px): shorten the clause or the default"))
    return I

# ---------------------------------------------------------------- CLI
def cmd_profile(urls):
    urls = urls or ["https://emergent.sh" + u for u in DEFAULT_PAGES.values()]
    live = _node("live", {"urls": urls, "widths": [int(w) for w in WIDTHS]})
    old = json.load(open(PROFILE)) if os.path.exists(PROFILE) else {}
    P = {"_note": "Hero prompt box (#hero-prompt-form textarea) computed style per hub and viewport, read from the live site by "
                  "ops/prompt_lines.py profile; ops/prompt_lines.mjs renders texts locally with it for rule L13 (Divit 2026-10-15). "
                  "Fonts: Inter v20 (SIL Open Font License) from fonts.gstatic.com, the files the live page loads, cached in rules/fonts/.",
         "fonts": old.get("fonts") or [
             {"family": "Inter", "file": "rules/fonts/inter-v20-latin.woff2", "source": "https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7W0Q5nw.woff2",
              "unicode_range": "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"},
             {"family": "Inter", "file": "rules/fonts/inter-v20-latin-ext.woff2", "source": "https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa25L7W0Q5n-wU.woff2",
              "unicode_range": "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF"}],
         "hubs": {}}
    for r in live:
        if r.get("error"): sys.exit(f"{r['url']} @{r['width']}: {r['error']}")
        hub = hub_of(r["url"].replace("https://emergent.sh", "").replace("https://emergent-sh.webflow.io", ""))
        h = P["hubs"].setdefault(hub, {"source_url": r["url"], "measured_at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), "viewports": {}})
        h["viewports"][str(r["width"])] = {"style": r["style"], "fonts_loaded": sorted({f"{a} {b}" for a, b, _ in r["fonts_loaded"]})}
    json.dump(P, open(PROFILE, "w"), indent=1, ensure_ascii=False); open(PROFILE, "a").write("\n")
    for hub, h in P["hubs"].items():
        print(hub, {w: (v["style"]["width"], v["style"]["font-family"], v["style"]["font-size"], v["style"]["font-weight"], v["style"]["line-height"]) for w, v in h["viewports"].items()})

def cmd_validate(urls):
    """Live (the real page, its own chip script) vs local (spec composition + cached style): every line count must match."""
    sys.path.insert(0, os.path.join(ROOT, "ops")); import hubctl as H
    full = [u if u.startswith("http") else "https://emergent.sh" + u for u in urls]
    # every prompt in the repo (all specs, default and chips) is also typed into each live box: the local count must match it too
    corpus = sorted({t for p in glob.glob(os.path.join(ROOT, "specs", "*", "*.json")) for _, t in compose(json.load(open(p)))})
    live = _node("live", {"urls": full, "widths": [int(w) for w in WIDTHS], "texts": corpus})
    bad = 0; rows = []; xbad = xn = 0
    by = {}
    for r in live:
        if r.get("error"): print("ERROR", r["url"], r["width"], r["error"]); bad += 1; continue
        by.setdefault(r["url"], {})[str(r["width"])] = r
        hub = hub_of(re.sub(r"^https://[^/]+", "", r["url"])); m = measure([(hub, t) for t in corpus])
        for t, L in zip(corpus, r.get("extra") or []):
            xn += 1
            if m[(hub, t)][str(r["width"])] != L: xbad += 1; print("CORPUS MISMATCH", r["url"], r["width"], L, m[(hub, t)], t[:80])
    for u, ws in by.items():
        path = re.sub(r"^https://[^/]+", "", u); hub = hub_of(path)
        spec = json.load(open(H.spath(path)))
        comp = dict(compose(spec))
        live_texts = {t["key"]: t for t in ws["1440"]["texts"]}
        m_spec = measure([(hub, t) for t in comp.values()])
        m_live = measure([(hub, t["text"]) for t in live_texts.values()])
        for k, lt in live_texts.items():
            for w in WIDTHS:
                L = {t["key"]: t for t in ws[w]["texts"]}[k]["lines"]
                loc = m_live[(hub, lt["text"])][w]
                sp = m_spec[(hub, comp[k])][w] if k in comp else None
                same_text = comp.get(k) == lt["text"]
                ok = L == loc and (sp is None or not same_text or sp == L)
                bad += not ok
                rows.append((path, k, w, L, loc, sp, same_text, ok))
    print("| page | prompt | width | live lines | local (live text) | local (spec text) | spec text = live text | match |")
    print("|---|---|---|---|---|---|---|---|")
    for r in rows: print("| " + " | ".join(str(x) for x in r) + " |")
    print(f"\n{len(rows)} page measurements, {bad} mismatches; corpus: {xn} texts typed into the live boxes, {xbad} mismatches")
    return 1 if bad or xbad else 0

def status_states():
    st = {}
    for h in CFG["hubs"].values():
        p = os.path.join(ROOT, "status", f"{h['repo_dir']}.json")
        if os.path.exists(p):
            for u, v in (json.load(open(p)).get("pages") or {}).items(): st[u] = v.get("state")
    return st

def cmd_sweep(states, out):
    st = status_states()
    specs = []
    for p in sorted(glob.glob(os.path.join(ROOT, "specs", "*", "*.json"))):
        s = json.load(open(p)); state = st.get(s.get("url"))
        if state in states: specs.append((s, state))
    pairs = [(s.get("hub") or hub_of(s["url"]), t) for s, _ in specs for _, t in compose(s)]
    pre = measure(pairs)
    rows = []
    for s, state in specs:
        for r in spec_lines(s, pre): rows.append((s["url"], state, r))
    off = [x for x in rows if not x[2]["ok"]]
    live_states = {"published"}
    def n_pages(xs, live): return len({u for u, stt, _ in xs if (stt in live_states) == live})
    L = [f"# Hero prompt lines (rule L13, Divit 2026-10-15): default <= 2 lines, each chip prompt <= 3 lines, at 1440 px",
         "", f"Measured {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())} with ops/prompt_lines.py (headless Chromium, live box style in rules/prompt_box.json: "
         "722 px wide at 1440, 240 px at 390; Inter 500 16px, line-height 22.86px, no padding). 390 px is reported, not judged.",
         "", f"States: {', '.join(states)}. Pages: {len(specs)}; prompts: {len(rows)}; offenders: {len(off)} prompts on {len({u for u, _, _ in off})} pages "
         f"(live {n_pages(off, True)} pages, pipeline {n_pages(off, False)} pages).", "",
         "Distribution at 1440: " + ", ".join(f"{k} " + "/".join(f"{n}L x{sum(1 for _, _, r in rows if (r['key'] == 'default') == (k == 'default') and r['1440'] == n)}" for n in sorted({r['1440'] for _, _, r in rows if (r['key'] == 'default') == (k == 'default')})) for k in ("default", "chip")),
         "", "| page | state | prompt | lines at 1440 | lines at 390 | limit | text |", "|---|---|---|---|---|---|---|"]
    rows.sort(key=lambda x: (x[2]["ok"], -(x[2]["1440"] - x[2]["limit"]), -x[2]["390"], x[0], x[2]["key"]))
    for u, state, r in rows:
        L.append(f"| {u} | {state} | {r['key']} | {r['1440']}{' **OVER**' if not r['ok'] else ''} | {r['390']} | {r['limit']} | {r['text'].replace('|', '/')} |")
    open(out, "w").write("\n".join(L) + "\n")
    print("\n".join(L[:8])); print(f"-> {out}")

def main(argv):
    if not argv: print(__doc__); return 0
    if argv[0] == "profile": cmd_profile(argv[1:]); return 0
    if argv[0] == "validate": return cmd_validate(argv[1:])
    if argv[0] == "text":
        r = measure([(argv[1], argv[2])])[(argv[1], argv[2])]; print(json.dumps(r)); return 0
    if argv[0] == "sweep":
        states = ["published", "approved", "reviewed", "images", "qc_pass", "spec"]; out = os.path.join(ROOT, ".cache", "prompt_lines_sweep.md")
        a = argv[1:]
        while a:
            if a[0] == "--states": states = a[1].split(","); a = a[2:]
            elif a[0] == "--out": out = a[1]; a = a[2:]
            else: sys.exit(f"unknown argument {a[0]}")
        cmd_sweep(states, out); return 0
    print(__doc__); return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
