"""Comparison tables from the vetted competitor library (rules/competitors/<dir>.json).
render(hub_dir, vs, rows) returns the exact Emergent-first markup the approved pages use."""
import json, os, datetime, re
from html import escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = "https://cdn.prod.website-files.com/6a0edf12ef1a8562ed56d806/6a0ef94db7f0a045fab57060_logo.svg"
def lib(d): return json.load(open(os.path.join(ROOT, "rules", "competitors", f"{d}.json")))
def _e(s): return escape(s, quote=False)
def render(d, vs, rows, variant=None):
    L = lib(d); vs = list(vs)
    EM = dict(L["emergent"]); EM.update({k: v for k, v in L.get("emergent_variants", {}).get(variant or "", {}).items() if not k.startswith("_")})
    if variant and variant not in L.get("emergent_variants", {}): raise ValueError(f'no emergent variant "{variant}" in the {d} library')
    if len(vs) != 3: raise ValueError("pick exactly 3 competitors")
    for c in vs:
        if c not in L["competitors"]: raise ValueError(f'"{c}" is not in the {d} library; add it with sources first')
    out = ["<div data-rt-embed-type='true'><style>", "  .cmp--emg-first thead th.col-brand-head { background: #ebebeb; }",
           "  .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; }",
           "  .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; }", "</style>",
           '<div class="cmp cmp--emg-first">', "  <table>", "    <colgroup>", '      <col class="col-feature" />', '      <col class="col-brand" />',
           '      <col class="col-other" />', '      <col class="col-other" />', '      <col class="col-other" />', "    </colgroup>", "    <thead>", "      <tr>",
           '        <th class="col-feature" scope="col"><span class="visually-hidden"></span></th>', '        <th class="col-brand-head" scope="col">',
           f'          <img class="brand-logo" src="{LOGO}" alt="Emergent" />', "        </th>"]
    out += [f'        <th scope="col">{_e(c)}</th>' for c in vs]
    out += ["      </tr>", "    </thead>", "    <tbody>"]
    for r in rows:
        rid, label = (r.split("=", 1) + [None])[:2] if "=" in r else (r, None)
        if rid not in L["dimensions"]: raise ValueError(f'row "{rid}" is not a dimension in the {d} library ({", ".join(L["dimensions"])})')
        label = label or L["dimensions"][rid][0]
        if label not in L["dimensions"][rid]: raise ValueError(f'label "{label}" is not allowed for {rid}: {L["dimensions"][rid]}')
        cells = []
        for c in vs:
            fact = L["competitors"][c]["facts"].get(rid)
            if not fact: raise ValueError(f'{c} has no verified fact for "{rid}"; pick another row or add it with a source')
            cells.append(fact["text"])
        out += ["      <tr>", f'        <th scope="row">{_e(label)}</th>', f'        <td class="col-brand">{_e(EM[rid])}</td>']
        out += [f'        <td class="col-other">{_e(t)}</td>' for t in cells]
        out += ["      </tr>"]
    out += ["    </tbody>", "  </table>", "</div></div>"]
    return "\n".join(out)
def stale(d, vs, rows, today=None):
    L = lib(d); today = today or datetime.date.today(); old = []
    for c in vs:
        for r in rows:
            rid = r.split("=", 1)[0]; fct = L["competitors"][c]["facts"][rid]
            age = (today - datetime.date.fromisoformat(fct["checked"])).days; limit = 90 if re.search(r"\d", fct["text"]) else 180
            if age > limit: old.append(f"{c} / {rid}: checked {fct['checked']} ({age} days, limit {limit})")
    return old
# ---- category sets (Divit 2026-10-14, competitor library extension): the page's primary keyword picks the default vendors ----
def category_for(d, primary):
    """The library's category set for a primary keyword: the first set (file order) with a whole-word term match, else "general"."""
    sets = {k: v for k, v in lib(d).get("category_sets", {}).items() if not k.startswith("_")}
    p = " ".join(re.findall(r"[a-z0-9]+", (primary or "").lower()))
    for key, cs in sets.items():
        if any(re.search(r"\b" + r"\s+".join(map(re.escape, t.lower().split())) + r"(s|es)?\b", p) for t in cs.get("terms", [])): return key
    return "general" if "general" in sets else None
def _host(u): return re.sub(r"^www\.", "", re.sub(r"^https?://", "", u or "").split("/")[0].lower())
def pick(d, primary, rows=None, top_urls=()):
    """Default table for a page: (category, vs, rows, variant). Vendors need a fact for every row; vendors ranking in the
    page's top 10 come first, then the set's order. Raises when the library has no category sets or fewer than 3 usable vendors."""
    L = lib(d); key = category_for(d, primary)
    if not key: raise ValueError(f"the {d} library has no category_sets: pass --vs A,B,C")
    cs = L["category_sets"][key]; rows = list(rows or cs["rows"]); rids = [r.split("=", 1)[0] for r in rows]
    ok = [v for v in cs["vendors"] if all(r in L["competitors"][v]["facts"] for r in rids)]
    tops = {_host(u) for u in top_urls}
    ranked = [v for v in ok if _host(L["competitors"][v].get("site", "")) in tops] + [v for v in ok if _host(L["competitors"][v].get("site", "")) not in tops]
    if len(ranked) < 3: raise ValueError(f'category "{key}" has {len(ranked)} vendor(s) with facts for rows {", ".join(rids)}: add facts or pass --vs')
    return key, ranked[:3], rows, cs.get("variant")
