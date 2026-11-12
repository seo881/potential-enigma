"""render_changed.py: render images for changed pages only (the GitHub Action .github/workflows/render.yml runs it; any machine can).

    python3 ops/render_changed.py <before-sha> <after-sha> [--pages PAGE,PAGE] [--no-commit] [--force]

--pages takes, comma-separated, any of (2026-11-11; a slug can exist in two hubs, e.g. fitness in LP and SurveyQuiz):
  /ai-survey-and-quiz-builder/fitness   the page URL path (a full https://... URL works too)
  SurveyQuiz:fitness                    HUB:slug, HUB = a hub key in config/collections.json (LP, Form, Auto, SurveyQuiz; any case)
  fitness                               a bare slug, ONLY when exactly one hub has it; an ambiguous bare slug is refused with the
                                        candidates named, and nothing is rendered
Any --pages entry that does not resolve refuses the whole run (exit 2). Queue entries resolve the same way; an unresolvable one
is reported and stays in the queue.

Render set = specs whose image_brief changed between the two commits, plus pages queued in status/render-queue.txt
(written by `hubctl ship` for pages whose images are not current), plus --pages; with --pages ONLY those pages are rendered (no range, no queue; 2026-11-06). A page is skipped when its
images/<dir>/<slug>/render.json already records the current brief hash. Each page goes through engine.render_spec,
which runs every image gate; a blocked brief is reported and left unrendered (exit 1 at the end).
After a render, render.json records the brief hash, the commit and the runner, so `hubctl ship` and `hubctl readiness`
can tell whether a page's images are current. Prints one line per page.
"""
import hashlib, json, os, subprocess, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
QUEUE = os.path.join(ROOT, "status", "render-queue.txt")

CFG = json.load(open(os.path.join(ROOT, "config", "collections.json")))

def resolve_page(token):
    """(url, spec_path) for a --pages / queue entry, or ValueError naming why not (unknown hub, no spec, ambiguous bare slug)."""
    t = token.strip()
    if t.startswith(("http://", "https://")): t = "/" + t.split("://", 1)[1].split("/", 1)[-1]
    t = t.split("?", 1)[0].split("#", 1)[0].rstrip("/")
    hubs = CFG["hubs"]
    if t.startswith("/"):
        cands = [(k, h) for k, h in hubs.items() if t.startswith(h["path"] + "/") and "/" not in t[len(h["path"]) + 1:]]
        if not cands: raise ValueError(f"{token}: no hub owns this URL (hub paths: {', '.join(h['path'] for h in hubs.values())})")
        k, h = cands[0]; slug = t[len(h["path"]) + 1:]
    elif ":" in t:
        hk, slug = t.split(":", 1); k = next((x for x in hubs if x.lower() == hk.strip().lower()), None)
        if k is None: raise ValueError(f"{token}: unknown hub {hk!r} (hubs: {', '.join(hubs)})")
        h = hubs[k]
    else:
        slug = t; hits = [(k, h) for k, h in hubs.items() if os.path.exists(os.path.join(ROOT, "specs", h["repo_dir"], slug + ".json"))]
        if len(hits) > 1:
            raise ValueError(f"{token}: ambiguous bare slug, it exists in {len(hits)} hubs; name one: " + ", ".join(f"{h['path']}/{slug} ({k}:{slug})" for k, h in hits))
        if not hits: raise ValueError(f"{token}: no spec in any hub")
        k, h = hits[0]
    slug = slug.strip()
    if not slug or "/" in slug: raise ValueError(f"{token}: no page slug")
    p = os.path.join(ROOT, "specs", h["repo_dir"], slug + ".json")
    if not os.path.exists(p): raise ValueError(f"{token}: no spec at specs/{h['repo_dir']}/{slug}.json ({k})")
    return f"{h['path']}/{slug}", p

def resolve_pages(tokens):
    """Resolve every --pages entry; ValueError listing every one that fails (all-or-nothing: never render a guessed page)."""
    out, errs = [], []
    for tok in tokens:
        if not tok.strip(): continue
        try: out.append(resolve_page(tok))
        except ValueError as e: errs.append(str(e))
    if errs: raise ValueError("refused: " + "; ".join(errs))
    return out

