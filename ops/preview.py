"""Render a page spec as a self-contained HTML preview of the child page: real copy, the live SVG images (motion plays),
working use-case tabs, the FAQ with its links, the comparison table, the Google snippet, the card cover and share image.
  python3 ops/preview.py <url> [out.html]
Not the Webflow template itself: a faithful reading copy for review before anything goes to the CMS."""
import json, os, re, sys, base64, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ops")); import hubctl as HC

def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(os.path.join(ROOT, path), "rb").read()).decode()

def build(url):
    s = json.load(open(HC.spath(url))); F = s["fields"]; im = s.get("images", {})
    esc = lambda t: html.escape(t or "", quote=True)
    fq = json.loads(re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;\s*</script>", F["faq"], re.S).group(1))
    src = {x["q"]: x for x in s.get("faq_sources", [])}
    hub = HC.CFG["hubs"][s["hub"]]
    img = lambda k: (data_uri(im[k]["path"], "image/svg+xml" if im[k]["path"].endswith(".svg") else "image/png"), esc(im[k].get("alt", ""))) if im.get(k, {}).get("path") else ("", "")
    tabs = ""
    panes = ""
    for i in range(1, 5):
        u, a = img(f"tab_image_{i}")
        tabs += f'<button role="tab" aria-selected="{"true" if i == 1 else "false"}" aria-controls="pane{i}" id="tab{i}" data-i="{i}">{esc(F[f"tab_label_{i}"])}</button>'
        panes += f'<div class="pane" role="tabpanel" id="pane{i}" aria-labelledby="tab{i}"{"" if i == 1 else " hidden"}><div class="pane-copy">{F[f"tab_content_{i}"]}</div><img src="{u}" alt="{a}" width="1200" height="800"></div>'
    feats = "".join(f'<div class="feat">{F[f"feature_{i}"]}</div>' for i in range(1, 7))
    steps = "".join(f'<li><span class="n">{esc(F[f"howto_step_{i}_title"][:2])}</span><div><h3>{esc(F[f"howto_step_{i}_title"][3:])}</h3><p>{esc(F[f"howto_step_{i}_des"])}</p></div></li>' for i in range(1, 8))
    faqs = ""
    for it in fq["items"]:
        sx = src.get(it["q"], {}); tag = {"paa": "People Also Ask", "related": "Related search", "secondary": "Secondary keyword", "keyword": "Keyword idea", "definition": "Definition"}.get(sx.get("source"), "")
        faqs += f'<details><summary>{esc(it["q"])}</summary><p>{it["a"]}</p><p class="src">Source: {tag}, "{esc(sx.get("ref", ""))}"</p></details>'
    table = re.sub(r"<style>.*?</style>", "", F["why_table"], flags=re.S)
    cov_u, cov_a = img("cover_image"); og_u, og_a = img("share_image")
    chips = "".join(f"<span>{esc(F[f'prompt_chip_{i}'])}</span>" for i in range(1, 5))
    page_url = "emergent.sh" + url
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(F['meta_title'])} (preview)</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#FFFFFF;--soft:#F5F5F6;--line:#E4E4E7;--ink:#0F172A;--sub:#475569;--muted:#64748B;--link:#1D4ED8;--note:#FEF9C3;
 box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0E0F11;--soft:#17181B;--line:#2A2B30;--ink:#F4F4F5;--sub:#C4C4CC;--muted:#9A9AA5;--link:#93B4FF;--note:#3A3415}}}}
