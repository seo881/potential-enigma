"""batch_review.py: Divit's ONE file per batch (launch run Part 6): the PA13 skim and the PA3 newly-passing read together.

    .venv/bin/python3 ops/batch_review.py plan/batches/batch-N.txt      -> .cache/review/batch-N.html (git-ignored)

Per page: H1, meta title and description, the hero prompt and 4 chip prompts, all 10 FAQ questions (questions admitted only by
the PA3 widening are highlighted with the reason), the launch review's notes and fixed blocking findings, and the image
contact sheet (rebuilt from the committed images, nothing re-rendered). Divit replies "approve batch N" or names pages and
questions to fix. Pages the pipeline stopped are listed at the top with the reason.
"""
import html, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc", "pipeline"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H, ship as S, paa_gate as PG

E = html.escape
def txt(h): return html.unescape(re.sub(r"<[^>]+>", "", h or "")).strip()

def sheet(url):
    import engine
    s = S.spec(url); d = os.path.basename(os.path.dirname(s["_path"])); slug = url.rsplit("/", 1)[1]
    p = os.path.join(ROOT, ".cache", "review", f"{d}_{slug}.png")
    if s.get("image_brief") and all(os.path.exists(os.path.join(ROOT, im.get("path", "") or "_")) for im in s.get("images", {}).values()):
        try: engine.render_spec(s["_path"], write=False)
        except Exception as e: return None, f"contact sheet not built: {type(e).__name__}"
    return (os.path.basename(p), None) if os.path.exists(p) else (None, "no contact sheet (images not rendered from a brief)")

def page_html(url, P):
    s = S.spec(url); F = s["fields"]; g = PG.Gate(url); items, page = PG.run_spec(g)
    rows = []
    for it in items:
        via = next((m for r, k, m in it["reasons"] if r == "PA3w"), None)
        bad = sorted({r for r, k, _ in it["reasons"] if k == "reject"})
        cls = "new" if via else ("bad" if bad else "")
        rows.append(f"<li class='{cls}'>{E(it['q'])}" + (f" <span class='tag'>PA3 widened: {E(via)}</span>" if via else "")
                    + (f" <span class='tag bad'>rejected: {E(', '.join(bad))}</span>" if bad else "") + "</li>")
    rv = s.get("review") or {}; fnd = rv.get("findings") or []
    notes = [f for f in fnd if f.get("severity") == "note"]; blocking = [f for f in fnd if f.get("severity") == "blocking"]
    img, why = sheet(url)
    chips = s.get("chip_prompts") or []
    out = [f"<section id='{E(url.rsplit('/', 1)[1])}'><h2>{E(txt(F['h1']))}</h2>",
           f"<p class='url'>{E(url)} · ship stage {E(P['stage'])} · QC {S.qc_total(url)} · PAA gate {sum(i['verdict'] != 'reject' for i in items)}/{len(items)}"
           + (f" · CMS draft {E(s.get('item_id') or '-')}" if s.get("item_id") else "") + "</p>",
           f"<p><b>Meta title</b> ({len(F['meta_title'])} chars): {E(F['meta_title'])}<br><b>Meta description</b> ({len(F['meta_description'])} chars): {E(F['meta_description'])}</p>",
           f"<p><b>Hero prompt</b>: {E(txt(F.get('hero_prompt')))}</p><ol class='chips'>"
           + "".join(f"<li><b>{E(F.get(f'prompt_chip_{i}', ''))}</b>: {E(chips[i - 1]) if i <= len(chips) and chips[i - 1] else '<i>missing</i>'}</li>" for i in range(1, 5)) + "</ol>",
           "<h3>FAQ (10 questions; highlighted = admitted only by the PA3 widening, read each)</h3><ol class='faq'>" + "".join(rows) + "</ol>"]
    if page: out.append("<p class='bad'>Gate page problems: " + E("; ".join(f"{r} {m}" for r, m in page)) + "</p>")
    out.append(f"<h3>Review ({E(rv.get('by', 'none'))})</h3>")
    if blocking: out.append("<p><b>Blocking findings (fixed in the one rework):</b></p><ul>" + "".join(f"<li>{E(f.get('field', ''))}: {E(f.get('issue', ''))}</li>" for f in blocking) + "</ul>")
    out.append("<p><b>Notes (ship as is):</b></p><ul>" + ("".join(f"<li>{E(f.get('field', ''))}: {E(f.get('issue', ''))}</li>" for f in notes) or "<li>none</li>") + "</ul>")
    out.append(f"<img src='{E(img)}' alt='contact sheet'>" if img else f"<p class='bad'>{E(why)}</p>")
    return "\n".join(out) + "</section>"

