"""flag_packet.py: Divit's flag packet grouped by subtype (Divit 2026-10-13).

    python3 ops/flag_packet.py build            every flagged FAQ candidate (AlsoAsked pulls and Semrush questions) on pages not yet
                                                shipped -> .cache/review/packet-flags-<date>.md (reading copy: count, pages, 3 real
                                                examples, pages each decision brings to 10) and .csv (decisions)
    python3 ops/flag_packet.py apply FILE.csv --by A-coord    apply Divit's marks -> rules/flag_decisions.json + golden cases
    python3 ops/flag_packet.py impact           counts only: per subtype, questions, pages and pages reaching 10 if approved

Decision sheet: one `subtype` row per subtype (approve | reject | blank = undecided). Mixed subtypes (PA10, PA14) also get one
`question` row per question (approve | reject | blank). Approved subtypes become notes and rejected ones rejects on every page
(qc/paa_gate.py judge). The sheet holds AlsoAsked and Semrush text: .cache only, never git.
"""
import collections, contextlib, csv, datetime, io, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H, paa_gate as P, park_rescue as R, semrush_questions as SQ

CACHE = os.path.join(ROOT, ".cache", "review"); DEC = os.path.join(ROOT, "rules", "flag_decisions.json")
SKIP_STATES = ("reviewed", "approved", "cms_draft", "published")
def today(): return datetime.date.today().isoformat()
def quiet(f, *a):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a)

def pages():
    st = {u: e for h in H.CFG["hubs"] for u, e in H.load_st(h)["pages"].items()}
    return [u for u, p in H.kmap().items() if p.get("status") == "planned" and (st.get(u) or {}).get("state") not in SKIP_STATES]

def collect():
    """[(subtype, url, source, q, qh)] for every flag, plus per-page pass counts for the impact estimate."""
    flags, base = [], {}
    for u in pages():
        s = u.rsplit("/", 1)[1]
        if not P.pulls(s) and not SQ.usable(s): continue
        g = P.Gate(u); f = quiet(R.feasibility, u); base[u] = f["total"]
        seen = set()
        if P.pulls(s):
            items, _ = quiet(P.run_pull, g)
            for i in items:
                if i["verdict"] != "flag" or P.qhash(i["q"]) in seen: continue
                seen.add(P.qhash(i["q"]))
                for r in i["reasons"]:
                    if r[1] == "flag": flags.append((P.flag_subtype(r[0], r[2]), u, "alsoasked", i["q"], P.qhash(i["q"])))
        for x in SQ.usable(s):
            if P.qhash(x["q"]) in seen: continue
            rs = g.judge({"q": x["q"], "source": "keyword", "n": 5})
            for r in rs:
                if r[1] == "flag": seen.add(P.qhash(x["q"])); flags.append((P.flag_subtype(r[0], r[2]), u, "semrush", x["q"], P.qhash(x["q"])))
    return flags, base

def impact(flags, base):
    """Pages that reach 10 when one subtype is approved. Feasibility already counts semrush/FAQ flags as usable, so pass-only =
    total - flagged semrush items counted; pull flags are not in the total (a6_count counts pull passes only)."""
    by_page = collections.defaultdict(lambda: collections.Counter())
    for st, u, src, q, qh in flags: by_page[u][(st, src)] += 1
    out = collections.Counter()
    for u, c in by_page.items():
        sq_flags = sum(v for (st, src), v in c.items() if src == "semrush")
        passes = base[u] - min(sq_flags, quiet(R.a6_count, u).get("sq", 0))
        for st in {st for st, _ in c}:
            add = sum(v for (s_, _), v in c.items() if s_ == st)
            if passes < 10 <= passes + add: out[st] += 1
    return out

