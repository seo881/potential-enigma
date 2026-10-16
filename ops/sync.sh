#!/usr/bin/env bash
# Commit exactly the paths you pass, then push to main (from main or a hub worktree).
#   bash ops/sync.sh "message" <path> [<path> ...]
#
# Many agents share one clone (and one git index), so this script commits ONLY the paths on its command line (Divit 2026-10-15:
# d5109889 swept in another agent's unfinished tests/golden/run.py, because the old script ran `git commit` on the whole index):
#   - paths are required; a directory is refused unless it is a per-page or per-run folder (allowlist below);
#     ".", globs, absolute paths, "..", options, private/ and .cache/ are refused
#   - `git add -- <paths>` then `git commit --only -- <paths>`: whatever else is staged or modified in the clone stays out
#   - the diffstat of exactly what will be committed is printed first
#   - conflict markers and the review lock (ruling 10 B2) are checked on these paths only
#   - the merge of origin happens AFTER the commit and only when origin moved (fetch first); no rebase, no autostash (2026-10-16), so other
#     agents' files into the commit; a pop conflict is reported (their changes stay in `git stash list`), never committed
# Shared files (status/<hub>.json, status/usage.jsonl, reports/INDEX.md, tests/golden/cases.jsonl) stay committable: pass only the
# shared files YOU changed, and remember the whole file is committed (another agent's pending edit to that same file goes with it).
set -euo pipefail
die() { echo "sync.sh: $*" >&2; exit 1; }
[ $# -ge 2 ] || die "usage: bash ops/sync.sh \"message\" <path> [<path> ...] (explicit paths are required; nothing is committed without them)"
msg="$1"; shift
[ -n "$msg" ] || die "empty commit message"
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$(git rev-parse --show-toplevel)"

# directories allowed as a whole: one page's images, one live-audit run
DIR_ALLOW='^(images/[^/]+/[^/]+|audits/live/[0-9]{4}-[0-9]{2}-[0-9]{2})/?$'
for p in "$@"; do
  case "$p" in
    ""|.|./|-*|/*|*..*|*'*'*|*'?'*|*'['*|:*) die "refusing path '$p': pass plain repo-relative file paths (no '.', options, globs, absolute or '..')";;
    private|private/*|.cache|.cache/*) die "refusing path '$p': private/ and .cache/ never go to git";;
  esac
  if [ -d "$p" ]; then
    echo "$p" | grep -Eq "$DIR_ALLOW" || die "refusing directory '$p': pass the files you changed (directories allowed: images/<hub>/<slug>, audits/live/<date>)"
  elif [ ! -e "$p" ] && ! git ls-files --error-unmatch -- "$p" >/dev/null 2>&1 && ! git cat-file -e "HEAD:$p" 2>/dev/null; then
    die "refusing path '$p': it does not exist and is not tracked"
  fi
done

# one sync at a time per clone (the index and the rebase are shared); a lock left by a dead process is taken over
LOCK="$(git rev-parse --git-common-dir)/sync.lock"
for i in $(seq 1 120); do
  if mkdir "$LOCK" 2>/dev/null; then echo $$ > "$LOCK/pid"; break; fi
  pid="$(cat "$LOCK/pid" 2>/dev/null || true)"
  if [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null; then rm -rf "$LOCK"; continue; fi
  [ "$i" -eq 120 ] && die "another ops/sync.sh holds $LOCK for 120 s (pid ${pid:-?}); rerun when it finishes"
  sleep 1
done
trap 'rm -rf "$LOCK"' EXIT

unstage() { git restore --staged -- "$@" 2>/dev/null || true; }
git add -- "$@"
if ! git diff --cached --quiet -- "$@"; then
  # an autostash that collided with an upstream commit leaves conflict markers in the tree: never commit them
  # (2026-10-12: 25 render.json files were committed with markers)
  bad="$(git diff --cached --name-only --diff-filter=d -z -- "$@" | xargs -0 grep -lE '^(<<<<<<< |>>>>>>> |=======$)' -- 2>/dev/null || true)"
  if [ -n "$bad" ]; then
    echo "refusing to commit: conflict markers in staged files (resolve them, then rerun):" >&2; echo "$bad" >&2; unstage "$@"; exit 1
  fi
  # review lock (ruling 10 B2): after review only fields named in a blocking finding may change
  PY="$HERE/../.venv/bin/python3"; [ -x "$PY" ] || PY=python3
  SPECS="$(git diff --cached --name-only --diff-filter=d -- "$@" | grep '^specs/.*\.json$' || true)"
  if [ -n "$SPECS" ] && ! echo "$SPECS" | xargs "$PY" "$HERE/review_lock.py"; then
    echo "refusing to commit: review lock (see above)" >&2; unstage "$@"; exit 1
  fi
  echo "committing (only these paths):"; git diff --cached --stat -- "$@"
  git commit -q --only -m "$msg" -- "$@"
  others="$(git diff --cached --name-only | wc -l | tr -d ' ')"
  [ "$others" = 0 ] || echo "note: $others other staged path(s) in this clone were left out of the commit (not yours)"
else
  echo "nothing to commit in the given paths; pushing any local commits"
fi

for i in 1 2 3 4 5; do
  git fetch -q origin main
  if ! git merge-base --is-ancestor FETCH_HEAD HEAD; then
    # origin moved: MERGE it (B-c-1 2026-10-16). Never rebase with --autostash in this shared tree: a conflicted autostash pop left
    # every other agent's uncommitted files in `git stash` and reset their specs mid-write (many writers hit it on 2026-10-16).
    # A merge never touches uncommitted files: if upstream changes a file someone has uncommitted, git refuses and nothing is lost.
    if ! git merge -q --no-edit FETCH_HEAD; then
      if [ -n "$(git ls-files -u)" ]; then git merge --abort 2>/dev/null || true; fi
      die "merge of origin/main refused (upstream touches files that are uncommitted here, or your commit conflicts); your commit is local and unpushed: rerun once those files are committed"
    fi
  fi
  if git push -q origin HEAD:main; then git log --oneline -1; exit 0; fi
  sleep $((i * 2))
done
die "push failed after 5 attempts"
