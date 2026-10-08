"""Serial (Oxford) comma (DECISIONS 2026-10-08): find lists "A, B and C" missing the comma before and/or.
find(text) -> (certain, ambiguous): lists of (start, end, snippet). fix(text) inserts the comma for certain cases only.
Certain: two or more commas before the conjunction in one clause, each item at most 4 words, or one comma with both items at most 2 words;
and the list is flat: no "and"/"or" inside an earlier item, and the clause does not continue with another comma after the conjunction
(that pattern is a nested pair, "date, start and end building, and miles", where a comma would be wrong).
Ambiguous (QC P2 note, never auto-fixed, never sends a page to a writer): an intro clause, longer items or a nested pair.
rules/serial_comma_exceptions.json lists reviewed snippets that look certain but are not lists (an appositive such as "Card photos, front and back")."""
import re, os, json
TAG = re.compile(r"<[^>]+>")
CLAUSE = re.compile(r"[^.;:!?()\[\]\n<>\"]+")
_EXC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rules", "serial_comma_exceptions.json")
EXCEPTIONS = [x["text"] for x in json.load(open(_EXC))["exceptions"]] if os.path.exists(_EXC) else []
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
            flat = not any(re.search(r"\b(and|or)\b", p) for p in parts[1:]) and "," not in seg[c.end():]
            seg_text = re.sub(r"\s+", " ", seg).strip()
            intro = re.search(r"\b(for example|for instance|for one|such as|including),", seg, re.I)
            if certain and (not flat or intro or any(e in seg_text for e in EXCEPTIONS)): certain = False
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
