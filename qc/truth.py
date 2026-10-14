"""truth.py: QC C6 and C7, claim and span binding (Divit 2026-10-14, spot-check under ruling 20; plan/truth-gap-2026-10-14.md).

B's review blocking rate on 2026-10-14 was 7 of 9 pages, 6 of them truth findings. Every one got through writing and QC because
spec.claims_used and spec.domain_sources were page-level lists that no check tied to a sentence: QC only asked that the lists exist
(R15, C2), that each quote had 6+ words (R15) and that the plan's own claims were listed (P2). C3 looks only for a fixed brand list
plus a fact verb, or a percentage. These checks bind sentences:

C6 (Emergent claims, every copy field and FAQ answer)
  - a sentence where Emergent itself is the subject does what an approved claim says: it builds, writes, changes, connects, exports
    or hosts (prompt-build, api-connect, code-export, custom-domain), or it matches an approved claim's wording; anything else is
    platform behaviour stated as automatic (CONTENT_DEFECTS #14): say the built app does it, or that the user prompts for it;
  - a plan or limit claim (free-start, no-caps) ends at its approved wording: no consequence clause after it;
  - billing, pricing, seat or credit words in a sentence about Emergent sit inside an approved wording;
  - the claim id a sentence relies on is listed in spec.claims_used.
C7 (third-party facts, FAQ answers, feature bodies and the features subheading)
  - a flat "No"/"Yes" answer to a question about what a category of third-party software or a law does needs a quoted span;
  - a sentence about a product category ("... software", "... tools", "... solutions") with a hard qualifier (never, only, all,
    "two kinds") needs a quoted span that carries the qualifier;
  - a sentence that names a vendor, a law or a regulator, or defines the primary keyword, is bound to a quote, and its numbers and
    scope qualifiers ("central", "once a year") sit inside the bound quotes.

Ruling 15: new writing only. check_spec() runs the rules only on r15 pages whose skeleton was built at or after rules/truth.json
`since` and that have no review, so `hubctl recheck` can never send a reviewed or live page to rework or the fix queue for them.
findings() is the pure rule (golden cases call it directly).
"""
import json, os, re, glob
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(ROOT, "rules", "truth.json")))
CAPS = json.load(open(os.path.join(ROOT, "rules", "capabilities.json")))
WORDING = {k: [re.compile(p, re.I) for p in v] for k, v in R["wording"].items()}
VERB_CLAIM = {v: cid for cid, vs in R["emergent_verbs"].items() for v in vs}
PLATFORM = re.compile(R["platform_terms"], re.I)
HARDQ = re.compile(R["hard_qualifiers"], re.I)
SPANQ = re.compile(R["span_qualifiers"], re.I)
INTEG = re.compile(r"\b(sync\w*|connect\w*|API|APIs|integrat\w*|two-way|reads? (from|and writes)|writes? (back|to|into)|posts? (to|into)|pushes|pulls? from)\b")
CATSUBJ = re.compile(r"^(?:(?!Your\b|The app\b|An app\b|Apps\b|Emergent\b|Some\b|Many\b|Most\b|Certain\b|A few\b|Several\b)[A-Za-z][\w'-]*\s+){0,5}?(?:" + R["category_nouns"] + r")\s+(?!(?:and|or|that|which|for|with|like|such|from|in|on|of|to|is|are)\b)([a-z]+)\b")
QCAT = re.compile(R["question_category"], re.I)
QEXCL = re.compile(R["question_exclude"], re.I)
HEDGE = re.compile(R["flat_hedges"], re.I)
TAILM = re.compile(R["tail_markers"], re.I)
SYN = {w: g for g in R["qualifier_synonyms"] for w in g}
GENERIC = set(R["generic_words"])
NON_VERBS = {"plus", "thus", "this", "us", "its", "as", "always", "perhaps", "yes", "versus", "news", "ads", "apps", "teams", "users", "customers", "forms", "pages", "rules"}
PLAN_CLAIMS = {"free-start", "no-caps", "code-export", "custom-domain"}
ADVERBS = {"also", "then", "only", "still", "now", "simply", "just", "already", "automatically", "instantly", "first", "even"}
MODALS = {"can", "could", "will", "would", "may", "might"}
STOP = set("""a an the and or but if then than so of to in on at by for with from into onto over under as is are was were be been being it its
this that these those there their they them you your yours we our us he she his her i me my not no yes do does did done can could will would
should may might must shall have has had each every any all some such which who whom whose what when where why how one also only more most other
same own about after before while because until up out off just very per via both either neither own s t""".split())

