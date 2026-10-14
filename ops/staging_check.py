"""staging_check.py: Divit's full staging check (plan/template-run-2026-10-14.md, "Staging check"; Divit 2026-10-14).
Read-only: HTTP GET/HEAD and a headless browser (ops/staging_check.mjs) on the public staging site. No Webflow API or MCP call,
no publish of any kind.

    .venv/bin/python3 ops/staging_check.py                      the full check: every live child page (status state published),
                                                                the 4 hubs and the 2 canary quiz pages
    .venv/bin/python3 ops/staging_check.py --baseline           capture the pixel-diff baseline (390 and 1440 px, every page)
                                                                into .cache/staging/baseline/ (header masked at diff time)
    options: --base URL (default the staging domain) --pages URL,URL  --sections carousel,learn,...  --concurrency N
             --rejudge DIR (judge an earlier run again, no browser)  --diff-threshold F (share of changed pixels in a section, default 0.002)  --expect-change CLS,CLS (sections the
             run changes on purpose; their diffs are listed, not failed; default section_build,section_blog-related)

Writes .cache/staging/<UTC timestamp>/report.md (+ summary.json, per-page JSON, diff images, divit/ screenshots at true size)
and a short summary on stdout. Exit 1 when any check fails.

Checks (sections): links (every internal href 200 on the staging host, no "#" placeholder and no detail_ template slug; the
verify-live function of ops/verify_live.py), console (0 error-level messages and page errors; only Divit's 2026-10-14 source
exception is ignored: rules/live_audit.json console_ignore_sources, matched on the error's source captured through CDP, never
on its text; every ignored error is listed), header (the header or navbar exists and is visible; its content is not judged: KS's work), faq (no
answer cut by overflow or an inner scroll at 1440 and 390; every item on hubs, the first on child pages), emptyp (no empty or
zero-width <p>), meta (og:image present and 200; every JSON-LD block parses; a FAQPage's questions equal the visible FAQ),
carousel (section_build on one child page per hub and the 4 hubs at 1440, 1024, 768 and 390: cover loads, 16:10 +-2%,
object-fit cover, alt; title inside the card and not clipped; one link per card to a live item that answers 200; 15 cards
then Load more adds more; hover moves only that card; equal heights per row; the expected classes), learn (section_blog-related
on the 4 template pages: 3 cards, the newest Learn articles in /learn order, images load, titles, links 200, no "No items
found"), pixel (diff against the baseline per section, header and footer masked), quiz (playthrough on the 2 canary pages at
390 and 1280 with the ops/quiz/test_embed.mjs checks; "not present" when the page is not on staging yet), divit (screenshots).
"""
import datetime, html as _html, json, os, re, subprocess, sys, time
from urllib.parse import urlsplit
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ops"))

STAGING_BASE = "https://emergent-sh.webflow.io"     # the staging domain of every earlier staging check (reports/2026-10-13)
CANON = "https://emergent.sh"
CACHE = os.path.join(ROOT, ".cache", "staging")
BASELINE = os.path.join(CACHE, "baseline")
CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))
HUBS = [h["path"] for h in CFG["hubs"].values()]
ALL_SECTIONS = ["links", "console", "header", "faq", "emptyp", "meta", "carousel", "learn", "pixel", "quiz", "divit"]
COVER_RATIO, RATIO_TOL = 1.6, 0.02
PAGE_SIZE = 15
WIDTHS_CAROUSEL = [1440, 1024, 768, 390]

# ---------------------------------------------------------------- page set
def published_urls():
    out = []
    for h in CFG["hubs"].values():
        p = os.path.join(ROOT, "status", f"{h['repo_dir']}.json")
        if os.path.exists(p): out += [u for u, e in json.load(open(p))["pages"].items() if e.get("state") == "published"]
    return sorted(out)

def quiz_pages():
    p = os.path.join(ROOT, "status", "quiz-canary.json")
    return json.load(open(p)).get("canary_pages", []) if os.path.exists(p) else []

def hub_of(url): return "/" + url.strip("/").split("/")[0]
def key_of(url): return url.strip("/").replace("/", "__") or "home"

def build_pages(only=None):
    live, quiz = published_urls(), quiz_pages()
    templates = {}
    for u in live:
        templates.setdefault(hub_of(u), u)     # one child page per hub carries the template checks (first published, by URL)
    urls = only if only else live + HUBS + quiz
    pages = []
    for u in urls:
        kind = "hub" if u in HUBS else "quiz" if u in quiz else "child"
        tpl = kind == "child" and (bool(only) or templates.get(hub_of(u)) == u)
        pages.append({"url": u, "key": key_of(u), "kind": kind, "hub": hub_of(u),
                      "carousel": kind == "hub" or tpl, "learn": tpl})
    return pages, live, templates

# ---------------------------------------------------------------- pure judges (golden: tests/golden/run.py kind staging-check)
def _inside(a, b, tol=1.0):
    return a["x"] >= b["x"] - tol and a["y"] >= b["y"] - tol and a["x"] + a["w"] <= b["x"] + b["w"] + tol and a["y"] + a["h"] <= b["y"] + b["h"] + tol

