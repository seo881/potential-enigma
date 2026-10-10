"""paa_gate.py: the PAA gate PA1-PA15 (PA14 brands, PA15 file formats: Divit 2026-10-09) (handover 2026-10-08 section 5; approved by Divit 2026-10-08).

  hubctl paa URL          gate the page's AlsoAsked pull (private/alsoasked/<slug>.json, from ops/alsoasked_pull.py)
  hubctl paa URL --spec   gate the spec's current FAQ (spec.faq_sources + fields.faq); PA1b: no answer may share a 6-word run
                          with the pull's answer_*/ai_overview* text (provenance only, never FAQ copy)
  hubctl paa-resource URL write AlsoAsked provenance into matching faq_sources items; a DataForSEO-PAA item with no match
                          that carries a secondary becomes source secondary (ref = that secondary, paa_ref = old ref); text byte-identical
  --cand                  also admit the page's SAFE synonym candidates (rules/paa_synonym_candidates.json; not yet approved)

Principle: a question is rejected unless it proves it belongs on the page. Each question gets pass, reject or flag
(needs a human judgment; never silently passed) with every reason by rule ID. Verdicts go to
private/alsoasked/verdicts/<slug>[.faq].json (git-ignored); one summary line goes to audit/paa/summary.md.
Not wired into the QC TOTAL; F4 is not retired yet. Patterns and lists: rules/paa_patterns.json,
rules/paa_blocklist.json, rules/paa_synonyms.json.
"""
import datetime, glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))
R = lambda f: json.load(open(os.path.join(ROOT, "rules", f)))
STOP = set("a an the of for to in on at by with and or is are do does did i we you my our your can how what which who when where why "
           "should would will it its be there this that from as if so any".split())
PROV = ("tool", "query", "depth", "parent", "fetched", "original")
JACCARD_DUP = 0.8      # PA9/PA10 same-intent threshold on content words (tune after the first full run)
MAX_RESPONDENT, MAX_BRANDED, MIN_ON_TOPIC, N_FAQ, MIN_SECONDARIES = 2, 0, 8, 10, 6   # PA8 brand cap 0 (Divit 2026-10-09)

def norm(s): return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9'.&-]+", " ", s.lower().replace("’", "'"))).strip()
def stem(w): return re.sub(r"(ies|es|s|ing|ed)$", "", w) if len(w) > 4 else w
SAME = {"make": "create", "build": "create", "design": "create", "setup": "create", "generate": "create"}  # same intent for PA9/PA10
def content(s): return {SAME.get(stem(w), stem(w)) for w in re.split(r"[\s-]+", norm(s).replace("set up", "setup")) if w and w not in STOP}
def jacc(a, b): return len(a & b) / len(a | b) if a | b else 0.0
def has(term, q): return re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", q) is not None
def phrase_re(p):  # head phrase, each word optionally plural, space or hyphen between words
    ws = norm(p).split()
    return re.compile(r"(?<![a-z0-9])" + r"[\s-]+".join(re.escape(w) + r"(?:s|es)?" for w in ws) + r"(?![a-z0-9])")

def hub_of(url):
    for k, h in CFG["hubs"].items():
        if url.startswith(h["path"] + "/"): return k, h
    sys.exit(f"no hub owns {url}")

