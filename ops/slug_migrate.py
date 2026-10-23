#!/usr/bin/env python3
"""Slug migration, steps 1 and 2 (DECISIONS 2026-10-23 SLUG MIGRATION). READ ONLY: no Webflow writes, ever, from this script.

A child slug is ONLY the page's own name: the hub's category word never appears in it, at the end or in the middle.

  slug_migrate.py inventory [--readback-dir .cache/readback]
      newest full `hubctl api-read <HUB>` per hub (run those first) + specs/, status/<dir>.json, plan/queue-ranked.txt,
      plan/keyword_map.json, plan/additions.json -> private/migration/inventory.json (git-ignored) and a count summary.
  slug_migrate.py map
      slug = the primary keyword as it appears in the page's H1 (skeleton.h1_phrase_for, found in spec fields.h1 or the CMS name;
      the primary itself when there is no H1 yet, source marked), ONLY the category word removed, lowercased, hyphenated.
      Flags: collision (a new slug used twice in a collection), h1_vs_primary. -> plan/slug-migration.json (Webflow items + pages
      named in tracked repo files); keyword-map-only pages, and collisions with MSV, go to private/migration/ (git-ignored).
  slug_migrate.py stage | canary HUB OLD | verify PAYLOAD READBACK... | rollback [--canary OLD] | crawl | repo-rewrite [--apply]
      staging prep and canary (see each function); none of them calls Webflow (api-update does, with --migration).
  slug_migrate.py sample [N] [--seed S]
      N random rows (old, H1, new) from plan/slug-migration.json.
  slug_migrate.py links
      counts hard-coded internal links to child pages in specs/ (non-archived) and in the newest CMS read.
"""
import glob, json, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slugs as SL   # THE slug function (ops/slugs.py slug_for): the permanent rule and its one exception, used everywhere
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config/collections.json")))
PRIV = os.path.join(ROOT, "private/migration")
CACHE = os.path.join(ROOT, ".cache/migration")
OUT = os.path.join(ROOT, "plan/slug-migration.json")

# Category words per hub (Divit 2026-10-23), as hyphen-token sequences, longest first; plural forms are the same word.
# Nothing else is ever removed or added (workflow, page, questionnaire, sheet, template, automated, questions all stay).
CATEGORY = {
    "LP":         {"strip": [["landing", "pages"], ["landing", "page"]]},
    "Form":       {"strip": [["forms"], ["form"]]},
    "Auto":       {"strip": [["automations"], ["automation"]]},
    "SurveyQuiz": {"strip": [["surveys"], ["survey"], ["quizzes"], ["quiz"]]},
}


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
def _norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", (t or "").lower())).strip()


def _find_in_h1(phrase, h1):
    """the H1's own spelling of phrase (hyphen, space and case insensitive), or None."""
    toks = _norm(phrase).split()
    if not toks: return None
    rx = r"(?<![A-Za-z0-9])" + r"[^A-Za-z0-9]+".join(re.escape(t) for t in toks) + r"s?(?![A-Za-z0-9])"   # the H1 may use the plural
    m = re.search(rx, h1 or "", re.I)
    return m.group(0) if m else None


# Tightened check (Divit 2026-10-23): words the H1 adds right before or after the keyword inside the same noun phrase
# ("Wedding RSVP Website", "Custom Thank You Page"). A word after the keyword that opens a clause (That, Around, for ...) or a
# capitalised clause subject (Clients Sign ...) is not an addition; those were read by hand and listed in H1_CLAUSE_OK.
H1_CONNECTORS = set("that which who whose whom for to with on in and then your you so where when while from at by into before after "
                    "without across as or but than every each any all one its their his her our around using".split())
H1_LEAD = re.compile(r"^\s*build\s+(?:(?:a|an|the|your(?:\s+own)?)\s+)?", re.I)
H1_ADDS = {"generator", "website", "app", "template", "builder", "maker", "software", "tool", "system", "page", "form", "survey",
           "quiz", "workflow", "automation", "sheet", "letter", "custom", "free", "online", "simple", "best"}


def h1_extra_words(h1, phrase):
    """[(side, word)] the H1 adds to the keyword phrase in the same noun phrase."""
    i = (h1 or "").lower().find((phrase or "").lower())
    if i < 0: return []
    pre, post = h1[:i], h1[i + len(phrase):]
    out = [("before", w) for w in H1_LEAD.sub("", pre).split() if w.lower() in H1_ADDS]
    m = re.match(r"^\s*([A-Za-z0-9'\u2019-]+)", post)
    if m and not re.match(r"^\s*[,.:;!?)]", post) and m.group(1).lower() in H1_ADDS: out.append(("after", m.group(1)))
    return out


def slugify(phrase):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", phrase.lower().replace("'", "").replace("’", ""))).strip("-")


# Divit's rulings on the flagged rows (DECISIONS 2026-10-23); the slug in the map already follows each one.
RESOLVED = {("LP", "startup-landing-page"): "DECISIONS 2026-10-23: startup, the H1 wins",
            ("Form", "hipaa-release-form"): "DECISIONS 2026-10-23: hipaa-release approved",
            ("Form", "wedding-rsvp"): "DECISIONS 2026-10-23: H1 fixed to the keyword (Wedding RSVP Form); slug stays wedding-rsvp",
            ("Form", "employment-verification-letter"): "DECISIONS 2026-10-23: the primary wins",
            ("Form", "independent-contractor-agreement"): "DECISIONS 2026-10-23: the primary wins",
            ("Form", "nda-form"): "DECISIONS 2026-10-23: the primary wins (nda)",
            ("LP", "thank-you-page"): "DECISIONS 2026-10-23: the primary wins",
            ("Form", "creator-application"): "H1 adds only the category word (Form): slug unaffected",
            ("SurveyQuiz", "customer-effort-score"): "H1 adds only the category word (Survey): slug unaffected"}


def _load_sources():
    km_p = os.path.join(ROOT, "plan/keyword_map.json")
    km = json.load(open(km_p)) if os.path.exists(km_p) else {}
    ad = json.load(open(os.path.join(ROOT, "plan/additions.json"))).get("pages", {})
    sys.path.insert(0, os.path.join(ROOT, "ops"))
    import skeleton as K   # h1_phrase_for: the keyword phrase the H1 carries (ruling 4)
    return km, ad, K


