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
  .venv/bin/pip install -q --upgrade pip >/dev/null 2>&1; .venv/bin/pip install -q pandas openpyxl pillow >/dev/null 2>&1
  PY=.venv/bin/python3; set -- --no-images
  echo "  macOS: using .venv (run every repo command as .venv/bin/python3 ...)"
else
  pip install -q pandas openpyxl pillow --break-system-packages >/dev/null 2>&1 || true
fi
if [ "$1" != "--no-images" ]; then
  echo "[3/5] image pipeline bootstrap (Inter, Lucide, cairosvg, rsvg)"
  bash pipeline/bootstrap.sh | tail -2
else
  echo "[3/5] image pipeline skipped (--no-images; on macOS the image stage runs in a Linux session until the recipe library is ported)"
fi
echo "[4/5] keyword map from the Semrush workbook in the Project"
WB=${WB:-}
for c in /mnt/project/Emergent_Hub_Child_Pages_Final_v3.xlsx private/Emergent_Hub_Child_Pages_Final_v3.xlsx; do [ -z "$WB" ] && [ -f "$c" ] && WB=$c; done
if [ -n "$WB" ] && [ -f "$WB" ]; then $PY plan/build_map.py "$WB"; else echo "  ERROR: Semrush workbook not found (Claude.ai: attach to the Project; Claude Code: put it in private/)."; exit 1; fi
echo "[5/5] QC smoke test on the frozen baselines"
$PY qc/qc_hub.py --all | tail -1
$PY ops/hubctl.py status
echo "SETUP OK"
