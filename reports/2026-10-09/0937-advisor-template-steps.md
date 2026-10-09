# Advisor chat: template launch steps checked and done, contact-form held, PA13 fixes ordered

## Request
Divit (2026-10-09): "can't you do all this? also check if something is also done from these" (the Designer-only steps T3, T5, T6, T10, T11, T12 and the batch-1 PA13 read), then: "drop it if you are unconvinced, then update the same in the github repo so code also has full context".

## Actions and results
- Webflow (advisor chat, agent opus-5.5|claude-ai|dv9k2): read the 4 child templates; T6 written (carousel visible on all 4); T3 and T11 found already done; T5 and T10 cannot be settled through the API and move to the staging check. Element IDs, before/after and rollback: `logs/templates.md` (2026-10-09 lines). Status: `plan/template-status.json`.
- PA13 pre-read of all 210 FAQ questions on the 21 launch pages (from the specs in this repo). 16 pages clean; contact-form held; 4 fixes ordered (DECISIONS 2026-10-09).
- Backlog: 4 gate gaps found by the read (`plan/backlog.md`).

## Decisions
- Launch set = 20 (contact-form held), the 4 PA13 fixes, template steps, staging-first publish: DECISIONS.md 2026-10-09.

## Webflow calls
- Writes: set_visibility true on section_build (4 templates). Rollback: set false on the same IDs.
- Reads: query_elements and get_settings on the 4 templates; get_page_metadata on the 4 template pages. No CMS calls, no publish.

## Not done
- The 4 PA13 fixes (Claude Code: QC, gate, draft update, bulk-verify).
- Launch-set files (`plan/batches/batch-1.txt`, `ops/out/launch/*`, `status/launch-checklist.md`) still list 21; Claude Code regenerates them for 20.

## Open questions for Divit
None.
