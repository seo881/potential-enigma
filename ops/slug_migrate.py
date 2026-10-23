#!/usr/bin/env python3
"""Slug migration, steps 1 and 2 (DECISIONS 2026-10-23 SLUG MIGRATION). READ ONLY: no Webflow writes, ever, from this script.

A child slug is ONLY the page's own name: the hub's category word never appears in it, at the end or in the middle.

  slug_migrate.py inventory [--readback-dir .cache/readback]
      newest full `hubctl api-read <HUB>` per hub (run those first) + specs/, status/<dir>.json, plan/queue-ranked.txt,
      plan/keyword_map.json, plan/additions.json -> private/migration/inventory.json (git-ignored) and a count summary.
  slug_migrate.py map [--no-fetch]
      strips the category word (hyphen-bounded, anywhere) and checks every new slug -> plan/slug-migration.json
      (Webflow items + pages named in tracked repo files). Pages known only from the keyword map (git-ignored) go to
      private/migration/slug-migration-kmap.json. The sitemap is cached in .cache/migration/.
  slug_migrate.py links
      counts hard-coded internal links to child pages in specs/ (non-archived) and in the newest CMS read.
"""
import glob, json, os, re, sys, urllib.request
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config/collections.json")))
PRIV = os.path.join(ROOT, "private/migration")
CACHE = os.path.join(ROOT, ".cache/migration")
OUT = os.path.join(ROOT, "plan/slug-migration.json")

# Category words per hub, as hyphen-token sequences, longest first. "strip" = the rule; "variant" = similar words that
# are flagged for Divit, never stripped automatically.
CATEGORY = {
    "LP":         {"strip": [["landing", "pages"], ["landing", "page"]], "variant": [["page"], ["pages"]]},
    "Form":       {"strip": [["forms"], ["form"]], "variant": []},
    "Auto":       {"strip": [["automations"], ["automation"]], "variant": [["automated"], ["workflow"], ["workflows"]]},
    "SurveyQuiz": {"strip": [["survey", "questions"], ["surveys"], ["survey"], ["quizzes"], ["quiz"]],
                   "variant": [["questionnaire"], ["questions"], ["poll"], ["polls"]]},
}
RESERVED = {"index", "page", "new", "edit", "admin", "login", "logout", "signin", "signup", "search", "404", "draft", "preview",
            "home", "sitemap", "robots", "feed", "rss"}
# bare results that read as site UI, a pronoun, a number or a different thing (Divit's examples first)
# Single function or industry words (feedback, payment, sales, video) are NOT flagged: the hub path carries the meaning,
# as on /ai-website-builder/video or /ai-website-builder/instant.
AMBIGUOUS = {"contact", "order", "sign-up", "approval", "it", "360", "sign-in", "sign-out", "checkout", "pricing", "interest",
             "style", "team", "funny", "category", "funnel", "matching"}
# short tokens that are clear acronyms in context (not "too short")
ACRONYMS = {"crm", "seo", "nda", "rfp", "nps", "pdf", "ppc", "b2b", "nft", "dei", "ach", "app", "hvac", "saas", "cpa", "pt", "qr", "it", "hr", "sms", "rfq", "dj", "spa", "pet", "api", "seo"}
DANGLING = {"ai", "free", "online", "best", "simple", "easy", "custom", "builder", "maker", "template", "templates", "generator",
            "creator", "example", "examples", "for", "to", "and", "or", "of", "with", "the", "a", "in", "on", "by", "questions"}


def hubs():
    return {h: v for h, v in CFG["hubs"].items()}


def newest_readback(d, rbdir):
    fs = sorted(glob.glob(os.path.join(rbdir, f"{d}-api-*.json")))
    return fs[-1] if fs else None