def cmd_map(args):
    """Divit 2026-10-23 (as the AI App Builder collection): slug = the primary keyword as it appears in the page's H1, with ONLY the
    category word removed, lowercased and hyphenated. No other change. Only collisions are flagged."""
    inv_p = os.path.join(PRIV, "inventory.json")
    if not os.path.exists(inv_p): sys.exit("run: slug_migrate.py inventory (after hubctl api-read for each hub)")
    inv = json.load(open(inv_p))
    km, ad, K = _load_sources()
    prev = {}
    for fp in (OUT, os.path.join(PRIV, "slug-migration-kmap.json")):
        if os.path.exists(fp): prev.update({(e["hub"], e["old_slug"]): e["new_slug"] for e in json.load(open(fp))["pages"]})
    rows_all = []
    for hub, H in inv["hubs"].items():
        d = hubs()[hub]["repo_dir"]
        specs = {}
        for f in glob.glob(os.path.join(ROOT, f"specs/{d}/*.json")):
            try: s = json.load(open(f))
            except Exception: continue
            if s.get("url"): specs[s["url"]] = s
        for r in [dict(x, origin="webflow") for x in H["webflow"]] + [dict(x, origin="planned") for x in H["planned"]]:
            u, s = r["url"], specs.get(r["url"], {})
            kw = s.get("keywords") if isinstance(s.get("keywords"), dict) else {}
            prim, psrc = kw.get("primary"), "spec"
            u2 = f"{hubs()[hub]['path']}/{prev.get((hub, r['slug']), r['slug'])}"   # plan-regen renamed planned pages in the plan files
            if not prim and (km.get(u) or km.get(u2) or {}).get("primary"): prim, psrc = (km.get(u) or km.get(u2))["primary"], "keyword_map"
            if not prim and (ad.get(u) or ad.get(u2) or {}).get("primary"): prim, psrc = (ad.get(u) or ad.get(u2))["primary"], "additions"
            h1 = (s.get("fields") or {}).get("h1") or (r.get("name") if r["origin"] == "webflow" else None)
            h1src = "spec" if (s.get("fields") or {}).get("h1") else ("webflow" if h1 else None)
            phrase, source = None, None
            if h1 and prim:
                cand = K.h1_phrase_for(prim)
                phrase = _find_in_h1(cand, h1) or _find_in_h1(prim, h1)
                source = "h1" if phrase else None
            if not phrase and prim:
                phrase, source = K.h1_phrase_for(prim), ("primary (no H1 yet)" if not h1 else "primary (phrase not found in H1)")
            if not phrase:
                phrase, source = r["slug"].replace("-", " "), "old slug (no H1, no primary)"
            # Divit 2026-10-23 FINAL: the slug is slug_for(hub, target keyword); the H1 phrase is kept only for the H1 checks
            n = SL.slug_for(hub, prim or phrase); removed = strip(hub, r["slug"])[1]
            if source and source.startswith("old slug"): source = "old slug (no H1, no primary)"
            else: source = "slug_for(primary)" if prim else "slug_for(H1 phrase)"
            e = {"hub": hub, "item_id": r.get("item_id"), "origin": r["origin"], "webflow_state": r.get("webflow_state"),
                 "repo_state": r.get("status_state"), "old_slug": r["slug"], "h1": h1, "h1_source": h1src, "h1_phrase": phrase,
                 "slug_source": source, "primary": prim, "primary_source": psrc if prim else None, "new_slug": n,
                 "removed": [x[1] + "@" + x[2] for x in removed], "flags": [],
                 "_public": r["origin"] == "webflow" or r.get("public_source", True)}
            if not n: e["flags"].append("empty")
            if prim and _norm(phrase) != _norm(prim): e["flags"].append("h1_vs_primary")
            if e["h1"] and prim and not SL.keyword_in_h1(e["h1"], prim): e["flags"].append("h1_lacks_keyword")
            if source == "slug_for(primary)" and phrase and h1:
                for side, w in h1_extra_words(h1, phrase): e["flags"].append(f"h1_adds_{side}:{w}")
            if n != strip(hub, r["slug"])[0]: e["flags"].append("differs_from_old_stripped")
            rows_all.append(e)
    # collisions: one new slug used twice within a collection
    by = defaultdict(list)
    for e in rows_all: by[(e["hub"], e["new_slug"])].append(e)
    for (hub, n), es in by.items():
        if len(es) > 1:
            for e in es: e["flags"].append("collision:" + ",".join(x["old_slug"] for x in es if x is not e))
    for e in rows_all:
        e["decision"] = "collision" if any(f.startswith("collision") for f in e["flags"]) else ("unchanged" if e["new_slug"] == e["old_slug"] else "change")
        if (e["hub"], e["new_slug"]) in SL.EXCEPTION_SLUGS and not e["new_slug"].endswith("-quiz"): e["resolution"] = "DECISIONS 2026-10-23: named exception (custom / free are part of the page's own name)"
        if (e["hub"], e["old_slug"]) in SL.EXCEPTION_SLUGS: e["decision"] = "exception"; e["resolution"] = "DECISIONS 2026-10-23: survey/quiz collision exception, the quiz keeps -quiz"
        if (e["hub"], e["old_slug"]) in RESOLVED: e["resolution"] = RESOLVED[(e["hub"], e["old_slug"])]
    public = [e for e in rows_all if e["_public"]]; private = [e for e in rows_all if not e["_public"]]
    for e in rows_all: e.pop("_public")
    tot = defaultdict(Counter)
    for e in public: tot[e["hub"]][e["origin"] + "_" + e["decision"]] += 1
    doc = {"_note": "Slug migration map (DECISIONS 2026-10-23 SLUG MIGRATION; Divit's rule 2026-10-23, as the AI App Builder collection): "
                    "slug = the primary keyword as it appears in the page's H1, ONLY the category word removed, lowercased and hyphenated; "
                    "no other change. Generated by ops/slug_migrate.py map (read only toward Webflow). decision: unchanged | change | exception (survey/quiz collision: the quiz keeps -quiz) | collision. "
                    "Pages known only from the git-ignored keyword map are in private/migration/slug-migration-kmap.json.",
           "rule": {h: ["-".join(s) for s in v["strip"]] for h, v in CATEGORY.items()},
           "totals": {h: dict(c) for h, c in tot.items()},
           "pages": [{k: v for k, v in e.items() if not (k == "primary" and e.get("primary_source") == "keyword_map")}   # no Semrush data in git
                     for e in sorted(public, key=lambda e: (e["hub"], e["origin"] != "webflow", e["old_slug"]))]}
    json.dump(doc, open(OUT, "w"), indent=1)
    os.makedirs(PRIV, exist_ok=True)
    json.dump({"pages": private}, open(os.path.join(PRIV, "slug-migration-kmap.json"), "w"), indent=1)
    # collisions with MSV: private only
    col = []
    for (hub, n), es in sorted(by.items()):
        if len(es) > 1:
            col.append({"hub": hub, "new_slug": n, "pages": [{"old_slug": x["old_slug"], "origin": x["origin"], "h1": x["h1"], "primary": x["primary"],
                        "msv": (km.get(hubs()[hub]["path"] + "/" + x["old_slug"]) or {}).get("primary_msv")} for x in es]})
    json.dump(col, open(os.path.join(PRIV, "collisions.json"), "w"), indent=1)
    print(json.dumps(doc["totals"], indent=1))
    print("rows:", len(rows_all), "(public", len(public), "+ keyword-map-only", len(private), ") collisions:", len(col),
          "h1_vs_primary:", sum("h1_vs_primary" in e["flags"] for e in rows_all),
          "h1_adds:", sum(any(f.startswith("h1_adds") for f in e["flags"]) for e in rows_all), "->", os.path.relpath(OUT, ROOT))

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


# ---------------------------------------------------------------- staging prep (step B) and canary (step C)
DAY = "2026-10-23"
CHILDEDITS = os.path.join(ROOT, "childedits", DAY)
BEFORE = os.path.join(CHILDEDITS, "slug-migration.before.json")
OUTDIR = os.path.join(ROOT, "ops", "out", "migration")          # git-ignored: payloads
REDIRECTS = os.path.join(ROOT, "reports", DAY, "slug-migration-redirects.csv")
FAQ = "awb---faq-data"


def _mapping(public_only=False):
    """{(hub path, old slug): new slug} for every row whose slug changes (live and planned)."""
    rows = json.load(open(OUT))["pages"]
    if not public_only and os.path.exists(os.path.join(PRIV, "slug-migration-kmap.json")):
        rows += json.load(open(os.path.join(PRIV, "slug-migration-kmap.json")))["pages"]
    return {(hubs()[e["hub"]]["path"], e["old_slug"]): e["new_slug"] for e in rows if e["new_slug"] != e["old_slug"] and e.get("decision") != "collision"}


def rewrite_links(text, mp):
    """every child-page URL (absolute emergent.sh or root-relative) whose slug changes, rewritten to the new slug; (text, n)."""
    n = [0]
    def one(m):
        new = mp.get((m.group(2), m.group(3)))
        if not new: return m.group(0)
        n[0] += 1; return f"{m.group(1) or ''}{m.group(2)}/{new}"
    out = re.sub(r"(https?://(?:www\.)?emergent\.sh)?(/ai-(?:landing-page|form|automation|survey-and-quiz)-builder)/([a-z0-9-]+)(?![a-z0-9-])", one, text or "")
    return out, n[0]


def _fresh_reads():
    rbdir = os.path.join(ROOT, ".cache/readback"); out = {}
    for hub, h in hubs().items():
        rb = newest_readback(h["repo_dir"], rbdir)
        out[hub] = (rb, json.load(open(rb))["result"]["items"])
    return out


def plan_items(reads, mp, only_target=None):
    """[(hub, item, new fieldData)] for every item whose slug or FAQ links change. only_target (hub, old slug): the canary, i.e.
    that one item's slug plus the links pointing at it, nothing else."""
    rows = {e["item_id"]: e for e in json.load(open(OUT))["pages"] if e.get("item_id")}
    sub = {only_target: mp[only_target]} if only_target else mp
    out = []
    for hub, (rb, items) in reads.items():
        path = hubs()[hub]["path"]
        for it in items:
            fd = it["fieldData"]; nf = {}
            r = rows.get(it["id"])
            if r and r["decision"] == "change" and (not only_target or only_target == (path, fd["slug"])):
                if r["old_slug"] != fd["slug"]: sys.exit(f"refused: {it['id']} slug is {fd['slug']} in Webflow, the map says {r['old_slug']} (re-run inventory/map)")
                nf["slug"] = r["new_slug"]
            txt, n = rewrite_links(fd.get(FAQ), sub)
            if n: nf[FAQ] = txt
            if nf: out.append((hub, it, nf, n))
    return out


