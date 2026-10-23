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
  slug_migrate.py sample [N] [--seed S]
      N random rows (old, H1, new) from plan/slug-migration.json.
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


def new_slug(hub, phrase):
    """slugify(phrase) with ONLY the hub's category word removed (hyphen-bounded, anywhere)."""
    s, removed = strip(hub, slugify(phrase))
    return s, removed


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
            if not prim and (km.get(u) or {}).get("primary"): prim, psrc = km[u]["primary"], "keyword_map"
            if not prim and (ad.get(u) or {}).get("primary"): prim, psrc = ad[u]["primary"], "additions"
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
            n, removed = new_slug(hub, phrase)
            e = {"hub": hub, "item_id": r.get("item_id"), "origin": r["origin"], "webflow_state": r.get("webflow_state"),
                 "repo_state": r.get("status_state"), "old_slug": r["slug"], "h1": h1, "h1_source": h1src, "h1_phrase": phrase,
                 "slug_source": source, "primary": prim, "primary_source": psrc if prim else None, "new_slug": n,
                 "removed": [x[1] + "@" + x[2] for x in removed], "flags": [],
                 "_public": r["origin"] == "webflow" or r.get("public_source", True)}
            if not n: e["flags"].append("empty")
            if prim and _norm(phrase) != _norm(prim): e["flags"].append("h1_vs_primary")
            if source == "h1":
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
    public = [e for e in rows_all if e["_public"]]; private = [e for e in rows_all if not e["_public"]]
    for e in rows_all: e.pop("_public")
    tot = defaultdict(Counter)
    for e in public: tot[e["hub"]][e["origin"] + "_" + e["decision"]] += 1
    doc = {"_note": "Slug migration map (DECISIONS 2026-10-23 SLUG MIGRATION; Divit's rule 2026-10-23, as the AI App Builder collection): "
                    "slug = the primary keyword as it appears in the page's H1, ONLY the category word removed, lowercased and hyphenated; "
                    "no other change. Generated by ops/slug_migrate.py map (read only toward Webflow). decision: unchanged | change | collision. "
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


def cmd_sample(args):
    import random
    n = int(args[0]) if args and args[0].isdigit() else 15
    seed = int(args[args.index("--seed") + 1]) if "--seed" in args else 20261023
    rows = json.load(open(OUT))["pages"]
    print("seed", seed)
    for e in random.Random(seed).sample(rows, n):
        print(f"{e['hub']}\t{e['old_slug']}\t{e['h1'] or '(no H1: ' + e['slug_source'] + ')'}\t{e['new_slug']}")


if __name__ == "__main__":
    cmds = {"inventory": cmd_inventory, "map": cmd_map, "links": cmd_links, "sample": cmd_sample}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds: sys.exit(__doc__)
    cmds[sys.argv[1]](sys.argv[2:])
