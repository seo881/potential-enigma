"""swap_recheck.py: Divit 2026-10-14 step 3. The pages re-parked because a ruling-18 FAQ swap could not reach 10 (status note
"r18-swap-short ...") are re-checked automatically whenever new Semrush or AlsoAsked data lands; a page whose listed questions all
have a code-built replacement now goes back to rework (a B writer swaps exactly those, ruling 18.3). Counts only, never question text.

    python3 ops/swap_recheck.py [--dry] [--quiet] [--force]      also: hubctl swap-recheck [--dry] [--quiet] [--force]

Per parked page: the Q numbers to swap (the note's lead clause, plus any FAQ item the gate rejects today for its question, not its
answer; PA12 item 1/2 shape problems add slot 1/2), then the replacements B would take: skeleton.plan_slots (every gate check,
answer-source checks included) minus near-duplicates (paa_gate.near_dup or PA9 Jaccard) of the kept and the dropped questions, and
minus the candidates judged off-intent or off-sense when the page was parked (status/swap_short.json, by hash). Enough for every
listed Q = released (state rework). Unchanged data since the last check (.cache/swap_recheck.json fingerprint) = skipped unless --force.
Runs at the end of `semrush_questions.py derive`, at the end of a successful `weekend.py aa` pull, and in `overnight.py next`.
"""
import contextlib, io, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H, paa_gate as P

TAG = "r18-swap-short"
BASE = os.path.join(ROOT, "status", "swap_short.json")      # judged-out candidates per page (hashes only): never counted again
CACHE = os.path.join(ROOT, ".cache", "swap_recheck.json")   # data fingerprint at the last check (git-ignored)
JUDGED = re.compile(r"off-intent|off-sense")                # park reasons that judged the existing candidates, not their number
QUESTION_OK = ("PA1b",)                                     # answer-text rejects: fixed in the answer, not by a swap

def parked():
    return [(u, e) for h in H.CFG["hubs"] for u, e in H.load_st(h)["pages"].items()
            if e.get("state") == "parked" and (e.get("note") or "").startswith(TAG)]

def listed(note):
    """The Q numbers in the note's lead clause: "Q10 needs a swap", "Q6, Q7, Q10 need swaps", "Q5-Q8 need swaps", "Q2 rejects"."""
    m = re.match(TAG + r"[^:]*:\s*((?:Q\d+(?:\s*-\s*Q\d+)?(?:,\s*|\s+and\s+)?)+)\s*(?:needs?|rejects)", note or "")
    out = set()
    for a, b in re.findall(r"Q(\d+)(?:\s*-\s*Q(\d+))?", m.group(1) if m else ""):
        out |= set(range(int(a), int(b or a) + 1))
    return out

def gate_needs(url, spec=None):
    """FAQ positions the gate (paa --spec) rejects today for the question itself, and PA12 item 1/2 shape problems. spec: judge this
    spec (golden: the spec at a commit) instead of the file."""
    g = P.Gate(url)
    if spec is not None: g.spec = spec; g.new_writing = not P.reviewed_already(spec)
    with contextlib.redirect_stdout(io.StringIO()): items, page = P.run_spec(g)
    need = {i["n"] for i in items if any(r[1] == "reject" and r[0] not in QUESTION_OK and not (r[0] == "PA12" and "lead with the answer" in r[2])
                                       for r in i["reasons"])}
    need |= {1 for r, m in page if r == "PA12" and "item 1" in m} | {2 for r, m in page if r == "PA12" and "item 2 is not" in m}
    return need, items

def near(a, b, prim): return P.near_dup(a, b, prim) or P.jacc(P.content(a), P.content(b)) >= P.JACCARD_DUP

def available(url, need, items, slots=None, excluded=(), spec=None):
    """Replacements for the positions in need: code-built slots in slot order, each not a near-duplicate of a kept question, a dropped
    one (their FAQ text, and the slot question and source wording they came from: a writer may reword a Semrush slot) or a replacement
    already taken; slot 1/2 (definition, how-to-build) only for position 1/2. Returns (filled, needed)."""
    import skeleton as SK
    prim = (H.kmap().get(url) or {}).get("primary") or url.rsplit("/", 1)[1].replace("-", " ")
    slots = slots if slots is not None else SK.quiet(SK.plan_slots, url, None)
    spec = spec if spec is not None else (json.load(open(H.spath(url))) if os.path.exists(H.spath(url)) else {})
    kept = [i["q"] for i in items if i["n"] not in need]
    own = [i["q"] for i in items] + [x for sl in spec.get("faq_plan") or [] for x in (sl.get("q"), sl.get("ref")) if x] + \
          [f["ref"] for f in spec.get("faq_sources") or [] if f.get("ref")]
    ownn = {P.norm(x) for x in own}
    g = P.Gate(url); resp = lambda q: g.asker(P.norm(q)) == "respondent"
    nresp = sum(resp(q) for q in kept); taken = []
    ok = lambda sl: sl.get("q") and P.qhash(sl["q"]) not in excluded and P.norm(sl.get("ref") or "") not in ownn and \
        not any(near(sl["q"], x, prim) for x in own + taken)
    for pos, sl in ((1, slots[0] if slots else None), (2, slots[1] if len(slots) > 1 else None)):
        if pos in need and sl and ok(sl): taken.append(sl["q"])
    rest = len([n for n in need if n not in (1, 2)])
    carried = [P.content(x) for x in own + taken]
    for sl in slots[2:]:
        if len(taken) >= len(need) or rest <= 0: break
        q = sl.get("q")
        if sl.get("kind") == "secondary":   # a code-built secondary slot no question of the page (kept or dropped) carries yet
            c = P.content(sl.get("ref") or "")
            if c and not any(c <= x for x in carried): carried.append(c); taken.append(sl["ref"]); rest -= 1
            continue
        if sl.get("kind") not in ("alsoasked", "semrush") or not ok(sl): continue
        if resp(q) and nresp >= P.MAX_RESPONDENT: continue
        nresp += resp(q); taken.append(q); rest -= 1
    return len(taken), len(need)

