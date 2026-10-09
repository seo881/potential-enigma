"""qc_hub.py: deterministic QC for build-hub child page specs.

Usage (from repo root):
    python3 qc/qc_hub.py specs/aab/accounts-payable-automation.json   # one page
    python3 qc/qc_hub.py --hub Auto                                   # every spec in a hub
    python3 qc/qc_hub.py --all                                        # every spec

Prime directive (from Divit's QC rulebook): a page ships only when P0 + P1 == 0.
P2 items are advisory and must be read, not ignored. Exit code = number of P0+P1 issues (capped at 100).

Rules come from: EMERGENT_BUILD_HUBS_HANDOFF.md section 0, Divit's builder-pages rulebook (global copy rules),
qc-build.md (layers, fix methodology), and the hub profile locked 2026-10-06 (DECISIONS.md).
Limits are calibrated on the 4 approved live pages. Rules only tighten (ratchet); loosening needs Divit.
"""
import json, re, sys, glob, os
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))
MAP_PATH = os.path.join(ROOT, "plan", "keyword_map.json")
KMAP = json.load(open(MAP_PATH)) if os.path.exists(MAP_PATH) else None
F4_RETIRED = True   # Divit, 2026-10-09: F4 retired, superseded by the PAA gate (qc/paa_gate.py, PA1-PA13); code kept, disabled
FONTS = ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"]
FONT = next((f for f in FONTS if os.path.exists(f)), FONTS[0])

# ---------------- text helpers ----------------
def strip_html(s): return unescape(re.sub(r"<[^>]+>", " ", s or "")).replace("\\\"", '"')
def words(s): return re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-/.%$]*", strip_html(s))
def norm(s): return re.sub(r"\s+", " ", strip_html(s).lower()).strip()
def h3p(html):
    m = re.fullmatch(r'\s*<h3(?: id="")?>(.+?)</h3>\s*<p(?: id="")?>(.+?)</p>\s*', html or "", re.S)
    return (m.group(1), m.group(2)) if m else None
def faq_obj(s):
    m = re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;\s*</script>", s or "", re.S)
    return json.loads(m.group(1)) if m else None
def mockup_keys(s):
    m = re.search(r"window\.awbMockup\s*=\s*\{(.*)\}\s*;", s or "", re.S)
    return re.findall(r'(?:^|,)\s*([A-Za-z0-9_]+)\s*:\s*"', m.group(1)) if m else None
SETTING_BEFORE = re.compile(r"\b(over|under|above|below|more than|less than|at least|up to|within)\s+$", re.I)
SETTING_AFTER = re.compile(r"^\s*(variance|tolerance|threshold|discount|off)\b", re.I)
def is_setting(sent, m):
    """A percentage that is a threshold or a setting ("over 10%", "a 2% tolerance", "15% off"), not an outcome statistic."""
    return bool(SETTING_BEFORE.search(sent[:m.start()]) or SETTING_AFTER.search(sent[m.end():]))
def sents_of(s): return [x.strip() for x in re.split(r"(?<=[.?!])\s+", (s or "").strip()) if x.strip()]
def _stem(w): return w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w
# keyword spelling variants ("T-shirt" / "t shirt" / "tshirt"): K-checks compare after mapping each variant to one form
KV = json.load(open(os.path.join(ROOT, "rules", "keyword_variants.json")))["groups"]
KV_RX = [(re.compile(r"(?<![a-z0-9])(?:" + "|".join(re.escape(v).replace(r"\ ", r"[\s-]?").replace(r"\-", r"[\s-]?") for v in g["variants"]) + r")(s?)(?![a-z0-9])"), g["canonical"]) for g in KV]
def kwmap(low):
    for rx, c in KV_RX: low = rx.sub(lambda m: c + m.group(1), low)
    return low
def kwn(s): return kwmap(norm(s))
HOUSE = {g["house"] for g in KV if g.get("house")}
def kw_bag(s): return {_stem(w) for w in re.findall(r"[a-z0-9]+", kwmap((s or "").lower()))}
def title_px(s):
    try:
        from PIL import ImageFont
        return round(ImageFont.truetype(FONT, 20).getlength(s))
    except Exception:
        return None

SMALL = {"a","an","the","and","but","or","nor","for","so","yet","as","at","by","in","of","on","to","up","via","vs","per"}  # AP style: 4+ letter words (With, From, Into) are capitalized, as in approved titles
def title_case_errors(s):
    errs = []
    toks = s.split()
    for i, t in enumerate(toks):
        if re.sub(r"s?[^A-Za-z]*$", "", t) in HOUSE: continue   # house spelling of a keyword ("T-shirt", rules/keyword_variants.json)
        for part in re.split(r"(-)", t):
            if part in ("-", "") or not part[0].isalpha(): continue
            first_or_last = i == 0 or i == len(toks) - 1
            if part.lower() in SMALL and not first_or_last and "-" not in t:
                if part[0].isupper(): errs.append(part)
            elif part[0].islower():
                errs.append(part)
    return errs

VOWEL_SOUND_ACRONYM = re.compile(r"^(F|H|L|M|N|R|S|X)[A-Z0-9]*$")   # an FAQ, an HR, an NPS, an SLA, an MBA
CONSONANT_VOWEL_WORDS = ("one", "once", "uni", "use", "usu", "uti", "euro", "eu", "ubiq", "ura", "ure", "ufo")
SILENT_H = ("hour", "honest", "honor", "honour", "heir")
def article_errors(text):
    errs = []
    for m in re.finditer(r"\b(a|an|A|An)\s+([A-Za-z0-9][\w\-]*)", text):
        art, w = m.group(1).lower(), m.group(2)
        low = w.lower()
        if w.isupper() and len(w) > 1:            # acronym: by letter sound
            vowel = bool(re.match(r"[AEIO]", w)) or bool(VOWEL_SOUND_ACRONYM.match(w))
            if w.startswith("U"): vowel = False
        elif w[0].isdigit():
            vowel = w.startswith(("8", "11", "18"))
        else:
            vowel = low[0] in "aeiou" and not low.startswith(CONSONANT_VOWEL_WORDS)
            if low.startswith(SILENT_H): vowel = True
        if art == "a" and vowel: errs.append(m.group(0))
        if art == "an" and not vowel: errs.append(m.group(0))
    return errs

