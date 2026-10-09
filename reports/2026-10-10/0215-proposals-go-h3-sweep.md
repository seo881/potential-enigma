# Divit's go on the live-audit proposals, H3 detector fix and serial-comma sweep, before-value guard

## Request

Divit (2026-10-10): "Divit's go on the proposals (reports/2026-10-10/0120-part3-live.md):
1. Google Forms "How you build": verify against Google's own documentation (support.google.com / workspace.google.com) that Gemini form drafting exists and on which plans. If confirmed with a source, update the library cell to the proposed wording (with source and check date) and regenerate the affected tables; if not confirmed, keep the current cell and log why.
2. 404-page feature_1: use the safe rewrite ("Your prompt asks for the designed page on every unknown URL; check its status code with your host before launch.").
3. 404-page Emergent build cell: "Prompt for the page and the rules behind it" (new LP library cell for utility pages).
4. client-onboarding explore_cta: "Build My Onboarding Questionnaire". New QC check: explore_cta at most 34 characters (P1), added to HUB_RULES and the writer brief.
5. 404-page meta description: "does not exist" quick fix now; the template JSON-LD escaping goes on the MONDAY backlog.
6. Template P2s: MONDAY backlog.
7. Fix the H3 serial-comma detector (verb series, noun phrases with clauses, 4-item lists), close the 4 open golden cases, then sweep the 20 live pages (fix path: item publish only, before-values, ledger, live re-check).
8. Process fix: before-values must be committed and pushed BEFORE any Webflow write; enforce it in the fix path (refuse to write if the before-value file isn't in git HEAD). Add a LESSONS line.
All live changes follow docs/LIVE_AUDIT.md. Report digest first, then stop."

## Digest

- **Live result: 17/17 items verified, 0 rolled back.**
  - verify_launch on emergent.sh: 20 pages, 4 templates and 4 hubs, 0 failing.
  - The new text is visible on the live HTML: the Gemini cell, the 404 safe sentence and "does not exist", both CTAs, and the serial commas.
  - Ledger for the 2026-10-09 audit: 79 fixed (1 P0, 78 P1); 0 proposals waiting; 20 not-an-issue (FAQ schema); 53 P2 on the backlog.

- **All 8 items are done.**
- **Item 1, confirmed from Google's own sources.**
  - The Help Center page "Create a form with Gemini in Google Forms" (support.google.com/docs/answer/16346789) says the feature "requires an eligible Google Workspace or Google AI plan". It also says it is desktop only and rolling out.
  - Workspace Updates (2025-06-11) lists the plans: Business Standard and Plus, Enterprise Standard and Plus, the Gemini Education add-ons, and Google AI Pro and Ultra.
  - The cell now reads "Editor, with Gemini drafting on some Workspace plans", with the source and check date 2026-10-10 in rules/competitors/form.json.
  - 148 tables were regenerated: 147 form specs plus 404-page. 11 of them are live.
- **Items 2 to 5:**
  - 404 feature_1 uses your safe sentence, its heading is now "A status code you check before launch", and the body is trimmed to the 165-182 band.
  - New LP `utility` variant, with "Prompt for the page and the rules behind it".
  - CTA "Build My Onboarding Questionnaire".
  - 404 meta "does not exist".
  - **QC D3** (CTA at most 34 characters, P1) is in QC, HUB_RULES and the writer brief. On the live pages it caught employee-engagement-survey (35 characters), now "Build My Engagement Survey". 20 specs not yet in Webflow are over the limit; they go to the batch-2 pass.
- **Item 7:**
  - H3 now catches verb series, noun phrases with clauses and 4-item lists. The 4 golden cases are guarded, and 9 new no-flag traps are guarded.
  - Before the sweep I read all 50 candidate hits on the live pages. 39 were real. The other 11 were detector errors, now fixed and kept out by the traps:
    - table cells running together;
    - an appositive ("Owen Tate, the lead therapist, gets...");
    - "one or two";
    - "3,000";
    - a pair inside the last item;
    - "such as" examples.
  - After the fixes the detector found 41 real misses on 18 live pages; all 41 are fixed.
- **Item 8:** `live-fix prepare` now writes the before-value and refuses to write the payload until that file is committed, unchanged and on origin/main. It refused for all 17 pages on its first run; the before-values were pushed (5ca21c6), and only then were payloads written. The LESSONS line is in.
- **Live writes:** 17 items. Each one was updated (changed fields only), published on its own, read back, then checked with a Layer A re-run on the live URL. No site publish.

## Actions and results

1. **Google check.** I fetched the Help Center page and the Workspace Updates post directly. The new fact is recorded in rules/competitors/form.json with its source, check date 2026-10-10 and the previous value. Tables were regenerated from the library (`ops/table.py`); each spec diff is the one cell only.
2. **404 and onboarding fields.**
   - Spec edits for 404 feature_1, meta_description and the table variant `utility`.
   - Spec edit for the client-onboarding explore_cta.
   - QC then flagged the 404 feature_1 body at 204 characters (L7, T1). I kept your sentence and replaced the rest with "Search engines read the status code, and people read the page." The body is now 177 characters. The heading changed because "A status code you ask for by name" restated the claim we removed.
3. **QC D3** added to qc/qc_hub.py, plus a row and a bullet in rules/HUB_RULES.md section 5, .claude/agents/page-writer.md and the writer brief in ops/ship.py.
4. **H3 detector** (qc/serial_comma.py):
   - New patterns:
     - three or more items of up to 8 words;
     - a first item fused with the verb;
     - one-comma lists whose 2nd and 3rd items run in parallel (both determiners, or both -s verbs after an -s verb).
   - Guards:
     - intro clauses;
     - appositives;
     - "one or two" ranges;
     - prepositional modifiers;
     - "such as" examples;
     - numbers with commas;
     - table cells and paragraphs as clause breaks.
   - Two comparison-library cells were added to rules/serial_comma_exceptions.json.
   - Golden suite: 91 cases, 0 regressions, 4 open misses (the PA13 cases).
   - The new golden kind `h3-noflag` keeps the traps uncaught.
5. **Sweep.** `serial_comma.fix` ran on the certain hits in the 20 live specs: 41 commas in 18 specs, in visible copy, mockup prompts and alt text. ship-qc gives TOTAL 0 on all 20.
6. **Fix path.**
   - The new `live-fix approve` turned the 6 proposals into writer fixes, `--by divit`.
   - The new `live-fix add` recorded 25 sweep, library and D3 findings in audits/live/2026-10-09/findings.json.
   - Fresh CMS read of the 17 items. `prepare` wrote 17 before-values and refused every payload. Before-values pushed (5ca21c6). `prepare` again wrote 17 payloads.
   - I diffed every field's before and after text: only the approved commas, cells, sentences and CTAs change.
7. **Sent** 17 payloads (data_cms_tool: update, item publish, read back) between 20:08 and 20:14 UTC. Every update and publish returned errors [].
8. **Verify:** `live-fix verify` per item (read-back equals the spec, Layer A re-run on the live URL). 17/17 FIXED (covering the 25 new findings and the 6 approved proposals); 0 rollbacks.
9. **Re-check:** Manifest rebuilt from the specs (`launch.py prepare`, files only). verify_launch on https://emergent.sh: 20 pages, 4 templates, 4 hubs, 0 failing. curl spot check of 5 pages: every new string is present. Audit report regenerated: reports/2026-10-09/0236-live-audit.md.

## Numbers

| | Count |
|---|---|
| Library cells changed | 2 (Google Forms build; LP utility variant) |
| Spec tables regenerated | 148 (11 live) |
| Live items written | 17 (item publish only) |
| Serial commas fixed on live pages | 41 on 18 pages |
| Detector false positives found and fixed before the sweep | 11 |
| Golden suite | 91 cases (4 h3-gap guarded, 9 h3-noflag guarded), 0 regressions |
| QC on the 20 live specs | TOTAL 0 |
| H3 P1 on specs not yet in Webflow (new detector) | 487 on 150 specs (auto-fixable; batch-2 deterministic pass) |
| D3 on specs not yet in Webflow | 20 |
| Rolled back | 0 |

## Decisions

- **Google Forms cell.** Approved wording (Divit, item 1), published only after Google's docs confirmed it: support.google.com/docs/answer/16346789 and workspaceupdates.googleblog.com/2025/06/help-me-create-gemini-google-forms.html. Recorded in DECISIONS 2026-10-10 and rules/competitors/form.json.
- **404 feature_1 heading and remaining body.** HUB_RULES section 5 (feature body 165-182, spread 12) and the claim registry: the old heading implied the hosting claim your rewrite removed.
- **LP `utility` variant.** The other rows are copied verbatim from the hub default, following the same pattern as the `seo` variant (Divit decision 4).
- **employee-engagement-survey CTA under D3.** The recheck rule says live pages that fail a new rule are fixed (CLAUDE.md 7c); a CTA is a text field in auto-fix scope (docs/LIVE_AUDIT.md). "Build My Engagement Survey" shortens the display name and keeps the verb.
- **Mockup prompts and alt text are swept too.** They are CMS fields covered by QC H3. Mockups are not rendered while the carousel is hidden, but they ship when it returns.
- **Detector false positives fixed before any write.** LESSONS rule 3 (gates tested like code): every false positive became a guarded no-flag case.
- **H3 on specs not yet in Webflow stays in the batch-2 pass.** Rules freeze per batch (DECISIONS 2026-10-08); the fix is deterministic (`serial_comma.fix`).

## Files changed and commits

- d0029e3 (repo side):
  - rules/competitors/form.json and lp.json;
  - 148 specs;
  - qc/qc_hub.py (D3) and qc/serial_comma.py;
  - rules/serial_comma_exceptions.json;
  - tests/golden/cases.jsonl and run.py;
  - ops/live_audit.py (before-value guard, approve, add), ops/hubctl.py, docs/LIVE_AUDIT.md;
  - rules/HUB_RULES.md, .claude/agents/page-writer.md, ops/ship.py;
  - DECISIONS.md, LESSONS.md, plan/backlog.md (MONDAY items 5 and 6);
  - findings and ledger.
- 5ca21c6: 17 before-values (childedits/2026-10-10/), pushed before any write.
- The commit after 5ca21c6 (see reports/INDEX.md): verify results, cms_draft fingerprints, ledger, hub logs, audit report and this report.

## Webflow calls

All calls were data_cms_tool on the 4 child collections, between 20:08 and 20:14 UTC (2026-10-09 UTC; 2026-10-10 IST). Each call was an update (changed fields only), then a publish of that item only, then a read-back. No site publish. Before-values: childedits/2026-10-10/<slug>.<issue>.before.json (pushed at 5ca21c6). Rollback: `hubctl live-rollback ISSUE` re-sends the before-value and publishes that item.

| Page | Item | Fields |
|---|---|---|
| 404-page | 6ac8a23f9873b6bc7b4343ba | meta, features subheading, feature 1, table, tab 4, mockup |
| sign-in-form | 6ac8a0256cea93e7ab27259f | table, tab 1 |
| t-shirt-order-form | 6ac8a04200f35689bf9ff3c2 | table, tab 2 |
| client-onboarding-questionnaire | 6ac8a0256cea93e7ab27259d | CTA, table, FAQ, how-to 2, mockup |
| booking-form | 6ac8a2bff143d8ebe3277361 | table, FAQ, how-to 5 |
| employee-information-form | 6ac8a06cc42bf1463b1a2cbc | table, FAQ, how-to 2, mockup |
| feedback-form | 6ac8a06cc42bf1463b1a2cb8 | table, FAQ, mockup |
| interest-form | 6ac8a04200f35689bf9ff3c4 | table, how-to 5, mockup |
| job-application-form | 6ac8a04200f35689bf9ff3c0 | table, feature 1, tab 3 alt |
| massage-intake-form | 6ac8a06cc42bf1463b1a2cba | table, FAQ, how-to 5 |
| registration-form | 6ac79cdc9308a032a2f7dd2d | table |
| document-automation | 6ac89f5186706b45a79b39b4 | mockup |
| ecommerce-automation | 6ac8a1af7019f6d354746f12 | mockup |
| sales-automation | 6ac89f5186706b45a79b39b2 | meta |
| event-landing-page | 6ac89f545408b01694dc164b | FAQ, mockup |
| law-firm-landing-page | 6ac89f545408b01694dc164d | tab 2 and 3 alts |
| employee-engagement-survey | 6ac8a15a5408b01694dd5e21 | CTA, tab 1 alt, mockup |

Logged in logs/aab.md, form.md, lp.md and sqb.md.

## Not done

- The template JSON-LD escaping (item 5) and the template P2s (item 6) are on the MONDAY backlog, as you asked. No template was touched.
- The widened H3 still leaves two patterns as P2 "ambiguous":
  - lists after "such as" ("such as hoodies, hats and tote bags");
  - lists followed by a trailing modifier (", along with ...").
  A few remain on t-shirt-order-form. Backlog line added.
- 487 H3 and 20 D3 issues on specs not yet in Webflow wait for the batch-2 deterministic pass and writer pass.

## Open questions for Divit

None blocking. Recommended default: run `serial_comma.fix` on all 150 not-yet-shipped specs in the batch-2 deterministic pass (one commit, QC after). It changes only punctuation that the detector now calls certain.
