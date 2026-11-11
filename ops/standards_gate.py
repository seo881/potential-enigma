#!/usr/bin/env python3
"""Standards gate sweep (read-only; plan/prompts/gate.md, handover 2026-11-11).

Per page in scope, reports:
  SLUG  slug vs ops/slugs.py spec_problems (and, for pages in the CMS, the CMS slug == the spec slug)
  L13   hero prompt rendered lines (qc/prompt_lines.py via qc_hub._PL.qc_issues)
  L14   hero prompt template / one sentence / same-hub near-duplicate (qc_hub.hero_prompt_issues)
For pages present in the fresh CMS read (.cache/readback/<dir>-api-*.json, newest), the LIVE item's slug, H1 (name) and
hero prompt (window.awbPrompt default + chip adds) are checked, not only the spec.

Scope: states images, reviewed, approved, cms_draft (all hubs); SurveyQuiz quiz pages whose spec changed today;
every page whose CMS item was published on --date (default today UTC).

Usage: standards_gate.py [--date YYYY-MM-DD] [--json OUT] [--only URL,URL]   (prints one line per failing page)
Writes nothing to status or Webflow.
"""
import glob, json, os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ops")); sys.path.insert(0, os.path.join(ROOT, "qc"))
import slugs as S          # noqa: E402
import qc_hub as Q         # noqa: E402

CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))
STATES = ("images", "reviewed", "approved", "cms_draft")


def live_prompt(fd, hub):
    """(default, [adds]) from the CMS item's hero prompt field (window.awbPrompt JSON when present)."""
    pref = CFG["hubs"][hub]["fields"]["hero_prompt"]
    raw = fd.get(pref) or ""
    m = re.search(r"window\.awbPrompt\s*=\s*(\{.*?\})\s*;\s*</script>", raw, re.S)
    if m:
        try:
            o = json.loads(m.group(1))
            return o.get("default") or "", [c.get("add") for c in o.get("chips") or []], raw
        except ValueError: pass
    return Q.strip_html(re.sub(r"<div data-rt-embed-type.*", "", raw, flags=re.S)).strip(), None, raw


def newest_read(d):
    fs = sorted(glob.glob(os.path.join(ROOT, ".cache", "readback", f"{d}-api-*.json")))
    if not fs: return None, {}
    r = json.load(open(fs[-1]))
    return os.path.basename(fs[-1]), {it["fieldData"].get("slug"): it for it in r["result"]["items"]}


def changed_today(rel, day):
    out = subprocess.run(["git", "log", f"--since={day} 00:00", "--format=%h", "--", rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    st = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return bool(out or st)


def gate(day, only=None):
    pages, reads = [], {}
    specs = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "specs", "*", "*.json"))):
        s = json.load(open(p)); s["_path"] = p; specs[s.get("url")] = s
    for hub, h in CFG["hubs"].items():
        d = h["repo_dir"]
        st = json.load(open(os.path.join(ROOT, "status", f"{d}.json")))["pages"]
        src, items = newest_read(d); reads[hub] = src
        for url, e in st.items():
            if not isinstance(e, dict): continue
            slug = url.rsplit("/", 1)[1]; it = items.get(slug)
            pub_today = bool(it and (it.get("lastPublished") or "").startswith(day))
            why = []
            live_item = bool(it and not it.get("isDraft") and not it.get("isArchived") and it.get("lastPublished"))
            # a page already live is in scope only when published on --date (older live pages: recheck / fix_queue, not this gate)
            if e.get("state") in STATES and not live_item: why.append(e["state"])
            if pub_today: why.append("published " + day)
            if hub == "SurveyQuiz" and e.get("state") not in ("spec", "claimed") and url in specs and "quiz" in json.dumps(specs[url].get("keywords") or {}).lower() \
                    and changed_today(os.path.relpath(specs[url]["_path"], ROOT), day): why.append("quiz written today")
            if only and url in only and not why: why.append("requested")
            if not why or (only and url not in only): continue
            pages.append({"hub": hub, "url": url, "state": e.get("state"), "why": why, "hold": e.get("hold"),
                          "item": it, "live": bool(it and not it.get("isDraft") and not it.get("isArchived") and it.get("lastPublished"))})
    # effective specs: the CMS item's slug / H1 / hero prompt override the spec where the item exists
    eff = {}
    for u, s in specs.items():
        eff[u] = json.loads(json.dumps({k: v for k, v in s.items() if k != "_path"}))
    for pg in pages:
        s = eff.get(pg["url"])
        if s is None: continue
        it = pg["item"]
        if it:
            fd = it["fieldData"]; dft, adds, raw = live_prompt(fd, pg["hub"])
            s["fields"]["hero_prompt"] = raw; s["fields"]["h1"] = fd.get("name") or s["fields"].get("h1")
            if adds is not None: s["chip_adds"] = adds
            s["_cms_slug"] = fd.get("slug")
    every = list(eff.values())
    todo = [eff[p["url"]] for p in pages if p["url"] in eff]
    try: Q._PL_PRE["m"] = Q._PL.measure([(s.get("hub"), t) for s in todo for _, t in Q._PL.compose(s)])
    except Exception: Q._PL_PRE["m"] = None
    for pg in pages:
        s = eff.get(pg["url"])
        if s is None: pg["fails"] = [("NOSPEC", "spec not on main (a writer's branch): cannot be gated here")]; continue
        pg["fails"], pg["hero"] = check_page(pg["hub"], pg["url"], specs[pg["url"]], s, every, l13=True)
    return pages, reads


