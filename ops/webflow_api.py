"""webflow_api.py: the direct Webflow Data API v2 client for CMS item writes (Divit, 2026-10-14). Used only by ops/ship.py (hubctl api-*).

Allowed requests, and nothing else (check() refuses before any network call, token read or retry):
  GET   /collections/{cid}/items             list (query offset and limit only, limit 1-100)
  GET   /collections/{cid}/items/{item_id}   one item
  POST  /collections/{cid}/items             create: 1-100 items, every item isDraft true with a name and a slug
  PATCH /collections/{cid}/items             update: 1-100 items, each with an id; never a slug (one TEMPORARY exception: the
                                             approved slug migration, migration_slug_block), isArchived or isDraft false
  POST  /collections/{cid}/items/publish     item publish by IDs: 1-100 itemIds
{cid} must be one of the 4 child collection IDs in config/collections.json. One exception, read only (Divit 2026-10-16): the Learn
collection (config learn_collection) allows GET list, so the published status of acrm---learn references can be checked; every
other request on it (one item, create, update, publish, anything else) is refused. Site publish, delete, unpublish, live-item
endpoints, collection schema, pages, components, assets, webhooks and every other path are refused in code.

Token: the macOS keychain, service "webflow", read at call time (`security find-generic-password -s webflow -w`). It is never
printed, logged, written, cached on disk or put in an exception message; Authorization is redacted in debug output
(WEBFLOW_API_DEBUG=1). Redirects are refused (a redirect would carry the Authorization header to another host).
Every function takes dry=True by default: the planned request is returned and nothing is sent.
Headless (EMG_HEADLESS): writes are refused, except tonight (DECISIONS 2026-10-15 night) while .cache/overnight-b/ruling19-lift-2026-10-15
exists (under 18 hours old) and no ship-stop file exists, for item create, update and publish sent by hubctl api-create | api-update |
api-publish only (headless_block).
"""
import json, os, re, subprocess, time, urllib.request, urllib.error, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))
BASE = "https://api.webflow.com/v2"
CHILD = {h["collection_id"]: hub for hub, h in CFG["hubs"].items()}   # the only collections this client may write
LEARN = CFG["learn_collection"]["collection_id"]                         # Learn: GET list only, never a write (Divit 2026-10-16)
READ_ONLY_LIST = {LEARN: "Learn"}
MAX_ITEMS = 100
ID = r"[0-9a-f]{24}"
RULES = [   # (method, path pattern, operation)
    ("GET",   re.compile(rf"^/collections/(?P<cid>{ID})/items$"), "list"),
    ("GET",   re.compile(rf"^/collections/(?P<cid>{ID})/items/(?P<iid>{ID})$"), "get"),
    ("POST",  re.compile(rf"^/collections/(?P<cid>{ID})/items$"), "create"),
    ("PATCH", re.compile(rf"^/collections/(?P<cid>{ID})/items$"), "update"),
    ("POST",  re.compile(rf"^/collections/(?P<cid>{ID})/items/publish$"), "publish"),
]

class Refused(Exception):
    """A request outside the allowlist (raised before any network call)."""
class ApiError(Exception):
    def __init__(self, status, msg): super().__init__(msg); self.status = status

def _refuse(msg): raise Refused("refused: " + msg)

