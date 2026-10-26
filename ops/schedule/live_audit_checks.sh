#!/bin/bash
# live_audit_checks.sh: Layer A of the live audit as a plain script, no Claude (Divit 2026-10-23). Read-only toward Webflow (HTTP GET/HEAD
# and a headless browser only): no CMS call, no publish of anything. Post-live QC never stops and is never skipped (Divit 2026-10-23).
#   bash ops/schedule/live_audit_checks.sh [--shards 10] [--page-timeout 300] [--base https://emergent.sh] [--shots] [--external]
#        [--urls U,U --run-name NAME]           a partial run (post-ship): audits/live/DATE/NAME/, never over the day's full run
#        [--phase all|manifest|capture|score] [--shard I]   split across machines (GitHub Actions matrix): manifest, then capture
#                                               shard I (or "hubs") on each runner, then score where every s*.raw.json was gathered
# Full run (default):
# 1. `live_audit.py run --all --dry --manifest-only` writes .cache/live/DATE/manifest.json (every live child page in status/live.json, the
#    4 hubs, the held pages);
# 2. the pages are split round-robin into N shards (default 10), each its own manifest and out file, run as parallel `node live_audit.mjs`
#    with a per-page timeout and a watchdog per shard; the held-page sweep runs once (shard 0 only); the hubs run in their own shard;
# 3. pages that failed on a transport error (timeout, http 0, net::ERR_*) are re-run ONCE, serially (capped; LESSONS 2026-10-13);
# 4. the shards are merged into .cache/live/DATE/raw.json and scored by `live_audit.py run --from-raw` -> audits/live/DATE/findings.json;
# 5. plain digest -> audits/live/DATE/digest.txt (counts by severity and code, failing URLs), a macOS notification with the counts, and
#    for a full run audits/live/last_success.json (ops/audit_status.py; the watchdog alerts when it is older than 26 h).
# A second run waits for the first (lock), never skips. Exit 0 when the checks completed (findings or not), 1 when they could not run.
# AUDIT_RUNNER names the runner in last_success.json (default mac:<host>).
set -u
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO" || exit 1
PY="$REPO/.venv/bin/python3"; [ -x "$PY" ] || PY=python3
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
export EMG_HEADLESS=1   # ruling 19: ops/webflow_api.py refuses CMS writes when set (nothing here calls it; belt and braces)
RUNNER="${AUDIT_RUNNER:-mac:$(hostname -s)}"
SHARDS=10; PAGE_TIMEOUT=300; BASE="https://emergent.sh"; SHOTS=0; EXTERNAL=0; URLS=""; RUNNAME=""; PHASE=all; SHARD=""
while [ $# -gt 0 ]; do case "$1" in
  --shards) SHARDS="$2"; shift 2;; --page-timeout) PAGE_TIMEOUT="$2"; shift 2;; --base) BASE="$2"; shift 2;;
  --shots) SHOTS=1; shift;; --no-shots) SHOTS=0; shift;; --external) EXTERNAL=1; shift;;
  --urls) URLS="$2"; shift 2;; --run-name) RUNNAME="$2"; shift 2;; --phase) PHASE="$2"; shift 2;; --shard) SHARD="$2"; shift 2;;
  *) echo "unknown option $1" >&2; exit 2;; esac; done
[ -n "$URLS" ] && [ -z "$RUNNAME" ] && RUNNAME="partial-$(date +%H%M)"
[ "$(date +%u)" = 1 ] && EXTERNAL=1   # external links weekly (Mondays), as live_audit.py
say() { echo "$(date '+%Y-%m-%d %H:%M:%S') checks${RUNNAME:+ [$RUNNAME]}: $*"; }
notify() { command -v osascript >/dev/null && osascript -e "display notification \"${1//\"/\'}\" with title \"Emergent live audit\"" >/dev/null 2>&1; true; }
fail() { say "FAILED: $*"; notify "Live audit checks FAILED: $*"; exit 1; }
# one run at a time per clone (the daily job, publish_watch.sh and post-ship runs can overlap): wait for the other run (up to 3 h),
# never skip; a lock left by a dead run is taken over
LOCKD="$REPO/.cache/live/checks.lock"; mkdir -p "$REPO/.cache/live"
if [ "$PHASE" = all ]; then
  for i in $(seq 1 1080); do
    if mkdir "$LOCKD" 2>/dev/null; then break; fi
    OP="$(cat "$LOCKD/pid" 2>/dev/null)"
    if [ -z "$OP" ] || ! kill -0 "$OP" 2>/dev/null; then rm -rf "$LOCKD"; continue; fi
    [ "$i" = 1 ] && say "waiting for the checks run in progress (pid $OP)"
    [ "$i" = 1080 ] && fail "another checks run (pid $OP) held the lock for 3 h"
    sleep 10
  done
  echo $$ > "$LOCKD/pid"; trap 'rm -rf "$LOCKD"' EXIT
