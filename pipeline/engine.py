"""Image engine: renders a page's `image_brief` (docs/IMAGE_BRIEF.md) into the six v5 images, with the same design
system, palettes, motion and gates as the 16 approved hand-built scenes.

  python3 pipeline/engine.py lint   specs/<dir>/<slug>.json       # render in memory + gates; prints issues, writes nothing
  python3 pipeline/engine.py render specs/<dir>/<slug>.json ...   # writes images/<dir>/<slug>/{uc-1..4.svg,cover.svg,og.png}
                                                                  # + a contact sheet in the review folder; updates spec.images
  python3 pipeline/engine.py demo                                 # renders pipeline/briefs/*.json for visual checks

Frames R1-R11 reuse the exact geometry of the approved scenes (IMAGE_PIPELINE_KT.md Part 7). Content flows through
blocks (engine_blocks.py). Anything that does not fit fails with a message naming the field: shorten the brief,
never the type size.
"""
import os, sys, re, io, json, base64, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _alias  # noqa: F401
import ds5 as L
import hubs_v5 as H
from qa import width as tw
import engine_blocks as B
from engine_blocks import BriefError, CTX, fit, T

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PALETTE = {"LP": "lp", "Form": "form", "Auto": "aab", "SurveyQuiz": "sqb", "lp": "lp", "form": "form", "aab": "aab", "sqb": "sqb"}

# Brand layer (Divit + the Webflow developer, 2026-10-07): neutral grey canvas behind every image; the artifact itself
# (buttons, chips, charts, accents) keeps colour, varied by hub rather than purple everywhere. Applies to engine renders only;
# build.py keeps the original palettes so the 24 live images stay reproducible until their re-render is approved.
NEUTRAL = dict(bg1="#FAFAFA", bg2="#EEEEF0", glow="#FFFFFF", grid="#52525B", spot="#71717A", sh="#18181B", line="#E4E4E7", hair="#EFEFF1")
H.PALS = {k: {**v, **NEUTRAL} for k, v in H.PALS.items()}
ACCENTS = {"violet": "aab", "blue": "lp", "emerald": "form", "orange": "sqb"}
ROTATION = ["blue", "emerald", "orange", "violet"]
def accent_for(hub, tab, idx):
    """One accent per image; the four tabs of a page rotate through the brand accents, starting with the hub's own."""
    if tab.get("accent"):
        if tab["accent"] not in ACCENTS: raise BriefError(f"tab {idx}: accent must be one of {', '.join(ACCENTS)}")
        return ACCENTS[tab["accent"]]
    own = next(k for k, v in ACCENTS.items() if v == PALETTE[hub])
    order = [own] + [a for a in ROTATION if a != own]
    return ACCENTS[order[(idx - 1) % len(order)]]

# ------------------------------------------------------------------ layout
def flow(blocks, x, y, w, h, where, top_gap=24, max_gap=40):
    """Lay blocks top to bottom inside (x, y, w, h). Gaps stretch (up to max_gap) to keep the panel balanced."""
    if not blocks: return "", 0.0
    snap = (CTX["clicks"], CTX.get("av", 0))
    hs = []
    for i, bd in enumerate(blocks):
        kind = bd.get("type")
        if kind not in B.BLOCKS: raise BriefError(f'{CTX["where"]}{where}[{i}]: unknown block type "{kind}". Known: {", ".join(sorted(B.BLOCKS))}')
        _, bh = B.BLOCKS[kind](bd, x, 0, w); hs.append(bh)
    CTX["clicks"], CTX["av"] = snap
    n = len(blocks); need = sum(hs) + top_gap * (n - 1)
    if need > h + 0.5:
        raise BriefError(f'{CTX["where"]}{where}: content is {need:.0f}px tall, the panel holds {h:.0f}px. Remove a block or rows.')
    gap = top_gap if n == 1 else min(max_gap, top_gap + (h - need) / (n - 1))
    s, yy = "", y
    for bd, bh in zip(blocks, hs):
        part, _ = B.BLOCKS[bd["type"]](bd, x, yy, w); s += part; yy += bh + gap
    used = (sum(hs) + gap * (n - 1)) / h
    # Balance: empty space that pools in one place once spacing has stretched to its limit. Calibrated 2026-10-07:
    # all 16 approved scenes pool at most 16%; the first AP sample's visibly empty panels pooled 17-25%.
    pooled = (h - hs[0]) / h if n == 1 else max(0.0, h - sum(hs) - max_gap * (n - 1)) / h
    if "hero" not in where and pooled > 0.165:
        CTX.setdefault("balance", []).append(f"{CTX['where']}{where}: {pooled:.0%} of the panel is empty space pooled in one place (max 16%); add a block, a row or a richer element so the panel reads full")
    # Hero cards are airier by design: the 16 approved scenes pool at most 21% (calibrated 2026-10-07, Divit's hero-gate decision)
    if "hero" in where and pooled > 0.215:
        CTX.setdefault("balance", []).append(f"{CTX['where']}{where}: the hero card is {pooled:.0%} empty space pooled in one place (max 21%); add a line, an action or a block, or use a shorter card")
    return s, used

def panel_box(x, y, w, h, pad=28): return (x + pad, y + pad, w - 2 * pad, h - 2 * pad)

def chrome_window(x, y, w, h, title):
    fit(title, 17, 600, 220, "main.chrome"); return L.window(x, y, w, h, title, 0)
