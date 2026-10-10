#!/bin/bash
# Weekend run loop (Divit, 2026-10-10). Plan, rules and position: plan/weekend-run.md; next unit: ops/weekend.py.
#   start:  nohup bash ops/schedule/weekend_run.sh >/dev/null 2>&1 &      (started detached; PID in .cache/weekend/pid)
#   watch:  tail -f ~/Library/Logs/emergent-weekend-run.log
#   stop:   touch ~/emergent-hubs/STOP      (clean stop after the current page; rm STOP before the next start)
# Loops headless Claude Code (CLAUDE_CONFIG_DIR=~/.claude-b, no fast mode) with "Continue the weekend run per plan/weekend-run.md".
# NO Webflow tools: no MCP server is loaded at all (--strict-mcp-config, empty config; DataForSEO retired 2026-10-10) and every
# Webflow tool is denied by name. AlsoAsked only through weekend.py aa (the per-page cap); ops/alsoasked_pull.py is not allowed. The AlsoAsked key comes from the macOS keychain (service "alsoasked", account $USER) before each
# session, never from a file or the repo, and is never printed; missing key: new pages stay held ("AlsoAsked key missing").
# Session limit: sleep to the reset time the message gives, else 20 minutes; limited for 7 continuous hours, a weekly-limit
# message or any mention of paid/extra usage: stop for good. Waits while another job holds a lock (ops/guards.py held) and
# keeps 08:20-09:45 local free for the 09:00 live audit (clean tree, no lock). Renders run locally in the background (render_bg).
set -u
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO" || exit 1
LOG="$HOME/Library/Logs/emergent-weekend-run.log"; AUDIT_LOG="$HOME/Library/Logs/emergent-live-audit.log"
RUN="$REPO/.cache/weekend"; mkdir -p "$RUN"
PY="$REPO/.venv/bin/python3"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export CLAUDE_CONFIG_DIR="$HOME/.claude-b"
unset CLAUDECODE CLAUDE_CODE_ENTRYPOINT CLAUDE_CODE_MESSAGING_SOCKET CLAUDE_CODE_MESSAGING_TOKEN CLAUDE_CODE_EXECPATH \
      CLAUDE_CODE_SESSION_ID CLAUDE_CODE_CHILD_SESSION CLAUDE_CODE_SESSION_ATTENDED CLAUDE_PID CLAUDE_EFFORT
PROMPT="Continue the weekend run per plan/weekend-run.md"
MAX_ITER_SECS=$((4 * 3600)); LIMIT_GIVEUP_SECS=$((7 * 3600))

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG"; }
notify() { osascript -e "display notification \"${1//\"/\'}\" with title \"Emergent weekend run\"" >/dev/null 2>&1; }

ALLOWED=(
  "Read" "Glob" "Grep" "Agent" "Skill" "ToolSearch" "TodoWrite" "WebSearch" "WebFetch"
  "Edit(specs/**)" "Edit(.cache/**)" "Edit(//tmp/**)" "Edit(//private/tmp/**)" "Edit(plan/backlog.md)"
  "Bash(.venv/bin/python3 ops/hubctl.py:*)" "Bash(python3 ops/hubctl.py:*)" "Bash(.venv/bin/python3 ops/weekend.py:*)"
  "Bash(.venv/bin/python3 qc/qc_hub.py:*)" "Bash(python3 qc/qc_hub.py:*)"
  "Bash(.venv/bin/python3 qc/paa_gate.py:*)" "Bash(.venv/bin/python3 ops/autofix.py:*)" "Bash(.venv/bin/python3 ops/table.py:*)"
  "Bash(.venv/bin/python3 ops/typeset.py:*)" "Bash(.venv/bin/python3 ops/review.py:*)" "Bash(.venv/bin/python3 ops/preview.py:*)"
  "Bash(.venv/bin/python3 tests/golden/run.py:*)" "Bash(.venv/bin/python3 -c:*)" "Bash(.venv/bin/python3 .cache/:*)"
  "Bash(.venv/bin/python3 /tmp/:*)" "Bash(.venv/bin/python3 /private/tmp/:*)"
  "Bash(bash ops/sync.sh:*)" "Bash(git status:*)" "Bash(git log:*)" "Bash(git diff:*)" "Bash(git show:*)" "Bash(git checkout -- specs/:*)"
  "Bash(date:*)" "Bash(ls:*)" "Bash(test -f:*)" "Bash(mkdir -p .cache/:*)" "Bash(wc:*)"
)
# Every Webflow tool, by name and by server, under the three names the server can appear as (no Webflow calls this weekend).
WF_TOOLS=(ask_webflow_ai asset_tool data_agent_instructions_tool data_analyze_tool data_apps_tool data_assets_tool data_campaigns_tool
  data_cms_tool data_comments_tool data_component_builder data_component_props_tool data_component_tool data_component_variants_tool
  data_element_builder data_element_settings_tool data_element_tool data_enterprise_tool data_fonts_tool data_forms_tool
  data_interactions_tool data_localization_tool data_pages_tool data_scripts_tool data_sitemap_tool data_sites_tool data_style_tool
  data_variable_tool data_webhook_tool data_whtml_builder designer_tool element_snapshot_tool get_asset_preview get_more_tools webflow_guide_tool)
