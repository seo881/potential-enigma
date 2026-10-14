"""skeleton.py: ruling 15 (Divit 2026-10-13), constrained writing. Code builds everything that can be decided before prose; the writer
writes prose only, section by section, and each section is QC'd (and autofixed) as it is written.

    python3 ops/skeleton.py build URL --by A-w-<n>     the skeleton: 10 FAQ slots (passing questions locked verbatim, US display;
                                                       Semrush questions in filtered form; secondaries in slots), hub + related links,
                                                       comparison table, hero default prompt, names; spec.pipeline = "r15"
    python3 ops/skeleton.py pack URL                   the compact page pack: locked FAQ, link plan, sections, claims menu, prevention
    python3 ops/skeleton.py set URL FIELD TEXT         write one field (plain text or HTML, exactly as given)
    python3 ops/skeleton.py answer URL N TEXT [--q QUESTION]   FAQ answer for slot N (the question only for a secondary slot)
    python3 ops/skeleton.py check URL SECTION          autofix (code) then QC filtered to that section: hero|features|why|usecases|howto|faq|all
    python3 ops/skeleton.py assemble URL               build fields.faq (awbFAQ embed) and faq_sources from the slots; links wrapped by code

Locked slots: the question text is fixed by code (an AlsoAsked question in its US-spelling display, ruling 14; a Semrush question as filtered).
The writer never edits it. Secondary slots: the writer writes a natural question that carries every word of the secondary (K8).
"""
import collections, contextlib, io, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H, paa_gate as P, park_rescue as R, semrush_questions as SQ, spelling as SP

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
}
# T1 (ops/typeset.py) files width findings under its own field names (canary 2026-10-13: they never reached a section check)
for _sec, _extra in {"hero": ["prompt_chip"], "features": ["feature_title", "feature_body"], "usecases": ["tab_label", "tab_title", "tab_body"],
                     "howto": ["howto_step_des", "howto_step_title"], "faq": ["faq_heading", "faq_q", "faq_a"]}.items():
    SECTIONS[_sec] = SECTIONS[_sec] + _extra
DEF_RX = re.compile(r"^(what is|what's|what are|what does)\b")
HOW_RX = re.compile(r"^(how (do|to|can|would) (i|you|we)?\s*(make|create|build|set up|design|write))|^how to (make|create|build|set up)")

SMALL = {"a", "an", "the", "and", "or", "for", "of", "to", "in", "on", "with", "by", "at", "vs"}
def _title(t):
    """HUB_RULES 4 title case (canary 2026-10-13: the skeleton set 'Customer service automation Builder')."""
    ws = t.split()
    return " ".join(w if any(ch.isupper() for ch in w[1:]) else (w.capitalize() if i == 0 or w.lower() not in SMALL else w.lower()) for i, w in enumerate(ws))
def _fits(text, field):
    """The text renders within the widest approved rendering of that field (ops/typeset.py ceilings, T1)."""
    try:
        import typeset as TS
        cfg = json.load(open(os.path.join(ROOT, "config", "typography.json"))); md = TS.mode(); F = cfg["ceilings"][md]["fields"]
        return field not in F or TS.width(text, TS.FIELDS[field], md) <= F[field]["px"] + 0.5
    except Exception: return True
GENERIC_SHORT = {"landing page", "page", "form", "survey", "quiz", "automation", "workflow", "workflow automation", "questionnaire", "application"}
def _shorter(disp, url=None):
    """Display-name variants, shortest last: drop leading words (keeping the hub noun), then a trailing hub noun. Never a bare hub
    phrase ('Landing Page') or another page's primary ('Approval Workflow' on document-approval-workflow), canary 2026-10-14."""
    out = [v for v in _shorter_raw(disp) if v == disp or (v.lower() not in GENERIC_SHORT and v.lower() not in _sib_prims(url))]
    # last resort: the last distinctive word ("Approval" for Document Approval Workflow), never a bare hub noun
    distinct = [w for w in disp.split() if w.lower() not in {"landing", "page", "form", "survey", "quiz", "automation", "workflow", "questionnaire"}]
    if distinct and distinct[-1] not in out: out.append(distinct[-1])
    return out
def _sib_prims(url):
    return {P.norm(p_["primary"]) for u, p_ in H.kmap().items() if u != url and p_.get("primary")}
