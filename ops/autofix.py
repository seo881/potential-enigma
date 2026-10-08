"""autofix.py: deterministic fixes for the 2026-10-08 QC checks, one check per run so each commit is revertible.

    python3 ops/autofix.py <c5|h3|s10|h4|c4> [--apply] [--json out.json]

Scope: written pages (states qc_pass, images, rework, reviewed, challenged). The 4 frozen original children, parked and
published pages are never touched. Every edit is guarded: QC runs on the page before and after, and an edit is kept only
if no P0/P1 issue (by code and field) gets worse, its own check included. An edit with alternatives tries each in order
(C5: keep the writer's phrase and add the qualifier; if the feature band or the measured width breaks, shorten the phrase).
What the guard refuses stays flagged for the combined writer pass. Without --apply nothing is written.

  c5   GitHub export qualified by plan: "to your GitHub repository" -> "... on paid plans" (emergent.sh/pricing: GitHub
       integration from the Standard plan; rules/capabilities.json code-export)
  h3   serial comma, certain cases only (qc/serial_comma.py; ambiguous ones stay P2 notes and never go to a writer)
  s10  zero-width characters and empty paragraphs removed (export strips them too: hubctl export_fields)
  h4   UK idioms with a one-to-one US form (MECH below); bare "on the day" -> "on the day itself"
  c4   custom-domain phrase + the approved wording: "(built into Emergent, uses credits)", or "(built in, uses credits)"
       when the sentence already names Emergent (rules/capabilities.json custom-domain)
"""
import json, re, sys, os, glob, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "qc")); sys.path.insert(0, os.path.join(ROOT, "ops"))
import qc_hub as Q, serial_comma as SC, guards

WRITTEN = {"qc_pass", "images", "rework", "reviewed", "challenged"}
SKIP_FIELDS = {"why_table", "category", "slug"}
ZW = re.compile("[​‌‍⁠﻿]|&zwj;|&#8205;|&zwnj;"); EMPTY_P = re.compile(r"<p[^>]*>\s*(&nbsp;|\s)*</p>")
MECH = {"tick the box": "check the box", "tick box": "checkbox", "whilst": "while", "amongst": "among", "learnt": "learned",
        "spelt": "spelled", "fortnight": "two weeks", "at the weekend": "on the weekend", "maths": "math", "post code": "ZIP code",
        "postcode": "ZIP code", "car park": "parking lot", "mobile phone": "cell phone", "different to": "different from"}
QUAL_C5 = re.compile(r"paid plan|standard|pro plan|on paid", re.I)
QUAL_C4 = re.compile(r"credit|built in|built-in|included", re.I)

def _sentence(text, s, e):
    a = max(text.rfind(". ", 0, s), text.rfind("<p>", 0, s), text.rfind('\\"', 0, s), 0)
    b = min([x for x in (text.find(". ", e), text.find("</p>", e), text.find('\\"', e)) if x >= 0] or [len(text)])
    return text[a:b]
def _cap(src, rep): return rep[0].upper() + rep[1:] if src[:1].isupper() else rep

def _in_title(v, i): return v.rfind("<h3", 0, i) > v.rfind("</h3>", 0, i)   # titles are never edited (2-line, 48-char slots)
def gen_c5(k, v):
    for m in re.finditer(r"\b(to|in) ((?:your|a) )?(own )?GitHub( repository| repo)?\b(?! on paid)", v):
        sent = _sentence(v, m.start(), m.end())
        if _in_title(v, m.start()): continue
        if QUAL_C5.search(sent) or not re.search(r"export|push|sync|repo", sent, re.I): continue
        c = [m.group(0) + " on paid plans"]
        if m.group(1) == "to":
            if m.group(2) == "your " and m.group(0) != "to your GitHub": c.append("to your GitHub on paid plans")
            c.append("to GitHub on paid plans")
        yield m.start(), m.end(), list(dict.fromkeys(c))
def gen_h3(k, v):
    for p, _s in SC.find(v)[0]: yield p, p, [","]
def gen_s10(k, v):
    for rx in (ZW, EMPTY_P):
        for m in rx.finditer(v): yield m.start(), m.end(), [""]
