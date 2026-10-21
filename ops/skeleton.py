"""skeleton.py: ruling 15 (Divit 2026-10-13), constrained writing. Code builds everything that can be decided before prose; the writer
writes prose only, section by section, and each section is QC'd (and autofixed) as it is written.

    python3 ops/skeleton.py build URL --by A-w-<n>     the skeleton: 10 FAQ slots (gate-passing AlsoAsked questions locked verbatim,
                                                       US display; then written slots up to 10, Divit 2026-10-16), hub + related links,
                                                       comparison table, hero default prompt, names; spec.pipeline = "r15"
    python3 ops/skeleton.py pack URL                   the compact page pack: locked FAQ, link plan, sections, claims menu, prevention
    python3 ops/skeleton.py set URL FIELD TEXT         write one field (plain text or HTML, exactly as given)
    python3 ops/skeleton.py answer URL N TEXT [--q QUESTION]   FAQ answer for slot N (--q: the question, written slots only; gated)
    python3 ops/skeleton.py set URL faq_q N QUESTION   the question of written slot N alone (gated as a written question)
    python3 ops/skeleton.py check URL SECTION          autofix (code) then QC filtered to that section: hero|features|why|usecases|howto|faq|all
    python3 ops/skeleton.py assemble URL               build fields.faq (awbFAQ embed) and faq_sources from the slots; links wrapped by code
    python3 ops/skeleton.py set URL quiz @FILE.json    quiz pages: the playable quiz JSON (docs/QUIZ.md) into spec.quiz; check URL quiz

Locked slots: the question text is fixed by code (an AlsoAsked question in its US-spelling display, ruling 14; the default definition
and how-to-build questions). The writer never edits it. Written slots (Divit 2026-10-16, "FULL-THROTTLE WRITING" item 1): when the
gate-passing PAA runs out, the writer writes the rest: plain, specific, useful, as a real searcher asks it, about THIS page's topic,
working in the suggested secondary naturally (at most one per question). It is gated like PAA plus PA18-PA21 (paa_gate) when set,
and recorded as source "written" (verbatim checks apply to paa only).
"""
import collections, contextlib, io, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H, paa_gate as P, park_rescue as R, semrush_questions as SQ, spelling as SP, quiz as QZ

def quiet(f, *a):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a)
def load(url): return json.load(open(H.spath(url)))
def save(url, s): json.dump(s, open(H.spath(url), "w"), indent=1, ensure_ascii=False)

HERO = {"Form": "Build a {p} that saves every response to a database I own.",
        "SurveyQuiz": "Build a {p} that collects every answer in a database I own.",
        "LP": "Build a {p} that saves every signup to a database I own.",
        "Auto": "Build {p} that runs on its own and logs every step."}
SECTIONS = {
    "hero": ["meta_title", "meta_description", "h1", "hero_description", "product_name", "breadcrumb", "explore_cta", "hero_prompt",
             "prompt_chip_1", "prompt_chip_2", "prompt_chip_3", "prompt_chip_4", "chip_adds", "chip_prompts"],
    "features": ["features_heading", "features_subheading", "feature_1", "feature_2", "feature_3", "feature_4", "feature_5", "feature_6"],
    "why": ["why_title", "why_description", "why_table"],
    "usecases": ["usecase_heading", "tab_label_1", "tab_label_2", "tab_label_3", "tab_label_4", "tab_content_1", "tab_content_2",
                 "tab_content_3", "tab_content_4", "mockup", "image_brief", "alt:", "images"],
    "howto": ["howto_title", "howto_description"] + [f"howto_step_{i}_{k}" for i in range(1, 8) for k in ("title", "des")],
    "faq": ["faq", "faq_sources"],
    "quiz": ["quiz"],   # playable quiz pages only (SurveyQuiz slug containing 'quiz'; docs/QUIZ.md, QC Z codes)
}
# T1 (ops/typeset.py) files width findings under its own field names (canary 2026-10-13: they never reached a section check)
for _sec, _extra in {"hero": ["prompt_chip"], "features": ["feature_title", "feature_body"], "usecases": ["tab_label", "tab_title", "tab_body"],
                     "howto": ["howto_step_des", "howto_step_title"], "faq": ["faq_heading", "faq_q", "faq_a"]}.items():
    SECTIONS[_sec] = SECTIONS[_sec] + _extra
DEF_RX = re.compile(r"^(what is|what's|what are|what does)\b")
HOW_RX = re.compile(r"^(how (do|to|can|would) (i|you|we)?\s*(make|create|build|set up|design|write))|^how to (make|create|build|set up)")

SMALL = {"a", "an", "the", "and", "or", "for", "of", "to", "in", "on", "with", "by", "at", "vs"}
PHRASAL = {"sign", "log", "check", "opt", "clock", "drop", "pick", "walk", "plug", "follow", "set", "roll", "move", "sign-"}
def _title(t):
    """HUB_RULES 4 title case (canary 2026-10-13: the skeleton set 'Customer service automation Builder'). A particle after a phrasal
    verb is capitalised, so is the last word and each part of a hyphenated compound; known acronyms take their house casing. A phrasal
    verb used as a noun modifier is hyphenated ("Safety Sign-In Sheet", "Potluck Sign-Up Sheet", "Check-In Form", decision 8
    follow-up 2026-10-15); as a verb (particle last, or followed by a small word) it stays open ("Sign Up for a Class")."""
    ws = t.split(); out = []
    for i, w in enumerate(ws):
        if any(ch.isupper() for ch in w[1:]): out.append(w); continue
        lw = w.lower(); particle = i > 0 and lw in ("in", "up", "on", "out", "off") and ws[i - 1].lower() in PHRASAL
        tw = "-".join(x[:1].upper() + x[1:].lower() for x in w.split("-")) if i == 0 or i == len(ws) - 1 or particle or lw not in SMALL else lw
        if particle and i + 1 < len(ws) and ws[i + 1].lower() not in SMALL and out and "-" not in out[-1]: out[-1] += "-" + tw
        else: out.append(tw)
    return case_acronyms(case_brands(" ".join(out)))
def _fits(text, field):
    """The text renders within the widest approved rendering of that field (ops/typeset.py ceilings, T1)."""
    try:
        import typeset as TS
        cfg = json.load(open(os.path.join(ROOT, "config", "typography.json"))); md = TS.mode(); F = cfg["ceilings"][md]["fields"]
        return field not in F or TS.width(text, TS.FIELDS[field], md) <= F[field]["px"] + 0.5
    except Exception: return True