def _shorter_raw(disp):
    ws = disp.split(); out = [disp]
    for k in range(1, len(ws) - 1): out.append(" ".join(ws[k:]))   # keep the hub noun ("Service Automation"), A-r-5 note 2026-10-13
    if len(ws) > 2 and " ".join(ws[-2:]).lower() == "landing page": out.append(" ".join(ws[:-2]))
    elif len(ws) > 2 and ws[-1].lower() in ("automation", "workflow", "survey", "quiz", "form"): out.append(" ".join(ws[:-1]))
    return out

COUNTABLE = re.compile(r"\b(form|survey|quiz|page|website|site|workflow|system|process|pipeline|app|bot|tool|tracker|dashboard|portal|engine|questionnaire|application|sheet|checklist|template|report|letter|agreement|contract|waiver|release|log|list|plan|policy)s?$")
def _a(primary):   # article for a definition question ("an audit workflow"; none for a mass noun: "returns automation")
    return "an" if primary[:1].lower() in "aeiou" else "a"
def _art(primary):
    return (_a(primary) + " ") if COUNTABLE.search(P.norm(primary)) else ""

ACRO = P.r18()["acronyms"]   # rules/paa_patterns.json (ruling 18 part 4e: CFOs, KYC ...); None = never cased (it, us)
def case_acronyms(text):
    """Known acronyms in their house casing, plurals too ("cfos" -> "CFOs", "kpis" -> "KPIs"); words already cased are kept."""
    def one(m):
        w = m.group(0); lw = w.lower()
        if lw in ACRO: return ACRO[lw] or w
        if lw.endswith("s") and ACRO.get(lw[:-1]): return ACRO[lw[:-1]] + "s"
        return w
    return re.sub(r"(?<![A-Za-z0-9'-])[A-Za-z0-9][A-Za-z0-9'-]*(?![A-Za-z0-9'-])", one, text)
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
    """The skeleton's FAQ slots in fill order (no writes): definition, how-to-build, passing candidates, secondaries, flagged
    candidates; each skipped when same-intent (paa_gate.near_dup) as a slot already taken. cap None = every fillable slot, which is
    the feasibility count (ruling 18 part 5: feasibility and the skeleton agree by construction)."""
    km = H.kmap().get(url) or {}; prim = km.get("primary") or url.rsplit("/", 1)[1].replace("-", " ")
    g = P.Gate(url, extra); cands = candidates(url, extra); have = []; slots = []
    full = lambda: cap is not None and len(slots) >= cap
    # Gate.finish's within-page caps, as run_spec applies them to the FAQ (Divit 2026-10-14 step 4): PA6 respondents, PA8 brands
    resp = lambda q: g.asker(P.norm(q or "")) == "respondent"; brand = lambda q: any(P.has(b, P.norm(q or "")) for b in g.library)
    capped = lambda c: (resp(c["q"]) and sum(resp(x.get("q")) for x in slots) >= P.MAX_RESPONDENT) or (brand(c["q"]) and sum(brand(x.get("q")) for x in slots) >= P.MAX_BRANDED)
    pick = lambda rx: next((c for c in cands if rx.search(P.norm(c["q"])) and c not in have and not capped(c)), None)
    d = pick(DEF_RX); have += [d] if d else []
    slots.append(d or {"kind": "definition", "q": f"What is {_art(prim)}{prim}?", "ref": prim, "locked": True})
    h = pick(HOW_RX); have += [h] if h else []
    slots.append(h or {"kind": "definition", "q": (f"How do I create {_art(prim)}{prim}?" if _art(prim) else f"How do I set up {prim}?"), "ref": prim, "locked": True})
    near = lambda q: any(P.near_dup(q, x["q"], prim) or P.jacc(P.content(q), P.content(x["q"])) >= P.JACCARD_DUP for x in slots if x.get("q"))
    for c in [c for c in cands if not c.get("flagged")]:
        if full(): break
        if c in have or near(c["q"]) or capped(c): continue
        slots.append(c)
    carried = [P.content(x["q"]) for x in slots]
    for x in sorted(km.get("secondaries") or [], key=lambda x: -(x.get("msv") or 0)):
        if full(): break
        c = P.content(x["kw"])
        if not c or any(c <= q for q in carried) or any(r[0] in R.KW_RULES and r[1] == "reject" for r in g.judge({"q": x["kw"], "source": "secondary"})): continue
        carried.append(c); slots.append({"kind": "secondary", "q": None, "ref": x["kw"], "locked": False})
    for c in [c for c in cands if c.get("flagged")]:
        if full(): break
        if c in have or near(c["q"]) or capped(c): continue
        slots.append(c)
    return slots

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
    if len(slots) < 10: sys.exit(f"refused: only {len(slots)} FAQ slots from passing sources (ruling 15: the skeleton needs 10); not writable yet")
    hubpath = H.CFG["hubs"][hub]["path"]; hubtext = H.CFG["hubs"][hub]["hub_link_text"]
    for i, sl in enumerate(slots, 1): sl.update({"n": i, "a": sl.get("a") or "", "link": None})
    slots[1]["link"] = {"url": "https://emergent.sh" + hubpath, "anchor": hubtext, "write_as": f"Emergent's {hubtext}"}
    rel = related_targets(url); free = [sl for sl in slots[2:] if not sl["link"]]
    for t, sl in zip(rel, free[1::3] or free):
        sl["link"] = {"url": "https://emergent.sh" + t["url"], "anchor": t["anchor"]}
    s["pipeline"] = "r15"; s["faq_plan"] = slots
    F = s["fields"]; disp = _title(km.get("display_name") or prim)
    if not s.get("faq_heading"):
        s["faq_heading"] = next((h_ for h_ in (f"{d} Questions, Answered" for d in _shorter(disp, url)) if _fits(h_, "faq_heading")), f"{disp} Questions, Answered")
    F["breadcrumb"] = F.get("breadcrumb") or disp; F["product_name"] = F.get("product_name") or f"{disp} Builder"
    if not F.get("explore_cta"):
        F["explore_cta"] = next((c_ for c_ in (f"Build My {d}" for d in _shorter(disp, url)) if len(c_) <= 34), "Build Mine Now")
    if not F.get("hero_prompt"):
        tmpl = HERO[hub]
        if hub == "Auto" and re.search(r"\b(workflow|system|process|pipeline|app|bot|tool|tracker|dashboard|portal|engine)$", P.norm(prim)):
            tmpl = "Build {a} {p} that runs on its own and logs every step."   # countable primary takes an article (canary 2026-10-14)
        F["hero_prompt"] = "<p>" + tmpl.format(p=prim, a=_a(prim)) + "</p>"
    s.setdefault("keywords", {})["primary"] = prim
    save(url, s)
    vs, rows = default_table(url)
    if len(vs) == 3:   # in-process: a library name may hold commas ("AI site builders (Wix, Framer)") that the CLI would split
        import table as TB
        try:
            html = TB.render(H.CFG["hubs"][hub]["repo_dir"], vs, rows)
            s2 = load(url); s2["fields"]["why_table"] = html; s2["table"] = {"vs": vs, "rows": rows, "variant": None}; save(url, s2)
        except Exception as e: print(f"table not built: {e}")
    s = load(url); s.setdefault("skeleton", {}).update({"built_by": by, "built": H.now(), "slots": len(slots), "flagged": sum(1 for x in slots if x.get("flagged")),
                                                        "flag_subtypes": sorted({f for x in slots for f in (x.get("flagged") or [])}),
                                                        "locked": sum(1 for x in slots if x["locked"]), "table": bool(s.get("table"))})
    save(url, s)
    print(f"{url}: skeleton built ({sum(1 for x in slots if x['locked'])} locked FAQ questions, {sum(1 for x in slots if not x['locked'])} secondary slots, "
          f"{sum(1 for x in slots if x.get('flagged'))} FLAGGED (cannot ship until Divit ticks the subtype), "
          f"{sum(1 for x in slots if x['link'])} links, table {'yes' if s.get('table') else 'NO'}); next: skeleton.py pack {url}")

