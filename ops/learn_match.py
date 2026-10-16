"""Topic-matched Learn references for child pages (Divit 2026-10-16, B-dev-19).

  hubctl learn-match URL [URL ...] [--write]     the 3 picks for each page, with scores and why (--write: spec.learn_refs and
                                                 spec.learn_refs_why; refused on live pages, which change only through an approved update)
  hubctl learn-match --all [--live] --report [--out DIR]   every page of the keyword map (--live: status/live.json live:true only);
                                                 --out writes DIR/plan.md and DIR/plan.json (URL -> 3 IDs); nothing in Webflow changes

Eligible articles: published in .cache/learn/inventory.json (isDraft false, not archived, lastPublished set) and HTTP 200 at
https://emergent.sh/learn/<slug> in .cache/learn/http_status.json (when that file exists), never the old default trio.
Score: token overlap (light stemming, per-hub synonyms, IDF over the Learn titles) between the article's slug and title and the page's
hub, primary, secondaries (hubctl.kmap()) and H1; how-to and builder-intent articles get a bonus; competitor-only articles (review,
pricing, alternatives, vendor-vs-vendor) and model news get a penalty unless the page names that vendor. The top 3 above THRESHOLD
win; empty slots fill from the hub's fixed relevant set in config/learn_sets.json, in order.
"""
import json, math, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(ROOT, ".cache", "learn", "inventory.json")
HTTP = os.path.join(ROOT, ".cache", "learn", "http_status.json")
SETS = os.path.join(ROOT, "config", "learn_sets.json")
THRESHOLD = 3.0          # sum of matched topic weights after intent adjustments
MIN_TOPIC_IDF = 2.5      # at least one matched topic token must be this rare across Learn titles
N = 3

STOP = set("""a an and the or of for to in on at by with from into your you my our i it its is are be what how why when which who that this
these those best top vs versus 2025 2026 step steps guide tested test tests tried real one per without do does can worth should every use used
using actually need minute minutes honest pick picks ranked compared review reviews explained simple easy fast faster quick full ultimate
complete list examples example type types way ways thing things more most new get make makes made create build built builder builders
tool tools software platform platforms app apps web website websites site ai free online no code generator template templates page pages
here what s t vs""".split())
# kept as weak (generic) matches: they say "builder intent" but carry no topic
GENERIC = {"build", "builder", "app", "website", "tool", "software", "platform", "ai", "free", "online", "code", "page", "template", "generat", "create", "make"}

IRREG = {"automation": "automat", "automate": "automat", "automated": "automat", "automating": "automat", "automations": "automat",
         "registration": "regist", "register": "regist", "registrations": "regist", "scheduling": "schedul", "schedule": "schedul",
         "scheduler": "schedul", "booking": "booking", "bookings": "booking", "booked": "booking", "surveys": "survey", "quizzes": "quiz",
         "questionnaires": "questionnair", "questionnaire": "questionnair", "businesses": "business", "analytics": "analyt", "analysis": "analyt",
         "reporting": "report", "reports": "report", "onboarding": "onboard", "ecommerce": "ecommerce", "e-commerce": "ecommerce",
         "invoices": "invoic", "invoice": "invoic", "invoicing": "invoic", "realtor": "realtor", "realtors": "realtor", "nonprofit": "nonprofit",
         "non": "non", "profit": "profit", "leads": "lead", "lead": "lead", "dashboards": "dashboard", "medical": "medic", "medicine": "medic",
         "patients": "patient", "customer": "customer", "customers": "customer", "employees": "employe", "employee": "employe", "employment": "employ", "hiring": "hire", "hr": "hr"}

def stem(w):
    w = w.lower()
    if w in IRREG: return IRREG[w]
    if len(w) > 4 and w.endswith("ies"): w = w[:-3] + "y"
    elif len(w) > 3 and w.endswith("s") and not w.endswith("ss"): w = w[:-1]
    for suf in ("ation", "ing", "ed", "er"):
        if len(w) > len(suf) + 3 and w.endswith(suf): w = w[: -len(suf)]; break
    if len(w) > 4 and w.endswith("e"): w = w[:-1]
    return w

