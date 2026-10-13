#!/usr/bin/env bash
# Commit and push from any checkout (main or a hub worktree): pull with rebase first, then commit, then push to main.
#   bash ops/sync.sh "message" <paths...>
set -euo pipefail
msg="$1"; shift
git pull -q --rebase --autostash origin main
git add -- "$@"
# an autostash that collides with an upstream commit (e.g. the render Action) leaves conflict markers in the tree: never commit them
# (2026-10-12: 25 render.json files were committed with markers)
if git diff --cached --name-only -z | xargs -0 -r grep -lE '^(<<<<<<< |>>>>>>> |=======$)' -- 2>/dev/null | grep -q .; then
  echo "refusing to commit: conflict markers in staged files (resolve them, then rerun):" >&2
  git diff --cached --name-only -z | xargs -0 -r grep -lE '^(<<<<<<< |>>>>>>> |=======$)' -- >&2; git reset -q; exit 1
fi
# review lock (ruling 10 B2): after review only fields named in a blocking finding may change
PY="$(dirname "$0")/../.venv/bin/python3"; [ -x "$PY" ] || PY=python3
if ! git diff --cached --name-only | grep '^specs/' | xargs "$PY" "$(dirname "$0")/review_lock.py"; then
  echo "refusing to commit: review lock (see above)" >&2; git reset -q; exit 1
fi
git diff --cached --quiet || git commit -q -m "$msg"
for i in 1 2 3 4 5; do
  if git push -q origin HEAD:main; then git log --oneline -1; exit 0; fi
  sleep $((i * 2)); git pull -q --rebase --autostash origin main
done
echo "push failed after 5 attempts" >&2; exit 1
