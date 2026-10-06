"""Block library for the image engine. Every block reproduces the styling of an element in an approved v5 scene
(scenes_v5.py / hubs_v5.py): same sizes, weights, colours, radii and spacing. A block renders at (x, y) with width w
and returns (svg, height). Text that does not fit raises BriefError naming the field and the overflow, so the
writer shortens the brief instead of anyone shrinking type."""
import math, re
import _alias  # noqa: F401
import ds5 as L
import hubs_v5 as H
from qa import width as tw

class BriefError(Exception):
    pass

CTX = {"clicks": 0, "where": ""}

def fit(text, size, weight, maxw, where, ls=0):
    text = str(text)
    w = tw(text, size, weight, ls)
    if w > maxw + 0.5:
        raise BriefError(f'{CTX["where"]}{where}: "{text}" is {w:.0f}px wide at {size}px, the space is {maxw:.0f}px. Shorten it.')
    return text

def T(*a, **k): return L.T(*a, **k)
def A(): return L.ACC
def AD(): return L.ACC_D
def AS(): return L.ACC_S
def hair(x1, y, x2): return H.hair(x1, y, x2)
def esc(s): return L.esc(s)

KINDS = {"ok", "warn", "bad", "acc", "n"}
def chipw(label, size=16, dot=True): return int(tw(label, size, 600) + (56 if dot else 40))
def chip(x, y, label, kind="acc", w=None, h=36, size=16, dot=True, where="chip"):
    if kind not in KINDS: raise BriefError(f'{CTX["where"]}{where}: chip kind "{kind}" must be one of {sorted(KINDS)}')
    return L.chip(x, y, label, kind, w or chipw(label, size, dot), h, size, dot)

def click(x, y):
    CTX["clicks"] += 1
    return H.click(x, y)

def button(x, y, label, primary=True, ic=None, w=None, h=52, do_click=False, where="button"):
    bw = int(w or tw(label, 17, 600) + (98 if ic else 72))
    fit(label, 17, 600, bw - (50 if ic else 30), where)
    s = L.button(x, y, bw, h, label, primary, ic)
    if do_click: s += click(x + bw - 18, y + h - 12)
    return s, bw

def avatar(cx, cy, r, ini, idx=0):
    pairs = [("#C2410C", "#9F1239"), ("#2563EB", "#4338CA"), ("#047857", "#115E59"), (L.ACC, getattr(L, "ACC2", L.ACC))]
    c1, c2 = pairs[idx % len(pairs)]
    CTX["av"] = CTX.get("av", 0) + 1
    return L.avatar(cx, cy, r, ini, c1, c2, gid=f"eav{CTX['av']}")

def icon_ok(name):
    import os
    from paths import ICON_DIR
    if not os.path.exists(os.path.join(ICON_DIR, name + ".svg")):
        raise BriefError(f'{CTX["where"]}icon "{name}" is not a Lucide icon (see lucide.dev/icons)')
    return name

MONEY = re.compile(r"^\$?(-?[\d,]+(?:\.\d+)?)$")
def money(s):
    m = MONEY.match(str(s).replace(" ", ""))
    return float(m.group(1).replace(",", "")) if m else None

# ---------------------------------------------------------------- blocks
def b_heading(d, x, y, w):
    s, h = "", 0
    right = d.get("right"); rw = 0
    if right:
        rw = tw(right, 30, 700, -0.3) + 16
    chip_d = d.get("chip"); cw = chipw(chip_d[0]) if chip_d else 0
    if d.get("eyebrow"):
        s += T(x, y + 16, fit(d["eyebrow"], 16, 600, w - max(rw, cw) - 12, "eyebrow", 1), 16, 600, L.MUTED, ls=1); h += 38
    size = d.get("size", 24 if w < 700 else 22)
    s += T(x, y + h + size, fit(d["title"], size, 700, w - max(rw, cw) - 16, "title", -0.3), size, 700, L.INK, ls=-0.3)
    if right:
        s += T(x + w, y + h + size, right, 30, 700, L.INK, "end", -0.3, True)
        if d.get("right_sub"): s += T(x + w, y + h + size + 30, d["right_sub"], 16, 600, L.MUTED, "end")
    if chip_d: s += chip(x + w - cw, y + h + size - 26, chip_d[0], chip_d[1] if len(chip_d) > 1 else "acc", cw, 36)
    h += size + 8
    if d.get("sub"):
        sw = (tw(d["right_sub"], 16, 600) + 16) if d.get("right_sub") else 0
        s += T(x, y + h + 18, fit(d["sub"], 16, 500, w - sw - 12, "sub"), 16, 500, L.MUTED); h += 26
    return s, h + 4

def b_rule(d, x, y, w):
    ic = icon_ok(d.get("icon", "git-branch"))
    s = L.rect(x, y, w, 46, 12, AS()) + L.icon(ic, x + 14, y + 11, 22, AD(), 2)
    s += T(x + 46, y + 29, fit(d["text"], 17, 600, w - 62, "rule"), 17, 600, AD())
    return s, 46