def pending_staged(reads):
    """items whose staged version is newer than the published one (a domain publish would push them too)."""
    out = []
    for hub, (rb, items) in reads.items():
        for it in items:
            lu, lp = it.get("lastUpdated"), it.get("lastPublished")
            if it.get("isDraft") or it.get("isArchived"): continue
            if lp is None or (lu and lu > lp): out.append({"hub": hub, "id": it["id"], "slug": it["fieldData"]["slug"], "lastUpdated": lu, "lastPublished": lp})
    return out


def _payload(plan, label):
    by = defaultdict(list)
    for hub, it, nf, _n in plan: by[hubs()[hub]["collection_id"]].append({"id": it["id"], "fieldData": nf})
    return [{"label": f"{label} {CHILD_NAME.get(c, c)}", "update_collection_items": {"collection_id": c, "request": {"items": its}}} for c, its in by.items()]


CHILD_NAME = {h["collection_id"]: n for n, h in CFG["hubs"].items()}


def cmd_stage(args):
    """slug_migrate.py stage: from the newest full reads (hubctl api-read x4) write
      childedits/<day>/slug-migration.before.json (slug + awb---faq-data of every item the migration touches; commit it),
      ops/out/migration/full-<hub>.json (api-update payloads: slugs + rewritten FAQ links; staged only, no publish action),
      reports/<day>/slug-migration-redirects.csv (old path,new path; one row per changing live page; single hop),
      .cache/migration/pending-staged.json (items with unpublished staged changes) and a summary. Nothing is sent to Webflow."""
    reads = _fresh_reads(); mp = _mapping()
    plan = plan_items(reads, mp)
    # single hop: no new slug is itself an old slug that changes again
    chains = [(k, v) for k, v in mp.items() if (k[0], v) in mp]
    if chains: sys.exit(f"refused: redirect chains {chains[:5]}")
    before = {"op": "slug-migration", "day": DAY, "note": "Before-values for the slug migration (DECISIONS 2026-10-23): slug and awb---faq-data of every touched item, from the reads named here. Rollback: ops/slug_migrate.py rollback.",
              "reads": {h: os.path.basename(rb) for h, (rb, _) in reads.items()},
              "items": [{"id": it["id"], "hub": hub, "collection": hubs()[hub]["collection_id"], "fieldData": {k: it["fieldData"].get(k) for k in nf}} for hub, it, nf, _n in plan]}
    os.makedirs(CHILDEDITS, exist_ok=True); json.dump(before, open(BEFORE, "w"), indent=1, ensure_ascii=False)
    os.makedirs(OUTDIR, exist_ok=True)
    for hub in hubs():
        sub = [p for p in plan if p[0] == hub]
        if sub: json.dump(_payload(sub, "slug migration (staged only)"), open(os.path.join(OUTDIR, f"full-{hubs()[hub]['repo_dir']}.json"), "w"), indent=1, ensure_ascii=False)
    live = {(hubs()[h]["path"], it["fieldData"]["slug"]) for h, (rb, its) in reads.items() for it in its if not it.get("isDraft") and it.get("lastPublished")}
    rows = sorted((f"{p}/{o}", f"{p}/{n}") for (p, o), n in mp.items() if (p, o) in live)
    with open(REDIRECTS, "w") as f:
        f.write("source,target\n"); [f.write(f"{a},{b}\n") for a, b in rows]
    pend = pending_staged(reads); os.makedirs(CACHE, exist_ok=True)
    json.dump(pend, open(os.path.join(CACHE, "pending-staged.json"), "w"), indent=1)
    c = Counter(); links = Counter()
    for hub, it, nf, n in plan: c[(hub, "slug" in nf, FAQ in nf)] += 1; links[hub] += n
    print(f"items touched: {len(plan)} (slug changes {sum(1 for p in plan if 'slug' in p[2])}, FAQ rewrites {sum(1 for p in plan if FAQ in p[2])}, links rewritten {sum(links.values())}: {dict(links)})")
    print(f"redirects: {len(rows)} rows -> {os.path.relpath(REDIRECTS, ROOT)}; before-values -> {os.path.relpath(BEFORE, ROOT)}; payloads -> {os.path.relpath(OUTDIR, ROOT)}/")
    print(f"pending staged changes (lastUpdated > lastPublished): {len(pend)}")
    for p in pend: print(f"  {p['hub']} {p['slug']} {p['id']} updated {p['lastUpdated']} published {p['lastPublished']}")


def cmd_canary(args):
    """slug_migrate.py canary HUB OLD_SLUG: the api-update payload for ONE page (its slug + every FAQ link pointing at it, no other
    change), ops/out/migration/canary-<slug>.json, and its single redirect row reports/<day>/canary-redirect.csv. Run it through
    hubctl api-update <payload> --dry-run, then --live --migration (staged only; the payload has no publish action)."""
    hub, old = args[0], args[1]; path = hubs()[hub]["path"]; mp = _mapping()
    if (path, old) not in mp: sys.exit(f"{hub} {old}: no slug change in the map")
    reads = _fresh_reads(); plan = plan_items(reads, mp, only_target=(path, old))
    B = json.load(open(BEFORE)); bidx = {x["id"]: x for x in B["items"]}
    for hub_, it, nf, _n in plan:   # the before-values must still be the live values
        for k in nf:
            if (bidx.get(it["id"]) or {}).get("fieldData", {}).get(k) != it["fieldData"].get(k):
                sys.exit(f"refused: {it['id']} {k} changed since {os.path.relpath(BEFORE, ROOT)}; re-run stage and commit")
    pf = os.path.join(OUTDIR, f"canary-{old}.json"); os.makedirs(OUTDIR, exist_ok=True)
    json.dump(_payload(plan, f"slug migration canary {old} (staged only)"), open(pf, "w"), indent=1, ensure_ascii=False)
    cp = os.path.join(ROOT, "reports", DAY, "canary-redirect.csv")
    with open(cp, "w") as f: f.write("source,target\n" + f"{path}/{old},{path}/{mp[(path, old)]}\n")
    print(f"canary {path}/{old} -> {path}/{mp[(path, old)]}: {len(plan)} item(s): " + ", ".join(f"{h}:{it['fieldData']['slug']}({it['id']}; {'+'.join(sorted(nf))}; {n} link(s))" for h, it, nf, n in plan))
    print(f"payload {os.path.relpath(pf, ROOT)}; redirect row {os.path.relpath(cp, ROOT)}")


def cmd_verify(args):
    """slug_migrate.py verify PAYLOAD READBACK...: every item in the payload has exactly the sent fields in the given reads; prints diffs."""
    pf, rbs = args[0], args[1:]
    got = {it["id"]: it for rb in rbs for it in json.load(open(rb))["result"]["items"]}
    bad = 0
    for a in json.load(open(pf)):
        for it in a["update_collection_items"]["request"]["items"]:
            g = (got.get(it["id"]) or {}).get("fieldData") or {}
            for k, v in it["fieldData"].items():
                ok = g.get(k) == v; bad += not ok
                print(("OK   " if ok else "DIFF ") + f"{it['id']} {k}" + ("" if ok else f": got {str(g.get(k))[:80]!r}"))
    print("read-back clean" if not bad else f"{bad} mismatch(es)"); return 1 if bad else 0


