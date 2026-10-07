"""Rendered widths of page text in the child template's real typography.

The template sets headings in Brockmann and body text in Inter (read from the site's Webflow typography variables,
2026-10-07: H1 3rem / -2px, H2 2.25rem / -0.04em weight 500, H3 1.75rem, text-size-medium 1.125rem, regular 1rem).
Each field's text is shaped with HarfBuzz (kerning on) in its font, size and tracking, and compared with a ceiling:
the widest rendering of that field across the four approved live child pages. Nothing new may render wider than
something Divit has already approved in this template.

  python3 ops/typeset.py calibrate     # recompute ceilings from the approved pages (writes config/typography.json)
  python3 ops/typeset.py fonts         # which fonts are available (Brockmann needs pipeline/assets.py with CDN access)

Brockmann is a licensed font: fetched into .cache/fonts/brockmann (git-ignored), never committed. Without it,
headings are measured in Inter and the ceilings for that mode are used (exact for body text, approximate for headings).
"""
import json, os, re, sys, glob
from html import unescape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from paths import FONT_DIR, CACHE
CFG_P = os.path.join(ROOT, "config", "typography.json")
BROCK = os.path.join(CACHE, "fonts", "brockmann")
INTER_W = {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold", 800: "ExtraBold"}
BROCK_W = {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold"}

# role -> (family, weight, size px, letter-spacing px or em string)
ROLES = {
 "h1":        ("heading", 500, 48, "-2px"),
 "h2":        ("heading", 500, 36, "-0.04em"),
 "h3":        ("heading", 500, 28, "0px"),
 "card-title":("heading", 500, 20, "0px"),
 "lead":      ("body", 400, 18, "0px"),
 "body":      ("body", 400, 16, "0px"),
 "label":     ("body", 500, 16, "0px"),
}
# logical field -> role (repeated fields are measured per item)
FIELDS = {
 "h1": "h1", "hero_description": "lead", "features_heading": "h2", "features_subheading": "lead",
 "feature_title": "card-title", "feature_body": "body", "usecase_heading": "h2", "tab_label": "label",
 "tab_title": "h3", "tab_body": "body", "howto_title": "h2", "howto_description": "lead", "howto_step_title": "card-title",
 "howto_step_des": "body", "why_title": "h2", "why_description": "lead", "faq_heading": "h2", "faq_q": "card-title",
 "faq_a": "body", "prompt_chip": "label", "breadcrumb": "label", "explore_cta": "label",
}
_hb = {}
def mode():
    return "brockmann" if all(os.path.exists(os.path.join(BROCK, f"Brockmann-{n}.ttf")) for n in BROCK_W.values()) else "inter"
def _font(family, weight, md):
    import uharfbuzz as hb
    if family == "heading" and md == "brockmann":
        w = min(BROCK_W, key=lambda k: abs(k - weight)); path = os.path.join(BROCK, f"Brockmann-{BROCK_W[w]}.ttf")
    else:
        w = min(INTER_W, key=lambda k: abs(k - weight)); path = os.path.join(FONT_DIR, f"Inter-{INTER_W[w]}.ttf")
    if path not in _hb:
        face = hb.Face(hb.Blob.from_file_path(path)); _hb[path] = (hb.Font(face), face.upem)
    return _hb[path]
def width(text, role, md=None):
    import uharfbuzz as hb
    md = md or mode(); family, weight, size, ls = ROLES[role]
    f, upem = _font(family, weight, md)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(f, buf, {"kern": True, "liga": True})
    adv = sum(p.x_advance for p in buf.glyph_positions) * size / upem
    lsp = float(ls[:-2]) * size if ls.endswith("em") else float(ls[:-2])
    return adv + lsp * max(len(text) - 1, 0)
def missing_glyphs(text, role, md=None):
    md = md or mode(); family, weight, _, _ = ROLES[role]
    from fontTools.ttLib import TTFont
    path = (os.path.join(BROCK, f"Brockmann-{BROCK_W[min(BROCK_W, key=lambda k: abs(k - weight))]}.ttf") if family == "heading" and md == "brockmann"
            else os.path.join(FONT_DIR, f"Inter-{INTER_W[min(INTER_W, key=lambda k: abs(k - weight))]}.ttf"))
    key = ("cmap", path)
    if key not in _hb: _hb[key] = set(TTFont(path).getBestCmap())
    return sorted({c for c in text if ord(c) not in _hb[key] and not c.isspace()})

def _txt(h): return unescape(re.sub(r"<[^>]+>", " ", h or "")).replace('\\"', '"').strip()
def _h3p(h):
    m = re.search(r"<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>", h or "", re.S)
    return (_txt(m.group(1)), _txt(m.group(2))) if m else (None, None)
def texts(spec):
    """field -> list of rendered strings for one spec."""
    F = spec["fields"]; out = {k: [] for k in FIELDS}
    for k in ("h1", "hero_description", "features_heading", "features_subheading", "usecase_heading", "howto_title", "howto_description", "why_title", "why_description", "breadcrumb", "explore_cta"):
        if F.get(k): out[k].append(_txt(F[k]))
    for i in range(1, 7):
        t, b = _h3p(F.get(f"feature_{i}"))
        if t: out["feature_title"].append(t); out["feature_body"].append(b)
    for i in range(1, 5):
        if F.get(f"tab_label_{i}"): out["tab_label"].append(F[f"tab_label_{i}"])
        if F.get(f"prompt_chip_{i}"): out["prompt_chip"].append(F[f"prompt_chip_{i}"])
        t, b = _h3p(F.get(f"tab_content_{i}"))
        if t: out["tab_title"].append(t); out["tab_body"].append(b)
    for i in range(1, 8):
        if F.get(f"howto_step_{i}_title"): out["howto_step_title"].append(F[f"howto_step_{i}_title"])
        if F.get(f"howto_step_{i}_des"): out["howto_step_des"].append(F[f"howto_step_{i}_des"])
    m = re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;\s*</script>", F.get("faq", ""), re.S)
    if m:
        fq = json.loads(m.group(1)); out["faq_heading"].append(fq.get("heading", ""))
        for it in fq.get("items", []): out["faq_q"].append(it["q"]); out["faq_a"].append(_txt(it["a"]))
    return out
def calibrate():
    approved = [json.load(open(p)) for p in glob.glob(os.path.join(ROOT, "specs", "*", "*.json"))
                if json.load(open(p)).get("status") in ("live-draft", "published") or json.load(open(p)).get("render_verified")]
    cfg = json.load(open(CFG_P)) if os.path.exists(CFG_P) else {}
    md = mode(); ceil = {}
    for f, role in FIELDS.items():
        ws = [(width(t, role, md), t, s["url"]) for s in approved for t in texts(s)[f] if t]
        if ws:
            w, t, u = max(ws); ceil[f] = {"px": round(w, 1), "from": u, "text": t[:80], "samples": len(ws)}
    cfg.update({"_note": __doc__.split("\n\n")[1].replace("\n", " "), "roles": ROLES, "fields": FIELDS})
    cfg.setdefault("ceilings", {})[md] = {"calibrated_on": "4 approved live child pages", "fields": ceil}
    json.dump(cfg, open(CFG_P, "w"), indent=1, ensure_ascii=False)
    print(f"calibrated {len(ceil)} fields in {md} mode from {len(approved)} approved pages -> {os.path.relpath(CFG_P, ROOT)}")
def check(spec):
    """[(severity, field, message)] for text that renders wider than the approved ceiling, or uses glyphs the font lacks."""
    if not os.path.exists(CFG_P): return [("P2", "typography", "no ceilings yet: run python3 ops/typeset.py calibrate")]
    cfg = json.load(open(CFG_P)); md = mode(); C = cfg.get("ceilings", {}).get(md)
    if not C: return [("P2", "typography", f"no ceilings for {md} mode: run python3 ops/typeset.py calibrate")]
    out = []
    for f, items in texts(spec).items():
        if f not in C["fields"]: continue
        lim = C["fields"][f]["px"]; role = FIELDS[f]
        for t in items:
            w = width(t, role, md)
            if w > lim + 0.5 and f in ("breadcrumb", "explore_cta"):
                out.append(("P2", f, f'keyword-length field renders {w:.0f}px, beyond the widest approved ({lim:.0f}px): confirm it in the template render (it cannot be shorter than the keyword)')); continue
            if w > lim + 0.5: out.append(("P1", f, f'renders {w:.0f}px in the template\'s {role} type, wider than anything approved ({lim:.0f}px, {C["fields"][f]["from"].rsplit("/",1)[1]}): "{t[:50]}"'))
            elif w > lim * 0.97: out.append(("P2", f, f'within 3% of the widest approved rendering ({w:.0f} of {lim:.0f}px): "{t[:40]}"'))
            mg = missing_glyphs(t, role, md)
            if mg: out.append(("P0", f, f"characters the template font cannot draw: {mg}"))
    if md == "inter": out.append(("P2", "typography", "headings measured in Inter (Brockmann not fetched on this machine); exact on the production Mac"))
    return out

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "calibrate": calibrate()
    elif a and a[0] == "fonts": print("mode:", mode(), "| Inter:", FONT_DIR, "| Brockmann:", BROCK if mode() == "brockmann" else "not fetched")
    else: print(__doc__)