def b_steps(d, x, y, w):
    s = ""; items = d["items"]
    if not 2 <= len(items) <= 5: raise BriefError(f'{CTX["where"]}steps: 2-5 items')
    live = [i for i in items if i.get("state") == "live"]
    if len(live) > 1: raise BriefError(f'{CTX["where"]}steps: at most one "live" step (the moment shown)')
    for i, it in enumerate(items):
        cy = y + 20 + i * 78; st = it.get("state", "next")
        if i < len(items) - 1:
            s += f'<line x1="{x+18}" y1="{cy+18}" x2="{x+18}" y2="{cy+60}" stroke="{L.ACC_M if st in ("done","skip","live") else L.HAIR}" stroke-width="2.5"/>'
        if st == "done": s += f'<circle cx="{x+18}" cy="{cy}" r="16" fill="{L.OK_S}"/>' + L.icon("check", x + 8, cy - 10, 20, L.OK, 2.6)
        elif st == "skip": s += f'<circle cx="{x+18}" cy="{cy}" r="15" fill="#fff" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="3 4"/>'
        elif st == "live": s += f'<circle class="pulse" cx="{x+18}" cy="{cy}" r="18" fill="{A()}" opacity="0.3"/><circle cx="{x+18}" cy="{cy}" r="24" fill="{A()}" opacity="0.12"/><circle cx="{x+18}" cy="{cy}" r="16" fill="url(#gAcc)"/><circle cx="{x+18}" cy="{cy}" r="5" fill="#fff"/>'
        else: s += f'<circle cx="{x+18}" cy="{cy}" r="15" fill="#fff" stroke="#CBD5E1" stroke-width="2"/>'
        col = L.MUTED if st in ("skip", "next") else L.INK
        right = it.get("right", ""); rw = (chipw(right) if st == "live" else tw(right, 16, 600)) + 16 if right else 0
        s += T(x + 52, cy - 4, fit(it["title"], 20, 600, w - 52 - rw, f"steps[{i}].title"), 20, 600, col)
        if it.get("sub"): s += T(x + 52, cy + 22, fit(it["sub"], 16, 500, w - 52 - rw, f"steps[{i}].sub"), 16, 500, L.MUTED)
        if right:
            if st == "live": s += chip(x + w - chipw(right), cy - 18, right, "acc")
            else: s += T(x + w, cy + 2, right, 16, 600, L.MUTED, "end", tnum=True)
    return s, 20 + (len(items) - 1) * 78 + 34

def b_kv(d, x, y, w):
    s = ""
    for i, row in enumerate(d["rows"]):
        k, v = row[0], row[1]; hl = len(row) > 2 and row[2]
        ry = y + i * 62
        if hl: s += L.rect(x - 16, ry, w + 32, 56, 12, AS(), A(), 2)
        s += T(x, ry + 24, fit(k, 16, 500, w, f"kv[{i}]"), 16, 500, L.SUB if hl else L.MUTED)
        s += T(x, ry + 48, fit(v, 19, 700, w, f"kv[{i}]"), 19, 700, L.INK, tnum=True)
    return s, len(d["rows"]) * 62 - 6

def b_lineitems(d, x, y, w):
    if d.get("compact"):                       # plain rows and a hairline total, as in the approved order page
        s = ""; tot = 0; ok = True
        for i, (name, amt) in enumerate(d["items"]):
            yy = y + 20 + i * 36
            s += T(x, yy, fit(name, 17, 500, w - tw(amt, 17, 600) - 24, f"lineitems[{i}]"), 17, 500, L.SUB) + T(x + w, yy, amt, 17, 600, L.INK, "end", tnum=True)
            m = money(amt); ok = ok and m is not None; tot += m or 0
        lab, amt = d["total"]; ty = y + 20 + len(d["items"]) * 36 - 6
        if ok and money(amt) is not None and abs(tot - money(amt)) > 0.005:
            raise BriefError(f'{CTX["where"]}lineitems: items add up to {tot:,.2f} but the total says {amt}. Numbers must add up.')
        s += hair(x, ty, x + w) + T(x, ty + 36, lab, 18, 700, L.INK) + T(x + w, ty + 36, amt, 20, 800, L.INK, "end", tnum=True)
        return s, ty + 42 - y
    s = hair(x, y, x + w); tot = 0; ok = True
    for i, (name, amt) in enumerate(d["items"]):
        yy = y + 34 + i * 38
        s += T(x + 4, yy, fit(name, 17, 500, w - tw(amt, 17, 600) - 24, f"lineitems[{i}]"), 17, 500, L.SUB) + T(x + w - 4, yy, amt, 17, 600, L.INK, "end", tnum=True)
        m = money(amt); ok = ok and m is not None; tot += m or 0
    ty = y + 34 + len(d["items"]) * 38 - 8
    lab, amt = d["total"]
    if ok and money(amt) is not None and abs(tot - money(amt)) > 0.005:
        raise BriefError(f'{CTX["where"]}lineitems: items add up to {tot:,.2f} but the total says {amt}. Numbers must add up.')
    s += L.rect(x - 12, ty, w + 24, 62, 12, AS(), A(), 2) + T(x + 4, ty + 38, fit(lab, 18, 700, w / 2, "total"), 18, 700, L.INK) + T(x + w - 4, ty + 38, amt, 22, 800, L.INK, "end", -0.2, True)
    return s, ty + 62 - y

