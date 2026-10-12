# Duplicate IDs in shared components (MONDAY A8, investigation only, 2026-10-12)

Nothing was changed. Webflow Audits flags "Duplicate ID" on the child templates (email-form x5, field x4) and hubs.

## Where they come from (read live HTML + Webflow component reads)
| Component (id) | Instances | Duplicate ids it renders | Pages |
|---|---|---|---|
| `section_usecase` (4a1e2fed-ef87-6e00-ca2d-e0d8e5150c66) | 11 | 4 mockup forms `id="email-form"` (one per use-case tab, class build_form-form), each with a textarea `id="field"` | the 4 child templates (every child page) and other templates using the use-case tabs |
| `Global / Signup Modal` (ecd6507c-a14b-f436-fb2d-d9e0e0e31d45) | 81 | 1 form `id="email-form"` (class hero_auth-form) | every page with the modal (site-wide) |
| `Build page hero` (20c1b760-6736-130c-e34b-872d2c8dc715) | 13 | 1 form `id="email-form"` (class header_form) | hub pages (with the signup modal: 2 per hub) |

On a child page that makes 5 `email-form` (4 use-case + 1 modal) and 4 `field`. The hero prompt form is already unique (`hero-prompt-form`, T9).

## Does anything reference these ids?
- Inline scripts on a child page, the home page and the Form hub: no `#email-form`, `#field`, `getElementById('email-form'|'field')`. The only getElementById calls are `hero-prompt-form`, `nav-button-mobile`, `emergent-turnstile-invis`.
- Site JS bundle (webflow.*.js): 0 references to `email-form`.
- The use-case mockup script reads `[data-mockup-text]` / `.build-usecase_tab-pane`, not ids; the template chip script uses `[data-filter]`.
- NOT checked (no access): Google Tag Manager container GTM-NCCB99P9, Segment and HubSpot form listeners. A GTM trigger of type Form Submission filtered on Form ID = email-form would break if the id changes.

## Safest fix (proposed, needs Divit's go: it edits component definitions)
1. Check GTM-NCCB99P9 for any trigger, variable or tag that uses Form ID / Element ID `email-form` or `field` (5 minutes in GTM, or grant read access).
2. If none: change one component at a time, reading before and after, rollback = restore the old id:
   - `section_usecase`: form ids `usecase-mockup-1..4`, textarea ids `usecase-mockup-text-1..4` (each component appears once per page, so static ids are unique per page). Keep the `name`/`data-name` attributes as they are (Webflow form submissions key on data-name, not id).
   - `Global / Signup Modal`: form id `signup-modal-form`.
   - `Build page hero`: form id `hub-hero-form`.
3. Publish happens only with Divit's site publish; then run Webflow Audits and the live audit (Layer A) on a child page and a hub.
4. If GTM does use `email-form`: keep the modal form's id (it is the one an analytics trigger would target) and change only the use-case mockup forms, which are demo forms that never submit.
