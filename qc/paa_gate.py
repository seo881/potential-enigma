"""paa_gate.py: the PAA gate PA1-PA15 (PA14 brands, PA15 file formats: Divit 2026-10-09) (handover 2026-10-08 section 5; approved by Divit 2026-10-08).
Ruling 18 (Divit 2026-10-14), NEW writing only (pools, skeletons, feasibility, never-reviewed FAQs; ruling 15): PA4 other sense
(sense_shift), PA16 named program/agency/state, PA17 spelling/translation/citation trivia, PA6 dropped shapes (navigational,
self-quiz, fragment; only where PA6 would flag), PA9/PA10 same-intent variants (near_dup). Lists: rules/paa_patterns.json.

  hubctl paa URL          gate the page's AlsoAsked pull (private/alsoasked/<slug>.json, from ops/alsoasked_pull.py), plus the
                          top-secondary pull private/alsoasked/<slug>--sec.json when one was made (weekend.py aa URL --kw secondary)
  hubctl paa URL --spec   gate the spec's current FAQ (spec.faq_sources + fields.faq); PA1b: no answer may share a 6-word run
                          with the pull's answer_*/ai_overview* text (provenance only, never FAQ copy)
  hubctl paa-resource URL write AlsoAsked provenance into matching faq_sources items; a DataForSEO-PAA item with no match
                          that carries a secondary becomes source secondary (ref = that secondary, paa_ref = old ref); text byte-identical
  --cand                  also admit the page's SAFE synonym candidates (rules/paa_synonym_candidates.json; not yet approved)

Written questions (Divit 2026-10-16, "FULL-THROTTLE WRITING" item 1): every page has 10 questions; gate-passing AlsoAsked PAA
first, verbatim (faq_sources source "paa"; "alsoasked" is the older label), then questions the writer writes (source "written").
A written question is judged by the same content gates (PA3-PA10, PA14-PA17) and takes no flag (a flag is a reject: rephrase it),
must not be a respondent's question (PA6; an unclassified asker is a note the reviewer judges), and also: PA18 at most one secondary keyword, PA19 not hub-level generic (a page-topic term: the
primary's distinguishing word or a page-specific secondary), PA20 never another page's primary, PA21 no third-party pricing.
Provenance and verbatim checks (PA1, PA1b, hubctl verbatim) apply to source paa only. PA11/PA12 no longer park a page for being
short of PAA: written questions take it to 10.

Principle: a question is rejected unless it proves it belongs on the page. Each question gets pass, reject or flag
(needs a human judgment; never silently passed) with every reason by rule ID. Verdicts go to
private/alsoasked/verdicts/<slug>[.faq].json (git-ignored); one summary line goes to audit/paa/summary.md.
Not wired into the QC TOTAL; F4 is not retired yet. Patterns and lists: rules/paa_patterns.json,
rules/paa_blocklist.json, rules/paa_synonyms.json.
"""
import datetime, glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))
R = lambda f: json.load(open(os.path.join(ROOT, "rules", f)))
STOP = set("a an the of for to in on at by with and or is are do does did i we you my our your can how what which who when where why "
           "should would will it its be there this that from as if so any".split())
PROV = ("tool", "query", "depth", "parent", "fetched", "original")
JACCARD_DUP = 0.8      # PA9/PA10 same-intent threshold on content words (tune after the first full run)
PARTICLES = {"up", "in", "out", "off", "on"}   # phrasal-verb particles: function words in PA9 when the head phrase carries them (sign up, check in)
def pa9_content(q, head):
    """PA9 overlap words: content(q) minus the phrasal-verb particles of the page's head phrase (B-dev-11, Divit's go 2026-10-15:
    "up" in "potluck sign up sheet" made the definition and the how-to-build question one intent)."""
    return content(q) - (PARTICLES & content(head or ""))
MAX_RESPONDENT, MAX_BRANDED, MIN_ON_TOPIC, N_FAQ, MIN_SECONDARIES = 2, 0, 8, 10, 6   # PA8 brand cap 0 (Divit 2026-10-09)

def norm0(s): return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9'.&-]+", " ", s.lower().replace("’", "'"))).strip()
import spelling as _SP
def norm(s): return _SP.to_us(norm0(s))   # ruling 14: UK spellings read as US (rules/us_spelling.json), so PA3 and H2 agree
def stem(w): return re.sub(r"(ies|es|s|ing|ed)$", "", w) if len(w) > 4 else w
SAME = {"make": "create", "build": "create", "design": "create", "setup": "create", "generate": "create"}  # same intent for PA9/PA10
def content(s): return {SAME.get(stem(w), stem(w)) for w in re.split(r"[\s-]+", norm(s).replace("set up", "setup")) if w and w not in STOP}
def jacc(a, b): return len(a & b) / len(a | b) if a | b else 0.0
def has(term, q): return re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", q) is not None
def qhash(q):  # stable id of a question (normalised text), for strike lists and sheets: never the text itself in git
    import hashlib; return hashlib.sha1(norm0(q).encode()).hexdigest()[:10]   # norm0: hashes stay stable when the spelling list grows
PA6_SHAPES = [("definition", r"^(what is|what's|what are|what does .* mean|define)\b"), ("how-to", r"^how (to|do|can|should|would) "),
              ("cost", r"\b(cost|price|pricing|how much|cheap|free)\b"), ("which tool", r"^(which|what) [a-z ]{0,30}(tools?|software|apps?|platforms?|systems?)\b"),
              ("comparison", r"\b(vs|versus|difference|compared?|better than)\b"), ("yes/no", r"^(can|does|do|is|are|should|will) "),
              ("why/benefit", r"^(why|what are the benefits|what are the advantages)\b"),
              # 'other' split further (2026-10-14: 303 of 866 flags were 'other', too broad for one tick)
              ("self-quiz (am I)", r"\bam i\b"), ("where/when", r"^(where|when)\b"),
              ("how long/often/well", r"^how (long|often|many|much|well|good|strong|healthy|smart|accurate|old|big|fast)\b"),
              ("headline (how X does Y)", r"^how (?!does|do|did|is|are|was|were|can|could|should|would|will|to)[a-z]+ [a-z]+"),
              ("open what/how/who", r"^(what|how|who|whom|whose) ")]
def pa6_shape(q):
    nq = norm(q or "")
    return next((name for name, rx in PA6_SHAPES if re.search(rx, nq)), "fragment or name (no question word)")