class Gate:
    def __init__(self, url, extra_heads=()):
        self.url, self.slug = url, url.rsplit("/", 1)[1]
        self.hub, h = hub_of(url); self.dir, self.hub_path = h["repo_dir"], h["path"]
        self.spec_path = os.path.join(ROOT, "specs", self.dir, self.slug + ".json")
        self.spec = json.load(open(self.spec_path)) if os.path.exists(self.spec_path) else {}
        self.primary = (self.spec.get("keywords") or {}).get("primary") or self.slug.replace("-", " ")
        self.heads = [phrase_re(p) for p in [self.primary] + R("paa_synonyms.json")["pages"].get(self.slug, []) + list(extra_heads)]
        # PA3 widened (Divit, 2026-10-08): head phrase reordered/inflected, or an approved secondary of the page (K8 test)
        self.head_words = [stem(w) for w in norm(self.primary).split()]
        secs = set((self.spec.get("keywords") or {}).get("secondaries_used") or [])
        kmp = os.path.join(ROOT, "plan", "keyword_map.json")
        if os.path.exists(kmp):
            secs |= {x["kw"] for x in (json.load(open(kmp)).get(url, {}) or {}).get("secondaries", []) if x.get("kw")}
        self.secondaries = sorted(secs)
        self.bl, self.pt = R("paa_blocklist.json"), R("paa_patterns.json")
        for e in self.bl["per_page"].get(self.slug, []):
            if not e.get("reason"): sys.exit(f"rules/paa_blocklist.json per_page {self.slug}: entry without a reason: {e.get('q')}")
        self.skip = {norm(e["q"]): e["reason"] for e in self.bl["per_page"].get(self.slug, [])}
        lib = os.path.join(ROOT, "rules", "competitors", self.dir + ".json")
        self.library = [c.lower() for c in json.load(open(lib)).get("competitors", {})] if os.path.exists(lib) else []
        self.siblings = []  # PA10: every other spec in the hub, with its head phrase
        for p in glob.glob(os.path.join(ROOT, "specs", self.dir, "*.json")):
            if os.path.basename(p).startswith("_") or p == self.spec_path: continue
            try: s = json.load(open(p))
            except Exception: continue
            prim = (s.get("keywords") or {}).get("primary") or ""
            for f in s.get("faq_sources") or []:
                if f.get("q"): self.siblings.append((s.get("url") or os.path.basename(p), prim, f["q"], content(f["q"])))

    def pa3_widened(self, q):
        qw = [stem(w) for w in re.split(r"[\s-]+", q) if w]
        hw = self.head_words; win = max(4, len(hw))
        if hw and all(w in qw for w in hw):
            for i in range(len(qw)):
                if set(hw) <= set(qw[i:i + win]): return "reordered or inflected head phrase"
        qs = set(qw)
        for k in self.secondaries:
            kw = [stem(w) for w in re.split(r"[\s-]+", norm(k)) if w]
            if kw and set(kw) <= qs: return f"secondary: {k}"
        return None

    def asker(self, q):
        if any(re.search(p, q) for p in self.pt["respondent"]): return "respondent"
        if any(re.search(p, q) for p in self.pt["builder"]): return "builder"
        return None

    def domain(self, q): return [d for d, ws in self.pt["domains"].items() if any(has(w, q) for w in ws)]

    def judge(self, item):
        """item: {q, prov, source}. Returns list of (rule, 'reject'|'flag'|'note', reason)."""
        q, out = norm(item["q"]), []
        prov, src = item.get("prov") or {}, item.get("source", "alsoasked")
        if item.get("n") in (1, 2): src = "slot"  # definition and how-to-build are template slots: exempt from PA1/PA2 (DECISIONS 2026-10-08)
        # PA1 provenance: PAA items come from AlsoAsked only (US, English) with full provenance
        if src in ("paa", "alsoasked"):
            if prov.get("tool") != "alsoasked-api": out.append(("PA1", "reject", f"PAA item not from AlsoAsked (tool {prov.get('tool') or 'dataforseo'})"))
            else:
                miss = [k for k in PROV if prov.get(k) in (None, "") and not (k == "parent" and prov.get("depth") == 1)]
                if miss: out.append(("PA1", "reject", "missing provenance: " + ", ".join(miss)))
                if prov.get("region") != "us" or prov.get("language") != "en" or prov.get("fallback"): out.append(("PA1", "reject", "not a US English result (or fallback)"))
            # PA2 depth
            d = prov.get("depth")
            if d and d >= 3 and not prov.get("depth_reason"): out.append(("PA2", "reject", f"depth {d} without a written reason"))
            if d == 2 and item.get("parent_verdict") == "reject": out.append(("PA2", "reject", "level 2 under a rejected parent"))
            if d == 2 and item.get("parent_verdict") == "flag": out.append(("PA2", "flag", "level 2 under a flagged parent"))
        # PA3 entity match: full head phrase or an approved synonym; a shared word never qualifies
        if not any(h.search(q) for h in self.heads):
            via = self.pa3_widened(q)
            if via: out.append(("PA3w", "note", via))
            else: out.append(("PA3", "reject", f'no head phrase "{self.primary}" (exact, reordered or inflected), approved secondary or synonym'))
        # PA4 wrong sense: global blocklist and the per-page skip list
        ws = [w for w in self.bl["wrong_sense"] if has(w, q)]
        if ws: out.append(("PA4", "reject", "wrong-sense term: " + ", ".join(ws)))
        if q in self.skip: out.append(("PA4", "reject", "per-page skip: " + self.skip[q]))
        if any(re.search(r"\b(apply|applying|application) (for|to) (the |an? )?" + h.pattern, q) for h in self.heads):
            out.append(("PA4", "reject", "treats the page's document as something one applies for (wrong sense)"))
        ctx = norm(item.get("ctx") or "")  # the AlsoAsked answer source: provenance used only to judge the sense, never copied
        cw = [w for w in self.bl["wrong_sense"] + self.bl.get("wrong_sense_source", []) if has(w, ctx)]
        if cw: out.append(("PA4", "reject", "answer source is about a different sense: " + ", ".join(cw[:3])))
        cn = [w for w in self.bl["non_us"] if has(w, ctx)]
        if cn: out.append(("PA5", "reject", "answer source is non-US: " + ", ".join(cn[:3])))
        # PA5 US audience
        nu = [w for w in self.bl["non_us"] if has(w, q)]
        if nu: out.append(("PA5", "reject", "non-US term: " + ", ".join(nu)))
        # PA6 asker
        a = self.asker(q); item["asker"] = a
        if a is None: out.append(("PA6", "flag", "asker unclassified (builder/respondent/unrelated): needs judgment"))
        # PA7 advice risk
        dom = self.domain(q); adv = any(re.search(p, q) for p in self.pt["advice"])
        if adv and dom: out.append(("PA7", "reject", "advice question in " + "/".join(dom)))
        elif adv: out.append(("PA7", "flag", "advice-shaped question: check it needs no professional advice"))
        elif dom and re.match(r"^(what|which) (is|are) ", q): out.append(("PA7", "flag", "definitional " + "/".join(dom) + " question: needs a primary (.gov or statute) source"))
        # PA8 third-party brands
        retail = [b for b in self.bl["retail_brands"] if has(b, q)]
        tools = [b for b in self.bl["tool_brands"] if has(b, q) and b not in self.library]
        lib = [b for b in self.library if has(b, q)]; item["brands"] = lib
        if retail: out.append(("PA8", "reject", "retailer or gift brand: " + ", ".join(retail)))
        if tools: out.append(("PA8", "reject", "brand not in the competitor library: " + ", ".join(tools)))
        # PA14 no brand or product names (Divit 2026-10-09): listed brands reject; an unlisted capitalised name is flagged
        raw = item.get("q") or ""
        br = [b for b in self.bl.get("pa14_brands", []) if has(b.lower(), q)]
        if br: out.append(("PA14", "reject", "brand or product name: " + ", ".join(sorted(set(br))[:4])))
        ok_caps = set(self.bl.get("pa14_proper_noun_ok", []))
        caps = [w for i, w in enumerate(re.findall(r"[A-Za-z0-9][A-Za-z0-9.'-]*", raw)) if i > 0 and w[0].isupper() and w.rstrip("?.'s") not in ok_caps and w not in ok_caps and w.lower().rstrip("?.") not in self.bl.get("pa15_formats", [])]
        if caps and not br: out.append(("PA14", "flag", "capitalised name, possibly a brand: " + ", ".join(caps[:3])))
        # PA15 no file formats or download-style asks
        fm = [f for f in self.bl.get("pa15_formats", []) if has(f, q)]
        if fm: out.append(("PA15", "reject", "file format or download ask: " + ", ".join(fm[:3])))
        # PA10 one page per question per hub: the page whose head phrase the question carries owns it
        cq = content(q)
        for surl, sprim, sq, sc in self.siblings:
            if jacc(cq, sc) < JACCARD_DUP: continue
            mine = any(h.search(q) for h in self.heads); theirs = bool(sprim) and phrase_re(sprim).search(q)
            # the longer head phrase is the more specific owner when both match (tournament registration form > registration form)
            if mine and theirs: mine = len(norm(self.primary)) >= len(norm(sprim))
            if mine: out.append(("PA10", "note", f"same question on {surl}; this page owns it"))
            elif theirs: out.append(("PA10", "reject", f"belongs to {surl} (\"{sq[:50]}\")"))
            else: out.append(("PA10", "flag", f"same question on {surl}: decide one owner"))
            break
        return out

    def verdict(self, reasons):
        if any(r[1] == "reject" for r in reasons): return "reject"
        if any(r[1] == "flag" for r in reasons): return "flag"
        return "pass"

    def finish(self, items):
        """Within-page rules: PA6 respondent cap, PA8 brand cap, PA9 same-intent duplicates (in item order)."""
        kept, resp, brand = [], 0, 0
        for it in items:
            if it["verdict"] == "reject": continue
            c = content(it["q"])
            dup = next((k for k in kept if jacc(c, content(k["q"])) >= JACCARD_DUP), None)
            if dup: it["reasons"].append(("PA9", "reject", f'same intent as "{dup["q"][:50]}"'))
            if it.get("asker") == "respondent":
                resp += 1
                if resp > MAX_RESPONDENT: it["reasons"].append(("PA6", "reject", f"more than {MAX_RESPONDENT} respondent questions"))
            if it.get("brands"):
                brand += 1
                if brand > MAX_BRANDED: it["reasons"].append(("PA8", "reject", f"more than {MAX_BRANDED} third-party brand question"))
            it["verdict"] = self.verdict(it["reasons"])
            if it["verdict"] != "reject": kept.append(it)
        return items

