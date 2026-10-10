"""Golden cases (LESSONS.md rule 3): every question, sentence or claim a human or the live audit rejected, which the gates missed.
The gate must catch each one. Cases point at a commit and a spec instead of copying text (no SERP or AlsoAsked text in new files).

    .venv/bin/python3 tests/golden/run.py          run all; exit 1 if a "guarded" case is no longer caught (regression)

Case kinds (tests/golden/cases.jsonl, one JSON object per line):
  gate-question  {url, sha, q_index, expect: [rule ids]}   the PAA gate rejects FAQ item q_index of the spec at that commit
  gate-text      {url, q, expect}                          the gate rejects this literal question with one of the expected rules
  qc-field       {url, field, text, expect}                QC raises one of the expected codes when the field holds this text
  qc-text        {url, field, text, check}                 QC flags `field` when it holds `text` (P0/P1 on that field)
  qc-f1          {url, aa, serp, expect_f1}               QC raises F1 exactly when the page has no AlsoAsked pull (DataForSEO capture irrelevant)
  h3-noflag      {text}                                    the serial-comma detector must NOT call this text a certain miss (a trap)
  review         {url, field, check, text}                 judgment catch (Layer B); kept for the record, not machine-tested
status: "open" = a known miss the gate does not catch yet (a backlog fix); "guarded" = caught; a guarded case that stops being
caught fails the suite. Open cases that start passing are reported so they can be marked guarded.
"""
import json, os, re, subprocess, sys, copy
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for d in ("ops", "qc", "pipeline"): sys.path.insert(0, os.path.join(ROOT, d))
CASES = os.path.join(ROOT, "tests", "golden", "cases.jsonl")

def spec_at(sha, url):
    import hubctl as H
    rel = os.path.relpath(H.spath(url), ROOT)
    return json.loads(subprocess.run(["git", "show", f"{sha}:{rel}"], cwd=ROOT, capture_output=True, text=True, check=True).stdout)

def caught(c):
    if c["kind"] == "gate-question":
        import paa_gate as PG
        g = PG.Gate(c["url"]); g.spec = spec_at(c["sha"], c["url"])
        items, _ = PG.run_spec(g); it = items[c["q_index"] - 1]
        rej = {r[0] for r in it["reasons"] if r[1] == "reject"}
        return it["verdict"] == "reject" and (not c.get("expect") or bool(rej & set(c["expect"])))
    if c["kind"] == "gate-text":   # a literal question (Divit's examples, our own copy): the gate's per-question rules reject it
        import paa_gate as PG
        rs = PG.Gate(c["url"]).judge({"q": c["q"], "source": "secondary", "n": 5})
        return bool({r[0] for r in rs if r[1] == "reject"} & set(c.get("expect") or [r[0] for r in rs]))
    if c["kind"] == "qc-field":    # a literal field value: QC raises the expected code on that field
        import qc_hub as Q, hubctl as H, glob as _g
        s = copy.deepcopy(json.load(open(H.spath(c["url"])))); s["fields"][c["field"]] = c["text"]
        every = Q.load_specs(sorted(_g.glob(os.path.join(ROOT, "specs", "*", "*.json"))))
        return any(i["code"] in c["expect"] and i["sev"] in ("P0", "P1") for i in Q.check(s, every))
    if c["kind"] == "audit-noflag":   # the live audit must NOT raise this code on a page that lacks the thing (a settled non-issue)
        import live_audit as LA
        m = {"pages": [{"url": c["url"], "hub": "/" + c["url"].split("/")[1], "fields": {}, "faq_items": [], "images": {}, "meta_title": "x" * 40, "meta_description": "y" * 120}]}
        raw = {"pages": [{"url": c["url"], "checks": {"http200": True}, "verify": {}, "render": {"http": 200, "jsonld": ['{"@context": "https://schema.org", "@type": "Organization", "name": "Emergent"}'], "links": [], "images": [], "text_visible": "", "text_all": "", "h1s": ["h"]}}], "hubs": [], "held": []}
        return not any(f["code"] == c["code"] for f in LA.evaluate(raw, m, "https://emergent.sh"))
    if c["kind"] == "h3-noflag":   # a sentence that looks like a list but is not one (intro clause, nested pair, appositive)
        import serial_comma as SC
        return not SC.find(c["text"])[0]
    if c["kind"] == "qc-f1":       # F1 depends only on the AlsoAsked pull (DataForSEO retired, Divit 2026-10-10): aa/serp say which sources exist
        import qc_hub as Q, hubctl as H, paa_gate as PG, glob as _g
        sys.path.insert(0, os.path.join(ROOT, "plan")); import serp as S
        s = json.load(open(H.spath(c["url"]))); s["status"] = "qc_pass"
        real_pp, real_load = PG.pull_path, S.load
        stub = os.path.join(ROOT, ".cache", "golden-aa-stub.json"); os.makedirs(os.path.dirname(stub), exist_ok=True)
        json.dump({"_meta": {"fetched": "2026-10-10"}, "response": {}}, open(stub, "w"))
        PG.pull_path = lambda slug: stub if c["aa"] else os.path.join(ROOT, ".cache", "golden-no-such-pull.json")
        S.load = lambda url: (real_load(url) or {"paa": [], "related": [], "organic": [], "features": [], "fetched": "2026-10-01"}) if c["serp"] else None
        try: hit = any(i["code"] == "F1" for i in Q.check(s, Q.load_specs([H.spath(c["url"])])))
        finally: PG.pull_path, S.load = real_pp, real_load
        return hit == c["expect_f1"]
    if c["kind"] == "qc-text":
        import qc_hub as Q, hubctl as H
        s = json.load(open(H.spath(c["url"]))); s = copy.deepcopy(s); f = c["field"]
        if f in s["fields"]: s["fields"][f] = c["text"]
        every = [x for x in Q.load_specs([H.spath(c["url"])])]
        return any(i["sev"] in ("P0", "P1") and (i["field"] or "").startswith(f) for i in Q.check(s, every))
    return None

def main():
    cases = [json.loads(l) for l in open(CASES) if l.strip()] if os.path.exists(CASES) else []
    reg, newly, open_, skipped = [], [], [], 0
    for c in cases:
        r = caught(c)
        if r is None: skipped += 1; continue
        if c["status"] == "guarded" and not r: reg.append(c["id"])
        elif c["status"] == "open" and r: newly.append(c["id"])
        elif c["status"] == "open": open_.append(c["id"])
    print(f"golden: {len(cases)} cases; regressions {len(reg)}; open misses {len(open_)}; open now caught {len(newly)}; not machine-tested {skipped}")
    for x in reg: print("  REGRESSION", x)
    for x in newly: print("  NOW CAUGHT (mark guarded)", x)
    for x in open_: print("  open", x)
    sys.exit(1 if reg else 0)

if __name__ == "__main__":
    main()
