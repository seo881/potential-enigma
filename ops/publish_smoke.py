"""Publish smoke check (Divit 2026-10-12): run by ops/schedule/publish_watch.sh the moment a new "Last Published" stamp shows on
emergent.sh, before (and independent of) the full live audit. Read-only: HTTP GET only, no Webflow API, no git, so a dirty
checkout or a busy session cannot delay it (the 10:05 UTC publish on 2026-10-12 waited 3 ticks behind "git pull failed").

    .venv/bin/python3 ops/publish_smoke.py [--base https://emergent.sh]

Checks the 4 hubs and one live page per hub with ops/verify_launch.mjs (all page checks, carousel hidden, Learn state).
Prints PASS/FAIL lines, writes .cache/live/smoke-<stamp>.txt, exits 1 on any failure (the watcher then raises a macOS alert)."""
import json, os, subprocess, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ops"))
import hubctl as H, live_audit as LA

def main(argv):
    base = argv[argv.index("--base") + 1] if "--base" in argv else "https://emergent.sh"
    pub = LA.published_urls(); pages = []
    for hub, h in H.CFG["hubs"].items():
        u = next((x for x in pub if H.hub_of(x) == hub), None)
        if u: pages.append(LA.manifest_entry(u))
    man = {"pages": pages, "hubs": sorted(h["path"] for h in H.CFG["hubs"].values())}
    d = os.path.join(ROOT, ".cache", "live"); os.makedirs(d, exist_ok=True)
    mp = os.path.join(d, "smoke-manifest.json"); json.dump(man, open(mp, "w"), indent=1, ensure_ascii=False)
    r = subprocess.run(["node", os.path.join(ROOT, "ops", "verify_launch.mjs"), mp, "--base", base], cwd=ROOT, capture_output=True, text=True, timeout=900)
    out = r.stdout + r.stderr
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    open(os.path.join(d, f"smoke-{stamp}.txt"), "w").write(out)
    bad = [l for l in out.splitlines() if l.startswith("FAIL")]
    print(out.strip().splitlines()[-1] if out.strip() else "no output")
    for l in bad: print(l[:300])
    return 1 if (bad or r.returncode not in (0, 1)) else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
