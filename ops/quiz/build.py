"""build.py: the playable-quiz embed's build and test pages (docs/QUIZ.md).

    python3 ops/quiz/build.py            write ops/quiz/embed.min.html from ops/quiz/embed.html, check its CSS selectors,
                                         and write the harness pages to .cache/quiz/ (used by ops/quiz/test_embed.mjs)

The minified copy is what goes into the Webflow HTML Embed (smaller; same code). Minifying only removes comments, indentation
and spaces around CSS punctuation, line by line, so the JavaScript keeps its line breaks and never depends on a parser.
The selector check fails the build if any CSS rule targets anything but the embed's own .emgq classes.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "qc"))
import quiz as Z
SRC = os.path.join(ROOT, "ops", "quiz", "embed.html")
MIN = os.path.join(ROOT, "ops", "quiz", "embed.min.html")
OUT = os.path.join(ROOT, ".cache", "quiz")

def minify(html):
    html = re.sub(r"<!--.*?-->\s*", "", html, flags=re.S)
    def css(m):
        c = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
        c = re.sub(r"\s+", " ", c)
        c = re.sub(r"\s*([{};:,>])\s*", r"\1", c).replace(";}", "}")
        return "<style>" + c.strip() + "</style>"
    html = re.sub(r"<style>(.*?)</style>", css, html, flags=re.S)
    def js(m):
        body = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
        lines = [l.strip() for l in body.split("\n")]
        return "<script>\n" + "\n".join(l for l in lines if l and not l.startswith("//")) + "\n</script>"
    html = re.sub(r"<script>(.*?)</script>", js, html, flags=re.S)
    return "\n".join(l for l in html.split("\n") if l.strip()) + "\n"

def selectors(html):
    """Every CSS selector in the embed's <style> (inside @media too)."""
    css = re.sub(r"/\*.*?\*/", "", "".join(re.findall(r"<style>(.*?)</style>", html, re.S)), flags=re.S)
    out = []
    for pre in re.findall(r"([^{}]+)\{", css):
        pre = pre.strip()
        if pre.startswith("@"): continue
        out += [s.strip() for s in pre.split(",") if s.strip()]
    return out

def bad_selectors(html):
    """Selectors that could touch anything outside the quiz: each compound must be one of the embed's own classes."""
    bad = []
    for s in selectors(html):
        for part in re.split(r"\s+|>|\+|~", s):
            if not part: continue
            if not re.fullmatch(r"(\.emgq(?:-[a-z0-9-]+)?)+(?::{1,2}[a-z-]+(?:\([^)]*\))?)*", part): bad.append(s); break
    return bad

def js_source(html):
    return re.search(r"<script>(.*?)</script>", html, re.S).group(1)

# Hostile base styles a site may carry (Webflow's normalize and typical global rules): the quiz must look the same under them.
HOSTILE = """<style>
body{margin:0;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:20px;color:#333;background:#fafafa}
h2{font-size:40px;line-height:48px;margin:20px 0 10px;font-weight:bold;color:#e11d48}
h3{font-size:30px;line-height:36px;margin:20px 0 10px;color:#e11d48}
p{margin:0 0 10px;color:#2563eb}
label{display:block;margin-bottom:5px;font-weight:bold;color:#7c3aed}
input[type=radio]{margin:4px 0 0;line-height:normal;width:40px;height:40px}
fieldset{border:3px solid #e11d48;margin:10px;padding:20px}
legend{font-size:30px;color:#e11d48}
button,[type=submit]{background:#16a34a;color:#000;border:0;padding:2px;border-radius:0}
section{padding:120px 0;background:#ddd}
ol{list-style:none;padding:0}
.probe{color:#7c3aed;font-weight:bold;margin-bottom:5px}
</style>"""