def strip(hub, slug):
    """(new_slug, removed_spans[(pos, word)]) removing every hyphen-bounded category sequence."""
    toks, out, removed, i = slug.split("-"), [], [], 0
    seqs = CATEGORY[hub]["strip"]
    while i < len(toks):
        for s in seqs:
            if toks[i:i + len(s)] == s:
                removed.append((i, "-".join(s), "end" if i + len(s) == len(toks) else ("start" if i == 0 else "middle")))
                i += len(s); break
        else:
            out.append(toks[i]); i += 1
    return "-".join(out), removed


def variants(hub, slug):
    toks = slug.split("-")
    return sorted({"-".join(v) for v in CATEGORY[hub]["variant"] for i in range(len(toks)) if toks[i:i + len(v)] == v})


# ---------------------------------------------------------------- inventory
def cmd_inventory(args):
    rbdir = os.path.join(ROOT, args[args.index("--readback-dir") + 1]) if "--readback-dir" in args else os.path.join(ROOT, ".cache/readback")
    km = json.load(open(os.path.join(ROOT, "plan/keyword_map.json"))) if os.path.exists(os.path.join(ROOT, "plan/keyword_map.json")) else {}
    ad = json.load(open(os.path.join(ROOT, "plan/additions.json"))).get("pages", {})
    queue = {}
    for line in open(os.path.join(ROOT, "plan/queue-ranked.txt")):
        if line.startswith("#") or not line.strip(): continue
        p = line.rstrip("\n").split("\t")
        if len(p) >= 3: queue[p[2]] = {"rank": int(p[0]), "class": p[3] if len(p) > 3 else None}
    inv = {"_note": "Slug migration inventory (DECISIONS 2026-10-23). Webflow = live state from hubctl api-read; repo = cross-reference.",
           "hubs": {}}
    summary = {}
    for hub, h in hubs().items():
        d, path = h["repo_dir"], h["path"]
        rb = newest_readback(d, rbdir)
        if not rb: sys.exit(f"{hub}: no api-read on disk; run hubctl api-read {hub}")
        R = json.load(open(rb))
        items = R["result"]["items"]
        status = json.load(open(os.path.join(ROOT, f"status/{d}.json"))).get("pages", {})
        specs = {}
        for f in glob.glob(os.path.join(ROOT, f"specs/{d}/*.json")):
            try: s = json.load(open(f))
            except Exception: continue
            u = s.get("url") or f"{path}/{os.path.basename(f)[:-5]}"
            specs[u] = {"file": os.path.relpath(f, ROOT), "item_id": s.get("item_id"), "status": s.get("status")}
        by_id = {}
        rows = []
        for it in items:
            fd = it.get("fieldData", {})
            slug = fd.get("slug"); url = f"{path}/{slug}"
            live = (not it.get("isDraft")) and (not it.get("isArchived")) and bool(it.get("lastPublished"))
            st = status.get(url, {})
            row = {"item_id": it["id"], "slug": slug, "url": url, "name": fd.get("name"), "isDraft": it.get("isDraft"),
                   "isArchived": it.get("isArchived"), "lastPublished": it.get("lastPublished"), "lastUpdated": it.get("lastUpdated"),
                   "webflow_state": "archived" if it.get("isArchived") else ("draft" if it.get("isDraft") else ("published" if it.get("lastPublished") else "staged")),
                   "live": live, "in_webflow": True,
                   "spec": specs.get(url, {}).get("file"), "status_state": st.get("state"), "status_item_id": st.get("cms_item_id"),
                   "queue_rank": queue.get(url, {}).get("rank"), "in_keyword_map": url in km, "in_additions": url in ad}
            if st.get("cms_item_id") and st["cms_item_id"] != it["id"]: row["mismatch"] = "status cms_item_id differs"
            by_id[it["id"]] = row; rows.append(row)
        webflow_urls = {r["url"] for r in rows}
        repo_urls = set(status) | set(specs) | {u for u in queue if u.startswith(path + "/")} | \
                    {u for u in km if u.startswith(path + "/")} | {u for u in ad if u.startswith(path + "/")}
        repo_urls = {u for u in repo_urls if u.startswith(path + "/")}
        planned = []
        for u in sorted(repo_urls - webflow_urls):
            st = status.get(u, {})
            planned.append({"item_id": None, "slug": u[len(path) + 1:], "url": u, "in_webflow": False,
                            "spec": specs.get(u, {}).get("file"), "status_state": st.get("state"), "status_item_id": st.get("cms_item_id"),
                            "queue_rank": queue.get(u, {}).get("rank"), "in_keyword_map": u in km, "in_additions": u in ad,
                            "public_source": bool(u in status or u in specs or u in queue or u in ad)})
        # status says in CMS but the item is not in the read
        ghosts = [u for u, v in status.items() if v.get("cms_item_id") and v["cms_item_id"] not in by_id]
        inv["hubs"][hub] = {"collection_id": h["collection_id"], "path": path, "readback": os.path.relpath(rb, ROOT),
                            "read_at": R.get("_meta", {}).get("read_at"), "webflow": rows, "planned": planned,
                            "status_ghosts": ghosts}
        summary[hub] = {"webflow_items": len(rows), **Counter(r["webflow_state"] for r in rows),
                        "live": sum(r["live"] for r in rows),
                        "planned_not_in_webflow": len(planned),
                        "planned_by_status": dict(Counter(p["status_state"] or "no-status" for p in planned)),
                        "planned_keyword_map_only": sum(not p["public_source"] for p in planned),
                        "status_ghosts": len(ghosts),
                        "id_mismatches": sum(1 for r in rows if r.get("mismatch"))}
    inv["summary"] = summary
    os.makedirs(PRIV, exist_ok=True)
    json.dump(inv, open(os.path.join(PRIV, "inventory.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))
    print("->", os.path.relpath(os.path.join(PRIV, "inventory.json"), ROOT))


# ---------------------------------------------------------------- sitemap
def sitemap_urls(fetch=True):
    os.makedirs(CACHE, exist_ok=True)
    cp = os.path.join(CACHE, "sitemap-urls.txt")
    if fetch or not os.path.exists(cp):
        def get(u):
            return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "emergent-hubs-slug-migrate"}), timeout=60).read().decode("utf-8", "replace")
        top = get("https://emergent.sh/sitemap.xml")
        locs = re.findall(r"<loc>([^<]+)</loc>", top)
        urls = []
        if "<sitemapindex" in top:
            for sm in locs: urls += re.findall(r"<loc>([^<]+)</loc>", get(sm))
        else: urls = locs
        paths = sorted({re.sub(r"^https?://(www\.)?emergent\.sh", "", u).rstrip("/") or "/" for u in urls})
        open(cp, "w").write("\n".join(paths) + "\n")
    return [l.strip() for l in open(cp) if l.strip()]


