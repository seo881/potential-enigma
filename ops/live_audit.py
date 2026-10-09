"""live_audit.py: the live audit (docs/LIVE_AUDIT.md; Divit, 2026-10-09). Wired into hubctl:

  hubctl live-audit [--since-publish | --all | --urls U,U | --set launch] [--base URL] [--dry] [--external] [--no-shots]
      Layer A (ops/live_audit.mjs + the checks below) -> audits/live/YYYY-MM-DD/findings.json, per-page day files,
      Layer B batches (4 pages each) in .cache/live/YYYY-MM-DD/layerB-N.md, and the fix plan. --dry changes nothing
      (no spec edits, no ledger rows, no state) and lists the would-fix items.
  hubctl live-audit record DATE LAYERB.json         merge one Layer B reviewer's findings (severity from the reviewer)
  hubctl live-audit drift DATE READBACK.json        classify "not rendered as approved" findings with a CMS read:
                                                    CMS differs from our last write = drift (reported, never overwritten)
  hubctl live-audit plan DATE                       recompute the fix plan (auto / writer / proposed / backlog)
  hubctl live-audit report DATE [--dry]             reports/DATE/HHMM-live-audit.md, digest first; audits/live/LEDGER.md
  hubctl live-fix prepare ISSUE --readback F.json   steps 1-3 of a fix: before-value, spec checks (QC 0, gate 10/10 if FAQ,
                                                    images current), payload ops/out/live/ISSUE.json (update + item publish + read)
  hubctl live-fix approve ISSUE --by divit [--note N]  a proposal Divit approved becomes a writer fix
  hubctl live-fix add DATE URL FIELD CODE SEV "MSG"  a finding from an approved sweep (action fix-by-writer)
  (prepare writes the before-value and refuses to write the payload until that file is committed, unchanged and pushed: rerun it then)
  hubctl live-fix verify ISSUE RESPONSE.json        step 4-5: read-back equals the spec, Layer A re-run on that URL; on failure
                                                    the rollback payload is written and must be sent at once
  hubctl live-rollback ISSUE [--done RESPONSE.json] re-send the before-value and publish the item (payload); --done records it

Webflow is reached only through the MCP, so the orchestrating Claude session sends every payload this module writes.
Hard limits (doc): at most 10 field changes per page per run; never slugs, the primary keyword in H1 or meta, deletions,
templates, components, classes, sitewide elements, hub pages, or drift. Public-safe outputs only (our own page copy).
"""
import datetime, glob, hashlib, html, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("ops", "qc", "pipeline"): sys.path.insert(0, os.path.join(ROOT, d))
import hubctl as H

AUD = os.path.join(ROOT, "audits", "live"); CACHE = os.path.join(ROOT, ".cache", "live"); OUTD = os.path.join(ROOT, "ops", "out", "live")
STATE = os.path.join(AUD, "state.json"); LEDGER_J = os.path.join(AUD, "ledger.json"); LEDGER_MD = os.path.join(AUD, "LEDGER.md")
CANON = "https://emergent.sh"
CONF = json.load(open(os.path.join(ROOT, "rules", "live_audit.json")))
TEXT_FIELDS = [k for k in CONF["rendered_fields"]]
AUTO_FIELDS = set(CONF["auto_fields"])          # fields the audit may change on its own (doc: text, FAQ, meta, alt, CMS links, images)
MAX_FIELDS = 10

def today(): return datetime.date.today().isoformat()
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
def jload(p, d): return json.load(open(p)) if os.path.exists(p) else d
def jsave(p, o): os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(o, open(p, "w"), indent=1, ensure_ascii=False)
def plain(v): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", v or ""))).strip()
def squash(v): return re.sub(r"\s+", "", v or "")
def slug_of(u): return u.rstrip("/").rsplit("/", 1)[1]
def spec(url): return json.load(open(H.spath(url)))
def faq_obj(F):
    m = re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;\s*</script>", F.get("faq") or "", re.S)
    return json.loads(m.group(1)) if m else {"items": []}
def git(*a): return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout.strip()

# ---------------------------------------------------------------- page selection
def published_urls():
    import guards as G
    return sorted(u for u, e in G.all_status().items() if e.get("state") == "published")

def select(args):
    st = jload(STATE, {"pages": {}})
    if "--urls" in args: return [u.strip() for u in args[args.index("--urls") + 1].split(",") if u.strip()]
    if "--set" in args and args[args.index("--set") + 1] == "launch":
        import launch; return launch.pages()
    pub = published_urls()
    if "--all" in args: return pub
    import guards as G; S = G.all_status()   # --since-publish (default): published pages not audited since their publish
    return [u for u in pub if (st["pages"].get(u, {}).get("last_audit") or "") < (S[u].get("updated") or "")]

def held_pages():
    """Every page held in status/ship/*.json (stopped), with its CMS item if it has one. None of them may be live anywhere."""
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "status", "ship", "*.json"))):
        for u, P in json.load(open(p))["pages"].items():
            if P.get("stopped"):
                s = spec(u) if os.path.exists(H.spath(u)) else {}
                out.append({"url": u, "item_id": s.get("item_id"), "collection": H.CFG["hubs"][H.hub_of(u)]["collection_id"], "ledger": os.path.basename(p)})
    return out

def manifest_entry(url):
    s = spec(url); F, _ = H.export_fields(url, s); hub = H.hub_of(url)
    fq = faq_obj(F)
    return {"url": url, "hub": H.CFG["hubs"][hub]["path"], "h1": plain(F["h1"]), "meta_title": F["meta_title"], "meta_description": F["meta_description"],
            "faq": [i["q"] for i in fq["items"]], "faq_items": [{"q": i["q"], "a": plain(i["a"])} for i in fq["items"]],
            "default_prompt": plain(re.sub(r"<div data-rt-embed-type.*", "", F.get("hero_prompt") or "", flags=re.S)), "chips": s.get("chip_adds") or s.get("chip_prompts") or [],
            "tab_labels": [plain(F.get(f"tab_label_{i}")) for i in range(1, 5)],
            "uc_images": [(s["images"].get(f"tab_image_{i}") or {}).get("cdn_url") for i in range(1, 5)],
            "images": {k: {"cdn_url": v.get("cdn_url"), "file_id": v.get("file_id"), "alt": v.get("alt"), "path": v.get("path")} for k, v in (s.get("images") or {}).items()},
            "fields": {k: plain(F.get(k)) for k in TEXT_FIELDS if isinstance(F.get(k), str) and plain(F.get(k))},
            "primary": (s.get("keywords") or {}).get("primary", ""), "item_id": s.get("item_id"),
            "in_sync": bool(s.get("cms_draft")) and s["cms_draft"].get("fingerprint") == __import__("guards").fingerprint(s)}

# ---------------------------------------------------------------- Layer A evaluation (deterministic)
ZW = re.compile("[​‌‍⁠﻿­]"); CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
ENT = re.compile(r"&(?:amp;)+(?:amp|lt|gt|quot|#\d+|nbsp);|&(?:amp|lt|gt|quot|nbsp|#\d{2,5});")
DASH = re.compile("[–—]"); CURLY = re.compile("[‘’“”]"); REPEAT = re.compile(r"(?i)\b([a-z]{2,}) +\1\b")   # spaces only: table cells (tabs) and lines are separate
def us_map():
    return json.load(open(os.path.join(ROOT, "rules", "us_spelling.json")))["map"]