def toks(text):
    out = []
    for w in re.findall(r"[a-z0-9]+", (text or "").lower().replace("e-commerce", "ecommerce").replace("non-profit", "nonprofit")):
        if w in STOP and stem(w) not in GENERIC: continue
        if w.isdigit() or len(w) < 2: continue
        out.append(stem(w))
    return out

# per-hub synonyms: page word (stemmed on load) -> article words it should also match
HUB_TERMS = {"LP": "landing lead funnel", "Form": "form intake submission", "Auto": "automat workflow", "SurveyQuiz": "survey quiz feedback"}
SYN = {
    "_all": {"lead": "lead crm sales", "crm": "crm lead sales", "sale": "sales crm lead", "ecommerce": "ecommerce store shop", "shop": "ecommerce store",
             "store": "ecommerce store", "restaurant": "restaurant", "real": "real estate realtor", "estate": "estate realtor",
             "realtor": "realtor estate", "property": "estate rental realtor", "rental": "rental estate", "tenant": "rental estate", "landlord": "rental estate",
             "event": "event", "webinar": "event", "conference": "event", "nonprofit": "nonprofit donation", "donation": "donation nonprofit",
             "charity": "nonprofit donation", "church": "church", "school": "school teacher", "student": "school teacher course", "teacher": "teacher school",
             "course": "course", "class": "course school", "membership": "membership", "member": "membership", "health": "healthcare medic",
             "healthcare": "healthcare medic", "patient": "healthcare medic", "medic": "healthcare medic", "clinic": "healthcare medic",
             "dental": "healthcare medic", "therapy": "therapist healthcare", "therapist": "therapist", "photography": "photography photograph",
             "photographer": "photograph photography", "wedding": "wedding", "portfolio": "portfolio", "coach": "coach coaching", "agency": "agency",
             "freelanc": "freelanc", "consult": "consult", "lawyer": "lawyer law", "legal": "law lawyer", "law": "law lawyer", "attorney": "law lawyer",
             "contractor": "contractor construction", "construction": "construction contractor", "clean": "clean", "hotel": "hotel",
             "saas": "saas", "startup": "startup mvp", "mvp": "mvp", "launch": "launch", "app": "app", "mobile": "mobile", "subscription": "subscription",
             "booking": "booking schedul appointment", "appointment": "booking schedul appointment",
             "reservation": "booking", "schedul": "schedul booking", "dashboard": "dashboard kpi", "kpi": "kpi dashboard",
             "analyt": "analyt dashboard", "budget": "budget financial", "financ": "financial budget", "accounting": "accountant financial",
             "accountant": "accountant", "invoic": "accountant financial", "expens": "budget financial", "payroll": "accountant financial",
             "portal": "portal", "client": "client onboard portal", "customer": "customer", "onboard": "onboard",
             "agent": "agent", "chatbot": "chatbot", "support": "chatbot customer", "ticket": "chatbot", "helpdesk": "chatbot",
             "marketplace": "marketplace", "directory": "directory", "seo": "seo", "marketing": "marketing", "project": "project",
             "task": "task project", "insurance": "insurance", "hair": "hair", "salon": "hair", "beauty": "hair", "spa": "massage", "massage": "massage",
             "fitness": "fitness", "gym": "fitness"},
    "LP": {"landing": "landing", "book": "author ebook", "ebook": "ebook author", "waitlist": "launch mvp", "prelaunch": "launch", "pre": "launch", "coming": "launch", "lead": "lead",
           "magnet": "lead", "squeeze": "lead", "opt": "lead", "funnel": "funnel lead", "product": "launch product", "one": "one", "click": "funnel",
           "thank": "funnel", "conversion": "lead convert"},
    "Form": {"form": "form", "intake": "intake onboard client", "inquiry": "lead",
             "signup": "regist", "sign": "regist", "regist": "regist event", "rsvp": "event wedding", "consent": "healthcare", "waiver": "waiver",
             "payment": "ecommerce stripe", "quote": "quote estimate", "estimate": "estimate quote", "feedback": "feedback survey",
             "job": "hire", "employ": "hire", "hire": "hire", "recruit": "hire", "volunteer": "nonprofit"},
    "Auto": {"workflow": "workflow automat", "automat": "automat workflow", "approval": "workflow", "process": "workflow", "pipeline": "workflow sales",
             "email": "marketing", "social": "marketing social", "content": "marketing", "inventory": "ecommerce store", "fulfillment": "ecommerce",
             "loan": "financial", "audit": "financial", "report": "dashboard report kpi", "compliance": "workflow", "it": "workflow", "document": "workflow", "data": "dashboard analyt",
             "nurtur": "lead crm sales", "follow": "sales crm", "outreach": "sales"},
    "SurveyQuiz": {"survey": "survey feedback", "quiz": "quiz interact", "poll": "survey", "questionnair": "survey", "feedback": "feedback survey",
                   "nps": "customer feedback", "satisfaction": "customer feedback", "market": "validat idea", "research": "validat idea",
                   "personality": "quiz interact", "trivia": "quiz interact", "test": "quiz", "assessment": "quiz", "product": "product validat",
                   "engagement": "employe", "exit": "employe", "pulse": "employe", "training": "course", "result": "dashboard analyt"},
}