def brief_hash(spec):
    return hashlib.sha256(json.dumps(spec.get("image_brief"), sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()

def render_dir(spec):
    hub_dir = os.path.basename(os.path.dirname(spec["_path"])); slug = spec["url"].rsplit("/", 1)[1]
    return os.path.join(ROOT, "images", hub_dir, slug)

def load(path):
    s = json.load(open(path)); s["_path"] = path; return s

def current(spec):
    """True when render.json records this brief's hash (rendered from exactly this brief)."""
    p = os.path.join(render_dir(spec), "render.json")
    return os.path.exists(p) and json.load(open(p)).get("brief_sha256") == brief_hash(spec)

def git(*a): return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)

def changed_specs(before, after):
    if not before or set(before) == {"0"} or git("cat-file", "-e", before + "^{commit}").returncode:
        before = after + "~1"
    out = git("diff", "--name-only", before, after, "--", "specs/").stdout.split()
    keep = []
    for rel in out:
        if not rel.endswith(".json") or not os.path.exists(os.path.join(ROOT, rel)): continue
        old = git("show", f"{before}:{rel}")
        new = json.load(open(os.path.join(ROOT, rel)))
        try: ob = json.loads(old.stdout).get("image_brief") if old.returncode == 0 else None
        except ValueError: ob = None
        if new.get("image_brief") and ob != new.get("image_brief"): keep.append(os.path.join(ROOT, rel))
    return keep

def main(argv):
    if "-h" in argv or "--help" in argv: print(__doc__); return 0
    before, after = (argv + ["", "HEAD"])[:2] if argv and not argv[0].startswith("--") else ("", "HEAD")
    paths = set(changed_specs(before, after)) if before or after != "HEAD" else set()
    queued = [l.strip() for l in open(QUEUE)] if os.path.exists(QUEUE) else []
    extra = argv[argv.index("--pages") + 1].split(",") if "--pages" in argv else []
    if extra:   # B-c-1 2026-11-06: --pages renders ONLY those pages (writers passed wide sha ranges and re-rendered other writers' pages)
        paths, queued = set(), []
        try: paths = {p for _u, p in resolve_pages(extra)}   # 2026-11-11: URL or HUB:slug; an ambiguous bare slug never picks a hub
        except ValueError as e: print(e); return 2
    unresolved = []
    for q in [q for q in queued if q.strip() and not q.startswith("#")]:
        try: paths.add(resolve_page(q)[1])
        except ValueError as e: print(f"SKIP {e}"); unresolved.append(q)
    import engine
    done, bad, skipped = [], [], []
    for p in sorted(paths):
        s = load(p)
        if not s.get("image_brief"): skipped.append(s["url"]); continue
        if current(s) and "--force" not in argv: skipped.append(s["url"]); print(f"CURRENT {s['url']}"); continue
        try: ok = engine.render_spec(p)
        except Exception as e: print(f"BLOCKED {s['url']}: {type(e).__name__}: {e}"); ok = False   # one bad brief never stops the queue
        if not ok: bad.append(s["url"]); continue
        s = load(p)   # render_spec rewrites the spec's image paths and alt text
        json.dump({"brief_sha256": brief_hash(s), "commit": git("rev-parse", "HEAD").stdout.strip(),
                   "runner": os.environ.get("RUNNER_NAME") and "github-actions" or os.uname().sysname.lower(),
                   "rendered": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")},
                  open(os.path.join(render_dir(s), "render.json"), "w"), indent=1)
        done.append(s["url"])
    if queued:   # the queue is consumed: pages still stale stay listed for the next run
        def _url(q):
            try: return resolve_page(q)[0]
            except ValueError: return None
        left = [q for q in queued if q.strip() and not q.startswith("#") and (q in unresolved or _url(q) in bad)]
        open(QUEUE, "w").write("".join(x.strip() + "\n" for x in left))
    print(f"rendered {len(done)}; current already {len(skipped)}; blocked {len(bad)}" + (f": {', '.join(bad)}" if bad else ""))
    if done and "--no-commit" not in argv and os.environ.get("GITHUB_ACTIONS"):
        git("config", "user.name", "github-actions[bot]"); git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
        git("add", "images", "specs", "status/render-queue.txt")
        msg = f"Render images (Action): {len(done)} page(s)\n\n" + "\n".join(done)
        if git("commit", "-q", "-m", msg).returncode == 0:
            for i in range(5):
                if git("push", "-q", "origin", "HEAD:main").returncode == 0: print("pushed", git("rev-parse", "--short", "HEAD").stdout.strip()); break
                git("pull", "-q", "--rebase", "origin", "main")
            else: print("push failed after 5 attempts"); return 1
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
