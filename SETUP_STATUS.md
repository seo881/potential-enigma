# Setup status

What exists, what does not yet, and what is next. Update this file whenever a setup item changes state.

## Built (2026-10-06, coordinator chat)
| Item | Where | Verified |
|---|---|---|
| Keyword plan generator from the Semrush workbook; live-page overrides; workbook issues | `plan/` | 603 pages (599 queued, 3 live drafts, 1 off-plan); 0 duplicate slugs, primaries or keywords |
| Collection config: IDs and logical field → slug map for all 4 hubs | `config/collections.json` | 62 slugs per collection, matched to the live items |
| Baseline specs of the 4 live pages (frozen) | `specs/*/` | exported from the CMS, byte-equal to the live fields |
| QC engine (structure, limits, hygiene, keywords, cannibalisation, vendor numbers, claims, duplication) | `qc/qc_hub.py`, `rules/claims.json` | calibrated on the 4 approved pages: only genuine findings, no false positives |
| Operations CLI (status, claim, brief, init, qc, state, payload, verify, record, publish-payload, log) | `ops/hubctl.py` | brief, init, qc and status tested on a real queue page |
| Writing rules, decisions log, runbook, kickoff prompts | `rules/HUB_RULES.md`, `DECISIONS.md`, `RUNBOOK.md`, `KICKOFF.md` | |
| Skills `hub-content` and `hub-qc` (content-first, independent review) | `.claude/skills/` (sources; Claude Code loads them from here), packaged `.skill` files for Claude.ai | validated with skill-creator |
| Claude Code layer: `CLAUDE.md`, `page-writer` and `page-reviewer` subagents | repo root, `.claude/agents/` | |
| Bulk operations: claim up to 50, `next <state>`, `bulk-payload` (100 drafts per call), `bulk-verify`, `publish-payload` (100 per call) | `ops/hubctl.py` | |
| Image brief schema (writers produce it with the copy) | `docs/IMAGE_BRIEF.md` | draft; consumed by the recipe library |
| One-shot setup for any chat | `ops/setup.sh` | fresh public clone at 28fe7fb: image bootstrap OK (20 scenes, all gates clean), keyword map rebuilt, QC smoke PASS, SETUP OK |

## Not built yet (next, in order)
1. **Image recipe library** (coordinator, about 1 day). The 11 approved layouts become functions that render a page's `image_brief` (`docs/IMAGE_BRIEF.md`), plus a numbers-consistency check, a `build.py` command that renders all briefs in a state, and one contact sheet per page. Validated by re-rendering the 16 approved scenes. Writers do not wait for it: they write briefs now; rendering catches up.
2. **Daily review page** for Divit (calibration in full, then a 10% sample plus flagged pages).
3. **Dry run**: 5 pages end to end (write → review → images → review page → drafts → verify), then the calibration batch (10 per hub, reviewed in full by Divit), then 200 a day.

## Waiting on Divit
- Install the two skills, and replace `Kickoff.md` in the Project with the updated `KICKOFF.md` (adds the writer and reviewer prompts and Claude Code mode).
- Choose the runtime: Claude Code (recommended for 200 a day; needs the workbook in `private/` and the Webflow MCP connected) or Claude.ai chats (about 12 chats a day). Check that your plan's usage limits cover about 200 pages a day of writing and review.
- Rotate the keys hard-coded in the old Python pipelines (Webflow token, Google service account, Gemini proxy key).
- Document-template pages (87, mostly Form, incl. queue #1, #2, #6): build now with a "generated document" angle, or park until the template can show a downloadable output.
- Playable quiz pages (48, 28.7% of queue volume): scope a quiz build (the collections are at the field cap, so it would reuse an embed field, like the FAQ does).
- Wave 3 top-10 pull from Semrush (242 pages from queue #208). At 200 a day this is needed by production day 2.
- Hub pages go-live date (child pages link up to them) and the Webflow plan's CMS item limit (about 600 new items).
