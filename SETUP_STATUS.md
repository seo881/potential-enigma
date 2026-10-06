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
| Skills `hub-content` and `hub-qc` | `skills/` (sources), packaged `.skill` files given to Divit | validated with skill-creator |
| One-shot setup for any chat | `ops/setup.sh` | fresh public clone at 28fe7fb: image bootstrap OK (20 scenes, all gates clean), keyword map rebuilt, QC smoke PASS, SETUP OK |

## Not built yet (next, in order)
1. **Image recipe library** (coordinator). Turn the 11 approved layouts (R1-R11 in `IMAGE_PIPELINE_KT.md` Part 7) into functions driven by a per-page `image_spec` (recipe, prompt chip, people, amounts, statuses, hero card, alt), plus a numbers-consistency check and a `build.py` command that renders a page from its spec. Validate by re-rendering the 16 approved scenes. **Until this exists, hub chats can write and QC copy, but stop at the image step.**
2. **Batch review page format**: one artifact per batch (copy, QC result, image contact sheet) so Divit reviews 5 pages in about 20 minutes.
3. **End-to-end dry run** on one queue page (spec → QC → images → review → draft item → verify → record) before the hub chats start.

## Waiting on Divit
- Install the two skills and set the Project instructions (text in `KICKOFF.md`).
- Rotate the keys hard-coded in the old Python pipelines (Webflow token, Google service account, Gemini proxy key).
- Document-template pages (87, mostly Form, incl. queue #1, #2, #6): build now with a "generated document" angle, or park until the template can show a downloadable output.
- Playable quiz pages (48, 28.7% of queue volume): scope a quiz build (the collections are at the field cap, so it would reuse an embed field, like the FAQ does).
- Wave 3 top-10 pull from Semrush (242 pages from queue #208), needed in about 10 days.
- Hub pages go-live date (child pages link up to them) and the Webflow plan's CMS item limit (about 600 new items).