def cmd_rollback(args):
    """slug_migrate.py rollback [--canary OLD_SLUG]: ONE command to build the restore. Writes ops/out/migration/rollback[-canary-<slug>].json
    (api-update payload: the before-values of slug and awb---faq-data, staged only) and reports/<day>/slug-migration-redirects-remove.csv
    (the 301 rows to delete). Then run: hubctl api-update <that payload> --live --migration.
    Slug restores pass the guard only with --rollback, only to each item's committed before-value, only while the freeze is active
    (Divit 2026-10-23 rollback exception in ops/webflow_api.py)."""
    B = json.load(open(BEFORE)); items = B["items"]
    if "--canary" in args:
        old = args[args.index("--canary") + 1]
        pf0 = os.path.join(OUTDIR, f"canary-{old}.json")
        ids = {it["id"] for a in json.load(open(pf0)) for it in a["update_collection_items"]["request"]["items"]}
        sent = {it["id"]: set(it["fieldData"]) for a in json.load(open(pf0)) for it in a["update_collection_items"]["request"]["items"]}
        items = [dict(x, fieldData={k: v for k, v in x["fieldData"].items() if k in sent[x["id"]]}) for x in items if x["id"] in ids]
    by = defaultdict(list)
    for x in items: by[x["collection"]].append({"id": x["id"], "fieldData": x["fieldData"]})
    name = "rollback" + (f"-canary-{args[args.index('--canary') + 1]}" if "--canary" in args else "")
    pf = os.path.join(OUTDIR, f"{name}.json"); os.makedirs(OUTDIR, exist_ok=True)
    json.dump([{"label": f"slug migration {name} (before-values)", "update_collection_items": {"collection_id": c, "request": {"items": its}}} for c, its in by.items()], open(pf, "w"), indent=1, ensure_ascii=False)
    src = os.path.join(ROOT, "reports", DAY, "canary-redirect.csv" if "--canary" in args else "slug-migration-redirects.csv")
    rp = os.path.join(ROOT, "reports", DAY, ("canary-" if "--canary" in args else "slug-migration-") + "redirects-remove.csv")
    open(rp, "w").write(open(src).read())
    print(f"rollback payload {os.path.relpath(pf, ROOT)} ({len(items)} item(s)); redirects to delete {os.path.relpath(rp, ROOT)}")
    print(f"run: .venv/bin/python3 ops/hubctl.py api-update {os.path.relpath(pf, ROOT)} --live --migration --rollback")


def cmd_crawl(args):
    """slug_migrate.py crawl [--workers N]: fetch every sitemap page outside the 4 hubs' child pages (static pages, Learn, other hubs,
    blog ...) and count hard-coded links to child pages whose slug changes -> .cache/migration/crawl.json + summary."""
    import concurrent.futures as cf
    mp = _mapping(); paths = sitemap_urls(fetch=True)
    hubp = {h["path"] for h in hubs().values()}
    todo = [p for p in paths if not any(p.startswith(h + "/") for h in hubp)]
    def get(p):
        try:
            r = urllib.request.urlopen(urllib.request.Request("https://emergent.sh" + p, headers={"User-Agent": "emergent-hubs-slug-migrate"}), timeout=30)
            return p, r.read().decode("utf-8", "replace"), None
        except Exception as e: return p, "", str(e)[:80]
    n = int(args[args.index("--workers") + 1]) if "--workers" in args else 12
    res, errs = {}, []
    with cf.ThreadPoolExecutor(n) as ex:
        for p, html, err in ex.map(get, todo):
            if err: errs.append((p, err)); continue
            hits = [m.group(0) for m in re.finditer(r"href=[\"']((?:https?://(?:www\.)?emergent\.sh)?/ai-(?:landing-page|form|automation|survey-and-quiz)-builder/[a-z0-9-]+)", html)]
            ch = [h for h in hits if rewrite_links(h, mp)[1]]
            if hits: res[p] = {"links": len(hits), "changing": len(ch), "targets": sorted(set(re.sub(r"^href=[\"']", "", h) for h in ch))}
    os.makedirs(CACHE, exist_ok=True); json.dump({"pages": res, "errors": errs, "fetched": len(todo)}, open(os.path.join(CACHE, "crawl.json"), "w"), indent=1)
    sec = Counter("/" + p.split("/")[1] for p in res)
    print(f"crawled {len(todo)} pages outside the 4 hubs' child pages ({len(errs)} errors); {len(res)} link to child pages; "
          f"{sum(v['changing'] for v in res.values())} links to changing slugs on {sum(1 for v in res.values() if v['changing'])} pages; by section {dict(sec)}")
    for p in list(res)[:15]: print(f"  {p}: {res[p]['links']} link(s), {res[p]['changing']} changing")


REPO_FILES = ["status/lp.json", "status/form.json", "status/aab.json", "status/sqb.json", "status/live.json", "status/feasibility.json",
              "status/synonyms.json", "status/fix_queue.json", "status/swap_short.json", "status/quiz-canary.json", "status/canary-r15.json",
              "plan/queue-ranked.txt", "plan/additions.json", "plan/overrides.json", "plan/keyword_map.json", "config/typography.json",
              "ops/heading_lines.mjs", "ops/ship.py"]   # files the code reads today (history files, logs and reports keep the old URLs)


def _walk_set(o, fn):
    if isinstance(o, dict): return {k: _walk_set(v, fn) for k, v in o.items()}
    if isinstance(o, list): return [_walk_set(v, fn) for v in o]
    if isinstance(o, str): return fn(o)
    return o


def cmd_repo_rewrite(args):
    """slug_migrate.py repo-rewrite [--apply]: the repo moves to the new slugs (DECISIONS 2026-10-23 one-publish plan, step 1).
      specs: git mv specs/<dir>/<old>.json -> <new>.json and images/<dir>/<old>/ -> <new>/; url, fields.slug and images[*].path follow;
        every child URL in every spec string is rewritten (FAQ, faq_plan, pending_links, notes). The text change is mechanical, so a
        review hash, approval fingerprint or cms_draft fingerprint that was current BEFORE the rewrite is restamped after it (history
        entry "slug migration"); a stamp that was already stale stays stale.
      REPO_FILES and rules/*.json: child URLs rewritten. Bare-slug keys (per_page, synonyms, flag_decisions "<slug>:<hash>",
        private pulls) are NOT renamed: new slugs repeat across hubs, so those stores keep the old slug via slugs.store_key.
      tests/golden/cases.jsonl: urls rewritten in cases that read the CURRENT spec (cases pinned to a sha keep the historical path).
    DRY by default."""
    sys.path.insert(0, os.path.join(ROOT, "ops")); import guards as G, subprocess, datetime
    apply = "--apply" in args; mp = _mapping(); ch = Counter(); moves = []; restamp = Counter()
    fn = lambda t: rewrite_links(t, mp)[0]
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    for hub, h in hubs().items():
        d, path = h["repo_dir"], h["path"]
        for f in sorted(glob.glob(os.path.join(ROOT, f"specs/{d}/*.json"))):
            raw = open(f).read(); s = json.loads(raw); sl = os.path.basename(f)[:-5]
            new = mp.get((path, sl)); n_links = rewrite_links(raw, mp)[1]
            if not new and not n_links: continue
            rc0 = G.review_changed(s) == [] if s.get("review_hash") else None
            fp0 = G.fingerprint(s)
            ap0 = (s.get("approval") or {}).get("fingerprint") == fp0
            cd0 = (s.get("cms_draft") or {}).get("fingerprint") == fp0
            lk0 = bool(s.get("lock_hash")) and (G.review_changed(dict(s, review_hash=s["lock_hash"])) or []) == []   # review lock (ruling 10 B2)
            s2 = _walk_set(s, fn)
            if new:
                s2["url"] = f"{path}/{new}"
                if (s2.get("fields") or {}).get("slug") == sl: s2["fields"]["slug"] = new
                for im in (s2.get("images") or {}).values():
                    if isinstance(im, dict) and (im.get("path") or "").startswith(f"images/{d}/{sl}/"): im["path"] = f"images/{d}/{new}/" + im["path"][len(f"images/{d}/{sl}/"):]
                nf = os.path.join(os.path.dirname(f), new + ".json")
                if os.path.exists(nf): sys.exit(f"refused: {os.path.relpath(nf, ROOT)} exists")
                moves.append((f, nf))
                if os.path.isdir(os.path.join(ROOT, "images", d, sl)): moves.append((os.path.join(ROOT, "images", d, sl), os.path.join(ROOT, "images", d, new)))
            ch["specs touched"] += 1; ch["spec links"] += n_links
            if apply:
                tgt = f
                if new:
                    subprocess.run(["git", "mv", os.path.relpath(f, ROOT), os.path.relpath(nf, ROOT)], cwd=ROOT, check=True); tgt = nf
                    imd = os.path.join(ROOT, "images", d, sl)
                    if os.path.isdir(imd): subprocess.run(["git", "mv", os.path.relpath(imd, ROOT), os.path.join("images", d, new)], cwd=ROOT, check=True)
                fp1 = G.fingerprint(s2)
                if rc0: s2["review_hash"] = G.review_hash(s2); restamp["review_hash"] += 1
                if lk0: s2["lock_hash"] = G.review_hash(s2); restamp["lock_hash"] += 1
                if ap0 and s2.get("approval"): s2["approval"]["fingerprint"] = fp1; restamp["approval"] += 1
                if cd0 and s2.get("cms_draft"): s2["cms_draft"]["fingerprint"] = fp1; restamp["cms_draft"] += 1
                s2.setdefault("history", []).append({"t": now, "state": s2.get("status"), "via": "slug-migration", "by": "slug_migrate",
                                                     "note": (f"slug {sl} -> {new}; " if new else "") + f"{n_links} child link(s) rewritten (DECISIONS 2026-10-23); stamps current before were restamped"})
                json.dump(s2, open(tgt, "w"), indent=1, ensure_ascii=False)
    files = REPO_FILES + sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "rules", "*.json")))
    for rel in files:
        fp = os.path.join(ROOT, rel)
        if not os.path.exists(fp): continue
        t, n = rewrite_links(open(fp).read(), mp)
        if n:
            ch[rel] += n
            if apply:
                if rel.endswith(".json"): json.loads(t)
                open(fp, "w").write(t)
    # the git-ignored live SERP pull is COPIED to the new slug (the old file stays for the other clone and history)
    import shutil
    for (p, o), n in mp.items():
        d = next(h["repo_dir"] for h in hubs().values() if h["path"] == p)
        for src in glob.glob(os.path.join(ROOT, "private", "serp", d, o + ".json")):   # serp is per hub dir and read by URL; the bare-slug
            # stores (alsoasked, verdicts, Semrush derived, rules per_page/synonyms/flag_decisions) keep the old key: slugs.store_key
            dst = os.path.join(os.path.dirname(src), n + os.path.basename(src)[len(o):])
            if not os.path.exists(dst):
                ch["private pulls copied"] += 1
                if apply: shutil.copy2(src, dst)
    gc = os.path.join(ROOT, "tests", "golden", "cases.jsonl"); out = []; ng = 0
    for line in open(gc):
        if not line.strip(): out.append(line); continue
        c = json.loads(line)
        if c.get("sha") or c.get("kind") in ("slug-rule", "slug-for"): out.append(line); continue
        t, n = rewrite_links(line, mp); ng += n; out.append(t)
    ch["golden case links"] = ng
    if apply: open(gc, "w").write("".join(out))
    ch["moves (specs + image folders)"] = len(moves)
    print(("APPLIED" if apply else "DRY RUN (nothing written)") + ": " + json.dumps(dict(ch)) + ("; restamped " + json.dumps(dict(restamp)) if apply else ""))