# topic vocabulary: only these (stemmed) words count as a match; everything else in a title is noise ("open", "team", "owner")
DOMAIN = """form intake submission survey quiz poll questionnaire feedback landing lead funnel automation workflow hr hire recruit employee
onboarding payroll benefit expense reimbursement leave timesheet attendance insurance claim tax invoice loan mortgage rental lease tenant
landlord property real estate realtor contract agreement waiver consent medical patient healthcare dental clinic therapist therapy pet
child school student teacher course training event wedding rsvp registration volunteer donation church nonprofit restaurant food menu
catering hotel booking appointment reservation scheduling salon hair massage beauty fitness vehicle ecommerce store shop order payment
checkout shipping inventory procurement vendor supplier quote estimate contractor construction cleaning photography photographer portfolio
resume job application sales crm marketing email social media content seo newsletter webinar ebook saas startup mvp product launch waitlist
mobile agency consulting coach coaching lawyer law legal finance financial accounting accountant budget dashboard kpi analytics report data
customer client nps satisfaction personality trivia chatbot agent support ticket helpdesk portal marketplace directory membership subscription
validate idea interactive affiliate b2b podcast author artist musician band dog breeder clothing boutique subscription""".split()

OLD_TRIO = {"6accb850129314c7c749f349", "6accb8444371ac13b53b0c12", "6ac8fd16a1e22e1121c2a3f1"}
MODEL_RX = re.compile(r"(^|-)(gemini|gpt|claude|opus|sonnet|haiku|fable|llama|grok|deepseek|qwen|mistral|kimi|glm|minimax|sakana|fugu|hy[0-9]|jev|"
                      r"openai|chatgpt|perplexity|phind|codex|luna|astra|argon|sol|llm)(-|$)")
COMP_RX = re.compile(r"^(?:best-)?(.+?)-(?:reviews?|pricing|alternatives(?:-and-competitors)?)$")
HOWTO_RX = re.compile(r"^(how-to-(build|create|make|launch|start|vibe|turn)|build-|generate-|idea-to-live|launch-a-)")
TOOLS_FOR_RX = re.compile(r"^(best-)?ai-tools-for-")   # third-party tool roundups for a profession: weaker than a build guide
LISTICLE_BUILDER_RX = re.compile(r"^best-.*(builder|builders|tools?|software)$")

