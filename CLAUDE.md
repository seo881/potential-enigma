# Emergent build-hub child pages (Claude Code)

This repo produces SEO child pages for Emergent's build hubs on Webflow. Read `RUNBOOK.md` first; `DECISIONS.md` holds every ruling from Divit (never re-ask them); `rules/HUB_RULES.md` is how pages are written.

## Setup
First time on a machine: `docs/CLAUDE_CODE_SETUP.md`. On macOS, `ops/setup.sh` creates `.venv`: run every repo command as `.venv/bin/python3 ...` (subagents too).

## Non-negotiables
- Nothing is created or published in Webflow without Divit's explicit go. Drafts only (`isDraft: true`).
- Touch only the child collections in `config/collections.json`. Never edit templates, components, classes or pages.
- Read before every write, commit the old value, read back after. Never force-push.
- Semrush data stays out of git: put the workbook at `private/Emergent_Hub_Child_Pages_Final_v3.xlsx` (git-ignored).
- **Claude Code is only the engine for scale.** Every page is human, operator grade, world class, exactly per `DECISIONS.md` and `rules/HUB_RULES.md`, and must never read as AI-written (HUB_RULES 2b; `rules/ai_tells.json` is enforced by QC).
- Every Webflow call needs Divit's approval in the prompt; never batch-approve on his behalf.

## Production at scale (target 200 pages/day): you are the orchestrator
1. `bash ops/setup.sh --no-images` (Linux sandbox: drop the flag to install the image pipeline).
2. `python3 ops/hubctl.py claim <HUB> 25 --by orchestrator` for each hub in the day's plan; commit and push the status.
3. For each claimed page, spawn a **page-writer** subagent (it first pulls the live SERP through the `dataforseo` MCP and saves it with `hubctl serp-save`) (one page per subagent, many in parallel). Each returns when its spec passes `qc` with TOTAL 0 and the page is in state `qc_pass`.
4. For each `qc_pass` page (`hubctl next qc_pass`), spawn a **page-reviewer** subagent. It never reviews a page it wrote. It sets `reviewed` or `rework` with notes; send `rework` pages back to a writer.
5. Image stage (ON HOLD until Emergent's brand palette is set; `hubctl images` refuses while `images_on_hold` is in config): `python3 ops/hubctl.py images-batch reviewed` renders every reviewed page's `image_brief` (6 images, gates, a contact sheet per page in `.cache/review/`). Read each contact sheet before Divit's review: one hero, readable text, numbers that add up, the story matching the tab copy.
6. Build the daily review page for Divit (calibration batch: every page; afterwards: a random 10% plus everything flagged). Only his go moves pages to `approved`.
7. Commit and push; `hubctl bulk-payload <HUB> --sha <sha>`; create drafts via the Webflow MCP (100 per call); read back; `hubctl bulk-verify`. Publish only on Divit's go (`hubctl publish-payload`).
8. Log every Webflow change in `logs/<dir>.md`. Commit after every stage so any session can resume.
