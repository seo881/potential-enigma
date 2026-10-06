# Emergent build-hub child pages (Claude Code)

This repo produces SEO child pages for Emergent's build hubs on Webflow. Read `RUNBOOK.md` first; `DECISIONS.md` holds every ruling from Divit (never re-ask them); `rules/HUB_RULES.md` is how pages are written.

## Non-negotiables
- Nothing is created or published in Webflow without Divit's explicit go. Drafts only (`isDraft: true`).
- Touch only the child collections in `config/collections.json`. Never edit templates, components, classes or pages.
- Read before every write, commit the old value, read back after. Never force-push.
- Semrush data stays out of git: put the workbook at `private/Emergent_Hub_Child_Pages_Final_v3.xlsx` (git-ignored).

## Production at scale (target 200 pages/day): you are the orchestrator
1. `bash ops/setup.sh --no-images` (Linux sandbox: drop the flag to install the image pipeline).
2. `python3 ops/hubctl.py claim <HUB> 25 --by orchestrator` for each hub in the day's plan; commit and push the status.
3. For each claimed page, spawn a **page-writer** subagent (one page per subagent, many in parallel). Each returns when its spec passes `qc` with TOTAL 0 and the page is in state `qc_pass`.
4. For each `qc_pass` page (`hubctl next qc_pass`), spawn a **page-reviewer** subagent. It never reviews a page it wrote. It sets `reviewed` or `rework` with notes; send `rework` pages back to a writer.
5. Image stage: render every `reviewed` page's `image_brief` through the recipe library, run the gates, produce contact sheets (`SETUP_STATUS.md` says whether the library is live).
6. Build the daily review page for Divit (calibration batch: every page; afterwards: a random 10% plus everything flagged). Only his go moves pages to `approved`.
7. Commit and push; `hubctl bulk-payload <HUB> --sha <sha>`; create drafts via the Webflow MCP (100 per call); read back; `hubctl bulk-verify`. Publish only on Divit's go (`hubctl publish-payload`).
8. Log every Webflow change in `logs/<dir>.md`. Commit after every stage so any session can resume.
