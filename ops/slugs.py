"""THE slug function (PERMANENT SLUG RULE, Divit 2026-10-23, final wording; CLAUDE.md and DECISIONS). Used everywhere:
ops/slug_migrate.py map, hubctl api-create (blocking), hubctl ship-check (blocking), hubctl slug-check, verify-live and the live audit.

  The target keyword is the one the page H1 is built around. The slug is that keyword STANDALONE: no prefixes (custom, best, top,
  free, online, AI), no suffixes (generator, maker, builder, template, app, website, examples), singular not plural. Then remove
  ONLY the hub category word (LP "landing page"; Form "form"; Automation "automation"; SurveyQuiz "survey" and "quiz").
  Lowercase and hyphenated, nothing else changed.

The only exceptions, in EXCEPTIONS below: safety-quiz, team-quiz, wellness-quiz (collisions with the live surveys); custom-order and
free-trial ("custom" and "free" are part of the page's own name; Divit 2026-10-23).
"""
import re

CATEGORY = {   # token sequences, longest first; plurals are the same word
    "LP":         [["landing", "pages"], ["landing", "page"]],
    "Form":       [["forms"], ["form"]],
    "Auto":       [["automations"], ["automation"]],
    "SurveyQuiz": [["surveys"], ["survey"], ["quizzes"], ["quiz"]],
}
PREFIXES = {"custom", "best", "top", "free", "online", "ai"}
SUFFIXES = {"generator", "maker", "builder", "template", "app", "website", "examples", "example"}
SUFFIX_PLURAL = {"generators": "generator", "makers": "maker", "builders": "builder", "templates": "template", "apps": "app", "websites": "website"}
LEAD = {"build", "a", "an", "the", "your", "own"}          # an H1 lead ("Build a ...", "Build Your Own ...") is not part of the keyword
CONNECT = {"and", "for", "with", "to", "that", "in", "on", "using", "by", "from", "of"}   # a clause after a suffix ("Generator and Signing App")
# singular of the keyword's last word: the irregular or ambiguous plurals spelled out, then a regular -s only where it is safe
PLURAL = {"pages": "page", "forms": "form", "surveys": "survey", "quizzes": "quiz", "sites": "site", "questionnaires": "questionnaire",
          "sheets": "sheet", "letters": "letter", "agreements": "agreement", "contracts": "contract", "waivers": "waiver",
          "workflows": "workflow", "automations": "automation", "polls": "poll", "funnels": "funnel", "slips": "slip"}
NOT_PLURAL = {"news", "sales", "business", "analytics", "logistics", "ethics", "fitness", "wellness", "class", "glass", "process", "status",
              "address", "access", "success", "progress", "express", "campus", "bonus", "census", "series", "species", "basics",
              "operations", "relations", "dynamics", "economics", "graphics", "metrics", "statistics", "returns", "minutes", "thanks",
              "yes", "jobs", "hr", "its", "us", "kudos", "means", "always", "pros", "aids", "goods", "earnings", "savings", "lens",
              "tennis", "chess", "dress", "christmas", "physics", "mathematics", "politics", "electronics", "esports", "sports", "ads",
              "questions", "results", "rewards", "leads", "events", "reviews", "terms", "rsvps", "nps", "kpis", "okrs", "sms", "pos", "gps", "faqs", "plus", "bus"}
EXCEPTIONS = {   # the ONLY named exceptions (Divit 2026-10-23): (hub, target keyword) -> slug
    ("SurveyQuiz", "safety quiz"): "safety-quiz", ("SurveyQuiz", "team quiz"): "team-quiz", ("SurveyQuiz", "wellness quiz"): "wellness-quiz",   # collisions with the live surveys
    ("Form", "custom order form"): "custom-order", ("LP", "free trial landing page"): "free-trial",   # "custom" / "free" are part of the page's own name
}
EXCEPTION_SLUGS = {(h, s) for (h, _k), s in EXCEPTIONS.items()}


def tokens(text):
    return [t for t in re.sub(r"[^a-z0-9]+", " ", (text or "").lower().replace("'", "").replace("’", "")).split() if t]


