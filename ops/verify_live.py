"""After publish: does the live page render exactly what was approved?
Checks the <title>, meta description, H1, the FAQ data, every image (by Webflow file ID), the share image, that every
emergent.sh link in the FAQ answers returns HTTP 200, and (Divit 2026-10-14) every internal href on the whole page, template
links included (carousel and Learn cards, nav, footer, breadcrumbs, CTAs, hub links): each must end in HTTP 200 after its
redirects, and no card may carry a placeholder href ("#") or a template-page slug (/<hub>/detail_<collection>). Divit 2026-10-16: the Learn
section (section_blog-related) shows exactly 3 cards linking to /learn/<slug>, with no "No items found".
Fetches https://emergent.sh<url> unless an HTML file is given.

    .venv/bin/python3 ops/verify_live.py --links URL_OR_PATH ...     internal-link check only, any emergent.sh page (hubs too)"""
import json, re, sys, time, urllib.request, urllib.error
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urlunsplit

def _get(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "Mozilla/5.0 (emergent-hubs verify)"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.status, r.read().decode("utf-8", "replace") if method == "GET" else ""

# ---- every internal href on the page (Divit 2026-10-14: a teammate's site publish shipped 404 Learn card links) ----
INTERNAL_HOSTS = {"emergent.sh", "www.emergent.sh"}
BASE = "https://emergent.sh"
# href="#" is the site's own JS-button pattern (sign-up modal, auth buttons): those anchors carry one of these attributes.
# A "#" (or empty) href without one of them is a card or CTA link that goes nowhere.
JS_BUTTON_ATTRS = ("dom-item", "data-auth")
TEMPLATE_SLUG = re.compile(r"(^|/)detail_[^/]*$")   # Webflow template page slug (detail_learn, detail_build, ...) in a link
SKIP_PATHS = ("/cdn-cgi/",)                          # Cloudflare's mailto obfuscation (__cf_email__) and challenge paths
RATE = 0.15                                          # seconds between requests (polite: about 6 per second)
RETRIES = 3
LINK_CACHE = {}                                      # url -> (final code, chain); shared across pages in one run
_last = [0.0]

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
_opener = urllib.request.build_opener(_NoRedirect)

def fetch_once(url, method="HEAD"):
    """One request, no redirect following. Returns (status, Location or None); raises on a network error."""
    wait = RATE - (time.time() - _last[0])
    if wait > 0: time.sleep(wait)
    _last[0] = time.time()
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "Mozilla/5.0 (emergent-hubs verify)"})
    try:
        with _opener.open(req, timeout=30) as r: return r.status, r.headers.get("Location")
    except urllib.error.HTTPError as e: return e.code, e.headers.get("Location") if e.headers else None

def link_status(url, fetch=None):
    """Final status of url after redirects (max 5 hops) and the chain [(url, status), ...]. HEAD first, GET when HEAD is refused;
    network errors, 429 and 5xx are retried with a pause and never cached (one bad probe must not fail a page). A stub fetch
    (tests) bypasses the cache and the pauses."""
    live = fetch is None; fetch = fetch or fetch_once
    if live and url in LINK_CACHE: return LINK_CACHE[url]
    chain, cur = [], url
    for _hop in range(6):
        for a in range(RETRIES):
            try:
                code, loc = fetch(cur, "HEAD")
                if code in (403, 405, 501): code, loc = fetch(cur, "GET")
            except Exception as e:
                code, loc = f"network error: {str(e)[:80]}", None
            if isinstance(code, int) and code != 429 and code < 500: break
            if live and a < RETRIES - 1: time.sleep(2 * (a + 1))
        chain.append((cur, code))
        if isinstance(code, int) and 300 <= code < 400 and loc:
            cur = urljoin(cur, loc); continue
        break
    final = chain[-1][1]
    if live and isinstance(final, int) and final != 429 and final < 500: LINK_CACHE[url] = (final, chain)
    return final, chain

class _Anchors(HTMLParser):
    """Every <a> in the document (script and style bodies are not parsed as markup), with cheap context: the class of the
    section it sits in, its own class and the start of its text."""
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out, self._sec, self._a = [], [], None
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "section": self._sec.append((d.get("class") or "").split(" ")[0])
        if tag == "a":
            self._a = {"href": d.get("href"), "attrs": d, "section": self._sec[-1] if self._sec else "", "text": ""}
            self.out.append(self._a)
    def handle_endtag(self, tag):
        if tag == "section" and self._sec: self._sec.pop()
        if tag == "a": self._a = None
    def handle_data(self, data):
        if self._a is not None and len(self._a["text"]) < 60: self._a["text"] = (self._a["text"] + " " + data.strip()).strip()

def _ctx(a):
    cls = (a["attrs"].get("class") or "").split(" ")[0]
    return f'{a["section"] or "-"} > a.{cls or "-"} "{a["text"][:40]}"'

