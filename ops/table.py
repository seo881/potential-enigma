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
           f'          <img class="brand-logo" src="{LOGO}" alt="emergent" />', "        </th>"]
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
