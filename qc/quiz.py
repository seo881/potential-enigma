"""quiz.py: the playable quiz (Divit 2026-10-14, day step 5; docs/QUIZ.md, rules/quiz.json).

One module for everything Python knows about spec.quiz: which pages are quiz pages, the QC checks (codes Z0-Z8, called from
qc/qc_hub.py), the scoring rule (mirrors the embed's JavaScript, ops/quiz/embed.html), exact result reachability, and the
export block that carries the quiz into the CMS: its own rich-text embed block <script id='awb-quiz-data'> window.awbQuiz = {...};
</script>, appended after the hero prompt's awbPrompt block in alpb---prompt (Divit 2026-10-14: carrier approved, conditions in
docs/QUIZ.md), and the parsers that read that field back (split_prompt) so every check still sees the hero prompt exactly.

    python3 qc/quiz.py check FILE.json [--primary "vocabulary quiz"]   QC one quiz JSON on its own (Z codes)
    python3 qc/quiz.py block FILE.json                                 print the CMS embed block the exporter appends

Severity: anything the embed's runtime validation rejects (it renders nothing, fail closed) is P0 (Z1, Z2), as is a diagnosis
claim (Z5). Content rules (lengths, sources, reachability, hygiene, franchises) are P1. Advisory checks are P2.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(ROOT, "rules", "quiz.json")))
_C = R["diagnosis"]["conditions"]
DIAG = [re.compile(p.replace("{C}", _C), re.I) for p in R["diagnosis"]["patterns"]]
FACT = re.compile(R["fact_rx"], re.I)
KEY_RX = re.compile(R["result_key_rx"])

def is_quiz_page(spec_or_url):
    """SurveyQuiz pages whose slug contains 'quiz' (Divit 2026-10-14 step 5)."""
    url = spec_or_url if isinstance(spec_or_url, str) else (spec_or_url.get("url") or "")
    return url.startswith("/ai-survey-and-quiz-builder/") and "quiz" in url.rsplit("/", 1)[-1]

def _s(x): return isinstance(x, str) and x.strip() != ""
def _int(x): return isinstance(x, int) and not isinstance(x, bool)

# ---------------------------------------------------------------- scoring (mirrors emgqScore in ops/quiz/embed.html)
def score(quiz, answers):
    """answers: one option index per question. -> (result key, points). Knowledge: points = correct answers, the result is the band
    holding it. Matching: one point per chosen option to its result; the most points wins, ties go to the result listed first."""
    Q, Rs = quiz["questions"], quiz["results"]
    if quiz["type"] == "knowledge":
        pts = sum(1 for q, a in zip(Q, answers) if 0 <= a < len(q["options"]) and q["options"][a].get("correct") is True)
        return next((r["key"] for r in Rs if r["min"] <= pts <= r["max"]), None), pts
    tally = {}
    for q, a in zip(Q, answers):
        if 0 <= a < len(q["options"]): k = q["options"][a].get("result"); tally[k] = tally.get(k, 0) + 1
    best = None
    for r in Rs:
        if best is None or tally.get(r["key"], 0) > tally.get(best, 0): best = r["key"]
    return best, tally.get(best, 0)

def best_path(quiz, key):
    """Matching: answers that make `key` win if any exist (exact: capacity assignment of the other questions), else None.
    Knowledge: answers scoring the band's minimum."""
    Q, Rs = quiz["questions"], quiz["results"]
    if quiz["type"] == "knowledge":
        r = next(r for r in Rs if r["key"] == key); need = r["min"]; out = []
        for q in Q:
            ci = next(i for i, o in enumerate(q["options"]) if o.get("correct") is True)
            wi = next((i for i, o in enumerate(q["options"]) if o.get("correct") is not True), ci)
            out.append(ci if need > 0 else wi); need -= 1 if need > 0 else 0
        return out
    order = [r["key"] for r in Rs]; pos = order.index(key)
    mine = [next((i for i, o in enumerate(q["options"]) if o.get("result") == key), None) for q in Q]
    s = sum(1 for m in mine if m is not None)
    if s == 0: return None
    cap = {k: (s - 1 if order.index(k) < pos else s) for k in order if k != key}
    rest = [qi for qi, m in enumerate(mine) if m is None]
    # bipartite b-matching by augmenting paths: question -> option result with capacity cap[result]
    assign = {}; load = {k: [] for k in cap}
    def try_q(qi, seen):
        for oi, o in enumerate(Q[qi]["options"]):
            k = o.get("result")
            if k not in cap or k in seen: continue
            seen.add(k)
            if len(load[k]) < cap[k]: load[k].append(qi); assign[qi] = oi; return True
            for other in list(load[k]):
                if try_q(other, seen):
                    load[k].remove(other); load[k].append(qi); assign[qi] = oi; return True
        return False
    for qi in rest:
        if not try_q(qi, set()): return None
    return [mine[qi] if mine[qi] is not None else assign[qi] for qi in range(len(Q))]