def chrome_doc(x, y, w, h): return L.rect(x, y, w, h, 14, "#fff", L.LINE, 1, "e1")
def chrome_phone(x, y, w, h):
    s = '<g filter="url(#e2)">' + L.rect(x, y, w, h, 46, "#111827") + '</g>' + L.rect(x + 10, y + 10, w - 20, h - 20, 37, "#fff")
    s += L.rect(x + w / 2 - 44, y + 22, 88, 24, 12, "#111827") + T(x + 40, y + 42, "9:41", 16, 700, L.INK, tnum=True)
    for i, hgt in enumerate([6, 9, 12, 15]): s += L.rect(x + w - 92 + i * 6, y + 42 - hgt, 4, hgt, 1, L.INK)
    s += L.rect(x + w - 60, y + 29, 26, 13, 4, "#fff", L.INK, 1.5) + L.rect(x + w - 57, y + 32, 18, 7, 2, L.INK) + L.rect(x + w - 32, y + 33, 2.5, 5, 1, L.INK)
    return s + L.rect(x + w / 2 - 50, y + h - 24, 100, 5, 2.5, "#111827")
def chrome_browser(x, y, w, h, url):
    fit(url, 16, 500, w - 260, "main.chrome"); return H.browser(x, y, w, h, url)
def connector(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1} C {x1+34} {y1}, {x2-34} {y2}, {x2} {y2}" stroke="{L.ACC}" stroke-opacity="0.55" stroke-width="2" fill="none" stroke-dasharray="4 5"/><circle cx="{x2}" cy="{y2}" r="4" fill="{L.ACC}"/>'
def scan(P):
    s = f'<defs><linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{L.ACC}" stop-opacity="0"/><stop offset="1" stop-color="{L.ACC}" stop-opacity="0.16"/></linearGradient></defs>'
    s += f'<g class="sweep"><rect x="{P[0]+1}" y="{P[1]+P[3]-120}" width="{P[2]-2}" height="84" fill="url(#beam)"/><line x1="{P[0]+1}" y1="{P[1]+P[3]-36}" x2="{P[0]+P[2]-1}" y2="{P[1]+P[3]-36}" stroke="{L.ACC}" stroke-width="2.5" stroke-opacity="0.7"/></g>'
    return s + L.rect(P[0] + P[2] - 150, P[1] + P[3] - 51, 128, 30, 15, L.ACC) + L.icon("scan-line", P[0] + P[2] - 140, P[1] + P[3] - 46, 20, "#fff", 2) + T(P[0] + P[2] - 114, P[1] + P[3] - 30, "Scanned", 16, 600, "#fff")

FRAMES = {
 "R1":  dict(main=("window", 60, 164, 700, 596), content=(156, 234, 540, 506), hero=(730, 196, 410, 300), mini=(770, 540, 370, 104)),
 "R2":  dict(main=("doc", 60, 164, 440, 596), content=(92, 198, 376, 516), panel=(560, 164, 580, 330), hero=(560, 524, 580, 236), connect=[(500, 330, 560, 300)]),
 "R3":  dict(main=("doc", 60, 164, 510, 596), content=(96, 196, 438, 532), panel=(610, 164, 530, 372), hero=(610, 568, 530, 176)),
 "R4":  dict(main=("phone", 60, 164, 300, 600), content=(90, 236, 240, 494), gap=16, panel=(430, 164, 710, 304), hero=(430, 500, 710, 260), connect=[(360, 470, 430, 330)]),
 "R5":  dict(main=("browser", 60, 164, 700, 596), content=(100, 236, 620, 508), gap=20, hero=(800, 214, 340, 272), mini=(800, 520, 340, 120)),
 "R6":  dict(main=("panel", 60, 164, 520, 596), content=(96, 200, 448, 524), hero=(620, 196, 520, 330), mini=(620, 570, 520, 120), connect=[(580, 360, 620, 330)]),
 "R7":  dict(main=("panel", 60, 164, 1080, 420), content=(96, 196, 1008, 356), hero=(420, 612, 720, 150), mini=(60, 612, 330, 150)),
 "R8":  dict(rule=(60, 164, 1080, 90), main=("panel", 60, 284, 720, 476), content=(92, 312, 656, 420), hero=(820, 300, 320, 300), mini=(820, 630, 320, 120)),
 "R9":  dict(main=("panel", 60, 164, 660, 596), content=(96, 196, 588, 532), hero=(760, 196, 380, 300), mini=(760, 540, 380, 120)),
 "R10": dict(main=("panel", 60, 164, 1080, 300), content=(96, 194, 1008, 240), kpi=(60, 500, 210, 260), hero=(300, 500, 840, 260)),
 "R11": dict(main=("panel", 60, 164, 1080, 360), content=(92, 192, 1016, 304), panel=(60, 560, 460, 200), hero=(560, 560, 580, 200)),
}

