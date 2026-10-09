# Launch-day fixes, staged: carousel hidden, Learn list fixed, hero prompt redesigned

## Request
Divit (2026-10-09), "Launch-day fixes, staged only (no production publish until I say so)". Scope: the 4 child templates and their 20 launch items, plus the carousel check on the 4 hubs; no existing class, component, interaction or sitewide element modified or referenced. The steps:
- 0: carousel hidden;
- 1: Learn list "No items found";
- 2: hero prompt redesign (content, behaviour, styling, CMS update, verify_launch);
- 3: logs;
- 4: "Publish staging again";
- 5: Part 3 on "live".

Follow-up: "That 'No' was a misclick ... Continue exactly where you stopped ... Pace the Webflow calls (wait about 65 s after any 429). Then tell me 'Publish staging again'."

## Actions and results
0. **Carousel:**
   - Hidden on the 4 child templates (visibility true -> false, read back).
   - The 4 hubs were already hidden (false before and after, no change).
   - DECISIONS line and the MONDAY backlog line added.
1. **Learn list.**
   - **Cause:** the Collection List limit is 100 on Form, LP and Automation. Each of those renders "No items found", while the same list with limit 3 renders on the Survey and Quiz template and on the live AI agent builder template. Everything else is identical: source Learn, dynamic, no filters, sort by publishing date descending. Finsweet `fs-list` is not involved; the list is already empty in the server HTML.
   - **Before:** Form, LP and Automation pages on staging showed 0 items with the empty state; Survey and Quiz showed items.
   - **After:** limit 3 on all 4, read back. The change shows on staging after the next publish.
2. **Hero prompt.**
   - **Content:** each of the 20 pages has a generic default with the primary keyword (no industries, names or scenarios) and 4 "Add ..." clauses, one per existing chip label.
     - Stored in `spec.chip_adds` and exported as `window.awbPrompt = {default, chips:[{label, add}]}`.
     - **QC:** the clauses now go through every copy check (house style, US spelling, dashes, claims and so on), plus the new L10 checks: 4 clauses, one sentence each starting "Add ", under 90 characters, and a default that carries the primary keyword.
     - **Results:** all 20 pass strict QC at 0. A planted bad clause is caught by L10, the dash check, the "!" check and the UK spelling check.
   - **Behaviour:** `ops/template/hero-chips.html` is a new embed on each template, replacing T1. The 4 T1 embeds were removed.
     - The box loads with the default. Chips toggle their clause, several at once, always in chip order. Typed text is kept. `aria-pressed` and keyboard work.
     - The template's older chip script is blocked by a capture-phase listener on document; the script itself is not edited.
     - The data is read lazily, because the prompt field renders after the embed.
     - Tested in Chromium on a copy of the staging page; every behaviour check passed.
   - **Styling:** `data-hubchip="1".."4"` was added to the 16 chips (attribute add only). `hubchip--on` is black (#000) with white text, with its CSS inside the embed, and no existing class is used.
     - On the reference page /ai-app-builder/vedic-astrology the selected chip is not black: `is-active` renders like an unselected chip and hover is light grey.
     - So I matched that page's black submit arrow (#000, white). This is in the backlog for your look on staging.
   - **CMS:** prompt field only on the 20 items.
     - Before-values: `childedits/2026-10-09/hero-prompt.before.json`.
     - Read back: the field matches the specs, and a before/after diff shows nothing else changed on any of the 25 items.
     - Pre-flight 20/20.
   - **verify_launch:**
     - default prefilled;
     - each chip adds its clause in order and removes it on a second click;
     - typed text survives;
     - `aria-pressed` and `hubchip--on` follow the state;
     - no console errors (known jsdom gaps and site noise ignored, listed in `rules/live_audit.json`);
     - carousel hidden on the 20 pages and the 4 hubs;
     - /ai-app-builder/vedic-astrology unchanged on staging (same text as production, none of our code). This already passes.
   - **Two fixes to the checkers:**
     - jsdom got a `CSS` polyfill, because Webflow's interactions script crashed the run.
     - The live audit now captures real-browser console errors and waits for `load` instead of network-idle, which the site never reaches.
3. **Logs:** `logs/templates.md` (every element ID, before/after, rollback) and the 4 hub logs. Template status was updated (T1 replaced, T3 limit, T6 hidden).

## Decisions
- DECISIONS 2026-10-09: carousel hidden until Monday; the hero prompt design as specified in this request.
- Learn limit 3: your spec ("the 3 newest") and the working templates.

## Files changed and commits
- 6ecbca8: specs (`chip_adds`, new default), `ops/hubctl.py` (prompt export), `qc/qc_hub.py` (L10, clauses QC'd), `ops/template/hero-chips.html`, before-values, `ops/live_audit.mjs`.
- This commit: `ops/verify_launch.mjs`, `ops/launch.py` (manifest clauses), `ops/live_audit.py` (console errors), `rules/live_audit.json`, spec fingerprints, `status/launch-checklist.md`, logs, DECISIONS, backlog, template status, this report.

## Webflow calls
**Element writes:**

| Change | Template | Hubs |
|---|---|---|
| Visibility | 4 | none |
| Learn limit | 3 | — |
| Attribute adds | 16 | — |
| Embeds created, code set | 4 | — |
| T1 embeds removed | 4 | — |

**CMS:** one `update_collection_items`, prompt field, on the 20 items. Every write was read back. Rollbacks are in `logs/templates.md` and `childedits/2026-10-09/hero-prompt.before.json`.

**Not done here:** no publish of any kind.

## Not done
- Verification on staging waits for the republish.

## Open questions for Divit
- Is the black selected chip (black like the submit arrow) the look you want? The reference page shows no black selected state.