BRITISH = ["enquiry", "colour", "organis", "customis", "optimis", "behaviour", "favourite", "licence", "centre", "analys" + "e", "catalogue", "cancelled", "travelled", "programme", "personalis", "prioritis", "recognis", "summaris"]
BANNED = [
    (r"[\u2013\u2014]", "em or en dash"), (r"[\u2018\u2019\u201c\u201d]", "curly quote"), (r"(?i)\bbuilt-in\b", '"built-in"'),
    (r"Type II", '"Type II" (only SOC 2 Type I is approved)'), (r"&amp;amp;", "double-escaped ampersand"), (r"!", "exclamation mark"),
    (r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", "emoji"), (r"(?i)\b(?:lorem|ipsum|TODO|TBD|placeholder)\b", "placeholder text"),
]
WE_OUR = re.compile(r"(?i)(?<![\w\-])(we|we're|we've|our|ours|us)(?![\w\-])")
VENDOR = ["zapier", "make", "n8n", "typeform", "jotform", "google forms", "surveymonkey", "unbounce", "leadpages", "instapage", "landingi",
          "qualtrics", "wix", "framer", "hubspot", "tally", "fillout", "power automate", "wrike", "pandadoc", "approveit", "interact"]
CLAIMS = json.load(open(os.path.join(ROOT, "rules", "claims.json")))
TELLS = json.load(open(os.path.join(ROOT, "rules", "ai_tells.json")))
US = json.load(open(os.path.join(ROOT, "rules", "us_spelling.json")))

# ---------------- checks ----------------
def check(spec, siblings):
    I = []
    def add(sev, code, field, msg): I.append({"sev": sev, "code": code, "field": field, "msg": msg})
    hub = spec.get("hub"); h = CFG["hubs"].get(hub)
    if not h: add("P0", "S0", "hub", f"unknown hub {hub!r}"); return I
    F = spec.get("fields", {}); prim = (spec.get("keywords") or {}).get("primary", "")
    allowed = set(h["fields"]) - set(CFG["image_fields"])
    for k in F:
        if k not in allowed: add("P0", "S0", k, "field not in the collection map (config/collections.json)")
    # S1 required
    for k in sorted(allowed - set(CFG["optional_fields"])):
        v = F.get(k)
        if v is None or (isinstance(v, str) and not strip_html(v).strip()): add("P0", "S1", k, "required field empty")
    # S2 / S3 rich text shape
    for k in [f"feature_{i}" for i in range(1, 7)] + [f"tab_content_{i}" for i in range(1, 5)]:
        if F.get(k) and not h3p(F[k]): add("P0", "S2", k, "must be exactly <h3>title</h3><p>body</p>")
    # S4 how-to numbering
    for i in range(1, 8):
        t = F.get(f"howto_step_{i}_title", "")
        if t and not t.startswith(f"0{i} "): add("P0", "S4", f"howto_step_{i}_title", f'must start with "0{i} "')
    # S5 FAQ
    fq = None
    try: fq = faq_obj(F.get("faq", ""))
    except Exception as e: add("P0", "S5", "faq", f"FAQ JSON does not parse: {e}")
    if F.get("faq") and fq is None and not any(x["code"] == "S5" for x in I): add("P0", "S5", "faq", "window.awbFAQ object not found")
    if fq:
        n = len(fq.get("items", []))
        if n != 10: add("P1", "S5", "faq", f"{n} FAQ items (exactly 10)")
        if not fq.get("heading"): add("P0", "S5", "faq", "FAQ heading missing")
        qs = [i.get("q", "") for i in fq.get("items", [])]
        for q in qs:
            if not q.endswith("?"): add("P1", "S5", "faq", f"question does not end with '?': {q[:60]}")
        if len(set(map(str.lower, qs))) != len(qs): add("P0", "S5", "faq", "duplicate FAQ question")
    # S6 mockup
    mk = mockup_keys(F.get("mockup", ""))
    if F.get("mockup") and (mk is None or len(mk) != 4): add("P0", "S6", "mockup", f"window.awbMockup must have 4 tab keys, found {mk}")
    # S7 comparison table
    t = F.get("why_table", "")
    if t:
        if "cmp--emg-first" not in t or "col-brand-head" not in t: add("P0", "S7", "why_table", "table must use the Emergent-first layout (cmp--emg-first)")
        heads = re.findall(r'<th scope="col">([^<]+)</th>', t)
        if len(heads) != 3: add("P1", "S7", "why_table", f"expected 3 competitor columns, found {len(heads)}")
        rows = re.findall(r'<th scope="row">', t)
        if len(rows) < 4: add("P1", "S7", "why_table", f"only {len(rows)} comparison rows (expected 4+)")
    # S8 images
    imgs = {k: dict(v) for k, v in spec.get("images", {}).items()}
    br = spec.get("image_brief") or {}
    if br:                                   # before the render stage, the alt text lives in the brief
        for i, tb in enumerate(br.get("tabs", []), 1): imgs.setdefault(f"tab_image_{i}", {}); imgs[f"tab_image_{i}"].setdefault("alt", tb.get("alt", "")) if imgs[f"tab_image_{i}"].get("alt") else imgs[f"tab_image_{i}"].update(alt=tb.get("alt", ""))
        for k, src in (("cover_image", br.get("cover", {})), ("share_image", br.get("og", {}))):
            imgs.setdefault(k, {})
            if not imgs[k].get("alt"): imgs[k]["alt"] = src.get("alt", "")
    for k in CFG["image_fields"]:
        im = imgs.get(k)
        if not im: add("P0", "S8", k, "image missing (spec.images)")
        elif not (im.get("alt") or "").strip(): add("P0", "S8", k, "alt text missing")
        elif im.get("path") and k != "share_image" and not im["path"].endswith(".svg"): add("P0", "S8", k, "use-case and cover images must be outlined SVG")

    # ---------- L: limits (calibrated on the approved pages) ----------
    mt = F.get("meta_title", "")
    if mt:
        if len(mt) > 60: add("P0", "L1", "meta_title", f"{len(mt)} chars (max 60)")
        px = title_px(mt)
        if px and px > 580: add("P0", "L1", "meta_title", f"{px}px at Google's 20px Arial (max ~580)")
        if not mt.endswith(" | Emergent"): add("P0", "L1", "meta_title", 'must end with " | Emergent"')
        if len(mt) < 30: add("P1", "L1", "meta_title", f"only {len(mt)} chars")
    md = F.get("meta_description", "")
    if md:
        if len(md) > 160: add("P0", "L2", "meta_description", f"{len(md)} chars (max 160)")
        elif len(md) > 155: add("P2", "L2", "meta_description", f"{len(md)} chars, may truncate past 155")
        if len(md) < 110: add("P1", "L2", "meta_description", f"only {len(md)} chars (min 110)")
    h1 = F.get("h1", "")
    if h1:
        if norm(h1) == norm(mt.replace(" | Emergent", "")): add("P0", "L3", "h1", "H1 must differ from the meta title")
        if len(h1) > 70: add("P1", "L3", "h1", f"{len(h1)} chars (max 70)")
        if not h1.startswith("Build "): add("P1", "L3", "h1", 'profile: H1 starts "Build a/an {keyword} ..."')
    hw = len(words(F.get("hero_description", "")))
    if hw > 32: add("P1", "L4", "hero_description", f"{hw} words (2-line hero, max ~30)")
    ww = len(words(F.get("why_description", "")))
    if ww > 25: add("P1", "L5", "why_description", f"{ww} words (max 25)")
    for k in ("features_heading", "usecase_heading", "why_title", "howto_title"):
        if len(F.get(k, "")) > 48: add("P1", "L6", k, f"{len(F[k])} chars: H2 wraps past 2 lines (max 48)")
    if len(F.get("features_subheading", "")) > 135: add("P1", "L6", "features_subheading", f"{len(F['features_subheading'])} chars (max 135)")
    if F.get("why_title") and not re.match(r"^Why (Build|Choose|Create)\b.*\?$", F["why_title"]): add("P2", "L6", "why_title", 'profile: "Why Build Your {Keyword} With Emergent?"')
    if F.get("howto_title") and not re.match(r"^How to (Build|Create|Make|Set Up|Automate|Run) ", F["howto_title"]): add("P2", "L6", "howto_title", 'profile: "How to Build/Create a/an {Keyword}"')
    bodies = []
    for i in range(1, 7):
        p = h3p(F.get(f"feature_{i}", ""))
        if p:
            b = len(strip_html(p[1]).strip()); bodies.append(b)
            if not 165 <= b <= 182: add("P1", "L7", f"feature_{i}", f"body {b} chars (feature grid band 165-182)")
            if len(strip_html(p[0])) > 48: add("P1", "L7", f"feature_{i}", "title wraps past 2 lines (max 48 chars)")
    if len(bodies) == 6 and max(bodies) - min(bodies) > 12: add("P1", "L7", "features", f"body spread {max(bodies)-min(bodies)} chars (max 12)")
    if fq:
        for it in fq.get("items", []):
            n = len(words(it.get("a", "")))
            if n > 75: add("P1", "L8", "faq", f"answer {n} words (max 75): {it['q'][:50]}")
            if n < 15: add("P1", "L8", "faq", f"answer {n} words (min 15): {it['q'][:50]}")
    for i in range(1, 5):
        for k in (f"prompt_chip_{i}", f"tab_label_{i}"):
            v = F.get(k, "")
            if len(v) > 26: add("P1", "L9", k, f"{len(v)} chars (max 26)")
    # ---------- H: hygiene (rulebook global rules) ----------
    for k, v in F.items():
        if not isinstance(v, str): continue
        txt = re.sub(r"<style>.*?</style>", "", v, flags=re.S)
        if k in ("why_table",): txt = re.sub(r"<img[^>]*>", "", txt)
        plain = strip_html(txt)
        for rx, label in BANNED:
            if label == "exclamation mark" and k in ("faq", "mockup", "why_table"):
                if re.search(r"!(?!=)", plain): add("P0", "H1", k, label)
                continue
            if re.search(rx, plain): add("P0", "H1", k, label)
        # quoted form-field labels ("May we contact your employer?") are the form's words, not Emergent's voice
        voice = strip_html((re.compile(r'\\"[^"\\]{1,80}\\"') if k == "faq" else re.compile(r'"[^"]{1,80}"')).sub(" ", txt))
        if k == "mockup": voice = ""   # user-voice prompts may say "my"
        for m in WE_OUR.finditer(voice):
            if m.group(0) == "US": continue   # the country, not the pronoun
            add("P0", "H1", k, f'"{m.group(0)}" (write "Emergent" or "Emergent\'s"; never we/our)')
        for w_ in re.findall(r"[A-Za-z]+", plain):
            lw = w_.lower()
            if lw in US["map"]: add("P1", "H2", k, f'UK spelling "{w_}": use "{US["map"][lw]}"')
            elif re.search(r"is(e|ed|es|ing|ation|ations|er|ers)$", lw) and len(lw) > 5 and not any(lw.startswith(x) or x in lw for x in US["ise_whitelist"]):
                add("P1", "H2", k, f'UK -ise spelling "{w_}": use -ize ({re.sub("is(?=(e|ed|es|ing|ation|ations|er|ers)$)", "iz", lw)})')
        for e in article_errors(plain): add("P1", "H4", k, f'article: "{e}"')
    for k in ["h1", "features_heading", "usecase_heading", "why_title", "howto_title"] + [f"prompt_chip_{i}" for i in range(1, 5)] + [f"tab_label_{i}" for i in range(1, 5)]:
        e = title_case_errors(F.get(k, ""))
        if e: add("P1", "H3", k, f"Title Case: {e}")
    # ---------- 2026-10-08 checks (Divit's registration-form feedback; audit/feedback-2026-10-08.md) ----------
    SR = json.load(open(os.path.join(ROOT, "rules", "style_rules.json")))
    sys.path.insert(0, os.path.join(ROOT, "qc")); import serial_comma as _SC
    _copy = {k: v for k, v in F.items() if isinstance(v, str) and k not in ("why_table", "category", "slug")}
    AUD = json.load(open(os.path.join(ROOT, "rules", "audience.json")))
    _group = hub in AUD["group_hubs"] or spec["url"] in {u for v in AUD["group_pages"].values() for u in v}
    def _wre(w): return r"(?<![A-Za-z0-9])" + re.escape(w) + r"(?![A-Za-z0-9])"
    # S10: zero-width characters and empty paragraphs (stripped at export too)
    for k, v in F.items():
        if isinstance(v, str) and (re.search("[\u200b\u200c\u200d\u2060\ufeff]|&zwj;|&#8205;|&zwnj;", v) or re.search(r"<p[^>]*>\s*(&nbsp;|\s)*</p>", v)):
            add("P1", "S10", k, "zero-width character or empty paragraph (renders a blank line): remove it")
    # V5: no plan tiers or rolling numbers in competitor table cells (Emergent column exempt)
    for cell in re.findall(r'<td class="col-other">(.*?)</td>', F.get("why_table") or "", re.S):
        _ct = strip_html(cell)
        if re.search(r"\d", _ct) and (re.search(r"\b(" + "|".join(SR["plan_words"]) + r")\b", _ct, re.I) or re.search(r"/mo\b|/month|per month|/year|\$", _ct, re.I) or len(re.findall(r"\d[\d,.]*", _ct)) >= 2):
            add("P1", "V5", "why_table", f'plan tiers or rolling numbers in a table cell: "{_ct[:70]}" (use wording that needs no monthly update)')
    for k, v in _copy.items():
        txt = strip_html(v); low = txt.lower()
        # H3: serial comma (certain cases block and are auto-fixable; ambiguous ones are listed)
        certain, ambiguous = _SC.find(v)
        for _p, snip in certain: add("P1", "H3", k, f'serial comma missing: "...{strip_html(snip).strip()}..." (auto-fixable)')
        for _p, snip in ambiguous: add("P2", "H3", k, f'possible list without a serial comma (check by hand): "...{strip_html(snip).strip()}..."')
        # H4: UK idioms
        for w, us in SR["uk_idioms"].items():
            bare = w in SR.get("uk_idioms_bare", [])   # British only when nothing follows it in the sentence (a tag ends it too)
            rx = _wre(w) + (r"(?=\s*(?:[.,;:!?)\]\\\"|]|$))" if bare else "")
            if re.search(rx, unescape(re.sub(r"<[^>]+>", " | ", v)).lower() if bare else low): add("P1", "H4", k, f'UK idiom "{w}": use "{us}"')
        # A5: the built app does things, not Emergent
        m_ = re.search(r"\bEmergent(?:'s app)? (?:can |will |then )?(" + "|".join(SR["built_app_verbs"]) + r")\b", txt)
        if m_: add("P1", "A5", k, f'"{m_.group(0)}": the built form/app does this, not Emergent (Emergent builds it)')
        # A6: never narrow the audience ("your team" is allowed on pages that target a group: rules/audience.json)
        for w in SR["narrowing"]:
            if _group and w in AUD["group_phrases"]: continue
            if re.search(_wre(w), low): add("P1", "A6", k, f'audience-narrowing phrase "{w}": write for anyone (DECISIONS: never narrow the audience)'); break
        # C4: custom domains are built in and use credits
        for sent in sents_of(txt):
            if re.search(r"\b(own|custom) domain", sent, re.I) and not re.search(r"credit|built in|built-in|included", sent, re.I):
                add("P1", "C4", k, f'custom domain without the approved wording (built in, uses credits): "{sent[:70]}"')
            # C5: GitHub export is on paid plans (emergent.sh/pricing: GitHub integration from Standard)
            if re.search(r"github", sent, re.I) and re.search(r"export|push|sync|repo", sent, re.I) and not re.search(r"paid plan|standard|pro plan|on paid", sent, re.I):
                add("P1", "C5", k, f'GitHub export without the plan qualifier (paid plans): "{sent[:70]}"')
    # Q9: one word carrying too much of the page (repeated metaphor); keywords excluded
    _kwords = {w for x in [prim] + list((spec.get("keywords") or {}).get("secondaries_used") or []) for w in re.findall(r"[a-z]+", x.lower())}
    _cnt = {}
    for k, v in _copy.items():
        if k in ("mockup", "faq"): continue
        for w in re.findall(r"[a-z]+", strip_html(v).lower()):
            if len(w) > 3 and w not in SR["repeat_generic"] and w not in _kwords: _cnt[w] = _cnt.get(w, 0) + 1
    for w, n in sorted(_cnt.items(), key=lambda x: -x[1])[:3]:
        if n >= SR["repeat_threshold"]: add("P2", "Q9", "page", f'"{w}" appears {n} times outside the FAQ: vary it (repeated metaphor)')

    # ---------- K: keywords, links, cannibalization ----------
    if prim:
        pr = kwn(prim)
        def has(field_text): return pr in kwn(field_text) or pr.rstrip("s") in kwn(field_text)
        if not has(mt): add("P0", "K1", "meta_title", f'primary "{prim}" not in meta title')
        if not has(h1): add("P0", "K1", "h1", f'primary "{prim}" not in H1')
        if not has(md): add("P1", "K2", "meta_description", f'primary "{prim}" not in meta description')
        if fq and fq.get("items") and not has(fq["items"][0]["q"] + " " + fq["items"][0]["a"]): add("P2", "K2", "faq", "primary not in the first FAQ item")
        if not has(F.get("hero_description", "") + F.get("features_subheading", "")): add("P2", "K2", "hero_description", "primary not in hero or features subheading")
        if not spec["url"].endswith("/" + F.get("slug", "")): add("P0", "K3", "slug", "slug does not match the spec URL")
    if fq:
        A_RX = re.compile(r"<a href=(?:\\?\"|')([^\"'\\]+)(?:\\?\"|')>([^<]+)</a>")
        hub_url = "https://emergent.sh" + h["path"]; hub_items = []; extra = []
        for idx, it in enumerate(fq.get("items", []), 1):
            links = A_RX.findall(it.get("a", ""))
            if len(links) > 1: add("P1", "K4", "faq", f"item {idx} has {len(links)} links (one per answer)")
            for u, txt_ in links:
                if not u.startswith("https://emergent.sh/"): add("P0", "K4", "faq", f"external link in FAQ: {u}"); continue
                if u.rstrip("/") == hub_url: hub_items.append(idx); continue
                extra.append((idx, u, txt_))
        if len(hub_items) != 1: add("P0", "K4", "faq", f"{len(hub_items)} hub links (exactly 1, to {hub_url})")
        elif hub_items[0] != 2: add("P1", "K4", "faq", f"the hub link sits in item {hub_items[0]}; it belongs in item 2 (the how-to-build answer)")
        if len(extra) > 3: add("P1", "K4", "faq", f"{len(extra)} related-page links (max 3)")
        if len(extra) < 2 and KMAP: add("P2", "K4", "faq", f"only {len(extra)} related-page link(s); link 2-3 sibling pages with exact-match anchors")
        for idx, u, txt_ in extra:
            path = u.replace("https://emergent.sh", "").rstrip("/")
            if idx == 1: add("P1", "K4", "faq", "no links in item 1 (the definition)")
            tgt = (KMAP or {}).get(path)
            hub_paths = {v["path"] for v in CFG["hubs"].values()}
            if path in hub_paths: continue
            if not tgt or tgt.get("status") in ("cut", "merged", "needs-decision"):
                add("P1", "K4", "faq", f"link target {path} is not a planned or live Emergent page"); continue
            if txt_.strip().lower() != tgt["primary"].lower(): add("P1", "K4", "faq", f'anchor "{txt_}" must be the target page\'s keyword "{tgt["primary"]}" (exact match)')
        # secondary keywords: the FAQ should carry as many as it can. A secondary counts when all its words sit in one
        # sentence, in any order, so writers never force an awkward exact string.
        if KMAP and prim:
            secs = [x["kw"].lower() for x in KMAP.get(spec["url"], {}).get("secondaries", [])]
            fsents = []
            for it_ in fq.get("items", []):
                fsents.append(it_.get("q", "")); fsents += sents_of(strip_html(it_.get("a", "")))
            fbags = [kw_bag(x) for x in fsents]
            got = [x for x in secs if any(kw_bag(x) <= b_ for b_ in fbags)]; need = min(6, len(secs))
            if len(got) < need: add("P1", "K8", "faq", f"FAQ carries {len(got)} of {len(secs)} secondaries (all words in one sentence, any order; need {need}); missing e.g. {[x for x in secs if x not in got][:5]}")
            # two secondaries in back-to-back sentences of one answer reads as keyword stuffing
            def sec_hits(sent):                  # verbatim secondaries, longest first; one inside the primary or a longer secondary does not count
                low = " " + kwmap(sent.lower()) + " "; out = set()
                for x in sorted({kwmap(y) for y in secs} | {kwmap(prim.lower())}, key=len, reverse=True):
                    rx = r"(?<![a-z0-9])" + re.escape(x) + r"(?![a-z0-9])"
                    if re.search(rx, low):
                        if x != kwmap(prim.lower()): out.add(x)
                        low = re.sub(rx, " | ", low)
                return out
            for idx, it_ in enumerate(fq.get("items", []), 1):
                ss = sents_of(strip_html(it_.get("a", ""))); hits = [sec_hits(x_) for x_ in ss]
                for j in range(len(ss) - 1):
                    pair = next(((p, q) for p in sorted(hits[j]) for q in sorted(hits[j + 1]) if p != q), None)
                    if pair: add("P1", "K8", f"faq item {idx}", f'secondaries "{pair[0]}" and "{pair[1]}" in back-to-back sentences read as keyword stuffing: "{ss[j][:50]}" / "{ss[j + 1][:50]}"')
    body = " ".join(strip_html(v) for k, v in F.items() if isinstance(v, str) and k not in ("why_table",))
    if KMAP and prim:
        me = KMAP.get(spec["url"], {})
        mine = {kwn(prim)} | {kwn(s["kw"]) for s in me.get("secondaries", [])}
        heads = [strip_html(h3p(F[k])[0]) for k in F if re.match(r"(feature|tab_content)_\d", k) and h3p(F.get(k, ""))]
        heads += [F.get(k, "") for k in ("features_heading", "usecase_heading", "why_title", "howto_title", "h1", "meta_title")]
        heads += [i["q"] for i in (fq or {}).get("items", [])]
        for url, p in KMAP.items():
            if url == spec["url"] or p.get("status") == "live-off-plan": continue
            kp = kwn(p["primary"])
            if kp in mine or any(kp in m for m in mine) or len(kp.split()) < 2: continue
            for hd in heads:
                if re.search(r"\b" + re.escape(kp) + r"\b", kwn(hd)):
                    add("P1", "K5", "headings", f'uses sibling primary "{p["primary"]}" ({url}) in a heading: "{hd[:60]}"'); break
        secs = [s["kw"] for s in me.get("secondaries", [])][:15]
        if secs:
            hit = [s for s in secs if kwn(s) in kwn(body)]
            cov = len(hit) / len(secs)
            if cov < 0.4: add("P2", "K6", "body", f"covers {len(hit)}/{len(secs)} top secondaries ({cov:.0%}); missing e.g. {[s for s in secs if s not in hit][:4]}")
        try:
            sys.path.insert(0, os.path.join(ROOT, "plan")); import serp as _S
            _live = _S.load(spec["url"]) or {}
        except Exception: _live = {}
        top = " ".join(me.get("top10", []) + [o.get("url", "") for o in _live.get("organic", [])]).lower()
        if top and t:
            for hd in re.findall(r'<th scope="col">([^<]+)</th>', t):
                brands = [b.strip().lower().replace(" ", "") for b in re.split(r"[/,()]", hd) if b.strip() and "builder" not in b.lower()]
                flat = top.replace("-", "").replace(" ", "")
                if brands and not any(b in flat for b in brands):
                    add("P2", "K7", "why_table", f'competitor "{hd}" is not in this page\'s top 10; prefer tools that rank for the query')
    # ---------- V/C: vendor numbers, claims ----------
    table_ok = False
    if spec.get("status") not in ("live-draft", "published"):
        if not spec.get("table"):
            add("P1", "V2", "why_table", "build the comparison table from the vetted library: hubctl table <url> --vs A,B,C --rows ...")
        else:
            try:
                sys.path.insert(0, os.path.join(ROOT, "ops")); import table as TB
                want = TB.render(h["repo_dir"], spec["table"]["vs"], spec["table"]["rows"], spec["table"].get("variant"))
                if want != t: add("P1", "V2", "why_table", "the table differs from the library (hand-edited or the library changed): regenerate it with hubctl table")
                else: table_ok = True
                for o in TB.stale(h["repo_dir"], spec["table"]["vs"], spec["table"]["rows"]): add("P1", "V3", "why_table", f"fact needs re-checking: {o}")
            except Exception as e:
                add("P1", "V2", "why_table", f"table spec invalid: {e}")
    if not spec.get("vendor_facts_checked") and not table_ok:
        for cell in re.findall(r'<td class="col-other">(.*?)</td>', t, re.S):
            if re.search(r"(?<![A-Za-z])\d", strip_html(cell)):
                add("P1", "V1", "why_table", f'competitor cell with a number needs a dated check (spec.vendor_facts_checked): "{strip_html(cell).strip()[:70]}"')
        for it in (fq or {}).get("items", []):
            for sent in re.split(r"(?<=[.;])\s+", strip_html(it.get("a", ""))):
                s = sent.lower()
                if re.search(r"\d", s) and any(re.search(r"\b" + re.escape(v) + r"\b", s) for v in VENDOR if v != "make"):
                    add("P1", "V1", "faq", f'vendor number needs a dated check: "{sent.strip()[:80]}"')
    for c in CLAIMS["patterns"]:
        for m in re.finditer(c["rx"], body, re.I):
            if c.get("status") == "banned": add("P0", "C1", "body", f'banned claim: "{m.group(0)}" ({c["why"]})')
            elif c.get("status") == "confirm": add("P2", "C1", "body", f'claim to confirm with Divit: "{m.group(0)}" ({c["why"]})')
    # ---------- A: human voice (never reads as AI-written) ----------
    for k, v in F.items():
        if not isinstance(v, str) or k in ("why_table", "mockup", "category", "slug"): continue
        plain = strip_html(re.sub(r"<style>.*?</style>", "", v, flags=re.S))
        low = plain.lower()
        for w in TELLS["block"]:
            if re.search(r"(?<![a-z\-])" + re.escape(w) + r"(?![a-z\-])", low): add("P1", "A1", k, f'AI-tell word "{w}": rewrite in plain operator language')
        for w in TELLS["flag"]:
            if re.search(r"(?<![a-z\-])" + re.escape(w) + r"(?![a-z\-])", low): add("P2", "A2", k, f'"{w}": keep only if literal and the plainest word')
        sentences = [x.strip() for x in re.split(r"(?<=[.?])\s+", plain) if x.strip()]
        for pat in TELLS["patterns"]:
            hit = any(re.search(pat["rx"], x, re.I) for x in sentences)
            if hit: add("P1" if pat["level"] == "block" else "P2", "A3", k, pat["why"])
    # repeated sentence openers across the page (templated rhythm)
    openers = {}
    for k, v in F.items():
        if not isinstance(v, str) or k in ("why_table", "mockup", "faq"): continue
        for x in re.split(r"(?<=[.?])\s+", strip_html(v)):
            w = x.strip().split()
            if len(w) >= 6: openers.setdefault(" ".join(w[:2]).lower(), []).append(k)
    for o, ks in openers.items():
        if len(ks) >= 4 and o not in ("every response", "every page"): add("P2", "A4", "body", f'{len(ks)} sentences open with "{o}": vary the rhythm')

    # ---------- I: image brief (rendered in memory through the engine and its gates) ----------
    frozen_spec = spec.get("status") in ("live-draft", "published")
    # ---------- F: FAQ sourced from what people actually search (live SERP via DataForSEO) ----------
    if not frozen_spec and fq:
        sys.path.insert(0, os.path.join(ROOT, "plan")); import serp as S
        live = S.load(spec["url"])
        if not live:
            add("P1", "F1", "faq", "no live SERP captured for this page: pull it with DataForSEO and run hubctl serp-save before writing the FAQ")
        else:
            srcs = {x.get("q"): x for x in spec.get("faq_sources", [])}
            paa_q = {S.tokens(i["q"]).__str__(): i["q"] for i in live["paa"]}
            prims = {}
            if KMAP:
                prims = {q["primary"].lower(): u for u, q in KMAP.items() if u != spec["url"] and q.get("status") != "live-off-plan" and len(q["primary"].split()) > 1}
            me_secs = {norm(x["kw"]) for x in (KMAP or {}).get(spec["url"], {}).get("secondaries", [])}
            used_paa = set()
            for it in fq.get("items", []):
                src = srcs.get(it["q"])
                if not src: add("P1", "F2", "faq", f'no source recorded in faq_sources for: "{it["q"][:60]}"'); continue
                kind, ref = src.get("source"), src.get("ref", "")
                if kind == "paa":
                    match = next((i["q"] for i in live["paa"] if i["q"].strip().lower() == ref.strip().lower()), None)
                    if not match: add("P1", "F2", "faq", f'source says PAA but "{ref[:60]}" is not in the captured PAA list')
                    else:
                        used_paa.add(match.lower())
                        if S.similar(it["q"], match) < 0.5: add("P1", "F3", "faq", f'"{it["q"][:50]}" drifts too far from the PAA question "{match[:50]}"; keep the searcher\'s phrasing')
                elif kind == "related":
                    if not any(ref.strip().lower() == r.lower() for r in live["related"]): add("P1", "F2", "faq", f'related search "{ref[:50]}" is not in the captured list')
                elif kind == "keyword":
                    if not any(ref.strip().lower() == k_["kw"].lower() for k_ in live.get("keywords", [])): add("P1", "F2", "faq", f'keyword idea "{ref[:50]}" is not in the captured DataForSEO keyword list')
                elif kind == "secondary":
                    if norm(ref) not in me_secs: add("P1", "F2", "faq", f'"{ref[:50]}" is not one of this page\'s secondaries')
                    if src.get("paa_ref"):  # reclassified from DataForSEO PAA by hubctl paa-resource: the PAA question still counts as answered
                        m_ = next((i["q"] for i in live["paa"] if i["q"].strip().lower() == src["paa_ref"].strip().lower()), None)
                        if m_: used_paa.add(m_.lower())
                elif kind == "definition":
                    if norm(ref) != norm(prim): add("P1", "F2", "faq", "a definition item must define the page's primary keyword")
                else:
                    add("P1", "F2", "faq", f'unknown source type "{kind}" (paa, related, secondary, keyword, definition)')
            me_page = (KMAP or {}).get(spec["url"], {"primary": prim, "secondaries": []})
            ok_paa, _skip = S.eligible(live, me_page, prims)
            # PA4 per-page skip list (Divit approved PA1-PA13, 2026-10-08): a logged, reasoned skip is not required by F4
            _pp = json.load(open(os.path.join(ROOT, "rules", "paa_blocklist.json")))["per_page"].get(spec["url"].rsplit("/", 1)[1], [])
            _pskip = {e["q"].strip().lower() for e in _pp if e.get("reason")}
            ok_paa = [i for i in ok_paa if i["q"].strip().lower() not in _pskip]
            for i in ([] if F4_RETIRED else ok_paa[:10]):
                if i["q"].lower() not in used_paa: add("P1", "F4", "faq", f'People Also Ask question not answered: "{i["q"]}"')
            if not live["paa"]: add("P2", "F5", "faq", "this SERP shows no People Also Ask box; FAQ comes from related searches and secondaries")
    on_hold = CFG.get("images_on_hold")
    if on_hold and not frozen_spec:
        add("P2", "I0", "images", f"image brief and rendering on hold since {on_hold['since']} (brand palette pending)")
    if not frozen_spec and not on_hold:
        if not spec.get("image_brief"):
            add("P1", "I1", "image_brief", "missing: write the 4 tabs, cover and og per docs/IMAGE_BRIEF.md")
        else:
            try:
                sys.path.insert(0, os.path.join(ROOT, "pipeline")); import engine
                iss, notes = engine.lint(spec)
                for x in iss: add("P1", "I4" if x.startswith("story:") else "I1", "image_brief", x)
                for x in notes: add("P2", "I2", "image_brief", x)
            except Exception as e:
                add("P2", "I0", "image_brief", f"image lint skipped ({type(e).__name__}: {e}); run bash ops/setup.sh")
            for i, tb in enumerate(spec["image_brief"].get("tabs", []), 1):
                p_ = (tb.get("prompt") or "").strip()
                if p_ and not (40 <= len(p_) <= 95): add("P2", "I3", f"tab {i} prompt", f"{len(p_)} chars; a prompt chip reads best at 60-85")

    # ---------- T: rendered width in the template's real typography (ops/typeset.py) ----------
    if spec.get("status") not in ("live-draft", "published"):
        try:
            sys.path.insert(0, os.path.join(ROOT, "ops")); import typeset as _TS
            for sev, fld, msg in _TS.check(spec): add(sev, "T1", fld, msg)
        except Exception as e:
            add("P2", "T0", "typography", f"width check skipped ({type(e).__name__}: {e})")
        if md:
            try:
                from PIL import ImageFont
                dpx = round(ImageFont.truetype(FONT, 14).getlength(md))
                if dpx > 920: add("P1", "L2", "meta_description", f"{dpx}px at Google's 14px Arial (truncates past about 920px)")
            except Exception: pass
        # structure: every rich-text field must have the same HTML skeleton as the approved live pages
        def skel(html_):
            return re.sub(r'\s+id=""', "", " ".join(re.findall(r"</?[a-z0-9]+[^>]*?>", html_ or "")))
        base = next((b_ for b_ in siblings if b_.get("hub") == hub and b_.get("status") == "live-draft"), None)
        if base:
            for k_ in [f"feature_{i}" for i in range(1, 7)] + [f"tab_content_{i}" for i in range(1, 5)]:
                if F.get(k_) and skel(F[k_]).replace(' id=""', "") != skel(base["fields"].get(k_, "")).replace(' id=""', ""):
                    add("P0", "S9", k_, f"HTML shape differs from the approved live page ({skel(F[k_])[:60]} vs {skel(base['fields'].get(k_, ''))[:60]})")
            if F.get("faq") and (not F["faq"].startswith("<div data-rt-embed-type='true'><div data-rt-embed-type='true'><script> window.awbFAQ = ") or not F["faq"].endswith("; </script></div></div>")):
                add("P0", "S9", "faq", "FAQ embed wrapper differs from the approved live pages")
            if F.get("mockup") and not re.fullmatch(r'<p id="">window\.awbMockup = \{ .* \};</p>', F["mockup"], re.S):
                add("P0", "S9", "mockup", "mockup embed shape differs from the approved live pages")
            for k_ in ("hero_prompt",):
                if F.get(k_) and not re.fullmatch(r"<p>[^<]+</p>", F[k_]): add("P0", "S9", k_, "must be a single <p>...</p> like the approved pages")

    # ---------- Q: craft (the criteria behind every past rejection; see rules/CONTENT_DEFECTS.md) ----------
    paras = []                                   # (field, text) for every prose paragraph a reader sees
    for k in ["hero_description", "features_subheading", "why_description", "howto_description"]:
        if F.get(k): paras.append((k, strip_html(F[k])))
    for k in [f"feature_{i}" for i in range(1, 7)] + [f"tab_content_{i}" for i in range(1, 5)]:
        pr = h3p(F.get(k, ""))
        if pr: paras.append((k, strip_html(pr[1])))
    for i in range(1, 8):
        if F.get(f"howto_step_{i}_des"): paras.append((f"howto_step_{i}_des", F[f"howto_step_{i}_des"]))
    for i_, it in enumerate((fq or {}).get("items", []), 1): paras.append((f"faq item {i_}", strip_html(it.get("a", ""))))
    kws = sorted({prim.lower()} | {x["kw"].lower() for x in (KMAP or {}).get(spec["url"], {}).get("secondaries", [])}, key=len, reverse=True) if prim else []
    LABEL_NEXT = {"for", "that", "which", "built", "designed", "made", "to", "with", "helps", "help", "tailored"}
    for k, ptxt in paras:
        sents = [x.strip() for x in re.split(r"(?<=[.?!])\s+", ptxt.strip()) if x.strip()]
        if not sents: continue
        first = sents[0]; fl = first.lower()
        kw = next((x for x in kws if fl.startswith(x)), None)
        if kw:
            nxt = fl[len(kw):].strip().split(" ")[0] if fl[len(kw):].strip() else ""
            if nxt in LABEL_NEXT or len(first.split()) < 7:
                add("P1", "Q1", k, f'opens with a keyword label ("{first[:60]}"): open with a full sentence that says what happens')
        for x in sents:
            n_ = len(x.split())
            if n_ > 40: add("P1", "Q2", k, f"{n_}-word sentence: split it (max 40; aim under 30): \"{x[:60]}...\"")
            elif n_ > 32: add("P2", "Q2", k, f"{n_}-word sentence; consider splitting: \"{x[:50]}...\"")
    if KMAP and prim and F.get("h1"):
        generic = {"automation", "automate", "builder", "form", "forms", "survey", "surveys", "page", "pages", "template", "templates", "software", "app", "workflow", "workflows", "quiz", "landing", "build"}
        own = set(re.findall(r"[a-z]+", prim.lower())) | {w for x in kws for w in re.findall(r"[a-z]+", x)}
        hook = set(re.findall(r"[a-z]+", F["h1"].lower())) - own - generic
        for u_, q_ in KMAP.items():
            if u_ == spec["url"] or q_.get("hub") != hub: continue
            sib = set(re.findall(r"[a-z]+", q_["primary"].lower())) - own - generic
            if sib and sib <= hook:
                add("P1", "Q3", "h1", f'H1 leans on a sibling page\'s topic ("{q_["primary"]}"): state this page\'s whole job, not one part of it'); break
    if spec.get("table") and spec.get("status") not in ("live-draft", "published"):
        try:
            sys.path.insert(0, os.path.join(ROOT, "ops")); import table as _TB
            # A variant is required only when every competitor is a specialist of that category and none is also a general tool
            # (Typeform is a form builder and a hiring tool: a rental agreement page must not be forced into the hiring variant)
            GENERAL = {"form-builder", "automation-platform", "landing-page-builder", "site-builder", "survey-tool", "quiz-tool"}
            _L = _TB.lib(h["repo_dir"]); per = [set(_L["competitors"].get(c, {}).get("categories", [])) for c in spec["table"]["vs"]]
            shared = set.intersection(*per) if per else set()
            for vk in ([] if shared & GENERAL else _L.get("emergent_variants", {})):
                if vk in shared and spec["table"].get("variant") != vk:
                    add("P1", "Q4", "why_table", f'these competitors are "{vk}" tools: use --variant {vk} so the Emergent column speaks to this buyer'); break
        except Exception: pass
    # ---------- V4: a category variant defines every row it is used with (Divit, 2026-10-07: no silent hub-default fallback) ----------
    if spec.get("table") and spec["table"].get("variant") and spec.get("status") not in ("live-draft", "published"):
        try:
            sys.path.insert(0, os.path.join(ROOT, "ops")); import table as _TB2
            _var = _TB2.lib(h["repo_dir"]).get("emergent_variants", {}).get(spec["table"]["variant"], {})
            for r_ in spec["table"].get("rows", []):
                rid = r_.split("=", 1)[0]
                if rid not in _var: add("P1", "V4", "why_table", f'variant "{spec["table"]["variant"]}" does not define row "{rid}", so the hub default shows: the variant must set it (Divit), or drop the row')
        except Exception as e: add("P2", "V4", "why_table", f"variant check skipped: {e}")
    # ---------- Q5-Q8: whole-page craft. Every instance is reported, so a writer fixes the class, not one example ----------
    units = []                                   # (field, text) for every piece of copy a reader sees
    for k in ["meta_title", "meta_description", "h1", "hero_description", "features_heading", "features_subheading", "why_title",
              "why_description", "usecase_heading", "howto_title", "howto_description"]:
        if F.get(k): units.append((k, strip_html(F[k]).strip()))
    for k in [f"feature_{i}" for i in range(1, 7)] + [f"tab_content_{i}" for i in range(1, 5)]:
        pr = h3p(F.get(k, ""))
        if pr: units.append((k, strip_html(pr[0]).strip() + ". " + strip_html(pr[1]).strip()))
    for i in range(1, 8):
        for suf in ("title", "des"):
            if F.get(f"howto_step_{i}_{suf}"): units.append((f"howto_step_{i}_{suf}", strip_html(F[f"howto_step_{i}_{suf}"]).strip()))
    for i_, it in enumerate((fq or {}).get("items", []), 1):
        units.append((f"faq item {i_}", it.get("q", "").strip() + " " + strip_html(it.get("a", "")).strip()))
    # Q5 tacked-on endings
    TAIL = re.compile(r"\b(?:and )?(?:which|that) is what\b", re.I)
    SO_TAIL = re.compile(r",\s+so\s+(?!far\b|on\b|much\b|many\b|long\b)", re.I)
    so_hits = []
    for lab, tx in units:
        for x in sents_of(tx):
            m_ = TAIL.search(x)
            if m_: add("P1", "Q5", lab, f'tacked-on "{m_.group(0)}" clause: end the sentence on its point: "{x[:90]}"')
            if SO_TAIL.search(x): so_hits.append((lab, x))
    for lab, x in so_hits:
        add("P1" if len(so_hits) > 2 else "P2", "Q5", lab, f'", so" ending ({len(so_hits)} on the page; more than 2 blocks): "{x[:90]}"')
    # Q6 repetition inside the page: a 6-word phrase in two different fields (the page's own keywords excluded)
    own_kws = sorted({prim.lower()} | {x["kw"].lower() for x in (KMAP or {}).get(spec["url"], {}).get("secondaries", [])}, key=len, reverse=True) if prim else []
    grams = {}                                   # gram -> {field: [(segment id, position)]}
    seg_tokens = {}
    for lab, tx in units:
        for si, x in enumerate(sents_of(tx)):
            low = " " + x.lower() + " "
            for kw_ in own_kws:
                low = re.sub(r"(?<![a-z0-9])" + re.escape(kw_) + r"(?![a-z0-9])", " | ", low)
            for gi, seg in enumerate(low.split("|")):
                tk = re.findall(r"[a-z0-9$%][a-z0-9$%'\-]*", seg); sid = (lab, si, gi); seg_tokens[sid] = tk
                for p in range(len(tk) - 5):
                    grams.setdefault(" ".join(tk[p:p + 6]), {}).setdefault(lab, []).append((sid, p))
    rep = {}                                     # (field, segment) -> set of start positions that repeat elsewhere
    for g, where in grams.items():
        if len(where) < 2: continue
        for lab, occ in where.items():
            for sid, p in occ: rep.setdefault(sid, set()).add(p)
    found = {}                                   # maximal repeated phrase -> fields it appears in
    for sid, ps in rep.items():
        ps = sorted(ps); runs = [[ps[0], ps[0]]]
        for p in ps[1:]:
            if p <= runs[-1][1] + 1: runs[-1][1] = p
            else: runs.append([p, p])
        tk = seg_tokens[sid]
        for a_, b_ in runs:
            fields = set()
            for p in range(a_, b_ + 1): fields |= set(grams[" ".join(tk[p:p + 6])])
            phrase = " ".join(tk[a_:b_ + 6]); found[phrase] = found.get(phrase, set()) | fields
    for phrase, fields in found.items():
        if any(phrase != o and phrase in o for o in found): continue
        add("P1", "Q6", ", ".join(sorted(fields)), f'"{phrase}" appears in {len(fields)} fields: say it once, and give the other field its own point')
    # Q7 "from X to Y" ranges
    FROMTO = re.compile(r"\bfrom\s+(?:[^\s,;:.?!]+\s+){0,5}?to\s+[^\s,;:.?!]+", re.I)
    ft = [(lab, m_.group(0)) for lab, tx in units for m_ in FROMTO.finditer(tx)]
    if len(ft) > 3:
        for lab, x in ft: add("P1", "Q7", lab, f'"{x}" is one of {len(ft)} "from X to Y" ranges on the page (max 3): keep only real journeys')
    # Q8 lists of three
    # an item is 1-3 words and does not start like a clause ("routing rule, so the form and the" is not a list)
    ITEM = r"(?!(?:so|which|that|then|but|while|because|when|where|if|and|or|it|they|you|we|this|these|each|every)\b)[\w$%'\-]+(?:\s[\w$%'\-]+){0,2}"
    TRIPLE = re.compile(r"(?<![\w$%'\-])" + ITEM + r",\s" + ITEM + r",?\s(?:and|or)\s[\w$%'\-]+")
    tr = [(lab, m_.group(0)) for lab, tx in units for x in sents_of(tx) for m_ in TRIPLE.finditer(x)]
    if len(tr) > 8:
        for lab, x in tr: add("P2", "Q8", lab, f'"{x}" is one of {len(tr)} "A, B, and C" lists on the page (more than 8 reads templated): use pairs or one specific')
    # ---------- P: plan before prose; domain claims verified and sourced (Divit, 2026-10-07) ----------
    if spec.get("status") not in ("live-draft", "published"):
        plan = spec.get("plan")
        if not isinstance(plan, dict): add("P1", "P1", "plan", "no spec.plan: write the plan (angle, tab_stories, openers, heading_shapes, claims_to_source) and run hubctl plan-check before the prose")
        else:
            if len((plan.get("angle") or "").strip()) < 40: add("P1", "P1", "plan", "plan.angle: say in a sentence or two how this page wins against the top 10")
            ts = plan.get("tab_stories") or []
            if len(ts) != 4 or len({norm(x) for x in ts}) != 4 or any(len((x or "").split()) < 5 for x in ts): add("P1", "P1", "plan", "plan.tab_stories: four distinct one-sentence stories, one per tab")
            op = plan.get("openers") or []
            if len(op) < 4 or len({norm(x).split(" ")[0] for x in op if x}) < 4: add("P1", "P1", "plan", "plan.openers: at least four planned paragraph openers that start differently")
            hs = plan.get("heading_shapes") or []
            if len(hs) < 4 or len({norm(x) for x in hs}) < 4: add("P1", "P1", "plan", "plan.heading_shapes: four tab heading shapes, different from each other and from sibling pages (hubctl plan-check)")
            if not isinstance(plan.get("claims_to_source"), list): add("P1", "P1", "plan", "plan.claims_to_source: list every claim about third-party systems, legal or professional terms, or best practice (empty list if none)")
            else:
                ds = spec.get("domain_sources") or []
                for d_ in ds:
                    if not (str(d_.get("source_url", "")).startswith("https://") and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(d_.get("date", ""))) and d_.get("claim")):
                        add("P1", "P2", "domain_sources", f'each source needs claim, an https source_url and an ISO date: {str(d_)[:80]}')
                have = {norm(d_.get("claim", "")) for d_ in ds}
                for c_ in plan["claims_to_source"]:
                    if norm(c_) not in have: add("P1", "P2", "domain_sources", f'claim not verified: "{c_[:80]}". Check it with a web search and record {{claim, source_url, date}} in spec.domain_sources')
    # ---------- P3/P4: sources are live (automated link check) and few (max 8) ----------
    if spec.get("status") not in ("live-draft", "published") and spec.get("domain_sources"):
        sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as _G3
        lc = _G3.link_cache(); import datetime as _dt3
        for d_ in spec["domain_sources"]:
            u = d_.get("source_url"); r = lc.get(u)
            if not r or (_dt3.date.today() - _dt3.date.fromisoformat(r["checked"])).days > 7: add("P1", "P3", "domain_sources", f"not link-checked in the last 7 days: run hubctl sources-check {spec['url']} ({u[:70]})")
            elif r["status"] in ("dead", "moved"): add("P1", "P3", "domain_sources", f"source is {r['status']} ({r.get('code')}): {u[:70]}" + (f" -> {r['final'][:60]}" if r["status"] == "moved" else "") + ". Replace it or cut the claim")
            elif r["status"] == "blocked": add("P2", "P3", "domain_sources", f"source refuses automated checks ({r.get('code')}), unverified: {u[:70]}")
        n_src = len({d_.get("source_url") for d_ in spec["domain_sources"]})
        started = (spec.get("history") or [{}])[0].get("t", "")
        if n_src > 8: add("P1" if started >= "2026-10-07 14:30 UTC" else "P2", "P4", "domain_sources", f"{n_src} sources (max 8 per page): keep the ones the copy needs, primary first")
    # ---------- R: the reviewer's scored rubric must pass before a page moves past review ----------
    try:
        st_ = json.load(open(os.path.join(ROOT, "status", f"{h['repo_dir']}.json")))["pages"].get(spec["url"], {}).get("state")
    except Exception: st_ = None
    if st_ == "challenged" or (st_ in ("approved", "cms_draft", "published") and spec.get("challenge")):   # challenger retired 2026-10-07: legacy pages only
        ch = spec.get("challenge") or {}
        if ch.get("result") != "pass": add("P1", "R2", "challenge", f'adversarial challenge is {ch.get("result", "missing")}: {"; ".join(ch.get("defects", []))[:120]}')
        if ch.get("by") and ch.get("by") in (spec.get("written_by"), (spec.get("review") or {}).get("by")): add("P1", "R2", "challenge", "the challenger must be a different agent from the writer and the reviewer")
    if st_ in ("reviewed", "challenged", "approved", "cms_draft", "published"):
        RUB = json.load(open(os.path.join(ROOT, "rules", "rubric.json")))["criteria"]
        rv = (spec.get("review") or {}).get("rubric", {})
        # the one rework (Divit, 2026-10-07): a later move to reviewed via `hubctl ready` closes the findings of the review it followed
        _rd = (spec.get("review") or {}).get("date", "")
        if _rd and any(h.get("state") == "reviewed" and h.get("t", "") > _rd for h in spec.get("history", [])): rv = {c["id"]: {"result": "pass"} for c in RUB}
        for c in RUB:
            r = rv.get(c["id"], {})
            if r.get("result") != "pass": add("P1", "R1", "review", f'rubric "{c["id"]}" is {r.get("result", "missing")}: {r.get("evidence", c["test"])[:90]}')

    # ---------- C2/C3: capability ledger, sourced facts and statistics ----------
    if spec.get("status") not in ("live-draft", "published"):
        CAP = json.load(open(os.path.join(ROOT, "rules", "capabilities.json"))); FACTS = json.load(open(os.path.join(ROOT, "rules", "facts.json")))
        copy_fields = {k: v for k, v in F.items() if isinstance(v, str) and k not in ("why_table", "category", "slug")}
        for k, v in copy_fields.items():
            plain = strip_html(v)
            for pend in CAP["pending"]:
                for m_ in re.finditer(pend["rx"], plain, re.I):
                    add("P1", "C2", k, f'capability claim needs Divit\'s approval ({pend["id"]}): "{m_.group(0)}" ({pend["why"]})')
        approved_ids = {c["id"] for c in CAP["approved"]}
        used = spec.get("claims_used")
        if used is None: add("P1", "C2", "claims_used", "list the capability-ledger ids this page relies on in spec.claims_used (rules/capabilities.json)")
        else:
            for cid in used:
                if cid not in approved_ids: add("P1", "C2", "claims_used", f'"{cid}" is not an approved capability')
        BRANDS = set()
        for lf in glob.glob(os.path.join(ROOT, "rules", "competitors", "*.json")):
            for name in json.load(open(lf))["competitors"]: BRANDS |= {b_.strip() for b_ in re.split(r"[/,()]", name) if len(b_.strip()) > 2 and "builder" not in b_.lower()}
        BRANDS |= {"Shopify", "WooCommerce", "BigCommerce", "QuickBooks", "Xero", "NetSuite", "Salesforce", "HubSpot", "Slack", "Stripe", "PayPal", "Google", "Microsoft", "Notion", "Airtable", "Mailchimp", "Calendly", "Asana", "Monday", "Jira", "Coupa", "SAP", "Oracle"}
        FACT_VERB = re.compile(r"\b(charges?|costs?|limits?|caps?|no longer|does not|doesn't|cannot|can't|only (offers|supports|allows)|requires?|stopped|removed|deprecated|lacks?|restricts?)\b", re.I)
        STAT = re.compile(r"\b\d+(\.\d+)?\s?(%|percent\b)|\b\d+(\.\d+)?x (faster|more|fewer|less)\b|\b\d+ times (faster|more)\b", re.I)
        matches = [m_ for f_ in FACTS["facts"] for m_ in f_["match"]]
        for k, v in copy_fields.items():
            if k == "mockup": continue
            for sent in re.split(r"(?<=[.?!])\s+", strip_html(v)):
                brand = next((b_ for b_ in BRANDS if re.search(r"\b" + re.escape(b_) + r"\b", sent)), None)
                stat = any(not is_setting(sent, m_) for m_ in STAT.finditer(sent))
                if (brand and FACT_VERB.search(sent)) or stat:
                    if not any(m_ in sent for m_ in matches):
                        add("P1", "C3", k, f'unsourced {"statistic" if stat else "fact about " + brand}: "{sent[:90]}". Add it to rules/facts.json with a source, or remove it')
        import datetime as _dt
        for f_ in FACTS["facts"]:
            if any(m_ in " ".join(strip_html(v) for v in copy_fields.values()) for m_ in f_["match"]):
                if (_dt.date.today() - _dt.date.fromisoformat(f_["checked"])).days > 90: add("P1", "C3", "facts", f'fact "{f_["id"]}" was last checked {f_["checked"]}: re-check it')
    # ---------- D2: near-duplicates (shared phrases) against every page in the hub ----------
    if spec.get("status") not in ("live-draft", "published"):
        sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as _G
        for sec, ou, c_ in _G.similarity(spec, siblings):
            if c_ > 0.30: add("P1", "D2", sec, f"{c_:.0%} of this section's phrases also appear on {ou}: rewrite it for this page")
            elif c_ > 0.18: add("P2", "D2", sec, f"{c_:.0%} of this section's phrases also appear on {ou}")
    # ---------- F6 / R3: SERP age, approval fingerprint ----------
    if spec.get("status") not in ("live-draft", "published"):
        try:
            sys.path.insert(0, os.path.join(ROOT, "plan")); import serp as _S, datetime as _dt
            lv = _S.load(spec["url"])
            if lv and (_dt.date.today() - _dt.date.fromisoformat(lv["fetched"])).days > 30: add("P1", "F6", "serp", f"SERP data from {lv['fetched']} is over 30 days old: re-pull it and re-check the FAQ")
        except Exception: pass
        if spec.get("approval"):
            try:
                sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as _G
                if _G.fingerprint(spec) != spec["approval"]["fingerprint"]: add("P0", "R3", "approval", "content or images changed after Divit approved this page: it must go back through review and approval")
            except Exception as e: add("P1", "R3", "approval", f"cannot verify the approval fingerprint: {e}")

    # ---------- D: duplication against siblings in the same hub ----------
    sents = {s.strip() for s in re.split(r"(?<=[.?])\s+", body) if len(s.split()) >= 9}
    for sib in siblings:
        if sib["url"] == spec["url"] or sib.get("hub") != hub: continue
        sb = " ".join(strip_html(v) for k, v in sib.get("fields", {}).items() if isinstance(v, str) and k != "why_table")
        dup = [s for s in sents if s in sb]
        if len(dup) >= 2: add("P1", "D1", "body", f"{len(dup)} sentences copied from {sib['url']}: \"{dup[0][:60]}...\"")
    return I

