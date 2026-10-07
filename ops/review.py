"""Render page specs as a readable review document (Markdown), in the order the page reads, for Divit's review.
  python3 ops/review.py <url> [<url> ...] > review.md"""
import json, os, re, sys, subprocess
from html import unescape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ops")); import hubctl as HC
def txt(h): return unescape(re.sub(r"<[^>]+>", "", h or "")).strip()
def h3p(h):
    m = re.search(r"<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>", h or "", re.S); return (txt(m.group(1)), txt(m.group(2))) if m else ("", txt(h))
def table_md(html):
    heads = ["", "Emergent"] + re.findall(r'<th scope="col">([^<]+)</th>', html)
    out = ["| " + " | ".join(heads) + " |", "|" + "---|" * len(heads)]
    for lab, cells in re.findall(r'<th scope="row">(.*?)</th>(.*?)</tr>', html, re.S):
        out.append("| **" + unescape(lab) + "** | " + " | ".join(unescape(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", cells, re.S)) + " |")
    return "\n".join(out)
def page(url):
    s = json.load(open(HC.spath(url))); F = s["fields"]; o = []
    qc = subprocess.run([sys.executable, os.path.join(ROOT, "qc", "qc_hub.py"), HC.spath(url)], capture_output=True, text=True).stdout
    o += [f"# {F['h1']}", f"`{url}`  ·  primary: **{s['keywords']['primary']}**", ""]
    o += ["## Search snippet", f"**{F['meta_title']}**  ({len(F['meta_title'])} chars)", "", f"{F['meta_description']}  ({len(F['meta_description'])} chars)", ""]
    o += ["## Hero", f"**{F['h1']}**", "", F["hero_description"], "", f"Prompt box: _{txt(F['hero_prompt'])}_  ·  Chips: " + " · ".join(F[f"prompt_chip_{i}"] for i in range(1, 5)), ""]
    o += [f"## {F['features_heading']}", F["features_subheading"], ""]
    for i in range(1, 7):
        t, b = h3p(F[f"feature_{i}"]); o += [f"**{t}**  ", b, ""]
    o += [f"## {F['usecase_heading']}"]
    for i in range(1, 5):
        t, b = h3p(F[f"tab_content_{i}"]); o += [f"**Tab {i}: {F[f'tab_label_{i}']}**  ", f"_{t}_  ", b, ""]
    o += [f"## {F['howto_title']}", F["howto_description"], ""]
    for i in range(1, 8): o += [f"**{F[f'howto_step_{i}_title']}**  ", F[f"howto_step_{i}_des"], ""]
    o += [f"## {F['why_title']}", F["why_description"], "", table_md(F["why_table"]), ""]
    fq = json.loads(re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;\s*</script>", F["faq"], re.S).group(1))
    src = {x["q"]: x for x in s.get("faq_sources", [])}
    o += [f"## {fq['heading']}"]
    for it in fq["items"]:
        sx = src.get(it["q"], {}); tag = {"paa": "People Also Ask", "related": "Related search", "secondary": "Secondary keyword", "definition": "Definition"}.get(sx.get("source"), "?")
        o += [f"**{it['q']}**  ", txt(it["a"].replace('\\"', '"')), f"<sub>Source: {tag}: \u201c{sx.get('ref', '')}\u201d</sub>", ""]
    o += ["## QC", "```", qc.strip(), "```", ""]
    return "\n".join(o)
if __name__ == "__main__":
    print("\n\n---\n\n".join(page(u) for u in sys.argv[1:]))
