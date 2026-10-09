#!/bin/bash
# Publish watch (Divit 2026-10-09, after two unplanned production publishes): every 30 minutes (launchd sh.emergent.publish-watch),
# read Webflow's "Last Published" stamp from https://emergent.sh/ (no API, no Claude). When it differs from the last one seen,
# run the live audit at once (all live pages and hubs, fixes on) through ops/schedule/live_audit_daily.sh, then store the stamp.
set -u
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO" || exit 1
LOG="$HOME/Library/Logs/emergent-live-audit.log"; STAMP="$REPO/.cache/live/last_published.txt"; mkdir -p "$(dirname "$STAMP")"
NOW="$(curl -s --max-time 30 "https://emergent.sh/?pw=$(date +%s)" | grep -o 'Last Published: [^-]*' | head -1 | sed 's/ *$//')"
[ -z "$NOW" ] && { echo "$(date '+%F %T') publish-watch: no Last Published stamp read" >> "$LOG"; exit 0; }
LAST="$(cat "$STAMP" 2>/dev/null)"
if [ "$NOW" != "$LAST" ]; then
  echo "$(date '+%F %T') publish-watch: site published ($LAST -> $NOW); running the live audit now" >> "$LOG"
  LIVE_AUDIT_ARGS="--all" bash "$REPO/ops/schedule/live_audit_daily.sh" && echo "$NOW" > "$STAMP"
fi