def flag_subtype(code, msg, q=None):
    """The packet groups flags by subtype (Divit 2026-10-13); PA6 splits by question shape (2026-10-14: 830 PA6 flags were too broad
    for one tick); PA10 and PA14 are per-question by nature (mixed)."""
    if code == "PA2": return "PA2 under a flagged parent"
    if code == "PA6": return "PA6 asker unclear: " + pa6_shape(q) if q else "PA6 asker unclear"
    if code == "PA7" and msg.startswith("advice-shaped"): return "PA7 advice-shaped"
    if code == "PA7" and msg.startswith("definitional"): return "PA7 " + msg.split()[1] + " definition"
    if code == "PA14": return "PA14 capitalised name"
    if code == "PA10": return "PA10 shared with a sibling page"
    return code + " " + msg[:30]
MIXED_SUBTYPES = ("PA14 capitalised name", "PA10 shared with a sibling page")
def _flag_decisions():
    p_ = os.path.join(ROOT, "rules", "flag_decisions.json")
    d = json.load(open(p_)) if os.path.exists(p_) else {}
    return {"subtypes": d.get("subtypes", {}), "questions": d.get("questions", {})}
def phrase_re(p):  # head phrase, each word optionally plural, space or hyphen between words
    ws = norm(p).split()
    return re.compile(r"(?<![a-z0-9])" + r"[\s-]+".join(re.escape(w) + r"(?:s|es)?" for w in ws) + r"(?![a-z0-9])")

# ---------- ruling 18 parts 4 and 5 (Divit 2026-10-14): prevention for NEW writing only (ruling 15: no recheck of reviewed pages) ----------
_R18 = None
def r18():
    global _R18
    if _R18 is None: _R18 = R("paa_patterns.json")
    return _R18
def reviewed_already(spec):
    """A spec that has been through review (spec.review is set by hubctl review and kept through rework, approval and publish):
    its own FAQ is judged as reviewed (ruling 15) and the r18 checks never re-gate it. Pools, skeletons and feasibility always use them."""
    return bool((spec or {}).get("review"))
_NEAR = {}
def content_near(s):
    """content() after the same-intent rewrite: verb classes (fill/complete/fill out/write/draw up = one; shorten/speed up = one),
    filler phrases and years removed (ruling 18 part 4a)."""
    if s in _NEAR: return _NEAR[s]
    nd = r18()["near_dup"]; t = " " + re.sub(r"\b(19|20)\d\d\b", " ", norm(s)) + " "
    for f in nd["fillers"]: t = re.sub(r"(?<![a-z0-9])" + f + r"(?![a-z0-9])", " ", t)
    for cls, vs in nd["verb_classes"].items():
        for v in vs: t = re.sub(r"(?<![a-z0-9])" + v + r"(?![a-z0-9])", cls, t)
    _NEAR[s] = {w[:-1] if len(w) > 4 and w.endswith("e") else w for w in content(t)}   # cycle/cycles, create/creates: one stem
    return _NEAR[s]
def near_dup(a, b, head=None):
    """Same intent after the ruling 18 rewrite. head: the page's primary; when given, both questions must say something beyond the
    head phrase (a best-practices question and the definition of the same head are different questions: nothing but filler is left
    once the head is set aside, so only the plain PA9 test applies)."""
    ca, cb = content_near(a), content_near(b)
    if head:
        h = content_near(head)
        if not (ca - h) or not (cb - h): return False
    return jacc(ca, cb) >= JACCARD_DUP
def drop_shape(q, source="alsoasked"):
    """Ruling 18 part 5: the question shapes code drops (navigational, self-quiz, fragment); None when the shape is allowed.
    A fragment (no question word) is judged on AlsoAsked and Semrush items only: a secondary is a keyword the writer turns into a question."""
    ds = r18()["drop_shapes"]; nq = norm(q or "")
    if re.search(ds["navigational"], nq): return "navigational (where is / where to find)"
    if re.search(ds["self-quiz (am I)"], nq): return "self-quiz (am I)"
    if source not in ("secondary", "slot", "definition") and not re.search(ds["question_word"], nq): return "fragment or name (no question word)"
    return None
def trivia(q, page_sense=""):
    """Ruling 18 part 4d: the spelling of the term, a translation, a citation (not on a page about spelling, language or citing)."""
    nq = norm(q or "")
    if any(has(w, page_sense) for w in r18()["trivia_page_exempt"]): return None
    if any(re.search(p, nq) for p in r18()["trivia"]): return "spelling, translation or citation trivia"
    m = re.match(r"^(is it|should it be|is the correct (spelling|term)|which is correct,?) (.+?) or (.+?)\??$", nq)
    if m and re.sub(r"[\s-]", "", m.group(3)) == re.sub(r"[\s-]", "", m.group(4)): return "spelling variant trivia (X or X)"
    return None

# ---------- written questions (Divit 2026-10-16 item 1) ----------
PAA_SOURCES = ("paa", "alsoasked")
WRITTEN = "written"
HUB_GENERIC = {"form", "survey", "quiz", "questionnaire", "landing", "page", "automation", "workflow", "builder", "template", "online",
               "free", "ai", "maker", "generator", "create", "example", "sample", "best", "digital", "custom", "simple", "website",
               "site", "tool", "automate", "automated"}
def _gstem(w): return SAME.get(stem(w), stem(w))
GENERIC_STEMS = {_gstem(w) for w in HUB_GENERIC}
def topic_terms(phrase):
    """A keyword's page-topic words: its content words minus the hub-level generic ones and phrasal particles (PA19)."""
    return content(phrase) - GENERIC_STEMS - PARTICLES
PRICE_RX = re.compile(r"\b(cost|costs|price|priced|prices|pricing|how much|cheap|cheapest|fee|fees|charge|charges|subscription|per month|per user|per seat)\b")
THIRD_PARTY_RX = re.compile(r"\b(software|tools?|apps?|platforms?|builders?|services?|vendors?|providers?|compan(y|ies)|plugins?|solutions?|makers?|generators?|products?)\b")

def hub_of(url):
    for k, h in CFG["hubs"].items():
        if url.startswith(h["path"] + "/"): return k, h
    sys.exit(f"no hub owns {url}")

