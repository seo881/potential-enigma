# Close-out 2026-11-17: hero-prompt backlog, health sweep, loose ends, redirects (B-c-2)

## Request
Divit's close-out: "1. Read the airline-questions re-run ... 2. Hero-prompt backlog: resume it NOW ... Ship via ship-update in groups, with verify-live, auto re-approval after a passing slim review, and restamp ... 3. Redirects ... 4. Loose ends ... 5. Final report", plus follow-ups the same day: advisor's 14 polish fixes, hyphen consistency, the health-data sweep of all live pages, F6 rulings, write-once and restamp gates, the redirect ruling (24 pre-existing targets permanent), "Go: resume all live writes".

## Actions and results
- Hero-prompt backlog: 280/280 prompts live and restamped. 217 shipped in 10 groups (212 + 4 advisor pages separately + document-approval after its flag swap); 63 needed fixes (cross-field mismatches, hub word, hyphenation, health data in chips), all slim-reviewed (one rework each where blocking) before shipping.
- Advisor polish (14): all applied; hyphen alignment page-wide on low-stock-alert, click-through, post-webinar, post-event, product-market-fit, quote-to-cash, safety/bathroom/meet-the-teacher sign-in sheets, potluck/club sign-up sheets, win-loss, post-purchase, high-converting; wedding-rsvp "form"; vendor-application exact keyword; interactive names its calculator.
- Health sweep (177 candidate live pages judged; 34 fixed + 3 borderlines Divit ruled to fix): every named person's health/accommodation detail now stays in the app; messages carry counts or "needs review". 37 pages live, verify-live PASS, restamped.
- Loose ends: Likert / QR code capitalisation (9 pages), dangling phrases after link removal (4 pages), wellness-quiz guest coordinator; all live and restamped.
- Redirects: the 24 pre-existing broken targets are permanent known issues (no expiry); daily check pins the 843-row list (P0 A11-list on any change); our 290 migration redirects stay fully monitored; site-publish checklist has no redirect import and no font fix (not staged).
- Gates added (all golden-tested): image slot map; write-once childedits + SYNC_RUN; restamp_refusal (go record alone never restamps; review + QC + verify-live); F6 only for AlsoAsked questions added or changed in the edit; yes-or-no keyword variant; Q6 counts keyword_forms variants; FAQ assembler never double-wraps links; LinkedIn 403 known exception.

## Numbers
Live 646 (LP 119, Form 285, Auto 98, SurveyQuiz 144). Hero backlog 280/280 live + restamped. Health 37/37 live + restamped. Golden 1270+ cases, 0 regressions at last full run.

## Decisions
Every rule above cites Divit 2026-11-16/17 in its commit and in rules/ or ops/ code comments.

## Files changed and commits
See git log 2026-11-17 (key: 1b2e60ec, 35b1608b, e6a2c662, 2c0bde42, f6344bd5, 26c936f7, 19c36541, e6401b0d, f2be6cf2).

## Webflow calls
Item updates + item publishes only, via hubctl api-update from ship-update payloads; rollbacks in childedits/2026-11-17/*.rollback.json; no site publish.

## Not done
None of the hero/health scope. The hero-backlog known-issue entries (expire 2026-11-19) can be removed after the next full audit confirms 0 A9 findings.

## Open questions for Divit
None blocking.
