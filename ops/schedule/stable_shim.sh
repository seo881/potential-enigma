#!/bin/bash
# stable_shim.sh: the ONE stable launchd entry point for post-live QC (Divit 2026-10-23: launchd from a stable path, independent of
# clone or account, alerting if the repo path is missing). Installed copy: ~/Library/Application Support/emergent/run.sh.
# Usage: run.sh <script relative to the repo> [args]. The repo is read from ~/Library/Application Support/emergent/repo (one line, an
# absolute clone path), written at each coordinator handover; if that is missing or not a clone, the first existing of
# ~/emergent-hubs-a and ~/emergent-hubs is used. When none exists: a macOS alert and exit 1 (never a silent skip).
set -u
D="$HOME/Library/Application Support/emergent"; LOG="$HOME/Library/Logs/emergent-stable-shim.log"
REPO="$(head -1 "$D/repo" 2>/dev/null)"
if [ -z "$REPO" ] || [ ! -f "$REPO/ops/audit_status.py" ]; then
  REPO=""; for c in "$HOME/emergent-hubs-a" "$HOME/emergent-hubs"; do [ -f "$c/ops/audit_status.py" ] && { REPO="$c"; break; }; done
fi
if [ -z "$REPO" ]; then
  echo "$(date '+%F %T') NO REPO for $*" >> "$LOG"
  osascript -e 'display notification "No emergent-hubs clone found: post-live QC cannot run" with title "emergent.sh live audit ALERT" sound name "Basso"' >/dev/null 2>&1
  exit 1
fi
echo "$(date '+%F %T') $REPO: $*" >> "$LOG"
exec /bin/bash "$REPO/$1" "${@:2}"