GENERIC_SHORT = {"landing page", "page", "form", "survey", "quiz", "automation", "workflow", "workflow automation", "questionnaire", "application"}
TRAIL_GENERIC = {"form", "survey", "quiz", "questionnaire", "automation", "workflow", "landing page"}
TRAIL_HUB = {"landing page", "automation", "workflow"}   # a cut of these leaves the topic ("Podcast", "Invoice"): fine in a heading
def _shorter(disp, url=None):
    """Display-name variants, longest first (decision 8, 2026-10-15): the display name, then whole trailing generic words dropped one
    at a time ("Yes or No Questions Survey" -> "Yes or No Questions"). The first (head/modifier) word is never dropped (it was:
    "Build My or No Questions Survey", "Sign Up Sheet Questions"); never a bare hub phrase or another page's primary
    ('Approval Workflow' on document-approval-workflow, canary 2026-10-14)."""
    return [v for v, _ in _cuts(disp, url)]
def _cuts(disp, url=None):
    """(variant, the words cut so far) pairs behind _shorter."""
    ws = disp.split(); out = [(disp, ())]; sib = _sib_prims(url) if url else set(); cut = ()
    while len(ws) > 1:
        k = 2 if len(ws) > 2 and " ".join(ws[-2:]).lower() == "landing page" else 1
        tail = " ".join(ws[-k:]).lower()
        if tail not in TRAIL_GENERIC: break
        ws = ws[:-k]; cut += (tail,); v = " ".join(ws)
        if v.lower() not in GENERIC_SHORT and P.norm(v) not in sib and ws[-1].lower() not in SMALL: out.append((v, cut))
    return out
def _sib_prims(url):
    return {P.norm(p_["primary"]) for u, p_ in H.kmap().items() if u != url and p_.get("primary")}
def faq_heading_for(disp, url=None):
    """'{Topic} Questions, Answered' (HUB_RULES 5) at the faq_heading width, never a doubled word: a name ending in 'Questions' takes
    '<name>, Answered', a name holding 'Questions' elsewhere '<name> FAQ'. When the full name does not fit: a hub-noun cut keeps the
    topic ("Podcast Questions, Answered" on podcast-landing-page), then '<name> FAQ' before any other trailing cut ("Likert
    Questionnaire FAQ", not "Likert Questions, Answered"; "Fundraiser Order Form FAQ", decision 8)."""
    def forms(d):
        if re.search(r"\bquestions$", d, re.I): return [f"{d}, Answered", f"{d} FAQ"]
        if re.search(r"\bquestions?\b", d, re.I): return [f"{d} FAQ"]
        return [f"{d} Questions, Answered", f"{d} FAQ"]
    cs = _cuts(disp, url); hubcut = [v for v, cut in cs[1:] if set(cut) <= TRAIL_HUB]
    cands = forms(disp)[:1] + [f for v in hubcut for f in forms(v)[:1]] + forms(disp)[1:] + [f for v, _ in cs[1:] for f in forms(v)[::-1]]
    fb = [f for v in _fallback(cs[-1][0], url) for f in forms(v)[::-1]]
    return next((h_ for h_ in cands + fb if _fits(h_, "faq_heading")), min(cands + fb, key=len))   # nothing fits: the shortest (T1 flags it)
FALLBACK_TRAIL = TRAIL_GENERIC | {"sheet"}
LEAD_GENERIC = {"reasonable", "employee", "employees", "staff", "customer", "client", "general", "simple", "basic", "online",
                "standard", "official", "new", "free", "custom", "digital", "automated", "personal"}
def _fallback(disp, url=None):
    """Width fallback when no heading fits (decision 8 follow-up, 2026-10-15): a trailing generic noun ("Form", "Sheet")
    dropped first, then leading generic qualifiers ("Reasonable", "Employee"), the head modifier always kept and at least two words
    left: "Accommodation Request FAQ", "Handbook Acknowledgment FAQ". Never a bare hub phrase or another page's primary."""
    ws = disp.split(); sib = _sib_prims(url) if url else set(); out = []
    def ok(v): return len(v) >= 2 and " ".join(v).lower() not in GENERIC_SHORT and P.norm(" ".join(v)) not in sib and v[0].lower() not in SMALL and v[-1].lower() not in SMALL
    if len(ws) > 2 and ws[-1].lower() in FALLBACK_TRAIL and ok(ws[:-1]): ws = ws[:-1]; out.append(" ".join(ws))
    while len(ws) > 2 and ws[0].lower() in LEAD_GENERIC and ok(ws[1:]): ws = ws[1:]; out.append(" ".join(ws))
    return out
def explore_cta_for(disp, url=None):
    """'Build My <name>' within 34 characters (QC D3), the name cut only by whole trailing generic words (decision 8); a cut
    'Landing Page' leaves 'Page' first ("Build My Lead Generation Page", not "Build My Generation Landing Page")."""
    vs = [x for v, cut in _cuts(disp, url) for x in ([v + " Page", v] if cut[:1] == ("landing page",) else [v])]
    return next((c_ for c_ in (f"Build My {d}" for d in vs) if len(c_) <= 34), "Build Mine Now")

COUNTABLE = re.compile(r"\b(form|survey|quiz|page|website|site|workflow|system|process|pipeline|app|bot|tool|tracker|dashboard|portal|engine|questionnaire|application|sheet|checklist|template|report|letter|agreement|contract|waiver|release|log|list|plan|policy)s?$")
PLURAL = re.compile(r"\b(questions|pages|forms|surveys|quizzes|templates|ideas|examples|workflows|sheets|checklists)$")
AN_LETTER = set("aefhilmnorsx")            # letters whose name starts with a vowel sound: "an SEO", "an HR", "an FAQ"; "a UX", "a KPI"
WORD_ACRO = {"saas", "hipaa", "osha", "nasa", "scorm"}   # acronyms read as a word: "a HIPAA release form", "a SaaS", "an OSHA"
CONS_SOUND = re.compile(r"^(uni(form|que|on|t|vers|corn|f|lateral|sex)|use|usu|usa|uti|ura|uri|uro|euro|eu\b|ewe|one\b|one-|once|ouija|ufo)")
VOWEL_H = re.compile(r"^(hour|honest|honou?r|heir)")
def _a(primary):
    """Article by sound, not letter (decision 8: "an uniform order form"): a uniform, a user, a one-page, a European, an hour,
    an honest; initialisms by their first letter's name (an SEO, an HR, a UX, a W-9), acronyms read as words by sound (a HIPAA)."""
    w = (primary.split() or [""])[0]; lw = w.lower(); cased = case_primary(w)
    if lw[:1].isdigit(): return "an" if re.match(r"^(8|11|18)(\D|$)|^8\d", lw) else "a"
    if lw not in WORD_ACRO and (cased.isupper() or (lw in ACRO and ACRO[lw])) and len(lw.replace("-", "")) <= 5 and lw not in ("it", "us"):
        return "an" if lw[0] in AN_LETTER else "a"
    if lw == "it" and cased == "IT": return "an"
    if VOWEL_H.match(lw): return "an"
    if CONS_SOUND.match(lw): return "a"
    return "an" if lw[:1] in "aeiou" else "a"