class Gate:
    def __init__(self, url, extra_heads=()):
        self.url, self.slug = url, url.rsplit("/", 1)[1]
        self.hub, h = hub_of(url); self.dir, self.hub_path = h["repo_dir"], h["path"]
        self.spec_path = os.path.join(ROOT, "specs", self.dir, self.slug + ".json")
        self.spec = json.load(open(self.spec_path)) if os.path.exists(self.spec_path) else {}
        self.primary = (self.spec.get("keywords") or {}).get("primary") or self.slug.replace("-", " ")
        self.heads = [phrase_re(p) for p in [self.primary] + R("paa_synonyms.json")["pages"].get(self.slug, []) + list(extra_heads)]
        # PA3 widened (Divit, 2026-10-08): head phrase reordered/inflected, or an approved secondary of the page (K8 test)
        self.head_words = [stem(w) for w in norm(self.primary).split()]
        secs = set((self.spec.get("keywords") or {}).get("secondaries_used") or [])
        self.workbook_secs = []   # the page's Semrush secondaries (plan/keyword_map.json): PA12 counts only these (Divit 2026-10-13)
        _pp = os.path.join(ROOT, "plan"); _pp in sys.path or sys.path.append(_pp); import kmap_load as _KL   # + tracked additions (plan/additions.json)
        _km = _KL.load(ROOT)
        if _km is not None:
            self.workbook_secs = [x["kw"] for x in (_km.get(url, {}) or {}).get("secondaries", []) if x.get("kw")]
            secs |= set(self.workbook_secs)
        self.secondaries = sorted(secs)
        # PA14 exemption (Divit 2026-10-12): the page's own keyword words and their initials (AP = accounts payable) are not brands
        self.page_terms = set()
        for k in [self.primary] + self.secondaries:
            ws = [w for w in re.split(r"[\s-]+", norm(k)) if w]
            self.page_terms |= set(ws)
            for n in (2, 3):
                self.page_terms |= {"".join(x[0] for x in ws[i:i + n]) for i in range(len(ws) - n + 1)}
        self.bl, self.pt = R("paa_blocklist.json"), R("paa_patterns.json")
        for e in self.bl["per_page"].get(self.slug, []):
            if not e.get("reason"): sys.exit(f"rules/paa_blocklist.json per_page {self.slug}: entry without a reason: {e.get('q') or e.get('qh')}")
        self.skip = {norm(e["q"]): e["reason"] for e in self.bl["per_page"].get(self.slug, []) if e.get("q")}
        # ruling 12 strikes are stored by hash (qhash), so no AlsoAsked text enters git
        self.skip_h = {e["qh"]: e["reason"] for e in self.bl["per_page"].get(self.slug, []) if e.get("qh")}
        lib = os.path.join(ROOT, "rules", "competitors", self.dir + ".json")
        self.library = [c.lower() for c in json.load(open(lib)).get("competitors", {})] if os.path.exists(lib) else []
        self.new_writing = not reviewed_already(self.spec)   # ruling 18 / ruling 15: r18 checks on this page's own FAQ only when never reviewed
        # ruling 18 part 4b: the page's own sense (primary, H1, slug): a sense_shift or named qualifier the page itself carries never fires
        self.page_sense = " " + norm(" ".join([self.primary, str((self.spec.get("fields") or {}).get("h1") or ""), self.slug.replace("-", " ")])) + " "
        # PA20 (written): every other page's multi-word primary across the hubs, unless this page's own primary or a secondary holds it
        own = [norm(self.primary)] + [norm(k) for k in self.secondaries]
        self.other_prims = []
        if _km is not None:
            for u, e in _km.items():
                op = norm((e or {}).get("primary") or "")
                if u == url or len(op.split()) < 2 or any(op in o for o in own): continue
                self.other_prims.append((u, op, phrase_re(op)))
        self.siblings = []  # PA10: every other spec in the hub, with its head phrase
        for p in glob.glob(os.path.join(ROOT, "specs", self.dir, "*.json")):
            if os.path.basename(p).startswith("_") or p == self.spec_path: continue
            try: s = json.load(open(p))
            except Exception: continue
            prim = (s.get("keywords") or {}).get("primary") or ""
            for f in s.get("faq_sources") or []:
                if f.get("q"): self.siblings.append((s.get("url") or os.path.basename(p), prim, f["q"], content(f["q"])))

    def pa3_widened(self, q):
        qw = [stem(w) for w in re.split(r"[\s-]+", q) if w]
        hw = self.head_words; win = max(4, len(hw))
        if hw and all(w in qw for w in hw):
            for i in range(len(qw)):
                if set(hw) <= set(qw[i:i + win]): return "reordered or inflected head phrase"
        qs = set(qw)
        for k in self.secondaries:
            kw = [stem(w) for w in re.split(r"[\s-]+", norm(k)) if w]
            if kw and set(kw) <= qs: return f"secondary: {k}"
        return None

    def asker(self, q):
        if any(re.search(p, q) for p in self.pt["respondent"]): return "respondent"
        if any(re.search(p, q) for p in self.pt["builder"]): return "builder"
        return None

    def domain(self, q): return [d for d, ws in self.pt["domains"].items() if any(has(w, q) for w in ws)]

    def sense_shift(self, q):
        """Ruling 18 part 4b: the question puts the page's head noun in another sense (insurance proposal on a business proposal-form
        page; medical lab requisition on a purchase requisition-form page). Fires only when the page itself is not in that sense."""
        for head, quals in r18()["sense_shift"].items():
            if not has(head, self.page_sense.strip()) or not phrase_re(head).search(q): continue
            off = [x for x in quals if has(x, q) and not has(x, self.page_sense)]
            if off: return f'"{head}" in another sense ({", ".join(off[:3])}); the page is not about that sense'
        return None

    def named(self, q, raw):
        """Ruling 18 part 4c: a named program or agency (American Community Survey, USPS, WHO surveys, IRS ...) or a US state used as a
        scope (state-specific and navigational). Two-letter state codes count only in capitals (never the ambiguous ones: IN, OR, ME,
        OK, HI ...) or lowercase right before the head phrase (keyword-sourced). The page's own primary, H1 or slug is exempt."""
        P18, bl = r18(), self.bl; hits = []
        hits += [n for n in P18["named"] if phrase_re(n).search(q) and not phrase_re(n).search(self.page_sense)]
        hits += [n for n in P18["named_upper"] if re.search(r"(?<![A-Za-z0-9])" + n + r"(?![A-Za-z0-9])", raw) and not has(n.lower(), self.page_sense)]
        hits += [s for s in bl.get("pa14_us_states", []) if has(s.lower(), q) and not has(s.lower(), self.page_sense)]
        skip = set(P18["state_abbr_skip"])
        hw = norm(self.primary).split()
        # a capitalised code used as a place: after in/for/from/of/to/a/an/the, or right before the head phrase or "state"
        # ("in DE", "a DE <head phrase>"), never a code used as an abbreviation of something else (CA, certificate authority)
        nxt = r"(?:state|" + re.escape(hw[0]) + r")" if hw else r"state"
        hits += [a for a in P18["state_abbr"] if a not in skip and re.search(r"(?:\b(?:in|for|from|of|to|a|an|the)\s+" + a + r"(?![A-Za-z0-9])|(?<![A-Za-z0-9.])" + a + r"\s+(?i:" + nxt + r"))", raw)]
        if raw == raw.lower() and hw:   # keyword-sourced (all lowercase): a state code directly before the head phrase
            hits += [a for a in P18["state_abbr"] if a not in skip and re.search(r"(?<![a-z0-9])" + a.lower() + r"\s+" + re.escape(hw[0]), q)]
        return sorted(set(hits))

    def judge(self, item):
        """The per-question rules, then Divit's flag decisions (rules/flag_decisions.json, Divit 2026-10-13): an approved flag subtype
        becomes a note, a rejected one a reject; a per-question decision (mixed subtypes such as PA10 and PA14) settles that question."""
        out = self._judge(item)
        if item.get("source") == WRITTEN:   # Divit 2026-10-16: a written question takes no flag; the writer rephrases it
            return [(r[0], "reject", "written question, rephrase it: " + r[2]) if r[1] == "flag" else r for r in out]
        if not any(r[1] == "flag" for r in out): return out
        fd = _flag_decisions(); qh = qhash(item.get("q") or "")
        res = []
        for r in out:
            if r[1] != "flag": res.append(r); continue
            st = flag_subtype(r[0], r[2], item.get("q")); d = (fd["questions"].get(self.slug + ":" + qh) or {}).get("decision") or (fd["subtypes"].get(st) or {}).get("decision")
            if d == "approve": res.append((r[0], "note", "approved by Divit (" + st + "): " + r[2]))
            elif d == "reject": res.append((r[0], "reject", "rejected by Divit (" + st + "): " + r[2]))
            else: res.append(r)
        return res

    def _judge(self, item):
        """item: {q, prov, source}. Returns list of (rule, 'reject'|'flag'|'note', reason)."""
        q, out = norm(item["q"]), []
        prov, src = item.get("prov") or {}, item.get("source", "alsoasked")
        written = src == WRITTEN
        if item.get("n") in (1, 2): src = "slot"  # definition and how-to-build are template slots: exempt from PA1/PA2 (DECISIONS 2026-10-08)
        # PA1 provenance: PAA items come from AlsoAsked only (US, English) with full provenance
        if src in ("paa", "alsoasked"):
            if prov.get("tool") != "alsoasked-api": out.append(("PA1", "reject", f"PAA item not from AlsoAsked (tool {prov.get('tool') or 'dataforseo'})"))
            else:
                miss = [k for k in PROV if prov.get(k) in (None, "") and not (k == "parent" and prov.get("depth") == 1)]
                if miss: out.append(("PA1", "reject", "missing provenance: " + ", ".join(miss)))
                if prov.get("region") != "us" or prov.get("language") != "en" or prov.get("fallback"): out.append(("PA1", "reject", "not a US English result (or fallback)"))
            # PA2 depth
            d = prov.get("depth")
            if d and d >= 3 and not prov.get("depth_reason"): out.append(("PA2", "reject", f"depth {d} without a written reason"))
            if d == 2 and item.get("parent_verdict") == "reject": out.append(("PA2", "reject", "level 2 under a rejected parent"))
            if d == 2 and item.get("parent_verdict") == "flag": out.append(("PA2", "flag", "level 2 under a flagged parent"))
        # PA3 entity match: full head phrase or an approved synonym; a shared word never qualifies
        if not any(h.search(q) for h in self.heads):
            via = self.pa3_widened(q)
            if via: out.append(("PA3w", "note", via))
            else: out.append(("PA3", "reject", f'no head phrase "{self.primary}" (exact, reordered or inflected), approved secondary or synonym'))
        # PA4 wrong sense: global blocklist and the per-page skip list
        ws = [w for w in self.bl["wrong_sense"] if has(w, q)]
        if ws: out.append(("PA4", "reject", "wrong-sense term: " + ", ".join(ws)))
        if q in self.skip: out.append(("PA4", "reject", "per-page skip: " + self.skip[q]))
        elif qhash(q) in self.skip_h: out.append(("PA4", "reject", "per-page skip: " + self.skip_h[qhash(q)]))
        if any(re.search(r"\b(apply|applying|application) (for|to) (the |an? )?" + h.pattern, q) for h in self.heads):
            out.append(("PA4", "reject", "treats the page's document as something one applies for (wrong sense)"))
        ctx = norm(item.get("ctx") or "")  # the AlsoAsked answer source: provenance used only to judge the sense, never copied
        cw = [w for w in self.bl["wrong_sense"] + self.bl.get("wrong_sense_source", []) if has(w, ctx)]
        if cw: out.append(("PA4", "reject", "answer source is about a different sense: " + ", ".join(cw[:3])))
        cn = [w for w in self.bl["non_us"] if has(w, ctx)]
        if cn: out.append(("PA5", "reject", "answer source is non-US: " + ", ".join(cn[:3])))
        # PA5 US audience
        nu = [w for w in self.bl["non_us"] if has(w, q)]
        if nu: out.append(("PA5", "reject", "non-US term: " + ", ".join(nu)))
        # PA6 asker
        a = self.asker(q); item["asker"] = a
        if written and a == "respondent": out.append(("PA6", "reject", "written question is not builder intent (a respondent asks it): ask what a person building this asks"))
        elif written and a is None: out.append(("PA6", "note", "asker unclassified on a written question: the reviewer judges builder intent"))
        elif a is None: out.append(("PA6", "flag", "asker unclassified (builder/respondent/unrelated): needs judgment"))
        # PA7 advice risk
        dom = self.domain(q); adv = any(re.search(p, q) for p in self.pt["advice"])
        if adv and dom: out.append(("PA7", "reject", "advice question in " + "/".join(dom)))
        elif adv: out.append(("PA7", "flag", "advice-shaped question: check it needs no professional advice"))
        elif dom and re.match(r"^(what|which) (is|are) ", q): out.append(("PA7", "flag", "definitional " + "/".join(dom) + " question: needs a primary (.gov or statute) source"))
        # PA8 third-party brands
        retail = [b for b in self.bl["retail_brands"] if has(b, q)]
        tools = [b for b in self.bl["tool_brands"] if has(b, q) and b not in self.library]
        lib = [b for b in self.library if has(b, q)]; item["brands"] = lib
        if retail: out.append(("PA8", "reject", "retailer or gift brand: " + ", ".join(retail)))
        if tools: out.append(("PA8", "reject", "brand not in the competitor library: " + ", ".join(tools)))
        # PA14 no brand or product names (Divit 2026-10-09): listed brands reject; an unlisted capitalised name is flagged
        raw = item.get("q") or ""
        br = [b for b in self.bl.get("pa14_brands", []) if has(b.lower(), q)]
        if br: out.append(("PA14", "reject", "brand or product name: " + ", ".join(sorted(set(br))[:4])))
        ok_caps = set(self.bl.get("pa14_proper_noun_ok", [])) | set(self.bl.get("pa14_domain_ok", []))
        for st in sorted(self.bl.get("pa14_us_states", []), key=len, reverse=True):   # US state names are places, not brands (backlog line 92)
            raw = re.sub(r"(?<![A-Za-z])" + re.escape(st) + r"(?![A-Za-z])", lambda m: m.group(0).lower(), raw)
        caps = [w for i, w in enumerate(re.findall(r"[A-Za-z0-9][A-Za-z0-9.'-]*", raw)) if i > 0
                and w.lower().rstrip("?.") not in self.page_terms and re.sub(r"'?s$", "", w.lower().rstrip("?.")) not in self.page_terms and w[0].isupper() and w.rstrip("?.'s") not in ok_caps and w not in ok_caps and w.lower().rstrip("?.") not in self.bl.get("pa15_formats", [])]
        if caps and not br: out.append(("PA14", "flag", "capitalised name, possibly a brand: " + ", ".join(caps[:3])))
        # PA15 no file formats or download-style asks
        fm = [f for f in self.bl.get("pa15_formats", []) if has(f, q)]
        if fm: out.append(("PA15", "reject", "file format or download ask: " + ", ".join(fm[:3])))
        # ruling 18 parts 4 and 5 (Divit 2026-10-14): new writing only; a reviewed page's own FAQ (run_spec marks it legacy) is never re-gated
        r18on = not item.get("legacy")
        if r18on:
            ss = self.sense_shift(q)
            if ss: out.append(("PA4", "reject", "other sense: " + ss))
            nm = self.named(q, item.get("q") or "")
            if nm: out.append(("PA16", "reject", "names a program, agency or state (state-specific or navigational): " + ", ".join(nm[:3])))
            tv = trivia(q, self.page_sense)
            if tv: out.append(("PA17", "reject", tv))
            sh = drop_shape(item.get("q") or "", src) if a is None else None   # part 5: only shapes that were PA6 flags (asker unclear)
            if sh: out.append(("PA6", "reject", "dropped shape: " + sh))
        if written: out += self.written_checks(q)
        # PA10 one page per question per hub: the page whose head phrase the question carries owns it
        cq = content(q)
        for surl, sprim, sq, sc in self.siblings:
            if jacc(cq, sc) < JACCARD_DUP and not (r18on and near_dup(q, sq, self.primary)): continue
            mine = any(h.search(q) for h in self.heads); theirs = bool(sprim) and phrase_re(sprim).search(q)
            # the longer head phrase is the more specific owner when both match (tournament registration form > registration form)
            if mine and theirs: mine = len(norm(self.primary)) >= len(norm(sprim))
            if mine: out.append(("PA10", "note", f"same question on {surl}; this page owns it"))
            elif theirs: out.append(("PA10", "reject", f"belongs to {surl} (\"{sq[:50]}\")"))
            else: out.append(("PA10", "flag", f"same question on {surl}: decide one owner"))
            break
        return out

    def secondaries_in(self, q):
        """The page's secondaries a question carries (all words, any order), the maximal ones only: one that another carried
        secondary contains is the same keyword use; a secondary inside the primary is the primary."""
        cq, cp = content(q), content(self.primary)
        hits = {frozenset(content(k)): k for k in self.secondaries if content(k) and content(k) <= cq and not content(k) <= cp}
        return sorted(k for c, k in hits.items() if not any(c < o for o in hits))

    def written_checks(self, q):
        """Divit 2026-10-16 item 1: the extra checks on a question the writer wrote (q normalised)."""
        out, cq = [], content(q)
        secs = self.secondaries_in(q)
        if len(secs) > 1: out.append(("PA18", "reject", f"{len(secs)} secondary keywords in one question (at most one): " + ", ".join(secs[:3])))
        topic = topic_terms(self.primary) or content(self.primary)
        own = bool(topic & cq) if topic_terms(self.primary) else topic <= cq
        if not own and not any(topic_terms(k) and content(k) <= cq for k in self.secondaries):
            out.append(("PA19", "reject", f"hub-level generic: names neither the page's topic ({', '.join(sorted(topic)) or self.primary}) nor a page-specific secondary"))
        mine = q
        for h in self.heads: mine = h.sub(" ", mine)
        for k in self.secondaries: mine = phrase_re(k).sub(" ", mine)
        oth = next(((u, op) for u, op, rx in self.other_prims if rx.search(mine)), None)
        if oth: out.append(("PA20", "reject", f'names another page\'s primary "{oth[1]}" ({oth[0]})'))
        if PRICE_RX.search(q) and (THIRD_PARTY_RX.search(q) or any(has(b.lower(), q) for b in self.bl.get("pa14_brands", []) + self.bl["tool_brands"] + self.library)):
            out.append(("PA21", "reject", "third-party pricing: never ask what other products or vendors cost"))
        return out

    def verdict(self, reasons):
        if any(r[1] == "reject" for r in reasons): return "reject"
        if any(r[1] == "flag" for r in reasons): return "flag"
        return "pass"

    def finish(self, items):
        """Within-page rules: PA6 respondent cap, PA8 brand cap, PA9 same-intent duplicates (in item order)."""
        kept, resp, brand = [], 0, 0
        for it in items:
            if it["verdict"] == "reject": continue
            c = pa9_content(it["q"], self.primary)
            # B-c-1 2026-10-16: a definition and a how-to question on the same head phrase are different intents ("What is X?" vs
            # "How do I create X?" share every content word once the verb is dropped); they never count as PA9 duplicates
            dup = next((k for k in kept if jacc(c, pa9_content(k["q"], self.primary)) >= JACCARD_DUP
                        and {pa6_shape(it["q"]), pa6_shape(k["q"])} != {"definition", "how-to"}), None)
            if dup: it["reasons"].append(("PA9", "reject", f'same intent as "{dup["q"][:50]}"'))
            elif not it.get("legacy"):   # ruling 18 part 4a (new writing only): same-intent variants (fill/complete/write; shorten/speed up)
                dup = next((k for k in kept if near_dup(it["q"], k["q"], self.primary)), None)
                if dup: it["reasons"].append(("PA9", "reject", f'same intent as "{dup["q"][:50]}" (same-intent variant)'))
            if it.get("asker") == "respondent":
                resp += 1
                if resp > MAX_RESPONDENT: it["reasons"].append(("PA6", "reject", f"more than {MAX_RESPONDENT} respondent questions"))
            if it.get("brands"):
                brand += 1
                if brand > MAX_BRANDED: it["reasons"].append(("PA8", "reject", f"more than {MAX_BRANDED} third-party brand question"))
            it["verdict"] = self.verdict(it["reasons"])
            if it["verdict"] != "reject": kept.append(it)
        return items