STOCK = re.compile(r"\b(Northwind|Globex|Initech|Acme|Contoso|Fabrikam|Wayne Enterprises|Umbrella Corp)\b")
PERSON = re.compile(r"\b([A-Z][a-z]+ (?:[A-Z][a-z]+|O'[A-Z][a-z]+))\b")
FIRST = set("""Aaron Abby Adam Aisha Alex Alice Amara Amir Amy Ana Andre Andrea Angela Anna Ava Ben Beth Brian Caleb Carla Carlos Carmen Chen Chloe Chris Claire Cole Dana Daniel David Diana Diego Elena Eli Ella Emily Emma Eric Ethan Eva Felix Fatima Grace Hana Hannah Ian Isaac Ivan Jack Jada James Jamal Jane Jason Jen Jenna Jess Jin John Jonah Jordan Jose Josh Julia Kai Kara Kate Kayla Ken Kevin Kim Laila Lara Laura Leah Lena Leo Liam Lily Lina Luca Lucy Luis Maya Maria Marco Marcus Mark Marta Mateo Max Mei Mia Michael Mike Mina Nadia Naomi Nate Nina Noah Nora Olivia Omar Owen Paul Priya Rachel Raj Ravi Rosa Ruth Ryan Sam Sara Sarah Sean Sofia Sophie Tara Tessa Theo Tom Tyler Uma Vera Victor Will Yara Zoe Hollis Dana Ana Jordan Rosa Maria Owen Hannah""".split())
def _all_text(s): return " ".join(txt(v) for v in s["fields"].values() if isinstance(v, str))
def persona_index(urls):
    """Two-word capitalized names that appear on more than one page of the batch or the live set (reused personas)."""
    import glob
    idx = {}
    for f in glob.glob(os.path.join(ROOT, "specs", "*", "*.json")):
        s = json.load(open(f))
        if s["url"] not in urls and not s.get("item_id"): continue
        for n in set(PERSON.findall(_all_text(s))):
            if n.split()[0] in FIRST: idx.setdefault(n, set()).add(s["url"])
    return {n: us for n, us in idx.items() if len(us) > 1}
def page_html_slim(url, P, risks, personas):
    """MONDAY B4 (Divit 2026-10-12): H1, subhead, meta, the 10 FAQ questions; only risky items highlighted."""
    s = S.spec(url); F = s["fields"]; g = PG.Gate(url); items, page = PG.run_spec(g); body = _all_text(s)
    flags = []
    rows = []
    for i, it in enumerate(items, 1):
        fl = sorted({r for r, k, _ in it["reasons"] if k in ("flag", "reject") and r != "PA6"}) if it["verdict"] in ("flag", "reject") else []
        via = next((m for r, k, m in it["reasons"] if r == "PA3w"), None)
        risky = bool(fl) or bool(STOCK.search(it["q"]))   # PA3-widened admits via approved secondaries are routine now (not highlighted)
        rows.append(f"<li class='{'risk' if risky else ''}'>{E(it['q'])}" + (f" <span class='tag'>{E(', '.join(fl))}</span>" if risky else "") + "</li>")
    stock = sorted(set(STOCK.findall(body)))
    if stock: flags.append("Stock company names in the copy (backlog line 104): " + ", ".join(stock))
    reused = sorted(n for n, us in personas.items() if url in us and n in body)
    if reused: flags.append("Persona names also used on other pages: " + "; ".join(f"{n} ({', '.join(u.rsplit('/', 1)[1] for u in sorted(personas[n]) if u != url)})" for n in reused))
    import qc_hub as Q
    every = Q.load_specs(sorted(__import__("glob").glob(os.path.join(ROOT, "specs", "*", "*.json"))))
    me = next(x for x in every if x["url"] == url)
    k7 = [i["msg"] for i in Q.check(me, every) if i["code"] == "K7"]
    flags += [f"K7: {m}" for m in k7 if not any("K7" in r for r in risks.get(url, []))]
    flags += risks.get(url, [])
    out = [f"<section id='{E(url.rsplit('/', 1)[1])}'><h2>{E(txt(F['h1']))}</h2>",
           f"<p class='url'>{E(url)} · QC {S.qc_total(url)} · gate {sum(i['verdict'] != 'reject' for i in items)}/{len(items)} · CMS {E(s.get('item_id') or '-')}</p>",
           f"<p class='sub'>{E(txt(F.get('hero_description')))}</p>",
           f"<p><b>Meta title</b> ({len(F['meta_title'])}): {E(F['meta_title'])}<br><b>Meta description</b> ({len(F['meta_description'])}): {E(F['meta_description'])}</p>"]
    if flags: out.append("<div class='riskbox'><b>Check these</b><ul>" + "".join(f"<li>{E(f)}</li>" for f in flags) + "</ul></div>")
    out.append("<ol class='faq'>" + "".join(rows) + "</ol>")
    return "\n".join(out) + "</section>"

