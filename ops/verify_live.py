"""After publish: does the live page render exactly what was approved?
Checks the <title>, meta description, H1, the FAQ data, every image (by Webflow file ID), the share image, and that every
emergent.sh link in the FAQ answers returns HTTP 200. Fetches https://emergent.sh<url> unless an HTML file is given."""
import json, re, urllib.request
from html import unescape

def _get(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "Mozilla/5.0 (emergent-hubs verify)"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.status, r.read().decode("utf-8", "replace") if method == "GET" else ""

def verify(spec, html=None, check_links=True):
    F = spec["fields"]; url = "https://emergent.sh" + spec["url"]; rep = []; ok = True
    if html is None:
        code, html = _get(url)
        if code != 200: return False, [f"FAIL {url} returned HTTP {code}"]
    def chk(name, cond, detail=""):
        nonlocal ok
        rep.append(("PASS " if cond else "FAIL ") + name + (f": {detail}" if detail and not cond else "")); ok = ok and cond
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
    if check_links:
        # links as they ship: export_fields turns links to pages that are not live into plain text (link-to-live)
        import hubctl as _H
        shipped = _H.export_fields(spec["url"], spec)[0].get("faq", "")
        for href in sorted(set(re.findall(r"<a href=(?:\\\\?\"|')(https://emergent\.sh[^\"'\\\\]*)", shipped))):
            try: code, _ = _get(href, "HEAD")
            except Exception as e: code = getattr(e, "code", str(e))
            chk(f"link {href}", code == 200, f"HTTP {code}")
    return ok, rep
