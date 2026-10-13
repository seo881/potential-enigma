# Learn correction applied, batch 3 written and QC-clean, two-account protocol pushed (interim: batch 3 not yet in the CMS)

## Digest for Divit
- **docs/TWO_ACCOUNTS.md is pushed** (fa071de8, plus a batch-hold rule in fabcde3a).
  - Account A had already started: its commit 075d9a83 reworked 4 pages that were in my batch 3.
  - A's versions are kept. I added the unique-name sweep they were missing.
  - New rule in the doc: pages listed in a B batch file are B's.
- **Learn:**
  - Source untouched.
  - Card link: Form, LP and Automation read back `detail_learn`; Survey is now set to it too (read back).
  - acrm---learn now holds your 3 articles on all 39 other live items (field only, no item publish; 39/39 in the update responses).
- **Batch 3:** 20 pages, all at QC 0 and gate 10/10, with chip_adds, unique names and images re-rendered (contact sheets read).
  - Not yet in the CMS: moving the 16 pages to `reviewed` was blocked by the auto-mode permission check (see Not done).
- **Unhide for staging:** done (11 sections, read back), then **re-hidden at once and read back** because batch 3 isn't staged yet. Nothing is unhidden now. I unhide again right before asking you to publish staging.

## Request
> (1) Learn: correct design, DECISIONS line + docs; Survey blog_link; fill acrm---learn on the other 39 live pages, no item publish; L12 rule. (2) Today's 20 (batch 3): pick, re-check, create with Learn refs, verify 20/20, isDraft false. (3) Unhide for staging, then "Publish to staging only now". (4) Verify after staging, etc. (5) Part C.
> Follow-up: "unhide for staging, yes, on one condition: unhide, publish STAGING ONLY, run the checks, then re-hide immediately whether or not they pass, and read back the hide before anything else happens. No production publish while anything is unhidden." Plus: push docs/TWO_ACCOUNTS.md before A starts; then a throughput plan.

## Actions and results
- **Before-values first:** committed and pushed in ab499153, before any write:
  - the Survey link;
  - visibility on 11 sections;
  - acrm---learn on 39 items.
- **Learn card link:** Form, LP and Automation read back `{collectionPage, detail_learn}` (the advisor's writes). Survey is set and read back.
- **Learn refs:** 3 update calls (Form 15, LP 9, Auto 9, SQB 6 items). The update responses show the 3 refs on 39/39.
- **Batch 3** (`plan/batches/batch-3.txt`): the highest total MSV among the 61 reviewed weekend pages, hubs mixed (Form 10, LP 4, SurveyQuiz 4, Automation 2, which is all the reviewed Automation pages), link clusters kept together.
  - Four writer agents with disjoint name-letter pools fixed L11 (chip_adds, 20/20), A1 stock and reused names, and J1 (splash-page).
  - The images were re-rendered and every contact sheet read.
- **Account A overlap:** A's commit 075d9a83 took consent-form, photo-release-form, ach-form and social-media-automation to `reviewed` while my writers were on them.
  - I kept A's versions.
  - A had left reused personas (e.g. a name on 10 other specs), so I applied the unique-name swaps, re-rendered and read the 4 sheets.
- **Final check, 20/20:** QC 0, gate (10, 10, no page problems), 4 chip_adds, images current. Name sweep: no person or business name shared with any other spec.
- **Unhide:** 11 set visible and read back; then 11 hidden again and read back. The staging site was never published in between.

## Numbers
- Webflow writes: 1 link, 39 CMS field updates (3 calls), 11 unhides, 11 re-hides. Reads for every one. No publish of any kind.
- Tokens, writer pass on batch 3: 589k in total, about 29k per page (status/usage.jsonl). This was a fix pass, not a full write.

## Decisions
- **Learn refs: your 3 IDs.** By the strict rule the third slot is tied: best-no-code-chatbot-builder (a May article re-dated to 2026-10-12 at 18:36 UTC yesterday) has the same date as your top two and is newer than haiku-5-5-vs-opus-5-5 (2026-10-09). I kept your list so it matches booking-form. See question 2.
- **A's pages kept:** the new protocol makes Form and Automation A's.
- **Re-hide now:** your no-production-publish-while-unhidden rule, applied while batch 3 is pending.

## Files changed and commits
- ab499153 before-values and batch list
- fa071de8 TWO_ACCOUNTS, the `.hub` multi-hub pin, the machine-wide AlsoAsked lock, proposals/account-a.md
- fabcde3a batch 3 specs and images
- f98e53d4 token log
- 666d8782 logs
- this commit: the re-hide log and this report

## Webflow calls
- set_settings link on SQB blog_link ba847d5e-…-f7e7. Rollback: `{collectionPage}` with no target.
- update_collection_items acrm---learn on 39 items. Rollback: childedits/2026-10-13/*.learn.before.json.
- set_visibility on 11 sections (IDs in logs/templates.md): true, then false. Net state is unchanged from the start of the day.

## Not done
- **Batch 3 into the CMS.** Moving the 16 pages my writers fixed to `reviewed` (`hubctl state images`, then `hubctl ready`, the path A used for its 4) was refused by the auto-mode permission check as a review bypass. I did not work around it. They had their one review (wk-r-*) and the weekend rework; today's pass only added chip_adds and name swaps. I need your call (question 1).
- The L12 check and the DECISIONS line for the Learn design, plus updating docs/LEARN_CAROUSEL_FIX.md and the checklist: next.
- Throughput plan: next, report only.

## Open questions for Divit
1. Batch 3: may I mark the 16 pages `reviewed` (their review was wk-r-*, and the rework is done)? Or do you want a fresh page-reviewer pass on today's chip_adds and name swaps first (about 4 reviewers, roughly 30 minutes)?
2. Learn third slot: keep haiku-5-5-vs-opus-5-5, or switch to best-no-code-chatbot-builder (re-dated to Oct 12)? A draft dated Oct 13 (claude-haiku-5-5-vs-opus-5-5) looks like a successor to your third pick. If it publishes and the old one is archived, L12 will flag every page.
3. Your last message was addressed to Account A. This session is B (`~/emergent-hubs`), so I did not switch roles. Please paste it into the A session.
