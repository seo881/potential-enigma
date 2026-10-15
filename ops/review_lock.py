"""review_lock.py: ruling 10 B2 (Divit 2026-10-13). After a page's review, only the fields named in a blocking finding may change
(mechanical H3/J1 autofixes are ignored by the review hash already). Checked at `hubctl ready` and in ops/sync.sh before commit.

    python3 ops/review_lock.py specs/<hub>/<slug>.json ...    exit 1 and list violations when a locked field changed

A same-day factual fix outside those fields needs a coordinator exception (`hubctl unlock URL FIELD --by A-coord --reason ...`),
recorded on the spec; the page then needs a slim review of that field before it ships (ruling 1).
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ops"))
import guards as G

def _matches(changed, named):
    """A finding's field may be a CMS field key, an image path such as image_brief.tabs[3].alt, or 'faq'."""
    n = (named or "").strip()
    if not n: return False
    if changed == n or changed.startswith(n) or n.startswith(changed): return True
    if (n.startswith("image") or n.startswith("alt")) and changed.startswith("alt:"): return True
    return False

def allowed_fields(spec):
    """Fields named in blocking findings of the latest review or slim review, plus coordinator exceptions."""
    events = [spec.get("review") or {}] + list(spec.get("slim_reviews") or [])
    last = max(events, key=lambda e: e.get("date") or "")   # only the latest review event's blocking findings unlock fields
    named = [f.get("field") for f in last.get("findings", []) if f.get("severity") == "blocking"]
    named += [x.get("field") for x in spec.get("lock_exceptions") or [] if (x.get("date") or "") >= (last.get("date") or "")]
    return [x for n in named if n for x in _split(n)]

def _split(named):
    """A finding may name several fields: "h1; usecase_heading; og (share image headline)" (B-r-16, 2026-10-15). Split on ; and ,
    drop parentheticals, and map the names reviewers use to the fields they live in (tab_heading_N -> tab_content_N, og -> alt:share_image)."""
    import re
    out = []
    for part in re.split(r"[;,]", re.sub(r"\([^)]*\)", "", named)):
        p = part.strip()
        if not p: continue
        out.append(p.split()[0] if p.split()[0] in ("faq", "mockup") else p)
        m = re.match(r"tab_heading_(\d)", p)
        if m: out.append(f"tab_content_{m.group(1)}")
        if p == "og" or p.startswith("og "): out += ["alt:share_image", "image_brief.og"]
    return out

def violations(spec):
    """Changed fields (since the stored review hash) that no blocking finding or exception names. [] when unlocked."""
    base = spec.get("lock_hash") or spec.get("review_hash")   # lock_hash: written at every review event, pass or block
    if not base: return []          # reviewed before hashes existed: ruling 1's slim review covers it
    ch = G.review_changed(dict(spec, review_hash=base)) or []
    named = allowed_fields(spec)
    return [c for c in ch if not any(_matches(c, n) for n in named)]

def main(paths):
    bad = 0
    for p in paths:
        if not (p.startswith("specs/") and p.endswith(".json")) or not os.path.exists(os.path.join(ROOT, p)): continue
        try: s = json.load(open(os.path.join(ROOT, p)))
        except ValueError: continue
        v = violations(s)
        if v: bad += 1; print(f"review lock: {p} changed {', '.join(v)} after review; only fields named in a blocking finding may change (ruling 10 B2). Coordinator exception: hubctl unlock")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
