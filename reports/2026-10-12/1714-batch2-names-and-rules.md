# Batch-2 names fixed before staging; stock-name, K7 and PA14 rules; A6 defaults; procurement and incident variants

## Digest for Divit
- **The 20 staged pages now use neutral, unique, non-famous names.** No Northwind, Globex, Initech or Acme is left in any batch-2 spec or image. Every person and business name on the 20 appears on no other page. Images were re-rendered and every contact sheet read. QC 0, gate 0 rejects, ship-qc 0 on 20/20.
- **CMS updated, changed fields only:** 17 items (3 had nothing to change). Before-values were committed first (a41bd115). Status was kept (isDraft false on 20). Read-back verify 20/20, pre-flight 20/20. Nothing published.
- **Heads-up: the site was already published to staging at 10:50 UTC** (after my Part B report). All 20 items carry that lastPublished. Staging showed the old names and emergent.sh is still 404 for these pages. The CMS now has the new names, so the next staging publish carries them.
- **Rules (each with golden cases; suite at 124 cases, 0 regressions):**
  - The four stock names, plus Contoso, Fabrikam, Wayne Enterprises and Umbrella Corp, are now an AI tell (A1, P1).
  - K7 matches multi-word brands (Adobe Acrobat no longer a false positive).
  - PA14 exempts acronyms of the page's own keywords (AP), domain acronyms (OCR and others) and US states.
- **A6 defaults applied:** credits.log reconciled, 14 F4-only parks re-queued, credit-capped pages and hipaa-release-form stay parked.
- **Publish to staging only now.**

## Request
> Stock names: fix the 7 pages BEFORE staging. Replace Northwind/Globex/Initech/Acme (and reused personas) with neutral, believable, non-famous names, unique per page; re-render affected images locally; QC 0, gate 10/10; update the CMS items (changed fields only, before-values committed first); pre-flight 20/20. Add these names to the AI-tell list with golden cases.
> A6 defaults: yes to all (credits.log reconciliation, credit-capped pages stay parked, re-queue the F4-only parks, hipaa-release-form stays parked).
> K7 matcher multi-word brands: yes, with a golden case.
> video-landing-page: keep Landingi as the third column.
> Procurement and incident-response Emergent variants: approve both and regenerate.
> PA14 acronym exemption (AP, OCR): yes, with golden cases.
> A8: waits for my GTM check; change nothing.
> Then tell me "Publish to staging only now".

## Actions and results
- **Names, three agents by hub group** (each with a reserved name pool, so no two pages draw the same name):
  - LP and SurveyQuiz pages: 6f5870f6.
  - Form pages: 4e73b0aa.
  - Automation pages: 5dfd5832, including the procurement and incident variants and both tables regenerated.

  The stock names were on 7 pages per the review box, but a full scan found them on 10 (counting image briefs), plus reused personas on 15. All were fixed.
- **My sweep after the agents** (every Title Case pair on the 20, checked against all 400+ specs):
  - Two real public figures in images, flagged by the Form agent: an architect's name on rental-agreement tab 4 and an actor's name on EVL tab 3. Both replaced (eefae347).
  - 18 background people and businesses still shared with other pages (e.g. Maple Grove on 5 other pages, Pine Hollow on 6, Ava Brooks on 7). Replaced on 10 pages by changing surnames and distinctive words only, so first names, pronouns and standalone mentions stay correct.
  - Leftovers from the swaps:
    - a stale URL (`nadiabrooks.example`);
    - Lumen Coaching and Lumen Apartments, each shared with 5 pages;
    - one name too wide for the phone mockup (caught by the image gate, shortened);
    - an article slip ("an Tarrant", fixed to "a Tarrant").

  Commits 930ca0bd, b2c40e72, a7043195. Final re-scan: no reused names, no stock names, and every new name appears in exactly one spec.
- **Contact sheets read:** liability-waiver, credit-card-authorization, rental-agreement, order-form, ebook, employee-satisfaction and EVL after my edits. The agents read the rest. Names fit, initials match, no clipping.
- **CMS:**
  - `ship-update --before-only` wrote 17 before-value files, committed and pushed at a41bd115.
  - Payloads built (no isDraft key) and sent per collection: SQB 3, Auto 5, Form 6, LP 3.
  - Read back all 20.
  - New `ship-update --verify`:
    - Every text field and alt equals the spec export.
    - Every image sent is a new CDN file compared with its before-value.
    - cms_draft fingerprint and image base SHA refreshed, so the next update diffs from here.
  - Result: 20/20. `LAUNCH_BATCH=batch-2 launch.py preflight`: 20 of 20 pass.
- **Rules agent:** 20c2b898 (QC, gate, golden), 89cf50d3 (A6 re-queue, `hubctl release` accepts a parked page with a note, DECISIONS lines, LESSONS line).
- `.cache/review/batch-2.html` regenerated (`--slim`). The risk box no longer lists stock names or reused personas.

