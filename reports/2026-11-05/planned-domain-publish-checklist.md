# Planned domain publish: the one pre-publish checklist (2026-11-05)

Prepared by B-quiz-2 for Divit's item 3 of 2026-11-05. This one emergent.sh publish carries two things: (a) the quiz embed height reservation (already on the template) and (b) the v2 redirect CSV. After it, (c) the canary quizzes are checked and the 47 quizzes become claimable.

**Divit publishes staging and production himself. Claude never publishes the site or a domain, and never imports redirects** (CLAUDE.md, NO SITE PUBLISH, Divit 2026-10-10). Every step marked DIVIT is a click by Divit. Every step marked CLAUDE is a read-only check or a repo change.

## 0. State at 2026-11-05 09:56 UTC (read-only)

- Quiz embed: SurveyQuiz template `6ab24754757025d10940d06a`, HtmlEmbed `117b49c2-044f-e98e-503d-a5470f7713be`, key `code`. The Data API read (get_settings query_settings, 2026-11-05) contains the reservation `body:has(#awb-quiz-data) .emgq-mount{display:block;min-height:438px}` plus the 479 px rule (435 px), as written on 2026-10-23 (logs/sqb.md, report reports/2026-10-23/1504-quiz-embed-cls-reservation.md).
- Staging (emergent-sh.webflow.io) and production (emergent.sh) already serve that embed byte for byte (ops/quiz/embed.min.html, sha256 77032c85af45a950..., 15243 bytes) on /ai-survey-and-quiz-builder/team. **No write was needed and none was made today.** The fix is not waiting for a publish: it is live on both hosts.
- The canary quizzes /ai-survey-and-quiz-builder/style and /vocabulary are CMS drafts: 404 on both hosts.
- CLS on staging, stand-in method (ops/quiz/cls.mjs), 5 runs x 1440 and 390: every run < 0.01. Data: reports/2026-11-05/quiz-cls-before.json. Negative control (reservation cancelled) fails as it should (0.055-0.061 at 1440, 0.0115 at 390): reports/2026-11-05/quiz-cls-negative-control.json.
- Redirects: production serves reports/2026-10-23/redirects-final.csv (843 rows). v2 pre-check against production: 813/843 rows ok, 30 A11-redirect (exactly the 30 changed rows in reports/2026-11-03/redirects-v2-changes.md), 0 A11-target. The v2 condition is met: /ai-landing-page-builder/resume returns 200 on both hosts.

## (a) Quiz height fix: staging CLS proof

1. CLAUDE, before asking: re-read embed `117b49c2` code (Data API, read-only) and confirm it is hash-identical to ops/quiz/embed.min.html (DECISIONS 2026-10-23). If it differs, STOP and report; do not write.
2. DIVIT: publish staging (webflow.io only). (Optional for the quiz: staging already serves the fix. It is needed for (b), so both are proven on staging together.)
3. CLAUDE, after the staging publish:
   ```
   node ops/quiz/cls.mjs --base https://emergent-sh.webflow.io --runs 5 --widths 1440,390 --out reports/<day>/quiz-cls-staging-after.json
   ```
   **Pass bar:** exit 0; every one of the 5 runs at 1440 and the 5 at 390 has CLS < 0.01 for both stand-ins (style, vocabulary); every run played start to restart; mount 438 px at 1440 and 435 px at 390; the control survey page has mount `display:none` and a 0 px gap between hero and section_stats.
4. CLAUDE: `node ops/quiz/cls.mjs --negative --stand style` must FAIL (proves the measure still sees the shift). Exit 3 expected.

## (b) Redirect v2 CSV import

What: `reports/2026-11-03/redirects-final-v2.csv` (843 rows + header `source,target`; 30 rows changed from redirects-final.csv, listed in reports/2026-11-03/redirects-v2-changes.md). Where: Webflow Dashboard > the site > Site settings > Publishing > 301 redirects > Import CSV. The import **replaces every existing 301**, which is intended: v2 already contains all 843 rows (the 553 pre-existing plus the migration's).

Pre-check (CLAUDE, read-only, within the hour before the import):
1. `wc -l reports/2026-11-03/redirects-final-v2.csv` = 844 (843 rows + header); no duplicate sources; every target is a path.
2. `curl -s -o /dev/null -w '%{http_code}' https://emergent.sh/ai-landing-page-builder/resume` = 200 (the v2 condition).
3. `.venv/bin/python3 ops/redirect_check.py check --csv reports/2026-11-03/redirects-final-v2.csv` against production: expect 813 ok, exactly 30 A11-redirect (the 30 changed rows), 0 A11-target. Any other failure: STOP and report.
4. Rollback file ready: reports/2026-10-23/redirects-final.csv (the 843 rows live today).

Import and publish:
5. DIVIT: import the v2 CSV in Site settings (above), then publish staging.
6. CLAUDE: `.venv/bin/python3 ops/redirect_check.py check --base https://emergent-sh.webflow.io --csv reports/2026-11-03/redirects-final-v2.csv` = 843/843, exit 0.
7. CLAUDE: (a) step 3 on the same staging publish.
8. CLAUDE: staged-vs-live sanity (canary safety rule, DECISIONS 2026-10-23): nothing else is pending. Divit confirms with KS that no one else has staged changes.
9. DIVIT: publish emergent.sh, once.

Post-check (CLAUDE, read-only):
10. `.venv/bin/python3 ops/redirect_check.py check --csv reports/2026-11-03/redirects-final-v2.csv` against https://emergent.sh = 843/843, exit 0. If it fails: report; the rollback is Divit re-importing reports/2026-10-23/redirects-final.csv.
11. Repo switch, one commit: in ops/redirect_check.py set `CSV` to reports/2026-11-03/redirects-final-v2.csv (and its docstring); remove the 24 `redir-*` entries from `known_open_issues` in rules/live_audit.json (keep hero-backlog-prompt and hero-backlog-chip-fight); DECISIONS line "v2 imported, <date>". Golden: `.venv/bin/python3 tests/golden/run.py` (only the known regressions).

## (c) Post-publish

1. CLAUDE: full live audit on the Mac runner: `launchctl kickstart -k gui/$(id -u)/sh.emergent.live-audit`; wait for audits/live/last_success.json to update. Pass: 0 A11 findings, no new real fails beyond the known hero-backlog drift; the AUDIT line reported.
2. Canary quizzes (style, vocabulary): they are drafts, so they need an item publish of those 2 items only (publish_collection_items, never a site publish), on Divit's explicit go for those 2 IDs (style 6ad1d94e15d6a1e8ebe0b148 and vocabulary 6ad1d94e15d6a1e8ebe0b146 per the specs; confirm both with a fresh read first). Then:
   - `.venv/bin/python3 ops/hubctl.py verify-live /ai-survey-and-quiz-builder/style` and the same for /vocabulary: PASS (hero prompt, awbQuiz = spec.quiz, embed present);
   - `node ops/quiz/cls.mjs --base https://emergent.sh --direct /ai-survey-and-quiz-builder/style,/ai-survey-and-quiz-builder/vocabulary`: every run < 0.01 at 1440 and 390;
   - play both quizzes at 390 and 1280 (node ops/quiz/test_embed.mjs checks).
   Any fail: unpublish the 2 items (the 2026-10-16 precedent), report.
3. CLAUDE, only when 1 and 2 pass: set `"result": "pass"` in status/quiz-canary.json (with the date and evidence paths), commit. The 47 queued SurveyQuiz quizzes become claimable (`hubctl claim SurveyQuiz`).
