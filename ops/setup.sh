#!/usr/bin/env bash
# One-shot setup for any build-hub chat. Run from the repo root: bash ops/setup.sh [--no-images]
set -e
cd "$(dirname "$0")/.."
echo "[1/5] system fonts (Liberation Sans = Arial metrics, for SERP title widths)"
(command -v apt-get >/dev/null && apt-get install -y -q fonts-liberation >/dev/null 2>&1 || (apt-get update -q >/dev/null 2>&1 && apt-get install -y -q fonts-liberation >/dev/null 2>&1)) || echo "  warn: fonts-liberation not installed; title pixel check will be skipped"
echo "[2/5] python deps"
PY=python3
if [ "$(uname)" = "Darwin" ]; then
  # macOS (Claude Code on Divit's machine): isolated venv, Arial for SERP widths, image stage elsewhere until it is ported
  [ -d .venv ] || python3 -m venv .venv
  .venv/bin/pip install -q --upgrade pip >/dev/null 2>&1
  .venv/bin/pip install -q pandas openpyxl pillow uharfbuzz fonttools brotli resvg-py >/dev/null 2>&1 || { echo "  ERROR: pip install failed"; exit 1; }
  PY=.venv/bin/python3
  echo "  macOS: using .venv (run every repo command as .venv/bin/python3 ...)"
else
  pip install -q pandas openpyxl pillow uharfbuzz fonttools brotli resvg-py --break-system-packages >/dev/null 2>&1 || true
fi
if [ "$1" != "--no-images" ]; then
  echo "[3/5] image engine: pinned assets (Inter 4.1, Lucide 1.52.0) and a smoke render of the 16 reference scenes"
  if [ "$(uname)" = "Darwin" ] || [ ! -d /root ]; then $PY pipeline/assets.py; else bash pipeline/bootstrap.sh | tail -1; $PY -c "import sys; sys.path.insert(0,'pipeline'); import assets; assets.brockmann()"; fi
  $PY -c "import json,sys; sys.path.insert(0,'ops'); import typeset as T; m=T.mode(); c=json.load(open('config/typography.json')).get('ceilings',{}); sys.exit(0 if m in c else 1)" || $PY ops/typeset.py calibrate
  echo "  typography: $($PY ops/typeset.py fonts)"
  $PY pipeline/engine.py lint pipeline/briefs/*.json | grep -E "^(OK|BLOCKED)" | sed 's/^/  /'
else
  echo "[3/5] image engine skipped (--no-images)"
fi
echo "[4/5] keyword map from the Semrush workbook in the Project"
WB=${WB:-}
for c in /mnt/project/Emergent_Hub_Child_Pages_Final_v3.xlsx private/Emergent_Hub_Child_Pages_Final_v3.xlsx; do [ -z "$WB" ] && [ -f "$c" ] && WB=$c; done
if [ -n "$WB" ] && [ -f "$WB" ]; then $PY plan/build_map.py "$WB"; else echo "  ERROR: Semrush workbook not found (Claude.ai: attach to the Project; Claude Code: put it in private/)."; exit 1; fi
echo "[5/5] QC smoke test on the frozen baselines"
$PY qc/qc_hub.py $($PY -c "import json,glob; print(' '.join(p for p in glob.glob('specs/*/*.json') if json.load(open(p)).get('status')=='live-draft'))") | tail -1
$PY ops/hubctl.py status
echo "SETUP OK"