def b_fields(d, x, y, w):
    s = ""
    for i, (lab, val) in enumerate(d["items"]):
        fy = y + i * 98
        s += T(x, fy + 16, fit(lab, 16, 600, w, f"fields[{i}].label"), 16, 600, L.MUTED)
        s += L.rect(x, fy + 26, w, 52, 12, "#F8FAFC", L.LINE, 1.2) + T(x + 16, fy + 59, fit(val, 18, 600, w - 32, f"fields[{i}].value"), 18, 600, L.INK)
    return s, len(d["items"]) * 98 - 20

def b_textarea(d, x, y, w):
    s, h = "", 0
    if d.get("label"): s += T(x, y + 16, fit(d["label"], 16, 600, w, "textarea.label"), 16, 600, L.MUTED); h = 26
    lines = d["lines"]; bh = 34 + len(lines) * 28
    s += L.rect(x, y + h, w, bh, 12, "#F8FAFC", L.LINE, 1.2)
    for i, l in enumerate(lines): s += T(x + 18, y + h + 40 + i * 28, fit(l, 18, 500, w - 36, f"textarea.lines[{i}]"), 18, 500, L.INK)
    return s, h + bh

def b_quote(d, x, y, w):
    txt = "\u201c" + d["text"] + "\u201d"
    bh = 84 if d.get("sub") else 58
    s = L.rect(x, y, w, bh, 14, "#FAFAFA", L.HAIR, 1.5) + T(x + 20, y + 36, fit(txt, 18, 500, w - 40, "quote"), 18, 500, L.INK)
    if d.get("sub"): s += T(x + 20, y + 64, fit(d["sub"], 16, 500, w - 40, "quote.sub"), 16, 500, L.MUTED)
    return s, bh

def b_button(d, x, y, w):
    full = d.get("full", False); ic = d.get("icon"); ic and icon_ok(ic)
    h = d.get("h", 56 if full else 50)
    nat = w if full else int(d.get("w") or tw(d["label"], 17, 600) + (98 if ic else 72))
    bx = x + w - nat if d.get("align") == "right" else (x + (w - nat) / 2 if d.get("align") == "center" else x)
    s, bw = button(bx,
                   y, d["label"], d.get("primary", True), ic, nat, h, d.get("click", False), "button")
    return s, h

def b_buttons(d, x, y, w):
    s = ""; cx = x
    for i, it in enumerate(d["items"]):
        ic = it.get("icon"); ic and icon_ok(ic)
        part, bw = button(cx, y, it["label"], i == 0 if "primary" not in it else it["primary"], ic, None, 52, it.get("click", False), f"buttons[{i}]")
        s += part; cx += bw + 12
    if cx - 12 > x + w: raise BriefError(f'{CTX["where"]}buttons: the row is {cx-12-x:.0f}px, the space is {w:.0f}px. Fewer or shorter buttons.')
    return s, 52

def b_code(d, x, y, w):
    if not d.get("label"):                      # short centred code box, as in the approved discount-code card
        size = d.get("size", 30)
        return L.rect(x, y, w, 70, 14, AS(), A(), 2) + T(x + w / 2, y + 46, fit(d["code"], size, 800, w - 40, "code", 4), size, 800, L.INK, "middle", 4), 70
    s = L.rect(x, y, w, 120, 16, AS(), A(), 2) + T(x + 26, y + 38, fit(d["label"], 16, 700, w - 52, "code.label"), 16, 700, AD())
    size = d.get("size", 40)
    s += T(x + 26, y + 92, fit(d["code"], size, 800, w - 52, "code", 5 if size >= 36 else 1), size, 800, L.INK, ls=5 if size >= 36 else 1)
    return s, 120

def b_stars(d, x, y, w):
    s, h = "", 0
    if d.get("label"): s += T(x, y + 18, fit(d["label"], 17, 700, w, "stars.label"), 17, 700, L.INK); h = 26
    n = int(d["n"]); size = d.get("size", 30)
    if not 0 <= n <= 5: raise BriefError(f'{CTX["where"]}stars: n must be 0-5')
    s += H.stars(x, y + h + size / 2 + 6, n, size, 6)
    return s, h + size + 12

def b_scale(d, x, y, w):
    s, h = "", 0
    for i, line in enumerate(d.get("question", [])):
        s += T(x, y + 28 + i * 30, fit(line, 24, 800, w, f"scale.question[{i}]", -0.4), 24, 800, L.INK, ls=-0.4); h = 28 + i * 30 + 18
    n = d.get("n", 5); sel = d.get("selected"); bs = min(76, (w - (n - 1) * 14) / n)
    for i in range(n):
        bx = x + i * (bs + 14); on = sel == i + 1
        s += L.rect(bx, y + h, bs, bs, 16, "url(#gAcc)" if on else "#F8FAFC", None if on else L.LINE, 1.5) + T(bx + bs / 2, y + h + bs / 2 + 10, str(i + 1), 26, 800, "#fff" if on else L.SUB, "middle", tnum=True)
    return s, h + bs

def b_chips(d, x, y, w):
    s = ""; cx = x
    for i, c in enumerate(d["items"]):
        lab, kind = c[0], c[1] if len(c) > 1 else "acc"; cw = chipw(lab)
        s += chip(cx, y, lab, kind, cw, 36, where=f"chips[{i}]"); cx += cw + 10
    if cx - 10 > x + w: raise BriefError(f'{CTX["where"]}chips: the row is {cx-10-x:.0f}px, the space is {w:.0f}px')
    return s, 36