def hygiene(text):
    """[(code, message, snippet)] for one text."""
    out = []; t = text or ""
    if re.search("(?m)^[\u200b\u200c\u200d\u2060\ufeff\\s]*[\u200b\u200c\u200d\u2060\ufeff][\u200b\u200c\u200d\u2060\ufeff\\s]*$", t):
        out.append(("A5-empty-p", "empty paragraph (Webflow rich-text zero-width placeholder)", ""))
        t = re.sub("(?m)^[\u200b\u200c\u200d\u2060\ufeff\\s]+$", "", t)
    for rx, code, msg in ((ZW, "A6-zw", "zero-width character"), (CTRL, "A6-ctrl", "control character"), (ENT, "A6-entity", "broken HTML entity shown as text"),
                          (DASH, "A6-dash", "em or en dash"), (CURLY, "A6-quote", "curly quote (house style: straight quotes)")):
        m = rx.search(t)
        if m: out.append((code, msg, t[max(0, m.start() - 30):m.end() + 30]))
    for line in t.split("\n"):
        if re.search(r"\S {2,}\S", line): out.append(("A6-space", "double space", line.strip()[:80])); break
    m = REPEAT.search(t)
    if m and m.group(1).lower() not in CONF["repeat_ok"]: out.append(("A6-repeat", f'repeated word "{m.group(1)}"', t[max(0, m.start() - 30):m.end() + 30]))
    UM = us_map()
    for w in set(re.findall(r"[A-Za-z]+", t)):
        if w.lower() in UM: out.append(("A6-uk", f'UK spelling "{w}" (use "{UM[w.lower()]}")', w)); break
    for o, c in ("()", "[]"):
        if t.count(o) != t.count(c): out.append(("A6-bracket", f"unbalanced {o}{c}", "")); break
    return out

def field_of(m, snippet):
    """Which spec field holds this text snippet (None = template text)."""
    s = squash(snippet)[:40]
    if not s: return None
    for k, v in m["fields"].items():
        if s in squash(v): return k
    for i, it in enumerate(m["faq_items"], 1):
        if s in squash(it["q"] + it["a"]): return f"faq#{i}"
    return None

