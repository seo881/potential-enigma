"""console_filter.py: Divit's narrow console-error exception (2026-10-14, widened 2026-10-15), shared by ops/staging_check.py
and ops/live_audit.py.

An error (a dict from ops/console_capture.mjs: {t, src, stack, kind, doc?, element?}) is ignored only when it matches an entry of
rules/live_audit.json console_ignore_sources, in one of two forms:
- source entry: `src` (regex) on the error's source (the reporting script URL or the top stack frame) and, where given,
  `stack_any` (regex) on at least one stack frame, and `kind` where given (clarity.js, the GTM and Bing UET Clarity loaders,
  Clarity's c.clarity.ms/c.gif collect beacon as a failed request, kind `log`, Adwire molecule.js);
- element entry (2026-10-15, the navbar <svg width="2o"> on the /ai-contests dropdown icon): the error was reported by the page
  document itself (`doc` true, kind `log`, never a script) and ops/console_capture.mjs tied it to the offending element, whose
  tag, attribute, value, navbar membership and link href all match `element`.
The message text is never used for the decision. A plain string (an older capture without a source) is never ignored. Every run
lists what was ignored (summary_line, ignored_lines).
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTE = "Divit's console exception (2026-10-14/15)"

def load_sources():
    return json.load(open(os.path.join(ROOT, "rules", "live_audit.json"))).get("console_ignore_sources", [])

def ignored_by(err, sources=None):
    """The name of the exception entry that covers this error, or None."""
    if not isinstance(err, dict): return None
    src, stack = err.get("src") or "", [f for f in err.get("stack") or [] if f]
    for s in load_sources() if sources is None else sources:
        if "element" in s:
            if element_match(err, s): return s["name"]
        elif src and re.search(s["src"], src) and (not s.get("kind") or err.get("kind") == s["kind"]) \
                and (not s.get("stack_any") or any(re.search(s["stack_any"], f) for f in stack)):
            return s["name"]
    return None

def element_match(err, s):
    """An element entry covers the error only when the document itself reported it (not a script: kind `log`, `doc` true,
    no script frame in the stack) and the element the capture tied it to matches every field of s["element"]."""
    el, want = err.get("element"), s["element"]
    if not isinstance(el, dict) or err.get("kind") != s.get("kind", "log") or err.get("doc") is not True: return False
    if any(re.search(r"\.m?js([?#]|$)", f or "") for f in [err.get("src") or ""] + list(err.get("stack") or [])): return False
    for k, rx in want.items():
        v = el.get(k)
        if isinstance(rx, bool):
            if v is not rx: return False
        elif v is None or not re.search(rx, str(v)): return False
    return True

def split(errs, sources=None):
    """(counted, ignored [(name, err)]) for a list of captured errors."""
    sources = load_sources() if sources is None else sources
    counted, ignored = [], []
    for e in errs or []:
        n = ignored_by(e, sources)
        if n: ignored.append((n, e))
        else: counted.append(e)
    return counted, ignored

def text(e): return e.get("t", "") if isinstance(e, dict) else str(e)

def in_force(sources=None):
    """The named exceptions in force, printed on every run: clarity.js, ..., navbar-ai-contests-svg-width (element)"""
    names = []
    for s in load_sources() if sources is None else sources:
        n = s["name"] + (" (element)" if "element" in s else "")
        if n not in names: names.append(n)
    return ", ".join(names)

def exception_tail(ignored, sources=None):
    """ (3 ignored by Divit's console exception (2026-10-14/15): adwire x1, clarity.js x2; in force: ...)"""
    by = {}
    for name, _e in ignored: by[name] = by.get(name, 0) + 1
    force = f"; in force: {in_force(sources)}"
    return (f" ({len(ignored)} ignored by {NOTE}: " + ", ".join(f"{k} ×{v}" for k, v in sorted(by.items())) + force + ")") if ignored else f" (0 ignored by {NOTE}{force})"

def summary_line(n_counted, ignored):
    """e.g. console: 0 errors (3 ignored by Divit's 2026-10-14 exception: adwire x1, clarity.js x2)"""
    return f"console: {n_counted} error{'s' if n_counted != 1 else ''}" + exception_tail(ignored)

def ignored_lines(rows):
    """rows: [(page, name, err)] -> report lines (page, message, source)."""
    return [f"- {page}: {name}: `{text(e)[:140]}` (source {e.get('src', '')[:120]}{elem(e)})" for page, name, e in rows]

def elem(e):
    el = e.get("element") if isinstance(e, dict) else None
    return f"; element <{el.get('tag')} {el.get('attr')}=\"{el.get('value')}\"> in {'navbar' if el.get('nav') else 'body'}, link {el.get('href')}" if isinstance(el, dict) else ""