fi
DATE="$(date +%F)"; RDATE="$DATE${RUNNAME:+/$RUNNAME}"; CDIR="$REPO/.cache/live/$RDATE"; SDIR="$CDIR/shards"; mkdir -p "$SDIR"
SEL=(--all); [ -n "$URLS" ] && SEL=(--urls "$URLS")
NAMEARG=(); [ -n "$RUNNAME" ] && NAMEARG=(--run-name "$RUNNAME")

# run one shard under a watchdog: node is killed after LIMIT seconds (its pages then count as transport errors and are re-run)
run_shard() {   # name manifest out limit [extra args]
  local name="$1" man="$2" out="$3" limit="$4"; shift 4
  local extra=(); [ "$SHOTS" = 1 ] && extra+=(--shots "$CDIR"); [ "$EXTERNAL" = 1 ] && extra+=(--external)
  node ops/live_audit.mjs "$man" "$out" --base "$BASE" --page-timeout "$PAGE_TIMEOUT" ${extra[@]+"${extra[@]}"} "$@" > "$SDIR/$name.log" 2>&1 &
  local pid=$!
  ( sleep "$limit"; kill -0 "$pid" 2>/dev/null && { echo "watchdog: killed after $limit s" >> "$SDIR/$name.log"; pkill -TERM -P "$pid" 2>/dev/null; kill -TERM "$pid" 2>/dev/null; } ) >/dev/null 2>&1 &
  local wd=$!
  wait "$pid"; local rc=$?
  kill "$wd" 2>/dev/null; wait "$wd" 2>/dev/null
  echo "$name rc=$rc $(grep -c '^FAIL\|^ok' "$SDIR/$name.log" 2>/dev/null) lines" >> "$SDIR/summary.txt"
}
shard_limit() { local n="$1"; echo $(( n * PAGE_TIMEOUT / 3 + 900 )); }   # a shard averages well under a third of the page cap