def _cols(d, w):
    cols = d["columns"]; n = len(cols)
    fr = d.get("widths") or [1 / n] * n
    xs, acc = [], 0
    for f in fr: xs.append(acc * w); acc += f
    return cols, xs, [f * w for f in fr]

def b_table(d, x, y, w):
    cols, xs, ws = _cols(d, w); s = ""
    for c, cx in zip(cols, xs): s += T(x + cx, y + 18, fit(c.upper(), 16, 700, ws[cols.index(c)] - 12, "table.columns", 1), 16, 700, L.MUTED, ls=1)
    rh = d.get("row_h", 54); avatar_col = d.get("avatars", False)
    for i, row in enumerate(d["rows"]):
        ry = y + 34 + i * rh
        if d.get("highlight") == i: s += L.rect(x - 18, ry, w + 36, rh - 6, 12, AS())
        if d.get("bad") == i: s += L.rect(x - 18, ry, w + 36, rh - 6, 10, L.BAD_S)
        for j, cell in enumerate(row):
            cx = x + xs[j]; base = ry + rh / 2 + 4
            if isinstance(cell, list):           # [label, kind] -> chip
                cw = min(chipw(cell[0]), ws[j] - 8); s += chip(cx, base - 22, cell[0], cell[1], cw, 36, where=f"table[{i}][{j}]"); continue
            txt = str(cell)
            if j == 0 and avatar_col:
                ini = re.sub(r"[^A-Za-z]", "", txt)[:2].upper() or "A"
                s += avatar(cx + 20, base - 6, 20, ini, i); cx += 50
                s += T(cx, base, fit(txt, 19, 700, ws[j] - 58, f"table[{i}][0]"), 19, 700, L.INK); continue
            kind = None
            if re.match(r"^[+\u2212-]\d", txt) and d.get("signed_cols") and j in d["signed_cols"]: kind = L.BAD if txt[0] in "\u2212-" else L.OK
            wt = 700 if j == 0 or kind else (700 if d.get("num_cols") and j in d["num_cols"] else 500)
            col = kind or (L.INK if wt == 700 else L.SUB)
            s += T(cx, base, fit(txt, 19 if wt == 700 else 18, wt, ws[j] - 10, f"table[{i}][{j}]"), 19 if wt == 700 else 18, wt, col, tnum=True)
    return s, 34 + len(d["rows"]) * rh - 6

def b_list(d, x, y, w):
    s = ""; rh = d.get("row_h", 76); cards = d.get("cards", False)
    for i, it in enumerate(d["items"]):
        ry = y + i * (rh + (16 if cards else 0)); muted = it.get("muted", False)
        if cards: s += L.rect(x, ry, w, rh, 16, "#F8FAFC" if muted else "#fff", L.HAIR, 1.5)
        ix = x + (24 if cards else 0); cy = ry + rh / 2
        right_w = 0
        if "score" in it: right_w = 176
        elif it.get("chip"): right_w = chipw(it["chip"][0]) + 12
        elif it.get("right"): right_w = tw(it["right"], 18, 700) + 12
        tx = ix
        if it.get("initials"): s += avatar(ix + 24, cy, 22 if not cards else 24, it["initials"], i); tx = ix + 60
        s += T(tx, cy - 4, fit(it["name"], 19, 700, x + w - tx - right_w - (24 if cards else 0), f"list[{i}].name"), 19, 700, L.INK)
        if it.get("sub"): s += T(tx, cy + 22, fit(it["sub"], 16, 500, x + w - tx - right_w - (24 if cards else 0), f"list[{i}].sub"), 16, 500, L.MUTED)
        rx = x + w - (24 if cards else 0)
        if "score" in it:
            sc = int(it["score"]); good = sc >= d.get("threshold", 80)
            s += L.rect(rx - 162, cy - 6, 112, 12, 6, "#E5E7EB") + L.rect(rx - 162, cy - 6, 112 * sc / 100, 12, 6, "url(#gAcc)" if good else "#94A3B8")
            s += T(rx, cy + 8, str(sc), 22, 800, L.INK if good else L.MUTED, "end", tnum=True)
        elif it.get("chip"):
            cw = chipw(it["chip"][0]); s += chip(rx - cw, cy - 18, it["chip"][0], it["chip"][1], cw, where=f"list[{i}].chip")
        elif it.get("right"):
            s += T(rx, cy + 6, it["right"], 18, 700, L.INK, "end", tnum=True)
    n = len(d["items"])
    return s, n * rh + (n - 1) * (16 if cards else 0)

