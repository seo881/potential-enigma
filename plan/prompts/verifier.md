# A-ver-<n>: verifier (slot policy, Divit 2026-11-11)

Read plan/prompts/README.md first. READ-ONLY toward Webflow: no CMS writes, no publishes.

For every page published today (status/live.json lastPublished on 2026-11-11, reports/2026-11-11/ship-groups.log) and every page A-ship publishes while you run (poll every 10 minutes):
1. `hubctl verify-live <url>` (title, meta, H1, FAQ, images, share image, links all 200).
2. Quiz pages (/ai-survey-and-quiz-builder/ with a quiz embed): production CLS at 390 and 1440, 3 runs each, max < 0.01 (as B-ship-9 did for vocabulary; tooling per DECISIONS 2026-11-06).
3. Standards gate on the live item: slug == ops/slugs.py slug_for of the H1 target keyword; hero prompt passes L13/L14 and the HERO PROMPT FIX bar.
4. Post-ship live audit per group if A-ship has not run it (docs/LIVE_AUDIT.md; its own folder audits/live/2026-11-11/postship-ver-<k>).
Write results to reports/2026-11-11/verifier-A-ver-<n>.md (no raw API responses), commit + push with explicit paths.
Any FAIL: report the URL, the check, and the evidence immediately in your result; do not fix it yourself.
Stop when A-ship has finished and every page shipped today is verified. Return: pages checked, PASS/FAIL per page, CLS numbers, SHAs, and the AUDIT line (last full run time, pages, fails).