def load_articles():
    inv = json.load(open(INV)); items = inv["items"] if isinstance(inv, dict) else inv
    http = json.load(open(HTTP))["results"] if os.path.exists(HTTP) else None
    arts = []
    for i in items:
        if i.get("isDraft") or i.get("isArchived") or not i.get("lastPublished") or i["id"] in OLD_TRIO: continue
        if http is not None and (http.get(i["id"]) or {}).get("status") != 200: continue
        arts.append({"id": i["id"], "slug": i["slug"], "name": i.get("name") or i["slug"]})
    vendors = set()
    for a in arts:
        m = COMP_RX.match(a["slug"])
        if m and not m.group(1).startswith(("ai-", "how", "what")): vendors.add(m.group(1))
    for a in arts:
        if "-vs-" in a["slug"]:
            sides = a["slug"].split("-vs-")
            if all(s in vendors or MODEL_RX.search(s) or s in ("emergent", "make", "zapier", "n8n", "hubspot", "salesforce", "airtable", "google-sheets", "stripe", "square") for s in sides):
                vendors.update(s for s in sides if not MODEL_RX.search(s))
    df = Counter()
    for a in arts:
        a["toks"] = set(toks(a["slug"].replace("-", " ") + " " + a["name"]))
        df.update(a["toks"])
        s = a["slug"]
        a["model"] = bool(MODEL_RX.search(s))
        m = COMP_RX.match(s)
        a["vendor"] = None
        if m and m.group(1) in vendors: a["vendor"] = [m.group(1)]
        elif "-vs-" in s and any(x in vendors for x in s.split("-vs-")): a["vendor"] = [x for x in s.split("-vs-")]
        a["howto"] = bool(HOWTO_RX.match(s))
        a["listicle"] = bool(LISTICLE_BUILDER_RX.match(s))
    n = len(arts)
    idf = {t: math.log(n / (1 + c)) for t, c in df.items()}
    return arts, idf

# synonym keys that are too ambiguous to count as a match on their own ("job" in "One Per Job", "application" = software)
# broad words: half weight, and never enough on their own to qualify an article
WEAK = {stem(w) for w in "customer client product launch market marketing agent media social store estate team idea mobile".split()}
NOT_TOPIC = "job application one sign pre coming click thank it opt exit test follow process data content email".split()
_VOCAB = set()
def vocab():
    if not _VOCAB:
        words = list(DOMAIN) + " ".join(HUB_TERMS.values()).split()
        for d in SYN.values():
            for a, b in d.items(): words += [a] + b.split()
        _VOCAB.update(stem(w) for w in words)
        _VOCAB.difference_update(stem(w) for w in NOT_TOPIC)
    return _VOCAB

def page_profile(url, k, h1, hub):
    w = Counter()
    def add(text, wt):
        for t in toks(text): w[t] = max(w[t], wt)
    add(k.get("primary"), 1.0); add(h1, 0.7)
    for s in k.get("secondaries") or []: add(s.get("kw") if isinstance(s, dict) else s, 0.5)
    add(url.rsplit("/", 1)[1].replace("-", " "), 0.8)
    add(HUB_TERMS.get(hub, ""), 0.3)
    syn = dict(SYN["_all"]); syn.update({stem(a): b for a, b in SYN.get(hub, {}).items()})
    for t, wt in list(w.items()):
        for s in (syn.get(t) or "").split():
            s = stem(s)
            if w[s] < wt * 0.6: w[s] = wt * 0.6
    raw = " ".join([k.get("primary") or "", h1 or "", url] + [(s.get("kw") if isinstance(s, dict) else s) for s in k.get("secondaries") or []]).lower()
    return w, raw, set(toks(HUB_TERMS.get(hub, "")))

def score(a, prof, idf):
    w, raw, hub_t = prof
    V = vocab()
    topic = [(t, w[t] * idf.get(t, 0) * (0.5 if t in WEAK else 1.0)) for t in a["toks"] if t in w and t in V]
    s = sum(x for _, x in topic)
    # a hub's own words (workflow, form, survey) count only when they are the article's subject (in its slug)
    slug_t = set(toks(a["slug"].replace("-", " ")))
    strong = any(idf.get(t, 0) >= MIN_TOPIC_IDF and t not in WEAK and (t not in hub_t or t in slug_t) for t, _ in topic)
    strong = strong or len({t for t, _ in topic if t in WEAK}) >= 2   # two broad words together ("product" + "launch") are a topic
    notes = []
    if a["howto"]: s += 1.0; notes.append("how-to")
    elif a["listicle"]: s += 0.4; notes.append("builder list")
    if TOOLS_FOR_RX.match(a["slug"]): s -= 1.5; notes.append("tool roundup")
    named = a["vendor"] and any(v.replace("-", " ") in raw or v in raw for v in a["vendor"])
    if a["vendor"] and not named: s -= 10.0; notes.append("competitor-only")
    if a["model"] and not named: s -= 6.0; notes.append("model news")
    matched = [t for t, _ in sorted(topic, key=lambda x: -x[1])]
    notes.append("hub-term only") if matched and set(matched) <= hub_t else None
    return round(s, 2), strong, matched, notes