def check(method, path, body=None, query=None):
    """The one gate: (method, path, body, query) against the allowlist. Returns (operation, collection_id) or raises Refused."""
    m = (method or "").upper()
    if not isinstance(path, str) or not re.fullmatch(r"/[a-z0-9/]+", path) or "//" in path:
        _refuse(f"{m} {path!r}: malformed path (lowercase letters, digits and / only; no query, dots or encoding)")
    if re.search(r"(^|/)sites(/|$)", path) or (path.endswith("/publish") and not path.endswith("/items/publish")):
        _refuse(f"{m} {path}: site publish and site endpoints are never allowed (no site publish, ever: Divit 2026-10-10)")
    hit = next(((op, rx.match(path)) for meth, rx, op in RULES if meth == m and rx.match(path)), None)
    if not hit: _refuse(f"{m} {path}: not on the allowlist (item read, create, update and item publish on the 4 child collections only)")
    op, mt = hit; cid = mt.group("cid")
    if cid in READ_ONLY_LIST and op != "list":
        _refuse(f"{m} {path}: the {READ_ONLY_LIST[cid]} collection is read only (GET list); {op} is never allowed on it (Divit 2026-10-16)")
    if cid not in CHILD and cid not in READ_ONLY_LIST: _refuse(f"{m} {path}: collection {cid} is not one of the 4 child collections in config/collections.json")
    q = dict(query or {})
    if op == "list":
        if set(q) - {"offset", "limit"}: _refuse(f"list query may carry offset and limit only, got {sorted(q)}")
        if not (isinstance(q.get("limit", 100), int) and 1 <= q.get("limit", 100) <= MAX_ITEMS): _refuse("list limit must be 1-100")
        if not (isinstance(q.get("offset", 0), int) and q.get("offset", 0) >= 0): _refuse("list offset must be a non-negative integer")
    elif q: _refuse(f"{op} takes no query parameters")
    if op in ("list", "get"):
        if body is not None: _refuse(f"{op} takes no body")
        return op, cid
    if not isinstance(body, dict): _refuse(f"{op} needs a JSON object body")
    if op == "publish":
        ids = body.get("itemIds")
        if set(body) != {"itemIds"} or not isinstance(ids, list) or not 1 <= len(ids) <= MAX_ITEMS: _refuse("publish body is {itemIds: [1-100 ids]} only")
        if len(set(ids)) != len(ids) or not all(isinstance(i, str) and re.fullmatch(ID, i) for i in ids): _refuse("publish itemIds must be unique 24-hex item IDs")
        return op, cid
    items = body.get("items")
    if set(body) != {"items"} or not isinstance(items, list) or not 1 <= len(items) <= MAX_ITEMS:
        _refuse(f"{op} body is {{items: [1-{MAX_ITEMS} items]}} only (got {len(items) if isinstance(items, list) else 'no list'})")
    for it in items:
        if not isinstance(it, dict) or not isinstance(it.get("fieldData"), dict): _refuse(f"{op}: every item needs a fieldData object")
        if op == "create":
            if set(it) - {"isDraft", "fieldData"}: _refuse(f"create items carry isDraft and fieldData only, got {sorted(it)}")
            if it.get("isDraft") is not True: _refuse("create: every item must be isDraft true (drafts only, CLAUDE.md)")
            if not (it["fieldData"].get("name") and it["fieldData"].get("slug")): _refuse("create: every item needs a name and a slug")
        else:
            if set(it) - {"id", "isDraft", "fieldData"}: _refuse(f"update items carry id, isDraft and fieldData only, got {sorted(it)}")
            if not (isinstance(it.get("id"), str) and re.fullmatch(ID, it["id"])): _refuse("update: every item needs a 24-hex id")
            if "isDraft" in it and it["isDraft"] is not True: _refuse("update: isDraft may only be true (status kept otherwise)")
            if "slug" in it["fieldData"]:
                why = migration_slug_block(cid, it["id"], it["fieldData"]["slug"])
                if why: _refuse("update: a slug never changes through the API" + (f" ({why})" if why != "-" else ""))
    if op == "create" and len({it["fieldData"]["slug"] for it in items}) != len(items): _refuse("create: duplicate slugs in one request")
    if op == "update" and len({it["id"] for it in items}) != len(items): _refuse("update: duplicate item ids in one request")
    return op, cid

# ---------- SLUG MIGRATION EXCEPTION (Divit 2026-10-23, DECISIONS "staged-write go ... Slug-guard exception approved").
# TEMPORARY: REMOVE this function and its call in check() when the slug migration is closed (status/freeze.json inactive for good).
# A slug in an update passes ONLY when (1) status/freeze.json is active with the slug-migration reason, (2) the process carries
# --migration, and (3) plan/slug-migration.json maps this exact item id, in this collection's hub, to exactly this new slug
# (decision "change"). Every other slug change stays refused. Golden: tests/golden cases api-migration-slug-*.
FREEZE_FILE = os.path.join(ROOT, "status", "freeze.json")
MIGRATION_MAP = os.path.join(ROOT, "plan", "slug-migration.json")
def migration_slug_block(cid, item_id, slug, argv=None, freeze=None, mapping=None):
    """None when this slug change is the approved migration change, else why it is refused ("-": no migration context at all)."""
    import sys as _s
    a = argv if argv is not None else (ARGV if ARGV is not None else _s.argv)
    if "--migration" not in a: return "-"
    try: f = freeze if freeze is not None else json.load(open(FREEZE_FILE))
    except (OSError, ValueError): return "migration: no status/freeze.json"
    if not f.get("active") or "slug migration" not in (f.get("reason") or "").lower(): return "migration: the slug-migration freeze is not active"
    try: m = mapping if mapping is not None else json.load(open(MIGRATION_MAP))
    except (OSError, ValueError): return "migration: no plan/slug-migration.json"
    hub = CHILD.get(cid)
    row = next((e for e in m.get("pages", []) if e.get("item_id") == item_id), None)
    if not row: return f"migration: item {item_id} is not in plan/slug-migration.json"
    if row.get("hub") != hub: return f"migration: item {item_id} belongs to {row.get('hub')}, not {hub}"
    if row.get("decision") != "change" or row.get("new_slug") == row.get("old_slug"): return f"migration: item {item_id} has no approved slug change"
    if slug != row.get("new_slug"): return f"migration: '{slug}' is not the approved slug '{row.get('new_slug')}' for {item_id}"
    return None