def evaluate(raw, man, base):
    """Findings for every page and hub: dicts with id, url, field, severity, code, rule, msg, snippet, fix kind."""
    by = {p["url"]: p for p in man["pages"]}; F = []; staging = base.rstrip("/") != CANON
    def add(url, code, sev, msg, field=None, snippet="", fix="proposed", **kw):
        F.append({"url": url, "field": field, "severity": sev, "code": code, "msg": msg, "snippet": (snippet or "")[:160], "fix": fix, "layer": "A", **kw})
    for r in raw["pages"]:
        url = r["url"]; m = by[url]; c = r["checks"]; R = r.get("render") or {}
        if not c.get("http200"): add(url, "A1-http", "P0", "page does not return HTTP 200", fix="proposed"); continue
        if R.get("http") not in (200, None): add(url, "A1-http", "P0", f"browser load returned {R.get('http')}")
        if R.get("robots") and "noindex" in R["robots"].lower(): add(url, "A2-noindex", "P0", "robots meta has noindex", field="template")
        if not c.get("canonical"): add(url, "A2-canonical", "P1", f"canonical is {R.get('canonical') or 'missing'}, not the page URL", field="template")
        if not staging and raw.get("sitemap_ok") and not r.get("in_sitemap"): add(url, "A2-sitemap", "P1", "not in /sitemap.xml", field="template")
        # title and meta: exact match with the spec; limits as QC L1/L2
        import qc_hub as Q
        for k, live, code in (("meta_title", R.get("title"), "A3-title"), ("meta_description", R.get("description"), "A3-meta")):
            if (live or "").strip() != (m[k] or "").strip(): add(url, code, "P1", f"{k} differs from the spec", field=k, snippet=(live or "missing")[:120], fix="drift-check")
        if len(m["meta_title"]) > 60 or (Q.title_px(m["meta_title"]) or 0) > 580: add(url, "A3-title-len", "P1", "meta title over 60 chars or 580 px", field="meta_title", fix="writer")
        if not 110 <= len(m["meta_description"]) <= 160: add(url, "A3-meta-len", "P1", f"meta description {len(m['meta_description'])} chars (110-160)", field="meta_description", fix="writer")
        if len(R.get("h1s") or []) != 1: add(url, "A3-h1", "P1", f"{len(R.get('h1s') or [])} H1 elements (exactly 1)", field="template")
        # every spec field rendered exactly once; nothing stray
        allt = squash(R.get("text_all"))
        for k, v in m["fields"].items():
            if k in ("meta_title", "meta_description"): continue
            n = allt.count(squash(v)) if len(squash(v)) >= 8 else 1
            if n == 0: add(url, "A4-missing", "P1", f"field {k} is not rendered as approved", field=k, fix="drift-check")
            elif n > 1 and k not in CONF["may_repeat"]: add(url, "A4-repeat", "P2", f"field {k} rendered {n} times", field=k, fix="backlog")
        vis = R.get("text_visible") or ""
        for pat in CONF["stray_patterns"]:
            mm = re.search(pat, vis)
            if mm: add(url, "A5-stray", "P1", f'stray template text: "{mm.group(0)}"', field=field_of(m, mm.group(0)) or "template", snippet=vis[max(0, mm.start() - 40):mm.end() + 40])
        for cls in R.get("empty_sections") or []: add(url, "A5-empty", "P2", f"empty visible section ({cls[:40]})", field="template", fix="backlog")
        # character hygiene: visible text, alt text, meta, JSON-LD
        texts = [("visible", vis), ("meta", (R.get("title") or "") + "\n" + (R.get("description") or ""))]
        texts += [("alt", i.get("alt") or "") for i in R.get("images") or []] + [("jsonld", j) for j in R.get("jsonld") or []]
        seen = set()
        for where, t in texts:
            for code, msg, snip in hygiene(t):
                fld = field_of(m, snip) if where in ("visible", "meta") else ("alt" if where == "alt" else "template")
                if (code, fld) in seen: continue
                seen.add((code, fld)); sev = "P2" if code == "A5-empty-p" else "P1"
                add(url, code, sev, f"{msg} in {where} text", field=fld or "template", snippet=snip,
                    fix=("auto" if (fld and (fld.split("#")[0] in AUTO_FIELDS) and code in CONF["deterministic_codes"]) else ("writer" if fld and fld.split("#")[0] in AUTO_FIELDS else "proposed")))
        # links
        hub_in_faq = sum(1 for l in R.get("links") or [] if l["in_faq"] and urlpath(l["href"]) == m["hub"])
        if hub_in_faq != 1: add(url, "A7-hub-link", "P1", f"hub link in the FAQ {hub_in_faq} times (exactly 1)", field="faq", fix="writer")
        for href, st in (r.get("link_status") or {}).items():
            if st["status"] != 200:
                fld = "faq" if any(l["href"] == href and l["in_faq"] for l in R.get("links") or []) else "template"
                add(url, "A7-link", "P0" if st["internal"] else "P1", f"{'internal' if st['internal'] else 'external'} link returns {st['status']}: {urlpath(href) or href}",
                    field=fld, fix="auto" if fld == "faq" and st["internal"] else "proposed")
        if not c.get("no_link_to_non_live"): add(url, "A7-nonlive", "P1", "links to a child page that is not live: " + ", ".join(r["verify"].get("dead_links") or []), field="faq", fix="auto")
        # images
        for i in R.get("images") or []:
            if i["visible"] and not i["loaded"] and i["src"]: add(url, "A8-load", "P1", f"image does not load: {i['src'][-60:]}", field=img_field(m, i["src"]) or "template")
        for k, im in m["images"].items():
            u = im.get("cdn_url") or ""
            want = "webp" if k == "share_image" else "svg"
            if u and not u.lower().endswith("." + want): add(url, "A8-format", "P1", f"{k} is not {want.upper()}", field=k, fix="auto")
            if not (im.get("alt") or "").strip(): add(url, "A8-alt", "P1", f"{k} has no alt text", field=k, fix="writer")
            live_alt = next((i["alt"] for i in R.get("images") or [] if u and u.split("/")[-1] in (i["src"] or "")), None)
            if live_alt is not None and k != "share_image" and live_alt.strip() != (im.get("alt") or "").strip():
                add(url, "A8-alt-live", "P1", f"{k} alt on the page differs from the spec", field=k, snippet=live_alt, fix="drift-check")
        for u, ratio in (r.get("uc_ratio") or {}).items():
            if ratio is None or abs(ratio - 1.5) > 0.01: add(url, "A8-ratio", "P1", f"use-case image is not 3:2 ({ratio})", field=img_field(m, u), fix="proposed")
        og = r.get("og") or {}
        if not og.get("ok"): add(url, "A8-og", "P1", f"og:image not a 1200x630 WebP under 300 KB ({og.get('type')}, {og.get('size')}, {og.get('bytes')} B)", field="share_image", fix="auto")
        # scripts (verify_launch checks): T1, T2, T10, T5
        for k, code, msg, fld in (("hero_prefilled", "A9-prompt", "hero prompt not prefilled (T1)", "hero_prompt"), ("chip_switches", "A9-chips", "chip does not switch the prompt (T1)", "hero_prompt"),
                                  ("chip_stable", "A9-chip-fight", "chip prompt overwritten after the click (older chip script fights T1)", "template"),
                                  ("faq_rendered", "A9-faq", "FAQ not rendered with all 10 questions (T2)", "faq"), ("first_tab_active", "A9-tab", "first use-case tab not active on load (T10)", "template"),
                                  ("carousel_cover_alt", "A9-cover-alt", "carousel cover images without alt (T5)", "template"), ("carousel_hidden", "A9-carousel-shown", "carousel shown while it should be hidden (Divit 2026-10-09)", "template"), ("comparison_table", "A9-table", "comparison table missing", "why_table"),
                                  ("learn_not_empty", "A5-learn", 'Learn section shows "No items found"', "template")):
            if not c.get(k, True): add(url, code, "P1", msg, field=fld, fix="proposed")
        ign = CONF.get("console_ignore", []); ce = [e for e in R.get("console_errors") or [] if not any(s in e for s in ign)]
        if ce: add(url, "A9-console", "P1", f"{len(ce)} console error(s) in Chromium: {ce[0][:120]}", field="template", fix="proposed")
        # JSON-LD: parses; FAQPage matches the visible FAQ word for word
        faqs = []
        for j in R.get("jsonld") or []:
            try: o = json.loads(j)
            except Exception: add(url, "A10-jsonld", "P1", "JSON-LD block does not parse", field="template"); continue
            for n in (o if isinstance(o, list) else o.get("@graph", [o])):
                if isinstance(n, dict) and n.get("@type") == "FAQPage": faqs = n.get("mainEntity") or []
        if faqs:   # FAQ schema on child templates is not needed (DECISIONS 2026-10-06); only a schema that exists must match
            sq = [(plain(x.get("name")), plain((x.get("acceptedAnswer") or {}).get("text"))) for x in faqs]
            want = [(i["q"], i["a"]) for i in m["faq_items"]]
            if [squash(a) + squash(b) for a, b in sq] != [squash(a) + squash(b) for a, b in want]: add(url, "A10-faq-match", "P1", "FAQ schema differs from the visible FAQ", field="faq", fix="drift-check")
    # A0: a page held in status/ship/*.json must not be live anywhere (LESSONS 2026-10-09 incident). P0, unpublish at once.
    for hp in raw.get("held") or []:
        live = [host for host, code in hp["status"].items() if code == 200]
        if live:
            add(hp["url"], "A0-held-live", "P0", f"HELD page is live on {', '.join(live)} (ledger {hp.get('ledger')})", field="item",
                fix="unpublish" if hp.get("item_id") else "proposed", item_id=hp.get("item_id"), collection=hp.get("collection"))
    for h in raw.get("hubs") or []:
        if not h.get("http200"): add(h["hub"], "A1-http", "P0", "hub page does not return HTTP 200", field="hub", fix="proposed"); continue
        if not h.get("carousel_hidden") and not h.get("carousel_has_all_new_cards"): add(h["hub"], "A9-carousel", "P1", "carousel misses live pages: " + ", ".join(h["missing"]), field="hub", fix="proposed")
        if not h.get("carousel_hidden") and not h.get("hub_card_cover_alt"): add(h["hub"], "A9-cover-alt", "P1", "hub card covers without alt: " + ", ".join(h["cover_alt_missing"]), field="hub", fix="proposed")
        for code, msg, snip in hygiene((h.get("render") or {}).get("text_visible", "")):
            add(h["hub"], code, "P2" if code == "A5-empty-p" else "P1", f"{msg} in hub text", field="hub", snippet=snip, fix="proposed")
        for href, st in (h.get("link_status") or {}).items():
            if st["status"] != 200: add(h["hub"], "A7-link", "P0" if st["internal"] else "P1", f"link returns {st['status']}: {urlpath(href) or href}", field="hub", fix="proposed")
    # the primary keyword, the page intent and hub pages are never changed automatically
    for f in F:
        if f["field"] in ("h1", "meta_title") and f["fix"] in ("auto", "writer"): f["fix"] = "writer-keep-primary"
    return F

def urlpath(href):
    try:
        from urllib.parse import urlparse
        u = urlparse(href); return u.path.rstrip("/") if u.netloc in ("emergent.sh", "www.emergent.sh") or u.netloc.endswith("webflow.io") else ""
    except Exception: return ""

def img_field(m, src):
    for k, im in m["images"].items():
        if im.get("cdn_url") and im["cdn_url"].split("/")[-1] in (src or ""): return k
    return None

def number(F, date):
    seen = {}
    for f in F:
        k = f"{date.replace('-', '')}-{slug_of(f['url']) if f['url'].count('/') > 1 else 'hub' + f['url'].replace('/', '-')}-{f['code']}"
        seen[k] = seen.get(k, 0) + 1; f["id"] = f"{k}-{seen[k]}"
    return F

