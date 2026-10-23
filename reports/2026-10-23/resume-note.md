# Resume note, B, 2026-10-23 (graceful stop by Divit)

Live: 339. Account A is paused; B covers all 4 hubs. The post-live QC launchd job stays loaded (permanent rule; never pause it).

## FIRST on resume
1. Read `hubctl audit-status` if it exists, otherwise audits/live/2026-10-23/. The last full audit (2026-10-23, commit 5b93bc09) found 327 pages with 0 real failures:
   - G1 (template, all pages): navbar /ai-contests svg width="2o". Divit picks: (a) fix "2o" to "20" in the Designer plus his site publish (recommended), or (b) widen the console exception.
   - G2: Learn card title "AI Workflow Builders in 2026 – Expert Picks" (en dash) on 41 Automation pages. Divit picks: the blog owner retitles it, or a ref swap on 41 pages (his go).
   - G3: 3 transient image-load results, no fix. G4: P2 backlog.
2. SHIPPING IS HELD until Divit says resume. About 39 pages are reviewed or approved and pass ship-check (rerun ship-check first). Ship with scratchpad ship5.sh per hub, explicit args (LP lp, Auto aab, Form form, SurveyQuiz sqb), in groups of 5 with verify-live.
   - Approvals under "Divit 2026-10-23 go": the standing go for 10-21 has expired; ask Divit for a fresh go on the new date.
3. NO new claims until Divit resumes them. Claim stop at about 45% weekly, hard stop 50% (32%+ when stopped).

## Mid-flight at the stop (check the agents' final commits)
- Quiz canary (B-dev-23), STOPPED AFTER STAGING PROOF: embed read-back and the staging-served embed are hash-identical to ops/quiz/embed.min.html (sha256 77032c85...). Staging CLS: all runs under 0.01 (max 0.00059 at 1440, 0.00078 at 390, both quizzes). Survey page: 0 px, no blank block (7720b644). NEXT: the production canary as planned (style-quiz item publish + verify-live + production CLS, then vocabulary-quiz). Divit already approved it if staging passes, which it did. Earlier detail: the embed min-height fix is staged (bcefdfde, 76ca6c7a) and Divit published staging. Steps: hash-verify the read-back, then CLS on staging, then the production canary (style-quiz, then vocabulary-quiz). See status/quiz-canary.json and logs/sqb.md for how far it got. If it is "pass", SurveyQuiz quiz pages (47) become claimable.
- Skip-proof audit (B-dev-20): the launchd stable path, GitHub Actions backup, post-ship and post-publish hooks, a 26h watchdog, and `hubctl audit-status` for the AUDIT field in the report block. Check its last commit for what is done.

## Rules added today (DECISIONS 2026-10-23)
- SCIM C2 exception; mental-health and laser Q1 (PA7) approved; PA12 skips "pdf" secondaries unless PDF is the subject; PA14 crossfit; acronyms NFT, HVAC, 5K; account A paused; post-live QC permanent; quiz embed rule is quiz-pages-only.

## Fixes logged, not done
- The skeleton default LP hero prompt "saves every signup" is on 56 LP specs, live ones included, and misfits service, shop and news pages. Per-hub rewrite plan for Divit (it touches many live pages).
- The related-link picker gives off-topic sibling links. Learn library gaps (yoga, studio, training).
