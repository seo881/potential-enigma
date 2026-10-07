#!/usr/bin/env bash
# Commit and push from any checkout (main or a hub worktree): pull with rebase first, then commit, then push to main.
#   bash ops/sync.sh "message" <paths...>
set -euo pipefail
msg="$1"; shift
git pull -q --rebase --autostash origin main
git add -- "$@"
git diff --cached --quiet || git commit -q -m "$msg"
for i in 1 2 3 4 5; do
  if git push -q origin HEAD:main; then git log --oneline -1; exit 0; fi
  sleep $((i * 2)); git pull -q --rebase --autostash origin main
done
echo "push failed after 5 attempts" >&2; exit 1