# ---------------------------------------------------------------- golden cases (LESSONS rule 3)
def golden_from(F, date):
    """Every audit catch the gates missed becomes a golden case (tests/golden/cases.jsonl). A catch on our own copy that QC passes."""
    p = os.path.join(ROOT, "tests", "golden", "cases.jsonl"); have = {json.loads(l)["id"] for l in open(p)} if os.path.exists(p) else set()
    new = []
    for f in F:
        if f["layer"] == "A" and f["code"].startswith(("A6", "A3-title-len", "A3-meta-len")) and f["field"] not in (None, "template", "hub", "alt") and f["id"] not in have:
            new.append({"id": f["id"], "source": "live-audit", "date": date, "kind": "qc-text", "url": f["url"], "field": f["field"].split("#")[0],
                        "check": f["code"], "text": f["snippet"], "expect": "caught", "status": "open"})
        if f["layer"] == "B" and f["severity"] in ("P0", "P1") and f["id"] not in have:
            new.append({"id": f["id"], "source": "live-audit-B", "date": date, "kind": "review", "url": f["url"], "field": f["field"], "check": f.get("rule") or f["code"],
                        "text": f["snippet"], "expect": "caught", "status": "open"})
    if new:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "a") as fh:
            for n in new: fh.write(json.dumps(n, ensure_ascii=False) + "\n")
    return len(new)

# ---------------------------------------------------------------- run
def cmd_run(args):
    date = today(); base = (args[args.index("--base") + 1] if "--base" in args else CANON).rstrip("/"); dry = "--dry" in args
    urls = select(args)
    import launch
    hubs = sorted({H.CFG["hubs"][H.hub_of(u)]["path"] for u in urls}) if ("--all" in args or "--set" in args or "--since-publish" in args or not args) else []
    if "--all" in args: hubs = sorted(h["path"] for h in H.CFG["hubs"].values())
    man = {"pages": [manifest_entry(u) for u in urls], "hubs": hubs, "held": held_pages(), "held_hosts": CONF["held_hosts"]}
    cdir = os.path.join(CACHE, date); os.makedirs(cdir, exist_ok=True)
    jsave(os.path.join(cdir, "manifest.json"), man)
    rawp = os.path.join(cdir, "raw.json")
    cmd = ["node", os.path.join(ROOT, "ops", "live_audit.mjs"), os.path.join(cdir, "manifest.json"), rawp, "--base", base]
    if "--no-shots" not in args: cmd += ["--shots", cdir]
    if "--external" in args or datetime.date.today().weekday() == 0: cmd += ["--external"]   # external links weekly (Mondays)
    print(f"Layer A on {len(urls)} pages and {len(hubs)} hubs at {base}" + (" (DRY)" if dry else ""))
    rc = subprocess.run(cmd, cwd=ROOT).returncode
    if rc: sys.exit(f"live_audit.mjs failed ({rc})")
    raw = json.load(open(rawp))
    F = number(evaluate(raw, man, base), date)
    # Layer B: full read on the first audit after publish or after any change; otherwise only where Layer A found something
    st = jload(STATE, {"pages": {}}); hashes = {}
    for r in raw["pages"]:
        hashes[r["url"]] = hashlib.sha256(squash((r.get("render") or {}).get("text_all")).encode()).hexdigest()[:16]
        open(os.path.join(cdir, slug_of(r["url"]) + ".txt"), "w").write((r.get("render") or {}).get("text_visible") or "")
    needB = [u for u in urls if st["pages"].get(u, {}).get("layer_b_hash") != hashes.get(u) or any(f["url"] == u and f["severity"] in ("P0", "P1") for f in F)]
    briefs = write_layer_b(date, needB, base)
    doc = {"date": date, "base": base, "dry": dry, "pages": urls, "hubs": hubs, "findings": F, "layer_b_needed": needB, "layer_b_briefs": briefs,
           "hashes": hashes, "raw": os.path.relpath(rawp, ROOT), "started": now()}
    jsave(findings_path(date), doc)
    plan(date)
    if not dry:
        for u in urls: st["pages"].setdefault(u, {})["last_audit"] = now()
        jsave(STATE, st); golden_from(F, date)
    d = json.load(open(findings_path(date)))
    print(digest(d))
    print(f"\nfindings: {os.path.relpath(findings_path(date), ROOT)}; Layer B batches: {len(briefs)} ({', '.join(os.path.relpath(b, ROOT) for b in briefs)})")
    print("Next: spawn one reviewer per Layer B batch, then `hubctl live-audit record DATE FILE` for each; `hubctl live-audit drift DATE READBACK` "
          "for drift-check findings; then the fixes (`live-fix prepare/verify`) unless --dry; then `hubctl live-audit report DATE`.")

def findings_path(date): return os.path.join(AUD, date, "findings.json")

def write_layer_b(date, urls, base):
    out = []; cdir = os.path.join(CACHE, date)
    for n in range(0, len(urls), 4):
        chunk = urls[n:n + 4]; p = os.path.join(cdir, f"layerB-{n // 4 + 1}.md")
        L = [f"# Live audit Layer B, batch {n // 4 + 1} ({date}, {base})", "",
             "Read each page in full against rules/HUB_RULES.md, rules/claims.json (claims ledger), DECISIONS.md and LESSONS.md, and check its screenshots.",
             "Load the rules pack first: `.venv/bin/python3 ops/hubctl.py pack <url> --role reviewer`.",
             "Look for: wrong or unsourced claims, stale figures, off-topic or junk FAQ items, grammar, tone, audience narrowing, broken sentences where",
             "template text and CMS text meet, and layout breaks at 390 px. Severity: P0 false/unsourced claim, legal or medical risk, broken page, wrong",
             "content; P1 rule violation, typo, grammar, junk FAQ item, bad alt, stray characters; P2 style preference (backlog only).", "",
             f"Write a JSON list to `.cache/live/{date}/layerB-{n // 4 + 1}.json`: one object per issue with keys url, field (spec field name or",
             '"template"), severity, rule (HUB_RULES section or rule id), issue (one sentence), snippet (the live text, at most 160 chars), fix (the',
             "corrected text, or empty when it needs Divit). An empty list when a page is clean. Then run",
             f"`.venv/bin/python3 ops/hubctl.py live-audit record {date} .cache/live/{date}/layerB-{n // 4 + 1}.json`.", ""]
        for u in chunk:
            s = slug_of(u)
            L += [f"## {u}", f"- live URL: {base}{u}", f"- rendered text: `.cache/live/{date}/{s}.txt`",
                  f"- screenshots: `.cache/live/{date}/{s}-1440.png`, `.cache/live/{date}/{s}-390.png`", f"- spec: `{os.path.relpath(H.spath(u), ROOT)}`", ""]
        open(p, "w").write("\n".join(L)); out.append(p)
    return out