def flatten(d):
    """AlsoAsked API response (schema from ops/alsoasked_schema.py): response.queries[].results[] question tree."""
    m, r, out = d["_meta"], d["response"], []
    def walk(nodes, depth, parent, term, fb):
        for n in nodes or []:
            prov = {"tool": m.get("tool"), "query": term, "depth": depth, "parent": parent, "fetched": m.get("fetched"),
                    "original": n.get("question"), "region": r.get("region"), "language": r.get("language"), "fallback": fb}
            ctx = " ".join(x for x in [n.get("answer_page_title"), n.get("answer_href"), n.get("answer_excerpt")] if isinstance(x, str))
            out.append({"q": n["question"], "source": "alsoasked", "prov": prov, "parent_q": parent, "ctx": ctx})
            walk(n.get("results"), depth + 1, n["question"], term, fb)
    for q in r.get("queries") or []: walk(q.get("results"), 1, None, q.get("term"), q.get("language_fallback") or q.get("region_fallback"))
    return out

MIN_IDEAS = 4   # PA12 for pages without Semrush secondaries (Divit 2026-10-13, ruling 5)
_WB_IDEAS = None
def workbook_ideas(url):
    """The Semrush workbook's keyword ideas for a page: its non-primary rows in 'Keyword report (pass 3)' (private/, git-ignored)."""
    global _WB_IDEAS
    if _WB_IDEAS is None:
        _WB_IDEAS = {}; wbp = os.path.join(ROOT, "private", "Emergent_Hub_Child_Pages_Final_v3.xlsx")
        if os.path.exists(wbp):
            import pandas as pd
            kr = pd.read_excel(wbp, "Keyword report (pass 3)", header=3)
            for _, r in kr.iterrows():
                if str(r["Role"]).startswith("Primary"): continue
                u = str(r["Page URL"]).replace("/ai-survey-quiz-builder/", "/ai-survey-and-quiz-builder/")
                _WB_IDEAS.setdefault(u, []).append(str(r["Keyword"]))
    return _WB_IDEAS.get(url, [])