HERO_SPEC = "/ai-survey-and-quiz-builder/employee-engagement-survey"   # a live SurveyQuiz page with chip_adds: its real hero prompt export
def hero_value(quiz=None):
    """The alpb---prompt value exactly as hubctl exports it (<p> + awbPrompt block [+ the quiz block]) for a real SurveyQuiz spec."""
    sys.path.insert(0, os.path.join(ROOT, "ops")); import hubctl as H
    s = json.load(open(H.spath(HERO_SPEC)))
    if quiz is not None: s["quiz"] = quiz
    return H.export_fields(HERO_SPEC, s, live=set())[0]["hero_prompt"]
def hero_form():
    chips = "".join(f"<div data-hubchip='{i}' class='probe-chip'>Chip {i}</div>" for i in range(1, 5))
    return f"<form id='hero-prompt-form' onsubmit='return false'><textarea name='prompt' rows='3' style='width:100%;box-sizing:border-box'></textarea>{chips}</form>" + open(os.path.join(ROOT, "ops", "template", "hero-chips.html")).read()

def page(quiz_block, embed, title="Quiz harness", hostile=True, data_after=True, carrier_html=None):
    head = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title}</title>{HOSTILE if hostile else ''}</head><body>"
    hero = "<section class='probe-section'><h2 class='probe-h2'>Page heading</h2><p class='probe-p'>Hero copy.</p><label class='probe'>A site label</label>" + hero_form() + "</section>"
    # the carrier: the hero prompt field's hidden rich text (the template's own element); worst case: after the quiz embed
    if carrier_html is not None: carrier = f"<div class='w-richtext' style='display:none'>{carrier_html}</div>"
    else: carrier = f"<div class='w-richtext emgq-src'>{quiz_block}</div>" if quiz_block else ""
    body = hero + ("" if data_after else carrier) + f"<div class='w-embed'>{embed}</div>" + (carrier if data_after else "") + "<footer><p class='probe-foot'>Footer</p></footer>"
    return head + body + "</body></html>"

def main():
    src = open(SRC).read()
    bad = bad_selectors(src)
    if bad: sys.exit("CSS selectors outside .emgq classes: " + ", ".join(bad))
    mn = minify(src); open(MIN, "w").write(mn)
    os.makedirs(OUT, exist_ok=True)
    fx = {n: json.load(open(os.path.join(ROOT, "ops", "quiz", "fixtures", f"{n}.json"))) for n in ("knowledge", "matching")}
    pages = {}
    for variant, emb in (("full", src), ("min", mn)):
        for n, q in fx.items():
            pages[f"{n}-{variant}"] = page(None, emb, carrier_html=hero_value(q))
    pages["knowledge-before"] = page(None, mn, data_after=False, carrier_html=hero_value(fx["knowledge"]))
    pages["hero-noquiz"] = page(None, mn, carrier_html=hero_value(None))   # a non-quiz page: the hero must behave exactly as with a quiz
    pages["json-tag"] = page(None, mn).replace("<footer>", "<script type='application/json' id='emgq-data'>" + json.dumps(fx["matching"]).replace("<", "\\u003c") + "</script><footer>")
    pages["nodata"] = page(None, mn)
    pages["badjson"] = page(None, mn).replace("<footer>", "<script type='application/json' id='emgq-data'>{\"version\": 1, \"type\": </script><footer>")
    short = dict(fx["matching"]); short["questions"] = fx["matching"]["questions"][:5]
    pages["badschema"] = page(Z.embed_block(short), mn)
    evil = json.loads(json.dumps(fx["knowledge"]))
    evil["title"] = "<img src=x onerror=alert(1)> & <b>bold</b> </script><script>window.pwned=1</script>"
    evil["questions"][0]["text"] = "<a href='https://example.com/x'>link</a> question?"
    evil["questions"][0]["source"]["url"] = "javascript:alert(1)"
    pages["escape"] = page(Z.embed_block(evil), mn)
    for k, v in pages.items(): open(os.path.join(OUT, f"page-{k}.html"), "w").write(v)
    print(f"embed.html {len(src)} chars, embed.min.html {len(mn)} chars; {len(selectors(src))} selectors, all .emgq; {len(pages)} harness pages in .cache/quiz/")

if __name__ == "__main__":
    main()
