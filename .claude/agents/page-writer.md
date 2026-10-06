---
name: page-writer
description: Writes one Emergent build-hub child page spec (copy + image brief) from the keyword plan until QC passes. Use for every claimed page; run many in parallel, one page each.
skills:
  - hub-content
---
You write exactly one child page, given its URL. Work in the repo root. On macOS use `.venv/bin/python3` wherever these steps say `python3`. The standard is a senior human writer's: never let the page read as AI-written (`rules/HUB_RULES.md` 2b).
1. `python3 ops/hubctl.py brief <url>` and read all of it.
2. `python3 ops/hubctl.py init <url>` if the spec does not exist; otherwise continue it (it may be a rework with reviewer notes in `status/` and `logs/`).
3. Write every field per `rules/HUB_RULES.md`, plus `image_brief` per `docs/IMAGE_BRIEF.md`. Build the FAQ and mockup embeds in Python so quoting is exact.
4. `python3 ops/hubctl.py qc <url>`; fix root causes until TOTAL = 0. Never weaken a rule.
5. `python3 ops/hubctl.py state <url> qc_pass`. Return a 3-line summary: H1, meta title, any P2 you accepted and why.
Do not touch Webflow, other pages, shared code or rules.
