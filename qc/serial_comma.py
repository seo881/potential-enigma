"""Serial (Oxford) comma (DECISIONS 2026-10-08): find lists "A, B and C" missing the comma before and/or.
find(text) -> (certain, ambiguous): lists of (start, end, snippet). fix(text) inserts the comma for certain cases only.
Certain: two or more commas before the conjunction in one clause, each item at most 4 words, or one comma with both items at most 2 words;
and the list is flat: no "and"/"or" inside an earlier item, and the clause does not continue with another comma after the conjunction
(that pattern is a nested pair, "date, start and end building, and miles", where a comma would be wrong).
Also certain (Divit 2026-10-10, golden h3-gap-*): three or more items with items up to 8 words (noun phrases with modifiers or
relative clauses, 4-item lists, a first item fused with the verb: "It gathers the company background, goals, key contacts and anything");
and one-comma lists whose 2nd and 3rd items run in parallel: both open with a determiner and the first item has one ("You get the form,
the rules that hide taken times and a table"), or both open with an -s verb after an -s verb in the first item ("It gives the date,
makes the case and takes registrations"). An intro clause ("Before launch, ...") is set aside and the list is read after it.
Ambiguous (QC P2 note, never auto-fixed, never sends a page to a writer): an intro clause with no list after it, longer items or a nested pair.
rules/serial_comma_exceptions.json lists reviewed snippets that look certain but are not lists (an appositive such as "Card photos, front and back")."""
import re, os, json
TAG = re.compile(r"<[^>]+>")
CLAUSE = re.compile(r"[^.;:!?()\[\]\n<>\"]+")
_EXC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rules", "serial_comma_exceptions.json")
EXCEPTIONS = [x["text"] for x in json.load(open(_EXC))["exceptions"]] if os.path.exists(_EXC) else []
DET = {"the", "a", "an", "each", "every", "your", "its", "their", "his", "her", "our", "one", "any", "all", "no", "some", "this", "that", "these", "those"}
INTRO = {"if", "when", "after", "before", "once", "while", "because", "although", "though", "unless", "until", "since", "in", "on", "at", "for",
         "with", "by", "during", "as", "from", "without", "within", "over", "under", "whenever", "where", "so", "then", "otherwise", "instead"}
NOT_VERB = {"is", "was", "has", "does", "this", "its", "his", "hers", "ours", "yours", "theirs", "plus", "less", "unless", "always", "perhaps"}
def _w(p): return re.findall(r"[A-Za-z'$0-9-]+", p)
def _intro(p): return bool(_w(p)) and _w(p)[0].lower() in INTRO
def _sverb(w): return len(w) > 3 and w.islower() and w.endswith("s") and not w.endswith("ss") and w not in NOT_VERB and w not in DET
NUM = r"(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)"
PREP = {"with", "for", "in", "on", "at", "by", "from", "to", "into", "via", "under", "over", "without", "along", "plus", "each", "together", "as", "both", "like"}
EXAMPLE = re.compile(r"(?i)\b(such as|like|including|for example|for instance|e\.g)\b")
def _shape(w):
    w0 = w.lower()
    return "det" if w0 in DET else "sverb" if _sverb(w) else "cap" if w[:1].isupper() else "num" if re.match(NUM + "$", w0) else w0
def _wide(parts, tail):
    """The 2026-10-10 patterns; parts: the comma-split text before the conjunction; tail: the text after it up to the next comma."""
    post = _w(tail); L = parts[1:] if _intro(parts[0]) and len(parts) >= 3 else parts
    lead, mid = L[0], [re.sub(r"(?i)\b" + NUM + r" or " + NUM + r"\b", "NorN", m) for m in L[1:]]
    if not mid or not post or any(not 1 <= len(_w(m)) <= 8 for m in mid) or _intro(lead): return False
    if re.match(NUM + "$", (_w(mid[-1]) or [""])[-1].lower()) and re.match(NUM + "$", post[0].lower()): return False   # "one or two"
    if _w(mid[-1])[0].lower() in PREP or any(EXAMPLE.search(x) for x in L): return False                          # a modifier or an example, not a list
    shapes = [_shape(_w(m)[0]) for m in mid]; parallel = _shape(post[0]) in shapes
    if re.search(r"\b(and|or)\b", mid[-1]) and not all(x == _shape(post[0]) for x in shapes): return False    # a pair inside the last item
    lw = _w(lead)
    if lw and len(lw) <= 3 and all(x[:1].isupper() for x in lw) and _w(mid[0])[0].lower() in DET: return False      # "Owen Tate, the lead therapist, gets"
    if len(mid) >= 2:
        return parallel or not re.search(r"\b(and|or)\b", tail) and not re.search(r"\b(and|or)\b", mid[-1])
    w1, w2, lw = _w(mid[0])[0], post[0], [x.lower() for x in lw]
    if w1.lower() in DET and w2.lower() in DET and any(x in DET for x in lw[1:]): return True
    return _sverb(w1) and _sverb(w2) and any(_sverb(x) for x in lw[:3])
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
            if certain and (not flat or intro): certain = False
            if not certain and "," not in seg[c.end():] and not intro: certain = _wide(parts, seg[c.end():])
            if certain and any(e in seg_text for e in EXCEPTIONS): certain = False
            pos = m.start() + c.start()
            out.append((pos, certain, text[max(0, pos - 40):pos + 20].replace("\n", " ")))
    return out
BLOCK = re.compile(r"</?(?:td|th|tr|p|h[1-6]|li|ul|ol|div|br|table|thead|tbody)\b[^>]*>", re.I)
def find(text):
    plain = BLOCK.sub(lambda t: "\n" + " " * (len(t.group(0)) - 1), text)          # a table cell or paragraph ends a clause
    plain = TAG.sub(lambda t: " " * len(t.group(0)), plain)
    plain = re.sub(r"(?<=\d),(?=\d{3})", "\x01", plain)                          # 3,000 is a number, not a list
    cs = _cases(plain)
    return [(p, s) for p, c, s in cs if c], [(p, s) for p, c, s in cs if not c]
def fix(text):
    certain, _ = find(text)
    for p, _s in sorted(certain, reverse=True): text = text[:p] + "," + text[p:]
    return text
