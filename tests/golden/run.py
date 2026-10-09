"""Golden cases (LESSONS.md rule 3): every question, sentence or claim a human or the live audit rejected, which the gates missed.
The gate must catch each one. Cases point at a commit and a spec instead of copying text (no SERP or AlsoAsked text in new files).

    .venv/bin/python3 tests/golden/run.py          run all; exit 1 if a "guarded" case is no longer caught (regression)

Case kinds (tests/golden/cases.jsonl, one JSON object per line):
  gate-question  {url, sha, q_index, expect: [rule ids]}   the PAA gate rejects FAQ item q_index of the spec at that commit
  qc-text        {url, field, text, check}                 QC flags `field` when it holds `text` (P0/P1 on that field)
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