_CACHE = {}
def ctx():
    if not _CACHE:
        sys.path.insert(0, os.path.join(ROOT, "ops")); import hubctl as H
        arts, idf = load_articles()
        _CACHE.update(H=H, arts=arts, idf=idf, by_id={a["id"]: a for a in arts}, sets=json.load(open(SETS)), kmap=H.kmap())
    return _CACHE

def h1_of(url):
    H = ctx()["H"]
    try: return ((json.load(open(H.spath(url))).get("fields") or {}).get("h1")) or ""
    except (OSError, ValueError, SystemExit): return ""

def match(url):
    c = ctx(); H = c["H"]; hub = H.hub_of(url); k = c["kmap"].get(url) or {"primary": url.rsplit("/", 1)[1].replace("-", " ")}
    h1 = h1_of(url); prof = page_profile(url, k, h1, hub)
    ranked = []
    for a in c["arts"]:
        s, strong, matched, notes = score(a, prof, c["idf"])
        if s >= THRESHOLD and strong: ranked.append((s, a, matched, notes))
    ranked.sort(key=lambda x: (-x[0], x[1]["slug"]))
    # at most one article that matches only on the hub's own word (landing, workflow, survey): the rest of the slots go to
    # topic matches or the hub's fixed set, so three near-identical "best X builders" lists never fill a page
    # and one article per identical set of matched words (three "analytics dashboard" explainers say the same thing to this reader)
    chosen, hub_only, seen = [], 0, set()
    for r in ranked:
        if len(chosen) >= N: break
        key = frozenset(r[2])
        if key in seen: continue
        if "hub-term only" in r[3]:
            if hub_only: continue
            hub_only += 1
        seen.add(key); chosen.append(r)
    picks = [{"id": a["id"], "slug": a["slug"], "score": s, "source": "scored",
              "why": f"score {s}: matches " + ", ".join(m[:4]) + (f" ({', '.join(n)})" if n else "")} for s, a, m, n in chosen]
    fixed = c["sets"]["hubs"][hub]["items"]
    for f in fixed:
        if len(picks) >= N: break
        if f["id"] in {p["id"] for p in picks}: continue
        if f["id"] not in c["by_id"]: continue   # not eligible any more (unpublished or not 200): skip, the set needs a refresh
        picks.append({"id": f["id"], "slug": f["slug"], "score": None, "source": "fallback", "why": f"{hub} fixed set: {f['reason']}"})
    return {"url": url, "hub": hub, "primary": k.get("primary"), "primary_msv": k.get("primary_msv"), "h1": h1, "picks": picks,
            "fallback": sum(p["source"] == "fallback" for p in picks), "candidates": len(ranked)}

def live_urls():
    d = json.load(open(os.path.join(ROOT, "status", "live.json")))["pages"]
    return sorted(u for u, v in d.items() if v.get("live"))

def write_spec(url, r):
    c = ctx(); H = c["H"]
    if url in set(live_urls()): sys.exit(f"refused: {url} is live; live items change only through an approved update payload (no --write on live pages)")
    if len(r["picks"]) != N: sys.exit(f"refused: {url}: only {len(r['picks'])} pick(s)")
    p = H.spath(url); s = json.load(open(p))
    s["learn_refs"] = [x["id"] for x in r["picks"]]
    s["learn_refs_why"] = [f"{x['slug']}: {x['why']}" for x in r["picks"]]
    pr = H.learn_spec_problems(s)
    if pr: sys.exit(f"refused: {url}: " + "; ".join(pr))
    json.dump(s, open(p, "w"), indent=1, ensure_ascii=False)
    print(f"wrote spec.learn_refs for {url}")