def cmd_plan_regen(args):
    """slug_migrate.py plan-regen [--apply]: the keyword plan's slugs regenerated from slugs.slug_for for every PLANNED page that has
    no spec and no writer at work (state none or parked): plan/keyword_map.json (git-ignored, in place), plan/additions.json,
    plan/queue-ranked.txt and its status/<dir>.json key. Pages with a spec or a writer at work keep their URL until the repo
    rewrite (repo-rewrite), so a spec, its status and its queue row never disagree. DRY by default."""
    apply = "--apply" in args
    rows = json.load(open(OUT))["pages"] + (json.load(open(os.path.join(PRIV, "slug-migration-kmap.json")))["pages"] if os.path.exists(os.path.join(PRIV, "slug-migration-kmap.json")) else [])
    specs = {}
    for f in glob.glob(os.path.join(ROOT, "specs", "*", "*.json")):
        try: specs[json.load(open(f)).get("url")] = f
        except ValueError: pass
    mp, kept = {}, []
    for e in rows:
        if e["origin"] != "planned" or e["new_slug"] == e["old_slug"] or e.get("decision") == "collision": continue
        path = hubs()[e["hub"]]["path"]; u = f"{path}/{e['old_slug']}"
        if u in specs or e.get("repo_state") not in (None, "parked"): kept.append((e["hub"], e["old_slug"], e["new_slug"], e.get("repo_state"), u in specs)); continue
        mp[(path, e["old_slug"])] = e["new_slug"]
    clash = [(p, n) for (p, o), n in mp.items() if any(r["hub"] and hubs()[r["hub"]]["path"] == p and r["old_slug"] == n for r in rows)]
    if clash: sys.exit(f"refused: new slugs already used as current URLs: {clash[:5]}")
    ch = Counter()
    files = ["plan/keyword_map.json", "plan/additions.json", "plan/queue-ranked.txt"] + [f"status/{h['repo_dir']}.json" for h in hubs().values()]
    for rel in files:
        fp = os.path.join(ROOT, rel)
        if not os.path.exists(fp): continue
        t, n = rewrite_links(open(fp).read(), mp); ch[rel] = n
        if apply and n:
            if rel.endswith(".json"): json.loads(t)   # still valid JSON
            open(fp, "w").write(t)
    print(("APPLIED" if apply else "DRY RUN (nothing written)") + f": {len(mp)} planned page(s) renamed; " + json.dumps(dict(ch)))
    print(f"kept for the repo rewrite (spec or writer at work): {len(kept)}: " + ", ".join(f"{h}:{o}({s or 'no status'}{', spec' if sp else ''})" for h, o, n, s, sp in kept))


def _redirect_rows(text):
    """(source, target) pairs from a Webflow 301 export (CSV, any header) or a pasted list ("old new", "old -> new", "old,new")."""
    import csv, io
    out = []
    for row in csv.reader(io.StringIO(text)):
        line = ",".join(row).strip()
        if not line: continue
        parts = [p.strip() for p in re.split(r"\s*(?:,|->|=>|\t|\s{1,})\s*", line) if p.strip()]
        if len(parts) < 2 or not parts[0].startswith("/") and not parts[0].startswith("http"): continue   # header or junk
        norm = lambda p: re.sub(r"^https?://(www\.)?emergent\.sh", "", p).rstrip("/") or "/"
        out.append((norm(parts[0]), norm(parts[1])))
    return out


def cmd_redirects_merge(args):
    """slug_migrate.py redirects-merge EXPORT [--out FILE]: Webflow's CSV import REPLACES every existing 301, so the import file must
    be Divit's export (Site settings > Publishing > 301 redirects > Export; or a pasted list in a file) merged with our rows
    (reports/<day>/slug-migration-redirects.csv). Dedupes; turns chains into single hops (an existing redirect whose target is one of
    our old paths now points straight at the new path); flags conflicts (the same source to two targets; an existing redirect away
    from one of our new paths; a loop). Writes the merged CSV (default .cache/migration/redirects-merged.csv) and prints counts.
    Nothing is sent to Webflow; the import is Divit's click."""
    existing = _redirect_rows(open(args[0]).read())
    ours = _redirect_rows(open(REDIRECTS).read())
    out = os.path.join(ROOT, args[args.index("--out") + 1]) if "--out" in args else os.path.join(CACHE, "redirects-merged.csv")
    oursrc = dict(ours); ournew = {t for _, t in ours}
    merged, seen, chains, conflicts, dups = [], {}, [], [], 0
    for s, t in existing:
        if s in seen:
            if seen[s] != t: conflicts.append(f"existing: {s} has two targets ({seen[s]}, {t})")
            else: dups += 1
            continue
        if t in oursrc: chains.append(f"{s} -> {t} becomes {s} -> {oursrc[t]} (single hop)"); t = oursrc[t]
        if s in oursrc and oursrc[s] != t: conflicts.append(f"{s}: existing target {t} vs migration target {oursrc[s]} (migration row kept)"); continue
        if s in ournew: conflicts.append(f"{s}: an existing redirect leaves one of our NEW paths (to {t}); it would hide the page (dropped)"); continue
        if s == t: conflicts.append(f"{s}: redirects to itself (dropped)"); continue
        seen[s] = t; merged.append((s, t))
    for s, t in ours:
        if s in seen:
            if seen[s] == t: dups += 1
            continue
        seen[s] = t; merged.append((s, t))
    loops = [s for s, t in merged if t in seen and seen[t] != t]   # any remaining two-hop
    for s in loops: conflicts.append(f"{s}: still two hops ({s} -> {seen[s]} -> {seen[seen[s]]})")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write("source,target\n"); [f.write(f"{s},{t}\n") for s, t in merged]
    print(f"existing {len(existing)} + migration {len(ours)} -> merged {len(merged)} rows ({dups} duplicate(s) dropped, {len(chains)} chain(s) collapsed, {len(conflicts)} conflict(s)) -> {os.path.relpath(out, ROOT)}")
    for c in chains: print("  CHAIN   " + c)
    for c in conflicts: print("  CONFLICT " + c)
    return 1 if conflicts else 0