def cmd_build(a):
    flags, base = collect(); imp = impact(flags, base)
    by = collections.defaultdict(list)
    for f in flags: by[f[0]].append(f)
    md = [f"# Flag packet by subtype ({today()}; Divit 2026-10-13)", "",
          "Tick a whole subtype approve or reject in `.cache/review/packet-flags-%s.csv`. Mixed subtypes (PA10, PA14) are decided per question. Approved subtypes apply on every page carrying them. Git-ignored: contains AlsoAsked and Semrush text." % today(), ""]
    rows = []
    for st, fs in sorted(by.items(), key=lambda x: -len(x[1])):
        pgs = {f[1] for f in fs}
        md.append(f"## {st}: {len(fs)} questions on {len(pgs)} pages; approving it brings {imp.get(st, 0)} page(s) to 10")
        rows.append({"kind": "subtype", "subtype": st, "page": "", "id": "", "source": "", "text": f"{len(fs)} questions, {len(pgs)} pages, +{imp.get(st, 0)} pages to 10", "decision": ""})
        mixed = st in P.MIXED_SUBTYPES
        for f in (fs if mixed else fs[:3]):
            md.append(f"- `{f[4]}` ({f[1].rsplit('/', 1)[1]}, {f[2]}) {f[3]}")
            if mixed: rows.append({"kind": "question", "subtype": st, "page": f[1].rsplit("/", 1)[1], "id": f[4], "source": f[2], "text": f[3], "decision": ""})
        if not mixed and len(fs) > 3: md.append(f"- … {len(fs) - 3} more of the same subtype")
        md.append("")
    os.makedirs(CACHE, exist_ok=True)
    open(os.path.join(CACHE, f"packet-flags-{today()}.md"), "w").write("\n".join(md))
    with open(os.path.join(CACHE, f"packet-flags-{today()}.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["kind", "subtype", "page", "id", "source", "text", "decision"]); w.writeheader(); w.writerows(rows)
    print(f"packet: {len(flags)} flagged questions in {len(by)} subtypes on {len({f[1] for f in flags})} pages -> .cache/review/packet-flags-{today()}.md + .csv")
    for st, fs in sorted(by.items(), key=lambda x: -len(x[1])): print(f"  {st}: {len(fs)} questions, {len({f[1] for f in fs})} pages, +{imp.get(st, 0)} pages to 10")

def cmd_impact(a):
    flags, base = collect(); imp = impact(flags, base); by = collections.Counter(f[0] for f in flags)
    for st, n in by.most_common(): print(f"{st}: {n} questions, +{imp.get(st, 0)} pages to 10")

def cmd_apply(a):
    f = a[0]; by = a[a.index("--by") + 1] if "--by" in a else ""
    if not by.startswith("A-"): sys.exit("refused: apply --by A-<id>; the decisions are Divit's marks on the packet")
    rows = list(csv.DictReader(open(f))); dec = json.load(open(DEC)); cases = []; n = collections.Counter()
    # real examples for the golden cases are taken BEFORE the decisions land (an approved subtype stops showing as a flag)
    pre_flags = collect()[0] if any(r["kind"] == "subtype" and r["decision"].strip() for r in rows) else []
    bad = [r for r in rows if r["decision"].strip().lower() not in ("", "approve", "reject")]
    if bad: sys.exit(f"refused: decisions are approve, reject or blank ({len(bad)} other)")
    examples = collections.defaultdict(list)
    for r in rows:
        if r["kind"] == "question": examples[r["subtype"]].append(r)
    for r in rows:
        d = r["decision"].strip().lower()
        if not d: continue
        if r["kind"] == "subtype":
            dec["subtypes"][r["subtype"]] = {"decision": d, "date": today(), "by": f"Divit (packet), applied by {by}"}; n[d + " subtype"] += 1
        else:
            dec["questions"][r["page"] + ":" + r["id"]] = {"decision": d, "subtype": r["subtype"], "date": today(), "by": f"Divit (packet), applied by {by}"}; n[d + " question"] += 1
            cases.append({"page": r["page"], "id": r["id"], "source": r["source"], "subtype": r["subtype"], "expect": "reject" if d == "reject" else "not-flag"})
    json.dump(dec, open(DEC, "w"), indent=1, ensure_ascii=False)
    # one golden case per decided subtype, on a real flagged question of that subtype (hash only)
    flags = pre_flags
    decided = {r["subtype"]: r["decision"].strip().lower() for r in rows if r["kind"] == "subtype" and r["decision"].strip()}
    for st, d in decided.items():
        ex = next((f for f in flags if f[0] == st), None)
        if not ex:   # flags of an approved subtype no longer show as flags: find one through the notes instead
            continue
        cases.append({"page": ex[1].rsplit("/", 1)[1], "id": ex[4], "source": ex[2], "subtype": st, "expect": "reject" if d == "reject" else "not-flag"})
    with open(os.path.join(ROOT, "tests", "golden", "cases.jsonl"), "a") as fh:
        for c in cases:
            url = next(u for u in H.kmap() if u.rsplit("/", 1)[1] == c["page"])
            fh.write(json.dumps({"id": f"flagdec-{today()}-{c['page']}-{c['id']}", "source": "Divit flag packet", "date": today(), "kind": "gate-flag-decision",
                                 "url": url, "qh": c["id"], "from": c["source"], "subtype": c["subtype"], "expect": c["expect"], "status": "guarded"}) + "\n")
    print("applied: " + ", ".join(f"{k} {v}" for k, v in n.items()) + f"; golden cases {len(cases)}")

if __name__ == "__main__":
    a = sys.argv[1:]
    {"build": cmd_build, "apply": cmd_apply, "impact": cmd_impact}.get(a[0] if a else "", lambda _: sys.exit(__doc__))(a[1:])
