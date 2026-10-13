# Overnight run, 2026-10-13 to 2026-10-14 (Divit, ruling 17)

Account A alone; B is stopped. Nothing ships overnight: no Webflow calls at all. The headless loop is `ops/schedule/overnight_run.sh` (CLAUDE_CONFIG_DIR=~/.claude-b, account A's config dir).

## Override (recorded)
- `.hub` = `A:LP,Form,Auto,SurveyQuiz` from 2026-10-13 ~18:20 UTC (was `A:LP`). Temporary, for the canary and tonight's run only. Restore `A:LP` before B restarts (the previous value is in `.cache/hub.before`).
- B-held pages are never touched: hubctl refuses them, and the loop skips any page whose status entry carries a B hold.

## Gate: the canary first (ruling 15)
- 3 pages from different hubs: hipaa-release-form (Form, writer A-w-47), customer-service-automation (Auto, A-w-48), post-event-survey (SurveyQuiz, A-w-49).
- Full review by A-r agents that wrote none of them.
- Pass = QC 0 on the first run and 0 blocking findings, 3 of 3. Otherwise fix the causes and re-canary. **No scaling before 3/3.**

## After the canary passes (filled in when it does)
