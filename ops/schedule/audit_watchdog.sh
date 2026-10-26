#!/bin/bash
# audit_watchdog.sh: post-live QC watchdog (Divit 2026-10-23 "post-live QC never stops"; A 2026-10-26). Every 2 h from launchd
# (sh.emergent.audit-watchdog). Alerts (macOS notification with sound) when the last full live audit is older than 26 h OR the
# GitHub Actions backup audit's newest completed run failed, was cancelled or timed out, or none succeeded in 26 h.
# Read-only: local files and the public GitHub API; no git, no Claude, no Webflow. Runs from whichever clone holds this file.
set -u
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO" || exit 1
PY="$REPO/.venv/bin/python3"; [ -x "$PY" ] || PY=python3
LOG="$HOME/Library/Logs/emergent-audit-watchdog.log"
OUT="$("$PY" ops/audit_status.py watchdog --runner "watchdog:$(hostname -s)" 2>&1)"; RC=$?
echo "$(date '+%F %T') rc=$RC $(echo "$OUT" | tr '\n' ' ')" >> "$LOG"
if [ $RC -ne 0 ]; then
  MSG="$(echo "$OUT" | grep -E 'STALE|FAILED|unknown|no completed' | head -2 | tr '\n' ' ' | tr -d '"')"
  osascript -e "display notification \"${MSG:-audit watchdog rc $RC}\" with title \"emergent.sh live audit ALERT\" sound name \"Basso\"" >/dev/null 2>&1
fi
exit 0