# ---------------------------------------------------------------- map
def judge(hub, old, new, removed):
    """flags for one mapping (before collection-level checks)."""
    f = []
    toks = new.split("-") if new else []
    if not new: f.append("empty")
    if any(r[2] == "middle" for r in removed): f.append("mid_slug")
    if any(r[2] == "start" for r in removed): f.append("start_slug")
    if new and (new.isdigit() or (len(new) <= 3 and new not in ACRONYMS)): f.append("too_short")
    if removed and toks and toks[-1] in {"maker", "builder", "generator", "creator", "template", "templates"}:
        f.append("dangling"); toks = toks[:-1]
    if new in AMBIGUOUS: f.append("ambiguous")
    if removed and new and (all(t in DANGLING for t in toks) or toks[0] in {"and", "or", "to", "for", "of", "with"} or toks[-1] in {"and", "or", "to", "for", "of", "with", "the", "a"}):
        f.append("dangling")
    if new in RESERVED: f.append("reserved")
    v = variants(hub, new if new else old)
    if v: f.append("variant:" + ",".join(v))
    return f


def recommend(hub, old, new, flags):
    """(recommended slug, note). Default: the stripped slug."""
    rec, note = new, ""
    if hub == "LP" and not new == old: pass
    if hub == "LP" and any(x.startswith("variant:page") for x in flags) and new == old:
        note = "'-page' type, not 'landing-page': keep (a thank-you or pricing page is its own page type)"
    if hub == "Auto" and any("workflow" in x for x in flags):
        note = "keep 'workflow': not the category word; stripping it would leave generic stems (approval, content, sales, audit, legal)"
    if hub == "Auto" and any("automated" in x for x in flags):
        rec = re.sub(r"(^|-)automated(-|$)", r"\1", new).strip("-")
        rec = re.sub(r"-system$", "", rec)
        note = "'automated' is the category word in adjective form: strip it"
    if hub == "SurveyQuiz" and any("questionnaire" in x for x in flags):
        rec = re.sub(r"-?questionnaire", "", new).strip("-") or new
        note = "'questionnaire' is a survey synonym: strip it"
    if hub == "SurveyQuiz" and old.endswith("survey-questions"):
        rec = old.replace("survey-questions", "questions").strip("-")
        note = "stripping 'survey-questions' leaves a bare adjective: keep 'questions'"
    special = {("SurveyQuiz", "it-survey"): ("it-support", "'it' reads as a pronoun; the page covers help desk, devices, software"),
               ("Auto", "it-automation"): ("it-operations", "'it' reads as a pronoun"),
               ("SurveyQuiz", "360-survey"): ("360-feedback", "a bare number; 360 feedback is the standard name"),
               ("Form", "sign-in-form"): ("visitor-sign-in", "bare 'sign-in' reads as the site's login; the page tracks who comes and goes"),
               ("Form", "sign-out-form"): ("staff-sign-out", "bare 'sign-out' reads as logout; the page shows who is away"),
               ("Form", "checkout-form"): ("equipment-checkout", "bare 'checkout' reads as a cart checkout; the page tracks who has each item"),
               ("Form", "interest-form"): ("interest-list", "bare 'interest' reads as financial interest"),
               ("Form", "approval-form"): ("approval-request", "bare 'approval' is too generic (Divit's example)"),
               ("Form", "sign-up-form"): ("sign-up", "reads as the site's sign-up, but the hub path disambiguates; accept"),
               ("Form", "contact-form"): ("contact", "the head term; the hub path disambiguates; accept"),
               ("Form", "order-form"): ("order", "the head term; every variant keeps its qualifier (cake-order, purchase-order); accept"),
               ("SurveyQuiz", "pricing-survey"): ("price-testing", "bare 'pricing' shadows the top-level /pricing page"),
               ("SurveyQuiz", "style-quiz"): ("personal-style", "bare 'style' is ambiguous"),
               ("SurveyQuiz", "team-survey"): ("team", "live survey keeps the bare stem; the planned team-quiz takes team-trivia"),
               ("SurveyQuiz", "team-quiz"): ("team-trivia", "collides with team-survey -> team"),
               ("SurveyQuiz", "safety-survey"): ("safety", "live survey keeps the bare stem; the planned safety-quiz takes safety-knowledge-check"),
               ("SurveyQuiz", "safety-quiz"): ("safety-knowledge-check", "collides with safety-survey -> safety"),
               ("SurveyQuiz", "wellness-survey"): ("wellness", "live survey keeps the bare stem; the planned wellness-quiz takes wellness-check"),
               ("SurveyQuiz", "wellness-quiz"): ("wellness-check", "collides with wellness-survey -> wellness"),
               ("SurveyQuiz", "quiz-funnel"): ("funnel", "the category word is the concept; the hub path says quiz; accept"),
               ("SurveyQuiz", "matching-quiz-maker"): ("matching", "'-maker' dangles once 'quiz' goes; drop it"),
               ("SurveyQuiz", "survey-questionnaire"): ("(park)", "nothing left but a synonym of the hub's own head term: park, the hub page owns it"),
               ("SurveyQuiz", "likert-questionnaire"): ("likert-scale", "'questionnaire' is a survey synonym; likert-scale is the page's own name"),
               ("LP", "category-landing-page"): ("product-category", "bare 'category' reads as an archive page; the page is a shop category"),
               ("LP", "landing-page-seo"): ("seo", "category word was at the start; the page is landing page SEO; accept")}
    if (hub, old) in special: rec, n = special[(hub, old)]; note = n or note
    return rec, note


