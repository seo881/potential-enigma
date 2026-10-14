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
  gate-r18       {url, sha, q_index, expect | absent, new_writing?}  ruling 18: FAQ item q_index of the spec at sha judged as NEW writing
                                                          rejects with an expected rule (absent: none of these rejects); new_writing false =
                                                          the reviewed page as it is (ruling 15: the r18 checks never re-gate it)
  gate-pool      {url, from: pull|semrush, qh, expect | absent}  ruling 18: a pool candidate (by hash) rejects with an expected rule, or not
  feas-skeleton  {url, expect_feasible}                   ruling 18 part 5: feasibility total == skeleton.slots_possible, feasible as expected
  acronym-case   {raw, expect}                            ruling 18 part 4e: skeleton.clean_question cases acronyms (plurals too)
  skel-admit     {url, qh, expect_admitted}               Divit 2026-10-14 step 4: skeleton.candidates admits the question (hash of its text or
                                                          source wording) exactly when expected (the gate's spec checks, answer source included)
  swap-recheck   {url, sha, note, expect_need, inject?, expect_filled?}  step 3: positions to swap for the spec at sha (note lead clause +
                                                          gate rejects); inject dropped|synthetic: replacements counted from those slots
  qc-r18         {url, sha, match, expect, keep_review?}  ruling 18 in QC R15: the spec at sha as new writing raises R15 `match` exactly when expected
  webflow-api    {test, ...}                              Divit 2026-10-14, ops/webflow_api.py + hubctl api-*: test refuse {method, path, body?,
                                                          query?, expect_refused} ({child} = a child collection id), dry-no-network, batching
                                                          {op, n, expect: sizes}, slug-skip {cands, live, limit?, expect_create, expect_skip},
                                                          create-cmd-skip, live-before-gate, before-gate {path, expect_ok}, backoff
                                                          {statuses, retry_after, expect_ok, expect_sleeps}, no-token
  quiz-qc        {fixture, set?, primary?, expect | clean, sev?}  playable quiz (Divit 2026-10-14 step 5, qc/quiz.py): the fixture in
                                                          ops/quiz/fixtures with `set` applied ([[path, value]], value "__delete__" removes)
                                                          raises a P0/P1 with one of `expect` (sev: that severity), or none of `clean`
  quiz-js        {fixture, set?, answers?, expect_valid, expect_key?, expect_points?}  the shipped embed's own JS (ops/quiz/logic.mjs on
                                                          embed.min.html): validates (or refuses) the quiz and maps the answers to the result
  quiz-agree     {fixture, set}                           the embed's runtime validation and QC agree: JS refuses exactly when QC has a P0 in Z1-Z3
  quiz-carrier   {test, ...}                              the carrier (alpb---prompt, Divit's conditions): noquiz-identical (every SurveyQuiz
                                                          spec without a quiz exports byte for byte as with no carrier), with-quiz {url, fixture}
                                                          (hero <p> and awbPrompt unchanged, one separate quiz block, Z9 clean), z9-wrong-quiz,
                                                          z9-no-carrier, verify-live {mutate: none|quiz|prompt|no-embed|no-quiz, expect_fail: [checks]},
                                                          ship-block {url, quiz, expect_blocked}, css-scope {inject?, expect_bad}, plan-type {primary, expect}
  verify-links   {fixture, page, fetch?, default?, mutate?, expect_fail, expect_bad?}  Divit 2026-10-14: verify-live checks every
                                                          internal href (template links too) on the saved page HTML in
                                                          tests/golden/fixtures/verify_live/<fixture>.html.gz (mutate: [[old, new]],
                                                          each must occur); offline: fetch {path: status | [status, location]}
                                                          answers each request, default (200) the rest; the page fails exactly
                                                          when expect_fail, and every href in expect_bad is among the failing ones
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
        return not any(r[1] == "flag" and PG.flag_subtype(r[0], r[2], q) == c["subtype"] for r in rs)
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
    if c["kind"] == "gate-r18":            # ruling 18 parts 4-5: FAQ item q_index of the spec at sha, judged as NEW writing (or as the
        import paa_gate as PG, io as _io, contextlib as _cl   # reviewed page it is, new_writing false: ruling 15, never re-gated)
        g = PG.Gate(c["url"]); g.spec = spec_at(c["sha"], c["url"]); g.new_writing = c.get("new_writing", True)
        with _cl.redirect_stdout(_io.StringIO()): items, _ = PG.run_spec(g)
        it = items[c["q_index"] - 1]
        if c.get("absent"): return not any(r[0] in c["absent"] for r in it["reasons"] if r[1] == "reject")
        return any(r[0] in c["expect"] and r[1] == "reject" for r in it["reasons"])
    if c["kind"] == "gate-pool":           # ruling 18: a candidate in the page's pool (AlsoAsked pull or Semrush usable, by qh) is rejected or not
        import paa_gate as PG, semrush_questions as SQ, io as _io, contextlib as _cl
        g = PG.Gate(c["url"])
        if c["from"] == "semrush":
            q = next((x["q"] for x in SQ.usable(g.slug) if PG.qhash(x["q"]) == c["qh"]), None)
            if q is None:   # a later re-derive may drop the question from the usable list (e.g. by the very rule under test): judge the raw cached row
                import os as _os
                for p_ in SQ.phrases(c["url"]):
                    if _os.path.exists(SQ.raw_path(p_)):
                        q = next((r["keyword"] for r in json.load(open(SQ.raw_path(p_)))["rows"] if PG.qhash(r["keyword"]) == c["qh"]), None) or q
            rs = g.judge({"q": q, "source": "keyword", "n": 5}) if q else None
        else:
            with _cl.redirect_stdout(_io.StringIO()): items = PG.run_pull(g)[0] if PG.pulls(g.slug) else []
            rs = next((i["reasons"] for i in items if PG.qhash(i["q"]) == c["qh"]), None)
        if rs is None: return False
        if c.get("absent"): return not any(r[0] in c["absent"] and r[1] == "reject" for r in rs)
        return any(r[0] in c["expect"] and r[1] == "reject" for r in rs)
    if c["kind"] == "feas-skeleton":       # ruling 18 part 5: feasibility is the skeleton's own slot count (overnight 2026-10-14: 10 vs 7)
        import park_rescue as R, skeleton as SK, io as _io, contextlib as _cl
        with _cl.redirect_stdout(_io.StringIO()): f = R.feasibility(c["url"], draft=False); n = SK.slots_possible(c["url"])   # draft=False: stable once claimed
        return f["total"] == n and f["feasible"] == c["expect_feasible"]
    if c["kind"] == "skel-admit":          # Divit 2026-10-14 step 4: the skeleton admits a candidate (by hash) exactly when the gate's
        import skeleton as SK, paa_gate as PG   # spec checks (answer source PA4/PA5 included) will pass it in the FAQ
        cs = SK.quiet(SK.candidates, c["url"])
        return any(c["qh"] in (PG.qhash(x["q"]), PG.qhash(x["ref"])) for x in cs) == c["expect_admitted"]
    if c["kind"] == "swap-recheck":        # Divit 2026-10-14 step 3: the r18-swap-short re-check on the spec at sha (dry, no writes)
        import swap_recheck as W, paa_gate as PG, hubctl as H
        s = spec_at(c["sha"], c["url"]); need, items = W.gate_needs(c["url"], s); need |= W.listed(c["note"])
        if sorted(need) != c["expect_need"]: return False
        if "inject" not in c: return True
        prim = H.kmap()[c["url"]]["primary"]; d = [{"kind": "definition", "q": f"What is {prim}?"}, {"kind": "definition", "q": f"How do I set up {prim}?"}]
        if c["inject"] == "dropped":       # the page's own dropped questions offered as replacements: never counted
            sl = d + [{"kind": "alsoasked", "q": i["q"], "ref": i["q"]} for i in items if i["n"] in need]
        else:                              # code-made questions on the page's head phrase, unlike any on the page: counted
            sl = d + [{"kind": "semrush", "q": x, "ref": x} for x in (f"Which approvals should a {prim} route to a second reviewer?",
                                                                       f"How many fields can a {prim} hold before people abandon it?")]
        return W.available(c["url"], need, items, sl, spec=s)[0] == c["expect_filled"]
    if c["kind"] == "acronym-case":        # ruling 18 part 4e: keyword-sourced questions case known acronyms, plurals too
        import skeleton as SK
        return SK.clean_question(c["raw"]) == c["expect"]
    if c["kind"] == "qc-r18":              # ruling 18 part 4 in QC R15: the spec at sha as NEW writing (review set aside) raises R15
        import qc_hub as Q, hubctl as H    # with `match` exactly when expected; keep_review: the reviewed page is never re-checked
        s = copy.deepcopy(spec_at(c["sha"], c["url"])); s["_path"] = H.spath(c["url"])
        if not c.get("keep_review"): s.pop("review", None)
        hit = any(i["code"] == "R15" and i["sev"] in ("P0", "P1") and c["match"] in i["msg"] for i in Q.check(s, Q.load_specs([H.spath(c["url"])])))
        return hit == c["expect"]
    if c["kind"] == "webflow-api":         # Divit 2026-10-14: the direct Data API path (allowlist, slug skip, batching, before gate,
        import ship                        # 429 backoff, no token in any output); dry run and stubs only, never the network
        return ship.api_golden(c)
    if c["kind"] in ("quiz-qc", "quiz-js", "quiz-agree", "quiz-carrier"):
        return quiz_case(c)
    if c["kind"] == "verify-links":        # Divit 2026-10-14: every internal href on the page; the HTTP layer is stubbed (offline)
        import verify_live as V, gzip
        html = gzip.open(os.path.join(ROOT, "tests", "golden", "fixtures", "verify_live", c["fixture"] + ".html.gz")).read().decode("utf-8")
        for old, new in c.get("mutate") or []:
            if old not in html: return False
            html = html.replace(old, new, 1)
        table, seen = c.get("fetch") or {}, []
        def fetch(url, method):
            from urllib.parse import urlsplit
            seen.append(url); r = table.get(urlsplit(url).path, c.get("default", 200))
            return (r[0], r[1]) if isinstance(r, list) else (r, None)
        ok, rep, bad = V.check_internal_links(html, "https://emergent.sh" + c["page"], fetch=fetch)
        return (not ok) == c["expect_fail"] and set(c.get("expect_bad") or []) <= set(bad) and len(seen) > 0
    if c["kind"] == "qc-text":
        import qc_hub as Q, hubctl as H
        s = json.load(open(H.spath(c["url"]))); s = copy.deepcopy(s); f = c["field"]
        if f in s["fields"]: s["fields"][f] = c["text"]
        every = [x for x in Q.load_specs([H.spath(c["url"])])]
        return any(i["sev"] in ("P0", "P1") and (i["field"] or "").startswith(f) for i in Q.check(s, every))
    return None