## Numbers
- 20 pages: QC TOTAL 0, ship-qc 0, gate 10 items with 0 rejects on all 20.
  - 36 flags remain: 33 PA6 (asker unclassified, a judgment call, not a defect) and 3 PA7 (definition questions, as in Part B).
  - The PA14 flags from Part B are gone.
- Name replacements: 116 people and businesses on 17 of the 20 pages (agents 80: LP+SQB 14, Form 35, Auto 31; my sweep 36, including the 2 real public figures). Mobile, brand-awareness and customer-feedback had none.
- Images re-rendered on 20 pages; all gates pass.
- Webflow: 2 bulk reads (4 collections each), 4 update calls (17 items). No create, no publish.
- Stock names elsewhere: 83 specs contain one of the new A1 names. The pages not yet live will fail QC when next checked. Three live-draft pages (approval-workflow, thank-you-page, customer-satisfaction) will show it on the next recheck. No recheck was run today.

## Decisions
- Stock and famous names replaced with neutral, unique names: Divit 2026-10-12 (this request), now DECISIONS 2026-10-12. Reused background names are covered by "and reused personas, unique per page". Applied to people and named businesses or places, not to real competitors (Adobe Acrobat, Microsoft Forms) or common phrases.
- Changed fields only, status kept, before-values committed first: Divit 2026-10-10 and this request. HUB_RULES not affected.
- Incident variant key `incident-response`, not `incident`: QC Q4 applies a variant by the competitors' shared category, and PagerDuty, Swimlane and Exabeam share `incident-response`. The wording follows the approval.
- Landingi kept as the third column on video-landing-page (Divit 2026-10-12). Its K7 P2 stays as a note.
- A8: no change (waits for the GTM check).

## Files changed and commits
- 6f5870f6, 4e73b0aa, 5dfd5832: names on the 20 specs, images and render.json, rules/competitors/aab.json variants.
- 20c2b898, 89cf50d3: qc/qc_hub.py, qc/paa_gate.py, rules/ai_tells.json, rules/paa_blocklist.json, tests/golden/*, ops/hubctl.py, status/form.json, logs/form.md, DECISIONS.md, LESSONS.md.
- eefae347, 930ca0bd, b2c40e72, a7043195: name sweep, invoice article fix.
- a41bd115: childedits/2026-10-12/*.batch-2.before.json (17).
- This commit: ops/ship.py (`ship-update --verify`), ops/launch.py (prints the right checklist name), specs/* (cms_draft refreshed), status/launch-checklist-batch-2.md, logs/templates.md, this report.

## Webflow calls
- list_collection_items (read) on LP, Auto, SQB, Form for the 20 IDs, before and after. Saved to .cache/readback/pre-names.json and after-names.json (not committed).
- update_collection_items, changed fields only, isDraft omitted:
  - SQB 6ab24754757025d10940d04e: 6accb39f13e0be4f1e5be583, 6accb44a40d5b6e947b71558, 6accb44a40d5b6e947b7155c.
  - Auto 6ab2470540448c8f7d1ccbf0: 6accb27bf4e029b5515a4626, 6accb27bf4e029b5515a4628, 6accb32573d2b6b752fb8d4e, 6accb32573d2b6b752fb8d50, 6accb32573d2b6b752fb8d52.
  - Form 6aaaaa02995bb2f9f4d6a36c: 6accb96b8570d8ef2122bde8, 6accb96b8570d8ef2122bdea, 6accb96b8570d8ef2122bdec, 6accba1c29454f1af2f01f0f, 6accba1c29454f1af2f01f11, 6accba1c29454f1af2f01f13.
  - LP 6aaaa937fe1a8d180b7c9f83: 6accb1512c9cca4363e93f7c, 6accb1fc9cd3f94473f62a82, 6accb1fc9cd3f94473f62a84.
- Before: the field values in childedits/2026-10-12/<slug>.batch-2.before.json. After: the spec export (verified 20/20).
- Rollback: update_collection_items with each before.json's fieldData on the same ID.
- No publish of any kind.

## Not done
- B5 onward: waiting for your staging publish.
- `hubctl recheck` after today's rule changes: not run, so live-draft and other pages that now fail A1 have not been queued. I'll run it with B5.
- Part C: not started (after B is live).
- A8: unchanged.

## Open questions for Divit (recommended default first)
1. **Publish to staging only now.** The CMS has the new names; the 10:50 UTC staging publish has the old ones.
2. Stock names on the other 83 specs: let the A1 ratchet send them to rework as each is next touched (default), or run a bulk name pass now.
3. The 33 PA6 flags (asker unclassified) on 8 pages: leave as notes (default), or have a reviewer clear them before production.
