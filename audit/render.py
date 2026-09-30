# Renders the hub audit. H2 target <= 48 chars (2 lines at the section heading width measured on the templates:
# "Why Build Your Approval / Workflow With Emergent?" wraps at ~24-26 chars/line). Subheading target <= 135 chars (~68/line).
# Meta title <= 60 chars; meta description 120-155 chars.
import json, textwrap
H2, SUB, TITLE = 48, 135, 60
def n(s): return len(s)
def flag(s, lim): return "✅" if n(s) <= lim else f"❌ {n(s)} > {lim}"
HUBS = json.load(open("hubs.json"))
def row(*c): return "| " + " | ".join(str(x).replace("\n"," ").replace("|","/") for x in c) + " |"
def render(key, h):
    L = [f"# {h['name']} hub: pre-launch audit", "", f"**Page:** `{h['url']}` (page ID `{h['page_id']}`, Draft)  ", "**Audited:** 30 Sep 2026, against live Designer content, live schema, and vendor pricing checked this week.", ""]
    L += ["## Scorecard", "", row("Priority","Count"), row("---","---")]
    pr = {}
    for f in h["findings"]: pr[f["p"]] = pr.get(f["p"],0)+1
    for p in ["P0 fact","P1 SEO","P1 readability","P2 polish"]: L.append(row(p, pr.get(p,0)))
    L += ["", "P0 = factually wrong or unverifiable claim (must fix before launch). P1 = ranking or readability. P2 = polish.", ""]
    m = h["meta"]
    L += ["## 1. Meta title, description, OG", "", row("Field","Current","Chars","Proposed","Chars","Why"), row("---","---","---","---","---","---")]
    for f in m:
        L.append(row(f["field"], f["cur"], n(f["cur"]), f["new"] or "Keep", n(f["new"]) if f["new"] else "", f["why"]))
    L += [""]
    L += ["## 2. Findings, section by section", "", row("#","Priority","Section / element","Current text","Issue","Proposed text","Len"), row("---","---","---","---","---","---","---")]
    for i,f in enumerate(h["findings"],1):
        lim = f.get("lim")
        ln = (flag(f["new"], lim) + f" ({n(f['new'])})") if (lim and f.get("new")) else (str(n(f["new"])) if f.get("new") else "")
        L.append(row(i, f["p"], f["where"], f["cur"], f["issue"], f.get("new","") or "(remove)", ln))
    L += [""]
    if h.get("faq"):
        L += ["## 3. FAQ changes (the FAQPage schema must be rebuilt word-for-word after these land)", "", row("#","Question","Current (excerpt)","Issue","Proposed answer"), row("---","---","---","---","---")]
        for i,f in enumerate(h["faq"],1): L.append(row(i, f["q"], f["cur"], f["issue"], f["new"]))
        L += [""]
    L += ["## 4. Verified as accurate (no change)", ""] + [f"- {v}" for v in h["verified"]] + [""]
    if h.get("house"): L += ["## 5. Housekeeping", ""] + [f"- {v}" for v in h["house"]] + [""]
    return "\n".join(L)
for i,(k,h) in enumerate(HUBS.items(),1):
    open(f"0{i}-{h['slug']}.md","w").write(render(k,h))
    print(k, "findings:", len(h["findings"]), "faq:", len(h.get("faq",[])))
