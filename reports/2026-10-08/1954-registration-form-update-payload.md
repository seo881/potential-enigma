# registration-form CMS update payload: built, NOT sent

Backfilled 2026-10-08 20:42 IST from `logs/form.md` (13:49 and 14:26 UTC entries), commits 697aaf6 and 9ea2d96, and the payload file itself.

## Request
Not recorded verbatim (the session predates the report rule). The work followed Divit's canary go (13:39 UTC) and the publish-readiness pass on /ai-form-builder/registration-form.

## Actions and results
- 13:49 UTC: after one review (reviewer-b-regf1, 1 blocking: FAQ 7 definition) and one rework (coordinator-b-q10), the CMS draft was behind by one field (`awb---faq-data`); an update payload was built and not sent (commit 697aaf6).
- 14:26 UTC: after the rules pass, the page was re-fixed to QC 0 and PAA gate 10/10 and the payload rebuilt with 13 fields at `ops/out/registration-form.update.payload.json` (git-ignored; file time 19:54 IST). Not sent.
- Checked now (read-only, 20:42 IST): the payload is a single `update_collection_items` on collection `6aaaaa02995bb2f9f4d6a36c`, item `6ac79cdc9308a032a2f7dd2d`, `isDraft: true`; it contains no link to `/ai-form-builder/conference-registration-form` or `/ai-form-builder/creator-application` (link-to-live sent them as plain text).

## Numbers
- Fields in the payload: 13: `name`, `description`, `meta-description`, `awb---faq-data`, `awb---how-to-step-1-des`, `afb---how-to-step-5-des`, `afb---how-to-step-7-des`, `awb---integration-feature-1`, `awb---mockup-data`, `acrm---key-feature-sub-heading`, `acrm---key-feature-4-content`, `acrm---key-feature-6-content`, `acrm---why-emergent-table`.
- Items: 1. QC TOTAL 0. PAA gate 10/10. Review: 1 blocking finding fixed, 7 notes ship.
- Payload size: 11,715 bytes (original create payload `ops/out/registration-form.payload.json`: 17,724 bytes).

## Decisions
- Built, not sent: nothing is written to Webflow without Divit's explicit go (CLAUDE.md, non-negotiables; DECISIONS 2026-09-29 to 10-05).
- Drafts only, `isDraft: true` (RUNBOOK section 4.2).
- Links to non-live pages shipped as plain text (DECISIONS 2026-10-08, "Hub link and link-to-live").

## Files changed and commits
- `ops/out/registration-form.update.payload.json`: git-ignored, not committed.
- Log lines in `logs/form.md`: commits 697aaf6 (13:49 UTC) and 9ea2d96 (14:26 UTC).

## Webflow calls
None for this payload. Prior and related: canary create at 13:39 UTC (commit 336b540), item `6ac79cdc9308a032a2f7dd2d` in collection `6aaaaa02995bb2f9f4d6a36c`, draft, never published.
- If sent: before = the 13 field values of the current CMS draft (as created from `ops/out/registration-form.payload.json`); after = the payload values.
- Rollback if sent: read the item first and commit the old values; re-send those values with `update_collection_items`. Full rollback of the canary: delete item `6ac79cdc9308a032a2f7dd2d` (collection had no registration-form item before).

## Not done
- Payload not sent: needs Divit's go.
- Not published: depends on the go and on the template edits that block first publish (`plan/template-edits-2026-10-08.md`).

## Open questions for Divit
1. Send the 13-field update to the draft now, or after the combined rework pass?
2. The page links to conference-registration-form and creator-application only as plain text until they are live: acceptable for first publish?