def fingerprint(url):
    import semrush_questions as SQ
    s = url.rsplit("/", 1)[1]
    fs = [P.pull_path(s), P.sec_pull_path(s), os.path.join(SQ.DER, s + ".json"), H.spath(url), os.path.join(ROOT, "plan", "keyword_map.json"),
          os.path.join(ROOT, "ops", "skeleton.py"), os.path.join(ROOT, "qc", "paa_gate.py")] + \
         [os.path.join(ROOT, "rules", f) for f in ("paa_patterns.json", "paa_blocklist.json", "paa_synonyms.json", "flag_decisions.json")]
    return "|".join(f"{os.path.relpath(f, ROOT)}:{os.stat(f).st_mtime_ns}:{os.stat(f).st_size}" if os.path.exists(f) else "-" for f in fs)

def _load(p, d):
    try: return json.load(open(p))
    except Exception: return d

def run(dry=False, quiet=False, force=False, by=None):
    """Returns {"parked", "checked", "unchanged", "releasable", "released", "pages": {slug: "filled/needed"}}."""
    import skeleton as SK
    base = _load(BASE, {"_note": "Divit 2026-10-14 step 3 (ops/swap_recheck.py): per r18-swap-short page parked because its existing "
                              "candidates were judged off-intent or off-sense, the hashes of those candidates; never counted as replacements.", "pages": {}})
    cache = _load(CACHE, {}); res = {"parked": 0, "checked": 0, "unchanged": 0, "releasable": 0, "released": 0, "pages": {}}
    base_new = False
    for url, e in parked():
        res["parked"] += 1; s = url.rsplit("/", 1)[1]; fp = fingerprint(url)
        if not force and cache.get(url) == fp: res["unchanged"] += 1; continue
        res["checked"] += 1
        need, items = gate_needs(url); need |= listed(e.get("note"))
        slots = SK.quiet(SK.plan_slots, url, None)
        if JUDGED.search(e.get("note") or "") and s not in base["pages"]:
            # first check after parking: the candidates on hand then were judged (ruling 18.4); only new data can release the page
            base["pages"][s] = {"t": H.now(), "excluded": sorted({P.qhash(x["q"]) for x in slots if x.get("kind") in ("alsoasked", "semrush") and x.get("q")})}
            base_new = True
        got, n = available(url, need, items, slots, set((base["pages"].get(s) or {}).get("excluded") or []))
        res["pages"][s] = f"{got}/{n}"
        if n and got >= n:
            res["releasable"] += 1
            if not dry and not (e.get("hold") and H.hold_account(e["hold"]) != H.clone_account()):
                qs = ", ".join(f"Q{x}" for x in sorted(need))
                H.set_state(url, "rework", via="swap-recheck", by=by or f"{H.clone_account()}-swap-recheck",
                            note=f"r18-swap-recheck (Divit 2026-10-14): {qs} need swaps; candidates now available ({got} for {n}); replace only "
                                 f"these from the code-built slots (skeleton plan_slots, slot order), every other field unchanged; draft kept")
                res["released"] += 1
        if not dry: cache[url] = fingerprint(url)   # after a release the spec changed: the page has left the parked set anyway
    if not dry:
        if base_new: json.dump(base, open(BASE, "w"), indent=1, sort_keys=True)
        os.makedirs(os.path.dirname(CACHE), exist_ok=True); json.dump(cache, open(CACHE, "w"), indent=1)
    line = (f"swap-recheck{' (dry)' if dry else ''}: {res['parked']} parked r18-swap-short pages; checked {res['checked']}, unchanged {res['unchanged']}; "
            f"releasable {res['releasable']}, released {res['released']}")
    print(line if quiet else line + ("\n" + "\n".join(f"  {k}: {v}" for k, v in sorted(res["pages"].items())) if res["pages"] else ""))
    return res

def hook(where):
    """For derive, aa and overnight next: never fails its caller."""
    try: return run(quiet=True)
    except BaseException as ex:   # SystemExit included (hubctl refusals)
        print(f"swap-recheck after {where} skipped: {type(ex).__name__}: {str(ex)[:200]}"); return None

def main(a):
    by = a[a.index("--by") + 1] if "--by" in a else None
    run(dry="--dry" in a, quiet="--quiet" in a, force="--force" in a, by=by)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