# ---------------------------------------------------------------- texts
def texts(quiz):
    """[(label, text)] for every visitor-facing string in the quiz."""
    out = [("quiz.title", quiz.get("title")), ("quiz.intro", quiz.get("intro"))]
    for i, q in enumerate(quiz.get("questions") or [], 1):
        if not isinstance(q, dict): continue
        out.append((f"quiz.q{i}.text", q.get("text"))); out.append((f"quiz.q{i}.explanation", q.get("explanation")))
        for j, o in enumerate(q.get("options") or [], 1):
            if isinstance(o, dict): out.append((f"quiz.q{i}.option{j}", o.get("text")))
    for i, r in enumerate(quiz.get("results") or [], 1):
        if isinstance(r, dict): out += [(f"quiz.result{i}.title", r.get("title")), (f"quiz.result{i}.description", r.get("description"))]
    return [(k, v) for k, v in out if isinstance(v, str)]

# ---------------------------------------------------------------- QC
def check(quiz, primary="", link_cache=None, today=None):
    """-> [{sev, code, field, msg}]. link_cache: guards.link_cache() for Z4 liveness (None skips it)."""
    I = []
    def add(sev, code, field, msg): I.append({"sev": sev, "code": code, "field": field, "msg": msg})
    if not isinstance(quiz, dict): add("P0", "Z1", "quiz", "spec.quiz must be a JSON object (docs/QUIZ.md)"); return I
    K = R["keys"]; L = R["lengths"]; (qmin, qmax), (omin, omax), (rmin, rmax) = R["counts"]["questions"], R["counts"]["options"], R["counts"]["results"]
    for k in quiz:
        if k not in K["quiz"]: add("P1", "Z1", "quiz", f'unknown key "{k}" (allowed: {", ".join(K["quiz"])})')
    if quiz.get("version") != 1: add("P0", "Z1", "quiz.version", "version must be 1")
    typ = quiz.get("type")
    if typ not in R["types"]: add("P0", "Z1", "quiz.type", f'type must be "knowledge" or "matching", not {typ!r}'); return I
    if not _s(quiz.get("title")): add("P0", "Z1", "quiz.title", "title missing")
    if "intro" in quiz and not isinstance(quiz["intro"], str): add("P0", "Z1", "quiz.intro", "intro must be text")
    Q, Rs = quiz.get("questions"), quiz.get("results")
    if not isinstance(Q, list): add("P0", "Z1", "quiz.questions", "questions must be a list"); return I
    if not isinstance(Rs, list): add("P0", "Z1", "quiz.results", "results must be a list"); return I
    if not qmin <= len(Q) <= qmax: add("P0", "Z2", "quiz.questions", f"{len(Q)} questions ({qmin}-{qmax})")
    if not rmin <= len(Rs) <= rmax: add("P0", "Z2", "quiz.results", f"{len(Rs)} results ({rmin}-{rmax})")
    rk = "result_knowledge" if typ == "knowledge" else "result_matching"
    keys = []
    for i, r in enumerate(Rs, 1):
        f = f"quiz.result{i}"
        if not isinstance(r, dict): add("P0", "Z1", f, "each result is an object {key, title, description" + (", min, max}" if typ == "knowledge" else "}")); continue
        for k in r:
            if k not in K[rk]: add("P1", "Z1", f, f'unknown key "{k}" for a {typ} result (allowed: {", ".join(K[rk])})')
        if not _s(r.get("key")): add("P0", "Z1", f, "key missing")
        elif not KEY_RX.match(r["key"]): add("P1", "Z1", f, f'key "{r["key"]}": lowercase letters, digits and hyphens, at most 24')
        if r.get("key") in keys: add("P0", "Z1", f, f'duplicate result key "{r.get("key")}"')
        keys.append(r.get("key"))
        if not _s(r.get("title")): add("P0", "Z1", f + ".title", "title missing")
        if not _s(r.get("description")): add("P0", "Z1", f + ".description", "description missing")
        if typ == "knowledge" and not (_int(r.get("min")) and _int(r.get("max"))): add("P0", "Z1", f, "a knowledge result needs whole-number min and max (its score band)")
    ok_opts = True
    for i, q in enumerate(Q, 1):
        f = f"quiz.q{i}"
        if not isinstance(q, dict): add("P0", "Z1", f, "each question is an object {text, options, ...}"); ok_opts = False; continue
        for k in q:
            if k not in K["question"]: add("P1", "Z1", f, f'unknown key "{k}" (allowed: {", ".join(K["question"])})')
        if not _s(q.get("text")): add("P0", "Z1", f + ".text", "question text missing")
        O = q.get("options")
        if not isinstance(O, list): add("P0", "Z1", f + ".options", "options must be a list"); ok_opts = False; continue
        if not omin <= len(O) <= omax: add("P0", "Z2", f + ".options", f"{len(O)} options ({omin}-{omax})")
        ok_ = "option_knowledge" if typ == "knowledge" else "option_matching"; nc = 0
        for j, o in enumerate(O, 1):
            if not isinstance(o, dict) or not _s(o.get("text")): add("P0", "Z1", f"{f}.option{j}", "option text missing"); ok_opts = False; continue
            for k in o:
                if k not in K[ok_]: add("P1", "Z1", f"{f}.option{j}", f'unknown key "{k}" for a {typ} option (allowed: {", ".join(K[ok_])})')
            if typ == "knowledge":
                if "correct" in o and not isinstance(o["correct"], bool): add("P1", "Z1", f"{f}.option{j}", "correct must be true or false")
                nc += o.get("correct") is True
            elif o.get("result") not in keys:
                add("P0", "Z3", f"{f}.option{j}", f'option maps to result "{o.get("result")}", which is not a result key: the option leads nowhere'); ok_opts = False
        if typ == "knowledge" and nc != 1: add("P0", "Z1", f + ".options", f"{nc} options marked correct (exactly 1)"); ok_opts = False
        tx = [(o.get("text") or "").strip().lower() for o in O if isinstance(o, dict)]
        if len(set(tx)) != len(tx): add("P1", "Z1", f + ".options", "two options with the same text")
    qt = [(q.get("text") or "").strip().lower() for q in Q if isinstance(q, dict)]
    if len(set(qt)) != len(qt): add("P1", "Z1", "quiz.questions", "two questions with the same text")
    blocking = any(i_["sev"] == "P0" for i_ in I)
    # Z3 reachability: every score lands in exactly one band; every result can be the outcome
    if typ == "knowledge" and not blocking:
        n = len(Q); cover = {}
        for r in Rs:
            if not (0 <= r["min"] <= r["max"] <= n): add("P0", "Z3", f'quiz.result.{r["key"]}', f'band {r["min"]}-{r["max"]} is outside 0-{n}'); continue
            for s_ in range(r["min"], r["max"] + 1):
                if s_ in cover: add("P0", "Z3", f'quiz.result.{r["key"]}', f'score {s_} is in two bands ({cover[s_]} and {r["key"]})')
                cover[s_] = r["key"]
        gaps = [s_ for s_ in range(n + 1) if s_ not in cover]
        if gaps: add("P0", "Z3", "quiz.results", f"scores {gaps} fall in no band: the bands must cover 0-{n} without gaps")
    if typ == "matching" and ok_opts and not blocking:
        for r in Rs:
            nq = sum(1 for q in Q if any(o.get("result") == r["key"] for o in q["options"]))
            if nq < 2: add("P1", "Z3", f'quiz.result.{r["key"]}', f'result "{r["key"]}" is mapped in {nq} question(s) (at least 2)')
            elif best_path(quiz, r["key"]) is None: add("P1", "Z3", f'quiz.result.{r["key"]}', f'no set of answers leads to "{r["key"]}" (ties go to the result listed first): map it in more questions')
    # Z4 sources: a knowledge question states a fact (its answer); any explanation that states a fact needs a source
    lc = link_cache
    for i, q in enumerate(Q, 1):
        if not isinstance(q, dict): continue
        f = f"quiz.q{i}"; src = q.get("source"); expl = q.get("explanation") or ""
        if src is not None:
            if not (isinstance(src, dict) and str(src.get("url", "")).startswith("https://")): add("P1", "Z4", f + ".source", "source needs an https url"); src = None
            elif len((src.get("quote") or "").split()) < L["quote_min_words"]: add("P1", "Z4", f + ".source", f'source needs the exact quoted span that states the fact (quote, {L["quote_min_words"]}+ words)')
            else:
                for k in src:
                    if k not in K["source"]: add("P1", "Z1", f + ".source", f'unknown key "{k}" (allowed: url, quote)')
                if lc is not None:
                    import datetime as _dt
                    r_ = lc.get(src["url"]); t_ = today or _dt.date.today()
                    if not r_ or (t_ - _dt.date.fromisoformat(r_["checked"])).days > 7: add("P1", "Z4", f + ".source", f"not link-checked in the last 7 days: run hubctl sources-check ({src['url'][:70]})")
                    elif r_["status"] in ("dead", "moved"): add("P1", "Z4", f + ".source", f"source is {r_['status']} ({r_.get('code')}): {src['url'][:70]}. Replace it or cut the question")
        derivable = q.get("derivable") is True
        if "derivable" in q and not isinstance(q["derivable"], bool): add("P1", "Z1", f, "derivable must be true or false")
        if typ == "knowledge":
            if derivable and not _s(expl): add("P1", "Z4", f + ".explanation", "a derivable question shows the working in its explanation")
            elif not derivable and src is None: add("P1", "Z4", f + ".source", "a knowledge question states a fact (its answer): add source {url, quote}, or mark it derivable (math, logic) and show the working")
            if src and not derivable:
                right = next((o.get("text", "") for o in q.get("options") or [] if isinstance(o, dict) and o.get("correct") is True), "")
                if right and right.strip().lower().rstrip(".") not in (src.get("quote") or "").lower() and not re.fullmatch(r"(?i)true|false|yes|no", right.strip()):
                    add("P2", "Z4", f + ".source", f'the quote does not contain the correct answer "{right[:40]}": check that it states it')
        elif src is None and FACT.search(expl):
            add("P1", "Z4", f + ".explanation", f'the explanation states a fact ("{FACT.search(expl).group(0)}"): add source {{url, quote}} or cut the fact')
    # Z5 diagnosis (P0), Z6 lengths, Z7 hygiene, Z8 franchises
    sys.path.insert(0, os.path.join(ROOT, "qc"))
    import qc_hub as Q_
    lim = {"title": L["title"], "intro": L["intro"], "text": L["question"], "explanation": L["explanation"]}
    pn = (primary or "").lower()
    for label, t in texts(quiz):
        for rx in DIAG:
            m = rx.search(t)
            if m: add("P0", "Z5", label, f'diagnosis claim "{m.group(0)}": a quiz never diagnoses; frame results as preferences or knowledge, never a condition'); break
        tail = label.rsplit(".", 1)[-1]
        mx = L["option"] if tail.startswith("option") else L["result_title"] if tail == "title" and ".result" in label else L["result_description"] if tail == "description" else lim.get(tail)
        if mx and len(t) > mx: add("P1", "Z6", label, f"{len(t)} chars (max {mx} at 390 px)")
        if re.search(r"[<>]", t): add("P1", "Z7", label, "no HTML or angle brackets: quiz text renders as plain text")
        for rx, why in Q_.BANNED:
            if re.search(rx, t): add("P1", "Z7", label, why)
        low = t.lower()
        for w in Q_.TELLS["block"]:
            if re.search(r"(?<![a-z\-])" + re.escape(w) + r"(?![a-z\-])", low): add("P1", "Z7", label, f'AI-tell word "{w}": rewrite in plain words')
        for m in Q_.WE_OUR.finditer(t):
            if m.group(0) != "US": add("P1", "Z7", label, f'"{m.group(0)}": never we/our in quiz text'); break
        import serial_comma as _SC
        if _SC.find(t)[0]: add("P1", "Z7", label, "serial comma missing (house style: a, b, and c)")
        for w_ in re.findall(r"[A-Za-z]+", t):
            if w_.lower() in Q_.US["map"]: add("P1", "Z7", label, f'UK spelling "{w_}": use "{Q_.US["map"][w_.lower()]}"')
        for nm in R["franchises"]["names"]:
            if re.search(r"(?<![a-z])" + re.escape(nm) + r"(?![a-z])", low) and nm not in pn:
                add("P1", "Z8", label, f'"{nm}" is a trademarked franchise or test: not as a result or question unless the page is about it'); break
    # P2: the quiz should be about the page's keyword (results match the page's promise)
    core = [w for w in re.findall(r"[a-z]+", pn) if w not in ("quiz", "test", "online", "free", "the", "a", "for", "and", "of")]
    if core and _s(quiz.get("title")) and not any(w in quiz["title"].lower() or w.rstrip("s") in quiz["title"].lower() for w in core):
        add("P2", "Z0", "quiz.title", f'the quiz title names none of "{" ".join(core)}": check it matches the page\'s promise')
    return I