def flatten(d):
    """AlsoAsked API response (schema from ops/alsoasked_schema.py): response.queries[].results[] question tree."""
    m, r, out = d["_meta"], d["response"], []
    def walk(nodes, depth, parent, term, fb):
        for n in nodes or []:
            prov = {"tool": m.get("tool"), "query": term, "depth": depth, "parent": parent, "fetched": m.get("fetched"),
                    "original": n.get("question"), "region": r.get("region"), "language": r.get("language"), "fallback": fb}
            ctx = " ".join(x for x in [n.get("answer_page_title"), n.get("answer_href"), n.get("answer_excerpt")] if isinstance(x, str))
            out.append({"q": n["question"], "source": "alsoasked", "prov": prov, "parent_q": parent, "ctx": ctx})
            walk(n.get("results"), depth + 1, n["question"], term, fb)
    for q in r.get("queries") or []: walk(q.get("results"), 1, None, q.get("term"), q.get("language_fallback") or q.get("region_fallback"))
    return out

def pull_path(slug): return os.path.join(ROOT, "private", "alsoasked", slug + ".json")

def answer_shingles(d, n=6):
    """PA1b: every 6-word run in the pull's answer_* and ai_overview* text (provenance only, never FAQ copy)."""
    txt = []
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.startswith(("answer_", "ai_overview")):
                    txt.extend([v] if isinstance(v, str) else [x for x in v if isinstance(x, str)] if isinstance(v, list) else [])
                else: walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(d["response"]); sh = set()
    for t in txt:
        w = norm(t).split(); sh |= {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}
    return sh

