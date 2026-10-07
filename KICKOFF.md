# Kickoff prompts

The repo holds all state. Paste one of these as the first message of a new chat; it rebuilds full context in a few minutes. Replace HUB with LP, Form, Auto or SurveyQuiz.

## Project instructions (set once, in the Project settings)
> This Project runs the Emergent build-hub child pages. Every chat starts by reading `EMERGENT_BUILD_HUBS_HANDOFF.md` sections 0 and 2, then cloning https://github.com/seo881/potential-enigma, running `bash ops/setup.sh`, and following `RUNBOOK.md`. State lives in that repo, never only in a chat. Follow Divit's rules (handoff section 0) and `DECISIONS.md`.

## Mode A: Claude Code (recommended for 200 pages a day)
One-time setup on the machine: clone the repo; copy the Semrush workbook to `private/Emergent_Hub_Child_Pages_Final_v3.xlsx`; connect the Webflow MCP server and authorise it; run `bash ops/setup.sh --no-images`. Then start Claude Code in the repo and say:
> Run today's production per CLAUDE.md: claim 50 pages per hub, write them with page-writer subagents in parallel, review them with page-reviewer subagents, and report counts by state. Do not touch Webflow.

## Mode B: Claude.ai Project chats
**Coordinator** (one; owns shared code, images, Webflow drafts, publishing):
> You are the coordinator for the Emergent build-hub child pages. Read the handoff (sections 0 and 2), clone the repo, run `bash ops/setup.sh`, then read `RUNBOOK.md`, `DECISIONS.md`, `SETUP_STATUS.md` and the latest entries in `logs/`. Report the state of all four hubs (`python3 ops/hubctl.py status`) and the next step, then wait for my go.

**Writer** (about 8 a day: two per hub, 25 pages each):
> You are a HUB writer for the Emergent build-hub child pages. Read the handoff (sections 0 and 2), clone the repo, run `bash ops/setup.sh --no-images`, read `RUNBOOK.md`, `DECISIONS.md` and `rules/HUB_RULES.md`, and use the hub-content skill. Do any `rework` pages for HUB first, then claim 25 pages for HUB and write them content-first until each is `qc_pass`. Commit every 5 pages. Do not touch Webflow.

**Reviewer** (about 2 a day; never the chat that wrote the pages):
> You are a reviewer for the Emergent build-hub child pages. Read the handoff (sections 0 and 2), clone the repo, run `bash ops/setup.sh --no-images`, read `RUNBOOK.md` and `rules/HUB_RULES.md`, and use the hub-qc skill. Review every page in `python3 ops/hubctl.py next qc_pass`, marking each `reviewed` or `rework` with notes. Commit every 10 pages. Do not touch Webflow.

**Continuing a chat that ran long:**
> Continue as the HUB writer (or reviewer, or coordinator). The previous chat stopped at the state in `status/` and `logs/`. Set up per `RUNBOOK.md` and resume.

## Mode C: Claude.ai batch writer (batches of 10 per reply; Divit's rhythm)
Start a fresh chat in the Project, upload the latest serp.zip (made on the Mac from private/serp), and paste:
> You are the batch writer for the Emergent build-hub child pages. Read the handoff (sections 0 and 2), clone the repo, run `bash ops/setup.sh`, then unzip serp.zip into private/serp. Read RUNBOOK.md, DECISIONS.md (newest first), rules/HUB_RULES.md, rules/SEVERITY.md, rules/CONTENT_DEFECTS.md, docs/IMAGE_BRIEF.md and the hub exemplars. Write batch N: the next 10 queued pages whose SERP is captured, in queue order. In one reply, for each page: plan, write the full spec, table from the library (research and source any missing competitor first), image brief with checks and story links, QC to zero, render images. Commit and push after every page. End with a one-line status per page. No Webflow calls. After every 5 batches, do the in-depth review of all 50 pages and publish batch previews (ops/preview.py --batch).
