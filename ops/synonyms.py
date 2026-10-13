"""synonyms.py: ruling 12 part 2 (Divit 2026-10-13). PA3 synonym candidates per page, for Divit's read; applied only from his sheet.

    python3 ops/synonyms.py sheet N [--pages URL,URL..]   tranche N: the next 50 queued pages under 10 (queue-rank order) or the given
                                                           pages -> .cache/review/pa3-tranche-N.md (reading copy) and .csv (decisions)
    python3 ops/synonyms.py apply N --by A-coord          apply Divit's filled .cache/review/pa3-tranche-N.csv
    python3 ops/synonyms.py status                        tranches, pages, decided (counts only)

Per page: the top 2 phrases (the first admits the most questions, the second the most the first does not) and under each phrase
EVERY question it admits, each re-gated with every other rule on (PA4, PA5, PA8, PA14, PA15...). Sheets hold AlsoAsked text, so they
live in .cache/ (git-ignored); git gets counts and question hashes only (status/synonyms.json, rules/paa_blocklist.json qh entries).

Decision sheet (.csv): one `phrase` row per phrase, decision `yes` or `no` (required: apply refuses a blank); one `question` row per
admitted question, decision blank = keep, `x` = strike. Applying:
  - approved phrases -> rules/paa_synonyms.json pages[slug] at once (per-page data, outside the Monday window: ruling 12);
  - struck questions -> rules/paa_blocklist.json per_page[slug] as {qh, reason, date} (PA4 skip) + a golden case (gate-pull-skip);
  - a page whose phrases are all rejected and that B has started (split write) goes back to the queue end, its draft kept;
  - status/synonyms.json records the decision; plan/queue-ranked.txt must be regenerated (ops/queue_rank.py).
"""
import collections, contextlib, csv, datetime, io, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H, paa_gate as P, park_rescue as R, guards as G

STATUS = os.path.join(ROOT, "status", "synonyms.json")
CACHE = os.path.join(ROOT, ".cache", "review")
STOP = set("a an the of for to in on and or is are what how do does why can i you your my with should be it this that best free".split())
def today(): return datetime.date.today().isoformat()
def load_status(): return json.load(open(STATUS)) if os.path.exists(STATUS) else {"_note": "Ruling 12 PA3 synonym tranches: counts only, no question text.", "pages": {}}
def save_status(d): json.dump(d, open(STATUS, "w"), indent=1, sort_keys=True)
def quiet(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)

def candidates(url):
    """[(phrase, kind, [admitted questions])] best first, re-gated with every other rule on; [] when nothing admits a question."""
    g = P.Gate(url)
    if not P.pulls(g.slug): return []
    items, _ = quiet(P.run_pull, g)
    rej = [i for i in items if i["verdict"] == "reject" and {x[0] for x in i["reasons"] if x[1] == "reject"} == {"PA3"}]
    head = [w for w in P.norm(g.primary).split() if w not in STOP]
    fmt = set(getattr(P, "FORMAT_WORDS", ()))
    core = [w for w in head if w not in fmt] or head
    grams = collections.Counter()
    for i in rej:
        ws = P.norm(i["q"]).split()
        for n in (1, 2, 3):
            for k in range(len(ws) - n + 1):
                t = ws[k:k + n]
                if t[0] in STOP or t[-1] in STOP: continue
                if not any(P.stem(a) == P.stem(c) for a in t for c in core): continue
                grams[" ".join(t)] += 1
    cands = [(p, "pull n-gram") for p, c in grams.most_common(8) if c >= 2] + [(p, k) for p, k in P.candidate_phrases(g.spec or {"keywords": {"primary": g.primary}})]
    seen, rows = set(), []
    for phrase, kind in cands:
        if phrase in seen or phrase == P.norm(g.primary): continue
        seen.add(phrase); gc = P.Gate(url, [phrase]); hr = P.phrase_re(phrase); adm = []
        for i in rej:
            if not hr.search(P.norm(i["q"])): continue
            rs = gc.judge({"q": i["q"], "ctx": i.get("ctx", ""), "source": "alsoasked", "prov": i.get("prov")})
            if not any(x[1] == "reject" for x in rs): adm.append(i["q"])
        if adm: rows.append((phrase, kind, adm))
    return rows

def top2(rows):
    if not rows: return []
    first = max(rows, key=lambda r: len(r[2])); rest = [r for r in rows if r is not first]
    second = max(rest, key=lambda r: len(set(r[2]) - set(first[2])), default=None)
    return [first] + ([second] if second and set(second[2]) - set(first[2]) else [])