def match_pull(q, nodes):
    """Best AlsoAsked node for a question under the same-intent rule (exact wording first, then Jaccard >= JACCARD_DUP, shallowest)."""
    nq, cq = norm(q), content(q); best = None
    for it in nodes:
        sc = 1.0 if norm(it["q"]) == nq else jacc(cq, content(it["q"]))
        if sc >= JACCARD_DUP and (best is None or (sc, -it["prov"]["depth"]) > (best[0], -best[1]["prov"]["depth"])): best = (sc, it)
    return best[1] if best else None

def resource(url):
    """hubctl paa-resource: write AlsoAsked provenance into faq_sources items whose question matches the pull. No copy changes."""
    g = Gate(url); p = pull_path(g.slug)
    if not os.path.exists(p): sys.exit(f"no AlsoAsked pull for {g.slug}")
    nodes = flatten(json.load(open(p)))
    before_raw = open(g.spec_path, "rb").read(); spec = json.loads(before_raw)
    snap = lambda s: (s["fields"].get("faq"), [(f.get("q"), f.get("source"), f.get("ref")) for f in s.get("faq_sources") or []])
    before = snap(spec); n = 0
    secs = (spec.get("keywords") or {}).get("secondaries_used") or []; rc = 0
    for f in spec.get("faq_sources") or []:
        m = match_pull(f["q"], nodes)
        if m:
            f["prov"] = {k: m["prov"][k] for k in ("tool", "query", "depth", "parent", "fetched", "original", "region", "language")}; n += 1
        elif f.get("source") == "paa":  # DataForSEO PAA with no AlsoAsked match: a secondary if its question carries one (PA12 test)
            k = next((k for k in secs if content(k) and content(k) <= content(f["q"])), None)
            if k: f["paa_ref"] = f.get("ref"); f["source"], f["ref"] = "secondary", k; rc += 1
    text = lambda s: (s["fields"].get("faq"), [f.get("q") for f in s.get("faq_sources") or []])
    assert text(spec) == (before[0], [q for q, _, _ in before[1]]), "paa-resource changed question or answer text: aborted, nothing written"
    out = json.dumps(spec, indent=1, ensure_ascii=False)
    assert json.loads(out)["fields"]["faq"].encode() == json.loads(before_raw)["fields"]["faq"].encode()
    open(g.spec_path, "w").write(out)
    print(f"{url}: {n} of {len(spec.get('faq_sources') or [])} FAQ items carry AlsoAsked provenance, {rc} reclassified paa -> secondary; question and answer text byte-identical")
    return 0