def internal_links(html, page_url):
    """Collect the page's internal hrefs. Returns (targets {absolute url: [anchors]}, placeholders [anchors], slugs [anchors])."""
    p = _Anchors(); p.feed(html); p.close()
    targets, placeholders, slugs = {}, [], []
    for a in p.out:
        h = a["href"]
        if h is None: continue
        h = h.strip()
        if h in ("", "#"):
            if not any(k in a["attrs"] for k in JS_BUTTON_ATTRS): placeholders.append(a)
            continue
        if h.startswith("#") or re.match(r"(?i)(mailto|tel|javascript|sms|data):", h): continue
        u = urlsplit(urljoin(page_url, h))
        if u.scheme not in ("http", "https") or u.hostname not in INTERNAL_HOSTS: continue
        if any(u.path.startswith(x) for x in SKIP_PATHS): continue
        if TEMPLATE_SLUG.search(u.path): slugs.append(dict(a, url=u.path)); continue   # fails as it stands, no request needed
        target = urlunsplit(("https", "emergent.sh", u.path or "/", u.query, ""))
        targets.setdefault(target, []).append(a)
    return targets, placeholders, slugs

def check_internal_links(html, page_url, fetch=None):
    """Every internal href on the page: (ok, report lines, failing hrefs). fetch(url, method) -> (status, location) is the single
    request; tests pass a stub so the golden suite stays offline."""
    targets, placeholders, slugs = internal_links(html, page_url)
    rep, bad = [], []
    for a in placeholders:
        rep.append(f'FAIL internal link placeholder href="{a["href"]}" (a card or CTA that goes nowhere): {_ctx(a)}'); bad.append(a["href"] or '""')
    for a in slugs:
        rep.append(f'FAIL internal link to a template page slug {a["url"]}: {_ctx(a)}'); bad.append(a["url"])
    redirected = failed = 0
    for t, anchors in sorted(targets.items()):
        code, chain = link_status(t, fetch)
        path = urlsplit(t).path + (("?" + urlsplit(t).query) if urlsplit(t).query else "")
        if code == 200:
            redirected += len(chain) > 1; continue
        failed += 1
        via = (" via " + " -> ".join(f"{urlsplit(u).path} {c}" for u, c in chain)) if len(chain) > 1 else ""
        rep.append(f"FAIL internal link {path}: HTTP {code}{via} ({len(anchors)} anchor(s); first: {_ctx(anchors[0])})")
        bad.append(path)
    n_a = sum(len(v) for v in targets.values())
    ok = not bad
    head = (f"internal links: {len(targets)} unique href(s) from {n_a} anchor(s), {len(targets) - failed} answer 200 ({redirected} after a "
            f"redirect), {failed} do not; {len(placeholders)} placeholder href(s); {len(slugs)} template-slug link(s)")
    return ok, [("PASS " if ok else "FAIL ") + head] + rep, bad

LEARN_CARD = re.compile(r"^(?:https?://(?:www\.)?emergent\.sh)?/learn/[a-z0-9][a-z0-9-]*/?$")
def learn_section(html):
    """Divit 2026-10-16: the template's Learn list (section_blog-related) sources the item's own acrm---learn refs, limit 3. It must show
    exactly 3 cards (role=listitem), each linking to /learn/<slug>, and no Webflow empty state ("No items found"). Returns (ok, line)."""
    m = re.search(r'<section[^>]*class="section_blog-related[^"]*"[^>]*>(.*?)</section>', html, re.S)
    if not m: return False, "FAIL Learn section: section_blog-related not on the page"
    sec = m.group(1); why = []
    cards = re.findall(r'<div[^>]*role="listitem"[^>]*>(.*?)(?=<div[^>]*role="listitem"|</section>|$)', sec, re.S)
    hrefs = [(re.search(r'<a[^>]*href="([^"]*)"', c) or [None, None])[1] for c in cards]
    if "No items found" in sec or "w-dyn-empty" in sec and re.search(r'class="[^"]*w-dyn-empty[^"]*"[^>]*>\s*<div', sec): why.append('"No items found" shown')
    if len(cards) != 3: why.append(f"{len(cards)} card(s), need 3")
    off = [h for h in hrefs if not (h and LEARN_CARD.match(h))]
    if off: why.append(f"{len(off)} card link(s) not /learn/<slug>: {', '.join(str(h) for h in off[:3])}")
    if why: return False, "FAIL Learn section (3 published acrm---learn refs): " + "; ".join(why)
    return True, "PASS Learn section: 3 cards to /learn/<slug>"

def _learn_hub(spec):
    import os as _os, sys as _sys; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__))); import hubctl as _H
    hub = next((k for k, h in _H.CFG["hubs"].items() if (spec.get("url") or "").startswith(h["path"] + "/")), None)
    return hub and _H.learn_from_item(hub)