def _quiz_fixture(c):
    q = json.load(open(os.path.join(ROOT, "ops", "quiz", "fixtures", c["fixture"] + ".json")))
    for path, val in c.get("set") or []:
        o = q
        for k in path[:-1]: o = o[k]
        if val == "__delete__": del o[path[-1]]
        else: o[path[-1]] = val
    return q

def _quiz_js(q, answers=None, cid="x"):
    p = os.path.join(ROOT, ".cache", "quiz", f"golden-{cid}.json"); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump({"quiz": q, "answers": answers}, open(p, "w"))
    r = subprocess.run(["node", os.path.join(ROOT, "ops", "quiz", "logic.mjs"), p], capture_output=True, text=True, cwd=ROOT)
    return json.loads(r.stdout)

QUIZ_HERO = "/ai-survey-and-quiz-builder/employee-engagement-survey"   # a real SurveyQuiz spec with chip_adds, used as a quiz page's body
def _quiz_spec(fixture="knowledge", url="/ai-survey-and-quiz-builder/vocabulary-quiz"):
    import hubctl as H
    s = copy.deepcopy(json.load(open(H.spath(QUIZ_HERO)))); s["url"] = url; s["status"] = "spec"
    s["quiz"] = json.load(open(os.path.join(ROOT, "ops", "quiz", "fixtures", fixture + ".json"))); return s

