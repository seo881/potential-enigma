# Site publish this week: redirect import and pre-publish checklist (2026-11-17)

Prepared by B-redir-3 for Divit's order of 2026-11-17: "Redirects: prepare the final CSV (843 rows plus the 30 fixes, all targets 200) and a pre-publish checklist for my site publish this week."

**Divit does the import and the publish. Claude never publishes the site, staging or any domain, and never imports redirects** (CLAUDE.md NO SITE PUBLISH, Divit 2026-10-10; DECISIONS 2026-11-06). Steps marked DIVIT are his clicks. Steps marked CLAUDE are read-only checks or repo changes. Preparing this file needed no Webflow call. Every pre-check below used the public site over HTTPS, or the CMS read-backs another agent took today at 07:28-07:30 UTC.

## 1. What the publish changes

| # | Change | Source | State today |
|---|---|---|---|
| 1 | **Redirect set replaced** by `reports/2026-11-17/redirects-final-v3.csv`: **843 rows** plus the header `source,target`. The bytes match the format of the file live today (CRLF, same row order). All 843 sources are kept: 0 added, 0 dropped. **30 targets change**, and the other 813 rows are byte-identical to the live set. | v1 `reports/2026-10-23/redirects-final.csv` (live since 10-23) + the v2 fixes `reports/2026-11-03/redirects-v2-changes.md` (DECISIONS 2026-11-03) | Verified 07:32 UTC: 771/771 targets return 200 directly, 0 failures (`reports/2026-11-17/redirects-v3-verify.md`) |
| 2 | Staged child CMS items | 4 child collections | **Nothing staged.** On the 07:28 UTC read-back, 0 of 646 live items were updated after their last publish. The one draft is Form `creator-application` (draft since 2026-10-09), and a site publish does not publish drafts. Nothing from the held hero-prompt backlog (280 pages) is staged. |
| 3 | Staged Learn items (other team's content) | Learns `6a0f028d0bfe272031dbddb8` | 0 of 769 published Learn items were updated after their last publish (07:30 UTC read-back). On 11-06 there were 14, so that RED has cleared. This is a timestamp check, not the field-by-field diff from 11-06. |
| 4 | Other collections (Blogs, News, Tutorials, Builds, App/Website/Web App Builders, FAQs, ...) | not ours | **Not checked.** Claude has no read-back of them and made no Webflow call. A site publish ships any staged edits in them. Divit checks the publish dialog, step D1. |
| 5 | Staged template, page, component or style changes | Designer | **None by Claude since 2026-10-23.** logs/templates.md has no write after the 10-23 quiz embed, and the 2026-11-06 quiz-embed change was never staged (reports/2026-11-06/quiz-cls-390-investigation.md). The page API is not readable by us, so changes by anyone else are unknown. Divit checks the publish dialog, step D1. |
| 6 | Font-loading fix (head code) | proposal `reports/2026-11-11/font-loading-proposal.md` | **Not applied.** Production still loads Inter through `WebFont.load` and has no Brockmann preload (checked 07:3x UTC). It is optional, and it is Divit's call whether it goes into this publish. It is not on the critical path (DECISIONS 2026-11-11). If he adds it, Claude re-runs the CLS check after the publish (section 4). |

Last Published stamp on emergent.sh and on emergent-sh.webflow.io: Mon 2026-11-16 13:38:31 UTC (same on both).

## 2. The 30 fixes (old target -> new target)

The 24 known issues `redir-*` in rules/live_audit.json are the 24 old targets below, and 30 rows point at them. Today 21 of those targets 301 to another page, which makes each row a 2-hop chain, and 3 return 404 (leadpages, dating, resume). No other row needs a fix. Every one of the other 813 targets returns 200 directly. No target is a hub child page that has been renamed or unpublished (S7 = 0 against status/live.json, 646 live pages).

| # | source | old target (today) | new target | why |
|---|---|---|---|---|
| 1 | /build/healthcare-website-builder | /ai-website-builder/healthcare (301) | /ai-website-builder/medical | chain end |
| 2 | /build/mobile-website-builder | /ai-website-builder/custom (301) | /ai-website-builder | chain end |
| 3 | /build/car-dealer-website-builder | /ai-website-builder/dealer (301) | /ai-website-builder/car-dealer | chain end |
| 4 | /build/interactive-website-builder | /ai-website-builder/interactive (301) | /ai-website-builder | chain end |
| 5 | /build/reseller-website-builder | /ai-website-builder/reseller (301) | /ai-website-builder/white-label | chain end |
| 6 | /build/hospitality-website-builder | /ai-website-builder/hospitality (301) | /ai-website-builder/hotel | chain end |
| 7 | /build/web3-website-builder | /ai-website-builder/blockchain (301) | /ai-website-builder/crypto | chain end |
| 8 | /build/website-builder-for-tradesmen | /ai-website-builder/contractor (301) | /ai-website-builder/construction | chain end |
| 9 | /build/betting-website-builder | /ai-website-builder/betting (301) | /ai-website-builder/casino | chain end |
| 10 | /build/react-website-builder | /ai-website-builder/custom (301) | /ai-website-builder | chain end |
| 11 | /build/no-code-website-builder | /ai-website-builder/no-code (301) | /ai-website-builder | chain end |
| 12 | /build/custom-website-builder | /ai-website-builder/custom (301) | /ai-website-builder | chain end |
| 13 | /build/property-management-website-builder | /ai-website-builder/property (301) | /ai-website-builder/real-estate | chain end |
| 14 | /build/instant-website-builder | /ai-website-builder/instant (301) | /ai-website-builder | chain end |
| 15 | /build/cloud-based-website-builder | /ai-website-builder/cloud-based (301) | /ai-website-builder | chain end |
| 16 | /build/dealership-website-builder | /ai-website-builder/dealer (301) | /ai-website-builder/car-dealer | chain end |
| 17 | /build/contractor-website-builder | /ai-website-builder/contractor (301) | /ai-website-builder/construction | chain end |
| 18 | /build/gym-website-builder | /ai-website-builder/gym (301) | /ai-website-builder/fitness | chain end |
| 19 | /build/responsive-website-builder | /ai-website-builder/custom (301) | /ai-website-builder | chain end |
| 20 | /build/online-course-website-builder | /ai-website-builder/course (301) | /ai-website-builder/lms | chain end |
| 21 | /build/conference-website-builder | /ai-website-builder/conference (301) | /ai-website-builder/event | chain end |
| 22 | /build/funnel-website-builder | /ai-website-builder/leadpages (404) | /ai-landing-page-builder | Divit 2026-11-03 |
| 23 | /build/charity-website-builder | /ai-website-builder/charity (301) | /ai-website-builder/non-profit | chain end |
| 24 | /build/attorney-website-builder | /ai-website-builder/attorney (301) | /ai-website-builder/law-firm | chain end |
| 25 | /build/dating-website-builder | /ai-website-builder/dating (404) | /ai-web-app-builder/dating | closest live page (DECISIONS 2026-11-03) |
| 26 | /build/lawyer-website-builder | /ai-website-builder/lawyer (301) | /ai-website-builder/law-firm | chain end |
| 27 | /build/subscription-website-builder | /ai-website-builder/subscription (301) | /ai-website-builder/membership | chain end |
| 28 | /build/automotive-website-builder | /ai-website-builder/automotive (301) | /ai-website-builder/auto | chain end |
| 29 | /build/property-website-builder | /ai-website-builder/property (301) | /ai-website-builder/real-estate | chain end |
| 30 | /build/ai-website-builder/resume | /ai-website-builder/resume (404) | /ai-landing-page-builder/resume | Divit 2026-11-03 (the condition is met: the page is live, 200) |

## 3. Pre-checks

Run on 2026-11-17 at about 07:30 UTC, read-only:

| # | Check | Result |
|---|---|---|
| P1 | `wc -l reports/2026-11-17/redirects-final-v3.csv` = 844 (843 + header) | GREEN |
| P2 | `.venv/bin/python3 ops/redirect_set_check.py verify --csv reports/2026-11-17/redirects-final-v3.csv --old reports/2026-10-23/redirects-final.csv` gives 0 duplicate sources, 0 self-loops, 0 chains (no target is a source), 0 sources that shadow a live child page or one of the 4 hub URLs, 0 hub targets that are not live, and 771/771 targets returning 200 with no redirect followed. Exit 0. | GREEN. Five targets returned a one-off 5xx and gave 200 on the first re-fetch (Webflow's occasional transient 500, the same pattern as on 11-06). |
| P3 | `.venv/bin/python3 ops/redirect_check.py check --csv reports/2026-11-17/redirects-final-v3.csv` against production: 813 rows ok, the 30 A11-redirect findings are exactly the 30 changed sources (production still serves v1), and 0 A11-target | GREEN once transients are set aside. The run gave 31 A11-redirect and 4 A11-target. All of them were transient 500s. The 4 targets and every one of the 813 unchanged sources passed on a re-fetch. |
| P4 | Child collections: nothing staged (section 1, row 2) | GREEN (07:28 UTC read-back) |
| P5 | Learn: nothing staged (section 1, row 3) | GREEN (07:30 UTC, timestamp check) |
| P6 | Other collections, and Designer pages, components and styles | **Divit, D1** (not readable by Claude) |
| P7 | Rollback file ready: `reports/2026-10-23/redirects-final.csv` (843 rows, the live set) | GREEN |

Re-run P2 and P3 within the hour before the import. They take about 2 minutes each and need no Webflow access. If staging was published after production, also run P3 with `--base https://emergent-sh.webflow.io`.

## 4. Steps

**D1. DIVIT, Designer: look before publishing (about 2 min).** Open the Designer > **Publish**. Before you click, read the list of changed pages, components and styles. Anything you or KS did not intend means STOP. If other teams' CMS items are staged (Blogs, News and the like), ask KS whether they may go live. Optional: add the font-loading head code from `reports/2026-11-11/font-loading-proposal.md` (Site settings > Custom code > Head; remove Inter in Site settings > Fonts).

**D2. DIVIT, redirect import.** Dashboard > the Emergent site > **Site settings > Publishing > 301 redirects** > **Import CSV** > `reports/2026-11-17/redirects-final-v3.csv`. The import replaces every existing 301, which is intended: v3 holds all 843. Afterwards the list shows **843** redirects. If Webflow shows any other count, STOP and re-import the rollback file (section 6).

**D3. DIVIT, the one publish.** Optionally publish staging (webflow.io) first, and Claude runs the check in section 5 against staging. Then publish emergent.sh and www together, once.

## 5. Post-publish checks (CLAUDE, read-only, straight after)

1. **Redirects, production:**
   `.venv/bin/python3 ops/redirect_check.py check --csv reports/2026-11-17/redirects-final-v3.csv`
   Pass = `rows ok 843 of 843`, 0 A11-redirect, 0 A11-target, exit 0. If a row fails on a 500 or a transport error, re-run that row. A persistent failure goes to Divit, with the rollback option.
2. **Repo switch (coordinator, one commit, after 1 passes):** in `ops/redirect_check.py`, set `CSV` to `reports/2026-11-17/redirects-final-v3.csv` and update its docstring. Remove the 24 `redir-*` entries from `known_open_issues` in `rules/live_audit.json`. Add the DECISIONS line "v3 redirects imported and published, <date>". Then run `.venv/bin/python3 tests/golden/run.py` (0 regressions). The daily check then runs 843+ rows against v3 on both runners. MIN_ROWS stays 843.
3. **Full live audit:** `launchctl kickstart -k gui/$(id -u)/sh.emergent.live-audit` (publish_watch also triggers it when the stamp changes). Wait for `audits/live/last_success.json` to update. Pass = 0 A11 findings, P0 0, and no new real fails beyond the standing known issues (LinkedIn 403, plus hero-backlog until it is handled). Template regressions (A5-learn, A9-carousel-shown, hub carousel) are P0 and would show that the publish carried a bad staged template change. If one appears, roll back (section 6).
4. **Publish smoke:** `.venv/bin/python3 ops/publish_smoke.py` passes (publish_watch runs it on the new stamp anyway).
5. **If the font fix went in:** `node ops/quiz/cls.mjs --base https://emergent.sh --direct /ai-survey-and-quiz-builder/style,/ai-survey-and-quiz-builder/vocabulary --runs 5 --widths 1440,390` gives every run under 0.01.
6. Report the AUDIT line.

**Known-issue entries to remove after a passing step 1:** the 24 `redir-*` entries (redir-attorney, -automotive, -betting, -blockchain, -charity, -cloud-based, -conference, -contractor, -course, -custom, -dating, -dealer, -gym, -healthcare, -hospitality, -instant, -interactive, -lawyer, -leadpages, -no-code, -property, -reseller, -resume, -subscription). Keep `linkedin-bot-403`. `hero-backlog-prompt` and `hero-backlog-chip-fight` are not affected by this publish: the backlog is not staged, so the publish neither ships nor clears it.

## 6. Rollback

- **Redirects:** Site settings > 301 redirects > Import CSV > `reports/2026-10-23/redirects-final.csv` (the exact 843-row set live until now), then publish. After that, the daily check and the 24 known issues are correct again as they stand. The repo switch in 5.2 is reverted with a new commit, never a reset.
- **A staged template or CMS change that should not have shipped:** Divit reverts it in the Designer, or restores a site backup (Site settings > Backups, the one from before this publish), then republishes. Claude does not do either.
- **Font fix:** remove the head code and restore Inter in Site settings > Fonts, then republish.

## 7. If Divit has not published by 2026-11-19

The 24 `redir-*` known issues already run to 2027-02-01. The `hero-backlog-prompt` and `hero-backlog-chip-fight` entries expire on **2026-11-19**, and after that they count as about 560 real fails in the audit. **The coordinator handles both** (extend the expiry or close the entries, per Divit's standing rulings). B-redir-3 has not edited `rules/live_audit.json`. The v3 CSV stays ready, and nobody asks Divit to import it (DECISIONS 2026-11-06: parked housekeeping that goes with his own next publish).

AUDIT: last full run 2026-11-16 14:11 UTC, 646 pages, 270 real fail (github-actions run; the Mac run at 13:41 UTC recorded 1 real fail)