def strip_html(s): return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", s or "")).replace("\\\"", '"')).strip()
def blocks(html):
    """Block-level parts of a field (an <h3> title and its <p> body are separate sentences)."""
    return [b for b in (strip_html(x) for x in re.split(r"(?i)</(?:h\d|p|li|div)>|<br\s*/?>", html or "")) if b]
def sents(t): return [x.strip() for x in re.split(r"(?<=[.?!])\s+", t) if x.strip()]
def _stem(w):
    w = w.lower().strip("'").removesuffix("'s")
    for suf in ("ies", "ing", "ed", "es", "s"):
        if len(w) >= len(suf) + 3 and w.endswith(suf) and not w.endswith("ss"):
            w = w[:-len(suf)] + ("y" if suf == "ies" else ""); break
    return w[:-1] if len(w) > 3 and w.endswith("e") else w   # base/based, rate/rated: one stem
def content(t, drop=()):
    return {_stem(w) for w in re.findall(r"[A-Za-z][A-Za-z0-9'-]*|\d[\d,.]*", t) if w.lower() not in STOP and w.lower() not in GENERIC and _stem(w) not in drop}

def faq_items(spec):
    m = re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;\s*</script>", (spec.get("fields") or {}).get("faq") or "", re.S)
    try: return json.loads(m.group(1))["items"] if m else []
    except Exception: return []

def _brands(spec):
    """Vendor names: every competitor library, the domain_sources hosts, and capitalised names that appear in the page's own quotes."""
    import urllib.parse as up
    b = set()
    for lf in glob.glob(os.path.join(ROOT, "rules", "competitors", "*.json")):
        try:
            for name in json.load(open(lf)).get("competitors", {}):
                b |= {x.strip() for x in re.split(r"[/,()]", name) if len(x.strip()) > 2 and "builder" not in x.lower()}
        except Exception: pass
    b |= {"Shopify", "WooCommerce", "BigCommerce", "QuickBooks", "Xero", "NetSuite", "Salesforce", "HubSpot", "Stripe", "PayPal", "Mailchimp",
          "Airtable", "Calendly", "Asana", "Jira", "Coupa", "SAP", "Oracle", "Workday", "ADP", "Gusto", "Paychex", "BILL", "HighRadius",
          "Zendesk", "Epic", "Cerner", "Drata", "Vanta", "UiPath", "Blue Prism", "Automation Anywhere", "Typeform", "Jotform", "Wix", "Squarespace"}
    for d in spec.get("domain_sources") or []:
        host = up.urlparse(d.get("source_url") or "").netloc.lower().removeprefix("www.").split(".")
        if len(host) >= 2 and host[-2] not in ("wikipedia", "gov", "europa", "ecfr", "nist", "census", "bls", "irs", "hhs", "investopedia", "ibm", "britannica", "oyster", "oysterhr"):
            b.add(host[-2])   # matched case-insensitively against a capitalised word only (see _names)
    prim = set(re.findall(r"[a-z0-9]+", ((spec.get("keywords") or {}).get("primary") or "").lower()))
    b = {x for x in b if x.lower() != "emergent" and x.lower() not in prim}   # "SEO" on the SEO automation page is the topic, not a vendor
    page = {x.lower() for d in spec.get("domain_sources") or [] for x in b if x.lower() in up.urlparse(d.get("source_url") or "").netloc.lower()}
    return b, page, prim

def _names(sent, brands):
    brands, page, brands_prim = brands
    out = []
    for x in brands:
        pat = r"(?<![A-Za-z])" + r"\s+".join(re.escape(w) for w in x.split()) + r"(?![A-Za-z])"
        for m in re.finditer(pat, sent, 0 if not x.islower() else re.I):
            if not m.group(0)[0].isupper(): continue
            if m.start() == 0 and " " not in x and x[1:].islower() and x.lower() not in page: continue   # "Outreach sequences ...": a common word
            if m.group(0) not in out: out.append(m.group(0))
            break
    for r_ in R["regulators"]:
        if r_.lower() in brands_prim: continue
        if re.search(r"(?<![A-Za-z0-9])" + re.escape(r_) + r"(?![A-Za-z0-9])", sent): out.append(r_)
    return out

def _claims_in(text, used=None):
    """[(claim id, start, end)] for every approved-wording match in text (only ids in `used` when given)."""
    return [(cid, m.start(), m.end()) for cid, pats in WORDING.items() if used is None or cid in used for p in pats for m in p.finditer(text)]