def cmd_record(args):
    date, fp = args[0], args[1]; d = json.load(open(findings_path(date))); new = json.load(open(fp))
    rows = []
    for x in new:
        f = {"url": x["url"], "field": x.get("field") or "template", "severity": x.get("severity", "P2"), "code": "B-" + re.sub(r"[^A-Za-z0-9]+", "", str(x.get("rule") or "review"))[:12],
             "rule": x.get("rule"), "msg": x.get("issue", "")[:300], "snippet": (x.get("snippet") or "")[:160], "suggested": x.get("fix") or "", "layer": "B"}
        f["fix"] = ("backlog" if f["severity"] == "P2" else "writer" if f["field"].split("#")[0] in AUTO_FIELDS and f["field"] not in ("h1", "meta_title") else "proposed")
        rows.append(f)
    ids = {f["id"] for f in d["findings"]}
    for f in number(rows, date):
        k, n = f["id"].rsplit("-", 1)[0], 1
        while f"{k}-{n}" in ids: n += 1
        f["id"] = f"{k}-{n}"; ids.add(f["id"])
    d["findings"] += rows
    st = jload(STATE, {"pages": {}})
    if not d.get("dry"):
        for u in {x["url"] for x in new} | set(d["layer_b_needed"]):
            if u in d["hashes"]: st["pages"].setdefault(u, {})["layer_b_hash"] = d["hashes"][u]
        jsave(STATE, st); golden_from(rows, date)
    d.setdefault("layer_b_recorded", []).append(os.path.relpath(fp, ROOT)); jsave(findings_path(date), d); plan(date)
    print(f"recorded {len(rows)} Layer B finding(s) from {fp}")

def cmd_drift(args):
    """Findings marked drift-check: compare the CMS item (readback) with the spec and our last write."""
    date, rb = args[0], args[1]; d = json.load(open(findings_path(date))); items = H._items_from_readback(rb)
    by = {it["id"]: it for it in items}; n = 0
    for f in d["findings"]:
        if f["fix"] != "drift-check": continue
        s = spec(f["url"]); it = by.get(s.get("item_id"))
        if not it: continue
        h = H.CFG["hubs"][H.hub_of(f["url"])]; k = (f["field"] or "").split("#")[0]
        if k not in h["fields"]: f["fix"] = "proposed"; continue
        want = H.export_fields(f["url"], s)[0].get(k) if k in s["fields"] else (s["images"].get(k) or {}).get("alt")
        got = it["fieldData"].get(h["fields"][k]); got = got.get("alt") if isinstance(got, dict) else got
        in_sync = bool(s.get("cms_draft")) and s["cms_draft"].get("fingerprint") == __import__("guards").fingerprint(s)
        if plain(got) != plain(want) and in_sync:
            f["fix"] = "drift-reported"; f["msg"] += " (CMS was edited outside our logs: drift, not overwritten)"; n += 1
        elif plain(got) != plain(want):
            f["fix"] = "auto" if k in AUTO_FIELDS and k not in ("h1", "meta_title") else "proposed"; f["msg"] += " (spec is ahead of the CMS: our change not yet sent)"
        else:
            f["fix"] = "proposed"; f["msg"] += " (CMS matches the spec: the template renders it differently)"
    jsave(findings_path(date), d); plan(date); print(f"drift-reported {n}")

# ---------------------------------------------------------------- fix plan, limits
def plan(date):
    d = json.load(open(findings_path(date))); per = {}
    for f in d["findings"]:
        if f["code"] == "A0-held-live" and f["fix"] == "unpublish":
            acts = [{"label": f"P0 {f['id']}: unpublish held item", "unpublish_collection_items": {"collection_id": f["collection"], "request": {"items": [{"id": f["item_id"]}]}}},
                    {"label": "read back", "list_collection_items": {"collection_id": f["collection"], "request": {"filter": {"id": {"eq": f["item_id"]}}, "limit": 1}}}]
            up = os.path.join(OUTD, f["id"] + ".unpublish.json"); jsave(up, acts); f["payload"] = os.path.relpath(up, ROOT)
            if f.get("status") != "unpublished": f["action"] = "unpublish-now"
            continue
        if f["severity"] == "P2": f["action"] = "backlog"; continue
        if f["fix"] in ("auto", "writer"):
            per.setdefault(f["url"], set()).add((f["field"] or "").split("#")[0])
            f["action"] = "would-fix" if d.get("dry") else ("fix" if f["fix"] == "auto" else "fix-by-writer")
        elif f["fix"] == "drift-reported": f["action"] = "drift-reported"
        elif f["fix"] == "drift-check": f["action"] = "drift-check"
        else: f["action"] = "proposed"
    for u, fields in per.items():
        if len(fields) > MAX_FIELDS:
            for f in d["findings"]:
                if f["url"] == u and f.get("action") in ("fix", "fix-by-writer", "would-fix"): f["action"] = "proposed"; f["msg"] += " (over 10 field changes: rework batch)"
    jsave(findings_path(date), d)

def digest(d):
    F = d["findings"]; c = lambda s: sum(f["severity"] == s for f in F)
    fx = [f for f in F if f.get("status") == "fixed"]; rb = [f for f in F if f.get("status") == "rolled-back"]
    wf = [f for f in F if f.get("action") in ("would-fix", "fix", "fix-by-writer") and f.get("status") not in ("fixed", "rolled-back")]
    pr = [f for f in F if f.get("action") == "proposed"]; dr = [f for f in F if f.get("action") == "drift-reported"]
    held = [f for f in F if f["code"] == "A0-held-live"]
    top = "".join(f"P0 HELD PAGE LIVE: {f['url']} (item {f.get('item_id')}): " + ("unpublished, verified. " if f.get("status") == "unpublished" else f"UNPUBLISH NOW: send {f.get('payload')}. ") for f in held)
    return top + (f"Live audit {d['date']}{' (DRY)' if d.get('dry') else ''} on {d['base']}: {len(d['pages'])} pages and {len(d['hubs'])} hubs checked; "
            f"issues P0 {c('P0')}, P1 {c('P1')}, P2 {c('P2')}; fixed {len(fx)}; rolled back {len(rb)}; "
            f"{'would fix' if d.get('dry') else 'fix pending'} {len(wf)}; proposals waiting for a go {len(pr)}; drift {len(dr)}; held pages live {len(held)}.")

# ---------------------------------------------------------------- fixes (steps 1-5 of the doc)
def find_issue(iid):
    for p in sorted(glob.glob(os.path.join(AUD, "*", "findings.json")), reverse=True):
        d = json.load(open(p))
        for f in d["findings"]:
            if f["id"] == iid: return p, d, f
    sys.exit(f"no issue {iid}")