T0=$(date +%s)
# ---- manifest + split ----
if [ "$PHASE" = all ] || [ "$PHASE" = manifest ]; then
  rm -f "$SDIR"/*
  "$PY" ops/live_audit.py run "${SEL[@]}" ${NAMEARG[@]+"${NAMEARG[@]}"} --dry --manifest-only --base "$BASE" > "$SDIR/manifest.out" 2>&1 || fail "manifest: $(tail -1 "$SDIR/manifest.out")"
  "$PY" - "$CDIR/manifest.json" "$SDIR" "$SHARDS" <<'PY' || fail "sharding"
import json, sys
man = json.load(open(sys.argv[1])); d = sys.argv[2]; n = int(sys.argv[3])
for i in range(n):
    json.dump({"pages": man["pages"][i::n], "hubs": [], "held": man.get("held", []) if i == 0 else [], "held_hosts": man.get("held_hosts")}, open(f"{d}/s{i}.manifest.json", "w"))
json.dump({"pages": man["pages"], "hubs": man["hubs"], "held": [], "held_hosts": man.get("held_hosts")}, open(f"{d}/hubs.manifest.json", "w"))
PY
fi
[ -s "$CDIR/manifest.json" ] || fail "no manifest at $CDIR/manifest.json"
read -r NPAGES NHUBS NHELD < <("$PY" -c "import json,sys;m=json.load(open(sys.argv[1]));print(len(m['pages']),len(m['hubs']),len(m.get('held',[])))" "$CDIR/manifest.json")
[ "$NPAGES" -gt 0 ] || fail "manifest lists 0 pages"
[ "$PHASE" = manifest ] && { say "manifest: $NPAGES pages, $NHUBS hubs, $NHELD held; $SHARDS shards in $SDIR"; exit 0; }
PER=$(( (NPAGES + SHARDS - 1) / SHARDS ))

# ---- capture ----
if [ "$PHASE" = capture ]; then   # one shard on this machine
  if [ "$SHARD" = hubs ]; then run_shard hubs "$SDIR/hubs.manifest.json" "$SDIR/hubs.raw.json" "$(( NHUBS * PAGE_TIMEOUT * 2 + 600 ))" --hubs-only
  else run_shard "s$SHARD" "$SDIR/s$SHARD.manifest.json" "$SDIR/s$SHARD.raw.json" "$(shard_limit "$PER")"; fi
  say "capture shard $SHARD done in $(( $(date +%s) - T0 ))s: $(tail -1 "$SDIR/summary.txt")"; exit 0
fi
if [ "$PHASE" = all ]; then
  say "start: $NPAGES pages, $NHUBS hubs, $NHELD held pages at $BASE; $SHARDS shards of ~$PER pages, page timeout ${PAGE_TIMEOUT}s, shard watchdog $(shard_limit "$PER")s; runner $RUNNER"
  for i in $(seq 0 $((SHARDS - 1))); do run_shard "s$i" "$SDIR/s$i.manifest.json" "$SDIR/s$i.raw.json" "$(shard_limit "$PER")" & done
  [ "$NHUBS" -gt 0 ] && run_shard hubs "$SDIR/hubs.manifest.json" "$SDIR/hubs.raw.json" "$(( NHUBS * PAGE_TIMEOUT * 2 + 600 ))" --hubs-only &
  wait
  say "shards done in $(( $(date +%s) - T0 ))s: $(tr '\n' ';' < "$SDIR/summary.txt")"
fi

# ---- score: merge; a shard with no out file (killed, or a matrix job that failed) leaves its pages as transport errors ----
merge() { "$PY" - "$CDIR/manifest.json" "$SDIR" "$SHARDS" "$CDIR/raw.json" "$BASE" <<'PY'
import json, os, sys, datetime
man = json.load(open(sys.argv[1])); d = sys.argv[2]; n = int(sys.argv[3]); out = sys.argv[4]
raw = {"base": sys.argv[5], "date": datetime.datetime.now(datetime.timezone.utc).isoformat(), "sitemap_ok": False, "pages": [], "hubs": [], "held": []}
got = {}
for name in [f"s{i}" for i in range(n)] + ["hubs", "retry"]:
    p = f"{d}/{name}.raw.json"
    if not os.path.exists(p): continue
    r = json.load(open(p)); raw["sitemap_ok"] = raw["sitemap_ok"] or r.get("sitemap_ok", False)
    for pg in r["pages"]:
        if name == "retry" or pg["url"] not in got or got[pg["url"]].get("transport_error"): got[pg["url"]] = pg
    raw["hubs"] += r["hubs"]; raw["held"] += r["held"]
for p in man["pages"]:
    if p["url"] not in got: got[p["url"]] = {"url": p["url"], "checks": {"http200": False}, "verify": {"http": 0}, "transport_error": "shard did not finish (watchdog)"}
raw["pages"] = [got[p["url"]] for p in man["pages"]]
json.dump(raw, open(out, "w"))
bad = [p["url"] for p in raw["pages"] if p.get("transport_error")]
json.dump({"pages": [p for p in man["pages"] if p["url"] in bad], "hubs": [], "held": []}, open(f"{d}/retry.manifest.json", "w"))
print(len(bad))
PY
}
rm -f "$SDIR/retry.raw.json"
NT="$(merge)" || fail "merge"
NRETRY="$NT"
if [ "$NT" -gt 0 ]; then
  say "re-running $NT page(s) that failed on a transport error (once, serially)"
  run_shard retry "$SDIR/retry.manifest.json" "$SDIR/retry.raw.json" "$(( NT * PAGE_TIMEOUT + 300 ))"
  NT="$(merge)" || fail "merge after retry"
fi
[ -s "$CDIR/raw.json" ] || fail "no raw.json"

# score (the same rules as `hubctl live-audit`), then the plain digest
"$PY" ops/live_audit.py run "${SEL[@]}" ${NAMEARG[@]+"${NAMEARG[@]}"} --dry --no-shots --base "$BASE" --from-raw "$CDIR/raw.json" > "$SDIR/score.out" 2>&1 || fail "scoring: $(tail -3 "$SDIR/score.out" | tr '\n' ' ')"
"$PY" - "$REPO/audits/live/$RDATE/findings.json" "$NRETRY" "$NT" "$RUNNER" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p)); d["transport_retried"] = int(sys.argv[2]); d["transport_failed"] = int(sys.argv[3])
d["runner"] = f"ops/schedule/live_audit_checks.sh on {sys.argv[4]}"
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False)
PY
"$PY" ops/live_audit.py plain-digest "$RDATE" > "$SDIR/digest.head" 2>&1 || fail "digest: $(tail -1 "$SDIR/digest.head")"
COUNTS="$(sed -n 2,3p "$SDIR/digest.head" | tr '\n' ' ' | sed 's/  */ /g')"
if [ -z "$URLS" ]; then "$PY" ops/audit_status.py success "$DATE" "$RUNNER" > /dev/null || fail "last_success.json"; fi
say "done in $(( $(date +%s) - T0 ))s; transport re-checked $NRETRY, still failing $NT; digest audits/live/$RDATE/digest.txt"
REAL="$("$PY" ops/audit_status.py real "$REPO/audits/live/$RDATE/findings.json" 2>&1)"; RRC=$?
say "$REAL"
# Divit 2026-10-26: alert only on REAL failures after exceptions (known open issues excluded); P2 stays in the report
[ $RRC -eq 3 ] && notify "Checks ${RUNNAME:-$DATE}: $REAL"
echo "COUNTS $RDATE: $COUNTS"
exit 0
