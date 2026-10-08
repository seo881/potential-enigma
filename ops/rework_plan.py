"""rework_plan.py: rebuild plan/rework-2026-10-08.md and Divit's reading files after the deterministic pass. No API calls.

    .venv/bin/python3 ops/rework_plan.py

Inputs: QC now (qc/qc_hub.py on every written spec), .cache/review/paa.csv (FAQ items to replace, strict gate with PA3
widened; risk tags), .cache/review/park-rescue.csv (ops/park_rescue.py), .cache/review/pa3-newly-passing.csv,
rules/paa_synonym_candidates.json, plan/keyword_map.json (order only; no Semrush numbers are written to the plan).
Outputs: plan/rework-2026-10-08.md (public: no question or keyword text, no volumes), .cache/review/pa3-newly-passing-fastlane.csv,
.cache/review/synonym-candidates-compact.csv. Prints counts only.
"""
import csv, json, os, re, sys, glob
from collections import Counter, defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "qc")); sys.path.insert(0, os.path.join(ROOT, "ops"))
import qc_hub as Q, paa_gate as P, guards as G

WRITTEN = {"qc_pass", "images", "rework", "reviewed", "challenged"}
HUBS = ["LP", "Form", "Auto", "SurveyQuiz"]
REVIEW = 89          # k tokens, one full review, measured on registration-form 2026-10-08
BATCH = 44           # k tokens per page, 4-page batch agents 2026-10-07 (six agents, older protocol): NOT measured under SEVERITY.md
WRITER = {"clean": 0, "faq": 35, "faq+copy": 65, "copy": 40}   # k tokens per page, estimates carried from the first plan
CR = os.path.join(ROOT, ".cache", "review")
COPY_NOTE = "A5/A6 or a leftover C4/C5/H3/H4 the guard could not fix"

def links(spec, hub_paths):
    text = " ".join(v for v in spec["fields"].values() if isinstance(v, str))
    return {m for m in re.findall(r"href=\\?[\"'](?:https?://(?:www\.)?emergent\.sh)?(/[a-z0-9/-]+)", text)
            if m.startswith(hub_paths) and m != spec["url"]}