def load_specs(paths):
    return [dict(json.load(open(p)), _path=p) for p in paths]

def main(argv):
    if not argv: print(__doc__); return 0
    if argv[0] == "--all": paths = sorted(glob.glob(os.path.join(ROOT, "specs", "*", "*.json")))
    elif argv[0] == "--hub": paths = sorted(glob.glob(os.path.join(ROOT, "specs", CFG["hubs"][argv[1]]["repo_dir"], "*.json")))
    else: paths = argv
    every = load_specs(sorted(glob.glob(os.path.join(ROOT, "specs", "*", "*.json"))))
    total = 0
    for s in load_specs(paths):
        issues = check(s, every)
        blocking = [i for i in issues if i["sev"] in ("P0", "P1")]
        frozen = s.get("status") in ("live-draft", "published") and s.get("frozen", True)
        if not frozen: total += len(blocking)
        print(f"\n=== {s['url']}  [{s.get('status','')}{' (frozen baseline, not counted)' if frozen else ''}]  P0={sum(i['sev']=='P0' for i in issues)} P1={sum(i['sev']=='P1' for i in issues)} P2={sum(i['sev']=='P2' for i in issues)}")
        for i in sorted(issues, key=lambda x: x["sev"]):
            print(f"  {i['sev']} {i['code']:3s} {i['field']:22s} {i['msg']}")
    if KMAP is None: print("\n(note: plan/keyword_map.json missing; keyword checks K5-K7 skipped. Run: python3 plan/build_map.py <workbook>)")
    print(f"\nTOTAL (P0+P1) = {total}  ->  {'PASS' if total == 0 else 'BLOCKED: fix and re-run'}")
    return min(total, 100)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
