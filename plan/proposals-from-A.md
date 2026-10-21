# Proposals from account A (rules, templates, code)

A writes proposals here; B reviews and applies them (DECISIONS 2026-10-21).

## 2026-10-21 (Account A)
- **Survey library: customer-feedback Emergent/competitor variant.** A-r-24 (cancellation-survey review): the code-built SurveyQuiz table's cells speak of employee survey templates on a customer cancellation page. Proposal: a customer-feedback variant (cancellation, newsletter, NPS-type pages) in rules/competitors/sqb.json, selected by primary keyword like the Automation category_sets. New writing only.
- **Form table K7 (P2) on most new Form pages:** Google Forms / Typeform / Jotform columns are not in the page's top 10 (code-built table). Proposal: pick table vendors from the page's own SERP top 10 when the library has them, else keep the hub default. New writing only.
- **B's recheck 4bb5d5a61c4e moved 3 old pre-r15 parked Form drafts to `rework`:** address-verification-form, anesthesia-consent-form, approval-form (no CMS item; parked before). They are not reworks of reviewed pages. Proposal: B returns them to `parked`, or releases them to the queue so A rebuilds them fresh (`skeleton.py build --fresh`) as new writing. A has not touched them.
- **Tooling notes from writers:** `hubctl images` asks for `--by`; `ops/render_changed.py` with no arguments wrote no render.json until run with `--pages URL`.