def cmd_pack(a):
    url = a[0]; s = load(url); km = H.kmap().get(url) or {}
    caps = json.load(open(os.path.join(ROOT, "rules", "capabilities.json")))["approved"]
    out = [f"# Page pack (ruling 15): {url}", "", f"Primary: {km.get('primary')} | intent: {km.get('intent')} | angle note: {(km.get('angle') or '')[:300]}", "",
           "## Sections, in order (write one, run `skeleton.py check URL <section>`, fix to 0, then the next)",
           "1 hero: meta_title, meta_description, h1, hero_description, prompt_chip_1-4 + chip_adds (hero_prompt, product_name, breadcrumb, explore_cta are set by code)",
           "2 features: features_heading, features_subheading, feature_1-6", "3 why: why_title, why_description (the table is built by code)",
           "4 usecases: usecase_heading, tab_label_1-4, tab_content_1-4, mockup, image_brief", "5 howto: howto_title, howto_description, 7 steps",
           "6 faq: one answer per slot with `skeleton.py answer URL N TEXT`; then `skeleton.py assemble URL`; then `skeleton.py check URL faq`", "",
           "## FAQ slots (locked questions are fixed; write the answer only)"]
    for sl in s.get("faq_plan") or []:
        q = sl["q"] if sl["locked"] else (f"[Semrush: keep or reword naturally (head phrase stays; --q): {sl['q']}]" if sl["kind"] == "semrush"
                                          else f"[you write a question carrying every word of: {sl['ref']}]")
        if sl.get("flagged"): q += f"  [FLAGGED: {', '.join(sl['flagged'])}; write it like any other; it waits for Divit's packet tick]"
        ln = f" | LINK: write the words \"{sl['link'].get('write_as') or sl['link']['anchor']}\" in the answer (code makes them the link)" if sl.get("link") else ""
        out.append(f"{sl['n']:2d}. ({sl['kind']}{', locked' if sl['locked'] else ''}) {q}{ln}")
    out += ["", "## Claims menu (cite the id in spec.claims_used; say nothing about Emergent outside these)"] + [f"- {c['id']}: {c['claim']}" for c in caps]
    out += ["", "## Third-party facts", "Every fact about another product, a law or a professional standard needs spec.domain_sources {claim, source_url, date, quote}: `quote` is the exact span from the source that states it. No span, no claim.",
            "Stay inside the span: a detail the quote does not state (how a file is sent, 'by API', a date, a number) needs its own source or comes out. GOOD: 'the buyer sends the approved invoice file to the bank' (the span). BAD: 'Emergent sends that file through the bank's API' (the span says nothing about an API).",
            "Never claim a step stops, prevents or eliminates a risk (fraud, fakes, spam, errors, duplicates) unless a source says so: say what it does. GOOD: 'confirmation keeps typed-in fake addresses from counting'. BAD: 'confirmation stops throwaway accounts' (a disposable inbox confirms too). QC R15 flags it.",
            "Never put an Emergent line in an answer that names another brand: next to a cited competitor fact it reads as a comparison (QC R15, CONTENT_DEFECTS #8). Put the Emergent line in an answer that names no other company."]
    pm = os.path.join(ROOT, "docs", "PREVENTION.md")
    if os.path.exists(pm):
        txt = open(pm).read(); m = re.search(r"## (?:\d+\.\s*)?Page-pack instructions.*?(?=\n## |\Z)", txt, re.S)
        if m: out += ["", m.group(0).strip()]
    p = os.path.join(ROOT, ".cache", "packs", url.rsplit("/", 1)[1] + ".r15.md"); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write("\n".join(out)); print(p)