FORMAT_WORDS = ["landing page", "questionnaire", "survey", "quiz", "template", "form", "page"]

def candidate_phrases(spec):
    """PA3 synonym candidates for a page: the head phrase minus its format word, and any abbreviation in the primary
    (a token written in capitals in the page's own title or H1). Candidates only: applied after Divit approves the batch."""
    prim = norm((spec.get("keywords") or {}).get("primary") or ""); out = []
    for fw in FORMAT_WORDS:
        if re.search(r"(?<![a-z0-9])" + re.escape(fw) + r"s?(?![a-z0-9])", prim):
            rest = norm(re.sub(r"(?<![a-z0-9])" + re.escape(fw) + r"s?(?![a-z0-9])", " ", prim, count=1))
            if rest and rest != prim: out.append((rest, "minus-format"))
            break
    shown = " ".join(str(spec.get("fields", {}).get(k) or "") for k in ("h1", "meta_title", "title", "name"))
    for tok in prim.split():
        if len(tok) >= 2 and re.search(r"(?<![A-Za-z0-9])" + re.escape(tok.upper()) + r"(?![A-Za-z0-9])", shown) and tok not in [c for c, _ in out]:
            out.append((tok, "abbreviation"))
    return out

def synonym_candidates(urls):
    """Write rules/paa_synonym_candidates.json: per page, each candidate with how many extra questions it admits
    (pull + current FAQ) and how many of those fail PA4/PA5 (incl. the answer-source sense check). No question text."""
    cp = os.path.join(ROOT, "rules", "paa_synonym_candidates.json")
    doc = json.load(open(cp)) if os.path.exists(cp) else {"_note": "", "pages": {}}
    doc["_note"] = ("PA3 synonym CANDIDATES proposed by code (DECISIONS 2026-10-08): not applied; rules/paa_synonyms.json holds approved ones only. "
                    "status unsafe = a question it admits fails PA4/PA5 or the answer-source sense check; no-evidence = admits nothing in the pull or FAQ. Counts only.")
    for url in urls:
        g = Gate(url); cands = candidate_phrases(g.spec); rows = []
        pull = json.load(open(pull_path(g.slug))) if os.path.exists(pull_path(g.slug)) else None
        nodes = flatten(pull) if pull else []; ctx = {norm(n["q"]): n["ctx"] for n in nodes}
        seen, qs = set(), []
        for it in nodes + [{"q": f["q"], "ctx": ctx.get(norm(((f.get("prov") or {}).get("original")) or ""), "")} for f in faq_items(g.spec)]:
            if norm(it["q"]) not in seen: seen.add(norm(it["q"])); qs.append(it)
        for phrase, kind in cands:
            gc = Gate(url, [phrase]); hr = phrase_re(phrase); adm = bad4 = bad5 = 0
            for it in qs:
                q = norm(it["q"])
                if any(h.search(q) for h in g.heads) or not hr.search(q): continue
                adm += 1; rs = gc.judge({"q": it["q"], "ctx": it.get("ctx", ""), "source": "secondary"})
                bad4 += any(r[0] == "PA4" and r[1] == "reject" for r in rs); bad5 += any(r[0] == "PA5" and r[1] == "reject" for r in rs)
            rows.append({"phrase": phrase, "kind": kind, "admits": adm, "pa4": bad4, "pa5": bad5, "pulled": bool(pull),
                         "status": "unsafe" if bad4 or bad5 else ("safe" if adm else "no-evidence")})
        doc["pages"][g.slug] = rows
    json.dump(doc, open(cp, "w"), indent=1, ensure_ascii=False)
    allr = [r for v in doc["pages"].values() for r in v]
    print(f"synonym candidates: {len(allr)} on {len(doc['pages'])} pages; " + ", ".join(f"{k} {sum(r['status'] == k for r in allr)}" for k in ("safe", "unsafe", "no-evidence")))
    return 0

