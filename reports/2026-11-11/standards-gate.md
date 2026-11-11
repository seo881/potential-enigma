# Standards gate sweep (A-g-2), 2026-11-11

## Request
Gate sweep per plan/prompts/gate.md; Divit's newest ruling: gate failures go to rework, never ship (hubctl hold, list for rework). Finish A-g-1's ops/standards_gate.py, add golden cases. Priority: 9 pages about to ship (written first to status/gate-2026-11-11.json), then images, then today's live pages.

## Actions and results
- ops/standards_gate.py finished (check_page pure function; scope fixed: pages already live are in scope only when published today, not every live page; skeleton quizzes (state spec) excluded; --only, --gate-file added). Reads: fresh hubctl api-read of all 4 hubs at 10:41 UTC.
- Checks: SLUG (ops/slugs.py spec_problems + CMS slug/H1), L13 (rendered prompt lines), L14 (template, one sentence, same-hub near-duplicate; HERO PROMPT FIX bar). For items in the CMS the item's own slug/H1/hero prompt are checked.
- 9 pre-ship pages (painting-quote, password-reset, podcast-application, massage-booking, photo-contest, cleaning-quote, friendship, product-recommendation, career): all PASS, committed 239c8953.
- Full sweep: 38 pages in scope (+cleaning-quote = 39 entries in status/gate-2026-11-11.json). Per state: Form published 3, cms_draft 5, images 11, reviewed 4; SurveyQuiz published 1, reviewed 5, images 8, rework 1.
- Counts per check (of 38 in scope): SLUG fail 0, L13 fail 0, L14 fail 0. 35 PASS. 3 NOSPEC (could not be gated).
- Today's live pages (vocabulary, health-coaching-intake, home-insurance-quote, job-posting): PASS on live item fields.
- No holds placed: no page failed a check.
- Golden: kind standards-gate, 6 cases (sg-pass, sg-slug-fail, sg-h1-keyword-fail, sg-cms-slug-mismatch-fail, sg-l14-template-fail, sg-l14-two-sentences-fail). All pass. The golden run also shows 2 unrelated REGRESSION lines (coord-b-c-in-b, pa9-donation-q9-still-rejected), not touched here (coordinator marker is now A; pre-existing).

## Decisions
- Live pages published before today are out of scope (older pages predate L14 and are for hubctl recheck / fix_queue): DECISIONS 2026-11-11 handover scope, gate.md.

## Not done / open
- NOSPEC: speech-therapy-intake, love-language, personality (state images): spec file is not on main (writer branch b-wip-2026-11-11); cannot be gated until reconciled. Not held (A-r reviewers hold claims on them); the gate must be rerun once their specs land.
- brand, coffee (state spec, skeletons) not gated; gate when written.