# ------------------------------------------------------------------ hero and supporting cards
def hero(d, x, y, w, h):
    kind = d.get("kind", "card")
    if kind == "message":
        fit(d["channel"], 18, 700, w - 110, "hero.channel"); fit(d["title"], 18, 600, w - 106, "hero.title")
        for i, l in enumerate(d.get("lines", [])): fit(l, 16, 500, w - 106, f"hero.lines[{i}]")
        if d.get("button") and h < 260: raise BriefError(f'{CTX["where"]}hero: a message hero with a button needs 260px; this frame gives {h}px. Use kind "card".')
        if len(d.get("lines", [])) * 26 + 158 > h - (84 if d.get("button") else 20): raise BriefError(f'{CTX["where"]}hero.lines: too many lines for this hero')
        if d.get("button"):
            bw = tw(d["button"], 17, 600) + 72 + (tw(d["button2"], 17, 600) + 60 if d.get("button2") else 0)
            if 82 + bw > w - 16: raise BriefError(f'{CTX["where"]}hero buttons are {bw:.0f}px; the hero fits {w-98:.0f}px. Shorten them.')
            if d.get("click", True): CTX["clicks"] += 1
        return H.appmsg(x, y, w, h, d["channel"], d["title"], d.get("lines", []), d.get("button"), d.get("button2"), d.get("click", True), d.get("when", "now"))
    s = H.spot(x, y, w, h) + L.rect(x, y, w, h, 20, "#fff", L.LINE, 1, "e2")
    top = y + 24
    if d.get("channel"):
        s += L.icon("hash", x + 24, y + 22, 20, L.SUB, 2.2) + T(x + 50, y + 38, fit(d["channel"], 18, 700, w - 120, "hero.channel"), 18, 700, L.INK) + T(x + w - 24, y + 38, d.get("when", "now"), 16, 600, L.MUTED, "end") + B.hair(x, y + 60, x + w)
        top = y + 80
    elif d.get("app"):
        s += L.rect(x + 24, y + 26, 44, 44, 12, "url(#gAcc)") + L.icon("sparkles", x + 35, y + 37, 22, "#fff", 2) + T(x + 84, y + 44, "Emergent", 18, 700, L.INK) + L.rect(x + 174, y + 27, 48, 24, 6, "#F1F5F9") + T(x + 198, y + 44, "APP", 16, 700, L.SUB, "middle")
        if d.get("app_sub"): s += T(x + 238, y + 44, fit(d["app_sub"], 16, 500, w - 262, "hero.app_sub"), 16, 500, L.MUTED)
        top = y + 70
    if d.get("title"):
        ic = d.get("icon"); kind_c = d.get("tone", "acc")
        bg, fg = {"acc": (L.ACC_S, L.ACC_D), "ok": (L.OK_S, L.OK), "warn": (L.WARN_S, L.WARN), "bad": (L.BAD_S, L.BAD)}[kind_c]
        tx = x + 24; cw = B.chipw(d["chip"][0]) if d.get("chip") else 0
        if ic:
            B.icon_ok(ic); s += L.rect(x + 24, top + 2, 44, 44, 12, bg)
            icon_svg = L.icon(ic, x + 34, top + 12, 24, fg, 2)
            s += ('<g class="ring">' + icon_svg + '</g>') if ic == "bell" else icon_svg; tx = x + 84
        tsize = d.get("title_size", 19)
        s += T(tx, top + 32, fit(d["title"], tsize, 700, x + w - tx - 24 - (cw + 12 if cw else 0), "hero.title"), tsize, 700, L.INK, tnum=True)
        if cw: s += B.chip(x + w - 24 - cw, top + 6, d["chip"][0], d["chip"][1] if len(d["chip"]) > 1 else "acc", cw, 34)
        top += 58
    act = d.get("action"); aw = 0; wide = w >= 560
    if act:
        aic = act.get("icon"); aic and B.icon_ok(aic)
        aw = int(tw(act["label"], 17, 600) + (98 if aic else 72))
        if wide:
            ay = y + h - 74 if not d.get("action_mid") else y + h / 2 - 25
            part, _ = B.button(x + w - 24 - aw, ay, act["label"], act.get("primary", True), aic, aw, 50, act.get("click", True), "hero.action"); s += part
        else:
            part, _ = B.button(x + 24, y + h - 74, act["label"], act.get("primary", True), aic, w - 48, 50, act.get("click", True), "hero.action"); s += part
    bw_ = w - 48 - (aw + 24 if act and wide else 0)
    bh_ = y + h - 24 - top - (74 if act and not wide else 0)
    part, _ = flow(d.get("blocks", []), x + 24, top, bw_, bh_, "hero.blocks", top_gap=16, max_gap=28)
    CTX["warn"] = [w_ for w_ in CTX.get("warn", []) if "hero.blocks" not in w_]   # heroes may be airy
    return s + part

def mini(d, x, y, w, h):
    kind = d.get("kind", "ok"); ic = B.icon_ok(d.get("icon", "database"))
    fit(d["title"], 18, 700, w - 110, "mini.title"); fit(d.get("sub", ""), 16, 500, w - 110, "mini.sub")
    return H.mini(x, y, w, h, ic, d["title"], d.get("sub", ""), kind)

def side_panel(d, x, y, w, h, where):
    s = H.panel(x, y, w, h); bx = panel_box(x, y, w, h)
    part, _ = flow(d.get("blocks", []), *bx, where); return s + part