def href_problem(href, hub=None, live=None, resolved=None):
    """Why a card href is wrong, or None. href: the attribute as written; resolved: the browser's absolute URL (optional);
    hub: the card must point at /<hub>/<slug>; live: the set of live paths."""
    h = (href or "").strip()
    if h in ("", "#") or h.startswith("#"): return f'placeholder href "{h}"'
    h = resolved or h
    path = urlsplit(h).path.rstrip("/") if "://" in h else h.split("?")[0].split("#")[0].rstrip("/")
    if re.search(r"(^|/)detail_[^/]*$", path): return f"template page slug {path}"
    if hub and not re.fullmatch(re.escape(hub) + r"/[a-z0-9-]+", path): return f"not an item URL of {hub}: {path}"
    if live is not None and path not in live: return f"not a live item: {path}"
    return None

def judge_cover(c):
    """Failures of one carousel cover (measured box, natural size, object-fit, alt)."""
    v = c.get("cover")
    if not v: return ["no cover image"]
    out = []
    if not (v.get("complete") and (v.get("nw") or 0) > 0): out.append("cover image not loaded")
    b = v["box"]
    if not b["h"] or abs((b["w"] / b["h"]) / COVER_RATIO - 1) > RATIO_TOL:
        out.append(f"cover box {b['w']:.0f}x{b['h']:.0f} is not 16:10 (ratio {b['w'] / b['h'] if b['h'] else 0:.3f})")
    if v.get("fit") != "cover":
        out.append(f"cover object-fit {v.get('fit')}")
        if v.get("nw") and v.get("nh") and b["h"] and abs((v["nw"] / v["nh"]) / (b["w"] / b["h"]) - 1) > RATIO_TOL:
            out.append(f"cover stretched (natural {v['nw']}x{v['nh']} in a {b['w']:.0f}x{b['h']:.0f} box)")
    if not (v.get("alt") or "").strip(): out.append("cover alt empty")
    return out

def judge_carousel(m, hub, live, live_hub_count):
    """{check: (ok, detail)} for one carousel measurement (one page, one width)."""
    r = {}
    if not m or not m.get("present"): return {"carousel_rendered": (False, "section_build not in the page (hidden or missing)")}
    if not m.get("displayed"): return {"carousel_rendered": (False, "section_build present but not displayed")}
    r["carousel_rendered"] = (True, "")
    miss = [c for c, ok in (m.get("classes") or {}).items() if not ok]
    r["classes"] = (not miss, "missing: " + ", ".join(miss) if miss else "")
    cards = m.get("cards") or []
    r["no_items_found"] = (not m.get("no_items_text") and len(cards) > 0, 'shows "No items found"' if m.get("no_items_text") else ("no cards" if not cards else ""))
    cov, tit, lnk = [], [], []
    for i, c in enumerate(cards, 1):
        cov += [f"card {i}: {x}" for x in judge_cover(c)]
        t = c.get("title")
        if not t or not t.get("text"): tit.append(f"card {i}: no title")
        else:
            if c.get("link") and not _inside(t["box"], c["link"]): tit.append(f"card {i}: title outside the card link")
            if not _inside(t["box"], c["item"]): tit.append(f"card {i}: title outside the card")
            if t["sw"] > t["cw"]: tit.append(f"card {i}: title clipped (scrollWidth {t['sw']} > clientWidth {t['cw']})")
        if c.get("n_links") != 1: lnk.append(f"card {i}: {c.get('n_links')} links (one link must wrap the card)")
        elif not c.get("link_wraps"): lnk.append(f"card {i}: the link does not wrap cover and title")
        elif c.get("link") and not (c["link"]["w"] >= c["item"]["w"] - 2 and c["link"]["h"] >= c["item"]["h"] - 2):
            lnk.append(f"card {i}: the link covers {c['link']['w']:.0f}x{c['link']['h']:.0f} of a {c['item']['w']:.0f}x{c['item']['h']:.0f} card")
        if not re.match(r"build_link", c.get("link_class") or ""): lnk.append(f"card {i}: link class {c.get('link_class')!r} (expected build_link)")
        p = href_problem(c.get("href"), hub, live, c.get("abs"))
        if p: lnk.append(f"card {i}: {p}")
    r["cover"] = (not cov, "; ".join(cov[:6]) + (f" (+{len(cov) - 6})" if len(cov) > 6 else ""))
    r["title"] = (not tit, "; ".join(tit[:6]) + (f" (+{len(tit) - 6})" if len(tit) > 6 else ""))
    r["card_link"] = (not lnk, "; ".join(lnk[:6]) + (f" (+{len(lnk) - 6})" if len(lnk) > 6 else ""))
    rows = {}
    for c in cards: rows.setdefault(round(c["item"]["y"] / 4), []).append(c["item"]["h"])
    bad = [f"row at y={k * 4}: heights {min(v):.1f}..{max(v):.1f}" for k, v in rows.items() if max(v) - min(v) > 1]
    r["equal_heights"] = (not bad, "; ".join(bad[:4]))
    if "hover" in m:
        h = m["hover"]
        if not h.get("done"): r["hover"] = (False, "hover not tested")
        else: r["hover"] = (h["changed"] == [h["hovered"]], f"hovered card {h['hovered'] + 1}; transform changed on cards {[i + 1 for i in h['changed']] or 'none'}")
    if "load_more" in m:
        lm = m["load_more"]; want = min(PAGE_SIZE, live_hub_count) if live_hub_count is not None else PAGE_SIZE
        first = lm.get("first", len(cards))
        r["first_page_15"] = (first == want, f"{first} cards on the first page (expected {want})")
        steps = lm.get("steps") or []
        if live_hub_count is None or live_hub_count > PAGE_SIZE:
            r["load_more"] = (bool(steps) and steps[0].get("after", 0) > steps[0].get("before", 0), "Load more: " + (", ".join(f"{s.get('before')}->{s.get('after')}" if "after" in s else s.get("error", "?") for s in steps) or "no visible Load more control"))
        else: r["load_more"] = (True, f"{live_hub_count} live items: no Load more needed")
        hs = [h for h in lm.get("all_hrefs") or [] if h]
        paths = [urlsplit(h).path.rstrip("/") if "://" in h else h.rstrip("/") for h in hs]
        dups = sorted({p for p in paths if paths.count(p) > 1})
        notlive = sorted({p for p in paths if live is not None and p not in live})
        r["only_live"] = (not notlive and not dups, ("not live: " + ", ".join(notlive[:8]) if notlive else "") + (" duplicates: " + ", ".join(dups[:5]) if dups else ""))
    return r