def b_timeline(d, x, y, w):
    items = d["items"]; n = len(items); s = ""
    if not 2 <= n <= 4: raise BriefError(f'{CTX["where"]}timeline: 2-4 points')
    pad = 110; xs = [x + pad + i * (w - 2 * pad) / (n - 1) for i in range(n)]; cy = y + 48
    reached = max([i for i, it in enumerate(items) if it.get("kind") != "next"] or [0])
    s += f'<line x1="{xs[0]}" y1="{cy}" x2="{xs[-1]}" y2="{cy}" stroke="{L.HAIR}" stroke-width="5" stroke-linecap="round"/>'
    if reached: s += f'<line x1="{xs[0]}" y1="{cy}" x2="{xs[reached-1] if items[reached].get("kind")=="bad" else xs[reached]}" y2="{cy}" stroke="{L.ACC_M}" stroke-width="5" stroke-linecap="round"/>'
    span = (w - 2 * pad) / (n - 1)
    for i, it in enumerate(items):
        k = it.get("kind", "ok"); col = L.BAD if k == "bad" else (A() if k != "next" else "#CBD5E1")
        if it.get("live") or k == "bad": s += f'<circle class="pulse" cx="{xs[i]}" cy="{cy}" r="16" fill="{col}" opacity="0.3"/>'
        s += T(xs[i], cy - 34, fit(it["label"], 20, 700, span - 20, f"timeline[{i}].label"), 20, 700, L.INK, "middle")
        s += f'<circle cx="{xs[i]}" cy="{cy}" r="16" fill="{col}"/>'
        if it.get("chip"):
            cw = min(chipw(it["chip"]), span - 16); s += chip(xs[i] - cw / 2, cy + 28, it["chip"], "bad" if k == "bad" else ("n" if k == "next" else "ok"), cw, 36, where=f"timeline[{i}].chip")
    return s, 48 + 28 + 36 + 2

def b_bars(d, x, y, w):
    s = ""; mx = d.get("max", 5); lw = d.get("label_w", 100)
    for i, it in enumerate(d["items"]):
        ry = y + i * 60; v = float(it["value"]); low = it.get("flag", False)
        s += T(x, ry + 26, fit(it["label"], 18, 700, lw - 12, f"bars[{i}]"), 18, 700, L.INK)
        bw = w - lw - 70
        s += L.rect(x + lw, ry + 10, bw, 22, 11, AS()) + L.rect(x + lw, ry + 10, max(22, bw * v / mx), 22, 11, L.BAD if low else "url(#gAcc)")
        s += T(x + w, ry + 28, it.get("display", f"{v:g}"), 19, 800, L.BAD if low else L.INK, "end", tnum=True)
    return s, len(d["items"]) * 60 - 16

def b_budget(d, x, y, w):
    used, this, total = float(d["used"]), float(d["this"]), float(d["total"])
    if used + this > total + 1e-9 and not d.get("over_ok"): raise BriefError(f'{CTX["where"]}budget: used + this ({used+this:g}) exceeds total ({total:g})')
    fmt = d.get("fmt", "${:,.0f}")
    big = fmt.format(used + this); s = T(x, y + 42, big, 42, 800, L.INK, ls=-0.8, tnum=True)
    s += T(x + tw(big, 42, 800, -0.8) + 14, y + 42, f"of {fmt.format(total)}", 20, 500, L.MUTED, tnum=True)
    by = y + 66; s1 = w * used / total; s2 = w * this / total
    s += L.rect(x, by, w, 16, 8, AS()) + L.rect(x, by, s1 + 8, 16, 8, "url(#gAcc)") + f'<rect class="glow" x="{x+s1}" y="{by}" width="{s2}" height="16" fill="{L.ACC_M}"/>' + f'<line x1="{x+s1}" y1="{by-4}" x2="{x+s1}" y2="{by+20}" stroke="#fff" stroke-width="2"/>'
    labs = d.get("legend", ["Spent", "This one", "Left"])
    vals = [used, this, total - used - this]; lx = x
    for lab, v, col in zip(labs, vals, [A(), L.ACC_M, AS()]):
        t = f"{lab} {fmt.format(v)}"; s += f'<circle cx="{lx+6}" cy="{by+42}" r="6" fill="{col}"/>' + T(lx + 20, by + 48, t, 16, 600, L.SUB, tnum=True); lx += tw(t, 16, 600) + 52
    if lx - 52 > x + w: raise BriefError(f'{CTX["where"]}budget legend is too wide; shorten the labels')
    return s, 66 + 56

def b_checks(d, x, y, w):
    s = ""; cx, cy, lines = x, y, 1
    for i, lab in enumerate(d["items"]):
        iw = 28 + tw(lab, 16, 600) + 28
        if cx + iw - 28 > x + w and cx > x: cx = x; cy += 36; lines += 1
        s += L.icon("circle-check", cx, cy, 20, L.OK, 2.2) + T(cx + 28, cy + 16, fit(lab, 16, 600, w - 28, f"checks[{i}]"), 16, 600, L.SUB); cx += iw
    return s, lines * 36 - 14

def b_confirm(d, x, y, w):
    cx = x + w / 2
    s = f'<circle cx="{cx}" cy="{y+36}" r="36" fill="{L.OK_S}"/>' + L.icon("check", cx - 18, y + 18, 36, L.OK, 2.6)
    s += T(cx, y + 118, fit(d["title"], 28, 700, w, "confirm.title", -0.4), 28, 700, L.INK, "middle", -0.4)
    h = 128
    if d.get("sub"): s += T(cx, y + 152, fit(d["sub"], 17, 500, w, "confirm.sub"), 17, 500, L.MUTED, "middle"); h = 160
    return s, h