def _art(primary):
    return (_a(primary) + " ") if COUNTABLE.search(P.norm(primary)) and not PLURAL.search(P.norm(primary)) else ""
def case_primary(p):
    """A primary keyword in running text: brands in their own casing ("a LinkedIn landing page", not "a linkedin landing page"),
    acronyms in house casing (QC R15), and a leading 'it' is the department (IT automation, IT request form; case_acronyms never
    cases 'it' in a sentence)."""
    return re.sub(r"^it\b(?=\s+\w)", "IT", case_acronyms(case_brands(p)))
def def_questions(prim):
    """The two default definition slots when no candidate fills them (plan_slots), acronyms cased (decision 8, QC R15)."""
    prim = P.head_phrase(prim)   # ruling 4 (Divit 2026-10-21): "best startup landing pages" -> "What is a startup landing page?"
    pc = case_primary(prim); art = _art(prim); plural = bool(PLURAL.search(P.norm(prim)))
    d = f"What {'are' if plural else 'is'} {art}{pc}?"
    h = f"How do I create {art}{pc}?" if art or plural else f"How do I set up {pc}?"
    return d[:1].upper() + d[1:], h
def hero_prompt_for(prim, hub):
    """The hero default prompt (ruling 15, HUB_RULES 5): 'Build' + the primary with the right article: by sound ("a uniform"), none on a
    mass noun ("Build SEO automation"), "a set of" before a plural ("Build a set of poll questions"), acronyms cased (decision 8)."""
    prim = P.head_phrase(prim)   # ruling 4 (Divit 2026-10-21): "Build a startup landing page ...", never "a set of best ..."
    tmpl = HERO[hub]; pc = case_primary(prim); plural = bool(PLURAL.search(P.norm(prim)))
    if hub == "Auto":
        if plural: tmpl = "Build {p} that run on their own and log every step."
        elif re.search(r"\b(workflow|system|process|pipeline|app|bot|tool|tracker|dashboard|portal|engine)$", P.norm(prim)):
            tmpl = "Build {a} {p} that runs on its own and logs every step."   # countable primary takes an article (canary 2026-10-14)
    else:
        tmpl = tmpl.replace("Build a {p}", "Build a set of {p}" if plural else "Build {a} {p}")
    return "<p>" + tmpl.format(p=pc, a=_a(prim)) + "</p>"
def built_fields(url):
    """Every code-built hero/FAQ field for a page, read-only (decision 8 golden cases and old/new reports): what cmd_build sets
    when the field is empty."""
    km = H.kmap()[url]; prim = km["primary"]; hub = H.hub_of(url); disp = _title(km.get("display_name") or prim); d, h = def_questions(prim)
    return {"faq_heading": faq_heading_for(disp, url), "explore_cta": explore_cta_for(disp, url), "hero_prompt": hero_prompt_for(prim, hub),
            "breadcrumb": disp, "product_name": f"{disp} Builder", "def_q": d, "how_q": h, "h1_phrase": h1_phrase_for(prim)}
def h1_phrase_for(prim):
    """Ruling 4 (Divit 2026-10-21): the keyword phrase the H1 carries, title case: the head phrase of a list-style primary
    ("Startup Landing Page" for "best startup landing pages"), the primary itself otherwise. QC K1 accepts either in the H1."""
    return _title(P.head_phrase(prim))

ACRO = P.r18()["acronyms"]   # rules/paa_patterns.json (ruling 18 part 4e: CFOs, KYC ...); None = never cased (it, us)
def case_acronyms(text):
    """Known acronyms in their house casing, plurals too ("cfos" -> "CFOs", "kpis" -> "KPIs"); words already cased are kept."""
    def one(m):
        w = m.group(0); lw = w.lower()
        if lw in ACRO: return ACRO[lw] or w
        if lw.endswith("s") and ACRO.get(lw[:-1]): return ACRO[lw[:-1]] + "s"
        return w
    return re.sub(r"(?<![A-Za-z0-9'-])[A-Za-z0-9][A-Za-z0-9'-]*(?![A-Za-z0-9'-])", one, text)
# Brand casing for code-built text (brand primaries: "What is a LinkedIn landing page?", "Build a YouTube landing page ...").
# The list is rules/paa_blocklist.json pa14_brands (the one brand list) plus WhatsApp; minus entries that are also everyday words
# ("word", "teams", "square", "notion", "indeed" ...), which are never cased from a lowercase primary. Brands not written as one
# capital then lowercase take their casing from BRAND_IRREGULAR; every other brand is each word capitalised (Shopify, Google Sheets).
BRAND_COMMON_WORD = {"word", "docs", "sheets", "teams", "square", "interact", "tally", "notion", "gemini", "claude", "copilot",
                     "framer", "indeed", "apple", "zoom", "excel", "slack", "stripe", "make.com", "monday.com"}
BRAND_IRREGULAR = {"linkedin": "LinkedIn", "tiktok": "TikTok", "youtube": "YouTube", "whatsapp": "WhatsApp", "hubspot": "HubSpot",
                   "paypal": "PayPal", "quickbooks": "QuickBooks", "chatgpt": "ChatGPT", "openai": "OpenAI", "gpt": "GPT", "adp": "ADP",
                   "ifttt": "IFTTT", "surveymonkey": "SurveyMonkey", "docusign": "DocuSign", "bamboohr": "BambooHR", "wordpress": "WordPress",
                   "wpforms": "WPForms", "pandadoc": "PandaDoc", "sharepoint": "SharePoint", "onedrive": "OneDrive", "ebay": "eBay",
                   "iphone": "iPhone", "ziprecruiter": "ZipRecruiter", "n8n": "n8n", "jotform": "Jotform"}