def faq_items(spec):
    """The spec's FAQ: questions from faq_sources (with their provenance), answers from fields.faq (window.awbFAQ JSON)."""
    m = re.search(r"window\.awbFAQ\s*=\s*(\{.*\})\s*;?\s*</script>", spec["fields"].get("faq", ""), re.S)
    faq = json.loads(m.group(1))["items"] if m else []
    src = {norm(f["q"]): f for f in spec.get("faq_sources") or []}
    out = []
    for i, f in enumerate(faq):
        s = src.get(norm(f["q"]), {})
        prov = s.get("prov") or {}
        out.append({"n": i + 1, "q": f["q"], "a": f.get("a", ""), "source": s.get("source", "unknown"), "prov": prov})
    return out

def run_pull(g):
    p = os.path.join(ROOT, "private", "alsoasked", g.slug + ".json")
    if not os.path.exists(p): sys.exit(f"no AlsoAsked pull for {g.slug}: pull it through ops/weekend.py aa <url>")
    raw = flatten(json.load(open(p))); items, seen = [], {}
    for it in sorted(raw, key=lambda x: x["prov"]["depth"]):  # AlsoAsked repeats wordings across branches: gate each wording once (shallowest)
        k = norm(it["q"])
        if k in seen: seen[k]["repeats"] = seen[k].get("repeats", 0) + 1; continue
        seen[k] = it; items.append(it)
    by_q = {}
    for it in sorted(items, key=lambda x: x["prov"]["depth"]):  # parents first, so PA2 sees the parent's verdict
        if it["prov"]["depth"] >= 2: it["parent_verdict"] = by_q.get(it["parent_q"], {}).get("verdict")
        it["reasons"] = g.judge(it); it["verdict"] = g.verdict(it["reasons"]); by_q[it["q"]] = it
    items = g.finish(sorted(items, key=lambda x: x["prov"]["depth"]))
    ok = sum(i["verdict"] == "pass" for i in items)
    extra = [("PA11", f"{len(raw)} nodes, {len(items)} distinct; {ok} passing AlsoAsked candidates (fill from secondaries; under {MIN_ON_TOPIC} on-topic in the final FAQ parks the page)")]
    return items, extra

def run_spec(g):
    items = faq_items(g.spec)
    vf = os.path.join(ROOT, "private", "alsoasked", "verdicts", g.slug + ".json")
    pv = {norm(i["q"]): i["verdict"] for i in json.load(open(vf))["items"]} if os.path.exists(vf) else {}
    pull = json.load(open(pull_path(g.slug))) if os.path.exists(pull_path(g.slug)) else None
    sh = answer_shingles(pull) if pull else set()
    ctx = {norm(n["q"]): n["ctx"] for n in flatten(pull)} if pull else {}
    for it in items:
        it["ctx"] = ctx.get(norm((it["prov"] or {}).get("original") or ""), "")
        if (it["prov"] or {}).get("depth") == 2: it["parent_verdict"] = pv.get(norm(it["prov"].get("parent") or ""), "flag")
        it["reasons"] = g.judge(it)
        w = norm(re.sub(r"<[^>]+>", " ", html.unescape(it["a"]))).split()
        hit = next((" ".join(w[i:i + 6]) for i in range(len(w) - 5) if " ".join(w[i:i + 6]) in sh), None)
        if hit: it["reasons"].append(("PA1b", "reject", f'answer shares a 6-word run with AlsoAsked answer text ("{hit}")'))
        it["verdict"] = g.verdict(it["reasons"])
    items = g.finish(items)
    page = []
    if len(items) != N_FAQ: page.append(("PA12", f"{len(items)} items, not exactly {N_FAQ}"))
    ok = [i for i in items if i["verdict"] != "reject"]
    if len(ok) < MIN_ON_TOPIC: page.append(("PA11", f"{len(ok)} on-topic items, under {MIN_ON_TOPIC}: the page parks"))
    if items and not re.match(r"^(what|which) (is|are) ", norm(items[0]["q"])): page.append(("PA12", "item 1 is not the definition"))
    if len(items) > 1:
        if not re.match(r"^how (do|can|to|should) (i |you |we )?(create|make|build|set up|design)", norm(items[1]["q"])): page.append(("PA12", "item 2 is not how-to-build"))
        if not re.search(r'href=["\'][^"\']*' + re.escape(g.hub_path) + r'/?["\']', items[1]["a"]): page.append(("PA12", "item 2 has no hub link"))
    secs = [content(k) for k in (g.spec.get("keywords") or {}).get("secondaries_used") or []]
    sec = sum(i["source"] == "secondary" or any(k and k <= content(i["q"]) for k in secs) for i in items); need = min(MIN_SECONDARIES, len((g.spec.get("keywords") or {}).get("secondaries_used") or []) or MIN_SECONDARIES)
    if sec < need: page.append(("PA12", f"{sec} items carrying a secondary, under {need}"))
    for it in items:
        first = norm(re.sub(r"<[^>]+>", " ", html.unescape(it["a"])))[:60]
        bad = [b for b in g.pt["answer_first_banned"] if first.startswith(b)]
        if bad: it["reasons"].append(("PA12", "reject", f'answer does not lead with the answer ("{bad[0]}")')); it["verdict"] = "reject"
    return items, page

