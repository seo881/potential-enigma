# Site publish this week: pre-publish checklist (2026-11-17)

Prepared for Divit's site publish this week. **Divit decided (2026-11-17) to keep the redirect set unchanged:** the 24 broken redirect targets are pre-existing (from before this project), are left unfixed, and are permanent known issues in the audit. This publish therefore imports no redirect CSV. `reports/2026-11-17/redirects-final-v3.csv` is kept only for reference and is not used.

**Divit does the publish. Claude never publishes the site, staging or any domain** (CLAUDE.md NO SITE PUBLISH, Divit 2026-10-10). Steps marked DIVIT are his clicks. Steps marked CLAUDE are read-only checks. Preparing this file needed no Webflow call.

## 1. What the publish changes

| # | Change | Source | State today |
|---|---|---|---|
| 1 | Redirect set | `reports/2026-10-23/redirects-final.csv` (843 rows: 553 pre-existing + our 290 migration redirects) | **Unchanged.** No import. The daily check pins this file (sha256 in rules/live_audit.json `redirect_list`). |
| 2 | Staged child CMS items | 4 child collections | Child pages ship by item publish, never by a site publish. Re-check just before publishing: if hero-backlog or fix items are mid-flight, items may be staged; a site publish would publish them too. Ask the coordinator for a staged-items read-back within the hour before. |
| 3 | Staged Learn items (other team's content) | Learns `6a0f028d0bfe272031dbddb8` | 0 of 769 published Learn items were updated after their last publish (07:30 UTC read-back, timestamp check). |
| 4 | Other collections (Blogs, News, Tutorials, Builds, App/Website/Web App Builders, FAQs, ...) | not ours | **Not checked** (no Claude read-back, no Webflow call). A site publish ships any staged edits in them: Divit checks the publish dialog, step D1. |
| 5 | Staged template, page, component or style changes | Designer | **None by Claude since 2026-10-23.** The font-loading fix is NOT staged (staging and production both load Inter via WebFont.load), so it is not part of this publish. Changes by anyone else are unknown: Divit checks the publish dialog, step D1. |

Last Published stamp on emergent.sh and emergent-sh.webflow.io: Mon 2026-11-16 13:38:31 UTC.

## 2. Pre-checks (CLAUDE, read-only, within the hour before)

| # | Check | Expect |
|---|---|---|
| P1 | `.venv/bin/python3 ops/redirect_check.py check` (the pinned 843-row set against production) | 819 rows ok; the only failures are the 24 permanent pre-existing targets; 0 A11-redirect; 0 A11-list |
| P2 | Child collections and Learn: staged-items read-back (`hubctl api-read <HUB>` for the 4 hubs; Learn read) | nothing staged, or every staged item listed for Divit |
| P3 | Other collections, Designer pages, components, styles | **Divit, D1** |

## 3. Steps

**D1. DIVIT, Designer: look before publishing (about 2 min).** Open the Designer > **Publish**. Before you click, read the list of changed pages, components and styles. Anything you or KS did not intend means STOP. If other teams' CMS items are staged, ask KS whether they may go live.

**D2. DIVIT, the one publish.** Optionally publish staging (webflow.io) first and have Claude run section 4 against staging. Then publish emergent.sh and www together, once.

## 4. Post-publish checks (CLAUDE, read-only, straight after)

1. **Redirects:** `.venv/bin/python3 ops/redirect_check.py check`. Pass = the same 24 permanent pre-existing targets only; 0 A11-redirect, 0 A11-list, 0 failures on any of our 290 migration rows. Anything else is a REAL alert to Divit.
2. **Full live audit:** `launchctl kickstart -k gui/$(id -u)/sh.emergent.live-audit` (publish_watch also triggers it on a new stamp). Pass = P0 0 and no new real fails beyond the standing known issues (linkedin-bot-403, the 24 permanent redirect targets, and the hero backlog while it is open). Template regressions (A5-learn, A9-carousel-shown, hub carousel) are P0 and mean the publish carried a bad staged template change: roll back (section 5).
3. **Publish smoke:** `.venv/bin/python3 ops/publish_smoke.py` passes.
4. Report the AUDIT line.

## 5. Rollback

- **A staged template or CMS change that should not have shipped:** Divit reverts it in the Designer, or restores the site backup from before this publish (Site settings > Backups), then republishes. Claude does neither.
- Redirects are unchanged by this publish, so there is no redirect rollback.

## 6. Known issues around this publish

- The 24 `redir-*` entries are permanent (no expiry; source: pre-existing redirects from before this project). They match only A11-target on their exact URL, so any other redirect failure, any failure on our 290 migration redirects, and any change to the pinned list still alert.
- `hero-backlog-prompt` / `hero-backlog-chip-fight` expire 2026-11-19 and are being cleared by shipping the backlog; the coordinator extends them by 7 days only if the backlog is not done by then.