def queued_under_10():
    import pull_wave as W
    out = []
    for p in W.queued():
        if not P.pulls(p["url"].rsplit("/", 1)[1]): continue
        f = quiet(R.feasibility, p["url"])
        if not f["feasible"]: out.append(p["url"])
    return out

def cmd_sheet(a):
    n = int(a[0]); st = load_status()
    urls = a[a.index("--pages") + 1].split(",") if "--pages" in a else [u for u in queued_under_10() if u.rsplit("/", 1)[1] not in st["pages"]][:50]
    md = [f"# PA3 synonym candidates, tranche {n} ({today()}; Divit ruling 12)", "",
          "For Divit's read. NOT applied until you fill the decision sheet: `.cache/review/pa3-tranche-%d.csv` (phrase rows: yes or no; question rows: x strikes that question). Git-ignored: contains AlsoAsked question text." % n,
          "Every listed question passes every other gate rule with the phrase on. Questions marked (also P1) are admitted by both phrases.", ""]
    rows_csv = []
    for u in urls:
        s = u.rsplit("/", 1)[1]; hub = H.hub_of(u)
        now_f = quiet(R.feasibility, u)
        t2 = top2(candidates(u)) if P.pulls(s) else []
        with_f = quiet(R.feasibility, u, tuple(p for p, _, _ in t2)) if t2 else now_f
        md.append(f"## {hub} · {s}: feasibility {now_f['total']}/10 now, {with_f['total']}/10 with both phrases")
        if not P.pulls(s): md.append("- no AlsoAsked pull yet (tonight's wave)")
        elif not t2: md.append("- no phrase admits a question (nothing to approve)")
        first = set(t2[0][2]) if t2 else set()
        for k, (phrase, kind, adm) in enumerate(t2, 1):
            md.append(f"- **P{k} \"{phrase}\"** ({kind}): admits {len(adm)}")
            rows_csv.append({"tranche": n, "hub": hub, "page": s, "kind": "phrase", "id": f"P{k}", "text": phrase, "also": "", "decision": ""})
            for q in adm:
                qh = P.qhash(q); also = " (also P1)" if k == 2 and q in first else ""
                md.append(f"  - `{qh}` {q}{also}")
                rows_csv.append({"tranche": n, "hub": hub, "page": s, "kind": "question", "id": qh, "text": q, "also": "P1" if also else "", "decision": ""})
        md.append("")
        st["pages"][s] = {"url": u, "tranche": n, "phrases": len(t2), "admits": len({q for _, _, a_ in t2 for q in a_}), "feasibility": now_f["total"],
                          "feasibility_with": with_f["total"], "pending": bool(t2), "sheet": today()}
    os.makedirs(CACHE, exist_ok=True)
    open(os.path.join(CACHE, f"pa3-tranche-{n}.md"), "w").write("\n".join(md))
    with open(os.path.join(CACHE, f"pa3-tranche-{n}.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["tranche", "hub", "page", "kind", "id", "text", "also", "decision"]); w.writeheader(); w.writerows(rows_csv)
    save_status(st)
    pend = [s for s, e in st["pages"].items() if e["tranche"] == n]
    print(f"tranche {n}: {len(urls)} pages, {sum(st['pages'][s]['pending'] for s in pend)} with phrases; reaching 10 with both phrases: "
          f"{sum(st['pages'][s]['feasibility_with'] >= 10 for s in pend)}; sheet .cache/review/pa3-tranche-{n}.md + .csv")

def cmd_apply(a):
    n = int(a[0]); by = a[a.index("--by") + 1] if "--by" in a else None
    if not by or not by.startswith("A-"): sys.exit("refused: apply --by A-<id> (coordinator); the decisions are Divit's, from his sheet")
    rows = list(csv.DictReader(open(os.path.join(CACHE, f"pa3-tranche-{n}.csv"))))
    blank = [f"{r['page']} {r['id']}" for r in rows if r["kind"] == "phrase" and r["decision"].strip().lower() not in ("yes", "no")]
    if blank: sys.exit(f"refused: {len(blank)} phrase row(s) without yes/no: " + ", ".join(blank[:8]))
    bad = [f"{r['page']} {r['id']}" for r in rows if r["kind"] == "question" and r["decision"].strip().lower() not in ("", "x")]
    if bad: sys.exit("refused: question rows take blank (keep) or x (strike): " + ", ".join(bad[:8]))
    syn = json.load(open(os.path.join(ROOT, "rules", "paa_synonyms.json")))
    bl = json.load(open(os.path.join(ROOT, "rules", "paa_blocklist.json")))
    st = load_status(); cases = []; out = collections.Counter(); back = []
    for page in sorted({r["page"] for r in rows}):
        pr = [r for r in rows if r["page"] == page]; e = st["pages"].get(page) or {}
        yes = [r["text"] for r in pr if r["kind"] == "phrase" and r["decision"].strip().lower() == "yes"]
        no = [r for r in pr if r["kind"] == "phrase" and r["decision"].strip().lower() == "no"]
        struck = sorted({r["id"] for r in pr if r["kind"] == "question" and r["decision"].strip().lower() == "x"})
        if yes:
            cur = syn["pages"].setdefault(page, [])
            cur += [p for p in yes if p not in cur]
        for qh in struck:
            ent = bl["per_page"].setdefault(page, [])
            if not any(x.get("qh") == qh for x in ent):
                ent.append({"qh": qh, "reason": f"struck by Divit from the ruling 12 PA3 tranche {n} sheet (admitted by a synonym, not this page's question)", "date": today()})
            cases.append({"id": f"r12-t{n}-{page}-{qh}", "source": "Divit strike (ruling 12)", "date": today(), "kind": "gate-pull-skip",
                          "url": e.get("url") or "", "qh": qh, "expect": ["PA4"], "note": "struck question stays out (hash only; text in the saved pull)", "status": "guarded"})
        e.update({"decided": today(), "approved": len(yes), "rejected": len(no), "struck": len(struck), "pending": False})
        st["pages"][page] = e; out["approved"] += len(yes); out["rejected"] += len(no); out["struck"] += len(struck)
        if not yes and e.get("url"):   # every phrase rejected: a split-write page goes back to the queue end, its draft kept
            hub = H.hub_of(e["url"]); ent = H.load_st(hub)["pages"].get(e["url"])
            if ent and ent.get("faq_pending") and ent.get("state") in ("claimed", "spec"):
                with G.lock("status-" + hub):
                    s_ = H.load_st(hub); s_["pages"].pop(e["url"], None); H.save_st(hub, s_)
                back.append(e["url"])
        elif yes and e.get("url"):     # approved: a split-write page may now get its FAQ
            hub = H.hub_of(e["url"])
            with G.lock("status-" + hub):
                s_ = H.load_st(hub); ent = s_["pages"].get(e["url"])
                if ent and ent.get("faq_pending"): ent["faq_pending"] = False; ent["faq_unblocked"] = H.now(); H.save_st(hub, s_)
    syn.setdefault("_log", []).append({"date": today(), "by": "Divit (ruling 12, tranche %d), applied by %s" % (n, by), "pages": len({r['page'] for r in rows}), "phrases_approved": out["approved"]})
    json.dump(syn, open(os.path.join(ROOT, "rules", "paa_synonyms.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(bl, open(os.path.join(ROOT, "rules", "paa_blocklist.json"), "w"), indent=1, ensure_ascii=False)
    if cases:
        with open(os.path.join(ROOT, "tests", "golden", "cases.jsonl"), "a") as f:
            for c in cases: f.write(json.dumps(c) + "\n")
    save_status(st)
    print(f"tranche {n} applied: {out['approved']} phrases approved, {out['rejected']} rejected, {out['struck']} questions struck ({len(cases)} golden cases); "
          f"{len(back)} split-write page(s) back to the queue end: {', '.join(back) or 'none'}. Next: ops/queue_rank.py, golden suite, commit.")

def cmd_status(a):
    st = load_status()["pages"]; by = collections.defaultdict(list)
    for s, e in st.items(): by[e["tranche"]].append(e)
    for t, es in sorted(by.items()):
        print(f"tranche {t}: {len(es)} pages, {sum(e['pending'] for e in es)} pending, {sum(1 for e in es if e.get('decided'))} decided, "
              f"{sum(e['feasibility'] >= 10 for e in es)} at 10 now, {sum(e['feasibility_with'] >= 10 for e in es)} at 10 with both phrases")

if __name__ == "__main__":
    a = sys.argv[1:]
    {"sheet": cmd_sheet, "apply": cmd_apply, "status": cmd_status}.get(a[0] if a else "", lambda _: sys.exit(__doc__))(a[1:])