def b_status(d, x, y, w):
    k = d.get("kind", "ok"); bg, fg = {"ok": (L.OK_S, L.OK), "acc": (AS(), AD()), "warn": (L.WARN_S, L.WARN), "bad": (L.BAD_S, L.BAD)}[k]
    ic = icon_ok(d.get("icon", "check"))
    s = f'<circle cx="{x+22}" cy="{y+24}" r="22" fill="{bg}"/>' + L.icon(ic, x + 11, y + 13, 22, fg, 2.6)
    s += T(x + 60, y + 20, fit(d["title"], 26, 700, w - 60, "status.title", -0.3), 26, 700, L.INK, ls=-0.3, tnum=True)
    if d.get("sub"): s += T(x + 60, y + 48, fit(d["sub"], 17, 500, w - 60, "status.sub"), 17, 500, L.MUTED)
    return s, 56

def b_event(d, x, y, w):
    s = L.rect(x, y, w, 140, 16, AS()) + L.rect(x + 24, y + 24, 92, 92, 16, "#fff")
    s += T(x + 70, y + 58, d["month"].upper()[:3], 16, 700, AD(), "middle", 1) + T(x + 70, y + 100, str(d["day"]), 36, 800, L.INK, "middle", tnum=True)
    s += T(x + 140, y + 62, fit(d["title"], 22, 700, w - 164, "event.title"), 22, 700, L.INK) + T(x + 140, y + 92, fit(d.get("sub", ""), 17, 500, w - 164, "event.sub"), 17, 500, L.SUB)
    return s, 140