def judge_learn(m, order, dates):
    """order: /learn listing hrefs (newest first); dates: href -> date string."""
    r = {}
    if not m or not m.get("present") or not m.get("displayed"): return {"learn_rendered": (False, "section_blog-related not rendered (hidden or missing)")}
    cards = m.get("cards") or []
    r["learn_rendered"] = (True, "")
    r["learn_3_cards"] = (len(cards) == 3 and not m.get("no_items_text"), f"{len(cards)} cards" + (' and "No items found"' if m.get("no_items_text") else ""))
    hrefs = [urlsplit(c.get("abs") or "").path.rstrip("/") for c in cards]
    bad = [f"card {i}: {href_problem(c.get('href'), '/learn', None, c.get('abs'))}" for i, c in enumerate(cards, 1) if href_problem(c.get("href"), "/learn", None, c.get("abs"))]
    r["learn_hrefs"] = (not bad, "; ".join(bad))
    im = [f"card {i}" for i, c in enumerate(cards, 1) if not (c.get("img") and c["img"].get("complete") and c["img"].get("nw", 0) > 0)]
    r["learn_images"] = (not im, "image not loaded: " + ", ".join(im) if im else "")
    t = [f"card {i}" for i, c in enumerate(cards, 1) if not c.get("title")]
    r["learn_titles"] = (not t, "no title: " + ", ".join(t) if t else "")
    if order:
        top = order[:3]
        if set(hrefs) == set(top): r["learn_newest"] = (True, "")
        else:
            pd = lambda s: datetime.datetime.strptime(s.strip(), "%b %d, %Y") if s and s.strip() else None
            cut = pd(dates.get(top[-1], "")) if len(top) == 3 else None
            ok = cut is not None and all(pd(dates.get(h, "")) and pd(dates.get(h, "")) >= cut for h in hrefs) and len(hrefs) == 3
            r["learn_newest"] = (ok, ("same publish date as the newest (tie): " if ok else "not the newest 3: ") + ", ".join(hrefs) + " vs /learn " + ", ".join(top))
    else: r["learn_newest"] = (False, "/learn listing not read")
    return r

def learn_order(html):
    items = re.findall(r'class="blog_item w-dyn-item".*?href="([^"]+)".*?fs-list-field="date"[^>]*>([^<]*)<', html, re.S)
    order, dates = [], {}
    for h, d in items:
        p = urlsplit(h).path.rstrip("/") if "://" in h else h.rstrip("/")
        if p not in dates: order.append(p); dates[p] = d
    return order, dates

def _ld_strings(o):
    if isinstance(o, dict):
        for v in o.values(): yield from _ld_strings(v)
    elif isinstance(o, list):
        for v in o: yield from _ld_strings(v)
    elif isinstance(o, str): yield o

def judge_jsonld(blocks, visible_q):
    """(ok, detail, warn): every block parses; a FAQPage's questions equal the visible FAQ questions (order and text)."""
    norm = lambda s: re.sub(r"\s+", " ", _html.unescape(s or "")).strip()
    errs, faqs, ents = [], [], []
    for i, b in enumerate(blocks, 1):
        try: j = json.loads(b)
        except Exception as e: errs.append(f"block {i} does not parse ({str(e)[:60]})"); continue
        for node in (j.get("@graph") if isinstance(j, dict) and isinstance(j.get("@graph"), list) else [j]):
            if isinstance(node, dict) and node.get("@type") == "FAQPage": faqs.append([norm(q.get("name")) for q in node.get("mainEntity") or []])
        ents += [s[:60] for s in _ld_strings(j) if re.search(r"&(#\d+|amp|quot|lt|gt|apos);", s)]
    if errs: return False, "; ".join(errs), ""
    warn = ("HTML entities in JSON-LD text: " + " | ".join(ents[:3])) if ents else ""
    if not faqs: return True, "no FAQPage (not required on child templates, DECISIONS 2026-10-06)", warn
    vq = [re.sub(r"^\d{1,2}[.)]\s+", "", norm(q)) for q in visible_q]   # a visible "1. " numbering is layout, not question text
    bad = [f"FAQPage {k}: {len(f)} questions vs {len(vq)} visible" + ("" if len(f) != len(vq) else f"; first difference: {next((a for a, b in zip(f, vq) if a != b), '')[:60]!r}") for k, f in enumerate(faqs, 1) if f != vq]
    return not bad, "; ".join(bad) or f"FAQPage matches {len(vq)} visible questions", warn