def show(r):
    print(f"{r['url']}  ({r['hub']}; primary '{r['primary']}'; {r['candidates']} above threshold; fallback {r['fallback']})")
    for x in r["picks"]: print(f"  {x['id']} {x['slug']:<52} {x['why']}")

def report(rows, out=None):
    c = ctx(); sets = c["sets"]["hubs"]
    use = Counter(x["slug"] for r in rows for x in r["picks"])
    slots = sum(len(r["picks"]) for r in rows); fb = sum(r["fallback"] for r in rows)
    full = sum(r["fallback"] == 0 for r in rows); allfb = sum(r["fallback"] == N for r in rows)
    lines = ["# Learn references: topic-matched plan", "",
             f"{len(rows)} pages; {len(c['arts'])} eligible Learn articles (published, HTTP 200, old trio excluded). Nothing written to Webflow.", "",
             "## Totals", "", f"- Slots: {slots}; scored {slots - fb}, fallback {fb}",
             f"- Pages fully scored (3 of 3): {full}; partly fallback: {len(rows) - full - allfb}; all fallback: {allfb}", "",
             "## Fixed relevant set per hub (fallback)", ""]
    for hub, h in sets.items():
        lines.append(f"### {hub}")
        for f in h["items"]: lines.append(f"- `{f['slug']}` ({f['id']}): {f['reason']}")
        lines.append("")
    by_hub = {}
    for r in rows: by_hub.setdefault(r["hub"], []).append(r)
    samples = []
    for hub in sets:
        rs = sorted(by_hub.get(hub, []), key=lambda r: r["url"])
        if not rs: continue
        picks = [x for x in rs if x["fallback"] == 0][:1] + [x for x in rs if 0 < x["fallback"] < N][:1] + [x for x in rs if x["fallback"] == N][:1]
        samples += picks
    for r in rows:
        if len(samples) >= 10: break
        if r not in samples: samples.append(r)
    lines += ["## Sample pages", ""]
    for r in samples[:10]:
        lines.append(f"**{r['url']}** (primary: {r['primary']}; fallback slots: {r['fallback']})")
        for x in r["picks"]:
            lines.append(f"- `{x['slug']}`: " + (f"score {x['score']}, " if x["score"] is not None else "fallback, ") + x["why"].split(": ", 1)[-1])
        lines.append("")
    lines += ["## How often each article is picked", "", "| Article | Pages |", "|---|---|"]
    lines += [f"| `{s}` | {n} |" for s, n in use.most_common()]
    lines += ["", "## Per hub", "", "| Hub | Pages | Fully scored | Partly fallback | All fallback |", "|---|---|---|---|---|"]
    for hub in sets:
        rs = by_hub.get(hub, [])
        lines.append(f"| {hub} | {len(rs)} | {sum(r['fallback'] == 0 for r in rs)} | {sum(0 < r['fallback'] < N for r in rs)} | {sum(r['fallback'] == N for r in rs)} |")
    md = "\n".join(lines) + "\n"
    if out:
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "plan.md"), "w").write(md)
        json.dump({"_note": "URL -> 3 Learn item IDs (acrm---learn), topic-matched (ops/learn_match.py). Proposal only: not written to Webflow or specs.",
                   "pages": {r["url"]: [x["id"] for x in r["picks"]] for r in rows},
                   "detail": {r["url"]: r["picks"] for r in rows}}, open(os.path.join(out, "plan.json"), "w"), indent=1)
        print(f"wrote {os.path.join(out, 'plan.md')} and plan.json")
    print(md if not out else "\n".join(lines[:9]))

def main(args):
    write = "--write" in args; out = None
    if "--out" in args: out = args[args.index("--out") + 1]
    urls = [a for a in args if a.startswith("/")]
    if "--all" in args:
        if write: sys.exit("refused: --write with --all (write page by page, never on live pages)")
        urls = live_urls() if "--live" in args else sorted(ctx()["kmap"])
        rows = [match(u) for u in urls]
        if "--report" in args: report(rows, out)
        else:
            for r in rows: show(r)
        return 0
    if not urls: print(__doc__); return 2
    for u in urls:
        r = match(u); show(r)
        if write: write_spec(u, r)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