def _live_html(spec):
    """A page as Webflow renders the item: the hero prompt rich text (embed blocks become w-embed divs), the template's hero-chips
    script (its comment mentions window.awbPrompt) and the quiz embed (its comment mentions window.awbQuiz)."""
    import hubctl as H
    v = H.export_fields(spec["url"], spec, live=set())[0]["hero_prompt"].replace("<div data-rt-embed-type='true'>", '<div class="w-embed w-script">')
    tpl = open(os.path.join(ROOT, "ops", "template", "hero-chips.html")).read()
    emb = open(os.path.join(ROOT, "ops", "quiz", "embed.html")).read()
    return f"<html><body><form id='hero-prompt-form'><textarea></textarea></form>{tpl}<div class=\"w-embed\">{emb}</div><div class=\"w-richtext\">{v}</div></body></html>"

def quiz_case(c):
    import quiz as Z
    if c["kind"] == "quiz-qc":
        iss = Z.check(_quiz_fixture(c), c.get("primary", ""))
        hit = lambda codes: [i for i in iss if i["code"] in codes and i["sev"] in ((c["sev"],) if c.get("sev") else ("P0", "P1"))]
        return bool(hit(c["expect"])) if c.get("expect") else not hit(c["clean"])
    if c["kind"] == "quiz-js":
        r = _quiz_js(_quiz_fixture(c), c.get("answers"), c["id"])
        if (r["error"] == "") != c["expect_valid"]: return False
        if c.get("expect_key") and (r["result"] or {}).get("key") != c["expect_key"]: return False
        if c.get("expect_points") is not None and (r["result"] or {}).get("points") != c["expect_points"]: return False
        if c.get("answers") and c["expect_valid"]:   # the Python mirror (QC reachability) scores the same
            k, pts = Z.score(_quiz_fixture(c), c["answers"])
            if (k, pts) != (r["result"]["key"], r["result"]["points"]): return False
        return True
    if c["kind"] == "quiz-agree":
        q = _quiz_fixture(c); js_ok = _quiz_js(q, None, c["id"])["error"] == ""
        py_ok = not any(i["sev"] == "P0" and i["code"] in ("Z1", "Z2", "Z3") for i in Z.check(q, ""))
        return js_ok == py_ok
    import hubctl as H, glob as _g
    t = c["test"]
    if t == "noquiz-identical":   # Divit's condition 2: pages without spec.quiz export exactly as before the carrier existed
        hub = H.CFG["hubs"]["SurveyQuiz"]; saved = hub.get("quiz_carrier"); n = 0
        try:
            for p in sorted(_g.glob(os.path.join(ROOT, "specs", "sqb", "*.json"))):
                s = json.load(open(p))
                if s.get("quiz") is not None: continue
                hub["quiz_carrier"] = saved; a = H.export_fields(s["url"], s, live=set())[0]
                hub["quiz_carrier"] = None; b = H.export_fields(s["url"], s, live=set())[0]
                if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True): return False
                n += 1
        finally: hub["quiz_carrier"] = saved
        return n >= c.get("min_pages", 1) and saved is not None
    if t == "with-quiz":
        s = _quiz_spec(c.get("fixture", "knowledge")); bare = copy.deepcopy(s); bare.pop("quiz")
        a = Z.split_prompt(H.export_fields(s["url"], s, live=set())[0]["hero_prompt"]); b = Z.split_prompt(H.export_fields(s["url"], bare, live=set())[0]["hero_prompt"])
        return a["p"] == b["p"] and a["prompt"] == b["prompt"] and a["prompt"] is not None and a["quiz"] == s["quiz"] and a["blocks"] == b["blocks"] + 1 and not Z.carrier_problems(s)
    if t == "z9-wrong-quiz":
        s = _quiz_spec(); real = Z.embed_block
        Z.embed_block = lambda q: real(dict(q, title="Another quiz"))
        try: return any("does not decode" in m for _, m in Z.carrier_problems(s))
        finally: Z.embed_block = real
    if t == "z9-no-carrier":
        hub = H.CFG["hubs"]["SurveyQuiz"]; saved = hub.get("quiz_carrier"); hub["quiz_carrier"] = None
        try: return any("no quiz carrier" in m for _, m in Z.carrier_problems(_quiz_spec()))
        finally: hub["quiz_carrier"] = saved
    if t == "verify-live":
        import verify_live as V
        s = _quiz_spec(c.get("fixture", "knowledge")); html = _live_html(s); m = c.get("mutate", "none")
        if m == "quiz": html = html.replace('"title":"How Well', '"title":"How Badly', 1)
        if m == "prompt": html = html.replace("window.awbPrompt = {\"default\": \"Build", "window.awbPrompt = {\"default\": \"Make", 1)
        if m == "no-embed": html = html.replace('class="emgq-mount"', 'class="other"')
        if m == "no-quiz": html = re.sub(r"<div class=\"w-embed w-script\"><script id='awb-quiz-data'>.*?</script></div>", "", html, flags=re.S)
        _ok, rep = V.verify(s, html=html, check_links=False)
        names = ("hero prompt data (awbPrompt) with the quiz block", "hero prompt text", "quiz data", "quiz embed")
        failed = {n for n in names if any(l.startswith("FAIL " + n) for l in rep)}
        passed = {n for n in names if any(l.startswith("PASS " + n) for l in rep)}
        return failed == set(c.get("expect_fail") or []) and passed | failed == set(names)
    if t == "ship-block":
        s = json.load(open(H.spath(QUIZ_HERO))) if not c.get("quiz") else _quiz_spec()
        return bool(H.quiz_ship_block(c["url"], s)) == c["expect_blocked"]
    if t == "css-scope":
        sys.path.insert(0, os.path.join(ROOT, "ops", "quiz")); import build as QB
        html = open(os.path.join(ROOT, "ops", "quiz", "embed.html")).read()
        if c.get("inject"): html = html.replace("</style>", c["inject"] + "\n</style>", 1)
        return bool(QB.bad_selectors(html)) == c["expect_bad"]
    if t == "plan-type":
        import skeleton as SK
        return SK.quiz_plan("/ai-survey-and-quiz-builder/x-quiz", c["primary"])["type"] == c["expect"]
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
