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
- **Work report after every task Divit gives** (RUNBOOK section 6): `reports/YYYY-MM-DD/HHMM-<slug>.md` with the sections Request (his prompt verbatim), Actions and results, Numbers, Decisions (each with the DECISIONS line, HUB_RULES section, URL or data file it follows), Files changed and commits (SHAs), Webflow calls (type, IDs, before/after, rollback), Not done, Open questions for Divit; plus a line in `reports/INDEX.md` (newest first: date, slug, summary, SHA). The repo is public: no keys, tokens, raw API responses, SERP or AlsoAsked question text, or anything from `private/` or `.cache/` in a report (reference paths). Commit and push with `ops/sync.sh`, then reply in chat in under 15 lines: summary, report path, SHA.

## Production at scale (target 200 pages/day): you are the orchestrator
1. `bash ops/setup.sh --no-images` (Linux sandbox: drop the flag to install the image pipeline).
2. `python3 ops/hubctl.py claim <HUB> 25 --by orchestrator` for each hub in the day's plan; commit and push the status.
3. For each claimed page, spawn a **page-writer** subagent (it first pulls the live SERP through the `dataforseo` MCP and saves it with `hubctl serp-save`) (one page per subagent, many in parallel). Each returns when its spec passes `qc` with TOTAL 0 and the page is in state `qc_pass`.
4. Image stage (before review, so reviewers judge copy and images together): `python3 ops/hubctl.py images-batch qc_pass` renders every QC-passed page's `image_brief` (6 images, gates, a contact sheet per page in `.cache/review/`). Read each contact sheet before Divit's review: one hero, readable text, numbers that add up, the story matching the tab copy.
5. For each page in state `images`, spawn a **page-reviewer** subagent (up to 4 pages each): **one review per page**, severity from `rules/SEVERITY.md` only (`hubctl review`). No blocking finding -> `reviewed`. Blocking -> `rework`: **one rework** by a writer (blocking findings only), QC to zero, re-render (`hubctl images`), then `hubctl ready <url> --by <id>` -> `reviewed`. No second review; notes ship. The writer and the reviewer are different agents; hubctl refuses otherwise.
6. Build the review for Divit: `python3 ops/preview.py <url>` writes a page preview with the live SVGs (open it in the browser), `python3 ops/review.py <urls> > review.md` the reading copy, `hubctl export-csv <HUB>` the CMS fields as a spreadsheet (`.cache/review/<hub>.csv`), plus the contact sheets (calibration batch: every page; afterwards: a random 10% plus everything flagged). Only his go moves pages to `approved`.
7. Before creating: read the whole collection to disk and run `hubctl cms-check <HUB> <readback.json>` (required within the hour; prevents duplicates). `hubctl bulk-payload <HUB> --sha <sha>` refuses any page changed since Divit approved it. Create drafts via the Webflow MCP; read back; `hubctl bulk-verify`. The very first page of the dry run is a single-item canary checked by Divit in the Designer.
7b. Publish only on Divit's go (`hubctl publish-payload`), then fetch every published page and run `hubctl verify-live <url>` (title, meta, H1, FAQ, images, share image, links all 200).
7c. Every day: `hubctl lookahead <HUB> 60` (library gaps for the next 3 days: research them first), `hubctl serp-budget`, `hubctl metrics`, `hubctl sample reviewed` (the pages Divit must see), `hubctl links <HUB>`. After any rule change: `hubctl recheck` (ratchet; live pages that now fail go to status/fix_queue.json) and `hubctl image-regress`. Weekly: pull rankings for published pages (dataforseo, depth 100) with `hubctl ranks-save`, then `hubctl ranks-report` (refresh queue).
8. Log every Webflow change in `logs/<dir>.md`. Commit after every stage so any session can resume.
