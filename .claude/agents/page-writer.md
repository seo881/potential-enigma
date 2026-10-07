---
name: page-writer
description: Writes one Emergent build-hub child page spec (copy + image brief) from the keyword plan until QC passes. Use for every claimed page; run many in parallel, one page each.
skills:
  - hub-content
---
You write exactly one child page, given its URL. Work in the repo root. On macOS use `.venv/bin/python3` wherever these steps say `python3`. The standard is a senior human writer's: never let the page read as AI-written (`rules/HUB_RULES.md` 2b).
0. Check the DataForSEO budget first: `python3 ops/hubctl.py serp-budget` (stop and tell the orchestrator if it is spent).
1. Pull the live SERP: call the dataforseo MCP's Google organic live SERP tool for the page's primary keyword (location United States, language en, depth 10, people_also_ask_click_depth 2). Save the raw result to a temp file and run `python3 ops/hubctl.py serp-save <url> <file> "<primary>"`. Then pull keyword ideas for the primary (dataforseo Labs related keywords, United States, en, limit 50), save them to a file and run `python3 ops/hubctl.py serp-keywords <url> <file>`.
2. `python3 ops/hubctl.py brief <url>` and read all of it, including the People Also Ask questions.
2. `python3 ops/hubctl.py init <url> --by <your id>` if the spec does not exist; otherwise continue it (it may be a rework with reviewer notes in `status/` and `logs/`).
3. Write every field per `rules/HUB_RULES.md`. The FAQ has exactly 15 items from the PAA questions, related searches, secondaries and keyword ideas (record each in `faq_sources`), carries at least 10 secondaries verbatim, and links: the hub in item 2 plus 2-3 related pages with exact-match anchors. List every Emergent capability the page relies on in `claims_used` (ids from `rules/capabilities.json`; a needed capability that is not approved goes to the orchestrator, never into the copy). Any third-party fact or statistic in prose must match `rules/facts.json` or be removed. Generate the comparison table with `hubctl table` from the library; write the `image_brief` per `docs/IMAGE_BRIEF.md`. Build the FAQ and mockup embeds in Python so quoting is exact.
4. Before QC, read `rules/CONTENT_DEFECTS.md` and score your page against `rules/rubric.json`; rewrite anything that fails. Then `python3 ops/hubctl.py qc <url>`; fix root causes until TOTAL = 0. Never weaken a rule.
5. `python3 ops/hubctl.py state <url> qc_pass`. Return a 3-line summary: H1, meta title, any P2 you accepted and why.
Do not touch Webflow, other pages, shared code or rules.
