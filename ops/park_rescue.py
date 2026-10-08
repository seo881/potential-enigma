"""park_rescue.py: rescue analysis for parked pages (PA11: under 8 on-topic FAQ sources). No API calls, no credits, no writes
outside .cache/review/. Counts only: no question or keyword text is printed (private/ data stays private).

    .venv/bin/python3 ops/park_rescue.py [URL ...]      default: the park group of plan/rework-2026-10-08.md

Per page, the sources a writer may use today (PA11), each counted once (same intent = paa_gate.JACCARD_DUP):
  faq   current FAQ items that pass the gate (strict: head phrase, PA3 widened)
  pull  gate-passing questions in the page's AlsoAsked pull that are not already in the FAQ
  sec   the page's secondaries (keyword map) that no FAQ question carries yet
Levers:
  (a) SAFE synonym candidates (rules/paa_synonym_candidates.json) if Divit approves them: extra FAQ items and pull questions they admit
  (b) question-form keyword ideas for the page in the Semrush workbook that are not already a secondary or an FAQ question
  (c) a second AlsoAsked pull on the page's top unused secondary: ESTIMATE only = mean gate-passing questions per first pull in
      the page's hub (1 credit per page; no pull is made); gap_after_c = what would still be missing
Class, in order: rescued by (a) / rescued by (b) / intent mismatch (evidence: 30%+ of the page's own pull is wrong-sense or non-US,
PA4/PA5: searchers mean something else; drop or merge) / needs (c) (the pull is on-sense but thin: almost every reject is PA3).
"""
import csv, json, os, re, statistics, sys
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "qc")); sys.path.insert(0, os.path.join(ROOT, "ops"))
import paa_gate as P, guards as G

QWORD = re.compile(r"^(how|what|why|when|where|who|which|can|do|does|is|are|should|will|could|would)\b", re.I)
WB = os.path.join(ROOT, "private", "Emergent_Hub_Child_Pages_Final_v3.xlsx")

def parked_from_plan():
    parts = re.split(r"^## ", open(os.path.join(ROOT, "plan", "rework-2026-10-08.md")).read(), flags=re.M)
    sec = next((s for s in parts if s.startswith("park")), "")
    return re.findall(r"^- (\S+) \(", sec, re.M)

def workbook_questions():
    if not os.path.exists(WB): return {}
    import pandas as pd
    kr = pd.read_excel(WB, "Keyword report (pass 3)", header=3); out = {}
    for _, r in kr.iterrows():
        k = str(r["Keyword"])
        if QWORD.match(k):
            u = str(r["Page URL"]).replace("/ai-survey-quiz-builder/", "/ai-survey-and-quiz-builder/")
            out.setdefault(u, []).append(k)
    return out

def dup(q, pool): return any(P.jacc(P.content(q), P.content(x)) >= P.JACCARD_DUP for x in pool)

def sources(url, extra=()):
    g = P.Gate(url, extra)
    faq, _ = P.run_spec(g); fq = [i["q"] for i in faq]
    on = [i["q"] for i in faq if i["verdict"] != "reject"]
    pull = []
    ws = n = 0
    if os.path.exists(P.pull_path(g.slug)):
        items, _ = P.run_pull(g); pull = [i["q"] for i in items if i["verdict"] == "pass" and not dup(i["q"], fq)]
        n = len(items); ws = sum(any(r[0] in ("PA4", "PA5") and r[1] == "reject" for r in i["reasons"]) for i in items)
    return g, fq, on, pull, (ws / n if n else 0.0), n

