#!/bin/bash
# Daily live audit on Divit's Mac (launchd: ~/Library/LaunchAgents/sh.emergent.live-audit.plist, 09:00 local, runs on wake).
#   bash ops/schedule/live_audit_daily.sh                      the daily run: hubctl live-audit --all, fixes enabled
#   LIVE_AUDIT_ARGS="--set launch --base https://emergent-sh.webflow.io --dry" bash ops/schedule/live_audit_daily.sh   a test
# Skips (and logs why) when the work tree has uncommitted changes or another session holds a lock (ops/guards.py held).
set -u
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO" || exit 1
LOG="$HOME/Library/Logs/emergent-live-audit.log"; ARGS="${LIVE_AUDIT_ARGS:---all}"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export CLAUDE_CONFIG_DIR="$HOME/.claude-b"
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG"; }
notify() { osascript -e "display notification \"${1//\"/\'}\" with title \"Emergent live audit\"" >/dev/null 2>&1; }
log "start (args: $ARGS)"
git pull -q --rebase origin main >> "$LOG" 2>&1 || { log "SKIP: git pull --rebase failed"; notify "Skipped: git pull failed (see log)"; exit 0; }
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then log "SKIP: work tree has uncommitted changes"; notify "Skipped: uncommitted changes in the repo"; exit 0; fi
if ! HELD="$(.venv/bin/python3 ops/guards.py held)"; then log "SKIP: lock held by another session: $HELD"; notify "Skipped: another session holds a lock ($HELD)"; exit 0; fi
PROMPT="$(sed "s|{{ARGS}}|$ARGS|g" ops/schedule/live_audit_prompt.md)"
ALLOWED=(
  "Read" "Glob" "Grep" "Agent"
  "Edit(specs/**)" "Write(.cache/live/**)"
  "Bash(.venv/bin/python3 ops/hubctl.py:*)" "Bash(.venv/bin/python3 ops/live_audit.py:*)" "Bash(.venv/bin/python3 tests/golden/run.py:*)"
  "Bash(.venv/bin/python3 ops/render_changed.py:*)" "Bash(node ops/live_audit.mjs:*)" "Bash(node ops/verify_launch.mjs:*)"
  "Bash(bash ops/sync.sh:*)" "Bash(git status:*)" "Bash(git log:*)" "Bash(git diff:*)"
  "mcp__webflow__data_cms_tool"
)
.venv/bin/python3 ops/guards.py run-locked session -- claude -p "$PROMPT" --permission-mode dontAsk --allowedTools "${ALLOWED[@]}" \
  --mcp-config "$REPO/.mcp.json" --output-format text >> "$LOG" 2>&1
RC=$?
REPORT="$(ls -t reports/*/*-live-audit*.md 2>/dev/null | head -1)"
DIGEST="$( [ -n "$REPORT" ] && awk '/^## Digest for Divit/{getline; getline; print; exit}' "$REPORT")"
log "end rc=$RC report=$REPORT digest=$DIGEST"
notify "${DIGEST:-Run ended (rc $RC); no report found, see ~/Library/Logs/emergent-live-audit.log}"
exit 0
