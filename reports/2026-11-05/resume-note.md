# Resume note, B, 2026-11-05 (graceful stop; Divit)

FIRST: Divit runs `! bash ops/hero_reapprove.sh` (records his HERO PROMPT FIX go dated TODAY for the 275 URLs in plan/hero-reapprove-urls.txt and re-approves each; the auto-mode classifier refuses this for Claude). Then start ONE ship agent and ONE verifier (brief: reports/2026-11-03/hero-ship-groups.log flow; update path = ship-update/api-update of alpb---prompt + chip adds only, item publish in groups of 10, verify-live, post-ship audit).

## State
- LIVE 417. HERO PROMPT FIX: all 281 template pages rewritten and slim-reviewed (written by B-hp-1..14, reviewed by B-hs-1..3). Shipped: 1 (automotive, verify-live PASS, postship P0 0 P1 0). 275 wait for re-approval. 5 need a separate pre-existing fix first (prompt already reviewed): link-in-bio + waxing-consent (D1 body duplicates), medical-history + audit-workflow (PA12), document-approval-workflow (FAQ flags pending).
- AUDIT 2026-11-04 12:45 UTC (Actions): 417 pages, 280 "real" fails. Expected: A9-prompt / A9-chip drift (spec has the new prompt, live has the old one) on the ~275 unshipped pages; it clears as they ship. The 24 redirect findings are known issues until 2026-11-17.
- The ship agent, verifier and quiz-canary agent died in a network outage (2026-11-03 evening); none is running.

## Done since the 11-03 report (all golden-tested; only the 3 known regressions)
- HERO templates removed from ops/skeleton.py; QC L14 blocks template / two-sentence / same-hub near-duplicate prompts (f53b811b); the 10-09 generic-default ship-check rule retired (7b7c7167). rules/hero_nouns.json is a writer hint only.
- Rework causes 1/7/9 in rework-checklist and both briefs (c9591a3c).
- Queue ranker: pulls found under old slugs; re-rank follows the CURRENT COORDINATOR marker (3d60a5de, 30e9c6f8). Claimable: Form 52, LP 7, Auto 1; SurveyQuiz 47 quizzes ready but blocked by the quiz canary.
- Mac audit retries transport errors on both runners; false A0 held-live fixed (b203bcbc).
- review-claim accepts B-hs-<n> (750d5474).

## Open for Divit
- Run ops/hero_reapprove.sh (above).
- The 5 separate-fix pages: say "fix them".
- Quiz canary: the restage/check + single pre-publish checklist (quiz embed + redirect v2 CSV) was NOT finished (agent died); restart it.
- Rule on the 5 held SurveyQuiz pages (body-type, fun: keep parked; product, questionnaire, user-experience: add the missing library vendors, then release).
- Writing stays stopped until Divit says.
