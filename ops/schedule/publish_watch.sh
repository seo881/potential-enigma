#!/bin/bash
# Publish watch (Divit 2026-10-09, after two unplanned production publishes): every 30 minutes (launchd sh.emergent.publish-watch),
# read Webflow's "Last Published" stamp from the public HTML of https://emergent.sh/ (curl only: no API, no Claude, no Webflow
# sites tool, so it cannot publish anything). When it differs from the last one seen:
#   1. SMOKE at once (Divit 2026-10-12): ops/publish_smoke.py checks the 4 hubs and one live page per hub (read-only HTTP, no git,
#      no Claude), so a dirty checkout or a busy session cannot delay it. Any failure raises a macOS alert and a log line
#      "SMOKE FAIL", once per stamp (.cache/live/smoke_alerted.txt). On 2026-10-12 the 10:05 UTC publish broke Learn and the
#      carousel on every live page and the audit waited 3 ticks behind "git pull failed", then reported it as P1.
#   2. Then the full live audit (all live pages and hubs, fixes on) through ops/schedule/live_audit_daily.sh, then store the stamp.
set -u
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO" || exit 1
LOG="$HOME/Library/Logs/emergent-live-audit.log"; STAMP="$REPO/.cache/live/last_published.txt"; mkdir -p "$(dirname "$STAMP")"
ALERTED="$REPO/.cache/live/smoke_alerted.txt"
NOW="$(curl -s --max-time 30 "https://emergent.sh/?pw=$(date +%s)" | grep -o 'Last Published: [^-]*' | head -1 | sed 's/ *$//')"
[ -z "$NOW" ] && { echo "$(date '+%F %T') publish-watch: no Last Published stamp read" >> "$LOG"; exit 0; }
LAST="$(cat "$STAMP" 2>/dev/null)"
if [ "$NOW" != "$LAST" ]; then
  echo "$(date '+%F %T') publish-watch: site published ($LAST -> $NOW); smoke check now" >> "$LOG"
  osascript -e "display notification \"Site published (${NOW#Last Published: }); not by Claude. Smoke check and live audit running now.\" with title \"emergent.sh site publish\"" >/dev/null 2>&1   # Divit 2026-10-14: tell him on every publish
  if [ "$(cat "$ALERTED" 2>/dev/null)" != "$NOW" ]; then
    SMOKE="$("$REPO/.venv/bin/python3" "$REPO/ops/publish_smoke.py" 2>&1)"; RC=$?
    if [ $RC -ne 0 ]; then
      echo "$(date '+%F %T') SMOKE FAIL after publish ($NOW):" >> "$LOG"; echo "$SMOKE" | head -12 >> "$LOG"
      osascript -e "display notification \"Site publish broke live pages: $(echo "$SMOKE" | grep -c '^FAIL') failing (Learn/carousel/template). See emergent-live-audit.log\" with title \"emergent.sh SMOKE FAIL\" sound name \"Basso\"" 2>/dev/null
    else
      echo "$(date '+%F %T') smoke ok: $(echo "$SMOKE" | head -1)" >> "$LOG"
    fi
    echo "$NOW" > "$ALERTED"
  fi
  echo "$(date '+%F %T') publish-watch: running the live audit now" >> "$LOG"
  LIVE_AUDIT_ARGS="--all" bash "$REPO/ops/schedule/live_audit_daily.sh"   # it stores the stamp itself only after a real run, so a skipped audit is retried next tick
fi
