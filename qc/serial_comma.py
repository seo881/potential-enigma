"""Serial (Oxford) comma (DECISIONS 2026-10-08): find lists "A, B and C" missing the comma before and/or.
find(text) -> (certain, ambiguous): lists of (start, end, snippet). fix(text) inserts the comma for certain cases only.
Certain: two or more commas before the conjunction in one clause, each item at most 4 words, or one comma with both items at most 2 words.
Ambiguous (reported, never auto-fixed): an intro clause or longer items, where the comma may not mark a list."""
import re
TAG = re.compile(r"<[^>]+>")
CLAUSE = re.compile(r"[^.;:!?()\[\]\n<>\"]+")
def _cases(text):
    out = []
    for m in CLAUSE.finditer(text):
        seg = m.group(0)
        for c in re.finditer(r"(?<!,) (and|or) ", seg):
            before = seg[:c.start()]
            if "," not in before: continue
            parts = [p.strip() for p in before.split(",")]
            items = [p for p in parts[1:]] if len(parts) > 1 else []
            last = parts[-1]
            if not last or not items: continue
            nwords = [len(p.split()) for p in parts[1:]] + [len(seg[c.end():].split(",")[0].split()[:5])]
            commas = before.count(",")
            first_ok = len(parts[0].split()) <= 4
            certain = (commas >= 2 and first_ok and all(1 <= n <= 4 for n in nwords[:-1])) or (commas == 1 and len(parts[0].split()) <= 2 and len(last.split()) <= 2)
            pos = m.start() + c.start()
            out.append((pos, certain, text[max(0, pos - 40):pos + 20].replace("\n", " ")))
    return out
def find(text):
    plain = TAG.sub(lambda t: " " * len(t.group(0)), text)
    cs = _cases(plain)
    return [(p, s) for p, c, s in cs if c], [(p, s) for p, c, s in cs if not c]
def fix(text):
    certain, _ = find(text)
    for p, _s in sorted(certain, reverse=True): text = text[:p] + "," + text[p:]
    return text