# ---------- token and transport (both replaceable by the golden tests; nothing here ever returns the token to a caller's output)
def _token():
    r = subprocess.run(["security", "find-generic-password", "-s", "webflow", "-w"], capture_output=True, text=True)
    tok = r.stdout.strip()
    if r.returncode or not tok: raise Refused("refused: no Webflow API token in the macOS keychain (service webflow); add it in Keychain Access, never in the repo")
    return tok
TOKEN = _token

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None   # urllib then raises HTTPError with the 3xx code
_OPENER = urllib.request.build_opener(_NoRedirect)

def _urllib(method, url, headers, data, timeout):
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with _OPENER.open(req, timeout=timeout) as r: return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e: return e.code, dict(e.headers or {}), e.read() or b""
TRANSPORT = _urllib
SLEEP = time.sleep

def redact(text, tok=None):
    t = str(text)
    if tok: t = t.replace(tok, "[redacted]")
    return re.sub(r"(?i)(bearer\s+)[^\s\"',}]+", r"\1[redacted]", t)

# Ruling 19 lift for the 2026-10-15 overnight loop only (DECISIONS 2026-10-15 night): with EMG_HEADLESS set, a CMS write passes
# only while the lift file exists (and is under 18 hours old), the operation is an item create, update or publish, the process is
# hubctl api-create | api-update | api-publish, and no verify-live failure has stopped shipping. Everything else stays refused.
LIFT_FILE = os.path.join(ROOT, ".cache", "overnight-b", "ruling19-lift-2026-10-15")
SHIP_STOP = os.path.join(ROOT, ".cache", "overnight-b", "ship-stop")
LIFT_CMDS = {"api-create": {"create"}, "api-update": {"update", "publish"}, "api-publish": {"publish", "update"}}   # api-publish: its automatic relink updates and item-publishes
ARGV = None   # replaceable by the golden tests (None = sys.argv)
def headless_block(op, argv=None):
    """None when this headless write may go, else the refusal text."""
    import sys as _s
    a = argv if argv is not None else (ARGV if ARGV is not None else _s.argv)
    base = "CMS writes are not allowed in a headless run (EMG_HEADLESS is set)"
    try: fresh = (time.time() - os.path.getmtime(LIFT_FILE)) < 18 * 3600
    except OSError: return base + "; ruling 19 is not lifted (no lift file)"
    if not fresh: return base + "; the ruling-19 lift file is older than 18 hours (ignored)"
    if os.path.exists(SHIP_STOP): return base + "; shipping is stopped for the night (verify-live failure: .cache/overnight-b/ship-stop)"
    via = os.path.basename(a[0]) if a else ""
    cmd = a[1] if len(a) > 1 else ""
    if via != "hubctl.py" or cmd not in LIFT_CMDS: return base + f"; under the lift only hubctl api-create | api-update | api-publish may write (this is {via} {cmd})"
    if op not in LIFT_CMDS[cmd]: return base + f"; {cmd} may not send a {op}"
    return None

def _debug(*parts):
    if os.environ.get("WEBFLOW_API_DEBUG"): print("[webflow-api]", *parts, file=__import__("sys").stderr)

