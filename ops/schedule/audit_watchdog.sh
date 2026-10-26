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
  # What "Open report" opens (Divit 2026-10-26: a click must open the report, not a blank Script Editor): the failing GitHub run when
  # the backup failed, else the newest audit digest.
  TARGET="$(echo "$OUT" | grep -q 'BACKUP AUDIT' && echo "$OUT" | grep -qE 'BACKUP AUDIT (FAILED|STALE)' && echo "https://github.com/seo881/potential-enigma/actions/workflows/live-audit.yml")"
  [ -z "$TARGET" ] && TARGET="$(ls -t "$REPO"/audits/live/*/digest.txt 2>/dev/null | head -1)"
  [ -z "$TARGET" ] && TARGET="$HOME/Library/Logs/emergent-audit-watchdog.log"
  BTN="$(osascript -e "display dialog \"${MSG:-audit watchdog rc $RC}\" & return & return & \"Report: $TARGET\" with title \"emergent.sh live audit ALERT\" buttons {\"OK\", \"Open report\"} default button \"Open report\" with icon caution giving up after 3600" 2>/dev/null)"
  case "$BTN" in *"Open report"*) open "$TARGET";; esac
fi
exit 0