def verify(spec, html=None, check_links=True, fetch=None):
    F = spec["fields"]; url = "https://emergent.sh" + spec["url"]; rep = []; ok = True
    if html is None:
        code, html = _get(url)
        if code != 200: return False, [f"FAIL {url} returned HTTP {code}"]
    def chk(name, cond, detail=""):
        nonlocal ok
        rep.append(("PASS " if cond else "FAIL ") + name + (f": {detail}" if detail and not cond else "")); ok = ok and cond
    import sys as _sy, os as _o; _sy.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import slugs as _SL, hubctl as _H0
    _sp = _SL.spec_problems(_H0.hub_of(spec["url"]), spec["url"], spec)   # PERMANENT SLUG RULE (Divit 2026-10-23)
    if _sp and _SL.migration_pending(): rep.append("PEND slug (migration pending): " + "; ".join(_sp))
    else: chk("slug (slugs.slug_for)", not _sp, "; ".join(_sp))
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    chk("title", t and unescape(t.group(1)).strip() == F["meta_title"], t.group(1)[:80] if t else "missing")
    d = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', html) or re.search(r'<meta[^>]+content="([^"]*)"[^>]+name="description"', html)
    chk("meta description", d and unescape(d.group(1)) == F["meta_description"], d.group(1)[:80] if d else "missing")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    chk("H1", h1 and unescape(re.sub(r"<[^>]+>", "", h1.group(1))).strip() == F["h1"], unescape(re.sub(r"<[^>]+>", "", h1.group(1)))[:80] if h1 else "missing")
    fq_live = re.search(r"window\.awbFAQ\s*=\s*(\{.*?\})\s*;\s*</script>", html, re.S)
    fq_spec = re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;\s*</script>", F.get("faq", ""), re.S)
    try:
        live_q = [i["q"] for i in json.loads(fq_live.group(1))["items"]] if fq_live else []
    except Exception: live_q = []
    want_q = [i["q"] for i in json.loads(fq_spec.group(1))["items"]] if fq_spec else []
    chk("FAQ questions", live_q == want_q, f"{len(live_q)} live vs {len(want_q)} approved")
    for k, im in spec.get("images", {}).items():
        if k == "cover_image": continue   # the cover renders only in the carousel (section_build), hidden on hubs and templates (Divit 2026-10-09)
        fid = im.get("file_id")
        chk(f"image {k}", bool(fid) and fid in html, "file id not found on the page" if fid else "no file id recorded")
    og = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html) or re.search(r'<meta[^>]+content="([^"]+)"[^>]+property="og:image"', html)
    sid = spec.get("images", {}).get("share_image", {}).get("file_id")
    chk("share image (og:image)", bool(og and sid and sid in og.group(1)), og.group(1)[:80] if og else "missing")
    if _learn_hub(spec):   # Divit 2026-10-16: rendered Learn list = 3 cards to /learn/<slug>, never "No items found"
        lok, lline = learn_section(html); rep.append(lline); ok = ok and lok
    if spec.get("quiz") is not None:   # playable quiz (docs/QUIZ.md): the hero prompt field (alpb---prompt) also carries window.awbQuiz
        import sys as _sys, os as _os; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "qc")); import quiz as _QZ
        import hubctl as _H
        want = _QZ.split_prompt(_H.export_fields(spec["url"], spec)[0].get("hero_prompt", ""))
        chk("hero prompt data (awbPrompt) with the quiz block", want["prompt"] is not None and _QZ.js_object(html, "awbPrompt") == want["prompt"], "window.awbPrompt missing or different from the approved default and chips")
        _t = lambda x: re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", x))).strip()
        chk("hero prompt text", bool(_t(want["p"])) and _t(want["p"]) in _t(html), "the hero prompt <p> text is not on the page")
        chk("quiz data", _QZ.from_block(html) == spec["quiz"], "window.awbQuiz missing or different from the approved quiz")
        chk("quiz embed", 'class="emgq-mount"' in html, "the template's quiz embed (emgq-mount) is not on the page")
    if check_links:
        # links as they ship: export_fields turns links to pages that are not live into plain text (link-to-live)
        import hubctl as _H
        shipped = _H.export_fields(spec["url"], spec)[0].get("faq", "")
        for href in sorted(set(re.findall(r"<a href=(?:\\\\?\"|')(https://emergent\.sh[^\"'\\\\]*)", shipped))):
            code, _chain = link_status(href.split("#")[0], fetch)
            chk(f"link {href}", code == 200, f"HTTP {code}")
        # every internal href on the rendered page, template links included (Divit 2026-10-14)
        lok, lrep, _bad = check_internal_links(html, url, fetch)
        rep.extend(lrep); ok = ok and lok
    return ok, rep

def main(argv):
    if "--links" not in argv: sys.exit(__doc__)
    fails = 0
    for x in [a for a in argv if a != "--links"]:
        url = x if x.startswith("http") else BASE + x
        code, html = _get(url)
        if code != 200: print(f"FAIL {url} returned HTTP {code}"); fails += 1; continue
        ok, rep, _ = check_internal_links(html, url)
        print(url); print("\n".join("  " + l for l in rep)); fails += not ok
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main(sys.argv[1:])
