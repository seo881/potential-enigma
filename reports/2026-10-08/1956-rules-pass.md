# Rules pass (2026-10-08, commit 9ea2d96)

Backfilled 2026-10-08 20:42 IST from commit 9ea2d96 and `logs/form.md` (14:26 UTC entry). Plan it executed: `audit/feedback-2026-10-08.md`.

## Request
Not recorded verbatim (the session predates the report rule). What was asked, per commit 6d99908 and `audit/feedback-2026-10-08.md`: fix every item of Divit's registration-form feedback on the page and at the cause, as one combined rules pass, with no Webflow writes.

## Actions and results
- `qc/paa_gate.py`: PA3 widened (head phrase exact, reordered or inflected, or an approved secondary). Gate summary regenerated: `audit/paa/summary.md` (one line per page, no question text).
- `qc/qc_hub.py`: nine new checks: V5 (no plan tiers or rolling numbers in competitor cells, Emergent column exempt), S10 (zero-width characters and empty paragraphs), H3 (serial comma; certain cases block and are auto-fixable, ambiguous ones listed), H4 (UK idioms), A5 (the built app does things, not Emergent), A6 (never narrow the audience), C4 (custom domains built in, use credits), C5 (GitHub export on paid plans), Q9 (one word carrying too much of the page).
- New `qc/serial_comma.py` (H3 engine) and `rules/style_rules.json` (UK idiom list, narrowing phrases, built-app verbs, repeat threshold 8, plan words).
- Competitor library reworded in `rules/competitors/{aab,form,lp,sqb}.json`: no rolling numbers or plan tiers, new Form rows for caps/waitlists and conditional logic, Emergent cells reworded, GitHub on paid plans.
- `ops/table.py`: logo alt "emergent" -> "Emergent". All comparison tables regenerated with `hubctl table`.
- `ops/hubctl.py`: link-to-live (`live_urls()`: the 4 hubs, `live_child_urls`, and published children); `export_fields()` strips zero-width characters and empty paragraphs and sends links to non-live child pages as plain text, recording them as pending.
- `audit/hubs-faq.json`: the 4 hub pages' FAQs saved for PA10 coverage.
- registration-form fixed to QC 0 and PAA gate 10/10; update payload rebuilt (see `1954-registration-form-update-payload.md`), not sent.
- Plans written, not executed: `plan/rework-2026-10-08.md` (combined pass per page), `plan/template-edits-2026-10-08.md` (T1-T12).

## Numbers
- Commit: 199 files changed, 1,074 insertions, 334 deletions.
- Specs touched (table regeneration): 184 (Auto 8, Form 147, LP 18, SurveyQuiz 11); registration-form also edited (28 insertions, 13 deletions).
- New QC checks: 9. UK idioms listed: 20. Narrowing phrases: 9. Plan words: 18.
- Rework plan, 183 pages: clean 1, code-fix only 0, FAQ replacements only 1, semantic copy only 4, FAQ + semantic 107, park (PA11, under 8 on-topic) 70. Estimated cost 17.12M tokens (review measured at 89k per page on registration-form).
- Template edits proposed: 12 (T1-T12): 8 block first publish, 1 conditional (T10), 3 do not.

## Decisions
- PA3 widened as ruled (DECISIONS 2026-10-08, "PA3 widened"); newly admitted questions exported for Divit's read before any rework.
- Serial comma enforced in QC H3 (DECISIONS 2026-10-08, "Serial (Oxford) comma everywhere").
- Hub link and link-to-live in the payload builder (DECISIONS 2026-10-08, "Hub link and link-to-live"; hubs live, same date).
- One combined pass per page planned, not per-check passes (DECISIONS 2026-10-08, "Fixes run as ONE combined pass").
- No rolling vendor numbers in tables (DECISIONS 2026-09-29 to 10-05, "Rolling vendor numbers").
- GitHub export qualified by plan: emergent.sh/pricing (GitHub integration from Standard).
- Custom domains "built in, use credits" and "No response caps" (DECISIONS 2026-09-29 to 10-05, approved claims; `rules/claims.json`).
- Audience never narrowed (DECISIONS 2026-09-29 to 10-05, "never narrow the audience").
- `hubctl recheck` deliberately not run: it would move every page to rework before the combined pass (`logs/form.md`, 14:26 UTC).

## Files changed and commits
- 9ea2d96 (rules pass): files listed above.
- 6d99908 (preceding): `audit/feedback-2026-10-08.md`, DECISIONS lines for this pass.

## Webflow calls
None (no reads or writes in this commit). The read-only template inspection it relies on is recorded in `audit/feedback-2026-10-08.md` (Findings section).

## Not done
- Combined rework pass: waits for Divit to read `.cache/review/pa3-newly-passing.csv` and give the go.
- Template edits T1-T12: each needs Divit's go, one call each.
- PAA synonym candidates (`rules/paa_synonym_candidates.json`) not applied: they need Divit's approval of the batch.
- registration-form update payload not sent.

## Open questions for Divit
1. Read the PA3 widening export and give the go for the combined pass (107 + 4 + 1 pages)?
2. 70 pages park under PA11: accept, or approve synonym candidates first to recover some?
3. Template edits: go per edit (T1, T2, T3, T4, T5, T9, T11, T12 block first publish; T5 and T6 are Designer-only settings for you or the Webflow developer).
4. Learn section (T3): Option A (newest posts site-wide) or hide when empty?
5. Placeholder testimonials and stats on the 4 hubs and 4 templates: your ruling (report only so far).
