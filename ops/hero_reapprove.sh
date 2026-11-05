#!/bin/bash
# HERO PROMPT FIX re-approval (Divit runs this; the auto-mode classifier refused it for Claude, 2026-11-03).
# Records Divit's go for the slim-reviewed pages whose ONLY ship-check failure is R3 (approval fingerprint), then re-approves each.
# Input: reapprove.txt (275 URLs from all 14 batches; excluded: automotive (already re-approved), link-in-bio + waxing-consent (pre-existing D1),
# medical-history + audit-workflow (PA12), document-approval-workflow (flags pending)).
set -u
cd ~/emergent-hubs-a || exit 1
F=plan/hero-reapprove-urls.txt
Q='HERO PROMPT FIX (Divit, 2026-11-03): "Replace the template default prompts on ALL pages, live and in the pipeline, across all 4 hubs, with page-specific ones ... Each page gets a slim review of only the prompt fields by an independent reviewer, then an API update, item publish (groups of 10) and verify-live." Hero prompt fields only; slim review passed.'
.venv/bin/python3 ops/hubctl.py go-record "$(date +%F)" --urls "$(paste -sd, "$F")" --quote "$Q" --by B-c-1 | tail -1
n=0; f=0
while read -r u; do
  if .venv/bin/python3 ops/hubctl.py state "$u" approved --by divit >/dev/null 2>&1; then n=$((n+1)); else f=$((f+1)); echo "FAIL $u"; fi
done < "$F"
echo "approved $n, failed $f"
bash ops/sync.sh "HERO PROMPT FIX: re-approve $n slim-reviewed pages on Divit's go (all batches)" status/go/$(date +%F).json status/lp.json status/form.json status/sqb.json status/aab.json $(sed 's#/ai-landing-page-builder/#specs/lp/#; s#/ai-form-builder/#specs/form/#; s#/ai-survey-and-quiz-builder/#specs/sqb/#; s#/ai-automation-builder/#specs/aab/#; s#$#.json#' "$F") | tail -1
