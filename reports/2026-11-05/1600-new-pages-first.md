# 2026-11-05 new pages live first (B-c-1)

## Request
Divit (pasted): "Priority (Divit): new pages live first. The hero-prompt rewrite for the ~275 live pages is ON HOLD as backlog (incl. the 14 polish items); don't ship any of it until I say. 1. Resume writing at full throttle on the claimable pages: Form 52, LP 7, Automation 1. ... 2. Independent reviews as pages land; ship each the moment it passes (standing go for 0-flag pages recorded with go-record; groups of 10; verify-live in parallel; post-ship audit). Flags to me in one packet. 3. Quiz unblock in parallel ... 4. Weekly: 20% (from /usage). Stop new claims at 40%. Before any session limit: commit and write a resume note."
Then: "only 10 percent of session limit remaining, pause all writing gracefully, and focus on taking as many pages live as possible"

## Actions and results
- Claimed Form 52, LP 7, Auto 1 (5d252b92). Standing go for new 0-flag pages: .cache/standing-go-2026-11-05, recorded per page in status/go/2026-11-05.json.
- 41 writers launched (B-w-405..443 plus 6 rework writers B-w-465..472); 22 pages written; 21 full reviews and 8 slim reviews (B-r-420..439, B-hs-10..17).
- Review results: 13 passed first time; 8 went to rework (solar, patient-intake, case-study, dj-booking, short-form, construction-quote, spa, employee-training), all 8 fixed and passed slim review. Top rework cause: features_subheading claiming all six features (5 pages) -> new QC L15.
- 19 pages pass ship-check; ship agent B-ship-7 published LP g1 (yoga, telehealth, tiktok; verify-live 3/3, 7075fcfc) and is shipping the rest (see reports/2026-11-05/ship-run.md).
- Writing paused at Divit's 10% message: 19 writers stopped; their partial specs committed (1ca42d57), states claimed/spec.
- Quiz unblock (B-quiz-2): the height fix was already live on staging and production (no write); CLS proof passes (max 0.0025 < 0.01; negative control fails as expected); checklist reports/2026-11-05/planned-domain-publish-checklist.md (adfc1816).

## Numbers
LP 7/7 written; Form 15 of 52 written; Auto 1/1 written. Live 417 -> 420+ (ship-run.md has the final count).

## Decisions
- Hero backlog drift in the audit (A9-prompt / A9-chip-fight, 280 URLs) registered as known until 2026-11-19, scoped to plan/hero-backlog-urls.txt (new urls_file key; golden 4 cases; eaaeab07). Follows Divit 2026-11-05 "ON HOLD as backlog".
- Hyphenation in code-built text: rules/keyword_forms.json + skeleton.case_forms (short-form, walk-through, Little League...; golden 7; 76e366ca). Follows Divit 2026-11-05 "correct hyphenation and the exact keyword".
- Coordinator unlocks (logged on each spec): solar feature_4/howto_step_4_des, case-study howto_step_6_des, spa howto_step_4_des/image_brief (finding text named them; the review lock reads only the field key), short-form hyphenation fields.
- QC L15 (new writing only, never-reviewed specs): features subheading claiming something of all six features. ~140 reviewed/live specs use the pattern and are deliberately not rechecked.

## Files changed and commits
eaaeab07, 5d252b92, d3813977, 5424eb80, 499b71e0, 76e366ca, 1ca42d57 (+ writer/reviewer/ship commits in git log for 2026-11-05).

## Webflow calls
All by B-ship-7 (item creates and item publishes only; before-values in childedits/2026-11-05/, logs/lp.md, logs/form.md, logs/aab.md). No site publish. Quiz agent: read-only.

## Not done
- 37 Form pages unwritten (19 partial specs + 18 never started); hero backlog on hold; QC L15 commit pending its golden run if not in git log.

## Open questions for Divit
1. Health details in chat: the patient-intake automation shows a patient's allergy sent by Slack/DM; no rule covers it. Blocking on healthcare pages?
2. Severity calibration: timing/number mismatches between fields were blocking on case-study but notes on benefits-enrollment and bankruptcy-intake. Always blocking?
3. Quiz: import redirects-final-v2.csv, then your one planned domain publish; then a go to item-publish style and vocabulary, which unlocks the 47 quizzes.
