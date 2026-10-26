#!/bin/bash
# Daily live audit on Divit's Mac (launchd: ~/Library/LaunchAgents/sh.emergent.live-audit.plist, 09:00 local, runs on wake; also run by
# publish_watch.sh after a site publish).
#   bash ops/schedule/live_audit_daily.sh                                  the daily run
#   launchctl kickstart -k gui/$(id -u)/sh.emergent.live-audit             the same, through launchd
# Divit 2026-10-23: the CHECKS come first and have no Claude dependency: ops/schedule/live_audit_checks.sh (plain bash + Python + node,
# read-only) writes audits/live/DATE/findings.json and digest.txt and notifies the counts. Only then, optionally, `claude -p` writes a
# prose digest from those findings (read-only tools). If that step fails (not logged in, timeout, anything), the log and the notification
# say "digest unavailable" with the plain counts. An older report's digest is never printed.
# The checks run even when the work tree is dirty or another session holds a lock (they write nothing to git or Webflow); that is logged.
set -u
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO" || exit 1
LOG="$HOME/Library/Logs/emergent-live-audit.log"
export EMG_HEADLESS=1   # ruling 19: ops/webflow_api.py refuses CMS writes when set
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export CLAUDE_CONFIG_DIR="$HOME/.claude"   # ruling 22 (Divit 2026-10-14): B is coordinator; the live audit runs in B's clone on account B
[ "$(basename "$REPO")" = "emergent-hubs-a" ] || { echo "$(date '+%Y-%m-%d %H:%M:%S') SKIP: ruling 22: the live audit runs only in B's clone ~/emergent-hubs-a (this is $REPO)" >> "$LOG"; exit 0; }
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG"; }
notify() { osascript -e "display notification \"${1//\"/\'}\" with title \"Emergent live audit\"" >/dev/null 2>&1; }
DATE="$(date +%F)"; ADIR="$REPO/audits/live/$DATE"
log "start (checks first: ops/schedule/live_audit_checks.sh; no Claude)"
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then log "note: work tree has uncommitted changes (not pulled; the checks read the specs as they are)"
else git pull -q --rebase origin main >> "$LOG" 2>&1 || log "note: git pull --rebase failed; checking with the local tree"; fi
HELD="$(.venv/bin/python3 ops/guards.py held 2>&1)" || log "note: lock held by another session ($HELD); the read-only checks run anyway"

# ---- 1. the checks (Claude-free) ----
rm -f "$ADIR/digest.txt" "$ADIR/digest-prose.txt"   # a digest from an earlier run today must never stand in for this run
bash ops/schedule/live_audit_checks.sh --no-shots >> "$LOG" 2>&1; CRC=$?
curl -s --max-time 30 "https://emergent.sh/?pw=$(date +%s)" | grep -o 'Last Published: [^-]*' | head -1 | sed 's/ *$//' > "$REPO/.cache/live/last_published.txt"   # seen by publish_watch.sh
if [ $CRC -ne 0 ] || [ ! -s "$ADIR/digest.txt" ]; then
  log "end: CHECKS FAILED (rc $CRC); no digest for $DATE"; notify "Live audit checks FAILED (rc $CRC); see ~/Library/Logs/emergent-live-audit.log"; exit 0
fi
COUNTS="$(sed -n 2,3p "$ADIR/digest.txt" | tr '\n' ' ' | sed 's/  */ /g')"
log "checks ok: $COUNTS (audits/live/$DATE/digest.txt)"
REAL="$(.venv/bin/python3 ops/audit_status.py real "$ADIR/findings.json" 2>&1)"; RRC=$?; log "$REAL"   # Divit 2026-10-26: alerts only on REAL failures

# ---- 2. optional prose digest by Claude (read-only; its failure never hides the counts) ----
PROMPT="$(sed "s|{{DATE}}|$DATE|g" ops/schedule/live_audit_prompt.md)"
ALLOWED=("Read" "Glob" "Grep")
# NO SITE PUBLISH (Divit 2026-10-10): the Webflow sites tool (publish_site) is denied under every name it can appear as,
# on top of .claude/settings.json; this step has no Webflow tool at all.
DENIED=("mcp__webflow__data_sites_tool" "mcp__Webflow__data_sites_tool" "mcp__claude_ai_Webflow__data_sites_tool"
        "mcp__webflow__data_cms_tool" "Edit" "Write" "Bash" "Agent")
# Ruling 19 (Divit 2026-10-14): the direct-API CMS write commands never run headless
for c in api-create api-update api-publish; do DENIED+=("Bash(.venv/bin/python3 ops/hubctl.py $c:*)" "Bash(python3 ops/hubctl.py $c:*)"); done
DENIED+=("Bash(.venv/bin/python3 ops/ship.py:*)" "Bash(python3 ops/ship.py:*)" "Bash(.venv/bin/python3 ops/webflow_api.py:*)" "Bash(python3 ops/webflow_api.py:*)")
OUT="$(mktemp -t emg-digest)"
claude -p "$PROMPT" --permission-mode dontAsk --allowedTools "${ALLOWED[@]}" --disallowedTools "${DENIED[@]}" --output-format text > "$OUT" 2>&1 &
CPID=$!; ( sleep 900; kill -TERM "$CPID" 2>/dev/null ) >/dev/null 2>&1 & WD=$!
wait "$CPID"; RC=$?; kill "$WD" 2>/dev/null; wait "$WD" 2>/dev/null
if [ $RC -eq 0 ] && grep -q "Live audit $DATE" "$OUT"; then   # the prose must name this run's date, or it is not this run's digest
  cp "$OUT" "$ADIR/digest-prose.txt"; log "prose digest: $(head -1 "$OUT" | cut -c1-300)"
  [ $RRC -eq 3 ] && notify "$REAL | $(head -1 "$OUT" | cut -c1-120)"
else
  log "digest unavailable (claude rc $RC: $(tail -1 "$OUT" | cut -c1-160)); plain counts: $COUNTS"
  [ $RRC -eq 3 ] && notify "Digest unavailable. $REAL"
fi
rm -f "$OUT"
log "end: checks rc $CRC; findings audits/live/$DATE/findings.json; digest audits/live/$DATE/digest.txt"
exit 0