# ------------------------------------------------------------------ one use-case image
def render_tab(hub, tab, idx=1):
    H.set_hub(accent_for(hub, tab, idx)); CTX.update(clicks=0, av=0, where=f"tab {idx}: ")
    rid = tab.get("recipe"); fr = FRAMES.get(rid)
    if not fr: raise BriefError(f"tab {idx}: recipe must be one of {', '.join(FRAMES)}")
    p = tab["prompt"].strip().strip('"\u201c\u201d')
    if tw("\u201c" + p + "\u201d", 19, 500) + 230 > 1080: raise BriefError(f'tab {idx}: prompt is too long for the prompt chip ({len(p)} chars); keep it to one sentence of about 60-85 characters')
    try: b = H.prompt("\u201c" + p + "\u201d")
    except AssertionError as e: raise BriefError(f"tab {idx}: prompt: {e}")
    kind, mx, my, mw, mh = fr["main"]; main = tab.get("main", {})
    if kind == "window": b += chrome_window(mx, my, mw, mh, main.get("chrome", "Workspace"))
    elif kind == "doc": b += chrome_doc(mx, my, mw, mh)
    elif kind == "phone": b += chrome_phone(mx, my, mw, mh)
    elif kind == "browser": b += chrome_browser(mx, my, mw, mh, main.get("chrome", "yourbrand.com"))
    else: b += H.panel(mx, my, mw, mh)
    if "rule" in fr:
        rx, ry, rw, rh = fr["rule"]; rt = tab.get("rule") or main.get("rule")
        if not rt: raise BriefError(f"tab {idx}: recipe R8 needs a 'rule' sentence")
        b += L.rect(rx, ry, rw, rh, 18, L.ACC_S, L.ACC_M, 1.5) + L.icon(B.icon_ok(tab.get("rule_icon", "git-branch")), rx + 30, ry + 32, 26, L.ACC_D, 2) + T(rx + 72, ry + 54, fit(rt, 20, 700, rw - 100, "rule"), 20, 700, L.ACC_D)
    cx_, cy_, cw_, ch_ = fr["content"]
    if kind == "doc" and main.get("scan"): ch_ -= 18          # keeps the last block clear of the scan pill, as in the approved invoice
    part, _ = flow(main.get("blocks", []), cx_, cy_, cw_, ch_, "main.blocks", top_gap=fr.get("gap", 24)); b += part
    if kind == "doc" and main.get("scan"): b += scan((mx, my, mw, mh))
    for c in fr.get("connect", []): b += connector(*c)
    if "panel" in fr:
        if not tab.get("panel"): raise BriefError(f"tab {idx}: recipe {rid} needs a 'panel' with blocks")
        b += side_panel(tab["panel"], *fr["panel"], "panel.blocks")
    if "kpi" in fr:
        kx, ky, kw, kh = fr["kpi"]; k = tab.get("kpi") or {}
        b += H.panel(kx, ky, kw, kh) + L.icon(B.icon_ok(k.get("icon", "chart-column")), kx + 28, ky + 28, 24, L.ACC, 2)
        b += T(kx + 28, ky + 90, fit(k.get("label", ""), 18, 700, kw - 56, "kpi.label"), 18, 700, L.INK) + T(kx + 28, ky + 148, fit(k.get("value", ""), 40, 800, kw - 56, "kpi.value", -1), 40, 800, L.INK, ls=-1, tnum=True) + T(kx + 28, ky + 180, fit(k.get("sub", ""), 16, 500, kw - 56, "kpi.sub"), 16, 500, L.MUTED)
    hx, hy, hw, hh = fr["hero"]
    if rid == "R5" and tab.get("hero", {}).get("h"): hh = max(240, min(360, int(tab["hero"]["h"])))
    if not tab.get("hero"): raise BriefError(f"tab {idx}: a hero card is required (the one moment)")
    b += '<g class="float">' + hero(tab["hero"], hx, hy, hw, hh) + '</g>'     # the one moment drifts gently; resting frame unchanged
    if "mini" in fr:
        mx_, my_, mw_, mh_ = fr["mini"]
        if rid == "R5": my_ = max(my_, hy + hh + 34)
        if not tab.get("mini"): raise BriefError(f"tab {idx}: recipe {rid} needs a 'mini' supporting card")
        b += mini(tab["mini"], mx_, my_, mw_, mh_)
    if CTX["clicks"] > 1: raise BriefError(f"tab {idx}: {CTX['clicks']} cursors; exactly one click per image (on the hero's button)")
    alt = tab.get("alt", "").strip()
    if not alt or len(alt) < 40: raise BriefError(f"tab {idx}: alt text missing or too short (one or two specific sentences)")
    CTX.setdefault("texts", {})[idx] = visible_text(b)
    return L.canvas(b, title=tab.get("title", ""), desc=alt)

def visible_text(svg_body):
    from html import unescape
    return [unescape(t) for t in re.findall(r"<text[^>]*>(.*?)</text>", svg_body, re.S)]