def check_spec(spec, add, link_cache=None):
    """Called from qc_hub.check: Z0 (quiz pages carry a quiz, other pages none) and every quiz check."""
    q = spec.get("quiz")
    if spec.get("status") in ("live-draft", "published") and not q: return
    if is_quiz_page(spec) and q is None:
        add("P1", "Z0", "quiz", "quiz page without spec.quiz: write the quiz JSON (docs/QUIZ.md; skeleton.py set URL quiz FILE.json)"); return
    if q is not None and not is_quiz_page(spec):
        add("P1", "Z0", "quiz", "spec.quiz on a page that is not a quiz page (SurveyQuiz slug containing 'quiz')"); return
    if q is None: return
    for i in check(q, (spec.get("keywords") or {}).get("primary", ""), link_cache):
        add(i["sev"], i["code"], i["field"], i["msg"])
    for sev, msg in carrier_problems(spec): add(sev, "Z9", "hero_prompt", msg)

def carrier_problems(spec):
    """Z9 (Divit 2026-10-14, carrier conditions): the exported hero prompt field with the quiz block still holds exactly the hero
    prompt (<p> and window.awbPrompt as without a quiz) plus one separate quiz block equal to spec.quiz. [] when clean."""
    sys.path.insert(0, os.path.join(ROOT, "ops")); import hubctl as H_
    car = H_.quiz_carrier(spec["url"], spec)
    if not car: return [("P1", "no quiz carrier configured (config quiz_carrier)")]
    with_q = H_.export_fields(spec["url"], spec, live=set())[0].get(car) or ""
    bare = dict(spec); bare.pop("quiz", None)
    without = H_.export_fields(spec["url"], bare, live=set())[0].get(car) or ""
    a, b = split_prompt(with_q), split_prompt(without); out = []
    if not without: out.append(("P0", f"the carrier field ({car}) is empty: the quiz has nothing to ride in"))
    if a["p"] != b["p"] or a["prompt"] != b["prompt"]: out.append(("P0", "the hero prompt (<p> or window.awbPrompt) changes when the quiz block is added"))
    if a["quiz"] != spec["quiz"]: out.append(("P0", "the exported quiz block does not decode to spec.quiz"))
    if a["blocks"] != b["blocks"] + 1 or not with_q.startswith(without): out.append(("P0", "the quiz must be one separate embed block appended after the hero prompt's own blocks"))
    if len(with_q) > 45000: out.append(("P0", f"carrier value {len(with_q)} chars: Webflow rich text code is capped at 50,000"))
    return out