TAIL_OK = re.compile(r"^\s*(?:(?:on|with|in|for|from) (?:Emergent|the app|every app|apps? built (?:with|on|in) Emergent|an app Emergent builds)|(?:your|the|an?|each|every|that|this|its)(?: first| new| finished)? (?:app|form|page|survey|workflow|site|quiz|automation|tool)s?|it|them)?\s*[.?!:)]*\s*$", re.I)
JOIN = re.compile(r"^\s*(?:,\s*)?(?:and|or|,|;)\s+(?:the |an? |with |it has |there is )?", re.I)

def _emergent_findings(field, sent, used):
    out = []
    used = set(used or [])
    hits = _claims_in(sent)
    # (1) a plan or limit claim ends at its approved wording (compliance FAQ 2, crm feature_5 on 2026-10-14)
    ends = sorted((e, cid) for cid, s_, e in hits if cid in R["end_at_wording"])
    if ends:
        end = max(e for e, _ in ends)
        rest = sent[end:]
        while True:   # another approved wording chained with "and" / "," continues the claim
            j = JOIN.match(rest)
            nxt = j and next(((cid, s_, e) for cid, s_, e in _claims_in(rest[j.end():]) if s_ == 0), None)
            if not nxt: break
            rest = rest[j.end() + nxt[2]:]
        if not TAIL_OK.match(rest) and TAILM.search(rest):
            out.append(("C6", field, f'plan or limit claim "{sent[ends[-1][0] - 20 if ends[-1][0] > 20 else 0:ends[-1][0]].strip()}..." runs past its approved wording ("{rest.strip()[:50]}"): end the sentence at the claims.json wording; a consequence of it is a new claim'))
    for cid in dict.fromkeys(c_ for c_, _, _ in hits):
        if used and cid not in used: out.append(("C6", field, f'the sentence states claim {cid} ("{sent[:50]}..."): list {cid} in spec.claims_used'))
    # (2) billing, pricing, seat and credit words in a sentence about Emergent sit inside an approved wording
    if re.search(r"\bEmergent\b(?!'s)", sent) or any(c_ in PLAN_CLAIMS for c_, _, _ in hits):
        spans = [(s_, e) for _, s_, e in hits]
        for m in PLATFORM.finditer(sent):
            if not any(s_ <= m.start() and m.end() <= e for s_, e in spans):
                out.append(("C6", field, f'"{m.group(0)}" states a plan, price or billing term about Emergent outside any approved claim wording (rules/capabilities.json): cut it or use the approved wording')); break
    # (3) Emergent itself as the subject: build-time verbs and approved wordings only (accounting FAQ 2, CONTENT_DEFECTS #14)
    for m in re.finditer(r"\bEmergent\b(?!'s)(?!-)", sent):
        prev = re.findall(r"[A-Za-z']+", sent[:m.start()])
        if prev and prev[-1].lower() in R["subject_blockers"]: continue
        toks = re.findall(r"[A-Za-z'-]+", sent[m.end():])[:6]
        i = 0
        while i < len(toks) and toks[i].lower() in ADVERBS: i += 1
        if i < len(toks) and toks[i].lower() in MODALS: continue          # "Emergent can build ...": a buildable feature (HUB_RULES 6)
        if i >= len(toks): continue
        verbs = [toks[i]]
        tail = sent[m.end():]
        for c in re.finditer(r"(?:,\s*(?:and\s+|then\s+)?|\s+and\s+(?:then\s+)?)([a-z]+(?<!ss)s)\s+(?=(?:your|the|a|an|each|every|its|it|them|any|all|that|those|this|to|from|in|back)\b)", tail):
            if re.search(r"\b(that|which|who|where|when|so|because|while|until)\b", tail[:c.start()]): break   # a relative or new clause: its verbs belong to the app
            verbs.append(c.group(1))
        for v in verbs:
            lv = v.lower()
            if not lv.endswith("s") or lv.endswith("ss") or lv in NON_VERBS: break               # "an Emergent app", "Emergent project": not a subject
            lemma = {"is": "be", "has": "have", "does": "do", "sets": "set", "lays": "lay"}.get(lv) or (lv[:-2] if re.search(r"(sh|ch|x|z|ss)es$", lv) else lv[:-1])
            if lemma == "set" and re.search(r"\bsets? up\b", sent): lemma = "set up"
            cid = VERB_CLAIM.get(lemma)
            if cid:
                if used and cid not in used: out.append(("C6", field, f'"Emergent {v}" relies on claim {cid}: list it in spec.claims_used'))
                continue
            if hits: continue     # the sentence states an approved wording ("Emergent has no task cap"); an uncited id is reported above
            out.append(("C6", field, f'"Emergent {v} ..." states platform behaviour that no approved claim covers (CONTENT_DEFECTS #14): say the built app does it ("the app {v} ...") or that the user prompts for it, or use a claims.json wording'))
            break
        else: continue
    return out