# ---------------------------------------------------------------- links (verify_live's every-internal-href check, on staging)
def href_findings(html, url_path, base=STAGING_BASE):
    """Offline half of the link check: (targets {staging url: [anchors]}, placeholders, template-slug anchors), from
    verify_live.internal_links with the staging host counted as internal; relative and emergent.sh links map to the staging host."""
    import verify_live as V
    if not hasattr(V, "internal_links"): sys.exit("ops/verify_live.py has no internal_links(): git pull the internal-link upgrade first")
    hosts = set(V.INTERNAL_HOSTS); V.INTERNAL_HOSTS = hosts | {urlsplit(base).hostname}
    try: targets, placeholders, slugs = V.internal_links(html, CANON + url_path)
    finally: V.INTERNAL_HOSTS = hosts
    out = {}
    for t, anchors in targets.items():
        u = urlsplit(t); out.setdefault(base + (u.path or "/") + (("?" + u.query) if u.query else ""), []).extend(anchors)
    return out, placeholders, slugs

def link_checker(base):
    import verify_live as V
    def check(html, url_path, extra_hrefs=()):
        """(ok, fail lines, n unique targets): every internal href answers 200 on the staging host; no "#" and no detail_ href."""
        targets, placeholders, slugs = href_findings(html, url_path, base)
        for h in extra_hrefs:   # card hrefs behind Load more (not in the first rendered DOM)
            if not h: continue
            p = urlsplit(h).path if "://" in h else h
            a = {"href": h, "url": p, "attrs": {}, "section": "section_build", "text": "(after Load more)"}
            if re.search(r"(^|/)detail_[^/]*$", p.rstrip("/")): slugs.append(a)
            elif p.strip() in ("", "#"): placeholders.append(a)
            else: targets.setdefault(base + p, []).append(a)
        fails = [f'placeholder href "{a["href"]}": {V._ctx(a)}' for a in placeholders] + [f"template-page slug {a['url']}: {V._ctx(a)}" for a in slugs]
        for t, anchors in sorted(targets.items()):
            code, _chain = V.link_status(t)
            if code != 200: fails.append(f"{urlsplit(t).path} HTTP {code} ({len(anchors)} anchor(s); first: {V._ctx(anchors[0])})")
        return not fails, fails, len(targets)
    return check, V.link_status