:root[data-theme="dark"]{{--bg:#0E0F11;--soft:#17181B;--line:#2A2B30;--ink:#F4F4F5;--sub:#C4C4CC;--muted:#9A9AA5;--link:#93B4FF;--note:#3A3415}}
*,*::before,*::after{{box-sizing:inherit}} html{{scroll-padding-top:env(safe-area-inset-top,0px)}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 24px}} section{{padding:72px 0;border-top:1px solid var(--line)}}
.note{{background:var(--note);font-size:14px;padding:10px 24px;text-align:center;color:var(--ink)}}
.snip{{background:var(--soft);padding:28px 0}} .snip .card{{max-width:640px}} .snip .u{{font-size:14px;color:var(--muted)}}
.snip .t{{font-family:Arial,sans-serif;font-size:20px;color:#1A0DAB;line-height:1.3;margin:4px 0}} .snip .d{{font-family:Arial,sans-serif;font-size:14px;color:var(--sub)}}
@media (prefers-color-scheme:dark){{.snip .t{{color:#8AB4F8}}}}
.crumb{{font-size:14px;color:var(--muted);padding-top:32px}} .crumb a{{color:var(--muted)}}
h1{{font-size:clamp(34px,5vw,56px);line-height:1.08;letter-spacing:-.02em;margin:16px 0 18px;max-width:900px;font-weight:800}}
.lede{{font-size:20px;color:var(--sub);max-width:720px;margin:0}}
.prompt{{margin:32px 0 0;max-width:760px;border:1px solid var(--line);border-radius:16px;padding:18px 20px;background:var(--bg);box-shadow:0 1px 2px rgba(15,23,42,.06)}}
.prompt p{{margin:0 0 14px;color:var(--ink)}} .chips{{display:flex;flex-wrap:wrap;gap:8px}} .chips span{{font-size:14px;border:1px solid var(--line);border-radius:999px;padding:4px 12px;color:var(--sub)}}
.btn{{display:inline-block;margin-top:20px;background:var(--ink);color:var(--bg);border-radius:10px;padding:12px 20px;font-weight:600;text-decoration:none}}
h2{{font-size:clamp(28px,3.4vw,40px);line-height:1.15;letter-spacing:-.015em;margin:0 0 12px;max-width:760px}}
.sub{{color:var(--sub);max-width:680px;margin:0 0 40px;font-size:18px}}
.feats{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
.feat{{background:var(--bg);padding:28px}} .feat h3{{font-size:18px;margin:0 0 8px;line-height:1.3}} .feat p{{margin:0;color:var(--sub)}}
[role=tablist]{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:24px}}
[role=tab]{{font:inherit;font-weight:600;border:1px solid var(--line);background:var(--bg);color:var(--sub);border-radius:999px;padding:8px 16px;cursor:pointer}}
[role=tab][aria-selected=true]{{background:var(--ink);color:var(--bg);border-color:var(--ink)}} [role=tab]:focus-visible,summary:focus-visible,a:focus-visible{{outline:2px solid var(--link);outline-offset:2px}}
.pane{{display:grid;grid-template-columns:1fr 1.6fr;gap:40px;align-items:center}} .pane[hidden]{{display:none}}
.pane-copy h3{{font-size:24px;line-height:1.25;margin:0 0 12px}} .pane-copy p{{color:var(--sub);margin:0}}
.pane img,.media img{{width:100%;height:auto;max-width:100%;border-radius:12px;display:block;background:#F4F4F5}}
ol.steps{{list-style:none;padding:0;margin:0;display:grid;gap:0;border-top:1px solid var(--line)}}
ol.steps li{{display:grid;grid-template-columns:56px 1fr;gap:16px;padding:22px 0;border-bottom:1px solid var(--line)}}
ol.steps .n{{font-weight:700;color:var(--muted);font-variant-numeric:tabular-nums}} ol.steps h3{{margin:0 0 6px;font-size:18px}} ol.steps p{{margin:0;color:var(--sub)}}
.tbl{{overflow-x:auto;border:1px solid var(--line);border-radius:14px}} table{{border-collapse:collapse;width:100%;min-width:760px;font-size:15px}}
th,td{{text-align:left;padding:14px 16px;border-bottom:1px solid var(--line);vertical-align:top}} thead th{{font-weight:700}} tbody th{{font-weight:600;color:var(--ink)}} td{{color:var(--sub)}}
td.col-brand,th.col-brand-head{{background:var(--soft);color:var(--ink);font-weight:600}} .brand-logo{{height:18px;width:auto}} @media (prefers-color-scheme:dark){{.brand-logo{{filter:invert(1)}}}}
.visually-hidden{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
details{{border-bottom:1px solid var(--line);padding:18px 0}} summary{{font-weight:600;font-size:18px;cursor:pointer;list-style:none}} summary::-webkit-details-marker{{display:none}}
summary::after{{content:"+";float:right;color:var(--muted);font-weight:400}} details[open] summary::after{{content:"\\2212"}}
details p{{color:var(--sub);margin:12px 0 0;max-width:820px}} details a{{color:var(--link)}} .src{{font-size:13px;color:var(--muted)}}
.media{{display:grid;grid-template-columns:1fr 1.6fr;gap:32px;align-items:start}} .media figure{{margin:0}} figcaption{{font-size:14px;color:var(--muted);margin-top:8px}}
@media (max-width:820px){{.feats{{grid-template-columns:1fr}} .pane,.media{{grid-template-columns:1fr}} section{{padding:48px 0}}}}
@media (prefers-reduced-motion:reduce){{*{{scroll-behavior:auto}}}}
</style></head><body>
<div class="note">Draft preview for review. Real copy and images; the live page uses Emergent's Webflow template.</div>
<div class="snip"><div class="wrap"><div class="card"><div class="u">{esc(page_url)}</div><div class="t">{esc(F['meta_title'])}</div><div class="d">{esc(F['meta_description'])}</div></div></div></div>
<main>
<div class="wrap"><div class="crumb"><a href="https://emergent.sh{hub['path']}">{esc(hub['hub_link_text'].replace('AI ', 'AI ', 1).title().replace('Ai ', 'AI '))}</a> / {esc(F['breadcrumb'])}</div>
<h1>{esc(F['h1'])}</h1><p class="lede">{esc(F['hero_description'])}</p>
<div class="prompt"><p>{esc(re.sub('<[^>]+>', '', F['hero_prompt']))}</p><div class="chips">{chips}</div></div>
<a class="btn" href="#">{esc(F['explore_cta'])}</a></div>
<section><div class="wrap"><h2>{esc(F['features_heading'])}</h2><p class="sub">{esc(F['features_subheading'])}</p><div class="feats">{feats}</div></div></section>
<section><div class="wrap"><h2>{esc(F['usecase_heading'])}</h2><div role="tablist" aria-label="Use cases">{tabs}</div>{panes}</div></section>
<section><div class="wrap"><h2>{esc(F['howto_title'])}</h2><p class="sub">{esc(F['howto_description'])}</p><ol class="steps">{steps}</ol></div></section>
<section><div class="wrap"><h2>{esc(F['why_title'])}</h2><p class="sub">{esc(F['why_description'])}</p><div class="tbl">{table}</div></div></section>
<section><div class="wrap"><h2>{esc(fq['heading'])}</h2>{faqs}</div></section>
<section><div class="wrap"><h2>Card cover and share image</h2><div class="media"><figure><img src="{cov_u}" alt="{cov_a}"><figcaption>Carousel card cover (SVG)</figcaption></figure><figure><img src="{og_u}" alt="{og_a}"><figcaption>Share image for LinkedIn, Slack and X (PNG, the one format those platforms accept)</figcaption></figure></div></div></section>
</main>
<script>
document.querySelectorAll('[role=tab]').forEach(t=>t.addEventListener('click',()=>{{
 document.querySelectorAll('[role=tab]').forEach(x=>x.setAttribute('aria-selected',x===t?'true':'false'));
 document.querySelectorAll('.pane').forEach(p=>p.hidden=p.id!=='pane'+t.dataset.i);}}));
</script></body></html>"""

if __name__ == "__main__":
    url = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, ".cache", "review", url.rsplit("/", 1)[1] + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True); open(out, "w").write(build(url)); print(f"preview: {out} ({os.path.getsize(out)//1024} KB)")