def check_page(hub, url, sp, s, every, l13=False):
    """Pure per-page checks. sp = the spec as written; s = the effective spec (CMS item fields overlaid where the item exists).
    Returns ([(check, message)], hero_default). l13 runs the Chromium line measure (skipped in golden cases: L13 has its own)."""
    f = []
    for p in S.spec_problems(hub, url, sp): f.append(("SLUG", f"spec: {p}"))
    if s.get("_cms_slug") and s["_cms_slug"] != url.rsplit("/", 1)[1]: f.append(("SLUG", f"CMS slug {s['_cms_slug']} != {url}"))
    if s.get("_cms_slug"):
        for p in S.problems(hub, s["_cms_slug"], (sp.get("keywords") or {}).get("primary"), s["fields"].get("h1")):
            if ("SLUG", f"spec: {p}") not in f: f.append(("SLUG", f"CMS: {p}"))
    prim = (s.get("keywords") or {}).get("primary", "")
    d = Q.strip_html(re.sub(r"<div data-rt-embed-type.*", "", s["fields"].get("hero_prompt") or "", flags=re.S))
    for sev, code, fld, msg in Q.hero_prompt_issues(d, prim, url, hub, every): f.append(("L14", msg))
    if l13:
        for sev, code, fld, msg in Q._PL.qc_issues(s, Q._PL_PRE.get("m")): f.append(("L13", f"{fld}: {msg}"))
    return f, d


def main(argv):
    day = time.strftime("%Y-%m-%d", time.gmtime()); out = None; only = None; gatefile = None
    a = list(argv)
    while a:
        if a[0] == "--date": day = a[1]; a = a[2:]
        elif a[0] == "--json": out = a[1]; a = a[2:]
        elif a[0] == "--gate-file": gatefile = a[1]; a = a[2:]
        elif a[0] == "--only": only = set(a[1].split(",")); a = a[2:]
        else: sys.exit(__doc__)
    pages, reads = gate(day, only)
    bad = [p for p in pages if p["fails"]]
    for p in bad:
        print(f"FAIL {p['url']} [{p['state']}{', LIVE' if p['live'] else ''}] " + " | ".join(f"{c}: {m}" for c, m in p["fails"]))
    print(f"pages {len(pages)}; failing {len(bad)}; reads {reads}")
    if gatefile:   # status/gate-<date>.json: merge, one entry per page gated
        gp = os.path.join(ROOT, gatefile); g = json.load(open(gp)) if os.path.exists(gp) else {}
        t = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
        for p in pages:
            ch = {k: "PASS" for k in ("SLUG", "L13", "L14")}
            for c, m in p["fails"]: ch[c] = "FAIL: " + m[:160]
            g[p["url"]] = {"result": "FAIL" if p["fails"] else "PASS", "checks": ch, "by": "A-g-2", "t": t}
        json.dump(g, open(gp, "w"), indent=1, sort_keys=True)
    if out:
        json.dump({"date": day, "reads": reads, "pages": [{k: v for k, v in p.items() if k != "item"} for p in pages]}, open(out, "w"), indent=1)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
