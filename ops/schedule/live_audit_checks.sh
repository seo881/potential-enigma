#!/bin/bash
# live_audit_checks.sh: Layer A of the live audit as a plain script, no Claude (Divit 2026-10-23). Read-only toward Webflow (HTTP GET/HEAD
# and a headless browser only): no CMS call, no publish of anything.
#   bash ops/schedule/live_audit_checks.sh [--shards 10] [--page-timeout 300] [--base https://emergent.sh] [--shots] [--external]
# 1. `live_audit.py run --all --dry --manifest-only` writes .cache/live/DATE/manifest.json (every live child page in status/live.json, the
#    4 hubs, the held pages);
# 2. the pages are split round-robin into N shards (default 10), each its own manifest and out file, run as parallel `node live_audit.mjs`
#    with a per-page timeout and a watchdog per shard; the held-page sweep runs once (shard 0 only); the hubs run in their own shard;
# 3. pages that failed on a transport error (timeout, http 0, net::ERR_*) are re-run ONCE, serially (capped; LESSONS 2026-10-13);
# 4. the shards are merged into .cache/live/DATE/raw.json and scored by `live_audit.py run --from-raw` -> audits/live/DATE/findings.json;
# 5. plain digest -> audits/live/DATE/digest.txt (counts by severity and code, failing URLs), and a macOS notification with the counts.
# Exit 0 when the checks completed (findings or not), 1 when they could not run. The last stdout line is the counts line.
set -u
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO" || exit 1
PY="$REPO/.venv/bin/python3"; [ -x "$PY" ] || PY=python3
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export EMG_HEADLESS=1   # ruling 19: ops/webflow_api.py refuses CMS writes when set (nothing here calls it; belt and braces)
SHARDS=10; PAGE_TIMEOUT=300; BASE="https://emergent.sh"; SHOTS=0; EXTERNAL=0
while [ $# -gt 0 ]; do case "$1" in
  --shards) SHARDS="$2"; shift 2;; --page-timeout) PAGE_TIMEOUT="$2"; shift 2;; --base) BASE="$2"; shift 2;;
  --shots) SHOTS=1; shift;; --no-shots) SHOTS=0; shift;; --external) EXTERNAL=1; shift;;
  *) echo "unknown option $1" >&2; exit 2;; esac; done
[ "$(date +%u)" = 1 ] && EXTERNAL=1   # external links weekly (Mondays), as live_audit.py
say() { echo "$(date '+%Y-%m-%d %H:%M:%S') checks: $*"; }
notify() { osascript -e "display notification \"${1//\"/\'}\" with title \"Emergent live audit\"" >/dev/null 2>&1; }
fail() { say "FAILED: $*"; notify "Live audit checks FAILED: $*"; exit 1; }
# one run at a time (the daily job and publish_watch.sh can overlap); a lock left by a dead run is taken over
LOCKD="$REPO/.cache/live/checks.lock"; mkdir -p "$REPO/.cache/live"
if ! mkdir "$LOCKD" 2>/dev/null; then
  OP="$(cat "$LOCKD/pid" 2>/dev/null)"
  if [ -n "$OP" ] && kill -0 "$OP" 2>/dev/null; then say "SKIP: another checks run is in progress (pid $OP)"; exit 1; fi
  rm -rf "$LOCKD"; mkdir "$LOCKD" || fail "lock"
fi
echo $$ > "$LOCKD/pid"; trap 'rm -rf "$LOCKD"' EXIT
DATE="$(date +%F)"; CDIR="$REPO/.cache/live/$DATE"; SDIR="$CDIR/shards"; mkdir -p "$SDIR"; rm -f "$SDIR"/*

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

T0=$(date +%s)
"$PY" ops/live_audit.py run --all --dry --manifest-only --base "$BASE" > "$SDIR/manifest.out" 2>&1 || fail "manifest: $(tail -1 "$SDIR/manifest.out")"
# split: N page shards (held sweep only in shard 0) + 1 hub shard
"$PY" - "$CDIR/manifest.json" "$SDIR" "$SHARDS" <<'PY' || fail "sharding"
import json, sys
man = json.load(open(sys.argv[1])); d = sys.argv[2]; n = int(sys.argv[3])
for i in range(n):
    json.dump({"pages": man["pages"][i::n], "hubs": [], "held": man.get("held", []) if i == 0 else [], "held_hosts": man.get("held_hosts")}, open(f"{d}/s{i}.manifest.json", "w"))
json.dump({"pages": man["pages"], "hubs": man["hubs"], "held": [], "held_hosts": man.get("held_hosts")}, open(f"{d}/hubs.manifest.json", "w"))
PY
read -r NPAGES NHUBS NHELD < <("$PY" -c "import json,sys;m=json.load(open(sys.argv[1]));print(len(m['pages']),len(m['hubs']),len(m.get('held',[])))" "$CDIR/manifest.json")
PER=$(( (NPAGES + SHARDS - 1) / SHARDS )); LIMIT=$(( PER * PAGE_TIMEOUT / 3 + 900 ))   # a shard averages well under a third of the page cap
say "start: $NPAGES pages, $NHUBS hubs, $NHELD held pages at $BASE; $SHARDS shards of ~$PER pages, page timeout ${PAGE_TIMEOUT}s, shard watchdog ${LIMIT}s"
for i in $(seq 0 $((SHARDS - 1))); do run_shard "s$i" "$SDIR/s$i.manifest.json" "$SDIR/s$i.raw.json" "$LIMIT" & done
run_shard hubs "$SDIR/hubs.manifest.json" "$SDIR/hubs.raw.json" "$(( NHUBS * PAGE_TIMEOUT * 2 + 600 ))" --hubs-only &
wait
say "shards done in $(( $(date +%s) - T0 ))s: $(tr '\n' ';' < "$SDIR/summary.txt")"

# merge; a shard with no out file (killed) leaves its pages as transport errors
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
NT="$(merge)" || fail "merge"
NRETRY="$NT"
if [ "$NT" -gt 0 ]; then
  say "re-running $NT page(s) that failed on a transport error (once, serially)"
  run_shard retry "$SDIR/retry.manifest.json" "$SDIR/retry.raw.json" "$(( NT * PAGE_TIMEOUT + 300 ))"
  NT="$(merge)" || fail "merge after retry"
fi
[ -s "$CDIR/raw.json" ] || fail "no raw.json"

# score (the same rules as `hubctl live-audit`), then the plain digest
"$PY" ops/live_audit.py run --all --dry --no-shots --base "$BASE" --from-raw "$CDIR/raw.json" > "$SDIR/score.out" 2>&1 || fail "scoring: $(tail -3 "$SDIR/score.out" | tr '\n' ' ')"
"$PY" - "$REPO/audits/live/$DATE/findings.json" "$NRETRY" "$NT" <<'PY'
import json, sys
p = sys.argv[1]; d = json.load(open(p)); d["transport_retried"] = int(sys.argv[2]); d["transport_failed"] = int(sys.argv[3]); d["runner"] = "ops/schedule/live_audit_checks.sh"
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False)
PY
"$PY" ops/live_audit.py plain-digest "$DATE" > "$SDIR/digest.head" 2>&1 || fail "digest: $(tail -1 "$SDIR/digest.head")"
COUNTS="$(sed -n 2,3p "$SDIR/digest.head" | tr '\n' ' ' | sed 's/  */ /g')"
say "done in $(( $(date +%s) - T0 ))s; transport re-checked $NRETRY, still failing $NT; digest audits/live/$DATE/digest.txt"
notify "Checks $DATE: $COUNTS"
echo "COUNTS $DATE: $COUNTS"
exit 0