def cmd_fix_prepare(args):
    iid = args[0]; rb = args[args.index("--readback") + 1]; p, d, f = find_issue(iid)
    if d.get("dry"): sys.exit("this run was --dry: nothing is changed")
    if f.get("action") not in ("fix", "fix-by-writer"): sys.exit(f"{iid}: action {f.get('action')} is not an automatic fix")
    url = f["url"]; s = spec(url); h = H.CFG["hubs"][H.hub_of(url)]
    it = next((x for x in H._items_from_readback(rb) if x["id"] == s.get("item_id")), None)
    if not it: sys.exit(f"{iid}: item {s.get('item_id')} not in {rb}")
    fd = it["fieldData"]; ex = H.export_fields(url, s)[0]; ch = {}
    for k, v in ex.items():
        if k in ("slug",) or (v in (None, "") and k in H.CFG["optional_fields"]): continue
        if fd.get(h["fields"][k]) != v: ch[k] = v
    sha = git("rev-parse", "HEAD")
    if git("status", "-sb").splitlines()[0].find("ahead") >= 0: sys.exit("push first: image URLs are pinned to a pushed commit")
    for k, im in s["images"].items():
        cur = fd.get(h["fields"][k]) or {}
        if im.get("file_id") != cur.get("fileId") or (im.get("alt") or "") != (cur.get("alt") or ""):
            ch[k] = {"url": f"{H.REPO_RAW}/{sha}/{im['path']}", "alt": im["alt"]} if im.get("file_id") != cur.get("fileId") else {"fileId": cur.get("fileId"), "url": cur.get("url"), "alt": im["alt"]}
    if not ch: sys.exit(f"{iid}: the spec equals the CMS; edit the spec first (writer) or nothing to fix")
    if len(ch) > MAX_FIELDS: sys.exit(f"{iid}: {len(ch)} fields change (max {MAX_FIELDS}): propose a rework instead")
    if "slug" in ch: sys.exit("never automatic: slug")
    import qc_hub as Q
    prim = (s.get("keywords") or {}).get("primary", "")
    for k in ("h1", "meta_title"):
        if k in ch and Q.kwn(prim) not in Q.kwn(plain(ch[k])): sys.exit(f"never automatic: the primary keyword would leave {k}")
    import ship
    iss = ship.qc_issues(url)
    if iss: sys.exit(f"QC TOTAL {len(iss)}: " + "; ".join(f"{i['code']} {i['field']}" for i in iss[:5]))
    if "faq" in ch:
        import paa_gate as PG
        items, page = PG.run_spec(PG.Gate(url))
        if sum(i["verdict"] != "reject" for i in items) != 10 or page: sys.exit("PAA gate is not 10/10")
    if s.get("image_brief") and not ship.images_current(dict(s, _path=H.spath(url))): sys.exit("images are not current: re-render first")
    # Before-value first, in git and pushed, then the payload (Divit 2026-10-10: refuse to write if the before-value is not in HEAD).
    before = {"id": it["id"], "collection": h["collection_id"], "lastUpdated": it.get("lastUpdated"), "fieldData": {h["fields"][k]: fd.get(h["fields"][k]) for k in ch}}
    bp = os.path.join(ROOT, f["before_file"]) if f.get("before_file") and f.get("status") == "before-saved" else \
         os.path.join(ROOT, "childedits", today(), f"{slug_of(url)}.{iid}.before.json")
    if not os.path.exists(bp) or json.load(open(bp)) != before:
        jsave(bp, before); f.update(status="before-saved", before_file=os.path.relpath(bp, ROOT)); jsave(p, d)
    ok, why = before_committed(bp)
    if not ok:
        sys.exit(f"{iid}: before-value saved to {os.path.relpath(bp, ROOT)} but {why}. Commit and push it (ops/sync.sh), then rerun prepare with a fresh read-back.")
    acts = [{"label": f"live fix {iid}: update {len(ch)} field(s)", "update_collection_items": {"collection_id": h["collection_id"], "request": {"items": [{"id": it["id"], "fieldData": {h["fields"][k]: v for k, v in ch.items()}}]}}},
            {"label": f"live fix {iid}: publish this item only", "publish_collection_items": {"collection_id": h["collection_id"], "request": {"items": [{"id": it["id"]}]}}},
            {"label": "read back", "list_collection_items": {"collection_id": h["collection_id"], "request": {"filter": {"id": {"eq": it["id"]}}, "limit": 1}}}]
    op = os.path.join(OUTD, iid + ".json"); jsave(op, acts)
    covers = [x["id"] for x in d["findings"] if x["url"] == url and x["id"] != iid and x.get("action") in ("fix", "fix-by-writer") and x.get("status") not in ("fixed", "rolled-back")]
    f.update(status="prepared", before_file=os.path.relpath(bp, ROOT), payload=os.path.relpath(op, ROOT), fields_changed=sorted(ch), cms_item=it["id"], covers=covers,
             before_text={k: plain(fd.get(h["fields"][k]) if not isinstance(fd.get(h["fields"][k]), dict) else fd[h["fields"][k]].get("alt")) for k in ch},
             after_text={k: plain(v if not isinstance(v, dict) else v.get("alt")) for k, v in ch.items()})
    jsave(p, d); print(f"{op}: send as data_cms_tool actions (update, item publish, read back); save the response, then `hubctl live-fix verify {iid} RESPONSE`")

def before_committed(bp):
    """The before-value file is tracked in HEAD, unchanged since, and HEAD is on origin/main."""
    rel = os.path.relpath(bp, ROOT); run = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True).returncode
    if run("cat-file", "-e", f"HEAD:{rel}"): return False, "it is not committed"
    if run("diff", "--quiet", "HEAD", "--", rel): return False, "it changed since the last commit"
    run("fetch", "-q", "origin", "main")
    if run("merge-base", "--is-ancestor", "HEAD", "origin/main"): return False, "the commit is not pushed"
    return True, ""

def cmd_fix_approve(args):
    """A proposal Divit approved becomes a writer fix: `live-fix approve ISSUE --by divit --note "..."`."""
    iid = args[0]; p, d, f = find_issue(iid); by = args[args.index("--by") + 1] if "--by" in args else ""
    if f.get("action") != "proposed": sys.exit(f"{iid}: action is {f.get('action')}, not proposed")
    if by.lower() != "divit": sys.exit("only Divit approves a proposal (--by divit)")
    note = args[args.index("--note") + 1] if "--note" in args else ""
    f.update(fix="writer", action="fix-by-writer", approved=f"Divit {now()}" + (f": {note}" if note else "")); jsave(p, d); ledger_sync()
    print(f"{iid}: approved; edit the spec, then `hubctl live-fix prepare {iid} --readback F`")

def cmd_fix_add(args):
    """A finding from an approved sweep: `live-fix add DATE URL FIELD CODE SEV "MSG" [--source S]` (action fix-by-writer)."""
    date, url, field, code, sev, msg = args[:6]; src = args[args.index("--source") + 1] if "--source" in args else ""
    p = findings_path(date); d = json.load(open(p)); n = sum(x["url"] == url and x["code"] == code for x in d["findings"]) + 1
    iid = f"{date.replace('-', '')}-{slug_of(url)}-{code}-{n}"
    d["findings"].append({"id": iid, "url": url, "field": field, "severity": sev, "code": code, "rule": code, "layer": "sweep", "msg": msg, "snippet": "",
                          "suggested": "", "fix": "writer", "action": "fix-by-writer", "source": src, "found_at": now()})
    jsave(p, d); ledger_sync(); print(iid)