def pull_path(slug): return os.path.join(ROOT, "private", "alsoasked", slug + ".json")
def sec_pull_path(slug): return os.path.join(ROOT, "private", "alsoasked", slug + "--sec.json")   # A6 (2026-10-12): one pull on the top secondary
def has_pull(slug):
    """Any saved AlsoAsked pull for the page (primary or top-secondary --sec): QC F1/F2 count the same pulls as the gate (B-dev-11, 2026-10-15)."""
    return any(os.path.exists(p) for p in (pull_path(slug), sec_pull_path(slug)))
def pulls(slug):
    """Every saved AlsoAsked pull for a page: the primary pull and, if made, the top-secondary pull (weekend.py aa --kw secondary)."""
    return [json.load(open(p)) for p in (pull_path(slug), sec_pull_path(slug)) if os.path.exists(p)]
def pull_nodes(slug): return [n for d in pulls(slug) for n in flatten(d)]

def answer_shingles(d, n=6):
    """PA1b: every 6-word run in the pull's answer_* and ai_overview* text (provenance only, never FAQ copy)."""
    txt = []
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.startswith(("answer_", "ai_overview")):
                    txt.extend([v] if isinstance(v, str) else [x for x in v if isinstance(x, str)] if isinstance(v, list) else [])
                else: walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(d["response"]); sh = set()
    for t in txt:
        w = norm(t).split(); sh |= {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}
    return sh