DENIED=("mcp__webflow" "mcp__Webflow" "mcp__claude_ai_Webflow" "mcp__webflow__*" "mcp__Webflow__*" "mcp__claude_ai_Webflow__*")
for t in "${WF_TOOLS[@]}"; do DENIED+=("mcp__webflow__$t" "mcp__Webflow__$t" "mcp__claude_ai_Webflow__$t"); done

# Seconds to sleep for a session-limit message: the reset time it names (+2 min), or 20 minutes; "WEEKLY" when it is not a 5-hour reset.
reset_wait() {
  "$PY" - "$1" <<'PYEOF'
import re, sys, time, datetime
from zoneinfo import ZoneInfo
t = open(sys.argv[1], errors="ignore").read()[-1500:]
if re.search(r"weekly|week limit|7-day limit", t, re.I): print("WEEKLY"); sys.exit()
m = re.search(r"limit reached\|(\d{10})", t)
if m: print(max(60, int(m.group(1)) - int(time.time()) + 120)); sys.exit()
m = re.search(r"resets?\s+(?:at\s+)?(?:([A-Z][a-z]{2})\s+(\d{1,2}),?\s+(?:at\s+)?)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s*(?:\(([^)]+)\))?", t, re.I)
if not m: print(1200); sys.exit()
mon, day, hh, mm, ap, tz = m.groups()
try: zone = ZoneInfo(tz) if tz else None
except Exception: zone = None
now = datetime.datetime.now(zone) if zone else datetime.datetime.now().astimezone()
h = int(hh) % 12 + (12 if (ap or "").lower() == "pm" else 0) if ap else int(hh)
r = now.replace(hour=h, minute=int(mm or 0), second=0, microsecond=0)
if mon: r = r.replace(month=datetime.datetime.strptime(mon, "%b").month, day=int(day))
while r <= now: r += datetime.timedelta(days=1)
secs = int((r - now).total_seconds()) + 120
print(min(secs, 5 * 3600 + 120))   # a 5-hour reset is never further; the 7-hour rule stops a longer limit
PYEOF
}