FULL_BEFORE = os.path.join(CHILDEDITS, "slug-migration-full.before.json")
FULL_PAYLOAD = os.path.join(OUTDIR, "full.json")
GLOSSARY_CID = "6a7ec305d1588226be6fe84f"
GLOSSARY_ITEMS = {"6ada1d308bdda167d0d2a515": "data-entry-automation", "6ad0b5cf77dcc42a34cf7d77": "what-is-task-automation",
                  "6ad0ad37a85323214cd0d52c": "document-automation"}   # Divit 2026-10-23: one-off Glossary write (3 links)
GLOSSARY_FIELD = "glossary---content"
EXTRA_PAGES = {"/ai-form-builder/wedding-rsvp": "ac55c3de"}   # reviewed changes shipped with the migration (DECISIONS 2026-10-23)


def _text_fields(hub, url):
    """CMS text fields as the spec exports them (images excluded): {cms field: value}."""
    sys.path.insert(0, os.path.join(ROOT, "ops")); import hubctl as H
    s = json.load(open(H.spath(url))); out, _pending = H.export_fields(url, s)
    fm = CFG["hubs"][hub]["fields"]; imgs = set(CFG.get("image_fields") or [])
    return {fm[k]: v for k, v in out.items() if k in fm and k not in imgs and isinstance(v, str)}


def cmd_stage_full(args):
    """slug_migrate.py stage-full [--glossary FILE]: THE staging payload for the one-publish plan (DECISIONS 2026-10-23), from the
    newest full reads (hubctl api-read x4):
      ops/out/migration/full.json    api-update payload, all 4 child collections: every slug change, every FAQ link rewrite and the
                                     reviewed changes of EXTRA_PAGES; staged only, no publish action. Run ONCE:
                                     hubctl api-update ops/out/migration/full.json --live --migration
      ops/out/migration/glossary-mcp.json   the 3 Glossary items' glossary---content with the links rewritten, as one Webflow MCP
                                     data_cms_tool update_collection_items action (the repo API refuses the Glossary collection);
                                     needs --glossary FILE: a read of those 3 items (list_collection_items output saved as JSON).
      childedits/<day>/slug-migration-full.before.json   before-values (the PUBLISHED values) of every field sent, incl. the Glossary.
    Items already staged to the target (the canary) keep their published before-values from slug-migration.before.json."""
    sys.path.insert(0, os.path.join(ROOT, "ops")); import hubctl as H
    reads = _fresh_reads(); mp = _mapping()
    rows = {e["item_id"]: e for e in json.load(open(OUT))["pages"] if e.get("item_id")}
    old_before = {x["id"]: x for x in json.load(open(BEFORE))["items"]} if os.path.exists(BEFORE) else {}
    plan, before = defaultdict(list), []
    for hub, (rb, items) in reads.items():
        path = hubs()[hub]["path"]; cid = hubs()[hub]["collection_id"]
        for it in items:
            fd = it["fieldData"]; nf = {}; r = rows.get(it["id"])
            if r and r["decision"] in ("change", "exception") and r["new_slug"] != r["old_slug"]:
                if fd["slug"] not in (r["old_slug"], r["new_slug"]): sys.exit(f"refused: {it['id']} slug {fd['slug']} is neither {r['old_slug']} nor {r['new_slug']}")
                if fd["slug"] != r["new_slug"]: nf["slug"] = r["new_slug"]
            txt, n = rewrite_links(fd.get(FAQ), mp)
            if n: nf[FAQ] = txt
            url_now = f"{path}/{r['new_slug'] if r else fd['slug']}"
            if url_now in EXTRA_PAGES:
                for k, v in _text_fields(hub, url_now).items():
                    v2 = rewrite_links(v, mp)[0]
                    if fd.get(k) != v2: nf[k] = v2
            if not nf: continue
            plan[cid].append({"id": it["id"], "fieldData": nf})
            ob = old_before.get(it["id"], {}).get("fieldData", {})
            bfd = {}
            for k in nf:   # published value: the old before-value where this item was already staged (canary), else the live read
                bfd[k] = ob[k] if (k in ob and it.get("lastUpdated", "") > (it.get("lastPublished") or "")) else fd.get(k)
            before.append({"id": it["id"], "hub": hub, "collection": cid, "fieldData": bfd})
    # the canary items already staged: nothing left to send, but their published before-values stay in the file for the rollback
    sent = {x["id"] for x in before}
    for iid, ob in old_before.items():
        if iid not in sent: before.append(dict(ob, note="already staged (canary); published before-value kept for rollback"))
    payload = [{"label": f"slug migration FULL {CHILD_NAME[c]} (staged only)", "update_collection_items": {"collection_id": c, "request": {"items": its}}} for c, its in plan.items()]
    gl = None
    if "--glossary" in args:
        g = json.load(open(args[args.index("--glossary") + 1]))
        gitems = (g.get("result") or g).get("items") if isinstance(g, dict) else g
        gl = []
        for it in gitems:
            if it["id"] not in GLOSSARY_ITEMS: continue
            txt, n = rewrite_links(it["fieldData"].get(GLOSSARY_FIELD), mp)
            if n:
                gl.append({"id": it["id"], "fieldData": {GLOSSARY_FIELD: txt}, "_links": n})
                before.append({"id": it["id"], "hub": "Glossary", "collection": GLOSSARY_CID, "fieldData": {GLOSSARY_FIELD: it["fieldData"].get(GLOSSARY_FIELD)}})
        json.dump([{"label": "slug migration: 3 Glossary links (one-off, Divit 2026-10-23; staged only)", "update_collection_items": {
            "collection_id": GLOSSARY_CID, "request": {"items": [{"id": x["id"], "fieldData": x["fieldData"]} for x in gl]}}}],
            open(os.path.join(OUTDIR, "glossary-mcp.json"), "w"), indent=1, ensure_ascii=False)
    os.makedirs(OUTDIR, exist_ok=True); json.dump(payload, open(FULL_PAYLOAD, "w"), indent=1, ensure_ascii=False)
    json.dump({"op": "slug-migration", "day": DAY, "note": "FULL staging before-values (published values of every field in ops/out/migration/full.json and glossary-mcp.json). Rollback: slug_migrate.py rollback-full.",
               "reads": {h: os.path.basename(rb) for h, (rb, _) in reads.items()}, "items": before}, open(FULL_BEFORE, "w"), indent=1, ensure_ascii=False)
    c = Counter()
    for cid, its in plan.items():
        for it in its:
            for k in it["fieldData"]: c[(CHILD_NAME[cid], k)] += 1
    print(f"full.json: {sum(len(v) for v in plan.values())} items in {len(plan)} collections; fields: " + ", ".join(f"{h}:{k}={n}" for (h, k), n in sorted(c.items())))
    if gl is not None: print(f"glossary-mcp.json: {len(gl)} items, {sum(x['_links'] for x in gl)} links")
    print(f"before-values: {os.path.relpath(FULL_BEFORE, ROOT)} ({len(before)} items)")


def cmd_rollback_full(args):
    """slug_migrate.py rollback-full: ONE restore payload from childedits/<day>/slug-migration-full.before.json (slugs, links, every
    staged field back to the PUBLISHED value): ops/out/migration/rollback-full.json (4 child collections; run
    hubctl api-update ops/out/migration/rollback-full.json --live --migration --rollback) and rollback-glossary-mcp.json (the 3
    Glossary items, one MCP update). Redirects: re-import private/migration/existing-redirects-2026-10-23.csv (the original
    553 rows), which replaces the migration's 301s. Nothing is published either way."""
    B = json.load(open(FULL_BEFORE)); by = defaultdict(list)
    for x in B["items"]: by[x["collection"]].append({"id": x["id"], "fieldData": x["fieldData"]})
    child = [{"label": f"slug migration ROLLBACK {CHILD_NAME.get(c, c)} (before-values)", "update_collection_items": {"collection_id": c, "request": {"items": its}}} for c, its in by.items() if c != GLOSSARY_CID]
    json.dump(child, open(os.path.join(OUTDIR, "rollback-full.json"), "w"), indent=1, ensure_ascii=False)
    if GLOSSARY_CID in by:
        json.dump([{"label": "slug migration ROLLBACK Glossary (before-values)", "update_collection_items": {"collection_id": GLOSSARY_CID, "request": {"items": by[GLOSSARY_CID]}}}],
                  open(os.path.join(OUTDIR, "rollback-glossary-mcp.json"), "w"), indent=1, ensure_ascii=False)
    print(f"rollback-full.json: {sum(len(v) for c, v in by.items() if c != GLOSSARY_CID)} items; rollback-glossary-mcp.json: {len(by.get(GLOSSARY_CID, []))} items")
    print("run: .venv/bin/python3 ops/hubctl.py api-update ops/out/migration/rollback-full.json --live --migration --rollback")
    print("then: the Glossary restore through the Webflow MCP (rollback-glossary-mcp.json), and re-import private/migration/existing-redirects-2026-10-23.csv")


