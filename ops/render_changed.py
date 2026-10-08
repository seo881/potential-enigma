"""render_changed.py: render images for changed pages only (the GitHub Action .github/workflows/render.yml runs it; any machine can).

    python3 ops/render_changed.py <before-sha> <after-sha> [--pages slug,slug] [--no-commit]

Render set = specs whose image_brief changed between the two commits, plus pages queued in status/render-queue.txt
(written by `hubctl ship` for pages whose images are not current), plus --pages. A page is skipped when its
images/<dir>/<slug>/render.json already records the current brief hash. Each page goes through engine.render_spec,
which runs every image gate; a blocked brief is reported and left unrendered (exit 1 at the end).
After a render, render.json records the brief hash, the commit and the runner, so `hubctl ship` and `hubctl readiness`
can tell whether a page's images are current. Prints one line per page.
"""
import hashlib, json, os, subprocess, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
QUEUE = os.path.join(ROOT, "status", "render-queue.txt")

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
    before, after = (argv + ["", "HEAD"])[:2] if argv and not argv[0].startswith("--") else ("", "HEAD")
    paths = set(changed_specs(before, after)) if before or after != "HEAD" else set()
    queued = [l.strip() for l in open(QUEUE)] if os.path.exists(QUEUE) else []
    extra = argv[argv.index("--pages") + 1].split(",") if "--pages" in argv else []
    import glob
    for slug in [q for q in queued + extra if q and not q.startswith("#")]:
        hit = glob.glob(os.path.join(ROOT, "specs", "*", slug.rsplit("/", 1)[-1] + ".json"))
        if hit: paths.add(hit[0])
        else: print(f"SKIP {slug}: no spec")
    import engine
    done, bad, skipped = [], [], []
    for p in sorted(paths):
        s = load(p)
        if not s.get("image_brief"): skipped.append(s["url"]); continue
        if current(s) and "--force" not in argv: skipped.append(s["url"]); print(f"CURRENT {s['url']}"); continue
        ok = engine.render_spec(p)
        if not ok: bad.append(s["url"]); continue
        s = load(p)   # render_spec rewrites the spec's image paths and alt text
        json.dump({"brief_sha256": brief_hash(s), "commit": git("rev-parse", "HEAD").stdout.strip(),
                   "runner": os.environ.get("RUNNER_NAME") and "github-actions" or os.uname().sysname.lower(),
                   "rendered": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")},
                  open(os.path.join(render_dir(s), "render.json"), "w"), indent=1)
        done.append(s["url"])
    if queued:   # the queue is consumed: pages still stale stay listed for the next run
        left = [q for q in queued if q.strip() and not q.startswith("#") and any(u.endswith("/" + q.strip().rsplit("/", 1)[-1]) for u in bad)]
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