BRAND_PAGE_WORDS = {"excel", "slack", "stripe"}   # page primaries (excel automation, slack automation, stripe donation form): cased as the first word only
BRANDS = {b: BRAND_IRREGULAR.get(b) or " ".join(x[:1].upper() + x[1:] for x in b.split())
          for b in [*json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rules", "paa_blocklist.json")))["pa14_brands"], "whatsapp"]
          if b not in BRAND_COMMON_WORD}
_BRAND_RX = re.compile(r"(?<![A-Za-z0-9'.-])(" + "|".join(re.escape(b) for b in sorted(BRANDS, key=len, reverse=True)) + r")(?![A-Za-z0-9'-])", re.I)
_BRAND_LEAD_RX = re.compile(r"^(" + "|".join(sorted(BRAND_PAGE_WORDS)) + r")\b(?=\s+\w)", re.I)
def case_brands(text):
    """Known brands in their own casing (LinkedIn, TikTok, YouTube, HubSpot, Google Sheets); a brand-and-everyday word (Excel, Slack,
    Stripe) only as the first word of a primary ("excel automation" -> "Excel automation"; "help teams excel" untouched)."""
    text = _BRAND_RX.sub(lambda m: BRANDS[m.group(0).lower()], text)
    return _BRAND_LEAD_RX.sub(lambda m: m.group(0)[:1].upper() + m.group(0)[1:].lower(), text)
def clean_question(raw):
    """A Semrush question as a starting point only (keyword-sourced: the writer may reword it naturally, head phrase kept, backlog line 91):
    years stripped, acronyms cased (plurals too, ruling 18), first letter capitalised, a question mark."""
    q = re.sub(r"\s+", " ", re.sub(r"\b(19|20)\d\d\b", " ", raw)).strip(" ?")
    q = case_acronyms(q)
    return q[:1].upper() + q[1:] + "?"

def spec_view(g):
    """What paa_gate.run_spec reads when it gates a spec's FAQ (Divit 2026-10-14 step 4): every answer source the saved pulls hold per
    wording (run_spec looks one up by the item's provenance wording, last node wins; run_pull gates each wording once, on its first
    shallowest node, which may carry no answer source: invoice-approval-workflow Q2 PA5, petition-form Q3 PA4), and the parent
    verdicts of the saved pull verdicts file (PA2; 'flag' when the file or the parent is missing)."""
    ctx = collections.defaultdict(list)
    for n in (P.pull_nodes(g.slug) if P.pulls(g.slug) else []):
        if n["ctx"] not in ctx[P.norm(n["q"])]: ctx[P.norm(n["q"])].append(n["ctx"])
    vf = os.path.join(ROOT, "private", "alsoasked", "verdicts", g.slug + ".json")
    try: pv = {P.norm(i["q"]): i["verdict"] for i in json.load(open(vf))["items"]}
    except Exception: pv = {}
    return ctx, pv
_WORSE = {None: 0, "pass": 0, "flag": 1, "reject": 2}
def spec_reasons(g, c, view, live=None):
    """The gate's reasons for candidate c as run_spec gives them once c is in the FAQ: the text the spec carries (US display, cleaned
    Semrush form: PA14/PA16 read the raw text), its faq_sources label, EVERY answer source the pull holds for its wording (PA4/PA5;
    a superset of the one run_spec picks), and the worse of the saved and the live parent verdict (PA2). The within-page caps of
    Gate.finish (PA6 respondents, PA8 brands, PA9) are applied by plan_slots."""
    ctx, pv = view; prov = c.get("prov") or {}
    it = {"q": c["q"], "source": "alsoasked" if c["kind"] == "alsoasked" else "keyword", "prov": prov}
    if prov.get("depth") == 2:
        pn = P.norm(prov.get("parent") or ""); it["parent_verdict"] = max(pv.get(pn, "flag"), (live or {}).get(pn), key=_WORSE.get)
    out = []
    for cx in ctx.get(P.norm(prov.get("original") or ""), []) or [""]:
        out += [r for r in g.judge(dict(it, ctx=cx)) if r not in out]
    return out

def candidates(url, extra=()):
    """FAQ candidates: AlsoAsked pull and Semrush questions, passing first, then flagged (ruling 18 part 5: flags may fill slots; the
    shapes code drops are gate rejects). extra: unapproved synonym phrases, only for ruling 12's 'feasibility with' column."""
    s = url.rsplit("/", 1)[1]; g = P.Gate(url, extra); out = []; live = {}
    if P.pulls(s):
        items, _ = quiet(P.run_pull, g); live = {P.norm(i["q"]): i["verdict"] for i in items}
        for i in items:
            if i["verdict"] not in ("pass", "flag"): continue
            orig = (i.get("prov") or {}).get("original") or i["q"]
            fl = sorted({P.flag_subtype(r[0], r[2], i["q"]) for r in i["reasons"] if r[1] == "flag"})
            out.append({"kind": "alsoasked", "q": SP.display(orig), "ref": orig, "prov": i.get("prov"), "locked": True, "flagged": fl})
    for x in SQ.usable(s):
        rs = g.judge({"q": x["q"], "source": "keyword", "n": 5})
        if any(r[1] == "reject" for r in rs): continue
        fl = sorted({P.flag_subtype(r[0], r[2], x["q"]) for r in rs if r[1] == "flag"})
        out.append({"kind": "semrush", "q": clean_question(x["q"]), "ref": x["q"], "prov": x["prov"], "locked": False, "flagged": fl})
    # Divit 2026-10-14 step 4: judged again as the gate's `paa --spec` will judge it once it sits in the FAQ (spec_reasons)
    view = spec_view(g); judged = []
    for c in out:
        rs = spec_reasons(g, c, view, live)
        if any(r[1] == "reject" for r in rs): continue
        c["flagged"] = sorted(set(c["flagged"]) | {P.flag_subtype(r[0], r[2], c["q"]) for r in rs if r[1] == "flag"}); judged.append(c)
    out = judged
    # a capitalised-name flag (PA14) is usually another company ("Does automation Direct accept returns?"): never a skeleton slot
    out = [c for c in out if "PA14 capitalised name" not in (c.get("flagged") or [])]
    # Divit 2026-10-13: flagged questions may fill slots, after passing questions and secondaries; marked in spec and pack
    return [c for c in out if not c["flagged"]] + [c for c in out if c["flagged"]]

def related_targets(url, n=3):
    """Live child pages to link from items 3-10, anchored with their exact primary: same cluster first, then keyword overlap."""
    km = H.kmap(); me = km.get(url) or {}; live = [u for u in H.live_urls() if u in km and u != url and u.count("/") == 2]
    mine = P.content(" ".join([me.get("primary", "")] + [x["kw"] for x in me.get("secondaries") or []]))
    def score(u):
        p_ = km[u]; same_cluster = bool(me.get("cluster")) and p_.get("cluster") == me.get("cluster")
        return (same_cluster, H.hub_of(u) == H.hub_of(url), len(mine & P.content(p_["primary"])))
    ranked = sorted(live, key=score, reverse=True)
    return [{"url": u, "anchor": km[u]["primary"]} for u in ranked if score(u)[2] > 0 or score(u)[0]][:n]

def default_table(url):
    import table as TB
    d = H.CFG["hubs"][H.hub_of(url)]["repo_dir"]; L = TB.lib(d)
    trios = collections.Counter(); rowsets = collections.Counter()
    for f in os.listdir(os.path.join(ROOT, "specs", d)):
        try: t = json.load(open(os.path.join(ROOT, "specs", d, f))).get("table") or {}
        except Exception: continue
        if t.get("vs") and len(t["vs"]) == 3 and all(c in L["competitors"] for c in t["vs"]): trios[tuple(t["vs"])] += 1
        if t.get("rows"): rowsets[tuple(t["rows"])] += 1
    top = (H.kmap().get(url) or {}).get("top10") or []
    rows = list(rowsets.most_common(1)[0][0]) if rowsets else ["build", "limits", "data", "ownership"]
    keys = [r.split("=")[0] for r in rows]
    pn = P.norm((H.kmap().get(url) or {}).get("primary") or "")
    def fits_page(c):   # canary 2026-10-13: no employee-listening tool on an event survey, no quiz specialist on a survey
        cats = set(L["competitors"][c].get("categories") or [])
        if "employee" in cats and not re.search(r"employee|staff|engagement|360|pulse|exit|onboarding|culture|hr\b|workplace", pn): return False
        if cats == {"quiz-tool"} and "quiz" not in pn: return False
        return True
    has_all = lambda c: fits_page(c) and all(k in (L["competitors"][c].get("facts") or {}) for k in keys)   # a competitor without a fact for a row cannot be tabled
    ranking = [c for c in L["competitors"] if has_all(c) and any(c.lower().split()[0] in (u or "").lower() for u in top)]
    pool = [c for c in (trios.most_common(1)[0][0] if trios else []) if c not in ranking and has_all(c)]
    pool += [c for c in L["competitors"] if c not in ranking and c not in pool and has_all(c)]
    vs = (ranking + pool)[:3]
    return vs, rows

def plan_slots(url, cap=10, extra=()):
    """The skeleton's FAQ slots in fill order (no writes), Divit 2026-10-16 item 1: definition, how-to-build, the gate-passing
    AlsoAsked questions (verbatim, each skipped when same-intent as a slot already taken, paa_gate.near_dup), then WRITTEN slots up to
    10: each suggests one secondary the page does not carry yet (MSV high to low, gate-clean as a keyword), then a Semrush question
    as a starting point (the writer may reword it), then free written slots. Flagged PAA no longer fills a slot (a written question
    does). cap None = the feasibility count: every PAA slot plus every suggestion, padded with free written slots to 10; every page
    with a plan can reach 10."""
    km = H.kmap().get(url) or {}; prim = km.get("primary") or url.rsplit("/", 1)[1].replace("-", " ")
    g = P.Gate(url, extra); cands = candidates(url, extra); have = []; slots = []
    full = lambda: cap is not None and len(slots) >= cap
    # Gate.finish's within-page caps, as run_spec applies them to the FAQ (Divit 2026-10-14 step 4): PA6 respondents, PA8 brands
    resp = lambda q: g.asker(P.norm(q or "")) == "respondent"; brand = lambda q: any(P.has(b, P.norm(q or "")) for b in g.library)
    capped = lambda c: (resp(c["q"]) and sum(resp(x.get("q")) for x in slots) >= P.MAX_RESPONDENT) or (brand(c["q"]) and sum(brand(x.get("q")) for x in slots) >= P.MAX_BRANDED)
    paa = [c for c in cands if c["kind"] == "alsoasked" and not c.get("flagged")]
    pick = lambda rx: next((c for c in paa if rx.search(P.norm(c["q"])) and c not in have and not capped(c)), None)
    d = pick(DEF_RX); have += [d] if d else []
    dq, hq = def_questions(prim)
    slots.append(d or {"kind": "definition", "q": dq, "ref": prim, "locked": True})
    h = pick(HOW_RX); have += [h] if h else []
    slots.append(h or {"kind": "definition", "q": hq, "ref": prim, "locked": True})
    near = lambda q: any(P.near_dup(q, x["q"], prim) or P.jacc(P.content(q), P.content(x["q"])) >= P.JACCARD_DUP for x in slots if x.get("q"))
    for c in paa:
        if full(): break
        if c in have or near(c["q"]) or capped(c): continue
        slots.append(c)
    carried = [P.content(x["q"]) for x in slots]
    for x in sorted(km.get("secondaries") or [], key=lambda x: -(x.get("msv") or 0)):
        if full(): break
        c = P.content(x["kw"])
        if not c or any(c <= q for q in carried) or any(r[0] in R.KW_RULES and r[1] == "reject" for r in g.judge({"q": x["kw"], "source": "secondary"})): continue
        carried.append(c); slots.append({"kind": "written", "q": None, "ref": x["kw"], "secondary": x["kw"], "locked": False})
    for c in [c for c in cands if c["kind"] == "semrush" and not c.get("flagged")]:
        if full(): break
        if near(c["q"]) or capped(c): continue
        slots.append({"kind": "written", "q": None, "ref": None, "secondary": None, "hint": c["q"], "locked": False})
    while len(slots) < (cap if cap is not None else P.N_FAQ):
        slots.append({"kind": "written", "q": None, "ref": None, "secondary": None, "locked": False})
    return slots

def quiz_plan(url, prim):
    """The quiz section of the skeleton: suggested type from the primary keyword (rules/quiz.json type_hints), counts, limits."""
    pn = P.norm(prim); th = QZ.R["type_hints"]
    typ = next((t for t in ("knowledge", "matching") if any(re.search(r"\b" + re.escape(w) + r"\b", pn) for w in th[t])), "matching")
    return {"type": typ, "questions": "6-10", "options": "2-6 per question", "results": "2-6",
            "promise": f"the quiz plays the page's promise: a {prim} a visitor can take, whose results answer what the H1 says it builds",
            "lengths": {k: v for k, v in QZ.R["lengths"].items() if not k.startswith("_")}}

def slots_possible(url, extra=()):
    """How many FAQ slots the skeleton can fill (no writes); park_rescue.feasibility returns the same number."""
    return len(plan_slots(url, None, extra))

def cmd_build(a):
    url = a[0]; by = a[a.index("--by") + 1] if "--by" in a else None
    if not by: sys.exit("build URL --by A-w-<n>")
    km = H.kmap().get(url) or sys.exit("not in the keyword map")
    sp = H.spath(url)
    if os.path.exists(sp) and json.load(open(sp)).get("pipeline") != "r15" and "--adopt" not in a:
        if "--fresh" not in a: sys.exit(f"{sp} is an old draft: rerun with --fresh (archive it, start clean) or --adopt (keep its prose, finish on the pipeline)")
        arch = os.path.join(os.path.dirname(sp), "_archive"); os.makedirs(arch, exist_ok=True)
        os.replace(sp, os.path.join(arch, os.path.basename(sp).replace(".json", f".{H.now()[:10]}.json")))
        print(f"archived the old draft to {os.path.relpath(arch, ROOT)}/")
    if not os.path.exists(H.spath(url)):
        subprocess.run([sys.executable, os.path.join(ROOT, "ops", "hubctl.py"), "init", url, "--by", by], check=True)
    s = load(url); prim = km["primary"]; hub = H.hub_of(url)
    slots = plan_slots(url, 10)
    if len(slots) < 10: sys.exit(f"refused: only {len(slots)} FAQ slots (the skeleton needs 10)")
    hubpath = H.CFG["hubs"][hub]["path"]; hubtext = H.CFG["hubs"][hub]["hub_link_text"]
    for i, sl in enumerate(slots, 1): sl.update({"n": i, "a": sl.get("a") or "", "link": None})
    slots[1]["link"] = {"url": "https://emergent.sh" + hubpath, "anchor": hubtext, "write_as": f"Emergent's {hubtext}"}
    rel = related_targets(url); free = [sl for sl in slots[2:] if not sl["link"]]
    for t, sl in zip(rel, free[1::3] or free):
        sl["link"] = {"url": "https://emergent.sh" + t["url"], "anchor": t["anchor"]}
    s["pipeline"] = "r15"; s["faq_plan"] = slots
    F = s["fields"]; B = built_fields(url)   # decision 8 (2026-10-15): deterministic builders, golden kind skel-field
    if not s.get("faq_heading"): s["faq_heading"] = B["faq_heading"]
    F["breadcrumb"] = F.get("breadcrumb") or B["breadcrumb"]; F["product_name"] = F.get("product_name") or B["product_name"]
    if not F.get("explore_cta"): F["explore_cta"] = B["explore_cta"]
    if not F.get("hero_prompt"): F["hero_prompt"] = B["hero_prompt"]
    s.setdefault("keywords", {})["primary"] = prim
    save(url, s)
    vs, rows = default_table(url)
    if len(vs) == 3:   # in-process: a library name may hold commas ("AI site builders (Wix, Framer)") that the CLI would split
        import table as TB
        try:
            html = TB.render(H.CFG["hubs"][hub]["repo_dir"], vs, rows)
            s2 = load(url); s2["fields"]["why_table"] = html; s2["table"] = {"vs": vs, "rows": rows, "variant": None}; save(url, s2)
        except Exception as e: print(f"table not built: {e}")
    s = load(url)
    if QZ.is_quiz_page(url):   # Divit 2026-10-14 step 5: the writer fills spec.quiz (6-10 questions), QC Z codes check it
        s.setdefault("quiz", None); s["quiz_plan"] = quiz_plan(url, prim); save(url, s); s = load(url)
    s.setdefault("skeleton", {}).update({"built_by": by, "built": H.now(), "slots": len(slots), "flagged": sum(1 for x in slots if x.get("flagged")),
                                                        "flag_subtypes": sorted({f for x in slots for f in (x.get("flagged") or [])}),
                                                        "locked": sum(1 for x in slots if x["locked"]), "table": bool(s.get("table"))})
    save(url, s)
    print(f"{url}: skeleton built ({sum(1 for x in slots if x['locked'])} locked FAQ questions, {sum(1 for x in slots if not x['locked'])} written slots, "
          f"{sum(1 for x in slots if x.get('flagged'))} FLAGGED (cannot ship until Divit ticks the subtype), "
          f"{sum(1 for x in slots if x['link'])} links, table {'yes' if s.get('table') else 'NO'}); next: skeleton.py pack {url}")

def cmd_pack(a):
    url = a[0]; s = load(url); km = H.kmap().get(url) or {}
    caps = json.load(open(os.path.join(ROOT, "rules", "capabilities.json")))["approved"]
    out = [f"# Page pack (ruling 15): {url}", "", f"Primary: {km.get('primary')} | intent: {km.get('intent')} | angle note: {(km.get('angle') or '')[:300]}", "",
           "## Sections, in order (write one, run `skeleton.py check URL <section>`, fix to 0, then the next)",
           "1 hero: meta_title, meta_description, h1, hero_description, prompt_chip_1-4 + chip_adds (hero_prompt, product_name, breadcrumb, explore_cta are set by code)",
           *([f"Ruling 4 (Divit 2026-10-21): the H1 carries the head phrase \"{h1_phrase_for(km['primary'])}\", never the modifiers of \"{km['primary']}\"; the full keyword goes in meta_title, meta_description and hero_description."] if km.get("primary") and P.head_phrase(km["primary"]) != km["primary"] else []),
           "2 features: features_heading, features_subheading, feature_1-6", "3 why: why_title, why_description (the table is built by code)",
           "4 usecases: usecase_heading, tab_label_1-4, tab_content_1-4, mockup, image_brief", "5 howto: howto_title, howto_description, 7 steps",
           "6 faq: one answer per slot with `skeleton.py answer URL N TEXT` (written slots: add --q QUESTION); then `skeleton.py assemble URL`; then `skeleton.py check URL faq`",
           *(["7 quiz (quiz pages): spec.quiz, the playable quiz JSON, with `skeleton.py set URL quiz @FILE.json`; then `skeleton.py check URL quiz` (see the Quiz section below)"] if QZ.is_quiz_page(url) else []), "",
           "## FAQ slots (locked questions are fixed; write the answer only. Written slots: you write the question, Divit 2026-10-16)",
           "Written questions: plain, specific and useful, phrased the way a real person building this asks it; about THIS page's topic, never hub-level generic;",
           "at most one secondary keyword per question, worked in naturally (no stuffing); builder intent; US audience; no state-specific, legal, medical or",
           "financial advice; no other company's pricing; no brand names; never another page's primary; never the same intent as another question here or on",
           "a sibling page. `answer --q` gates the question (PA3-PA21) and refuses a reject. Answers: answer-first, truthful, a source for every fact, Emergent",
           "claims from the claims menu only."]
    for sl in s.get("faq_plan") or []:
        if sl["locked"] or (sl["kind"] == "written" and sl.get("q")): q = sl["q"]
        elif sl["kind"] == "semrush": q = f"[Semrush: keep or reword naturally (head phrase stays; --q): {sl['q']}]"
        elif sl["kind"] == "secondary": q = f"[you write a question carrying every word of: {sl['ref']}]"
        else: q = "[WRITTEN: you write the question" + (f"; work in the secondary '{sl['secondary']}'" if sl.get("secondary") else "") + \
                  (f"; a starting point you may reword: {sl['hint']}" if sl.get("hint") else "") + "]"
        if sl.get("flagged"): q += f"  [FLAGGED: {', '.join(sl['flagged'])}; write it like any other; it waits for Divit's packet tick]"
        ln = f" | LINK: write the words \"{sl['link'].get('write_as') or sl['link']['anchor']}\" in the answer (code makes them the link)" if sl.get("link") else ""
        out.append(f"{sl['n']:2d}. ({sl['kind']}{', locked' if sl['locked'] else ''}) {q}{ln}")
    if QZ.is_quiz_page(url):
        out += quiz_pack(s)
    out += ["", "## Claims menu (cite the id in spec.claims_used; say nothing about Emergent outside these)"] + [f"- {c['id']}: {c['claim']}" for c in caps]
    out += ["", "## Third-party facts", "Every fact about another product, a law or a professional standard needs spec.domain_sources {claim, source_url, date, quote}: `quote` is the exact span from the source that states it. No span, no claim.",
            "Stay inside the span: a detail the quote does not state (how a file is sent, 'by API', a date, a number) needs its own source or comes out. GOOD: 'the buyer sends the approved invoice file to the bank' (the span). BAD: 'Emergent sends that file through the bank's API' (the span says nothing about an API).",
            "Never claim a step stops, prevents or eliminates a risk (fraud, fakes, spam, errors, duplicates) unless a source says so: say what it does. GOOD: 'confirmation keeps typed-in fake addresses from counting'. BAD: 'confirmation stops throwaway accounts' (a disposable inbox confirms too). QC R15 flags it.",
            "Never put an Emergent line in an answer that names another brand: next to a cited competitor fact it reads as a comparison (QC R15, CONTENT_DEFECTS #8). Put the Emergent line in an answer that names no other company.",
            "Every Emergent sentence maps to a claim above in its own wording (QC C6). Emergent itself only builds, writes, changes, connects, exports or hosts; what the finished app does at run time is 'the app ...'. GOOD: 'The app reads your chart of accounts through the ledger's API.' BAD: 'Emergent reads your chart of accounts before the first rule runs.' A plan claim ends at its wording: GOOD 'The free tier covers building and publishing.' BAD '... which lets you run one control for a full cycle.' No billing words (overage, bill, per-seat, credits) outside an approved wording.",
            "Every third-party fact is bound to a quote (QC C7). Never answer 'Does/Can <category> software ...?' with a flat No or Yes unless a quote says it: GOOD 'It depends on the product: ...', or answer for the app Emergent builds. A sentence about a product category with never, only, all or 'two kinds' needs a quote that says it. A sentence naming a vendor, law or regulator rests on a quote, and its numbers and qualifiers ('central', 'once a year', 'every') are in that quote."]
    pm = os.path.join(ROOT, "docs", "PREVENTION.md")
    if os.path.exists(pm):
        txt = open(pm).read(); m = re.search(r"## (?:\d+\.\s*)?Page-pack instructions.*?(?=\n## |\Z)", txt, re.S)
        if m: out += ["", m.group(0).strip()]
    p = os.path.join(ROOT, ".cache", "packs", url.rsplit("/", 1)[1] + ".r15.md"); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write("\n".join(out)); print(p)

def quiz_pack(s):
    qp = s.get("quiz_plan") or {}; L = QZ.R["lengths"]
    return ["", "## Quiz (this is a playable quiz page; docs/QUIZ.md has the schema and two worked examples in ops/quiz/fixtures/)",
        f"Suggested type: {qp.get('type', 'matching')} (knowledge = one correct option per question and score bands; matching = each option maps to a result key). Choose the other type only if the page's promise needs it.",
        "Shape: {\"version\": 1, \"type\", \"title\", \"intro\", \"questions\": [{\"text\", \"options\": [{\"text\", \"correct\": true | \"result\": key}], \"explanation\", \"source\": {\"url\", \"quote\"}, \"derivable\"}], \"results\": [{\"key\", \"title\", \"description\", \"min\", \"max\"}]}.",
        "Counts: 6-10 questions, 2-6 options each, 2-6 results. Knowledge: bands (min-max) cover every score 0..N once, no gaps, no overlap. Matching: every result is mapped by options in at least 2 questions, and some set of answers must lead to it (ties go to the result listed first).",
        "Promise: the title and results deliver what the H1 and the primary keyword promise (a vocabulary quiz tests vocabulary; a style quiz names a style). The results read as the page's own example of what Emergent builds, written for the person taking the quiz.",
        "Sources: every knowledge question states a fact (its answer), so it carries source {url, quote}: the quote is the exact span (6+ words) from the page that states the answer. A question whose answer follows by calculation or logic (math) may instead be \"derivable\": true with the working in its explanation. In any quiz, an explanation that states a fact (a number, a study, 'the largest', 'means') carries a source. No span, no fact: cut it. `hubctl sources-check URL` link-checks the quiz sources too.",
        "Never diagnose (QC Z5, P0): no medical, psychological or clinical claims. Never 'you have X', 'you are depressed/ADHD/anxious/a narcissist', 'signs of', 'a test for'. Personality-style results are preferences ('your answers lean toward ...'), never conditions or fixed traits. GOOD: 'Your answers lean toward quiet evenings and small groups.' BAD: 'You are an introvert with social anxiety.'",
        "No trademarked characters, franchises or branded tests as results (Hogwarts houses, Marvel heroes, Myers-Briggs types) unless the page is about them (QC Z8). Keep every question and result suitable for a school-age reader.",
        f"Mobile at 390 px (QC Z6): title <= {L['title']}, intro <= {L['intro']}, question <= {L['question']}, option <= {L['option']}, explanation <= {L['explanation']}, result title <= {L['result_title']}, result description <= {L['result_description']} characters. Plain text only: no HTML, no angle brackets; house style applies (straight quotes, no dashes or exclamation marks, serial comma, US spelling, no we/our).",
        "GOOD option set: four plausible answers of the same kind and length. BAD: one obviously silly option, or 'All of the above'."]

def cmd_set(a):
    url, field, text = a[0], a[1], a[2]; s = load(url)
    if field == "faq_q":   # Divit 2026-10-16: set URL faq_q N QUESTION (a written slot's question, gated)
        set_written_q(url, s, int(text), a[3]); save(url, s); print(f"slot {text} question set"); return
    if field in ("hero_prompt", "why_table", "faq", "slug", "category"): sys.exit(f"refused: {field} is built by code (ruling 15)")
    if field == "chip_adds": s["chip_adds"] = json.loads(text)
    elif field == "image_brief": s["image_brief"] = json.loads(text)
    elif field in ("plan", "domain_sources", "claims_used"): s[field] = json.loads(text)
    elif field == "quiz":
        if not QZ.is_quiz_page(url): sys.exit("refused: only quiz pages (SurveyQuiz slug containing 'quiz') carry a quiz")
        s["quiz"] = json.load(open(text[1:])) if text.startswith("@") else json.loads(text)
    else: s["fields"][field] = text
    save(url, s); print(f"set {field}")

def written_problems(url, s, n, q):
    """Divit 2026-10-16: a written question as the gate will judge it in the FAQ: the per-question rules (PA3-PA21, flags are rejects)
    and the same intent as another question of the page (PA9 / near_dup)."""
    g = P.Gate(url); out = [f"{r[0]} {r[2]}" for r in g.judge({"q": q, "source": P.WRITTEN, "n": n}) if r[1] == "reject"]
    prim = g.primary
    for sl in s.get("faq_plan") or []:
        o = sl.get("q")
        if sl.get("n") == n or not o: continue
        if P.jacc(P.pa9_content(q, prim), P.pa9_content(o, prim)) >= P.JACCARD_DUP or P.near_dup(q, o, prim):
            out.append(f"PA9 same intent as slot {sl['n']}"); break
    return out

def set_written_q(url, s, n, q):
    sl = s["faq_plan"][n - 1]
    if sl["locked"]: sys.exit(f"refused: slot {n}'s question is locked (ruling 15)")
    if sl["kind"] == "written":
        q = q.strip()
        if not q.endswith("?"): sys.exit("refused: a question ends with '?'")
        bad = written_problems(url, s, n, q)
        if bad: sys.exit("refused (written question): " + "; ".join(bad))
        sl["q"] = q; return
    if sl["kind"] == "semrush":
        if not any(h.search(P.norm(q)) for h in P.Gate(url).heads): sys.exit("refused: a reworded Semrush question must keep the head phrase (backlog line 91)")
    elif not all(w in P.norm(q) for w in P.norm(sl["ref"]).split()): sys.exit(f"refused: the question must carry every word of the secondary '{sl['ref']}' (K8)")
    sl["q"] = q

def cmd_answer(a):
    url, n, text = a[0], int(a[1]), a[2]; s = load(url); sl = s["faq_plan"][n - 1]
    if "--q" in a:
        if sl["locked"]: sys.exit(f"refused: slot {n}'s question is locked (ruling 15)")
        q = a[a.index("--q") + 1]
        set_written_q(url, s, n, q)   # written: gated (Divit 2026-10-16); older semrush/secondary slots: their old checks
    sl["a"] = text; save(url, s); print(f"slot {n} answered")

def _wrap(ans, link):
    """Code places the link: the first occurrence of the anchor words becomes <a href='...'>anchor</a> (single quotes, K4)."""
    words = link.get("write_as") or link["anchor"]
    m = re.search(re.escape(words), ans, re.I)
    if not m: return ans, False
    inner = m.group(0)
    if link.get("write_as"): pre, anc = inner[:len(inner) - len(link["anchor"])], inner[len(inner) - len(link["anchor"]):]
    else: pre, anc = "", inner
    return ans[:m.start()] + pre + f"<a href='{link['url']}'>{anc}</a>" + ans[m.end():], True

def cmd_assemble(a):
    url = a[0]; s = load(url); items, srcs, miss = [], [], []
    for sl in s["faq_plan"]:
        if not sl.get("q") or not sl.get("a"): sys.exit(f"slot {sl['n']} has no {'question' if not sl.get('q') else 'answer'} yet")
        ans = sl["a"]
        if sl.get("link"):
            ans, ok = _wrap(ans, sl["link"])
            if not ok: miss.append(sl["n"])
        items.append({"q": sl["q"], "a": ans})
        # Divit 2026-10-16: every item is "paa" (an AlsoAsked question, verbatim, with provenance) or "written" (code's default
        # definition/how-to questions and the writer's questions; origin keeps the slot kind, secondary the keyword it works in)
        src = "paa" if sl["kind"] == "alsoasked" else "written"
        e = {"q": sl["q"], "source": src, "ref": sl.get("ref")}
        if src == "written":
            e["origin"] = sl["kind"]
            sec = sl.get("secondary") or (sl.get("ref") if sl["kind"] == "secondary" else None)
            if sec: e["secondary"] = sec
        if sl.get("prov"): e["prov"] = sl["prov"]
        srcs.append(e)
    s["fields"]["faq"] = ("<div data-rt-embed-type='true'><div data-rt-embed-type='true'><script> window.awbFAQ = "
                          + json.dumps({"heading": s.get("faq_heading"), "items": items}, ensure_ascii=False) + "; </script></div></div>")
    s["faq_sources"] = srcs; save(url, s)
    print(f"faq assembled ({len(items)} items)" + (f"; LINK WORDS MISSING in slot(s) {miss}: write the words given in the pack" if miss else ""))

def cmd_check(a):
    url, sec = a[0], a[1]
    for fx in ("s10", "h4", "c4", "c5"):   # h3 (serial comma) left to the writer: it inserted wrong commas in the canary
        subprocess.run([sys.executable, os.path.join(ROOT, "ops", "autofix.py"), fx, "--apply", "--url", url], capture_output=True)
    import qc_hub as Q
    s = load(url); s["_path"] = H.spath(url)
    every = Q.load_specs([os.path.join(ROOT, "specs", d, f) for d in os.listdir(os.path.join(ROOT, "specs")) if os.path.isdir(os.path.join(ROOT, "specs", d))
                          for f in os.listdir(os.path.join(ROOT, "specs", d)) if f.endswith(".json")])
    iss = Q.check(s, every)
    keep = SECTIONS.get(sec)
    # a field label may name several fields ("feature_4, tab_content_4") or a family ("howto_step_title"): match any part against the
    # section's fields by prefix in either direction (canary 2026-10-13: the old prefix test hid cross-field Q6 and T1 issues)
    def hits(label):
        parts = [x for x in re.split(r"[,\s]+", label or "") if x]
        strip = lambda x: re.sub(r"_\d+", "", x)
        return any(p_.startswith(k) or k.startswith(p_) or strip(k) == strip(p_) for p_ in parts for k in keep)
    sel = [i for i in iss if i["sev"] in ("P0", "P1") and (sec == "all" or hits(i["field"]))]
    for i in sel: print(f"  {i['sev']} {i['code']} {i['field']}: {i['msg'][:220]}")
    print(f"{sec}: {len(sel)} P0/P1" + ("  -> fix and re-run" if sel else "  -> clean"))
    sys.exit(1 if sel else 0)

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    {"build": cmd_build, "pack": cmd_pack, "set": cmd_set, "answer": cmd_answer, "assemble": cmd_assemble, "check": cmd_check}[a[0]](a[1:])