def source_urls(spec):
    return sorted({q["source"]["url"] for q in ((spec.get("quiz") or {}).get("questions") or [])
                   if isinstance(q, dict) and isinstance(q.get("source"), dict) and str(q["source"].get("url", "")).startswith("https://")})

# ---------------------------------------------------------------- export
def embed_block(quiz):
    """The rich-text embed block carrying the quiz (appended to the carrier field at export, docs/QUIZ.md). Angle brackets,
    ampersands and line separators are JSON-escaped, so the value can never close the script or open a tag."""
    js = json.dumps(quiz, ensure_ascii=False, separators=(",", ":"))
    for a, b in (("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026"), (" ", "\\u2028"), (" ", "\\u2029")): js = js.replace(a, b)
    return f"<div data-rt-embed-type='true'><div data-rt-embed-type='true'><script id='awb-quiz-data'> window.awbQuiz = {js}; </script></div></div>"

def js_object(html, name):
    """The object assigned to window.<name> in a <script> (a field value or a live page): every 'window.<name> =' is tried and the
    first one that decodes as JSON and is followed by '; </script>' wins, so a comment that mentions the name (hero-chips.html,
    the quiz embed) is never mistaken for the data. None when absent."""
    dec = json.JSONDecoder()
    for m in re.finditer(r"window\." + re.escape(name) + r"\s*=\s*", html or ""):
        try: obj, end = dec.raw_decode(html, m.end())
        except ValueError: continue
        if isinstance(obj, dict) and re.match(r"\s*;\s*</script>", html[end:]): return obj
    return None
def from_block(html): return js_object(html, "awbQuiz")

EMBED_START = "<div data-rt-embed-type='true'>"
def split_prompt(value):
    """The hero prompt field as exported (or read back): {p: the visible <p> HTML before any embed block, prompt: window.awbPrompt,
    quiz: window.awbQuiz, blocks: number of embed blocks}. The <p> and awbPrompt are what the hero shows; the quiz block is separate."""
    v = value or ""; i = v.find(EMBED_START)
    return {"p": v if i < 0 else v[:i], "prompt": js_object(v, "awbPrompt"), "quiz": js_object(v, "awbQuiz"),
            "blocks": v.count("<div data-rt-embed-type='true'><div data-rt-embed-type='true'>")}

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("check", "block"): sys.exit(__doc__)
    qz = json.load(open(a[1]))
    if a[0] == "block": print(embed_block(qz)); sys.exit(0)
    pr = a[a.index("--primary") + 1] if "--primary" in a else ""
    iss = check(qz, pr)
    for i in iss: print(f"  {i['sev']} {i['code']} {i['field']}: {i['msg']}")
    n = sum(1 for i in iss if i["sev"] in ("P0", "P1")); print(f"quiz: {n} P0/P1"); sys.exit(min(n, 100))
