"""spelling.py: one spelling-variant list for every check (Divit ruling 14, 2026-10-13).

rules/us_spelling.json `map` (UK -> US) is the single variant list:
  - H2 (qc_hub) blocks the UK form in visible copy;
  - PA3 (paa_gate.norm) and the K keyword checks (qc_hub.kwmap) read the UK form as its US form, so "acknowledgement" matches the
    head phrase "employee handbook acknowledgment form" and counts as the keyword;
  - display(): the display text of a verbatim AlsoAsked question is normalised to US spelling (and to the house form of a keyword
    variant, rules/keyword_variants.json, e.g. "T-shirt"), the original staying in prov.original. Spelling normalisation is not a
    reword: ruling 4 still forbids any other change (`hubctl verbatim` accepts exactly the original or display(original)).
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = json.load(open(os.path.join(ROOT, "rules", "us_spelling.json")))["map"]
KV = json.load(open(os.path.join(ROOT, "rules", "keyword_variants.json")))["groups"]
_RX = re.compile(r"(?<![A-Za-z])(" + "|".join(sorted((re.escape(k) for k in MAP), key=len, reverse=True)) + r")(s?)(?![A-Za-z])", re.I)

def _case(src, dst):
    if src.isupper(): return dst.upper()
    if src[:1].isupper(): return dst[:1].upper() + dst[1:]
    return dst

def to_us(s):
    """UK -> US spelling, word by word (plural -s kept), case preserved. Used lower-cased for matching and as-is for display."""
    return _RX.sub(lambda m: _case(m.group(1), MAP[m.group(1).lower()]) + m.group(2), s or "")

def display(q):
    """The display text of a verbatim AlsoAsked question: US spelling and keyword house forms only, nothing else."""
    out = to_us(q)
    for g in KV:
        if not g.get("house"): continue
        rx = re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(re.escape(v).replace(r"\ ", r"[\s-]?").replace(r"\-", r"[\s-]?") for v in g["variants"]) + r")(?![A-Za-z0-9])", re.I)
        out = rx.sub(g["house"], out)
    return out

def verbatim_ok(q, original):
    """Ruling 4 + 14: the FAQ question is the AlsoAsked original, or the original with only spelling/house-form normalisation."""
    return bool(original) and q in (original, display(original))