def main(bf):
    L = S.load_ledger(bf); urls = S.batch_urls(bf); name = S.batch_name(bf)
    stopped = [(u, L["pages"][u]) for u in urls if L["pages"][u].get("stopped")]
    live = [u for u in urls if not L["pages"][u].get("stopped")]
    body = [f"<h1>{E(name)}: {len(live)} pages for your review</h1>",
            "<p>Reply <b>approve " + E(name.replace('-', ' ')) + "</b>, or name pages and questions to fix. Highlighted questions were admitted only by the PA3 widening; "
            "reject any and it goes on that page's PA4 skip list with your reason.</p>"]
    if stopped and "--with-held" in sys.argv: body.append("<h2>Held (not in this review)</h2><ul>" + "".join(f"<li>{E(u)}: {E(P['stopped'])}</li>" for u, P in stopped) + "</ul>")
    body.append("<ol class='toc'>" + "".join(f"<li><a href='#{E(u.rsplit('/', 1)[1])}'>{E(u)}</a></li>" for u in live) + "</ol>")
    if "--slim" in sys.argv:
        rp = os.path.join(ROOT, ".cache", "review", f"{name}-risks.json"); risks = json.load(open(rp)) if os.path.exists(rp) else {}
        personas = persona_index(set(live))
        body[1] = "<p>H1, subhead, meta and the 10 FAQ questions per page. Only risky items are highlighted: gate flags on a question, and the <b>Check these</b> box (stock names, reused personas, table cells from snippets, K7). Reply with page and item, or <b>staging published</b> once you publish to staging.</p>"
        body += [page_html_slim(u, L["pages"][u], risks, personas) for u in live]
    else:
        body += [page_html(u, L["pages"][u]) for u in live]
    css = ("body{font:15px/1.5 -apple-system,Segoe UI,sans-serif;max-width:980px;margin:24px auto;padding:0 16px;color:#1a1a1a;background:#fff}"
           "section{border-top:2px solid #ddd;margin-top:32px;padding-top:8px}.url{color:#666;font-size:13px}li.new{background:#fff3c4}"
           "li.risk{background:#fff3c4}.riskbox{background:#fff7e0;border-left:4px solid #e0a800;padding:6px 12px;margin:8px 0}.sub{font-size:17px;color:#333}li.bad,.bad{color:#a40000}.tag{font-size:12px;color:#7a5b00;margin-left:6px}img{max-width:100%;border:1px solid #ddd}")
    out = os.path.join(ROOT, ".cache", "review", f"{name}.html"); os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(f"<!doctype html><meta charset='utf-8'><title>{E(name)} review</title><style>{css}</style>" + "\n".join(body))
    print(f"{os.path.relpath(out, ROOT)}: {len(live)} pages in publish order ({len(stopped)} held pages left out)")

if __name__ == "__main__":
    main(sys.argv[1])