def gen_h4(k, v):
    for w, us in MECH.items():
        for m in re.finditer(r"(?<![A-Za-z0-9])" + re.escape(w) + r"(?![A-Za-z0-9])", v, re.I): yield m.start(), m.end(), [_cap(m.group(0), us)]
    for m in re.finditer(r"(?<![A-Za-z0-9])on the day(?=\s*(?:[.,;:!?)\]\\\"]|<|$))", v, re.I): yield m.start(), m.end(), [_cap(m.group(0), "on the day itself")]
def gen_c4(k, v):
    for m in re.finditer(r"\b(?:under|on) (?:(?:your|a|the) )?(?:[A-Za-z]+(?:'|&#39;|&rsquo;)s )?(?:own |custom )domain\b(?! \()", v):
        sent = _sentence(v, m.start(), m.end())
        if QUAL_C4.search(sent) or _in_title(v, m.start()): continue
        c = ([] if "Emergent" in sent else [m.group(0) + " (built into Emergent, uses credits)"]) + [m.group(0) + " (built in, uses credits)"]
        yield m.start(), m.end(), c
GEN = {"c5": (gen_c5, "C5"), "h3": (gen_h3, "H3"), "s10": (gen_s10, "S10"), "h4": (gen_h4, "H4"), "c4": (gen_c4, "C4")}

def blocking(issues): return collections.Counter((i["code"], i["field"]) for i in issues if i["sev"] in ("P0", "P1"))
def worse(before, after): return [k for k in after if after[k] > before.get(k, 0)]
def plain(s): return re.sub(r"\s+", " ", Q.strip_html(s)).strip()

def run(name, apply=False):
    gen, code = GEN[name]
    st = {u: e.get("state") for u, e in guards.all_status().items()}
    every = Q.load_specs(sorted(glob.glob(os.path.join(ROOT, "specs", "*", "*.json"))))
    scope = [s for s in every if st.get(s["url"]) in WRITTEN]
    rep = {"check": code, "pages_changed": 0, "instances_changed": 0, "refused": 0, "examples": [], "changed": {}, "refused_at": []}
    for s in scope:
        F = s["fields"]; base = blocking(Q.check(s, every)); raw = open(s["_path"]).read(); changed = 0
        for k in list(F):
            if not isinstance(F[k], str) or k in SKIP_FIELDS: continue
            for a, b, cands in sorted(gen(k, F[k]), key=lambda x: -x[0]):
                old = F[k]; ok = False
                for c in cands:
                    F[k] = old[:a] + c + old[b:]
                    after = blocking(Q.check(s, every))
                    if not worse(base, after): ok = True; base = after; break
                if not ok:
                    F[k] = old; rep["refused"] += 1; rep["refused_at"].append((s["url"], k, plain(old[max(0, a - 60):b + 30]))); continue
                changed += 1
                if len(rep["examples"]) < 40: rep["examples"].append((s["url"], k, plain(old[max(0, a - 70):b + 40]), plain(F[k][max(0, a - 70):a + len(c) + 40])))
        if changed:
            rep["pages_changed"] += 1; rep["instances_changed"] += changed; rep["changed"][s["url"]] = changed
            if apply:
                ea = raw.isascii() and json.dumps(json.loads(raw), indent=1, ensure_ascii=True) == raw.rstrip("\n")
                with open(s["_path"], "w") as fh: fh.write(json.dumps({k: v for k, v in s.items() if k != "_path"}, indent=1, ensure_ascii=ea) + ("\n" if raw.endswith("\n") else ""))
    left = collections.Counter(); left_pages = set()
    for s in scope:
        for i in Q.check(s, every):
            if i["code"] == code and i["sev"] in ("P0", "P1"): left[i["field"]] += 1; left_pages.add(s["url"])
    rep["instances_left"] = sum(left.values()); rep["pages_left"] = sorted(left_pages); rep["left_by_field"] = dict(left)
    return rep

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in GEN: print(__doc__); sys.exit(1)
    r = run(a[0], "--apply" in a)
    if "--json" in a: json.dump(r, open(a[a.index("--json") + 1], "w"), indent=1, ensure_ascii=False)
    print(f'{r["check"]}: pages changed {r["pages_changed"]}, instances changed {r["instances_changed"]}, refused by the guard {r["refused"]}, '
          f'instances left {r["instances_left"]} on {len(r["pages_left"])} pages {r["left_by_field"]}{"" if "--apply" in a else " (dry run)"}')
