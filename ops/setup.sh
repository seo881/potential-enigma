#!/usr/bin/env bash
# One-shot setup for any build-hub chat. Run from the repo root: bash ops/setup.sh [--no-images]
set -e
cd "$(dirname "$0")/.."
echo "[1/5] system fonts (Liberation Sans = Arial metrics, for SERP title widths)"
(apt-get install -y -q fonts-liberation >/dev/null 2>&1 || (apt-get update -q >/dev/null 2>&1 && apt-get install -y -q fonts-liberation >/dev/null 2>&1)) || echo "  warn: fonts-liberation not installed; title pixel check will be skipped"
echo "[2/5] python deps"
pip install -q pandas openpyxl pillow --break-system-packages >/dev/null 2>&1 || true
if [ "$1" != "--no-images" ]; then
  echo "[3/5] image pipeline bootstrap (Inter, Lucide, cairosvg, rsvg)"
  bash pipeline/bootstrap.sh | tail -2
else
  echo "[3/5] image pipeline skipped (--no-images)"
fi
echo "[4/5] keyword map from the Semrush workbook in the Project"
WB=/mnt/project/Emergent_Hub_Child_Pages_Final_v3.xlsx
if [ -f "$WB" ]; then python3 plan/build_map.py "$WB"; else echo "  ERROR: $WB not found. Ask Divit to attach it to the Project."; exit 1; fi
echo "[5/5] QC smoke test on the frozen baselines"
python3 qc/qc_hub.py --all | tail -1
python3 ops/hubctl.py status
echo "SETUP OK"