NUM = re.compile(r"(?<![\w:])[$£€]?\d[\d,]*(?:\.\d+)?%?(?![\w:])")
def _safe_eval(expr):
    import ast, operator as op
    ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.USub: op.neg, ast.Mod: op.mod}
    cmps = {ast.Eq: lambda a, b: abs(a - b) < 1e-6, ast.NotEq: lambda a, b: abs(a - b) >= 1e-6, ast.Lt: op.lt, ast.LtE: op.le, ast.Gt: op.gt, ast.GtE: op.ge}
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in ops: return ops[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in ops: return ops[type(n.op)](ev(n.operand))
        if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "round": return round(*[ev(x) for x in n.args])
        if isinstance(n, ast.Compare) and len(n.ops) == 1 and type(n.ops[0]) in cmps: return cmps[type(n.ops[0])](ev(n.left), ev(n.comparators[0]))
        raise BriefError(f"checks: only numbers, + - * / %, round() and one comparison are allowed: {expr}")
    return ev(ast.parse(expr, mode="eval"))

def check_numbers(br, texts):
    """Every derived number is declared and true; every declared number is drawn exactly as written."""
    issues = []; covered = set()
    def where_txt(w): return " ".join(texts.get(w, []))
    for c in br.get("checks", []):
        ws = c.get("where"); ws = ws if isinstance(ws, list) else [ws]
        for w in ws: covered.add(w)
        if "expr" in c:
            try:
                if _safe_eval(c["expr"]) is not True: issues.append(f'checks: "{c["expr"]}" is false. The numbers in the image must add up.')
            except BriefError as e: issues.append(str(e))
            except ZeroDivisionError: issues.append(f'checks: division by zero in "{c["expr"]}"')
            for sh in c.get("shows", []):
                if not any(sh in where_txt(w) for w in ws): issues.append(f'checks: "{sh}" is declared for {ws} but is not drawn there exactly like that')
        if "same" in c:
            missing = [w for w in ws if c["same"] not in where_txt(w)]
            if missing: issues.append(f'checks: "{c["same"]}" must appear in {ws}; missing in {missing}')
    # every quantity drawn must be accounted for by value in that image's declarations (expr, shows, same or fact)
    def vals(sx):
        return {float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", sx)}
    declared = {}
    for c in br.get("checks", []):
        ws = c.get("where"); ws = ws if isinstance(ws, list) else [ws]
        src = " ".join([c.get("expr", ""), c.get("same", "")] + list(c.get("shows", [])) + list(c.get("fact", []) if isinstance(c.get("fact"), list) else [c.get("fact", "")]))
        for w in ws: declared.setdefault(w, set()).update(vals(src))
    for w, t in texts.items():
        if w not in declared: continue
        for n in [n.rstrip(",.") for n in NUM.findall(" ".join(t))]:
            if not re.search(r"[$£€%]|\d,\d|\d\.\d", n): continue
            v = float(re.sub(r"[^\d.]", "", n.replace(",", "")))
            if v not in declared[w]:
                issues.append(f"{'tab ' + str(w) if isinstance(w, int) else w}: draws {n}, which no check or fact declares. Declare it (fact if it is standalone) so every number in the image is accounted for")
    # a "fact" must be standalone: block any fact value that other numbers in the same image produce
    def qty_vals(w):
        out = []
        for n in [n.rstrip(",.") for n in NUM.findall(" ".join(texts.get(w, [])))]:
            if re.search(r"[$£€%]|\d,\d|\d\.\d", n): out.append(float(re.sub(r"[^\d.]", "", n.replace(",", ""))))
        return out
    for c in br.get("checks", []):
        if "fact" not in c: continue
        ws = c.get("where"); ws = ws if isinstance(ws, list) else [ws]
        for w in ws:
            allv = qty_vals(w)
            for fv in vals(" ".join(c["fact"] if isinstance(c["fact"], list) else [c["fact"]])):
                others = sorted({x for x in allv if x != fv})
                hits = []
                for i_, a_ in enumerate(others):
                    for b_ in others[i_ + 1:]:
                        for label, r in (("sum", a_ + b_), ("difference", b_ - a_), ("product", a_ * b_), ("ratio", b_ / a_ if a_ else None),
                                         ("percent", 100 * a_ / b_ if b_ else None), ("percent change", 100 * (b_ - a_) / a_ if a_ else None)):
                            if r is not None and abs(r - fv) < 0.005 and fv not in (0, 1): hits.append(f"{label} of {a_:g} and {b_:g}")
                    for j_, b_ in enumerate(others[i_ + 1:], i_ + 1):
                        for c_ in others[j_ + 1:]:
                            if abs(a_ + b_ + c_ - fv) < 0.005: hits.append(f"sum of {a_:g}, {b_:g} and {c_:g}")
                if hits:
                    issues.append(f"{'tab ' + str(w) if isinstance(w, int) else w}: {fv:g} is declared a standalone fact but equals the {hits[0]} drawn in the same image. Declare it as an expr, or change the mock data so it is genuinely standalone")
    for w, t in texts.items():
        if w in covered or (isinstance(w, int) and br["tabs"][w - 1].get("no_derived")): continue
        nums = [n.rstrip(",.") for n in NUM.findall(" ".join(t))]
        nums = [n for n in nums if re.search(r"[$£€%]|\d,\d|\d\.\d", n)]      # quantities: money, percentages, decimals, grouped numbers (not IDs or years)
        if len(nums) >= 2:
            issues.append(f"{'tab ' + str(w) if isinstance(w, int) else w}: shows {len(nums)} numbers ({', '.join(nums[:4])}...) but declares no checks. Add image_brief.checks for every derived value (totals, differences, percentages, counts), or set no_derived: true on the tab if none is derived")
    return issues

WORD_NUM = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
            "fifteen": 15, "twenty": 20, "thirty": 30, "tenth": 10, "half": 50, "quarter": 25}
def _story_norm(s):
    from html import unescape
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip().lower()
def _digits(s): return {float(x.replace(",", "")) for x in re.findall(r"(?<![\w:\-/])\d[\d,]*(?:\.\d+)?", s)}
def _story_nums(s): return _digits(s) | {float(v) for w, v in WORD_NUM.items() if re.search(r"\b" + w + r"\b", s)}
def _rules_drawn(tab):
    out = [tab["rule"]] if tab.get("rule") else []
    def walk(o):
        if isinstance(o, dict):
            if o.get("type") == "rule" and o.get("text"): out.append(o["text"])
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk({k: v for k, v in tab.items() if k != "rule"}); return out
def check_story(spec, br, texts):
    """Copy-to-image story links: each tab's key rule and numbers must be in both the tab copy and the image (docs/IMAGE_BRIEF.md)."""
    F = spec.get("fields") or {}
    if spec.get("_demo") or not F.get("tab_content_1"): return []
    issues = []
    for i, tab in enumerate(br["tabs"], 1):
        copy = _story_norm(F.get(f"tab_content_{i}", "")); drawn = _story_norm(" ".join(texts.get(i, [])))
        st = tab.get("story") or []
        if not st: issues.append(f'story: tab {i}: no story links. Add "story": [{{"copy": exact phrase from tab_content_{i}, "image": exact text drawn}}] for the tab\'s key rule and numbers'); continue
        for e in st:
            c, im = _story_norm(e.get("copy", "")), _story_norm(e.get("image", ""))
            if not c or c not in copy: issues.append(f'story: tab {i}: copy "{e.get("copy", "")}" is not in tab_content_{i} word for word')
            if not im or im not in drawn: issues.append(f'story: tab {i}: image text "{e.get("image", "")}" is not drawn in tab {i} exactly like that')
            if c and im and _story_nums(c) != _story_nums(im):
                issues.append(f'story: tab {i}: the numbers differ between copy "{e.get("copy", "")}" and image "{e.get("image", "")}": say the same thing in both')
        for v in sorted(_digits(copy) - _story_nums(drawn)):
            issues.append(f"story: tab {i}: the tab copy says {v:g} but the image never shows it: draw it, or take it out of the copy")
        linked = [_story_norm(e.get("image", "")) for e in st]
        for r in _rules_drawn(tab):
            if not any(l_ and l_ in _story_norm(r) for l_ in linked):
                issues.append(f'story: tab {i}: the image draws the rule "{r}" but no story link ties it to the copy: add one, so the copy states the same rule')
    return issues

RESERVED_DOMAIN = re.compile(r"(^|\.)(example\.(com|net|org)|[a-z0-9-]+\.(example|test|invalid))$")
DOMAIN = re.compile(r"(?<![\w.-])((?:[a-z0-9-]+\.)+(?:com|co|io|net|org|app|ai|dev|so|us|uk|biz|info|xyz|tech|store|shop))(?![\w-])", re.I)
def check_domains(texts):
    """Images draw only reserved example domains (RFC 2606: example.com/.net/.org, *.example, *.test), never a real one (catalogue row 30)."""
    out = []
    for w, t in texts.items():
        for m in DOMAIN.finditer(" ".join(t)):
            d_ = m.group(1).lower()
            if not RESERVED_DOMAIN.search(d_):
                out.append(f"{'tab ' + str(w) if isinstance(w, int) else w}: draws the domain {d_}, which may be someone's real site or email. Use a reserved example domain (northwind.example, maya@lumen.example, example.com)")
    return sorted(set(out))

def check_glyphs(texts):
    from fontTools.ttLib import TTFont
    from paths import FONT_DIR
    cmap = set(TTFont(FONT_DIR + "Inter-Regular.ttf").getBestCmap())
    bad = sorted({c for t in texts.values() for s in t for c in s if not c.isspace() and ord(c) not in cmap})
    return [f"characters Inter cannot draw (they would render as boxes): {bad}"] if bad else []

# ------------------------------------------------------------------ cover (800x500) and share image (1200x630)
def big_button(x, y, w, h, label, ic=None, primary=True):
    return __import__("covers_v5").big_button(x, y, w, h, label, ic, primary)
def cover_canvas(b, title, desc):
    L.W, L.H = 800, 500; s = L.canvas(b, title=title, desc=desc); L.W, L.H = 1200, 800; return s
def render_cover(hub, d):
    H.set_hub(PALETTE[hub]); CTX.update(clicks=0, av=0, where="cover: "); k = d.get("kind")
    if k == "action":
        b = H.spot(150, 80, 500, 340) + L.rect(150, 80, 500, 340, 28, "#fff", L.LINE, 1.5, "e2")
        b += L.icon("hash", 186, 118, 30, L.SUB, 2.4) + T(226, 144, fit(d["channel"], 30, 700, 380, "channel"), 30, 700, L.INK) + H.hair(150, 176, 650)
        b += L.rect(186, 204, 64, 64, 16, "url(#gAcc)") + L.icon("sparkles", 202, 220, 32, "#fff", 2)
        b += T(272, 232, fit(d["title"], 32, 700, 350, "title"), 32, 700, L.INK, tnum=True) + T(272, 268, fit(d.get("sub", ""), 26, 500, 350, "sub"), 26, 500, L.MUTED)
        w1 = int(tw(d["primary"], 28, 700) + 38 + 56); w2 = int(tw(d.get("secondary", ""), 28, 700) + 56) if d.get("secondary") else 0
        if w1 + (w2 + 16 if w2 else 0) > 430: raise BriefError("cover: buttons too wide; shorten their labels")
        b += big_button(186, 312, w1, 72, d["primary"], d.get("icon", "check"))
        if w2: b += big_button(186 + w1 + 16, 312, w2, 72, d["secondary"], None, False)
        b += H.click(186 + w1 - 36, 368)
    elif k == "confirm":
        X, Y, W_ = 130, 60, 540; b = H.spot(X, Y, W_, 380) + L.rect(X, Y, W_, 380, 28, "#fff", L.LINE, 1.5, "e2") + f'<path d="M{X} {Y+56} V{Y+28} a28 28 0 0 1 28 -28 H{X+W_-28} a28 28 0 0 1 28 28 V{Y+56} Z" fill="#FBFBFD"/>' + H.hair(X, Y + 56, X + W_)
        for i in range(3): b += f'<circle cx="{X+30+i*22}" cy="{Y+28}" r="7" fill="#E3E6EE"/>'
        cx = X + W_ / 2; b += f'<circle cx="{cx}" cy="{Y+136}" r="44" fill="{L.OK_S}"/>' + L.icon("check", cx - 24, Y + 112, 48, L.OK, 2.6)
        b += T(cx, Y + 236, fit(d["title"], 40, 800, W_ - 60, "title", -0.8), 40, 800, L.INK, "middle", -0.8)
        bw = int(tw(d["button"], 28, 700) + 38 + 80); fit(d["button"], 28, 700, W_ - 160, "button")
        b += big_button(cx - bw / 2, Y + 270, bw, 72, d["button"], B.icon_ok(d.get("icon", "arrow-right"))) + H.click(cx + bw / 2 - 20, Y + 330)
    elif k == "code":
        X, Y, W_ = 140, 70, 520; b = H.spot(X, Y, W_, 360) + L.rect(X, Y, W_, 360, 28, "#fff", L.LINE, 1.5, "e2")
        b += f'<circle cx="{X+62}" cy="{Y+70}" r="34" fill="{L.OK_S}"/>' + L.icon(B.icon_ok(d.get("icon", "check")), X + 43, Y + 51, 38, L.OK, 2.6) + T(X + 116, Y + 84, fit(d["title"], 40, 800, W_ - 150, "title", -0.8), 40, 800, L.INK, ls=-0.8)
        b += L.rect(X + 32, Y + 140, W_ - 64, 140, 20, L.ACC_S, L.ACC, 2.5) + T(X + 62, Y + 186, fit(d["label"], 26, 700, W_ - 124, "label"), 26, 700, L.ACC_D) + T(X + 62, Y + 250, fit(d["code"], 52, 800, W_ - 124, "code", 6), 52, 800, L.INK, ls=6)
        if d.get("foot"): b += T(X + 32, Y + 326, fit(d["foot"], 26, 600, W_ - 64, "foot"), 26, 600, L.SUB, tnum=True)
    elif k == "score":
        # with stars: the rating row sits under the title; without stars (a metric card) the card is shorter and centred
        st_ = "stars" in d; Hc = 380 if st_ else 296; dy = 0 if st_ else -84
        X, Y, W_ = 130, (500 - Hc) // 2 if not st_ else 60, 540; b = H.spot(X, Y, W_, Hc) + L.rect(X, Y, W_, Hc, 28, "#fff", L.LINE, 1.5, "e2")
        b += T(X + 36, Y + 76, fit(d["title"], 36, 800, W_ - 72, "title", -0.6), 36, 800, L.INK, ls=-0.6)
        if st_: b += H.stars(X + 36, Y + 140, int(d["stars"]), 54, 14)
        b += H.hair(X + 36, Y + 196 + dy, X + W_ - 36) + T(X + 36, Y + 262 + dy, fit(d["label"], 28, 700, 220, "label"), 28, 700, L.MUTED) + T(X + 36, Y + 330 + dy, fit(d["value"], 60, 800, 260, "value", -1.5), 60, 800, L.INK, ls=-1.5, tnum=True)
        if d.get("delta"):
            lab = d["delta"]; cw = int(tw(lab, 26, 600) + 56); b += B.chip(X + W_ - 36 - cw, Y + 282 + dy, lab, d.get("delta_kind") or ("bad" if re.match(r"\s*(down|lowest|fell|dropped|worst|[-\u2212])", lab.lower()) else "ok"), cw, 52, 26)   # a negative fact is never drawn green
    else:
        raise BriefError('cover.kind must be one of "action", "confirm", "code", "score"')
    alt = d.get("alt", "").strip()
    if len(alt) < 20: raise BriefError("cover: alt text missing or too short")
    CTX.setdefault("texts", {})["cover"] = visible_text(b)
    return cover_canvas(b, d.get("title", ""), alt)

def og_lines(headline, lines=None):
    size = 50
    if not lines:
        lines = [""]
        for wd in headline.split():
            cand = (lines[-1] + " " + wd).strip()
            if tw(cand, size, 800, -1.2) <= 480: lines[-1] = cand
            else: lines.append(wd)
    for l in lines:
        if tw(l, size, 800, -1.2) > 480: raise BriefError(f"og: headline line too wide for the 480px column: {l!r}")
    if len(lines) > 3: raise BriefError("og: headline needs more than 3 lines; shorten it")
    if len(lines) > 1 and len(lines[-1].split()) == 1: raise BriefError(f"og: orphan last line {lines[-1]!r}; set og.lines to balance the break")
    return lines

def render_og_svg(hub, d, cover_src):
    import outline
    src = cover_src
    for pat in [r'<rect width="800" height="500" fill="url\(#bg\)"/>', r'<rect width="800" height="500" fill="url\(#glowA\)"/>',
                r'<rect width="800" height="500" fill="url\(#glowB\)"/>', r'<rect width="800" height="500" fill="url\(#grid\)" mask="url\(#gridMask\)"/>']:
        src = re.sub(pat, '', src)
    cov = base64.b64encode(outline.convert(src).encode()).decode()
    H.set_hub(PALETTE[hub]); lines = og_lines(d["headline"], d.get("lines"))
    y0 = 315 - (len(lines) * 62 + 70) / 2 + 40
    b = T(72, y0 - 18, "emergent", 30, 800, L.ACC_D, ls=-0.5)
    for i, l in enumerate(lines): b += T(72, y0 + 44 + i * 62, l, 50, 800, L.INK, ls=-1.2)
    b += T(72, y0 + 44 + len(lines) * 62 + 10, "From a prompt to a working app. Free to start.", 22, 500, L.SUB)
    b += f'<image x="590" y="130" width="590" height="369" href="data:image/svg+xml;base64,{cov}"/>'
    L.W, L.H = 1200, 630; s = L.canvas(b, title="", desc=""); L.W, L.H = 1200, 800
    return outline.convert(s)

# ------------------------------------------------------------------ gates, lint, render
def gates(svg, kind):
    import qa3
    issues = qa3.run(svg)
    if kind == "cover":
        issues = [i for i in issues if not i.startswith("off-canvas")]
        small = [s for s in map(float, re.findall(r'font-size="([\d.]+)"', svg)) if s * 360 / 800 < 11]
        if small: issues.append(f"legibility: text under 26 design px on the cover ({min(small)})")
    else:
        small = [s for s in map(float, re.findall(r'font-size="([\d.]+)"', svg)) if s * 830 / 1200 < 11]
        if small: issues.append(f"legibility: text under 16 design px ({min(small)})")
    return issues

def brief_of(spec):
    br = spec.get("image_brief")
    if not br: raise BriefError("spec has no image_brief")
    tabs = br.get("tabs", [])
    if len(tabs) != 4: raise BriefError(f"image_brief needs exactly 4 tabs (found {len(tabs)})")
    return br

def build_all(spec):
    """Render every image in memory. Returns (outputs, issues, warnings). outputs: list of (relpath, bytes|str)."""
    hub = spec["hub"]; br = brief_of(spec); out, issues = [], []; CTX["warn"] = []; CTX["balance"] = []; CTX["texts"] = {}
    cfg = json.load(open(os.path.join(REPO, "config", "collections.json")))
    d = f"images/{cfg['hubs'][hub]['repo_dir']}/{spec['url'].rsplit('/', 1)[1]}"
    if spec.get("_demo"): d = f"images/_demo/{spec['url'].rsplit('/', 1)[1]}"
    import outline
    for i, tab in enumerate(br["tabs"], 1):
        try:
            src = render_tab(hub, tab, i); g = gates(src, "uc")
            if g: issues += [f"tab {i}: gate: {x}" for x in g]
            else: out.append((f"{d}/uc-{i}.svg", outline.convert(src)))
        except BriefError as e: issues.append(str(e))
    cover_src = None
    try:
        cover_src = render_cover(hub, br.get("cover", {})); g = gates(cover_src, "cover")
        if g: issues += [f"cover: gate: {x}" for x in g]
        else: out.append((f"{d}/cover.svg", outline.convert(cover_src)))
    except BriefError as e: issues.append(str(e))
    og = br.get("og", {})
    try:
        if not og.get("headline"): raise BriefError("og: headline missing")
        if len(og.get("alt", "")) < 20: raise BriefError("og: alt text missing or too short")
        if cover_src: out.append((f"{d}/og.svg.tmp", render_og_svg(hub, og, cover_src)))
    except BriefError as e: issues.append(str(e))
    issues += CTX.get("balance", [])
    texts = dict(CTX.get("texts", {}))
    issues += check_numbers(br, texts) + check_glyphs(texts) + check_story(spec, br, texts) + (check_domains(texts) if (spec.get("fields") and not spec.get("_demo")) else [])   # reference scenes rebuild approved live images: untouched
    cov = br.get("cover", {})
    if cov.get("kind") == "code" and not re.fullmatch(r"[A-Z0-9][A-Z0-9-]{3,15}", str(cov.get("code", ""))):
        issues.append(f'cover: the code card is for a referral or discount code (like SAVE20); "{cov.get("code")}" is not one. Use the action, confirm or score cover (catalogue row 31)')
    return out, issues, list(CTX.get("warn", []))

def lint(spec):
    try:
        _, issues, warns = build_all(spec)
    except BriefError as e:
        return [str(e)], []
    return issues, warns

def render_spec(spec_path, write=True):
    import raster, tempfile
    from PIL import Image
    from paths import REVIEW
    spec = json.load(open(spec_path)); out, issues, warns = build_all(spec)
    if issues:
        print(f"BLOCKED {spec['url']}:"); [print("  -", x) for x in issues]; return False
    br = spec["image_brief"]; os.makedirs(REVIEW, exist_ok=True); pngs = []
    slug = spec["url"].rsplit("/", 1)[1]; d = os.path.dirname(out[0][0])
    os.makedirs(os.path.join(REPO, d), exist_ok=True)
    for rel, content in out:
        if rel.endswith(".svg.tmp"):
            tmp = os.path.join(tempfile.gettempdir(), f"_og_{slug}.svg"); open(tmp, "w").write(content)
            png = os.path.join(tempfile.gettempdir(), f"_og_{slug}.png"); raster.to_png(tmp, png, 1200, 630)
            buf = io.BytesIO(); Image.open(png).convert("RGB").save(buf, "PNG", optimize=True)
            if write: open(os.path.join(REPO, d, "og.png"), "wb").write(buf.getvalue())
            continue
        if write: open(os.path.join(REPO, rel), "w").write(content)
    # spec.images: paths and alt text
    alts = {f"tab_image_{i}": t["alt"] for i, t in enumerate(br["tabs"], 1)}
    alts["cover_image"] = br["cover"]["alt"]; alts["share_image"] = br["og"]["alt"]
    files = {**{f"tab_image_{i}": f"{d}/uc-{i}.svg" for i in range(1, 5)}, "cover_image": f"{d}/cover.svg", "share_image": f"{d}/og.png"}
    spec.setdefault("images", {})
    for k in files: spec["images"][k] = {**spec["images"].get(k, {}), "path": files[k], "alt": alts[k]}
    if write: json.dump(spec, open(spec_path, "w"), indent=1, ensure_ascii=False)
    # contact sheet: 4 use-case images at true desktop size, the cover in its card, the share image
    for i in range(1, 5):
        p = os.path.join(tempfile.gettempdir(), f"_{slug}_uc{i}.png"); raster.to_png(os.path.join(REPO, d, f"uc-{i}.svg"), p, 830); pngs.append(p)
    cp = os.path.join(tempfile.gettempdir(), f"_{slug}_cover.png"); raster.to_png(os.path.join(REPO, d, "cover.svg"), cp, 720)
    sheet = Image.new("RGB", (830 * 2 + 20, 553 * 2 + 20 + 360), "white")
    for i, p in enumerate(pngs): sheet.paste(Image.open(p).convert("RGB").resize((830, 553)), ((i % 2) * 850, (i // 2) * 573))
    card = Image.new("RGB", (392, 300), "#F7F7F9"); card.paste(Image.new("RGB", (376, 290), "white"), (8, 5)); card.paste(Image.open(cp).convert("RGB").resize((360, 225)), (16, 13))
    sheet.paste(card, (0, 1166)); sheet.paste(Image.open(os.path.join(REPO, d, "og.png")).convert("RGB").resize((600, 315)), (420, 1166))
    sp = os.path.join(REVIEW, f"{d.split('/')[1]}_{slug}.png"); sheet.save(sp)
    spec["_sheet"] = sp
    print(f"RENDERED {spec['url']} -> {d}/ (6 files); contact sheet: {sp}")
    for w_ in warns: print("  note:", w_)
    return True

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "lint":
        bad = 0
        for p in a[1:]:
            iss, wr = lint(json.load(open(p))); bad += len(iss)
            print(("OK      " if not iss else "BLOCKED ") + p); [print("  -", x) for x in iss]; [print("  note:", x) for x in wr]
        sys.exit(1 if bad else 0)
    elif a[0] == "render":
        ok = all([render_spec(p) for p in a[1:]]); sys.exit(0 if ok else 1)
    elif a[0] == "demo":
        import glob
        for p in sorted(glob.glob(os.path.join(REPO, "pipeline", "briefs", "*.json"))):
            render_spec(p, write=True)
    else: sys.exit(__doc__)
