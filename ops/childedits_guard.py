#!/usr/bin/env python3
"""childedits write-once commit guard (Divit 2026-11-16), called by ops/sync.sh on the staged paths.
  childedits_guard.py RUN < name-status lines ("M\tpath", "A\tpath", "D\tpath", "R100\told\tnew")
Refuses (exit 1, one line per problem):
  - any change (M), deletion (D) or rename (R) of an existing childedits/**/*.before.json or *.rollback.json: they are write-once;
  - a NEW childedits file whose name does not contain the committing run's name (SYNC_RUN; comma-separated tokens allowed):
    another run's before-value/rollback never goes into your commit. With no SYNC_RUN, any childedits file is refused."""
import re, sys

GUARDED = re.compile(r"^childedits/.+\.(before|rollback)\.json$")

def problems(lines, run):
    toks = [t for t in (run or "").split(",") if t.strip()]
    out = []
    for ln in lines:
        parts = ln.rstrip("\n").split("\t")
        if len(parts) < 2: continue
        st, paths = parts[0], parts[1:]
        for p in paths:
            if not p.startswith("childedits/"): continue
            name = p.rsplit("/", 1)[-1]
            if GUARDED.match(p) and st[:1] in ("M", "D", "R", "T"):
                out.append(f"{p}: before-values and rollbacks are write-once; this commit would {'modify' if st[:1] in 'MT' else 'delete' if st[:1] == 'D' else 'rename'} an existing one")
            elif st[:1] in ("A", "C"):
                if not toks: out.append(f"{p}: committing childedits files needs SYNC_RUN=<your batch/run name> (only your own run's files)")
                elif not any(t in name for t in toks): out.append(f"{p}: not this run's file (SYNC_RUN={run}); never commit another run's childedits files")
    return out

if __name__ == "__main__":
    pr = problems(sys.stdin.readlines(), sys.argv[1] if len(sys.argv) > 1 else "")
    for p in pr: print("childedits guard: " + p, file=sys.stderr)
    sys.exit(1 if pr else 0)