def cmd_diff_staged(args):
    """slug_migrate.py diff-staged [--glossary FILE] (step 4): after the staging write, read the 4 collections again (hubctl api-read x4
    first) and prove the staged state is EXACTLY the migration:
      - every sent field now equals full.json exactly; every field NOT sent equals the pre-staging read named in the before file;
      - every item NOT in full.json (canary aside) is field-for-field identical to that pre-staging read: anything else STOPS (exit 1).
        (lastUpdated > lastPublished is only informational: a publish to the webflow.io staging domain also sets lastPublished.)
      - counts per collection (expected, staged, exact, mismatched, unexpected).
    --glossary FILE: a fresh MCP read of the 3 Glossary items, checked the same way against glossary-mcp.json."""
    sys.path.insert(0, os.path.join(ROOT, "ops")); import hubctl as H
    P = json.load(open(FULL_PAYLOAD)); B = json.load(open(FULL_BEFORE))
    want = {it["id"]: (a["update_collection_items"]["collection_id"], it["fieldData"]) for a in P for it in a["update_collection_items"]["request"]["items"]}
    canary = {x["id"]: x for x in B["items"] if x.get("note", "").startswith("already staged")}
    pre = {}
    for hub, f in (B.get("reads") or {}).items():
        for it in json.load(open(os.path.join(ROOT, ".cache", "readback", f)))["result"]["items"]: pre[it["id"]] = it
    cur = _fresh_reads(); stop = []; rows = []
    for hub, (rb, items) in cur.items():
        c = Counter(); cid = hubs()[hub]["collection_id"]
        c["expected"] = sum(1 for i, (cc, _) in want.items() if cc == cid)
        for it in items:
            staged = (it.get("lastUpdated") or "") > (it.get("lastPublished") or "")
            if staged and not it.get("isDraft"): c["staged"] += 1   # informational: a webflow.io publish also sets lastPublished
            fd = it["fieldData"]; p0 = (pre.get(it["id"]) or {}).get("fieldData")
            if it["id"] in want:
                sent = want[it["id"]][1]
                bad = [k for k, v in sent.items() if fd.get(k) != v]
                bad += [k + " (not sent, changed)" for k in set(fd) | set(p0 or {}) if k not in sent and fd.get(k) != (p0 or {}).get(k)]
                if bad: c["mismatched"] += 1; stop.append(f"{hub} {fd.get('slug')} {it['id']}: " + ", ".join(sorted(bad)[:6]))
                else: c["exact"] += 1
            elif it["id"] in canary:
                cf_ = canary[it["id"]]; c["canary"] += 1
            elif p0 is None:
                c["unexpected"] += 1; stop.append(f"{hub} {fd.get('slug')} {it['id']}: UNEXPECTED item (not in the pre-staging read)")
            elif fd != p0:
                c["unexpected"] += 1; stop.append(f"{hub} {fd.get('slug')} {it['id']}: UNEXPECTED change in " + ", ".join(sorted(k for k in set(fd) | set(p0) if fd.get(k) != p0.get(k))[:6]))
        missing = [i for i, (cc, _) in want.items() if cc == cid and i not in {x["id"] for x in items}]
        for i in missing: stop.append(f"{hub} {i}: expected item not in the read"); c["mismatched"] += 1
        rows.append((hub, c))
    if "--glossary" in args:
        g = json.load(open(args[args.index("--glossary") + 1])); gitems = {x["id"]: x for x in ((g.get("result") or g).get("items") if isinstance(g, dict) else g)}
        GP = json.load(open(os.path.join(OUTDIR, "glossary-mcp.json")))[0]["update_collection_items"]["request"]["items"]; c = Counter(expected=len(GP))
        for x in GP:
            got = (gitems.get(x["id"]) or {}).get("fieldData", {}).get(GLOSSARY_FIELD)
            if got == x["fieldData"][GLOSSARY_FIELD]: c["exact"] += 1
            else: c["mismatched"] += 1; stop.append(f"Glossary {x['id']}: glossary---content differs from glossary-mcp.json")
        rows.append(("Glossary", c))
    print(f"{'collection':12} {'expected':>8} {'staged':>7} {'exact':>6} {'canary':>7} {'mismatch':>9} {'unexpected':>11}")
    for h, c in rows: print(f"{h:12} {c['expected']:8} {c['staged']:7} {c['exact']:6} {c['canary']:7} {c['mismatched']:9} {c['unexpected']:11}")
    for s in stop: print("  STOP " + s)
    print("EXACT: the staged state is the migration and nothing else" if not stop else f"STOP: {len(stop)} problem(s); do not publish")
    return 1 if stop else 0


def _fetch(url, follow=False):
    """(status, location, body) without following redirects (follow=True: urllib default)."""
    import urllib.request, urllib.error
    class NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    op = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedir)
    req = urllib.request.Request(url, headers={"User-Agent": "emergent-hubs-slug-verify", "Cache-Control": "no-cache"})
    for attempt in range(3):
        try:
            r = op.open(req, timeout=40); return r.status, r.headers.get("Location"), r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e: return e.code, e.headers.get("Location"), (e.read() or b"").decode("utf-8", "replace")
        except Exception as e:
            if attempt == 2: return 0, None, str(e)
    return 0, None, ""