def main(urls):
    km = json.load(open(os.path.join(ROOT, "plan", "keyword_map.json")))
    cand = json.load(open(os.path.join(ROOT, "rules", "paa_synonym_candidates.json")))["pages"]
    wq = workbook_questions()
    paa = {r["url"]: r for r in csv.DictReader(open(os.path.join(ROOT, ".cache", "review", "paa.csv")))}
    med = {h: round(statistics.mean(int(r["pull_pass"]) for r in paa.values() if r["hub"] == h), 1) for h in {r["hub"] for r in paa.values()}}
    specs = {s["url"]: s for s in G.all_specs()}
    rows = []
    for url in urls:
        g, fq, on, pull, wrong, npull = sources(url)
        secs = sorted((km.get(url) or {}).get("secondaries", []), key=lambda x: -x.get("msv", 0))
        unused = [x["kw"] for x in secs if P.content(x["kw"]) and not any(P.content(x["kw"]) <= P.content(q) for q in fq)]
        base = len(on) + len(pull) + len(unused)
        safe = [c["phrase"] for c in cand.get(g.slug, []) if c.get("status") == "safe"]
        a_add = 0
        if safe:
            _, _, on_c, pull_c, _w, _n = sources(url, safe)
            a_add = max(0, len(on_c) - len(on)) + len([q for q in pull_c if not dup(q, pull)])
        seck = {k.lower() for k in [x["kw"] for x in secs]}
        b_ideas = [k for k in wq.get(url, []) if k.lower() not in seck and not dup(k, fq + pull)]
        b_add = len([k for k in b_ideas if any(h.search(P.norm(k)) for h in g.heads) or g.pa3_widened(P.norm(k))])
        c_est = med.get(g.hub, 0)
        need = P.MIN_ON_TOPIC - base
        if base + a_add >= P.MIN_ON_TOPIC: cls = "rescued by (a)"
        elif base + b_add >= P.MIN_ON_TOPIC: cls = "rescued by (b)"
        elif base + a_add + b_add >= P.MIN_ON_TOPIC: cls = "rescued by (a)+(b)"
        elif wrong >= 0.30: cls = "intent mismatch"
        else: cls = "needs (c)"
        r = paa.get(url, {})
        rej = Counter({k: int(v) for k, v in (x.split(":") for x in (r.get("rejects_by_rule_strict") or "").split() if ":" in x)})
        cause = ""; merge = ""
        if cls == "intent mismatch":
            top = ["PA4"] + [k for k, _ in rej.most_common(2) if k != "PA4"][:1]
            cause = f"{wrong:.0%} of the AlsoAsked pull is wrong-sense or non-US: " + {"PA3": "searchers' questions are about another subject (head phrase absent)", "PA4": "wrong sense of the head phrase",
                     "PA5": "non-US audience", "PA7": "advice-seeking (legal/medical/tax)", "PA1": "unsourced or non-PAA items",
                     "PA9": "duplicates", "PA12": "answer-first or structure"}.get(top[0] if top else "", "too few searched questions") + \
                    f" ({npull} distinct questions in the pull, {len(pull)} usable)"
            pw = set(P.norm((specs.get(url, {}).get("keywords") or {}).get("primary", "")).split())
            best = None
            for u2, s2 in specs.items():
                if u2 == url or not u2.startswith(g.hub_path + "/") or s2.get("status") == "spec": continue
                w2 = set(P.norm((s2.get("keywords") or {}).get("primary", "")).split())
                if w2 and w2 < pw and (best is None or len(w2) > len(best[1])): best = (u2, w2)
            merge = best[0] if best else ""
        risk = r.get("risk_tags", "")
        rows.append({"url": url, "hub": g.hub, "faq_on_topic": len(on), "pull_new": len(pull), "secondaries_unused": len(unused), "base": base,
                     "short_by": max(0, need), "a_safe_synonyms": len(safe), "a_adds": a_add, "b_adds": b_add, "b_ideas_on_page": len(wq.get(url, [])),
                     "c_estimate": c_est, "gap_after_c": max(0, round(P.MIN_ON_TOPIC - base - a_add - b_add - c_est, 1)),
                     "wrong_sense_share": round(wrong, 2), "class": cls, "cause": cause, "merge_target": merge, "risk_tags": risk})
        print(f"{url}: base {base} (faq {len(on)}, pull {len(pull)}, sec {len(unused)}); a +{a_add}, b +{b_add}, c ~{c_est} -> {cls}", flush=True)
    os.makedirs(os.path.join(ROOT, ".cache", "review"), exist_ok=True)
    out = os.path.join(ROOT, ".cache", "review", "park-rescue.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(Counter(r["class"] for r in rows), "->", out)
    return rows

if __name__ == "__main__":
    main(sys.argv[1:] or parked_from_plan())
