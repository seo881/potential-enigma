# A-g-<n>: standards gate sweep (handover step 2)

Read plan/prompts/README.md. Scope: every page in state images, reviewed, approved or cms_draft (all 4 hubs), every quiz written today, and every page published 2026-11-11 (status/live.json; vocabulary, health-coaching-intake, home-insurance-quote, job-posting and any later ship).

1. Build a read-only script under ops/ (e.g. ops/standards_gate.py) that, per page, reports: slug vs ops/slugs.py spec_problems; hero prompt L13 (rendered lines) and L14 (template, one sentence, same-hub near-duplicate) using qc/qc_hub.py functions; for live pages compare the LIVE item fields (fresh hubctl api-read) not only the spec. Add a golden case under tests/golden for one pass and one fail of each check. Commit.
2. Run it; write counts and the failing list to reports/2026-11-11/standards-gate.md (no raw API responses). Commit + push.
3. Do NOT fix pages yourself. For each failing non-live page: `hubctl hold <url> --by A-g-<n> --note "standards gate: <check>"` so the ship agent cannot ship it. Live failures: list them with the exact field and proposed fix path (ship-update with before-values, item publish, verify-live) for the coordinator.
Return: counts per check and per state, failing URLs with the reason, SHAs.