def main():
    st = {u: e.get("state") for u, e in G.all_status().items()}
    every = Q.load_specs(sorted(glob.glob(os.path.join(ROOT, "specs", "*", "*.json"))))
    specs = {s["url"]: s for s in every if st.get(s["url"]) in WRITTEN}
    paa = {r["url"]: r for r in csv.DictReader(open(os.path.join(CR, "paa.csv")))}
    resc = {r["url"]: r for r in csv.DictReader(open(os.path.join(CR, "park-rescue.csv")))}
    km = json.load(open(os.path.join(ROOT, "plan", "keyword_map.json")))
    vol = lambda u: (km.get(u) or {}).get("total_msv", 0)
    hub_paths = tuple(h["path"] + "/" for h in Q.CFG["hubs"].values())
    rows = {}
    for u, s in specs.items():
        codes = Counter(i["code"] for i in Q.check(s, every) if i["sev"] in ("P0", "P1"))
        r = paa.get(u, {}); rep = int(r.get("replace_strict") or 0); tags = r.get("risk_tags", "")
        lm, roll = "legal/medical" in tags, "rolling-figures" in tags
        if u in resc: grp = "park"
        elif rep == 0 and not codes: grp = "clean"
        elif rep and not codes: grp = "faq"
        elif rep: grp = "faq+copy"
        else: grp = "copy"
        rows[u] = {"url": u, "hub": s["hub"], "group": grp, "replace": rep, "codes": codes, "lm": lm, "roll": roll,
                   "links": links(s, hub_paths), "park_class": resc.get(u, {}).get("class", "")}
    # ---- fast lane: 1-2 replacements without legal/medical or rolling-figure tags, plus copy-only, plus employee-engagement-survey
    fast = [u for u, r in rows.items() if r["group"] != "park" and (
        (r["replace"] in (1, 2) and not r["lm"] and not r["roll"]) or r["group"] in ("copy", "clean") or u.endswith("/employee-engagement-survey"))]
    # publish order: link-connected fast-lane pages travel together (components), components and pages by demand
    adj = defaultdict(set)
    for u in fast:
        for v in rows[u]["links"]:
            if v in fast: adj[u].add(v); adj[v].add(u)
    seen, comps = set(), []
    for u in sorted(fast, key=lambda x: -vol(x)):
        if u in seen: continue
        comp, stack = [], [u]
        while stack:
            x = stack.pop()
            if x in seen: continue
            seen.add(x); comp.append(x); stack.extend(adj[x] - seen)
        comps.append(sorted(comp, key=lambda x: -vol(x)))
    comps.sort(key=lambda c: -max(vol(x) for x in c))
    order = [u for c in comps for u in c]
    # ---- review options (non-park pages)
    live = [r for r in rows.values() if r["group"] != "park"]
    wtok = sum(WRITER[r["group"]] for r in live)
    full_b = [r for r in live if r["lm"] or r["roll"] or r["replace"] >= 5]
    opts = [("(a) full review, every page", len(live), wtok, REVIEW * len(live)),
            ("(b) full review only for legal/medical, rolling-figure and 5+ replacement pages; code QC + PAA gate + PA13 skim for the rest",
             len(live), wtok, REVIEW * len(full_b)),
            ("(c) batch review, 4 pages per agent, every page (per-page cost UNMEASURED under the current protocol)", len(live), wtok, BATCH * len(live))]
    # ---- counts per hub
    G_ORDER = ["clean", "faq", "faq+copy", "copy", "park"]
    G_NAME = {"clean": "clean", "faq": "FAQ only", "faq+copy": "FAQ + A5/A6 (or leftover copy)", "copy": "copy only", "park": "park"}
    cnt = Counter((r["hub"], r["group"]) for r in rows.values())
    park_cls = Counter(r["park_class"] for r in rows.values() if r["group"] == "park")
    no_park = [h for h in HUBS if not cnt[(h, "park")] and any(cnt[(h, g)] for g in G_ORDER)]
    L = []
    L.append("# Combined rework pass plan (2026-10-08, rebuilt after the deterministic pass): NOT executed\n")
    L.append("Rebuilt by `ops/rework_plan.py` after Part 1 (C5, H3, S10, H4, C4 autofixed where the guard allowed: commits a05c597, a1c5029, 566f1c0, dc083c5), "
             "Part 2 (A6 allows \"your team\" on group pages: c32850e) and Part 3 (park rescue analysis: f912f1f, `.cache/review/park-rescue.csv`). "
             "One combined pass per page (DECISIONS 2026-10-08): one writer pass for FAQ replacements (approved secondaries and gate-passing AlsoAsked "
             "questions only, never rejected PAA) and the copy flags QC still raises, then one QC and one review. Nothing runs until Divit has read "
             "`.cache/review/pa3-newly-passing-fastlane.csv` (and the full `.cache/review/pa3-newly-passing.csv` for the rest) and given the go.\n")
    L.append("Groups: **clean** = no FAQ item to replace and QC TOTAL 0. **FAQ only** = FAQ items to replace, no copy flag. "
             f"**FAQ + A5/A6** = FAQ items to replace and a copy flag ({COPY_NOTE}). **copy only** = copy flags, no FAQ change. "
             "**park** = fewer than 8 on-topic FAQ sources (PA11) even counting gate-passing AlsoAsked questions and unused secondaries.\n")
    L.append("## Counts per hub\n")
    L.append("| Hub | " + " | ".join(G_NAME[g] for g in G_ORDER) + " | Total |"); L.append("|---" * (len(G_ORDER) + 2) + "|")
    for h in HUBS:
        L.append(f"| {h} | " + " | ".join(str(cnt[(h, g)]) for g in G_ORDER) + f" | {sum(cnt[(h, g)] for g in G_ORDER)} |")
    L.append("| **All** | " + " | ".join(str(sum(cnt[(h, g)] for h in HUBS)) for g in G_ORDER) + f" | {len(rows)} |\n")
    L.append(f"Park ({sum(park_cls.values())}): " + ", ".join(f"{k} {v}" for k, v in sorted(park_cls.items())) +
             ". Rescued by (a) only if Divit approves those pages' SAFE synonym candidates; (b) adds nothing (the workbook's question-form ideas "
             "are all secondaries already, on non-parked pages); (c) is an estimate at about one gate-passing question per pull (1 credit a page), "
             "so most of the 51 would still be short after one pull. Details per page: `.cache/review/park-rescue.csv`.\n")
    L.append("**Hubs that can go fully live without any parked page:** " + (", ".join(no_park) if no_park else "none") +
             " (every written page in these hubs is outside the park group; their never-written queue items parked for library gaps are separate).\n")
    L.append("## Review options (pages outside the park group)\n")
    L.append("| Option | Pages | Writer tokens | Review tokens | Total |"); L.append("|---|---|---|---|---|")
    for name, n, w, rv in opts: L.append(f"| {name} | {n} | {w / 1000:.2f}M | {rv / 1000:.2f}M | {(w + rv) / 1000:.2f}M |")
    L.append(f"\nWriter tokens per page are the first plan's estimates (FAQ only {WRITER['faq']}k, FAQ + copy {WRITER['faq+copy']}k, copy only {WRITER['copy']}k). "
             f"Review: {REVIEW}k measured on registration-form (2026-10-08). Option (b) gives a full review to {len(full_b)} pages and none to the other "
             f"{len(live) - len(full_b)}. Option (c): {BATCH}k per page is the mean of six 4-page batch agents on 2026-10-07 under the older review protocol; "
             "it is not measured under SEVERITY.md and must be measured on the first batch before it is relied on. "
             f"If Divit approves the (a) synonyms, the {park_cls.get('rescued by (a)', 0)} rescued pages add about "
             f"{park_cls.get('rescued by (a)', 0) * (WRITER['faq+copy'] + REVIEW) / 1000:.2f}M at option (a) rates.\n")
    L.append(f"## FAST LANE ({len(order)} pages, publish order)\n")
    L.append("Pages with 1-2 FAQ replacements and no legal/medical or rolling-figure tag, the copy-only and clean pages, and employee-engagement-survey. "
             "Order: pages that link to each other share a block letter and publish together; blocks and single pages by demand. A link to a page that is not live ships as plain "
             "text and is re-linked when the target goes live (DECISIONS 2026-10-08).\n")
    n = 0; blk = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for c in comps:
        b = next(blk) if len(c) > 1 else None
        for u in c:
            n += 1; r = rows[u]
            L.append(f"{n}. {'**block ' + b + '** ' if b else ''}{u} ({G_NAME[r['group']]}; FAQ items to replace: {r['replace']}; QC: {', '.join(sorted(r['codes'])) or 'clean'})")
    L.append("")
    for g in G_ORDER:
        grp = sorted((r for r in rows.values() if r["group"] == g), key=lambda r: r["url"])
        L.append(f"## {G_NAME[g]} ({len(grp)})")
        for r in grp:
            extra = f"; {r['park_class']}" if g == "park" else ""
            tags = "; ".join(t for t, on in (("legal/medical", r["lm"]), ("rolling figures", r["roll"])) if on)
            L.append(f"- {r['url']} (FAQ items to replace: {r['replace']}; QC: {', '.join(sorted(r['codes'])) or 'clean'}{extra}{'; ' + tags if tags else ''})")
        L.append("")
    open(os.path.join(ROOT, "plan", "rework-2026-10-08.md"), "w").write("\n".join(L))
    # ---- reading files (private: .cache/review/)
    pos = {u: i for i, u in enumerate(order, 1)}
    pa3 = [r for r in csv.DictReader(open(os.path.join(CR, "pa3-newly-passing.csv"))) if r["url"] in pos]
    pa3.sort(key=lambda r: (pos[r["url"]], r["set"], int(r["n"] or 0)))
    with open(os.path.join(CR, "pa3-newly-passing-fastlane.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["publish_order", "url", "set", "n", "verdict", "question", "admitted_by"])
        for r in pa3: w.writerow([pos[r["url"]], r["url"], r["set"], r["n"], r["verdict"], r["question"], r["admitted_by"]])
    cand = json.load(open(os.path.join(ROOT, "rules", "paa_synonym_candidates.json")))["pages"]
    out = []
    for u, r in rows.items():
        cs = cand.get(u.rsplit("/", 1)[1], [])
        if not cs: continue
        unlock = []
        for c in cs:
            if c["status"] != "safe": continue
            g0, g1 = P.Gate(u), P.Gate(u, [c["phrase"]])
            for f_ in (P.run_spec,) + ((P.run_pull,) if os.path.exists(P.pull_path(g0.slug)) else ()):
                a = {i["q"] for i in f_(g0)[0] if i["verdict"] != "reject"}; b = [i["q"] for i in f_(g1)[0] if i["verdict"] != "reject"]
                unlock += [q for q in b if q not in a and q not in unlock]
        out.append({"page": u, "park": r["group"] == "park", "park_class": r["park_class"],
                    "proposed_synonym": "; ".join(c["phrase"] for c in cs), "status": "; ".join(c["status"] for c in cs),
                    "questions_unlocked": len(unlock), "questions": " | ".join(unlock)})
    out.sort(key=lambda x: (not x["park"], x["page"]))
    with open(os.path.join(CR, "synonym-candidates-compact.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    print("groups", dict(Counter(r["group"] for r in rows.values())), "| park", dict(park_cls), "| fast lane", len(order), "in", len(comps), "blocks")
    for name, n_, w_, rv in opts: print(f"  {name[:60]}: pages {n_}, writer {w_ / 1000:.2f}M, review {rv / 1000:.2f}M, total {(w_ + rv) / 1000:.2f}M")
    print("hubs fully live without a parked page:", no_park)
    print(f"pa3-newly-passing-fastlane.csv: {len(pa3)} rows on {len({r['url'] for r in pa3})} pages; "
          f"synonym-candidates-compact.csv: {len(out)} pages ({sum(x['park'] for x in out)} parked), {sum(x['questions_unlocked'] for x in out)} questions unlocked")

if __name__ == "__main__":
    main()
