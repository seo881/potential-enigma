#!/bin/bash
# Divit runs this (2026-11-05): re-approve the pages fixed under his rulings 1-2 after their slim reviews passed.
# Only R3 (approval fingerprint) blocks them; this records his go and approves each, then commits.
# After it: the ship agent updates the 6 live items (api-update of the changed fields) and item-publishes them,
# and updates patient-intake's existing CMS draft, then publishes it; verify-live and the post-ship audit follow.
set -u
cd ~/emergent-hubs-a || exit 1
URLS="/ai-landing-page-builder/solar /ai-landing-page-builder/telehealth /ai-form-builder/chiropractic-intake /ai-form-builder/acupuncture-intake /ai-form-builder/cleaning-quote /ai-form-builder/coaching-application /ai-automation-builder/patient-intake"
Q='Divit 2026-11-05: rulings 1-2 fixes (health details in transit; cross-field mismatches always blocking) re-approved after independent slim reviews; update and item-publish.'
.venv/bin/python3 ops/hubctl.py go-record "$(date +%F)" --urls "$(echo $URLS | tr ' ' ',')" --quote "$Q" --by B-c-1 | tail -1
for u in $URLS; do .venv/bin/python3 ops/hubctl.py state "$u" approved --by divit 2>&1 | tail -1; done
bash ops/sync.sh "Divit: re-approve 7 rulings-1-2 fixes" status/go/$(date +%F).json status/lp.json status/form.json status/aab.json specs/lp/solar.json specs/lp/telehealth.json specs/form/chiropractic-intake.json specs/form/acupuncture-intake.json specs/form/cleaning-quote.json specs/form/coaching-application.json specs/aab/patient-intake.json | tail -1