def match_pull(q, nodes):
    """Best AlsoAsked node for a question under the same-intent rule (exact wording first, then Jaccard >= JACCARD_DUP, shallowest)."""
    nq, cq = norm(q), content(q); best = None
    for it in nodes:
        sc = 1.0 if norm(it["q"]) == nq else jacc(cq, content(it["q"]))
        if sc >= JACCARD_DUP and (best is None or (sc, -it["prov"]["depth"]) > (best[0], -best[1]["prov"]["depth"])): best = (sc, it)
    return best[1] if best else None

def resource(url):
    """hubctl paa-resource: write AlsoAsked provenance into faq_sources items whose question matches the pull. No copy changes."""
    g = Gate(url)
    if not pulls(g.slug): sys.exit(f"no AlsoAsked pull for {g.slug}")
    nodes = pull_nodes(g.slug)
    before_raw = open(g.spec_path, "rb").read(); spec = json.loads(before_raw)
    snap = lambda s: (s["fields"].get("faq"), [(f.get("q"), f.get("source"), f.get("ref")) for f in s.get("faq_sources") or []])
    before = snap(spec); n = 0
    secs = (spec.get("keywords") or {}).get("secondaries_used") or []; rc = 0
    for f in spec.get("faq_sources") or []:
        m = match_pull(f["q"], nodes)
        if m:
            f["prov"] = {k: m["prov"][k] for k in ("tool", "query", "depth", "parent", "fetched", "original", "region", "language")}; n += 1
        elif f.get("source") == "paa":  # DataForSEO PAA with no AlsoAsked match: a secondary if its question carries one (PA12 test)
            k = next((k for k in secs if content(k) and content(k) <= content(f["q"])), None)
            if k: f["paa_ref"] = f.get("ref"); f["source"], f["ref"] = "secondary", k; rc += 1
    text = lambda s: (s["fields"].get("faq"), [f.get("q") for f in s.get("faq_sources") or []])
    assert text(spec) == (before[0], [q for q, _, _ in before[1]]), "paa-resource changed question or answer text: aborted, nothing written"
    out = json.dumps(spec, indent=1, ensure_ascii=False)
    assert json.loads(out)["fields"]["faq"].encode() == json.loads(before_raw)["fields"]["faq"].encode()
    open(g.spec_path, "w").write(out)
    print(f"{url}: {n} of {len(spec.get('faq_sources') or [])} FAQ items carry AlsoAsked provenance, {rc} reclassified paa -> secondary; question and answer text byte-identical")
    return 0