def cmd_fix_apply(args):
    """Deterministic fixes (rules/live_audit.json deterministic_codes) applied to the spec field; then QC as usual in prepare."""
    iid = args[0]; p, d, f = find_issue(iid)
    if d.get("dry"): sys.exit("this run was --dry: nothing is changed")
    if f["code"] not in CONF["deterministic_codes"]: sys.exit(f"{iid}: {f['code']} needs a writer (`hubctl live-fix brief {iid}`)")
    url = f["url"]; sp = H.spath(url); raw = open(sp).read(); s = json.loads(raw); k = (f["field"] or "").split("#")[0]
    if f["code"] in ("A7-nonlive", "A7-link", "A8-format", "A8-og"):
        print(f"{iid}: no spec edit; the export (links to non-live pages become text) or the pinned image file is the fix; run prepare"); return
    UM = us_map()
    def fx(v):
        v = ZW.sub("", v); v = CTRL.sub("", v)
        v = re.sub(r"&(?:amp;)+(amp|lt|gt|quot|#\d+|nbsp);", r"&\1;", v)
        v = v.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '\\"' if k == "faq" else '"').replace("\u201d", '\\"' if k == "faq" else '"')
        v = re.sub(r"(?<=\S) {2,}(?=\S)", " ", v)
        v = REPEAT.sub(lambda m: m.group(0) if m.group(1).lower() in CONF["repeat_ok"] else m.group(1), v)
        return re.sub(r"[A-Za-z]+", lambda m: (UM[m.group(0).lower()].capitalize() if m.group(0)[0].isupper() else UM[m.group(0).lower()]) if m.group(0).lower() in UM else m.group(0), v)
    if k in s["fields"]: old = s["fields"][k]; s["fields"][k] = fx(old); changed = old != s["fields"][k]
    elif k in s.get("images", {}): old = s["images"][k]["alt"]; s["images"][k]["alt"] = fx(old); changed = old != s["images"][k]["alt"]
    else: sys.exit(f"{iid}: field {k} is not in the spec")
    if not changed: sys.exit(f"{iid}: nothing to change in {k}")
    open(sp, "w").write(json.dumps(s, indent=1, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""))
    print(f"{iid}: {k} fixed in the spec; commit and push, then `hubctl live-fix prepare {iid} --readback F`")

def cmd_fix_brief(args):
    iid = args[0]; p, d, f = find_issue(iid); bp = os.path.join(CACHE, d["date"], f"fix-{iid}.md")
    L = [f"# Live audit fix {iid}", "", f"Page {f['url']} (spec `{os.path.relpath(H.spath(f['url']), ROOT)}`), field `{f['field']}`, {f['severity']} {f['code']}.",
         f"Issue: {f['msg']}", f"Live text: {f.get('snippet', '')}", f"Reviewer's suggested fix: {f.get('suggested', '')}", "",
         "Edit ONLY this field in the spec (one pass, per HUB_RULES). Never the slug, never the primary keyword in the H1 or meta title, never a claim",
         "outside rules/claims.json. If the FAQ changes, rebuild the awbFAQ embed in Python and keep the gate at 10/10. Then run",
         f"`.venv/bin/python3 ops/hubctl.py ship-qc {f['url']}` until TOTAL 0, and report the before and after text."]
    os.makedirs(os.path.dirname(bp), exist_ok=True); open(bp, "w").write("\n".join(L) + "\n"); print(bp)

def rerun_layer_a(url, base):
    date = today(); cdir = os.path.join(CACHE, date, "verify"); os.makedirs(cdir, exist_ok=True)
    man = {"pages": [manifest_entry(url)], "hubs": []}; mp = os.path.join(cdir, slug_of(url) + ".manifest.json"); jsave(mp, man)
    rp = os.path.join(cdir, slug_of(url) + ".raw.json")
    subprocess.run(["node", os.path.join(ROOT, "ops", "live_audit.mjs"), mp, rp, "--base", base], cwd=ROOT, check=True)
    return evaluate(json.load(open(rp)), man, base)

def cmd_fix_verify(args):
    iid, resp = args[0], args[1]; p, d, f = find_issue(iid); url = f["url"]; s = spec(url); h = H.CFG["hubs"][H.hub_of(url)]
    raw = json.load(open(resp)); errs = [json.loads(b["text"]).get("error") for b in raw if b.get("text", "").lstrip().startswith("{") and json.loads(b["text"]).get("error")]
    it = next((x for x in H._items_from_readback(resp) if x["id"] == s.get("item_id")), None)
    ok = not errs and it is not None
    if ok:
        ex = H.export_fields(url, s)[0]
        ok = all(it["fieldData"].get(h["fields"][k]) == ex[k] for k in f["fields_changed"] if k in ex)
    after = rerun_layer_a(url, d["base"]) if ok else []
    still = [x for x in after if x["code"] == f["code"] and (x["field"] or "") == (f["field"] or "")]
    worse = [x for x in after if x["severity"] in ("P0", "P1") and x["code"] not in {y["code"] for y in d["findings"] if y["url"] == url}]
    if ok and not still and not worse:
        import guards as G
        s["cms_draft"] = {"fingerprint": G.fingerprint(s), "sha": git("rev-parse", "--short", "HEAD"), "date": now(), "verified": True, "note": f"live fix {iid}"}
        json.dump(s, open(H.spath(url), "w"), indent=1, ensure_ascii=False)
        f.update(status="fixed", fixed_at=now(), commit=git("rev-parse", "--short", "HEAD"), published_at=now(), verified=True)
        for x in d["findings"]:   # one page-level update covers every fix on that page
            if x["id"] in (f.get("covers") or []):
                x.update(status="fixed", fixed_at=f["fixed_at"], commit=f["commit"], published_at=f["published_at"], verified=True, cms_item=f["cms_item"],
                         before_file=f["before_file"], fixed_by=iid)
        print(f"FIXED {iid}" + (f" (+{len(f.get('covers') or [])} covered)" if f.get("covers") else ""))
    else:
        rp = write_rollback(f, d)
        for x in d["findings"]:
            if x["id"] in (f.get("covers") or []): x.update(status="rollback-pending", rolled_with=iid)
        f.update(status="rollback-pending", verify_note=("; ".join(map(str, errs)) or "read-back mismatch" if not ok else f"Layer A still fails ({len(still)}) or new issues ({len(worse)})"))
        print(f"VERIFY FAILED {iid}: SEND {rp} NOW, then `hubctl live-rollback {iid} --done RESPONSE`")
    jsave(p, d); ledger_sync()

def write_rollback(f, d):
    b = json.load(open(os.path.join(ROOT, f["before_file"])))
    acts = [{"label": f"ROLLBACK {f['id']}: before-values", "update_collection_items": {"collection_id": b["collection"], "request": {"items": [{"id": b["id"], "fieldData": b["fieldData"]}]}}},
            {"label": f"ROLLBACK {f['id']}: publish this item only", "publish_collection_items": {"collection_id": b["collection"], "request": {"items": [{"id": b["id"]}]}}},
            {"label": "read back", "list_collection_items": {"collection_id": b["collection"], "request": {"filter": {"id": {"eq": b["id"]}}, "limit": 1}}}]
    rp = os.path.join(OUTD, f["id"] + ".rollback.json"); jsave(rp, acts); f["rollback_file"] = os.path.relpath(rp, ROOT); return rp