def strip_category(hub, toks):
    out, i = [], 0
    while i < len(toks):
        for s in CATEGORY[hub]:
            if toks[i:i + len(s)] == s: i += len(s); break
        else: out.append(toks[i]); i += 1
    return out


def standalone(toks):
    """the keyword standalone: H1 lead, prefixes, suffixes (and a clause after one) gone, last word singular."""
    t = list(toks)
    if t and t[0] == "build":
        t = t[1:]
        while t and t[0] in LEAD: t = t[1:]
    while len(t) > 1 and t[0] in PREFIXES:
        t = t[1:]
        if len(t) > 1 and t[0].isdigit(): t = t[1:]
    for i in range(1, len(t)):   # a suffix followed by a clause: cut there ("nda form generator and signing app")
        w = SUFFIX_PLURAL.get(t[i], t[i])
        if w in SUFFIXES and (i + 1 == len(t) or t[i + 1] in CONNECT): t = t[:i]; break
    while len(t) > 1 and SUFFIX_PLURAL.get(t[-1], t[-1]) in SUFFIXES: t = t[:-1]
    if t:
        w = t[-1]
        if w in PLURAL: t[-1] = PLURAL[w]
        elif w.endswith("ies") and len(w) > 4: t[-1] = w[:-3] + "y"
        elif w.endswith("s") and not w.endswith(("ss", "us", "is")) and w not in NOT_PLURAL and len(w) > 3: t[-1] = w[:-1]
    return t


def slug_for(hub, target_keyword):
    """THE slug for a page of HUB whose H1 is built around target_keyword (a keyword or the H1 phrase itself)."""
    key = " ".join(tokens(target_keyword))
    if (hub, key) in EXCEPTIONS: return EXCEPTIONS[(hub, key)]
    return "-".join(strip_category(hub, standalone(tokens(target_keyword))))


def has_banned(hub, slug):
    """[(kind, word)] for a category word, listed prefix or listed suffix anywhere in a slug (exceptions aside)."""
    if (hub, slug) in EXCEPTION_SLUGS: return []
    t = slug.split("-"); out = []
    if strip_category(hub, t) != t: out.append(("category", next("-".join(s) for s in CATEGORY[hub] for i in range(len(t)) if t[i:i + len(s)] == s)))
    if t and t[0] in PREFIXES: out.append(("prefix", t[0]))
    out += [("suffix", w) for w in t[1:] if SUFFIX_PLURAL.get(w, w) in SUFFIXES]
    return out


def _norm(t): return " ".join(tokens(t))


def keyword_in_h1(h1, kw):
    """the H1 carries the target keyword (case and hyphen/space aside, the last word may be plural)."""
    tk = tokens(kw)
    if not tk: return False
    rx = r"(?<![a-z0-9])" + r"[^a-z0-9]+".join(re.escape(x) for x in tk) + r"s?(?![a-z0-9])"
    return bool(re.search(rx, (h1 or "").lower())) or bool(standalone(tk) and re.search(r"(?<![a-z0-9])" + r"[^a-z0-9]+".join(re.escape(x) for x in standalone(tk)) + r"s?(?![a-z0-9])", (h1 or "").lower()))


def problems(hub, slug, target_keyword, h1=None):
    """[] when the slug is slug_for(target keyword) (and, given an H1, the H1 carries the keyword); else the reasons. BLOCKING."""
    if not target_keyword: return ["no target keyword (spec keywords.primary)"]
    out = []
    want = slug_for(hub, target_keyword)
    if slug != want: out.append(f"slug '{slug}' != slug_for('{target_keyword}') = '{want}'")
    for kind, w in has_banned(hub, slug): out.append(f"slug '{slug}' carries the {kind} '{w}'")
    if h1 is not None and not keyword_in_h1(h1, target_keyword): out.append(f"H1 does not carry the target keyword '{target_keyword}'")
    return out


