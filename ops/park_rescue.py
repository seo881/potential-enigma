"""park_rescue.py: rescue analysis for parked pages (PA11: under 8 on-topic FAQ sources). No API calls, no credits, no writes
outside .cache/review/. Counts only: no question or keyword text is printed (private/ data stays private).

    .venv/bin/python3 ops/park_rescue.py [URL ...]      default: the park group of plan/rework-2026-10-08.md
    .venv/bin/python3 ops/park_rescue.py --a6 URL ...   A6 count (2026-10-12): approved synonyms only, both pulls; see a6_count

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

def dup(q, pool, head=None):
    """Same intent (PA9): plain Jaccard on content words, or a same-intent variant (ruling 18 part 4a, paa_gate.near_dup)."""
    return any(P.jacc(P.content(q), P.content(x)) >= P.JACCARD_DUP or P.near_dup(q, x, head) for x in pool)

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

KW_RULES = ("PA4", "PA5", "PA8", "PA14", "PA15", "PA16", "PA17")   # rules that reject a question for words the keyword itself carries (PA16/PA17: ruling 18)

def a6_count(url, extra=()):
    """A6 (Divit 2026-10-12): on-topic FAQ sources for a page, counting APPROVED synonyms only (rules/paa_synonyms.json; never the
    --cand candidates), each counted once (same intent = PA9):
      faq   current FAQ items the gate does not reject (PA11's own count)
      pull  gate-passing AlsoAsked questions from the primary and top-secondary pulls, not same-intent as a counted FAQ item
      sec   keyword-map secondaries no counted question carries yet, one per content-word set, and not rejected for their own
            words (PA4, PA5, PA8, PA14, PA15: e.g. a file-format ask)
    extra: unapproved candidate phrases, only for ruling 12's 'feasibility with the top 2 candidates' column (never for claim).
    Returns a dict of counts only."""
    g = P.Gate(url, extra)
    faq, _ = P.run_spec(g) if (g.spec.get("fields") or {}).get("faq") else ([], None)   # a parked page may have no FAQ yet
    on = [i["q"] for i in faq if i["verdict"] != "reject"]
    pull = []
    if P.pulls(g.slug):
        items, _ = P.run_pull(g); pull = [i["q"] for i in items if i["verdict"] == "pass" and not dup(i["q"], on)]
    km = json.load(open(os.path.join(ROOT, "plan", "keyword_map.json"))).get(url) or {}
    carried = [P.content(q) for q in on + pull]; seen, sec = [], 0
    for x in sorted(km.get("secondaries") or [], key=lambda x: -(x.get("msv") or 0)):
        c = P.content(x.get("kw") or "")
        if not c or c in seen or any(c <= q for q in carried): continue
        seen.append(c)
        if any(r[0] in KW_RULES and r[1] == "reject" for r in g.judge({"q": x["kw"], "source": "secondary"})): continue
        sec += 1
    # Semrush phrase_questions (Divit 2026-10-13): usable questions from ops/semrush_questions.py derive, deduped against what is counted
    import semrush_questions as SQ
    sq = 0; counted = on + pull
    for x in SQ.usable(g.slug):
        if dup(x["q"], counted): continue
        counted.append(x["q"]); sq += 1
    return {"faq": len(on), "pull": len(pull), "sec": sec, "sq": sq, "total": len(on) + len(pull) + sec + sq, "pulls": len(P.pulls(g.slug)), "spec_faq": bool(faq), "_qs": counted}

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
    if sys.argv[1:2] == ["--a6"]:   # A6 count per page (counts only): faq + pull + sec = total
        for u in sys.argv[2:]: print(u, json.dumps(a6_count(u)), flush=True)
    else: main(sys.argv[1:] or parked_from_plan())

def feasibility(url, extra=(), draft=True):
    """Ruling 10 B1 (Divit 2026-10-13), ruling 18 part 5 (2026-10-14): can this page reach 10 FAQ items with 0 rejects? Since ruling 18
    it is the skeleton's own count (ops/skeleton.py plan_slots, no cap): every slot the skeleton would fill from the AlsoAsked pull,
    the Semrush questions, the uncarried secondaries and the 2 template slots, flagged questions included except the shapes the gate
    now drops (fragment, self-quiz, navigational, state- or platform-specific) and PA14 capitalised names, each same-intent
    question once (near_dup). The overnight run of 2026-10-14 found lead-nurturing-workflow at feasibility 10 but skeleton 7/10:
    the old count skipped the skeleton's filler-aware duplicate test. Under 10: no writer; the page waits at the end of the queue.
    A page that already has a FAQ draft keeps the ruling 10 count (_feasibility_draft). Returns counts only: pull (AlsoAsked slots), sq (Semrush), sec (secondary slots), slots (template), flagged, total."""
    spp = os.path.join(ROOT, "specs", P.hub_of(url)[1]["repo_dir"], url.rsplit("/", 1)[1] + ".json")
    sp = json.load(open(spp)) if os.path.exists(spp) else {}
    if draft and (sp.get("fields") or {}).get("faq"): return _feasibility_draft(url, extra)   # an existing draft keeps its own FAQ count
    import skeleton as SK
    plan = SK.plan_slots(url, None, extra)
    k = Counter(sl.get("kind") for sl in plan); total = len(plan)
    return {"faq": 0, "pull": k["alsoasked"], "sec": k["secondary"], "sq": k["semrush"], "recoverable": 0, "slots": k["definition"],
            "flagged": sum(1 for sl in plan if sl.get("flagged")), "total": total, "feasible": total >= P.N_FAQ,
            "pulls": len(P.pulls(url.rsplit("/", 1)[1])), "spec_faq": False}

def _feasibility_draft(url, extra=()):
    """A page that already has a FAQ draft (rework, --adopt): its count before ruling 18 (ruling 10 B1). Ruling 10 B1 (Divit 2026-10-13): can this page reach 10 FAQ items with 0 rejects after its one pull? Counts a6_count
    (gate-passing FAQ items, pull items, uncarried secondaries) plus RECOVERABLE items: FAQ items the gate rejects only for
    PA3 whose source is a keyword or secondary that itself contains the head phrase (backlog line 91: the writer can put the
    head term back). A page with no FAQ yet also gets its 2 template slots (definition, how-to-build). Pass and flag both
    count (flags are allowed when listed in Divit's packet, ruling 4). Under 10: no writer; the page waits at the end of the queue."""
    c = a6_count(url, extra); g = P.Gate(url, extra); rec = 0
    if c["spec_faq"]:
        srcs = {x.get("q"): x for x in g.spec.get("faq_sources") or []}
        faq, _ = P.run_spec(g)
        for i in faq:
            if i["verdict"] != "reject": continue
            rules = {r[0] for r in i["reasons"] if r[1] == "reject"}
            src = srcs.get(i["q"]) or {}
            if rules == {"PA3"} and src.get("source") in ("keyword", "secondary") and any(h.search(P.norm(src.get("ref") or "")) for h in g.heads):
                rec += 1
    # template slots (definition, how-to-build) only where no counted question already is one (skeleton.py fills them the same way;
    # 2026-10-13: the old +2 double-counted pages whose pull already holds the definition or the how-to question)
    slots = 0
    if not c["spec_faq"]:
        import re as _re
        qs = [P.norm(q) for q in c.get("_qs", [])]
        slots += 0 if any(_re.match(r"^(what is|what's|what are|what does)\b", q) for q in qs) else 1
        slots += 0 if any(_re.search(r"^(how (do|to|can|would) (i|you|we)?\s*(make|create|build|set up|design|write))|^how to (make|create|build|set up)", q) for q in qs) else 1
    total = c["total"] + rec + slots
    return dict(c, recoverable=rec, slots=slots, total=total, feasible=total >= P.N_FAQ)
