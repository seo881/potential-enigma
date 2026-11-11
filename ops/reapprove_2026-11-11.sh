#!/bin/bash
# Divit runs this (DECISIONS 2026-11-11 item 2): re-approve cleaning-quote and massage-booking.
# Both passed their slim review after a fix; their only ship-check failure is R3 (approval fingerprint) / the R3 hold.
set -eu
cd ~/emergent-hubs-a
P=".venv/bin/python3 ops/hubctl.py"
$P go-record "$(date -u +%F)" --urls /ai-form-builder/cleaning-quote,/ai-form-builder/massage-booking \
  --quote 'Divit 2026-11-11: re-approve cleaning-quote and massage-booking (slim reviews passed); run by Divit' --by B-c-1
$P unhold /ai-form-builder/massage-booking --by B-c-1 --reason "Divit re-approved 2026-11-11 (his own command)"
for u in /ai-form-builder/cleaning-quote /ai-form-builder/massage-booking; do $P state "$u" approved --by divit; done
$P ship-check /ai-form-builder/cleaning-quote /ai-form-builder/massage-booking
bash ops/sync.sh "Divit re-approves cleaning-quote and massage-booking (his own command)" \
  status/go/$(date -u +%F).json status/form.json status/hold-lifts.jsonl specs/form/cleaning-quote.json specs/form/massage-booking.json
