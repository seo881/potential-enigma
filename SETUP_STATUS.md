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
| Human-voice standard and AI-tell checks | `rules/HUB_RULES.md` 2b, `rules/ai_tells.json`, QC codes A1-A4 | approved pages: 0 hits; planted AI copy: every tell caught |
| **Image engine**: 11 recipes from the approved scenes, 44 blocks, covers, share images, fit and number checks, balance check, contact sheets; QC lint (I1/I2); `hubctl images` / `images-batch` | `pipeline/engine.py`, `pipeline/engine_blocks.py`, `docs/IMAGE_BRIEF.md`, `pipeline/briefs/` | all 16 approved scenes rebuilt from briefs, gates clean; 20/20 SVGs byte-identical on the Linux and macOS paths; the 24 live images still rebuild byte-identical |
| Portable pipeline: path resolver, pinned assets (Inter 4.1, Lucide 1.52.0), renderer with a pure-Python fallback (`resvg-py`) | `pipeline/paths.py`, `assets.py`, `raster.py`, `_alias.py` | macOS path simulated end to end |
| Claude Code config: `.mcp.json` (Webflow), `.claude/settings.json` (permissions), macOS-ready `ops/setup.sh`, setup guide | repo root, `docs/CLAUDE_CODE_SETUP.md` | Linux path tested; macOS path to be confirmed on Divit's machine |
| One-shot setup for any chat | `ops/setup.sh` | fresh public clone at 28fe7fb: image bootstrap OK (20 scenes, all gates clean), keyword map rebuilt, QC smoke PASS, SETUP OK |

## Not built yet (next, in order)
1. **Daily review page** for Divit (calibration batch in full, then a 10% sample plus flagged pages), built from specs and contact sheets.
2. **Dry run**: 5 pages end to end (write → review → images → review page → drafts → verify), then the calibration batch (10 per hub, reviewed in full by Divit), then 200 a day.

## Waiting on Divit
- Install the two skills, and replace `Kickoff.md` in the Project with the updated `KICKOFF.md` (adds the writer and reviewer prompts and Claude Code mode).
- Runtime chosen: Claude Code. Run `docs/CLAUDE_CODE_SETUP.md` on your machine and report the result of the check in step 4.
- Rotate the keys hard-coded in the old Python pipelines (Webflow token, Google service account, Gemini proxy key).
- Document-template pages (87, mostly Form, incl. queue #1, #2, #6): build now with a "generated document" angle, or park until the template can show a downloadable output.
- Playable quiz pages (48, 28.7% of queue volume): scope a quiz build (the collections are at the field cap, so it would reuse an embed field, like the FAQ does).
- Wave 3 top-10 pull from Semrush (242 pages from queue #208). At 200 a day this is needed by production day 2.
- Hub pages go-live date (child pages link up to them) and the Webflow plan's CMS item limit (about 600 new items).