def cmd_held_done(args):
    """held-done ISSUE RESPONSE: the unpublish was sent; the read-back must show isDraft true; then re-check the URLs."""
    iid, resp = args[0], args[1]; p, d, f = find_issue(iid)
    it = next((x for x in H._items_from_readback(resp) if x["id"] == f.get("item_id")), None)
    ok = it is not None and it.get("isDraft") is True
    codes = {h: subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", h.rstrip("/") + f["url"]], capture_output=True, text=True).stdout for h in CONF["held_hosts"]}
    f.update(status="unpublished" if ok else "unpublish-unverified", unpublished_at=now(), recheck=codes); jsave(p, d); ledger_sync()
    print(("UNPUBLISHED " if ok else "UNPUBLISH NOT VERIFIED ") + iid + f" (isDraft {it.get('isDraft') if it else '?'}; now {codes}; the CDN can serve the old page for a few minutes)")

def cmd_rollback(args):
    iid = args[0]; p, d, f = find_issue(iid)
    if not f.get("before_file"): sys.exit(f"{iid}: no before-value (nothing was changed)")
    if "--done" in args:
        resp = args[args.index("--done") + 1]; b = json.load(open(os.path.join(ROOT, f["before_file"])))
        it = next((x for x in H._items_from_readback(resp) if x["id"] == b["id"]), None)
        ok = it is not None and all(it["fieldData"].get(k) == v or (isinstance(v, dict) and (it["fieldData"].get(k) or {}).get("alt") == v.get("alt")) for k, v in b["fieldData"].items())
        f.update(status="rolled-back" if ok else "rollback-unverified", rolled_back_at=now())
        for x in d["findings"]:
            if x["id"] in (f.get("covers") or []): x.update(status=f["status"], rolled_back_at=f["rolled_back_at"])
        jsave(p, d); ledger_sync()
        print(("ROLLED BACK " if ok else "ROLLBACK NOT VERIFIED ") + iid); return
    rp = write_rollback(f, d); jsave(p, d); print(f"{rp}: send it, then `hubctl live-rollback {iid} --done RESPONSE`")

# ---------------------------------------------------------------- ledger, day files, report
def ledger_sync():
    L = jload(LEDGER_J, {"rows": {}})
    for p in sorted(glob.glob(os.path.join(AUD, "*", "findings.json"))):
        d = json.load(open(p))
        if d.get("dry"): continue
        for f in d["findings"]:
            st = f.get("status") or {"proposed": "proposed", "backlog": "backlog", "drift-reported": "drift-reported"}.get(f.get("action"), f.get("action") or "open")
            L["rows"][f["id"]] = {"id": f["id"], "date": d["date"], "url": f["url"], "field": f["field"], "severity": f["severity"], "rule": f.get("rule") or f["code"],
                                  "desc": f["msg"][:140], "commit": f.get("commit", ""), "item": f.get("cms_item", ""), "published": f.get("published_at", ""),
                                  "verified": "yes" if f.get("verified") else "", "rollback": f.get("before_file", ""), "status": st}
    jsave(LEDGER_J, L)
    head = ["id", "date", "url", "field", "severity", "rule", "description", "fix commit", "CMS item", "published at", "verified", "rollback file", "status"]
    rows = ["# Live audit ledger", "", "One row per issue (docs/LIVE_AUDIT.md). Generated from audits/live/*/findings.json by ops/live_audit.py; do not edit by hand.", "",
            "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in sorted(L["rows"].values(), key=lambda r: r["id"], reverse=True):
        rows.append("| " + " | ".join(str(r[k]).replace("|", "/") for k in ("id", "date", "url", "field", "severity", "rule", "desc", "commit", "item", "published", "verified", "rollback", "status")) + " |")
    open(LEDGER_MD, "w").write("\n".join(rows) + "\n")

def cmd_report(args):
    date = args[0]; d = json.load(open(findings_path(date))); F = d["findings"]
    for u in sorted({f["url"] for f in F}):
        mine = [f for f in F if f["url"] == u]; s = slug_of(u) if u.count("/") > 1 else "hub" + u.replace("/", "-")
        L = [f"# {u}: live audit {date}{' (DRY)' if d.get('dry') else ''}", "", f"Base: {d['base']}", ""]
        for f in mine:
            L += [f"## {f['id']} ({f['severity']}, {f['code']}, {f.get('action')}{', ' + f['status'] if f.get('status') else ''})", f"- field: {f['field']}", f"- caught by: {f['code']} (Layer {f['layer']}): {f['msg']}"]
            if f.get("snippet"): L.append(f"- live text: {f['snippet']}")
            for k in f.get("fields_changed") or []:
                L += [f"- {k} before: {f['before_text'].get(k, '')[:500]}", f"- {k} after: {f['after_text'].get(k, '')[:500]}"]
            L.append("")
        open(os.path.join(AUD, date, s + ".md"), "w").write("\n".join(L))
    if not d.get("dry"): ledger_sync()
    hhmm = datetime.datetime.now().strftime("%H%M"); rp = os.path.join(ROOT, "reports", date, f"{hhmm}-live-audit{'-dry' if d.get('dry') else ''}.md")
    os.makedirs(os.path.dirname(rp), exist_ok=True)
    act = lambda a: [f for f in F if f.get("action") == a]
    L = ["# Live audit " + date + (" (DRY run: nothing changed)" if d.get("dry") else ""), "", "## Digest for Divit", "", digest(d), ""]
    for title, rows in (("P0: held pages live (unpublish at once)", [f for f in F if f["code"] == "A0-held-live"]), ("Would fix (auto or by a writer)" if d.get("dry") else "Fixes", [f for f in F if f.get("action") in ("would-fix", "fix", "fix-by-writer")]),
                        ("Proposals waiting for a go", act("proposed")), ("Drift (edited in Webflow, reported, not overwritten)", act("drift-reported")),
                        ("Needs a CMS read to classify (drift check)", act("drift-check")), ("Backlog (P2)", act("backlog"))):
        L += [f"### {title} ({len(rows)})", ""] + [f"- {f['severity']} {f['url']} `{f['field']}` {f['code']}: {f['msg']}{' [' + f['status'] + ']' if f.get('status') else ''}" for f in rows[:80]] + [""]
    L += ["## Request", "", "Scheduled or requested live audit per docs/LIVE_AUDIT.md (DECISIONS 2026-10-09).", "",
          "## Actions and results", "", f"- Layer A on {len(d['pages'])} pages and {len(d['hubs'])} hubs at {d['base']}; Layer B batches: {len(d.get('layer_b_briefs') or [])}; recorded: {len(d.get('layer_b_recorded') or [])}.",
          f"- Findings: `audits/live/{date}/findings.json`; per-page files `audits/live/{date}/<slug>.md`; ledger `audits/live/LEDGER.md`.", "",
          "## Webflow calls", "", "- " + ("none (dry run)" if d.get("dry") else "see the ledger rows for this date (update and item publish per fix, read back)"), "",
          "## Not done", "", "- Proposals and drift wait for Divit.", "", "## Open questions for Divit", "", "- Each proposal above has a recommended fix in its per-page file."]
    open(rp, "w").write("\n".join(L) + "\n"); print(rp); print(digest(d))

def main(args):
    sub = args[0] if args and not args[0].startswith("--") else "run"
    rest = args[1:] if sub != "run" or (args and args[0] == "run") else args
    {"run": cmd_run, "record": cmd_record, "drift": cmd_drift, "plan": lambda a: plan(a[0]), "report": cmd_report, "held-done": cmd_held_done}[sub](rest)

def fix_main(args):
    {"apply": cmd_fix_apply, "brief": cmd_fix_brief, "prepare": cmd_fix_prepare, "verify": cmd_fix_verify,
     "approve": cmd_fix_approve, "add": cmd_fix_add}[args[0]](args[1:])

if __name__ == "__main__":
    main(sys.argv[1:])