# Keep 08:20-09:45 local free for the 09:00 live audit, and wait while any job holds a lock.
audit_ran_today() { grep -qE "^$(date +%F) (09|1[0-9]|2[0-3]):[0-9:]+ (end rc=|SKIP)" "$AUDIT_LOG" 2>/dev/null; }   # the 09:00 run happened (or tried)
watch_pending() {   # the site was published since the last audited stamp (same public-HTML read as publish_watch.sh): its audit needs a free tree
  local now; now="$(curl -s --max-time 30 "https://emergent.sh/?pw=$(date +%s)" | grep -o 'Last Published: [^-]*' | head -1 | sed 's/ *$//')"
  [ -n "$now" ] && [ "$now" != "$(cat "$REPO/.cache/live/last_published.txt" 2>/dev/null)" ]
}
wait_for_others() {
  local stashed="" hm=0 wstart=0
  while :; do
    [ -f "$REPO/STOP" ] && return
    hm=$((10#$(date +%H%M)))
    if [ "$hm" -ge 820 ] && [ "$hm" -lt 945 ] && ! audit_ran_today; then
      if [ -z "$stashed" ] && [ -n "$(git status --porcelain --untracked-files=no)" ]; then
        git stash push -q -m "weekend-wip $(date +%F-%H%M) (audit window)" && stashed=1 && log "audit window: stashed uncommitted work"
      fi
      log "audit window: waiting for the 09:00 live audit"; sleep 300; continue
    fi
    if watch_pending && { [ $wstart -eq 0 ] && wstart=$(date +%s); [ $(( $(date +%s) - wstart )) -lt 2700 ]; }; then
      log "publish watch: a site publish is waiting for its live audit; pausing (up to 45 min)"; sleep 300; continue
    fi
    HELD="$("$PY" ops/guards.py held)" && break
    [ "$HELD" = "render" ] && break                      # our own background render: never wait on it
    log "lock held by another job ($HELD): waiting"; sleep 120
  done
  [ "$hm" -ge 945 ] && [ "$hm" -lt 1000 ] && ! audit_ran_today && { log "WARNING: no live audit ran this morning (skipped or late)"; notify "No live audit ran this morning; see ~/Library/Logs/emergent-live-audit.log"; }
  if [ -n "$stashed" ]; then
    git pull -q --rebase origin main >> "$LOG" 2>&1
    git stash pop -q >> "$LOG" 2>&1 && log "audit window over: restored stashed work" || log "WARNING: stash pop failed; work kept in git stash list"
  fi
}

# Local renders (Divit 2026-10-10): images render on this Mac as soon as a page reaches the images stage, in the background,
# while writer and review units keep running. Never an idle wait on the render Action.
RPID=0
render_bg() {
  [ $RPID -ne 0 ] && kill -0 $RPID 2>/dev/null && return
  [ -s "$REPO/status/render-queue.txt" ] || return
  "$PY" ops/weekend.py render >> "$LOG" 2>&1 & RPID=$!
  log "local render started in the background (pid $RPID)"
}

finish() { log "$1"; "$PY" ops/weekend.py tick --final >> "$LOG" 2>&1; notify "$1"; log "weekend run ended"; exit 0; }

echo $$ > "$RUN/pid"
caffeinate -dimsu -w $$ &
log "weekend run started (pid $$, caffeinate $!)"
trap 'log "terminated by signal"; exit 0' TERM INT
LIMITED_SINCE=0; ERRS=0; IDLE=0; RENDER_WAITS=0; N=0; W_LAST=""
"$PY" ops/weekend.py init >> "$LOG" 2>&1

while :; do
  [ -f "$REPO/STOP" ] && finish "STOP file found: stopped cleanly"
  wait_for_others
  [ -f "$REPO/STOP" ] && finish "STOP file found: stopped cleanly"
  git pull -q --rebase --autostash origin main >> "$LOG" 2>&1 || log "git pull failed (continuing)"

  # Code first: exhausted, stop, or only render waits need no Claude session (no tokens).
  render_bg
  NEXT="$("$PY" ops/weekend.py next 2>&1)"; NRC=$?
  [ $NRC -eq 3 ] && finish "both queues exhausted: $(echo "$NEXT" | tail -1)"
  [ $NRC -eq 4 ] && finish "STOP file found: stopped cleanly"
  if [ $NRC -ne 0 ]; then log "weekend.py next failed (rc $NRC): $(echo "$NEXT" | tail -3 | tr '\n' ' ')"; ERRS=$((ERRS + 1)); [ $ERRS -ge 6 ] && finish "stopped: weekend.py next failed 6 times running"; sleep 600; continue; fi
  if echo "$NEXT" | head -1 | grep -q '^WAIT-RENDER'; then
    # Nothing but renders left: render now in the foreground (seconds per page), then ask again. Same list unchanged 30 times: stop.
    [ $RPID -ne 0 ] && wait $RPID 2>/dev/null; RPID=0
    "$PY" ops/weekend.py render >> "$LOG" 2>&1
    W_NOW="$(echo "$NEXT" | head -1)"
    if [ "$W_NOW" = "${W_LAST:-}" ]; then RENDER_WAITS=$((RENDER_WAITS + 1)); sleep 60; else RENDER_WAITS=0; fi; W_LAST="$W_NOW"
    log "only render waits ($(echo "$W_NOW" | cut -c1-200)); rendered locally (unchanged round $RENDER_WAITS)"
    [ $RENDER_WAITS -ge 30 ] && finish "stopped: the same pages stayed unrendered for 30 rounds (blocked briefs?)"
    continue
  fi
  RENDER_WAITS=0

  # AlsoAsked key from the keychain for this session only (never printed or written); missing: keep new pages held
  export ALSOASKED_API_KEY="$(security find-generic-password -a "$USER" -s alsoasked -w 2>/dev/null)"
  if [ -z "$ALSOASKED_API_KEY" ]; then
    log "AlsoAsked key missing (keychain service alsoasked, account $USER): new pages held"
    grep -q '"block_new"' "$REPO/status/weekend-run.json" 2>/dev/null || "$PY" ops/weekend.py block-new "AlsoAsked key missing" >> "$LOG" 2>&1
  elif grep -q '"block_new": "AlsoAsked key missing' "$REPO/status/weekend-run.json" 2>/dev/null; then
    "$PY" ops/weekend.py unblock-new >> "$LOG" 2>&1; log "AlsoAsked key found: new-page hold released"
  else
    log "AlsoAsked key found (keychain); new pages $(grep -q '"block_new"' "$REPO/status/weekend-run.json" 2>/dev/null && echo 'held for another reason' || echo 'not held')"
  fi

  N=$((N + 1)); OUT="$RUN/iter-$(date +%Y%m%d-%H%M%S).txt"; BEFORE="$(git rev-parse HEAD)"; START=$(date +%s)
  log "iteration $N start: $(echo "$NEXT" | head -4 | cut -c1-160 | tr '\n' ';')"
  "$PY" ops/guards.py run-locked weekend -- claude -p "$PROMPT" --permission-mode dontAsk \
      --allowedTools "${ALLOWED[@]}" --disallowedTools "${DENIED[@]}" \
      --strict-mcp-config --mcp-config '{"mcpServers":{}}' --settings '{"fastMode": false}' \
      --output-format text > "$OUT" 2>&1 &
  CPID=$!
  while kill -0 $CPID 2>/dev/null; do
    sleep 30; render_bg
    if [ $(( $(date +%s) - START )) -gt $MAX_ITER_SECS ]; then log "iteration $N over 4 hours: stopping it"; pkill -TERM -P $CPID; kill $CPID 2>/dev/null; fi
  done
  wait $CPID; RC=$?
  git pull -q --rebase --autostash origin main >> "$LOG" 2>&1
  TAIL="$(tail -c 600 "$OUT" | tr '\n' ' ')"; MINS=$(( ($(date +%s) - START) / 60 ))
  log "iteration $N end rc=$RC after ${MINS} min: $(echo "$TAIL" | tail -c 300)"

  # Session or weekly limit, or paid usage: decided from the last lines only, when the exit failed or the output is short.
  if [ $RC -ne 0 ] || [ "$(wc -c < "$OUT" | tr -d ' ')" -lt 700 ]; then
    if echo "$TAIL" | grep -qiE 'extra usage|usage credits|paid usage|overage'; then finish "stopped for good: the run reached paid or extra usage ($TAIL)"; fi
    if echo "$TAIL" | grep -qiE 'limit reached|hit your( [a-z-]+)? limit|usage limit|session limit|rate limit|resets? (at )?[0-9]'; then
      W="$(reset_wait "$OUT")"
      [ "$W" = "WEEKLY" ] && finish "stopped for good: weekly limit reached ($TAIL)"
      [ $LIMITED_SINCE -eq 0 ] && LIMITED_SINCE=$(date +%s)
      [ $(( $(date +%s) - LIMITED_SINCE + W )) -gt $LIMIT_GIVEUP_SECS ] && finish "stopped for good: still limited after 7 hours ($TAIL)"
      log "session limit: sleeping $((W / 60)) min (until $(date -v+${W}S '+%a %H:%M'))"; sleep "$W"; continue
    fi
  fi
  if [ $RC -ne 0 ]; then
    ERRS=$((ERRS + 1)); log "iteration $N failed (rc $RC, $ERRS in a row)"
    [ $ERRS -ge 6 ] && finish "stopped: 6 failed iterations in a row (see $OUT)"
    sleep $((ERRS * 300)); continue
  fi
  LIMITED_SINCE=0; ERRS=0
  if [ "$(git rev-parse HEAD)" = "$BEFORE" ]; then IDLE=$((IDLE + 1)); log "iteration $N made no commit ($IDLE in a row)"; else IDLE=0; fi
  [ $IDLE -ge 3 ] && finish "stopped: 3 iterations in a row made no commit (see $OUT)"
done