# ---------------------------------------------------------------- pixel diff
def diff_page(key, w, base_meta, cur_meta, base_dir, cur_dir, out_dir, threshold, expect):
    """Per-section diff of two full-page screenshots: header rows and self-moving boxes (marquees, sliders, video, canvas, iframe;
    recorded at capture) masked, footer skipped. Returns [findings]."""
    from PIL import Image
    import numpy as np
    Image.MAX_IMAGE_PIXELS = None   # our own full-page screenshots
    bp, cp = os.path.join(base_dir, f"{key}-{w}.png"), os.path.join(cur_dir, f"{key}-{w}.png")
    if not (os.path.exists(bp) and os.path.exists(cp)): return [{"section": "*", "status": "no baseline" if not os.path.exists(bp) else "no screenshot"}]
    A, B = np.asarray(Image.open(bp).convert("RGB")), np.asarray(Image.open(cp).convert("RGB"))
    def keyed(meta):
        seen, out = {}, {}
        for s in meta.get("sections") or []:
            n = seen.get(s["cls"], 0); seen[s["cls"]] = n + 1; out[f"{s['cls']}#{n}"] = s
        return out
    if (base_meta.get("doc_h") or 0) and (cur_meta.get("doc_h") or 0) > 2 * base_meta["doc_h"]:
        return [{"section": "*", "status": "page height", "detail": f"{base_meta['doc_h']} -> {cur_meta['doc_h']} px (unstyled render or a layout blow-up)"}]
    ka, kb = keyed(base_meta), keyed(cur_meta)
    ha, hb = base_meta.get("header_box"), cur_meta.get("header_box")
    res = []
    for k in sorted(set(ka) | set(kb), key=lambda x: (kb.get(x) or ka.get(x))["y"]):
        cls = k.split("#")[0]
        if cls in ("section_footer",): continue
        if k not in kb: res.append({"section": k, "status": "removed", "expected": cls in expect}); continue
        if k not in ka: res.append({"section": k, "status": "added", "expected": cls in expect}); continue
        sa, sb = ka[k], kb[k]
        ca, cb = A[sa["y"]:sa["y"] + sa["h"]].copy(), B[sb["y"]:sb["y"] + sb["h"]].copy()
        for img, s, hbx in ((ca, sa, ha), (cb, sb, hb)):   # header rows (KS's header work) masked in both
            if hbx:
                y0, y1 = max(0, int(hbx["y0"]) - s["y"]), min(img.shape[0], int(hbx["y1"] + 1) - s["y"])
                if y1 > y0: img[y0:y1] = 0
        # boxes that move on their own (marquees, sliders) or always differ (video, canvas, iframe), from either capture, section-relative
        rel = [(v["x"], v["y"] - s0["y"], v["w"], v["h"]) for meta, s0 in ((base_meta, sa), (cur_meta, sb)) for v in meta.get("volatile") or []
               if v["y"] < s0["y"] + s0["h"] and v["y"] + v["h"] > s0["y"]]
        for img in (ca, cb):
            for x, y, w_, h_ in rel:   # 2 px of padding: a box measured a pixel off still covers its edge
                img[max(0, y - 2):max(0, y + h_ + 2), max(0, x - 2):max(0, x + w_ + 2)] = 0
        if ca.shape != cb.shape:
            res.append({"section": k, "status": "resized", "detail": f"{ca.shape[1]}x{ca.shape[0]} -> {cb.shape[1]}x{cb.shape[0]}", "expected": cls in expect})
            h = min(ca.shape[0], cb.shape[0]); ca, cb = ca[:h], cb[:h]
            if not h: continue
        # a pixel differs only if no pixel within 1 px of it in the other capture matches (sub-pixel text shifts are not changes)
        a16, b16 = ca.astype(np.int16), cb.astype(np.int16)
        d = np.min([np.abs(a16 - np.roll(np.roll(b16, dy, 0), dx, 1)).max(axis=2) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
        m = d > 24
        frac = float(m.mean()) if m.size else 0.0
        if frac > threshold:
            os.makedirs(out_dir, exist_ok=True)
            hl = cb.copy(); hl[m] = (hl[m] * 0.3 + np.array([255, 0, 0]) * 0.7).astype(np.uint8)
            comp = np.concatenate([ca, np.full((ca.shape[0], 8, 3), 255, np.uint8), cb, np.full((ca.shape[0], 8, 3), 255, np.uint8), hl], axis=1)
            f = os.path.join(out_dir, f"{key}-{w}-{k.replace('#', '_')}.png"); Image.fromarray(comp).save(f, optimize=True)
            prev = next((r for r in res if r["section"] == k), None)
            item = {"section": k, "status": "changed", "share": round(frac, 4), "image": os.path.relpath(f, os.path.dirname(out_dir)), "expected": cls in expect}
            if prev: prev.update({**item, "status": "resized+changed", "detail": prev.get("detail")})
            else: res.append(item)
    return res

# ---------------------------------------------------------------- run
def run_node(job_path):
    return subprocess.run(["node", os.path.join(ROOT, "ops", "staging_check.mjs"), job_path], cwd=ROOT).returncode

def opt(args, k, d=None):
    return args[args.index(k) + 1] if k in args else d

def main(args):
    t0 = time.time()
    base = (opt(args, "--base", STAGING_BASE)).rstrip("/")
    only = [u.strip() for u in (opt(args, "--pages") or "").split(",") if u.strip()]
    only = [urlsplit(u).path.rstrip("/") if "://" in u else "/" + u.strip("/") for u in only]
    sections = [s.strip() for s in (opt(args, "--sections") or ",".join(ALL_SECTIONS)).split(",") if s.strip()]
    conc = int(opt(args, "--concurrency", "4")); threshold = float(opt(args, "--diff-threshold", "0.002"))
    expect = set((opt(args, "--expect-change") or "section_build,section_blog-related").split(","))
    baseline = "--baseline" in args
    pages, live, templates = build_pages(only or None)
    live_set = set(live)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    out = BASELINE if baseline else os.path.join(CACHE, ts)
    rejudge = opt(args, "--rejudge")      # judge an earlier run's browser results again (no browser run)
    if rejudge:
        out = rejudge if os.path.isabs(rejudge) else os.path.join(ROOT, rejudge); ts = os.path.basename(out.rstrip("/"))
        job0 = json.load(open(os.path.join(out, "job.json"))); pages = job0["pages"]; sections = job0["sections"]
    os.makedirs(out, exist_ok=True)
    divit_targets = {}
    if not baseline and "divit" in sections and not rejudge:
        fh, ft = HUBS[0], templates.get(HUBS[0])
        divit_targets = {fh: [["hub-carousel", ".section_build"]]}
        if ft: divit_targets[ft] = [["template-carousel", ".section_build"], ["template-learn", ".section_blog-related"]]
        q = quiz_pages()
        if q: divit_targets[q[0]] = [["quiz", ".emgq-mount"]]
        for p in pages:
            if p["url"] in divit_targets: p["divit"] = divit_targets[p["url"]]
    job = {"base": base, "out": out, "pages": pages, "sections": sections, "baseline": baseline, "concurrency": conc,
           "shots": os.path.join(out, "shots") if (baseline or "pixel" in sections) else "", "divit": os.path.join(out, "divit") if divit_targets else ""}
    if baseline: job["shots"] = out
    jp = os.path.join(out, "job.json")
    if not rejudge: json.dump(job, open(jp, "w"), indent=1)
    print(f"staging check{' (baseline capture)' if baseline else ''}: {base}, {len(pages)} pages -> {os.path.relpath(out, ROOT)}", flush=True)
    rc = 0 if rejudge else run_node(jp)
    R = {}
    for p in pages:
        f = os.path.join(out, "pages", p["key"] + ".json")
        R[p["url"]] = json.load(open(f)) if os.path.exists(f) else {"url": p["url"], "fatal": "no result", "widths": {}, "console": []}
    if baseline:
        meta = {"captured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "base": base, "mask": "header/navbar box (rows) and section_footer, applied at diff time", "pages": {}}
        old = os.path.join(BASELINE, "meta.json")
        if os.path.exists(old) and only: meta["pages"] = json.load(open(old)).get("pages", {})
        absent = [p["url"] for p in pages if R[p["url"]].get("not_present")]   # quiz pages not on staging yet: nothing to capture
        for p in pages:
            ws = R[p["url"]].get("widths", {})
            if p["url"] not in absent: meta["pages"][p["key"]] = {"url": p["url"], **{w: ws[w].get("shot_sections") for w in ws if ws[w].get("shot_sections")}}
        json.dump(meta, open(old, "w"), indent=1)
        keys = {p["key"] for p in pages if p["url"] not in absent}
        n = sum(len([w for w in v if w.isdigit()]) for k, v in meta["pages"].items() if k in keys)
        mins = (time.time() - t0) / 60
        print(f"baseline: {n} screenshots ({len(keys)} pages x 390/1440) in {mins:.1f} min -> {os.path.relpath(BASELINE, ROOT)}; node exit {rc}"
              + (f"; not present on staging (skipped): {', '.join(absent)}" if absent else ""))
        return 0 if rc == 0 and n == 2 * len(keys) else 1

    # ---- judge
    import console_filter as CF
    csources = CF.load_sources(); ign_rows, n_counted = [], 0
    check_links, link_status = link_checker(base) if "links" in sections else (None, None)
    order, dates = [], {}
    if "learn" in sections:
        try:
            import urllib.request
            order, dates = learn_order(urllib.request.urlopen(urllib.request.Request(base + "/learn", headers={"User-Agent": "Mozilla/5.0 (emergent-hubs staging check)"}), timeout=30).read().decode("utf-8", "replace"))
        except Exception as e: print("could not read /learn:", e)
    bmeta = json.load(open(os.path.join(BASELINE, "meta.json"))) if os.path.exists(os.path.join(BASELINE, "meta.json")) else None
    hub_counts = {h: sum(1 for u in live if hub_of(u) == h) for h in HUBS}
    rows = []
    for p in pages:
        r = R[p["url"]]; W = r.get("widths", {}); C = {}
        g = W.get("1440") or {}
        if p["kind"] == "quiz" and (r.get("not_present") or g.get("status") == 404):
            C["present"] = (None, f"not present on staging (HTTP {g.get('status')}); the quiz pages ship after the canary")
            rows.append((p, C, r)); continue
        C["http200"] = (all((W.get(w) or {}).get("status") == 200 for w in W) and bool(W) and not r.get("fatal"),
                        r.get("fatal") or ", ".join(f"{w}: {(W[w] or {}).get('status')} {(W[w] or {}).get('error') or ''}".strip() for w in W if (W[w] or {}).get("status") != 200))
        if not C["http200"][0]: rows.append((p, C, r)); continue
        css = [w for w in W if "stylesheet" in ((W[w] or {}).get("error") or "")]
        C["styles_loaded"] = (not css, "a stylesheet did not load at " + ", ".join(css) + " px (after 2 reloads)" if css else "")
        if "console" in sections:   # only Divit's 2026-10-14 source exception applies (ops/console_filter.py); any other error fails
            errs = r.get("console") or []
            counted, ign = CF.split(errs, csources)
            uniq = sorted({f"{e['t']} [source {e.get('src') or '?'}]" for e in counted})
            C["console"] = (not counted, f"{len(uniq)} unique: " + " | ".join(u[:160] for u in uniq[:4]) if counted else "")
            pagesrc = lambda x: "this page (inline markup or script)" if x and urlsplit(x).path.rstrip("/") == p["url"] and urlsplit(x).hostname == urlsplit(base).hostname else x
            r["_console_raw"] = sorted({(e["t"], pagesrc(e.get("src") or "")) for e in errs})
            ign_rows += [(p["url"], n, e) for n, e in ign]; n_counted += len(counted)
        if "header" in sections:
            hd = [w for w in ("1440", "390") if not (W.get(w) or {}).get("header")]
            C["header"] = (not hd, "no visible header/navbar at " + ", ".join(hd) if hd else "")
        if "links" in sections:
            hp = os.path.join(out, "html", p["key"] + ".html")
            if os.path.exists(hp):
                extra = ((W.get("1440") or {}).get("carousel") or {}).get("load_more", {}).get("all_hrefs") or []
                ok, fl, n = check_links(open(hp).read(), p["url"], extra)
                C["links"] = (ok, f"{len(fl)} of {n} failing: " + "; ".join(fl[:5]) + (f" (+{len(fl) - 5})" if len(fl) > 5 else "") if fl else "")
            else: C["links"] = (False, "no rendered HTML saved")
        if "faq" in sections:
            cut = [f"{w}px Q{x['i']} cut {x['cut']}px{' (inner scroll)' if x['scroll'] else ''} in .{x['cls']}" for w in ("1440", "390") for x in (W.get(w) or {}).get("faq_clip") or [] if x["cut"] > 1]
            noq = not any((W.get(w) or {}).get("faq_clip") for w in ("1440", "390"))
            C["faq_clip"] = (not cut, "; ".join(cut[:5]) if cut else ("no FAQ accordion found" if noq else ""))
        if "emptyp" in sections:
            ep = (W.get("1440") or {}).get("empty_p") or []
            C["empty_p"] = (not ep, "; ".join(f"in {e['section']} after {e['after'][:40]!r} ({e['raw']})" for e in ep[:4]))
        if "meta" in sections:
            og = g.get("og_image") or ""
            st = link_status(og)[0] if (og and link_status) else None
            C["og_image"] = (bool(og) and (st == 200 if link_status else True), f"og:image {'missing' if not og else og[-60:] + ' HTTP ' + str(st)}" if not og or st != 200 else "")
            ok, d, warn = judge_jsonld(g.get("jsonld") or [], g.get("faq_questions") or [])
            C["jsonld"] = (ok, d if not ok else ""); r["_jsonld_note"] = d if ok else ""
            if warn: C["jsonld_entities"] = (None, warn)
        if "carousel" in sections and p["carousel"]:
            for w in WIDTHS_CAROUSEL:
                for name, (ok, d) in judge_carousel((W.get(str(w)) or {}).get("carousel"), p["hub"], live_set, hub_counts.get(p["hub"])).items():
                    C[f"carousel.{name}@{w}"] = (ok, d)
            if link_status:   # every card href answers 200 (also covered by the links check; listed here per carousel)
                hs = ((W.get("1440") or {}).get("carousel") or {}).get("load_more", {}).get("all_hrefs") or []
                bad = [h for h in hs if h and not href_problem(h) and link_status(base + (urlsplit(h).path if "://" in h else h))[0] != 200]
                if hs: C["carousel.card_href_200"] = (not bad, "not 200: " + ", ".join(bad[:5]) if bad else f"{len(hs)} card hrefs 200")
        if "learn" in sections and p["learn"]:
            for w in ("1440", "390"):
                for name, (ok, d) in judge_learn((W.get(w) or {}).get("learn"), order, dates).items():
                    C[f"learn.{name}@{w}"] = (ok, d)
            if link_status:
                cards = (((W.get("1440") or {}).get("learn") or {}).get("cards") or [])
                bad = [c.get("href") for c in cards if link_status(base + urlsplit(c.get("abs") or "").path)[0] != 200]
                if cards: C["learn.links_200"] = (not bad, "not 200: " + ", ".join(map(str, bad)) if bad else "")
        if "quiz" in sections and p["kind"] == "quiz":
            for w in ("390", "1280"):
                q = (W.get(w) or {}).get("quiz")
                if not q: C[f"quiz@{w}"] = (False, "no playthrough result"); continue
                C[f"quiz@{w}"] = (q.get("present") and not q.get("error") and not q.get("fails"), q.get("error") or (f"{len(q['fails'])} of {q.get('checks')} checks failed: " + " | ".join(q["fails"][:4]) if q.get("fails") else f"{q.get('checks')} checks passed ({q.get('type')}, {q.get('questions')} questions, {q.get('results')} results)"))
        if "pixel" in sections:
            if not bmeta or p["key"] not in bmeta.get("pages", {}): C["pixel"] = (None, "no baseline for this page")
            else:
                found = []
                for w in ("1440", "390"):
                    bm, cm = bmeta["pages"][p["key"]].get(w), (W.get(w) or {}).get("shot_sections")
                    if not bm or not cm: found.append({"section": "*", "status": "missing", "w": w}); continue
                    for f in diff_page(p["key"], w, bm, cm, BASELINE, os.path.join(out, "shots"), os.path.join(out, "diff"), threshold, expect):
                        f["w"] = w; found.append(f)
                r["_pixel"] = found
                hard = [f for f in found if not f.get("expected") and f["status"] not in ("added",)]
                C["pixel"] = (not hard, "; ".join(f"{f['w']}px {f['section']} {f['status']}{' ' + str(f.get('share')) if f.get('share') else ''}{' ' + f['detail'] if f.get('detail') else ''}" for f in hard[:5]))
        rows.append((p, C, r))
    # ---- report
    runtime = time.time() - t0
    fail_pages = [(p, C) for p, C, r in rows if any(v[0] is False for v in C.values())]
    by_check = {}
    for p, C, r in rows:
        for k, (ok, d) in C.items():
            kk = re.sub(r"@\d+$", "", k); s = by_check.setdefault(kk, [0, 0, 0]); s[0 if ok else 1 if ok is False else 2] += 1
    L = [f"# Staging check {ts}", "", f"- Base: {base}", f"- Pages: {sum(1 for p in pages if p['kind'] == 'child')} child pages (live), {sum(1 for p in pages if p['kind'] == 'hub')} hubs, {sum(1 for p in pages if p['kind'] == 'quiz')} quiz canary pages",
         f"- Template pages (carousel and Learn): {', '.join(templates.get(h, '-') for h in HUBS)}",
         f"- Sections: {', '.join(sections)}", f"- Runtime: {runtime / 60:.1f} min (concurrency {conc})",
         f"- Baseline: {bmeta['captured_at'] + ' (' + bmeta['base'] + ')' if bmeta else 'none'}", f"- Result: **{len(fail_pages)} page(s) with a failing check**", "",
         "## Checks", "", "| check | pass | fail | info |", "|---|---|---|---|"]
    L += [f"| {k} | {v[0]} | {v[1]} | {v[2]} |" for k, v in sorted(by_check.items())]
    L += ["", "## Failures", ""]
    for p, C in fail_pages:
        L.append(f"### {p['url']} ({p['kind']})")
        L += [f"- **{k}**: {d}" for k, (ok, d) in C.items() if ok is False]
        L.append("")
    if not fail_pages: L += ["None.", ""]
    L += ["## Notes (info, not failures)", ""]
    for p, C, r in rows:
        for k, (ok, d) in C.items():
            if ok is None: L.append(f"- {p['url']} {k}: {d}")
    L += ["", "## Carousel and Learn (template pages and hubs)", ""]
    for p, C, r in rows:
        if not p["carousel"]: continue
        L.append(f"- {p['url']}: " + ", ".join(f"{k} {'ok' if ok else 'FAIL' if ok is False else 'info'}" for k, (ok, d) in C.items() if k.startswith(("carousel", "learn"))))
    raw = {}
    for p, C, r in rows:
        for t, src in r.get("_console_raw") or []: raw.setdefault((t, src), []).append(p["url"])
    cline = CF.summary_line(n_counted, [(n, e) for _u, n, e in ign_rows]) if "console" in sections else ""
    L += ["", "## Console errors", "", cline, "", "Every error captured (error level, with its source), counted unless Divit's 2026-10-14 exception covers its source:", ""]
    ign_keys = {(e["t"], e.get("src") or "") for _u, _n, e in ign_rows}
    L += [f"- {len(set(v))} page(s){' (ignored by the exception)' if (t, src) in ign_keys else ''}: `{t[:160]}` (source {src[:100] or '?'})" for (t, src), v in sorted(raw.items(), key=lambda x: -len(set(x[1])))[:30]] or ["None."]
    L += ["", "Ignored by the exception (page, message, source):", ""] + (CF.ignored_lines(ign_rows[:200]) or ["None."])
    L += ["", "## Pixel diff (per section; header rows and footer masked)", ""]
    anyd = False
    for p, C, r in rows:
        for f in r.get("_pixel") or []:
            anyd = True; L.append(f"- {p['url']} {f['w']}px {f['section']}: {f['status']}{' share ' + str(f['share']) if f.get('share') else ''}{' ' + f['detail'] if f.get('detail') else ''}{' (expected: the run changes this section)' if f.get('expected') else ''}{' -> ' + f['image'] if f.get('image') else ''}")
    if not anyd: L.append("No section differs from the baseline above the threshold." if bmeta else "No baseline (run --baseline first).")
    if divit_targets or any(r.get("divit") for _p, _C, r in rows):
        L += ["", "## Screenshots for Divit (true size, deviceScaleFactor 1, first carousel page before Load more)", ""]
        for p, C, r in rows:
            for k, v in (r.get("divit") or {}).items(): L.append(f"- {p['url']} {k}: {'divit/' + v if v else 'not rendered (section hidden or page not present)'}")
    rp = os.path.join(out, "report.md"); open(rp, "w").write("\n".join(L) + "\n")
    json.dump({"base": base, "ts": ts, "runtime_s": round(runtime), "pages": [{"url": p["url"], "kind": p["kind"], "checks": {k: {"ok": ok, "detail": d} for k, (ok, d) in C.items()}} for p, C, r in rows]},
              open(os.path.join(out, "summary.json"), "w"), indent=1)
    print(f"\n{base}: {len(rows)} pages checked in {runtime / 60:.1f} min; {len(fail_pages)} with a failing check")
    if cline: print("  " + cline)
    for k, v in sorted(by_check.items()):
        if v[1]: print(f"  FAIL {k}: {v[1]} result(s) (page x width)")
    quiz_np = [p["url"] for p, C, r in rows if p["kind"] == "quiz" and "present" in C]
    if quiz_np: print(f"  quiz pages not present on staging: {', '.join(quiz_np)}")
    print(f"report: {os.path.relpath(rp, ROOT)}")
    return 1 if fail_pages or rc else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