def main(argv):
    if not argv: print(__doc__); return 0
    cand = []
    if "--cand" in argv:
        cp = os.path.join(ROOT, "rules", "paa_synonym_candidates.json")
        cand = [c["phrase"] for c in (json.load(open(cp))["pages"].get(argv[0].rsplit("/", 1)[1], []) if os.path.exists(cp) else []) if c.get("status") == "safe"]
    g = Gate(argv[0], cand); mode = ("spec" if "--spec" in argv else "pull") + ("+cand" if "--cand" in argv else "")
    items, page = run_spec(g) if mode.startswith("spec") else run_pull(g)
    c = {v: sum(i["verdict"] == v for i in items) for v in ("pass", "reject", "flag")}
    tally = {}
    for i in items:
        for rule in sorted({r[0] for r in i["reasons"] if r[1] == "reject"}): tally[rule] = tally.get(rule, 0) + 1
    vd = os.path.join(ROOT, "private", "alsoasked", "verdicts"); os.makedirs(vd, exist_ok=True)
    out = os.path.join(vd, g.slug + {"spec": ".faq", "pull": "", "spec+cand": ".faq.cand", "pull+cand": ".cand"}[mode] + ".json")
    json.dump({"url": g.url, "mode": mode, "date": datetime.date.today().isoformat(), "counts": c, "rejects_by_rule": tally,
               "page": [{"rule": r, "msg": m} for r, m in page],
               "items": [{k: i.get(k) for k in ("n", "q", "source", "asker", "verdict")} | {"depth": (i.get("prov") or {}).get("depth"),
                          "reasons": [{"rule": r, "kind": k, "msg": m} for r, k, m in i["reasons"]]} for i in items]},
              open(out, "w"), indent=1, ensure_ascii=False)
    ts = ", ".join(f"{k} {v}" for k, v in sorted(tally.items())) or "none"
    line = f"- {datetime.date.today().isoformat()} {g.url} [{mode}]: {len(items)} questions; pass {c['pass']}, reject {c['reject']}, flag {c['flag']}; rejects by rule: {ts}" + \
           (f"; page: {'; '.join(f'{r} {m}' for r, m in page)}" if page else "")
    sp = os.path.join(ROOT, "audit", "paa", "summary.md")
    if not os.path.exists(sp): open(sp, "w").write("# PAA gate summary (qc/paa_gate.py)\n\nOne line per run; per-question verdicts stay in private/alsoasked/verdicts/.\n\n")
    open(sp, "a").write(line + "\n")
    if "--quiet" not in argv: print(line[2:])
    if mode.startswith("spec") and "--quiet" not in argv:
        for i in items:
            if i["verdict"] != "pass": print(f"  Q{i['n']} {i['verdict']}: {', '.join(sorted({r[0] for r in i['reasons'] if r[1] in ('reject', 'flag')}))}  [{i['q'][:60]}]")
    return 0 if not page and c["reject"] == 0 and c["flag"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