def b_slots(d, x, y, w):
    s = ""; items = d["items"]; sel = d.get("selected"); cw = (w - 16) / 2
    for i, t in enumerate(items):
        sx = x + (i % 2) * (cw + 16); sy = y + (i // 2) * 72; on = i == sel
        s += L.rect(sx, sy, cw, 58, 14, "url(#gAcc)" if on else "#fff", None if on else L.LINE, 1.5) + T(sx + cw / 2, sy + 36, fit(t, 18, 700, cw - 20, f"slots[{i}]"), 18, 700, "#fff" if on else L.INK, "middle", tnum=True)
    return s, ((len(items) + 1) // 2) * 72 - 14

def b_media(d, x, y, w):
    items = d["items"]; n = len(items); gap = 24; tw_ = (w - gap * (n - 1)) / n; s = ""
    for i, it in enumerate(items):
        tx = x + i * (tw_ + gap); th = tw_ * 0.5625
        s += L.rect(tx, y, tw_, th, 14, "#0F172A") + f'<circle cx="{tx+tw_/2}" cy="{y+th/2}" r="30" fill="#fff" opacity="0.94"/><path d="M{tx+tw_/2-9} {y+th/2-16} l24 16 l-24 16 z" fill="#0F172A"/>'
        if it.get("duration"): s += L.rect(tx + 14, y + th - 40, 62, 28, 8, "#1E293B") + T(tx + 45, y + th - 20, it["duration"], 16, 700, "#F1F5F9", "middle", tnum=True)
        s += T(tx, y + th + 42, fit(it["title"], 20, 700, tw_, f"media[{i}].title"), 20, 700, L.INK)
        if it.get("sub"): s += T(tx, y + th + 68, fit(it["sub"], 16, 500, tw_, f"media[{i}].sub"), 16, 500, L.MUTED)
        if "stars" in it: s += H.stars(tx + 2, y + th + 102, int(it["stars"]), 24, 6)
        if it.get("tag"):
            cw = min(chipw(it["tag"]), tw_ - 160); s += chip(tx + tw_ - cw, y + th + 86, it["tag"], "acc", cw, 34, where=f"media[{i}].tag")
    return s, (tw_ * 0.5625) + 118

def b_product(d, x, y, w):
    ic = icon_ok(d.get("icon", "package"))
    s = L.rect(x, y, w, 150, 16, "#F8FAFC", L.HAIR, 1.5) + L.rect(x + 24, y + 25, 100, 100, 16, AS()) + L.icon(ic, x + 50, y + 51, 48, A(), 1.6)
    bl = d.get("button"); bw = int(tw(bl, 17, 600) + 72) if bl else 0
    tw_avail = w - 148 - (bw + 40 if bl else 24)
    if d.get("eyebrow"): s += T(x + 148, y + 50, fit(d["eyebrow"], 16, 700, tw_avail, "product.eyebrow"), 16, 700, AD())
    s += T(x + 148, y + 84, fit(d["title"], 22, 700, tw_avail, "product.title"), 22, 700, L.INK)
    if d.get("sub"): s += T(x + 148, y + 112, fit(d["sub"], 16, 500, tw_avail, "product.sub"), 16, 500, L.MUTED)
    if bl:
        part, _ = button(x + w - bw - 24, y + 51, bl, True, None, bw, 48, d.get("click", False), "product.button"); s += part
    return s, 150

def b_doc_header(d, x, y, w):
    s = ""
    if d.get("initials"): s += L.rect(x, y, 52, 52, 14, "url(#gAcc)") + T(x + 26, y + 33, d["initials"][:2], 18, 800, "#fff", "middle")
    else: s += L.rect(x, y, 52, 52, 14, AS()) + L.icon(icon_ok(d.get("icon", "file-text")), x + 14, y + 14, 24, AD(), 2)
    lab = d.get("label", ""); lw = tw(lab, 16, 700, 2.5) + 16 if lab else 0
    s += T(x + 68, y + 22, fit(d["title"], 20, 700, w - 68 - lw, "doc_header.title"), 20, 700, L.INK) + T(x + 68, y + 46, fit(d.get("sub", ""), 16, 500, w - 68 - lw, "doc_header.sub"), 16, 500, L.MUTED)
    if lab: s += T(x + w, y + 22, lab, 16, 700, L.MUTED, "end", 2.5)
    return s, 52

def b_filler(d, x, y, w):
    n = int(d.get("n", 3)); wid = [0.94, 0.87, 0.9, 0.67]
    return "".join(L.rect(x, y + i * 22, w * wid[i % 4], 9, 4.5, "#EEF0F5") for i in range(n)), n * 22 - 13

def b_redline(d, x, y, w):
    s = T(x, y + 18, fit(d["heading"], 18, 700, w, "redline.heading"), 18, 700, L.INK)
    s += T(x, y + 52, fit(d["before"], 18, 500, w, "redline.before"), 18, 500, L.SUB)
    yy = y + 88; wo = tw(d["old"], 18, 600); wn = tw(d["new"], 18, 700)
    if wo + wn + 40 + tw(d.get("after", ""), 18, 500) > w: raise BriefError(f'{CTX["where"]}redline: old + new + after text is too wide; shorten "after"')
    s += T(x, yy, d["old"], 18, 600, L.BAD) + f'<line x1="{x-1}" y1="{yy-6}" x2="{x+wo+1}" y2="{yy-6}" stroke="{L.BAD}" stroke-width="2"/>'
    x2 = x + wo + 12; s += L.rect(x2 - 8, yy - 23, wn + 16, 32, 8, L.OK_S) + T(x2, yy, d["new"], 18, 700, L.OK)
    if d.get("after"): s += T(x2 + wn + 16, yy, d["after"], 18, 500, L.SUB)
    return s, 96

def b_comment(d, x, y, w):
    s = L.rect(x, y, w, 88, 14, "#FAFAFC", L.HAIR, 1.5) + avatar(x + 32, y + 34, 20, d["initials"], d.get("color", 0))
    s += T(x + 64, y + 28, fit(d["name"], 16, 700, w - 84, "comment.name"), 16, 700, L.INK) + T(x + 64, y + 54, fit(d["text"], 16, 500, w - 84, "comment.text"), 16, 500, L.SUB)
    return s, 88

def b_note(d, x, y, w):
    ic = icon_ok(d.get("icon", "info"))
    s = L.rect(x, y, w, 48, 12, "#fff", "#D6D3E6", 1.5) + L.icon(ic, x + 16, y + 12, 24, L.MUTED, 2) + T(x + 52, y + 30, fit(d["text"], 16, 500, w - 68, "note"), 16, 500, L.MUTED)
    return s, 48

def b_extract(d, x, y, w):
    s = ""
    for i, it in enumerate(d["items"]):
        yy = y + 24 + i * 56; name, val, conf = it
        s += T(x, yy, fit(name, 17, 500, 160, f"extract[{i}].name"), 17, 500, L.MUTED) + T(x + 172, yy, fit(val, 18, 700, w - 172 - 150, f"extract[{i}].value"), 18, 700, L.INK, tnum=True)
        s += L.rect(x + w - 148, yy - 11, 76, 8, 4, L.ACC_M) + L.rect(x + w - 148, yy - 11, 76 * conf / 100, 8, 4, "url(#gAcc)") + T(x + w, yy, f"{conf}%", 16, 600, L.SUB, "end", tnum=True)
    return s, len(d["items"]) * 56 - 20

def b_metric(d, x, y, w):
    s, h = "", 0
    if d.get("label"): s += T(x, y + 18, fit(d["label"], 18, 700, w, "metric.label"), 18, 700, L.INK); h = 28
    size = d.get("size", 40)
    s += T(x, y + h + size, fit(d["value"], size, 800, w, "metric.value", -1), size, 800, L.INK, ls=-1, tnum=True); h += size + 8
    if d.get("sub"): s += T(x, y + h + 20, fit(d["sub"], 16, 500, w, "metric.sub"), 16, 500, L.MUTED); h += 28
    return s, h

def b_bullets(d, x, y, w):
    return "".join(T(x, y + 18 + i * 30, fit("\u2022 " + t, 16, 500, w, f"bullets[{i}]"), 16, 500, L.SUB) for i, t in enumerate(d["items"])), len(d["items"]) * 30 - 6

def b_meta(d, x, y, w):
    ic = icon_ok(d.get("icon", "database")); col = {"ok": L.OK, "acc": AD(), "muted": L.MUTED}[d.get("kind", "ok")]
    return L.icon(ic, x, y, 20, col, 2) + T(x + 28, y + 16, fit(d["text"], 16, 600, w - 28, "meta"), 16, 600, L.SUB), 22

def b_text(d, x, y, w):
    size = int(d.get("size", 18)); wt = int(d.get("weight", 700 if size >= 20 else 500))
    col = {"ink": L.INK, "sub": L.SUB, "muted": L.MUTED, "acc": AD(), "ok": L.OK, "bad": L.BAD}[d.get("color", "ink" if wt >= 600 else "sub")]
    anchor = "middle" if d.get("align") == "center" else "start"; tx = x + w / 2 if anchor == "middle" else x
    ls = -0.3 if size >= 22 else 0
    return T(tx, y + size, fit(d["text"], size, wt, w, "text", ls), size, wt, col, anchor, ls, True), size + 6

def b_title(d, x, y, w):
    size = int(d.get("size", 22))
    s = T(x, y + size, fit(d["title"], size, 700, w, "title.title", -0.3), size, 700, L.INK, ls=-0.3, tnum=True)
    if d.get("sub"): s += T(x, y + size + 28, fit(d["sub"], 17, 500, w, "title.sub"), 17, 500, L.SUB, tnum=True); return s, size + 34
    return s, size + 6

def b_pill(d, x, y, w):
    k = d.get("kind", "ok"); bg, fg = {"ok": (L.OK_S, L.OK), "acc": (AS(), AD()), "warn": (L.WARN_S, L.WARN), "bad": (L.BAD_S, L.BAD)}[k]
    ic = icon_ok(d.get("icon", "check")); pw = tw(d["label"], 17, 700) + 74
    s = L.rect(x, y, pw, 48, 12, bg) + L.icon(ic, x + 18, y + 14, 20, fg, 2.6) + T(x + 46, y + 30, d["label"], 17, 700, fg)
    if d.get("then"):
        s += L.icon("arrow-right", x + pw + 22, y + 14, 20, L.MUTED, 2) + T(x + pw + 50, y + 30, fit(d["then"], 16, 500, w - pw - 50, "pill.then"), 16, 500, L.MUTED)
    return s, 48

def b_callout(d, x, y, w):
    bl = d.get("button"); bw = int(tw(bl, 17, 600) + 72) if bl else 0; avail = w - 56 - (bw + 24 if bl else 0)
    s = L.rect(x, y, w, 132, 16, AS())
    s += T(x + 28, y + 42, fit(d.get("eyebrow", ""), 16, 700, avail, "callout.eyebrow"), 16, 700, AD()) + T(x + 28, y + 78, fit(d["title"], 22, 700, avail, "callout.title"), 22, 700, L.INK)
    if d.get("sub"): s += T(x + 28, y + 108, fit(d["sub"], 16, 500, avail, "callout.sub"), 16, 500, L.SUB)
    if bl:
        part, _ = button(x + w - bw - 28, y + 48, bl, d.get("primary", False), None, bw, 48, d.get("click", False), "callout.button"); s += part
    return s, 132

def b_receipt(d, x, y, w):
    s = L.rect(x, y, w, 226, 14, "#FAFAFC", L.HAIR, 1.5) + L.icon("receipt", x + 18, y + 18, 22, L.MUTED, 2)
    s += T(x + 50, y + 36, fit(d["merchant"], 17, 700, w - 68, "receipt.merchant"), 17, 700, L.INK) + T(x + 18, y + 68, fit(d.get("sub", ""), 16, 500, w - 36, "receipt.sub"), 16, 500, L.MUTED)
    for i, wd in enumerate([0.68, 0.55, 0.73]): s += L.rect(x + 18, y + 90 + i * 20, (w - 36) * wd, 8, 4, "#E9EBF2")
    s += f'<line x1="{x+18}" y1="{y+168}" x2="{x+w-18}" y2="{y+168}" stroke="#D9DCE6" stroke-width="1.5" stroke-dasharray="4 5"/>'
    s += T(x + 18, y + 204, d.get("label", "Total"), 17, 600, L.SUB) + T(x + w - 18, y + 204, d["total"], 22, 800, L.INK, "end", -0.2, True)
    return s, 226

def b_linkbox(d, x, y, w):
    return L.rect(x, y, w, 48, 12, "#F8FAFC", L.LINE, 1.2) + T(x + 16, y + 30, fit(d["text"], 17, 600, w - 32, "linkbox"), 17, 600, AD()), 48

def b_item(d, x, y, w):
    s = L.rect(x, y, w, 84, 14, AS()) + L.rect(x + 14, y + 14, 56, 56, 12, d.get("swatch", L.ACC_M))
    s += T(x + 84, y + 38, fit(d["title"], 17, 700, w - 98, "item.title"), 17, 700, L.INK) + T(x + 84, y + 62, fit(d.get("sub", ""), 16, 500, w - 98, "item.sub"), 16, 500, L.SUB)
    return s, 84

def b_columns(d, x, y, w):
    """Side-by-side sub-columns, each a vertical stack of blocks: {"cols": [{"w": 0.5, "blocks": [...]}, ...], "gap": 40}."""
    gap = d.get("gap", 40); cols = d["cols"]; avail = w - gap * (len(cols) - 1); s = ""; hmax = 0; cx = x
    for ci, c in enumerate(cols):
        cw = avail * c.get("w", 1 / len(cols)); cy = y
        for i, bd in enumerate(c["blocks"]):
            kind = bd.get("type")
            if kind not in BLOCKS or kind == "columns": raise BriefError(f'{CTX["where"]}columns[{ci}][{i}]: bad block type "{kind}"')
            part, bh = BLOCKS[kind](bd, cx, cy, cw); s += part; cy += bh + c.get("gap", 22)
        hmax = max(hmax, cy - y - c.get("gap", 22)); cx += cw + gap
    return s, hmax

def b_space(d, x, y, w): return "", int(d.get("h", 12))

BLOCKS = {k[2:]: v for k, v in globals().items() if k.startswith("b_")}