def cmd_verify_site(args):
    """slug_migrate.py verify-site --base URL [--workers N] [--audit] (step 5): READ ONLY, the same on staging and production.
      new URLs   every live child page under its new URL: 200, the spec's H1, canonical = the new path, carousel (section_build with
                 cards), Learn (3 cards to /learn/<slug>), FAQ (window.awbFAQ questions = the spec's)
      old URLs   every changed live page's old URL: exactly one 301 to its new URL, and that target answers 200 (single hop)
      redirects  every row of reports/<day>/redirects-final.csv (the 553 pre-existing rows, chains collapsed, plus ours): 301 to the
                 target, target not itself a redirect
      old links  every page in the base sitemap (hubs, Glossary, carousels, child pages): 0 hrefs to an old child URL
      sitemap    the base sitemap lists every new URL and no old URL
    --audit then runs the full live audit against the same base (hubctl live-audit --all --base URL). Prints one table."""
    import concurrent.futures as cf
    sys.path.insert(0, os.path.join(ROOT, "ops")); import hubctl as H, verify_live as V
    base = args[args.index("--base") + 1].rstrip("/"); n = int(args[args.index("--workers") + 1]) if "--workers" in args else 12
    rows = [e for e in json.load(open(OUT))["pages"] if e["origin"] == "webflow" and e.get("webflow_state") == "published"]
    mp = _mapping(); res = defaultdict(lambda: [0, 0, []])   # check -> [checked, passed, failures]
    def rec(check, ok, why=""):
        r = res[check]; r[0] += 1; r[1] += bool(ok)
        if not ok: r[2].append(why)
    def page(e):
        path = hubs()[e["hub"]]["path"]; new = f"{path}/{e['new_slug']}"; out = []
        st, loc, html = _fetch(base + new)
        out.append(("new URL 200", st == 200, f"{new}: {st}"))
        if st != 200: return out
        sp = H.spath(new); s = json.load(open(sp)) if os.path.exists(sp) else {}
        want_h1 = (s.get("fields") or {}).get("h1") or e.get("h1")
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S); h1 = re.sub(r"\s+", " ", __import__("html").unescape(re.sub(r"<[^>]+>", "", h1.group(1)))).strip() if h1 else None
        out.append(("H1", h1 == (want_h1 or "").strip(), f"{new}: {h1!r} vs {want_h1!r}"))
        can = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', html) or re.search(r'<link[^>]+href="([^"]+)"[^>]+rel="canonical"', html)
        out.append(("canonical", bool(can) and re.sub(r"^https?://[^/]+", "", can.group(1)).rstrip("/") == new, f"{new}: {can.group(1) if can else 'missing'}"))
        car = re.search(r'class="section_build[^"]*"(.*?)</section>', html, re.S)
        out.append(("carousel", bool(car) and len(re.findall(r'href="[^"]*/ai-[a-z-]+-builder/[a-z0-9-]+"', car.group(1))) > 0, f"{new}: section_build missing or without cards"))
        lok, lline = V.learn_section(html); out.append(("Learn", lok, f"{new}: {lline}"))
        fq = re.search(r"window\.awbFAQ\s*=\s*(\{.*?\})\s*;\s*</script>", html, re.S); fs = re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;\s*</script>", (s.get("fields") or {}).get("faq", ""), re.S)
        try: lq = [i["q"] for i in json.loads(fq.group(1))["items"]] if fq else []
        except Exception: lq = []
        sq = [i["q"] for i in json.loads(fs.group(1))["items"]] if fs else None
        out.append(("FAQ", bool(lq) and (sq is None or lq == sq), f"{new}: {len(lq)} live vs {len(sq) if sq else '?'} spec"))
        return out
    def old(e):
        path = hubs()[e["hub"]]["path"]; o, nw = f"{path}/{e['old_slug']}", f"{path}/{e['new_slug']}"
        st, loc, _ = _fetch(base + o); tgt = re.sub(r"^https?://[^/]+", "", loc or "").rstrip("/")
        ok = st == 301 and tgt == nw
        st2 = _fetch(base + nw)[0] if ok else None
        return [("old URL 301 single hop", ok and st2 == 200, f"{o}: {st} -> {loc} ({st2})")]
    def redir(row):
        s, t = row; st, loc, _ = _fetch(base + s); got = re.sub(r"^https?://[^/]+", "", loc or "").rstrip("/") or "/"
        tt = t if t.startswith("http") and not t.startswith(base) else re.sub(r"^https?://[^/]+", "", t).rstrip("/") or "/"
        ok = st == 301 and (got == tt or loc == t)
        st2 = _fetch(t if t.startswith("http") else base + t)[0] if ok else None
        return [("redirect rows (301, single hop)", ok and st2 == 200, f"{s}: {st} -> {loc} (target {st2})")]
    changed = [e for e in rows if e["new_slug"] != e["old_slug"]]
    csvp = os.path.join(ROOT, "reports", DAY, "redirects-final.csv")
    rrows = [tuple(l.strip().split(",", 1)) for l in open(csvp).read().splitlines()[1:] if "," in l] if os.path.exists(csvp) else []
    with cf.ThreadPoolExecutor(n) as ex:
        for out in ex.map(page, rows):
            for c, ok, why in out: rec(c, ok, why)
        for out in ex.map(old, changed):
            for c, ok, why in out: rec(c, ok, why)
        for out in ex.map(redir, rrows):
            for c, ok, why in out: rec(c, ok, why)
    # sitemap and old links. The sub-sitemaps (page-sitemap.xml ...) are served on emergent.sh by Cloudflare, not by Webflow: on a
    # webflow.io base they 404, so the sitemap checks run only where the base serves them; the page list for the link crawl then
    # comes from the production sitemap with the migrated paths swapped in.
    sst, _, sm = _fetch(base + "/sitemap.xml", follow=True)
    locs = re.findall(r"<loc>([^<]+)</loc>", sm); own = True
    if "<sitemapindex" in sm:
        allp = []
        for u in locs:
            stx, _, body = _fetch(base + re.sub(r"^https?://[^/]+", "", u), follow=True)
            if stx != 200: own = False; stx, _, body = _fetch(u, follow=True)
            allp += re.findall(r"<loc>([^<]+)</loc>", body)
        locs = allp
    paths = sorted({re.sub(r"^https?://[^/]+", "", u).rstrip("/") or "/" for u in locs})
    pset = set(paths)
    if own:
        rec("sitemap fetched", sst == 200 and bool(paths), f"{base}/sitemap.xml: {sst}")
        for e in changed:
            p_ = hubs()[e["hub"]]["path"]
            rec("sitemap: new URL listed", f"{p_}/{e['new_slug']}" in pset, f"{p_}/{e['new_slug']} not in the sitemap")
            rec("sitemap: old URL absent", f"{p_}/{e['old_slug']}" not in pset, f"{p_}/{e['old_slug']} still in the sitemap")
    else:
        print(f"  sitemap checks skipped on {base}: its sub-sitemaps are not served there (Cloudflare on emergent.sh); run verify-site on production after the publish")
    moved = {f"{hubs()[e['hub']]['path']}/{e['old_slug']}": f"{hubs()[e['hub']]['path']}/{e['new_slug']}" for e in changed}
    crawl = sorted({moved.get(p, p) for p in paths} | {f"{hubs()[e['hub']]['path']}/{e['new_slug']}" for e in rows} | {h["path"] for h in hubs().values()})
    oldset = {f"{p}/{o}" for (p, o) in mp}
    def links(p):
        st_, _, html = _fetch(base + p)
        bad = sorted({h for h in re.findall(r'href="(?:https?://(?:www\.)?(?:emergent\.sh|emergent-sh\.webflow\.io))?(/ai-(?:landing-page|form|automation|survey-and-quiz)-builder/[a-z0-9-]+)', html) if h in oldset})
        return p, st_, bad
    with cf.ThreadPoolExecutor(n) as ex:
        for p, st_, bad in ex.map(links, crawl):
            if st_ in (301, 302, 404) and p not in moved.values(): continue   # a sitemap page that is itself a redirect or gone: not a page to scan
            rec("0 links to old URLs (every page)", st_ == 200 and not bad, f"{p}: HTTP {st_}" if st_ != 200 else f"{p}: " + ", ".join(bad[:5]))
    print(f"verify-site {base}")
    print(f"{'check':45} {'checked':>8} {'passed':>7} {'failed':>7}")
    tot_f = 0
    for c, (k, p, f) in res.items():
        print(f"{c:45} {k:8} {p:7} {k - p:7}"); tot_f += k - p
    for c, (k, p, f) in res.items():
        for w in f[:10]: print(f"  FAIL {c}: {w}")
        if len(f) > 10: print(f"  ... {len(f) - 10} more {c} failure(s)")
    os.makedirs(CACHE, exist_ok=True)
    json.dump({c: {"checked": k, "passed": p, "failures": f} for c, (k, p, f) in res.items()}, open(os.path.join(CACHE, f"verify-site-{re.sub(r'[^a-z0-9]+', '-', base)}.json"), "w"), indent=1)
    if "--audit" in args:
        import subprocess
        r = subprocess.run([sys.executable, os.path.join(ROOT, "ops", "hubctl.py"), "live-audit", "--all", "--base", base], cwd=ROOT)
        print(f"live audit on {base}: exit {r.returncode}")
        tot_f += bool(r.returncode)
    print("ALL PASS" if not tot_f else f"FAILED: {tot_f}")
    return 1 if tot_f else 0


def cmd_sample(args):
    import random
    n = int(args[0]) if args and args[0].isdigit() else 15
    seed = int(args[args.index("--seed") + 1]) if "--seed" in args else 20261023
    rows = json.load(open(OUT))["pages"]
    print("seed", seed)
    for e in random.Random(seed).sample(rows, n):
        print(f"{e['hub']}\t{e['old_slug']}\t{e['h1'] or '(no H1: ' + e['slug_source'] + ')'}\t{e['new_slug']}")


if __name__ == "__main__":
    cmds = {"inventory": cmd_inventory, "map": cmd_map, "links": cmd_links, "sample": cmd_sample, "stage": cmd_stage,
            "canary": cmd_canary, "verify": cmd_verify, "rollback": cmd_rollback, "crawl": cmd_crawl, "repo-rewrite": cmd_repo_rewrite, "plan-regen": cmd_plan_regen, "redirects-merge": cmd_redirects_merge, "stage-full": cmd_stage_full, "rollback-full": cmd_rollback_full, "diff-staged": cmd_diff_staged, "verify-site": cmd_verify_site}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds: sys.exit(__doc__)
    sys.exit(cmds[sys.argv[1]](sys.argv[2:]) or 0)