def cmd_map(args):
    inv_p = os.path.join(PRIV, "inventory.json")
    if not os.path.exists(inv_p): sys.exit("run: slug_migrate.py inventory (after hubctl api-read for each hub)")
    inv = json.load(open(inv_p))
    smap = sitemap_urls(fetch="--no-fetch" not in args)
    top = {p.strip("/") for p in smap if p.count("/") == 1 and p != "/"}
    smset = set(smap)
    hub_paths = {h["path"].strip("/") for h in hubs().values()}
    public, private, totals = [], [], {}
    for hub, H in inv["hubs"].items():
        path = H["path"]
        rows = [dict(r, origin="webflow") for r in H["webflow"]] + [dict(r, origin="planned") for r in H["planned"]]
        current = Counter(r["slug"] for r in rows)
        ents = []
        for r in rows:
            new, removed = strip(hub, r["slug"])
            flags = judge(hub, r["slug"], new, removed)
            ents.append({"hub": hub, "item_id": r.get("item_id"), "origin": r["origin"],
                         "webflow_state": r.get("webflow_state"), "repo_state": r.get("status_state"),
                         "old_slug": r["slug"], "new_slug": new, "removed": [x[1] + "@" + x[2] for x in removed],
                         "flags": flags, "_public": r["origin"] == "webflow" or r.get("public_source", True)})
        # collection-level checks
        news = Counter(e["new_slug"] for e in ents)
        olds = {e["old_slug"]: e for e in ents}
        stems = defaultdict(list)
        for e in ents: stems[e["new_slug"]].append(e["old_slug"])
        for e in ents:
            n, o = e["new_slug"], e["old_slug"]
            if n != o:
                if news[n] > 1:
                    others = [x for x in stems[n] if x != o]
                    kinds = {("quiz" if "quiz" in x.split("-") else "survey" if "survey" in x.split("-") else "other") for x in stems[n]}
                    e["flags"].append(("survey_quiz_collision:" if hub == "SurveyQuiz" and {"quiz", "survey"} <= kinds else "duplicate_new:") + ",".join(others))
                if n in current and n in olds and olds[n]["new_slug"] == n:
                    e["flags"].append("clashes_current:" + n)
                url = f"{path}/{n}"
                if url in smset and url != f"{path}/{o}": e["flags"].append("clashes_sitemap:" + url)
            if n in top or n.rstrip("s") in top or (n + "s") in top: e["flags"].append("toplevel_name:/" + next(t for t in (n, n.rstrip("s"), n + "s") if t in top))
            if n in hub_paths or n == path.strip("/"): e["flags"].append("hub_path")
            rec, note = recommend(hub, o, n, e["flags"])
            e["recommended"], e["note"] = rec, note
            blocking = [f for f in e["flags"] if f.split(":")[0] in {"empty", "too_short", "ambiguous", "dangling", "reserved", "duplicate_new",
                                                                     "survey_quiz_collision", "clashes_current", "clashes_sitemap", "hub_path", "start_slug"}]
            var = {v for f in e["flags"] if f.startswith("variant:") for v in f[8:].split(",")}
            hard_var = var & {"automated", "questionnaire"}          # category word in another form: Divit decides per page
            class_var = var & {"page", "pages", "workflow", "workflows"}   # one class ruling (LP -page types, Auto -workflow)
            if blocking or hard_var or rec != n: e["decision"] = "needs_call"
            elif class_var: e["decision"] = "class_call"; e["class"] = "LP -page types" if hub == "LP" else "Auto -workflow"
            elif n == o: e["decision"] = "unchanged"
            else: e["decision"] = "auto"
        for e in ents:
            pub = e.pop("_public")
            (public if pub else private).append(e)
        t = Counter((e["origin"], e["decision"]) for e in ents)
        totals[hub] = {o: {d: t[(o, d)] for d in ("unchanged", "auto", "class_call", "needs_call")} for o in ("webflow", "planned")}
    pub_totals = defaultdict(Counter)
    for e in public: pub_totals[e["hub"]][(e["origin"] + "_" + e["decision"])] += 1
    doc = {"_note": "Slug migration map (DECISIONS 2026-10-23 SLUG MIGRATION). Generated by ops/slug_migrate.py map; read only toward Webflow. "
                    "decision: unchanged (no category word), auto (stripped, all checks pass), class_call (one ruling covers the class; recommended shown), needs_call (Divit decides; see recommended/note). "
                    "Pages known only from the git-ignored keyword map are in private/migration/slug-migration-kmap.json.",
           "rule": {h: {"strip": ["-".join(s) for s in v["strip"]], "flag_only": ["-".join(s) for s in v["variant"]]} for h, v in CATEGORY.items()},
           "sitemap_paths_checked": len(smap),
           "totals": {h: dict(c) for h, c in pub_totals.items()},
           "pages": sorted(public, key=lambda e: (e["hub"], e["origin"] != "webflow", e["old_slug"]))}
    json.dump(doc, open(OUT, "w"), indent=1)
    os.makedirs(PRIV, exist_ok=True)
    json.dump({"pages": private, "totals_all": totals}, open(os.path.join(PRIV, "slug-migration-kmap.json"), "w"), indent=1)
    print(json.dumps(totals, indent=1))
    print("needs_call (public map):", sum(e["decision"] == "needs_call" for e in public), "->", os.path.relpath(OUT, ROOT))