def _bind(sent, quotes, drop):
    """Best quoted span for a sentence: (share of the sentence's content words found in one quote, the quote, shared words)."""
    cw = content(sent, drop)
    best = (0.0, None, set())
    for q in quotes:
        sh = cw & content(q, drop)
        sc = len(sh) / max(len(cw), 1)
        if sc > best[0]: best = (sc, q, sh)
    return best

def _qualifiers_outside(sent, quotes):
    qtext = " ".join(q for q in quotes if q).lower()
    out = []
    for m in SPANQ.finditer(sent):
        w = m.group(0).lower()
        pre = re.search(r"\b([A-Z][A-Za-z]+)\s+$", sent[:m.start()])
        if w[0].isdigit() and pre and pre.group(1) not in ("In", "On", "By", "For", "At", "From", "Since", "Until", "After", "Before", "About", "Over", "Under"):
            continue   # a number in a name ("Indicator 8", "Form 941", "Recital 32")
        if any(re.search(r"(?<![a-z0-9])" + re.escape(x) + r"(?![a-z0-9])", qtext) for x in SYN.get(w, [w])): continue
        if w in SYN.get("must", ()) and any(re.match(R["obligation_quote"], q or "", re.I) for q in quotes): continue   # a quoted requirement ("conduct a CHNA every three years")
        out.append(m.group(0))
    return out

