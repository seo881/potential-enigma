"""Golden cases (LESSONS.md rule 3): every question, sentence or claim a human or the live audit rejected, which the gates missed.
The gate must catch each one. Cases point at a commit and a spec instead of copying text (no SERP or AlsoAsked text in new files).

    .venv/bin/python3 tests/golden/run.py          run all; exit 1 if a "guarded" case is no longer caught (regression)

Case kinds (tests/golden/cases.jsonl, one JSON object per line):
  gate-question  {url, sha, q_index, expect: [rule ids]}   the PAA gate rejects FAQ item q_index of the spec at that commit
  gate-question  {url, sha, q_index, absent: [rule ids]}   (absent instead of expect) item q_index carries none of these rules, at any level
  gate-text      {url, q, expect | absent, levels?}         (absent: none of these rules may fire, e.g. PA3 on a spelling variant)
  spelling-verbatim {q, orig, expect_ok}                  ruling 14: q is the original or its US-spelling/house-form display, nothing else
  gate-flag-decision {url, qh, from, subtype, expect}     Divit's flag packet: the question is rejected (expect reject) or no longer flagged for that subtype
  sq-filter      {url, q, expect_drop}                    Semrush question filter: drop reason (no_head|drop_class|brand|gate_reject|duplicate) or null = kept
  kw-variant     {a, b, expect_same}                      ruling 14: the K keyword checks treat a and b as the same keyword
  gate-text      {url, q, expect, levels?}                 the gate rejects this literal question with one of the expected rules
                                                          (levels ["reject","flag"]: a flag counts too; default reject only)
  qc-field       {url, field, text, expect, drop_key?, path?}  QC raises one of the expected codes when the field holds this text (or the spec
                                                          key drop_key is missing; or path, a list of keys into the spec, e.g. ["image_brief","tabs",0,"alt"], holds it)
  k7-header      {url, header, expect_k7}                 QC K7 fires on a why_table column header exactly when expect_k7 (top-10 URLs: keyword map + saved SERP)
  qc-code-text   {url, field, text, code, match?}         QC raises exactly `code` (message containing `match`) on that field for this text
  qc-text-clean  {url, field, text, check}                 QC must NOT raise `check` on that field for this text
  qc-text        {url, field, text, check}                 QC flags `field` when it holds `text` (P0/P1 on that field)
  gate-pa12-secs {url, expect_pa12}                        PA12's secondary test fails exactly when expected (ruling 5: Semrush secondaries, bar min(6, n); none = 4 on-topic workbook ideas)
  gate-pull-skip {url, qh, expect}                       ruling 12: the pull question with hash qh (Divit struck it) is rejected with an expected rule (PA4)
  review-lock    {url, field, expect_refused, sha?}       (sha: the spec at that commit, so a later review event cannot age the case)             ruling 10 B2: post-review change to a field is refused unless a blocking finding names it
  feasibility    {url, expect_feasible}                   ruling 10 B1: feasibility (pull + sources + recoverable keyword items) reaches 10 when expected
  aa-decision    {rows, saved, now, expect}               weekend.py aa: reuse a saved pull, refuse a recent charge with no save, ignore 401/403 rejections
  gate-asker     {url, q, expect_asker}                   PA6 classifies the question as builder | respondent (None = flag)
  qc-f2-aa       {url, aa, expect_f2}                     legacy-capture page with an item labelled alsoasked: F2 exactly when there is no AlsoAsked pull
  qc-f1          {url, aa, serp, expect_f1}               QC raises F1 exactly when the page has no AlsoAsked pull (DataForSEO capture irrelevant)
  audit-noflag   {url, code}                              the live audit does NOT raise `code` on a bare page (a settled non-issue)
  audit-link     {url, href, status_code, internal?, hub?, expect_finding}  A7-link raises a finding for this link status exactly when expected
  engine-brief   {url, path, value, expect: renders|brief-error, match?}  the image engine on the spec's brief with image_brief[path] = value
                                                          renders cleanly, or reports a BriefError issue (containing `match`); never crashes
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
        if c.get("absent"): return not any(r[0] in c["absent"] for r in it["reasons"])   # an exemption: the rule must stay silent
        rej = {r[0] for r in it["reasons"] if r[1] == "reject"}
        return it["verdict"] == "reject" and (not c.get("expect") or bool(rej & set(c["expect"])))
    if c["kind"] == "gate-text":   # a literal question (Divit's examples, our own copy): the gate's per-question rules reject it
        import paa_gate as PG
        rs = PG.Gate(c["url"]).judge({"q": c["q"], "source": "secondary", "n": 5}); lv = c.get("levels") or ["reject"]
        if c.get("absent"): return not any(r[0] in c["absent"] for r in rs)   # ruling 14: the rule must stay silent (a spelling variant)
        return bool({r[0] for r in rs if r[1] in lv} & set(c.get("expect") or [r[0] for r in rs]))
    if c["kind"] == "gate-pull-skip":   # ruling 12: a question Divit struck (stored as its hash) stays rejected PA4 on that page's pull
        import paa_gate as PG, io as _io, contextlib as _cl
        g = PG.Gate(c["url"])
        if not PG.pulls(g.slug): return False
        with _cl.redirect_stdout(_io.StringIO()): items, _ = PG.run_pull(g)
        it = next((i for i in items if PG.qhash(i["q"]) == c["qh"]), None)
        return bool(it) and it["verdict"] == "reject" and any(r[0] in c["expect"] and r[1] == "reject" for r in it["reasons"])
    if c["kind"] == "review-lock":   # ruling 10 B2: after review, a change to field F is refused unless a blocking finding names F
        import review_lock as RL, hubctl as H
        s = copy.deepcopy(spec_at(c["sha"], c["url"]) if c.get("sha") else json.load(open(H.spath(c["url"])))); s["fields"][c["field"]] = (s["fields"].get(c["field"]) or "") + " Changed after review."
        return bool(RL.violations(s)) == c["expect_refused"]
    if c["kind"] == "feasibility":   # ruling 10 B1: the pre-writing feasibility count reaches 10 exactly when expected
        import park_rescue as R
        return R.feasibility(c["url"])["feasible"] == c["expect_feasible"]
    if c["kind"] == "aa-decision":  # weekend.py aa no-double-charge rule (Divit 2026-10-13): rows + saved status -> reuse/refuse/pull
        import weekend as W
        return W.aa_decision(c["rows"], c.get("saved"), c["now"])[0] == c["expect"]
    if c["kind"] == "gate-asker":   # PA6 asker class of a literal question (ruling 4: fix the patterns, never reword the question)
        import paa_gate as PG
        return PG.Gate(c["url"]).asker(PG.norm(c["q"])) == c["expect_asker"]
    if c["kind"] == "qc-field":    # a literal field value: QC raises the expected code on that field
        import qc_hub as Q, hubctl as H, glob as _g
        s = copy.deepcopy(json.load(open(H.spath(c["url"]))))
        if c.get("drop_key"): s.pop(c["drop_key"], None)   # a spec-level key that is missing (e.g. chip_adds)
        elif c.get("path"):                                  # a nested spec value (image alt text, image brief)
            o = s
            for k in c["path"][:-1]: o = o[k]
            o[c["path"][-1]] = c["text"]
        else: s["fields"][c["field"]] = c["text"]
        every = Q.load_specs(sorted(_g.glob(os.path.join(ROOT, "specs", "*", "*.json"))))
        return any(i["code"] in c["expect"] and i["sev"] in ("P0", "P1") for i in Q.check(s, every))
    if c["kind"] == "k7-header":   # K7 on one comparison-table column header (multi-word brands: Divit 2026-10-12)
        import qc_hub as Q, hubctl as H, re as _re
        s = copy.deepcopy(json.load(open(H.spath(c["url"]))))
        s["fields"]["why_table"] = _re.sub(r'<th scope="col">[^<]+</th>', '<th scope="col">' + c["header"] + '</th>', s["fields"].get("why_table", ""), count=1)
        hit = any(i["code"] == "K7" and ('"' + c["header"] + '"') in i["msg"] for i in Q.check(s, Q.load_specs([H.spath(c["url"])])))
        return hit == c["expect_k7"]
    if c["kind"] == "audit-noflag":   # the live audit must NOT raise this code on a page that lacks the thing (a settled non-issue)
        import live_audit as LA
        m = {"pages": [{"url": c["url"], "hub": "/" + c["url"].split("/")[1], "fields": {}, "faq_items": [], "images": {}, "meta_title": "x" * 40, "meta_description": "y" * 120}]}
        raw = {"pages": [{"url": c["url"], "checks": {"http200": True}, "verify": {}, "render": {"http": 200, "jsonld": ['{"@context": "https://schema.org", "@type": "Organization", "name": "Emergent"}'], "links": [], "images": [], "text_visible": "", "text_all": "", "h1s": ["h"]}}], "hubs": [], "held": []}
        return not any(f["code"] == c["code"] for f in LA.evaluate(raw, m, "https://emergent.sh"))
    if c["kind"] == "audit-link":     # A7-link on one link status (page or hub): a finding exactly when expect_finding says so
        import live_audit as LA
        ls = {c["href"]: {"internal": c.get("internal", False), "status": c["status_code"]}}
        if c.get("hub"):
            raw = {"pages": [], "held": [], "hubs": [{"hub": c["url"], "http200": True, "carousel_hidden": True, "render": {"text_visible": ""}, "link_status": ls}]}
            m = {"pages": []}
        else:
            m = {"pages": [{"url": c["url"], "hub": "/" + c["url"].split("/")[1], "fields": {}, "faq_items": [], "images": {}, "meta_title": "x" * 40, "meta_description": "y" * 120}]}
            raw = {"pages": [{"url": c["url"], "checks": {"http200": True}, "verify": {}, "link_status": ls, "render": {"http": 200, "jsonld": [], "links": [], "images": [], "text_visible": "", "text_all": "", "h1s": ["h"]}}], "hubs": [], "held": []}
        hit = any(f["code"] == "A7-link" for f in LA.evaluate(raw, m, "https://emergent.sh"))
        return hit == c["expect_finding"]
    if c["kind"] == "audit-sev":      # one failed verify check (page) or a shown carousel (hub) raises code at severity
        import live_audit as LA
        if c.get("hub"):
            raw = {"pages": [], "held": [], "hubs": [{"hub": c["url"], "http200": True, "carousel_hidden": False, "carousel_has_all_new_cards": True, "hub_card_cover_alt": True, "missing": [], "cover_alt_missing": [], "render": {"text_visible": ""}, "link_status": {}}]}
            m = {"pages": []}
        else:
            m = {"pages": [{"url": c["url"], "hub": "/" + c["url"].split("/")[1], "fields": {}, "faq_items": [], "images": {}, "meta_title": "x" * 40, "meta_description": "y" * 120}]}
            raw = {"pages": [{"url": c["url"], "checks": {"http200": True, c["check"]: False}, "verify": {}, "link_status": {}, "render": {"http": 200, "jsonld": [], "links": [], "images": [], "text_visible": "", "text_all": "", "h1s": ["h"]}}], "hubs": [], "held": []}
        return any(f["code"] == c["code"] and f["severity"] == c["severity"] for f in LA.evaluate(raw, m, "https://emergent.sh"))
    if c["kind"] == "engine-brief":   # the image engine on a spec's brief with one value set: renders, or a BriefError issue; never a crash
        sys.path.insert(0, os.path.join(ROOT, "pipeline")); import engine as E, hubctl as H
        s = copy.deepcopy(json.load(open(H.spath(c["url"])))); o = s["image_brief"]
        for k in c["path"][:-1]: o = o[k]
        o[c["path"][-1]] = c["value"]
        try: _, issues, _ = E.build_all(s)
        except Exception: return False
        return (not issues) if c["expect"] == "renders" else any(c.get("match", "") in i for i in issues)
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
    if c["kind"] == "qc-f2-aa":    # legacy-capture page, FAQ item 3 labelled alsoasked (Divit 2026-10-13): F2 only when there is no pull
        import qc_hub as Q, hubctl as H, paa_gate as PG
        sys.path.insert(0, os.path.join(ROOT, "plan")); import serp as S
        s = json.load(open(H.spath(c["url"]))); s["status"] = "qc_pass"
        x = next(x for x in s.get("faq_sources", []) if x.get("source") != "definition"); x["source"], x["ref"] = "alsoasked", x.get("q")
        real_pp, real_load = PG.pull_path, S.load
        stub = os.path.join(ROOT, ".cache", "golden-aa-stub.json"); os.makedirs(os.path.dirname(stub), exist_ok=True)
        json.dump({"_meta": {"fetched": "2026-10-10"}, "response": {}}, open(stub, "w"))
        PG.pull_path = lambda slug: stub if c["aa"] else os.path.join(ROOT, ".cache", "golden-no-such-pull.json")
        S.load = lambda url: real_load(url) or {"paa": [], "related": [], "keywords": [], "organic": [], "features": [], "fetched": "2026-10-01"}
        try: hit = any(i["code"] == "F2" and "alsoasked" in i.get("msg", i.get("message", "")) for i in Q.check(s, Q.load_specs([H.spath(c["url"])])))
        finally: PG.pull_path, S.load = real_pp, real_load
        return hit == c["expect_f2"]
    if c["kind"] == "gate-pa12-secs":   # PA12 secondaries bar = min(6, the page's Semrush workbook secondaries) (Divit 2026-10-13)
        import paa_gate as PG, io, contextlib
        with contextlib.redirect_stdout(io.StringIO()): _items, page = PG.run_spec(PG.Gate(c["url"]))
        return any(r == "PA12" and "secondar" in m for r, m in page) == c["expect_pa12"]
    if c["kind"] == "spelling-verbatim":   # ruling 14: US-spelling/house-form display of a verbatim question is ok; any other change is not
        import spelling as SP
        return SP.verbatim_ok(c["q"], c["orig"]) == c["expect_ok"]
    if c["kind"] == "kw-variant":          # ruling 14: the K checks read a UK spelling as the keyword's US spelling
        import qc_hub as Q
        return (Q.kw_bag(c["a"]) == Q.kw_bag(c["b"])) == c["expect_same"]
    if c["kind"] == "gate-flag-decision":  # Divit's packet: a decided flag subtype/question is a reject (rejected) or no longer that flag (approved)
        import paa_gate as PG, semrush_questions as SQ, io as _io, contextlib as _cl
        g = PG.Gate(c["url"]); qs = []
        if c.get("from") == "semrush": qs = [x["q"] for x in SQ.usable(g.slug)]
        elif PG.pulls(g.slug):
            with _cl.redirect_stdout(_io.StringIO()): qs = [i["q"] for i in PG.run_pull(g)[0]]
        q = next((x for x in qs if PG.qhash(x) == c["qh"]), None)
        if q is None: return False
        rs = g.judge({"q": q, "source": "keyword" if c.get("from") == "semrush" else "alsoasked", "n": 5})
        if c["expect"] == "reject": return any(r[1] == "reject" for r in rs)
        return not any(r[1] == "flag" and PG.flag_subtype(r[0], r[2]) == c["subtype"] for r in rs)
    if c["kind"] == "sq-filter":           # Semrush phrase_questions filter (Divit 2026-10-13): dropped for the expected reason, or kept (None)
        import semrush_questions as SQ
        return SQ.keep_reason(c["url"], c["q"]) == c.get("expect_drop")
    if c["kind"] == "qc-code-text":        # QC raises exactly `code` on `field` when it holds `text` (canary 2026-10-14: R15 brand + moat)
        import qc_hub as Q, hubctl as H
        s = copy.deepcopy(json.load(open(H.spath(c["url"])))); s["fields"][c["field"]] = c["text"]
        return any(i["code"] == c["code"] and i["sev"] in ("P0", "P1") and c.get("match", "") in i["msg"] for i in Q.check(s, Q.load_specs([H.spath(c["url"])])))
    if c["kind"] == "qc-text-clean":       # the check must NOT flag this text (Divit 2026-10-14: C2 flags compliance claims, not a bare acronym)
        import qc_hub as Q, hubctl as H
        s = copy.deepcopy(json.load(open(H.spath(c["url"])))); s["fields"][c["field"]] = c["text"]
        return not any(i["code"] == c["check"] and i["sev"] in ("P0", "P1") and (i["field"] or "").startswith(c["field"]) for i in Q.check(s, Q.load_specs([H.spath(c["url"])])))
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
