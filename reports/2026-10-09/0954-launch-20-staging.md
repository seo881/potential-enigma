# Launch set 20: PA13 fixes, verifier additions, pre-flight 20/20, staging step sent

## Request
Divit (2026-10-09):

> git pull first (advisor commit 3bababc: DECISIONS 2026-10-09, plan/template-status.json, logs/templates.md, plan/backlog.md, reports/2026-10-09/*-advisor-template-steps.md).
>
> 1. Launch set = 20: remove contact-form from plan/batches/batch-1.txt's launch list, ops/out/launch/* (publish payload, rollback files, manifest) and status/launch-checklist.md. Its draft 6ac8a2bff143d8ebe327735f stays a draft.
> 2. PA13 fixes (DECISIONS 2026-10-09), each from an approved secondary or a gate-passing AlsoAsked question, answer-first, no AlsoAsked answer text:
>    - employee-information-form: replace Q4 (ADP fill-out question).
>    - employee-engagement-survey: replace Q5 (near-duplicate of Q4).
>    - t-shirt-order-form: display text "T-shirt" in every question; original wording stays in provenance.
>    - feedback-form: Q1 reads "What is a feedback form?".
>    Each page: QC 0, PAA gate 10/10, FAQ schema/awbFAQ rebuilt from the new text, then update its CMS draft (changed fields only) and bulk-verify 0 mismatches.
> 3. Add to ops/verify_launch.mjs: carousel cover img alt non-empty (4 template cards + 4 hub cards); first use-case tab active on load.
> 4. Pre-flight on the 20 (must be 20/20), rebuild .cache/review/batch-1.html for the 20.
> 5. Then STAGING FIRST: read the site domains, send publish.json for the 20 (isDraft false), read back, and STOP with: "Publish to staging only now."
> 6. When I say "staging published": run verify_launch.mjs against the webflow.io domain for the 20 pages and 4 hub carousels. If cover alt is empty, bind altText on the 4 template covers and 4 hub card covers to the item Name field (standing go, DECISIONS 2026-10-09), then tell me to re-publish staging and re-verify. Any other failure: propose the fix, publish nothing.
> 7. All pass: tell me "Publish to emergent.sh now." When I say "live": verify on emergent.sh, hubctl verify-live per page, hubctl links --relink (update and publish those items only), re-verify, hubctl readiness. Any page failing live: send its rollback file immediately.

This report covers steps 1-5. Steps 6 and 7 wait for "staging published".

## Actions and results
1. **Pulled** 3bababc (fast-forward).
2. **Launch set = 20.** The contact-form line in `plan/batches/batch-1.txt` is now a comment that holds the reason; its ledger entry in `status/ship/batch-1.json` is marked held. `ops/launch.py prepare` regenerated `ops/out/launch/` (git-ignored) for the 20:
   - `publish.json`: 20 IDs in 4 actions, isDraft false, empty fieldData; contact-form is not in it;
   - 20 rollback files, with `contact-form.json` removed;
   - `manifest.json` (now with tab labels, used by the verifier).
3. **PA13 fixes** (specs; FAQ questions themselves are not quoted here, see the specs):
   - **employee-information-form Q4**: replaced with the gate-passing AlsoAsked fill-out question. Source `keyword` (primary), with AlsoAsked provenance. The answer is new and leads with the steps.
   - **employee-engagement-survey Q5**: replaced with the gate-passing AlsoAsked anonymity question. Source `keyword` (primary), with AlsoAsked provenance. The answer leads with "Usually not", and its numbers match the page (no group under five, per feature 2).
   - **t-shirt-order-form**: 8 questions now read "T-shirt". Each faq_sources item keeps the old wording in `q_original`; refs and provenance are unchanged.
     - Normalising exposed a real near-duplicate: Q2 and Q4 became the same question (PA9 reject, gate 9/10).
     - Q4 was replaced with the only gate-passing AlsoAsked question left (making the form in Google Forms). It is recorded under the approved secondary "shirt order form", so that secondary stays covered.
   - **feedback-form Q1**: now "What is a feedback form?". Ref and provenance are unchanged.
   - **Result on all 4:** strict QC (`ship-qc`) 0, plain `hubctl qc` PASS, PAA gate 10/10. awbFAQ was rebuilt in Python from the new text; the FAQ schema is built by the template from awbFAQ.
4. **CMS updates** (changed field only, `awb---faq-data`, isDraft true):
   - read first; before-values committed in `childedits/2026-10-09/`;
   - sent, and the responses matched the specs;
   - draft fingerprints recorded in the specs.
5. **verify_launch.mjs:**
   - `--base` runs it against staging. Content links (written as emergent.sh) are checked on the base host. Canonical must still be the emergent.sh URL. Output goes to `verify-live-staging.json`.
   - **T5 (cover alt):** on every page, the `.section_build` cover images need a non-empty alt. This is summarised as one line per child template. On each hub page, the cards linking to the launched pages need a cover alt.
   - **T10:** the tab labelled `tab_label_1` is `w--current` on load, its pane is `w--tab-active`, and no sibling tab is current.
   - **Smoke run** against emergent.sh: the script ran end to end. It fails as expected because nothing is live yet.
   - jsdom 24.1.0 is installed in `ops/node_modules` (git-ignored).
6. **Pre-flight on the 20:** 20 of 20 pass (`status/launch-checklist.md`). Every item has the matching draft, all fields match (0 mismatches), awbPrompt and awbFAQ (10 items) are present, all images resolve to Webflow files, and every slug is unique.
7. **Review file:** `.cache/review/batch-1.html` has exactly the 20 pages in publish order, every page at gate 10/10. 50 PA3-widened questions are highlighted (down from 54: contact-form's are gone and the replacements changed the count).
8. **Staging step:**
   - **Site domains:** staging `emergent-sh.webflow.io` (last staging publish 2026-10-09 08:29 UTC). Custom domains `emergent.sh` and `www.emergent.sh` were last published 2026-10-08 16:23 UTC.
   - **Sent** `publish.json`.
   - **Read back:**
     - all 20 have isDraft false and lastPublished empty, with all fields unchanged (0 mismatches);
     - contact-form is still a draft;
     - a full read of the 4 child collections (25 items) shows exactly these 20 as non-draft, and none is published or archived.
   - No site publish was sent.

## Numbers
- Launch set: 20 (Form 10, Automation 4, Landing Page 5, Survey and Quiz 1).
- PA13: 4 pages and 12 questions changed. That is 3 replacements (EIF Q4, EES Q5, T-shirt Q4) plus 9 text fixes (8 T-shirt, 1 feedback). Every page is at QC 0 and gate 10/10.
- Pre-flight: 20/20. Read-back after isDraft false: 0 mismatches.

## Decisions
- **Launch set = 20; PA13 fixes; staging first:** DECISIONS.md 2026-10-09 (advisor lines). Source rules: HUB_RULES FAQ section, PAA gate PA1-PA13 (`qc/paa_gate.py`).
- **T-shirt Q4 replaced:** after normalisation it duplicated Q2 (PA9). Divit's bar was gate 10/10, and the replacement came from the allowed sources: a gate-passing AlsoAsked question, with the secondary kept.
- **Source label for AlsoAsked-only replacements:** `keyword`/`secondary` with provenance, as other writers recorded them (`plan/backlog.md`: F2 has no alsoasked kind).
- **T-shirt answers and heading** still use the keyword spellings. The ruling covers question display text only; this is in the backlog for Divit.

## Files changed and commits
- c2e29e0: 4 specs (PA13), `childedits/2026-10-09/*.before.json`, `plan/batches/batch-1.txt`, ledger, `ops/hubctl.py` (the read-back parser skips the MCP session notice block), `ops/launch.py`.
- d0b1b82: draft fingerprints, `ops/verify_launch.mjs`, `ops/launch.py` (tab labels, run order), `status/launch-checklist.md` (20/20), `.gitignore` (ops/node_modules).
- This commit: hub logs, `plan/backlog.md`, this report, INDEX.

## Webflow calls
- **Session** ses_3KS7I2bs2N7e4yiavva4p4u12Dm; **agent** opus-5.5|claude-code|pub20.
- **Reads:**
  - the 4 PA13 items (before);
  - the 20 launch items (pre-flight);
  - `get_site` (domains);
  - the 20 launch items plus contact-form (after isDraft false);
  - all items of the 4 child collections.
- **Write 1 (PA13):** `update_collection_items`, `awb---faq-data` only, isDraft true, on:
  - Form 6aaaaa02995bb2f9f4d6a36c: 6ac8a06cc42bf1463b1a2cbc, 6ac8a04200f35689bf9ff3c2, 6ac8a06cc42bf1463b1a2cb8;
  - Survey and Quiz 6ab24754757025d10940d04e: 6ac8a15a5408b01694dd5e21.
  - Before: `childedits/2026-10-09/`. Rollback: re-send the before-value.
- **Write 2 (staging step):** `update_collection_items`, isDraft true -> false, empty fieldData, on the 20 IDs in `ops/out/launch/publish.json`. The IDs are listed per collection in `logs/form.md`, `logs/aab.md`, `logs/lp.md` and `logs/sqb.md`.
  - Rollback before any publish: the same call with isDraft true.
  - Rollback after a publish: `ops/out/launch/rollback/<slug>.json`.
- **No publish calls, site or item.**

## Not done
- Steps 6 and 7 wait for "staging published" and then "live".
- **Warning:** the 20 items are now non-draft, so any full-site publish will take them live, including a publish to emergent.sh.

## Open questions for Divit
- t-shirt-order-form: should the answers and the FAQ heading also use "T-shirt"? They currently carry "t shirt" and "tshirt". This is in the backlog.