def findings(spec):
    """Pure rule: [(code, field, message)] for the spec as new writing (no gating)."""
    F = spec.get("fields") or {}
    used = spec.get("claims_used") or []
    quotes = [d.get("quote") or "" for d in spec.get("domain_sources") or [] if (d.get("quote") or "").strip()]
    prim = ((spec.get("keywords") or {}).get("primary") or "").lower()
    drop = {_stem(w) for w in re.findall(r"[a-z0-9]+", prim)}
    brands = _brands(spec)
    out = []
    units = []   # (field label, kind, text, question)
    for k, v in F.items():
        if not isinstance(v, str) or k in ("faq", "why_table", "mockup", "hero_prompt", "slug", "category", "meta_title", "meta_description", "name", "breadcrumb", "explore_cta", "product_name") \
                or re.search(r"(?:^|_)heading$|_title$|_title_\d|^tab_label|^prompt_chip", k): continue
        units.append((k, "feature" if re.fullmatch(r"feature_\d|features_subheading", k) else "copy", blocks(v), None))
    for i, it in enumerate(faq_items(spec), 1):
        units.append((f"faq item {i}", "faq", [strip_html(it.get("a", ""))], strip_html(it.get("q", ""))))
    for field, kind, text, q in units:
        ss = [x for b in text for x in sents(b)]
        for s in ss: out += _emergent_findings(field, s, used)
        if kind == "copy": continue
        # C7 (a): a flat yes or no to a question about what third-party software, a provider or a law does (AR FAQ 4 and 6, payroll FAQ 7)
        if kind == "faq" and q and ss and re.match(r"^(no|yes)\b\s*[.,:;]", ss[0], re.I) and not HEDGE.match(ss[0]) and re.match(r"^(do|does|can|is|are|will|would|could)\b", q, re.I) \
                and QCAT.search(q) and not QEXCL.search(q) and "Emergent" not in q \
                and not re.search(r"\bEmergent\b|\bthe app\b|\byou can build\b", " ".join(ss[:2])):
            sc = max(_bind(x, quotes, drop)[0] for x in ss[:2])   # the yes or no and the sentence that carries it
            if sc < 0.5:
                out.append(("C7", field, f'opens with a flat "{ss[0].split()[0].strip(".,:;")}" about what a category of third-party software or a law does, with no quoted span that says it: answer what a domain_sources quote states ("It depends on the product: ..."), or answer for the app Emergent builds'))
        for s in ss:
            names = _names(s, brands)
            app_voice = bool(re.match(r"^(the|your|an|this|that|each) (app|form|workflow|automation|page|survey)\b|^apps? built\b|^in an app\b", s, re.I)) or "Emergent" in s
            imper = (s.split() or [""])[0].lower().strip(",:") in R["imperatives"]   # advice to the reader (SEVERITY: unsourced-advice is a note)
            integ = bool(INTEG.search(s)) or (names and all(n_ in R["api_connect_brands"] for n_ in names) and not re.search(r"\d|%|\b(charges?|costs?|fees?|limits?|caps?|does not|doesn't|cannot|can't|only|never)\b", s))   # a vendor named as the thing the built app connects to is an api-connect claim (C6), not a vendor fact
            cat = CATSUBJ.match(s)
            defn = bool(prim) and re.match(r"^(?:an? |the )?" + re.escape(prim) + r"s?\b(?:,? or [^,]+,)?\s+(is|are|means|refers to)\b", s.lower())
            hard = HARDQ.search(s)
            if cat and hard and not app_voice and cat.group(1) not in ("should", "need", "needs", "must", "can", "could", "may", "might"):   # advice, or a soft "some/most" (SEVERITY: a note)
                # C7 (b): a category generalization with a hard qualifier (healthcare FAQ 4 "two kinds", crm FAQ 4)
                sc, bq, _ = _bind(s, quotes, drop)
                miss = _qualifiers_outside(hard.group(0), [bq] if bq and sc >= 0.5 else [])
                if sc < 0.5 or miss:
                    out.append(("C7", field, f'"{s[:70]}": a statement about a product category with "{hard.group(0)}" needs a quoted span that says it (domain_sources), or cut the qualifier'))
                    continue
            if (names and not app_voice and not integ and not imper) or defn:
                # C7 (c): vendor, law or regulator facts and the primary's definition are bound to a quote, qualifiers included
                sc, bq, sh = _bind(s, quotes, drop)
                bound = sc >= 0.34 or len(sh) >= 3
                if names and not bound:
                    own = [d.get("quote") or "" for d in spec.get("domain_sources") or [] for n_ in names
                           if n_.lower() in ((d.get("quote") or "") + " " + (d.get("source_url") or "")).lower() or n_.lower() in (d.get("claim") or "").lower()]
                    if own and all(any(n_.lower() in ((d.get("quote") or "") + (d.get("source_url") or "") + (d.get("claim") or "")).lower() for d in spec.get("domain_sources") or []) for n_ in names):
                        u = _bind(s, [" ".join(own)], drop)
                        proper = {_stem(w) for w in re.findall(r"(?<!^)(?<![.!?] )\b[A-Z][\w'-]*", s)} | {_stem(w) for n_ in names for w in n_.split()}
                        v = _bind(s, [" ".join(own)], drop | proper)   # what the sentence says beyond the names it cites
                        if u[0] >= 0.34 or len(u[2]) >= 3 or v[0] >= 0.33: bound, bq = True, u[1]
                if not bound:
                    if not names: continue   # a definition in the writer's own words binds to no quote: a note at most (A-r-spot1)
                    what = ", ".join(names[:2]) if names else "the primary's definition"
                    out.append(("C7", field, f'"{s[:70]}" states a fact about {what} with no quoted span in domain_sources: add the source quote that says it, or cut it'))
                    continue
                near = [q_ for q_ in quotes if len(content(s, drop) & content(q_, drop)) >= 2] or [bq]
                cl = [c_ for c_ in re.split(r",\s+(?:and|while|but|so)\s+|;\s+|,\s+(?=an? app|the app|Emergent)", s) if not names or any(n_ in c_ for n_ in names)]
                miss = _qualifiers_outside(" ".join(cl) or s, near)   # only the clause that states the vendor or law fact
                if miss:
                    out.append(("C7", field, f'"{s[:70]}": "{", ".join(dict.fromkeys(miss))}" is not in the quoted span it rests on: keep to what the quote says, or source it'))
    seen, res = set(), []
    for o in out:
        if o not in seen: seen.add(o); res.append(o)
    return res

def applies(spec):
    """Ruling 15: new writing only. r15 pages built at or after `since`, not yet reviewed."""
    if spec.get("pipeline") != "r15" or spec.get("review"): return False
    built = (spec.get("skeleton") or {}).get("built") or ((spec.get("history") or [{}])[0] or {}).get("t", "")
    return bool(built) and built >= R["since"]

def check_spec(spec, add):
    if not applies(spec): return
    for code, field, msg in findings(spec): add("P1", code, field, msg)

if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        s = json.load(open(p))
        for f in findings(s): print(f"{os.path.basename(p)}  {f[0]} {f[1]}: {f[2]}")