def request(method, path, body=None, query=None, dry=True, timeout=None, max_tries=6):
    """Send one allowed request. dry=True (the default) returns the plan and sends nothing.
    429: honour Retry-After (else 2, 4, 8 ... s, cap 60). 5xx and network errors retry on GET only; a write whose outcome is
    unknown raises, and the caller re-reads the collection (creates are idempotent by slug)."""
    op, cid = check(method, path, body, query)
    n = len(body.get("items") or body.get("itemIds") or []) if isinstance(body, dict) else 0
    plan = {"dry": dry, "op": op, "method": method.upper(), "path": path, "query": query or {}, "count": n}
    if dry: return plan
    if method.upper() != "GET" and os.environ.get("EMG_HEADLESS"):   # ruling 19: CMS writes never run headless (Divit 2026-10-14)
        why = headless_block(op)
        if why: _refuse(why)
    tok = TOKEN(); url = BASE + path + ("?" + urllib.parse.urlencode(query) if query else "")
    headers = {"Authorization": "Bearer " + tok, "Accept": "application/json", "User-Agent": "emergent-hubs-ship/1"}
    data = None
    if body is not None: data = json.dumps(body, ensure_ascii=False).encode(); headers["Content-Type"] = "application/json"
    shown = {k: ("Bearer [redacted]" if k.lower() == "authorization" else v) for k, v in headers.items()}
    for attempt in range(max_tries):
        _debug(method.upper(), url, json.dumps(shown), f"attempt {attempt + 1}")
        try: status, hdrs, raw = TRANSPORT(method.upper(), url, headers, data, timeout or (60 if method.upper() == "GET" else 180))
        except Exception as e:
            if method.upper() == "GET" and attempt + 1 < max_tries: SLEEP(min(60, 2 ** (attempt + 1))); continue
            raise ApiError(0, f"{method.upper()} {path}: network error ({type(e).__name__}); "
                              + ("outcome unknown: read the collection back before any retry" if method.upper() != "GET" else "gave up")) from None
        hl = {k.lower(): v for k, v in (hdrs or {}).items()}
        _debug("->", status, "rate-limit remaining", hl.get("x-ratelimit-remaining", "?"))
        if status == 429 and attempt + 1 < max_tries:
            ra = hl.get("retry-after"); wait = int(ra) if ra and str(ra).isdigit() else 2 ** (attempt + 1)
            SLEEP(min(60, max(1, wait))); continue
        if status >= 500 and method.upper() == "GET" and attempt + 1 < max_tries: SLEEP(min(60, 2 ** (attempt + 1))); continue
        if status >= 300:
            txt = raw.decode("utf-8", "replace")[:300] if isinstance(raw, (bytes, bytearray)) else str(raw)[:300]
            raise ApiError(status, f"{method.upper()} {path} -> HTTP {status}: {redact(txt, tok)}") from None
        try: return json.loads(raw or b"{}")
        except ValueError: raise ApiError(status, f"{method.upper()} {path}: response is not JSON") from None
    raise ApiError(429, f"{method.upper()} {path}: still rate limited after {max_tries} tries")

def chunks(seq, n=MAX_ITEMS):
    seq = list(seq); return [seq[i:i + n] for i in range(0, len(seq), n)]

# ---------- the five operations
def list_items(cid, dry=False):
    """Every item of a child collection (staged: drafts included), paginated 100 at a time. dry=True returns [] and the first planned read."""
    out, off = [], 0
    while True:
        r = request("GET", f"/collections/{cid}/items", query={"offset": off, "limit": MAX_ITEMS}, dry=dry)
        if dry: return [], [r]
        got = r.get("items") or []; out += got
        total = (r.get("pagination") or {}).get("total")
        off += len(got)
        if not got or (total is not None and off >= total) or (total is None and len(got) < MAX_ITEMS): return out, []
def list_learn(dry=False):
    """Every item of the Learn collection (read only: GET list, staged, drafts included) for the acrm---learn published check."""
    return list_items(LEARN, dry=dry)
def get_item(cid, iid, dry=False): return request("GET", f"/collections/{cid}/items/{iid}", dry=dry)
def create_items(cid, items, dry=True, on_batch=None):
    """POST in batches of up to 100; on_batch(chunk, response) runs after each batch so the caller logs and writes rollback at once."""
    res = []
    for ch in chunks(items):
        r = request("POST", f"/collections/{cid}/items", {"items": ch}, dry=dry); res.append(r)
        if on_batch: on_batch(ch, r)
    return res
def update_items(cid, items, dry=True, on_batch=None):
    res = []
    for ch in chunks(items):
        r = request("PATCH", f"/collections/{cid}/items", {"items": ch}, dry=dry); res.append(r)
        if on_batch: on_batch(ch, r)
    return res
def publish_items(cid, ids, dry=True, on_batch=None):
    res = []
    for ch in chunks(ids):
        r = request("POST", f"/collections/{cid}/items/publish", {"itemIds": ch}, dry=dry); res.append(r)
        if on_batch: on_batch(ch, r)
    return res
def created_of(resp):
    """Items in a create response: {items: [...]} for a list body, or a single item."""
    if not isinstance(resp, dict): return []
    return resp.get("items") or ([resp] if resp.get("id") else [])