FORMAT_WORDS = ["landing page", "questionnaire", "survey", "quiz", "template", "form", "page"]

def candidate_phrases(spec):
    """PA3 synonym candidates for a page: the head phrase minus its format word, and any abbreviation in the primary
    (a token written in capitals in the page's own title or H1). Candidates only: applied after Divit approves the batch."""
    prim = norm((spec.get("keywords") or {}).get("primary") or ""); out = []
    for fw in FORMAT_WORDS:
        if re.search(r"(?<![a-z0-9])" + re.escape(fw) + r"s?(?![a-z0-9])", prim):
            rest = norm(re.sub(r"(?<![a-z0-9])" + re.escape(fw) + r"s?(?![a-z0-9])", " ", prim, count=1))
            if rest and rest != prim: out.append((rest, "minus-format"))
            break
    shown = " ".join(str(spec.get("fields", {}).get(k) or "") for k in ("h1", "meta_title", "title", "name"))
    for tok in prim.split():
        if len(tok) >= 2 and re.search(r"(?<![A-Za-z0-9])" + re.escape(tok.upper()) + r"(?![A-Za-z0-9])", shown) and tok not in [c for c, _ in out]:
            out.append((tok, "abbreviation"))
    return out

def synonym_candidates(urls):
    """Write rules/paa_synonym_candidates.json: per page, each candidate with how many extra questions it admits
    (pull + current FAQ) and how many of those fail PA4/PA5 (incl. the answer-source sense check). No question text."""
    cp = os.path.join(ROOT, "rules", "paa_synonym_candidates.json")
    doc = json.load(open(cp)) if os.path.exists(cp) else {"_note": "", "pages": {}}
    doc["_note"] = ("PA3 synonym CANDIDATES proposed by code (DECISIONS 2026-10-08): not applied; rules/paa_synonyms.json holds approved ones only. "
                    "status unsafe = a question it admits fails PA4/PA5 or the answer-source sense check; no-evidence = admits nothing in the pull or FAQ. Counts only.")
    for url in urls:
        g = Gate(url); cands = candidate_phrases(g.spec); rows = []
        pull = json.load(open(pull_path(g.slug))) if os.path.exists(pull_path(g.slug)) else None
        nodes = flatten(pull) if pull else []; ctx = {norm(n["q"]): n["ctx"] for n in nodes}
        seen, qs = set(), []
        for it in nodes + [{"q": f["q"], "ctx": ctx.get(norm(((f.get("prov") or {}).get("original")) or ""), "")} for f in faq_items(g.spec)]:
            if norm(it["q"]) not in seen: seen.add(norm(it["q"])); qs.append(it)
        for phrase, kind in cands:
            gc = Gate(url, [phrase]); hr = phrase_re(phrase); adm = bad4 = bad5 = 0
            for it in qs:
                q = norm(it["q"])
                if any(h.search(q) for h in g.heads) or not hr.search(q): continue
                adm += 1; rs = gc.judge({"q": it["q"], "ctx": it.get("ctx", ""), "source": "secondary"})
                bad4 += any(r[0] == "PA4" and r[1] == "reject" for r in rs); bad5 += any(r[0] == "PA5" and r[1] == "reject" for r in rs)
            rows.append({"phrase": phrase, "kind": kind, "admits": adm, "pa4": bad4, "pa5": bad5, "pulled": bool(pull),
                         "status": "unsafe" if bad4 or bad5 else ("safe" if adm else "no-evidence")})
        doc["pages"][g.slug] = rows
    json.dump(doc, open(cp, "w"), indent=1, ensure_ascii=False)
    allr = [r for v in doc["pages"].values() for r in v]
    print(f"synonym candidates: {len(allr)} on {len(doc['pages'])} pages; " + ", ".join(f"{k} {sum(r['status'] == k for r in allr)}" for k in ("safe", "unsafe", "no-evidence")))
    return 0

def faq_items(spec):
    """The spec's FAQ: questions from faq_sources (with their provenance), answers from fields.faq (window.awbFAQ JSON)."""
    m = re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;?\s*</script>", spec["fields"].get("faq", ""), re.S)
    faq = json.loads(m.group(1))["items"] if m else []
    src = {norm(f["q"]): f for f in spec.get("faq_sources") or []}
    out = []
    for i, f in enumerate(faq):
        s = src.get(norm(f["q"]), {})
        prov = s.get("prov") or {}
        out.append({"n": i + 1, "q": f["q"], "a": f.get("a", ""), "source": s.get("source", "unknown"), "prov": prov})
    return out

def run_pull(g):
    if not pulls(g.slug): sys.exit(f"no AlsoAsked pull for {g.slug}: pull it through ops/weekend.py aa <url>")
    raw = pull_nodes(g.slug); items, seen = [], {}   # primary pull plus the top-secondary pull, if any
    for it in sorted(raw, key=lambda x: x["prov"]["depth"]):  # AlsoAsked repeats wordings across branches: gate each wording once (shallowest)
        k = norm(it["q"])
        if k in seen: seen[k]["repeats"] = seen[k].get("repeats", 0) + 1; continue
        seen[k] = it; items.append(it)
    by_q = {}
    for it in sorted(items, key=lambda x: x["prov"]["depth"]):  # parents first, so PA2 sees the parent's verdict
        if it["prov"]["depth"] >= 2: it["parent_verdict"] = by_q.get(it["parent_q"], {}).get("verdict")
        it["reasons"] = g.judge(it); it["verdict"] = g.verdict(it["reasons"]); by_q[it["q"]] = it
    items = g.finish(sorted(items, key=lambda x: x["prov"]["depth"]))
    ok = sum(i["verdict"] == "pass" for i in items)
    extra = [("PA11", f"{len(raw)} nodes, {len(items)} distinct; {ok} passing AlsoAsked candidates (written questions fill the rest to {N_FAQ}, Divit 2026-10-16)")]
    return items, extra