# ---------------------------------------------------------------- links
LINK = re.compile(r"(?:https?://(?:www\.)?emergent\.sh)?(/ai-(?:landing-page|form|automation|survey-and-quiz)-builder/[a-z0-9-]+)")


def _walk(o, path=()):
    if isinstance(o, dict):
        for k, v in o.items(): yield from _walk(v, path + (k,))
    elif isinstance(o, list):
        for v in o: yield from _walk(v, path)
    elif isinstance(o, str):
        yield ".".join(path), o


def cmd_links(args):
    by_field, by_hub, files, targets = Counter(), Counter(), set(), Counter()
    for f in sorted(glob.glob(os.path.join(ROOT, "specs/*/*.json"))):
        s = json.load(open(f))
        for key, txt in _walk(s):
            if key == "url": continue
            for m in LINK.finditer(txt):
                by_field[key] += 1; by_hub[f.split(os.sep)[-2]] += 1; files.add(f); targets[m.group(1)] += 1
    print("specs (non-archived): %d links in %d files, %d distinct targets" % (sum(by_field.values()), len(files), len(targets)))
    for k, v in by_field.most_common(): print(f"  {v:5d}  {k}")
    print("  by hub dir:", dict(by_hub))
    rbdir = os.path.join(ROOT, ".cache/readback")
    tot = 0
    for hub, h in hubs().items():
        rb = newest_readback(h["repo_dir"], rbdir)
        if not rb: continue
        c, items_with = Counter(), 0
        for it in json.load(open(rb))["result"]["items"]:
            n0 = sum(c.values())
            for k, v in it["fieldData"].items():
                if isinstance(v, str): c[k] += len(LINK.findall(v))
            items_with += sum(c.values()) > n0
        tot += sum(c.values())
        print(f"CMS {hub}: {sum(c.values())} links in {items_with} items; fields: {dict((k, v) for k, v in c.items() if v)}")
    print("CMS total:", tot)


if __name__ == "__main__":
    cmds = {"inventory": cmd_inventory, "map": cmd_map, "links": cmd_links}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds: sys.exit(__doc__)
    cmds[sys.argv[1]](sys.argv[2:])
