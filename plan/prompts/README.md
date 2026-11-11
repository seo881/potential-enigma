# Agent prompts for the 2026-11-11 handover (A coordinator)

Rebuilt by A-c-1 from RUNBOOK, DECISIONS 2026-11-03..11 (slot policy, standing go incl. item 5, review lock, hold ownership, HERO PROMPT FIX) and reports/2026-11-11/resume-note.md. B's originals were in its scratchpad, outside the repo.

Every agent, every prompt:
- Repo `~/emergent-hubs` (account A, CURRENT COORDINATOR: A). Run every repo command as `.venv/bin/python3 ...`.
- Read CLAUDE.md, LESSONS.md, and the DECISIONS lines from 2026-11-03 onward before starting.
- Commit only the paths you changed, with `bash ops/sync.sh "<msg>" <paths...>` (never directories except images/<hub>/<slug> and audits/live/<date>). Never discard another agent's uncommitted work; check `git status` first.
- NO SITE PUBLISH EVER. CMS item publishes only, through `hubctl api-*` (never the Webflow connector for CMS writes).
- Never edit templates, components, classes or pages; only the 4 child collections.
- Quality gates unchanged. Every page must read as human, operator-grade (HUB_RULES 2b, rules/ai_tells.json).
- Standards gate on every page touched: slug == `ops/slugs.py` slug_for (spec_problems empty); hero prompt passes QC L13 + L14 and the HERO PROMPT FIX bar (one specific sentence in the user's voice, concrete realistic build, exact primary keyword, approved capabilities only, unique in the hub).
- Report back in under 20 lines: what you did per page, states, commit SHAs, anything for Divit.

Files: ship.md, verifier.md, reviewer.md, writer.md, rework.md, gate.md.