def migration_pending():
    """True while the slug-migration freeze is active (status/freeze.json): live pages still carry old slugs, so verify-live and the
    live audit report a slug mismatch without failing; create and ship-check block regardless."""
    import json, os
    fp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "status", "freeze.json")
    try: f = json.load(open(fp))
    except (OSError, ValueError): return False
    return bool(f.get("active")) and "slug migration" in (f.get("reason") or "").lower()


def spec_problems(hub, url, spec):
    """problems() for a spec: slug from its url, target keyword from keywords.primary, H1 from fields.h1."""
    kw = spec.get("keywords") if isinstance(spec.get("keywords"), dict) else {}
    return problems(hub, url.rsplit("/", 1)[1], kw.get("primary"), (spec.get("fields") or {}).get("h1"))


_RENAMES = None
def git_rels(rel):
    """[rel] plus its pre-migration path (specs/<dir>/<old>.json or images/<dir>/<old>/...), so git history and git show at a commit
    before the slug migration still find the file (DECISIONS 2026-10-23; renames come from plan/slug-migration.json)."""
    global _RENAMES
    import json, os
    if _RENAMES is None:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _RENAMES = {}
        try:
            cfg = json.load(open(os.path.join(root, "config", "collections.json")))["hubs"]
            for e in json.load(open(os.path.join(root, "plan", "slug-migration.json")))["pages"]:
                if e["new_slug"] != e["old_slug"] and e.get("decision") in ("change",):
                    d = cfg[e["hub"]]["repo_dir"]; _RENAMES[(d, e["new_slug"])] = e["old_slug"]
        except (OSError, ValueError, KeyError): pass
    parts = rel.replace(os.sep, "/").split("/")
    if len(parts) >= 3 and parts[0] in ("specs", "images"):
        slug = parts[2][:-5] if parts[0] == "specs" and parts[2].endswith(".json") else parts[2]
        old = _RENAMES.get((parts[1], slug))
        if old: return [rel, "/".join(parts[:2] + [old + (".json" if parts[0] == "specs" and parts[2].endswith(".json") else "")] + parts[3:])]
    return [rel]


def git_show(sha, rel, root):
    """git show sha:rel, falling back to the pre-migration path; '' when neither exists."""
    import subprocess
    for r in git_rels(rel):
        p = subprocess.run(["git", "show", f"{sha}:{r}"], cwd=root, capture_output=True, text=True)
        if p.returncode == 0: return p.stdout
    return ""


_STORE = None
def store_key(url):
    """The key of a page's slug-keyed stores (private/alsoasked/<key>.json, AlsoAsked verdicts, Semrush derived questions,
    rules/paa_blocklist.json per_page, rules/paa_synonyms.json, rules/paa_synonym_candidates.json, rules/flag_decisions.json
    "<key>:<hash>", status/synonyms.json, status/swap_short.json). These stores are keyed by a bare slug ACROSS hubs, and the
    migrated slugs repeat across hubs (crm, membership, newsletter, it ...), so they keep the pre-migration slug, which is unique:
    a page in plan/slug-migration.json -> its old slug (old == new when unchanged); a page created after the migration ->
    "<slug>--<repo dir>" (never shared across hubs). DECISIONS 2026-10-23 SLUG MIGRATION."""
    global _STORE
    import json, os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cfg = json.load(open(os.path.join(root, "config", "collections.json")))["hubs"]
    if _STORE is None:
        _STORE = {}
        for f in (os.path.join(root, "plan", "slug-migration.json"), os.path.join(root, "private", "migration", "slug-migration-kmap.json")):
            try:
                for e in json.load(open(f))["pages"]:
                    _STORE.setdefault(f"{cfg[e['hub']]['path']}/{e['new_slug'] if e.get('decision') != 'collision' else e['old_slug']}", e["old_slug"])
                    _STORE.setdefault(f"{cfg[e['hub']]['path']}/{e['old_slug']}", e["old_slug"])
            except (OSError, ValueError, KeyError): pass
    url = (url or "").split("?")[0].rstrip("/")
    if url in _STORE: return _STORE[url]
    slug = url.rsplit("/", 1)[-1]
    d = next((h["repo_dir"] for h in cfg.values() if url.startswith(h["path"] + "/")), None)
    return f"{slug}--{d}" if d else slug