def cmd_set(a):
    url, field, text = a[0], a[1], a[2]; s = load(url)
    if field in ("hero_prompt", "why_table", "faq", "slug", "category"): sys.exit(f"refused: {field} is built by code (ruling 15)")
    if field == "chip_adds": s["chip_adds"] = json.loads(text)
    elif field == "image_brief": s["image_brief"] = json.loads(text)
    elif field in ("plan", "domain_sources", "claims_used"): s[field] = json.loads(text)
    else: s["fields"][field] = text
    save(url, s); print(f"set {field}")

def cmd_answer(a):
    url, n, text = a[0], int(a[1]), a[2]; s = load(url); sl = s["faq_plan"][n - 1]
    if "--q" in a:
        if sl["locked"]: sys.exit(f"refused: slot {n}'s question is locked (ruling 15)")
        q = a[a.index("--q") + 1]
        if sl["kind"] == "semrush":
            if not any(h.search(P.norm(q)) for h in P.Gate(url).heads): sys.exit("refused: a reworded Semrush question must keep the head phrase (backlog line 91)")
        elif not all(w in P.norm(q) for w in P.norm(sl["ref"]).split()): sys.exit(f"refused: the question must carry every word of the secondary '{sl['ref']}' (K8)")
        sl["q"] = q
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
        src = {"alsoasked": "alsoasked", "semrush": "keyword", "secondary": "secondary", "definition": "definition"}[sl["kind"]]
        e = {"q": sl["q"], "source": src, "ref": sl["ref"]}
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
