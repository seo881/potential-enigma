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
        if n != 15: add("P1", "S5", "faq", f"{n} FAQ items (exactly 15)")
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
        voice = plain
        if k == "mockup": voice = ""   # user-voice prompts may say "my"
        for m in WE_OUR.finditer(voice):
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
    # ---------- K: keywords, links, cannibalization ----------
    if prim:
        pr = norm(prim)
        def has(field_text): return pr in norm(field_text) or pr.rstrip("s") in norm(field_text)
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
        # secondary keywords: the FAQ should carry as many as it can
        if KMAP and prim:
            secs = [x["kw"].lower() for x in KMAP.get(spec["url"], {}).get("secondaries", [])]
            ftxt = " ".join((i.get("q", "") + " " + strip_html(i.get("a", ""))).lower() for i in fq.get("items", []))
            got = [x for x in secs if x in ftxt]; need = min(10, len(secs))
            if len(got) < need: add("P1", "K8", "faq", f"FAQ carries {len(got)} of {len(secs)} secondaries verbatim (need {need}); missing e.g. {[x for x in secs if x not in got][:5]}")
    body = " ".join(strip_html(v) for k, v in F.items() if isinstance(v, str) and k not in ("why_table",))
    if KMAP and prim:
        me = KMAP.get(spec["url"], {})
        mine = {norm(prim)} | {norm(s["kw"]) for s in me.get("secondaries", [])}
        heads = [strip_html(h3p(F[k])[0]) for k in F if re.match(r"(feature|tab_content)_\d", k) and h3p(F.get(k, ""))]
        heads += [F.get(k, "") for k in ("features_heading", "usecase_heading", "why_title", "howto_title", "h1", "meta_title")]
        heads += [i["q"] for i in (fq or {}).get("items", [])]
        for url, p in KMAP.items():
            if url == spec["url"] or p.get("status") == "live-off-plan": continue
            kp = norm(p["primary"])
            if kp in mine or any(kp in m for m in mine) or len(kp.split()) < 2: continue
            for hd in heads:
                if re.search(r"\b" + re.escape(kp) + r"\b", norm(hd)):
                    add("P1", "K5", "headings", f'uses sibling primary "{p["primary"]}" ({url}) in a heading: "{hd[:60]}"'); break
        secs = [s["kw"] for s in me.get("secondaries", [])][:15]
        if secs:
            hit = [s for s in secs if norm(s) in norm(body)]
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
                elif kind == "definition":
                    if norm(ref) != norm(prim): add("P1", "F2", "faq", "a definition item must define the page's primary keyword")
                else:
                    add("P1", "F2", "faq", f'unknown source type "{kind}" (paa, related, secondary, keyword, definition)')
            me_page = (KMAP or {}).get(spec["url"], {"primary": prim, "secondaries": []})
            ok_paa, _skip = S.eligible(live, me_page, prims)
            for i in ok_paa[:10]:
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
                for x in iss: add("P1", "I1", "image_brief", x)
                for x in notes: add("P2", "I2", "image_brief", x)
            except Exception as e:
                add("P2", "I0", "image_brief", f"image lint skipped ({type(e).__name__}: {e}); run bash ops/setup.sh")
            for i, tb in enumerate(spec["image_brief"].get("tabs", []), 1):
                p_ = (tb.get("prompt") or "").strip()
                if p_ and not (40 <= len(p_) <= 95): add("P2", "I3", f"tab {i} prompt", f"{len(p_)} chars; a prompt chip reads best at 60-85")

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
