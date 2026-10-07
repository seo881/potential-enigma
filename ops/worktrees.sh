#!/usr/bin/env bash
# One git worktree per hub, for four simultaneous Claude Code sessions (RUNBOOK "Parallel hubs").
#   bash ops/worktrees.sh            -> ~/emergent-hubs-lp, -form, -auto, -survey
#   WT_BASE=/some/dir bash ops/worktrees.sh   (testing)
# Each worktree is pinned to its hub (.hub): hubctl claim refuses any other hub there. Git-ignored shared state
# (.venv, private/, .cache/, .locks/, the keyword map) is symlinked to this checkout, so all sessions share one SERP
# store, one DataForSEO budget and one set of file locks. Commit with ops/sync.sh, which rebases on origin/main first.
set -euo pipefail
MAIN="$(cd "$(dirname "$0")/.." && pwd)"; BASE="${WT_BASE:-$HOME}"
cd "$MAIN"; mkdir -p .locks; git fetch -q origin
for pair in lp:LP form:Form auto:Auto survey:SurveyQuiz; do
  name=${pair%%:*}; hub=${pair##*:}; wt="$BASE/emergent-hubs-$name"; br="hub/$name"
  if [ -d "$wt/.git" ] || [ -f "$wt/.git" ]; then echo "exists: $wt"
  else git worktree add -q -B "$br" "$wt" origin/main; fi
  git -C "$wt" branch -q --set-upstream-to=origin/main "$br"
  echo "$hub" > "$wt/.hub"
  for p in .venv private .cache .locks plan/keyword_map.json plan/queue.csv; do
    [ -e "$MAIN/$p" ] || continue
    if [ -e "$wt/$p" ] && [ ! -L "$wt/$p" ]; then continue; fi
    ln -sfn "$MAIN/$p" "$wt/$p"
  done
  echo "ready: $wt  hub=$hub  branch=$br -> origin/main"
done
echo "Start one Claude Code session per worktree. Each claims only its hub: python3 ops/hubctl.py claim <HUB> 25 --by <session>."