def run_spec(g):
    items = faq_items(g.spec)
    vf = os.path.join(ROOT, "private", "alsoasked", "verdicts", g.slug + ".json")
    pv = {norm(i["q"]): i["verdict"] for i in json.load(open(vf))["items"]} if os.path.exists(vf) else {}
    ps = pulls(g.slug); sh = set().union(*(answer_shingles(d) for d in ps)) if ps else set()
    ctx = {norm(n["q"]): n["ctx"] for n in pull_nodes(g.slug)}
    for it in items:
        it["legacy"] = not g.new_writing   # ruling 15/18: a reviewed page's own FAQ is judged without the r18 checks
        it["ctx"] = ctx.get(norm((it["prov"] or {}).get("original") or ""), "")
        if (it["prov"] or {}).get("depth") == 2: it["parent_verdict"] = pv.get(norm(it["prov"].get("parent") or ""), "flag")
        it["reasons"] = g.judge(it)
        w = norm(re.sub(r"<[^>]+>", " ", html.unescape(it["a"]))).split() if it["source"] != WRITTEN else []   # PA1b: paa only (Divit 2026-10-16)
        hit = next((" ".join(w[i:i + 6]) for i in range(len(w) - 5) if " ".join(w[i:i + 6]) in sh), None)
        if hit: it["reasons"].append(("PA1b", "reject", f'answer shares a 6-word run with AlsoAsked answer text ("{hit}")'))
        it["verdict"] = g.verdict(it["reasons"])
    items = g.finish(items)
    page = []
    if len(items) != N_FAQ: page.append(("PA12", f"{len(items)} items, not exactly {N_FAQ}"))
    # PA11 (Divit 2026-10-16): no longer parks a page in spec mode; a rejected item is replaced with a written question
    if items and not re.match(r"^(what|which) (is|are) ", norm(items[0]["q"])): page.append(("PA12", "item 1 is not the definition"))
    if len(items) > 1:
        if not re.match(r"^how (do|can|to|should) (i |you |we )?(create|make|build|set up|design)", norm(items[1]["q"])): page.append(("PA12", "item 2 is not how-to-build"))
        if not re.search(r'href=["\'][^"\']*' + re.escape(g.hub_path) + r'/?["\']', items[1]["a"]): page.append(("PA12", "item 2 has no hub link"))
    # PA12 secondaries (Divit 2026-10-13, ruling 5): the page's Semrush workbook secondaries count, bar min(6, how many it has).
    # A page with NO Semrush secondaries uses the workbook's keyword ideas for the page as its secondaries (min 4, on-topic);
    # DataForSEO ideas and padding never count. Fewer than 4 on-topic workbook ideas = PA12 fails (the page stays parked).
    if g.workbook_secs:
        wb = [content(k) for k in g.workbook_secs]
        sec = sum(i["source"] == "secondary" or any(k and k <= content(i["q"]) for k in wb) for i in items)   # "secondary" labels: QC F2 checks them
        need = min(MIN_SECONDARIES, len(wb))
        if sec < need: page.append(("PA12", f"{sec} items carrying a workbook secondary, under {need}"))
    else:
        ideas = [k for k in workbook_ideas(g.url) if any(h.search(norm(k)) for h in g.heads) or g.pa3_widened(norm(k))]
        wb = [content(k) for k in ideas]
        sec = sum(any(k and k <= content(i["q"]) for k in wb) for i in items)
        # Divit 2026-10-16: a page short of keyword ideas is no longer parked (written questions fill it); with ideas, the bar stands
        if len(ideas) >= MIN_IDEAS and sec < MIN_IDEAS: page.append(("PA12", f"{sec} items carrying a workbook keyword idea, under {MIN_IDEAS}"))
    for it in items:
        first = norm(re.sub(r"<[^>]+>", " ", html.unescape(it["a"])))[:60]
        bad = [b for b in g.pt["answer_first_banned"] if first.startswith(b)]
        if bad: it["reasons"].append(("PA12", "reject", f'answer does not lead with the answer ("{bad[0]}")')); it["verdict"] = "reject"
    return items, page

def main(argv):
    if not argv: print(__doc__); return 0
    cand = []
    if "--cand" in argv:
        cp = os.path.join(ROOT, "rules", "paa_synonym_candidates.json")
        cand = [c["phrase"] for c in (json.load(open(cp))["pages"].get(argv[0].rsplit("/", 1)[1], []) if os.path.exists(cp) else []) if c.get("status") == "safe"]
    g = Gate(argv[0], cand); mode = ("spec" if "--spec" in argv else "pull") + ("+cand" if "--cand" in argv else "")
    items, page = run_spec(g) if mode.startswith("spec") else run_pull(g)
    c = {v: sum(i["verdict"] == v for i in items) for v in ("pass", "reject", "flag")}
    tally = {}
    for i in items:
        for rule in sorted({r[0] for r in i["reasons"] if r[1] == "reject"}): tally[rule] = tally.get(rule, 0) + 1
    vd = os.path.join(ROOT, "private", "alsoasked", "verdicts"); os.makedirs(vd, exist_ok=True)
    out = os.path.join(vd, g.slug + {"spec": ".faq", "pull": "", "spec+cand": ".faq.cand", "pull+cand": ".cand"}[mode] + ".json")
    json.dump({"url": g.url, "mode": mode, "date": datetime.date.today().isoformat(), "counts": c, "rejects_by_rule": tally,
               "page": [{"rule": r, "msg": m} for r, m in page],
               "items": [{k: i.get(k) for k in ("n", "q", "source", "asker", "verdict")} | {"depth": (i.get("prov") or {}).get("depth"),
                          "reasons": [{"rule": r, "kind": k, "msg": m} for r, k, m in i["reasons"]]} for i in items]},
              open(out, "w"), indent=1, ensure_ascii=False)
    ts = ", ".join(f"{k} {v}" for k, v in sorted(tally.items())) or "none"
    line = f"- {datetime.date.today().isoformat()} {g.url} [{mode}]: {len(items)} questions; pass {c['pass']}, reject {c['reject']}, flag {c['flag']}; rejects by rule: {ts}" + \
           (f"; page: {'; '.join(f'{r} {m}' for r, m in page)}" if page else "")
    sp = os.path.join(ROOT, "audit", "paa", "summary.md")
    if "--log" not in argv: sp = None   # read-only by default (ruling 10, Divit 2026-10-13): two clones co-editing this file conflicted
    if sp and not os.path.exists(sp): open(sp, "w").write("# PAA gate summary (qc/paa_gate.py)\n\nOne line per run; per-question verdicts stay in private/alsoasked/verdicts/.\n\n")
    if sp: open(sp, "a").write(line + "\n")
    if "--quiet" not in argv: print(line[2:])
    if mode.startswith("spec") and "--quiet" not in argv:
        for i in items:
            if i["verdict"] != "pass": print(f"  Q{i['n']} {i['verdict']}: {', '.join(sorted({r[0] for r in i['reasons'] if r[1] in ('reject', 'flag')}))}  [{i['q'][:60]}]")
    return 0 if not page and c["reject"] == 0 and c["flag"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
