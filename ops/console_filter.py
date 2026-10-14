"""console_filter.py: Divit's narrow console-error exception (2026-10-14), shared by ops/staging_check.py and ops/live_audit.py.

An error (a dict from ops/console_capture.mjs: {t, src, stack}) is ignored only when its SOURCE matches an entry of
rules/live_audit.json console_ignore_sources: `src` (regex) on the error's source (the reporting script URL or the top stack
frame) and, where given, `stack_any` (regex) on at least one stack frame. The message text is never used. A plain string (an
older capture without a source) is never ignored. Every run lists what was ignored (summary_line, ignored_lines).
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTE = "Divit's 2026-10-14 exception"

def load_sources():
    return json.load(open(os.path.join(ROOT, "rules", "live_audit.json"))).get("console_ignore_sources", [])

def ignored_by(err, sources=None):
    """The name of the exception entry that covers this error, or None."""
    if not isinstance(err, dict): return None
    src, stack = err.get("src") or "", [f for f in err.get("stack") or [] if f]
    for s in load_sources() if sources is None else sources:
        if src and re.search(s["src"], src) and (not s.get("stack_any") or any(re.search(s["stack_any"], f) for f in stack)):
            return s["name"]
    return None

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

def exception_tail(ignored):
    """ (3 ignored by Divit's 2026-10-14 exception: adwire x1, clarity.js x2)"""
    by = {}
    for name, _e in ignored: by[name] = by.get(name, 0) + 1
    return f" ({len(ignored)} ignored by {NOTE}: " + ", ".join(f"{k} ×{v}" for k, v in sorted(by.items())) + ")" if ignored else f" (0 ignored by {NOTE})"

def summary_line(n_counted, ignored):
    """e.g. console: 0 errors (3 ignored by Divit's 2026-10-14 exception: adwire x1, clarity.js x2)"""
    return f"console: {n_counted} error{'s' if n_counted != 1 else ''}" + exception_tail(ignored)

def ignored_lines(rows):
    """rows: [(page, name, err)] -> report lines (page, message, source)."""
    return [f"- {page}: {name}: `{text(e)[:140]}` (source {e.get('src', '')[:120]})" for page, name, e in rows]
