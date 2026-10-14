# Coordinator handoff: A -> B (ruling 22, Divit 2026-10-14)

Starting with ruling 22, B (`~/emergent-hubs-a`, `CLAUDE_CONFIG_DIR=~/.claude`) is the coordinator and the only Webflow writer. A makes no Webflow calls until a new ruling. Before acting, read CLAUDE.md, LESSONS.md, DECISIONS.md (2026-10-14 from the top), `plan/template-run-2026-10-14.md`, and the latest report, `reports/2026-10-14/2015-coordinator-evening-ship-spot-library.md`.

## 1. Template run (ruling 21 + addendum + evening correction)

- **Plan:** `plan/template-run-2026-10-14.md`.
- **Rollback snapshot:** f12e5ebb (`childedits/2026-10-14/template-run/`).
- **Log:** `logs/templates.md`.
- **Designer session:** `ses_3KdRZfKThMwzr1r57LsQEq1dI5W` (agent_id `opus-5.5|claude-code|tue13`, site `6a0edf12ef1a8562ed56d806`). A new account needs its own Webflow MCP session. Divit relaunches the Designer MCP app from the "Unable to connect" link and keeps the tab in the foreground. Make designer_tool calls strictly sequential: `get_current_page` first, and no data calls in parallel (parallel calls caused the timeouts). `query_elements` can answer while the Designer is disconnected, so it is a data-side read only. A both-way read-back needs designer_tool itself.
- **Done** (A-wf-4's final report, stopped on ruling 22 with no Webflow calls after the STOP):
  - **Step 0:** snapshot f12e5ebb.
  - **Card links:** all 12 in page mode (from the previous agent). Proven only by the staging check.
  - **Carousel cards:** already match the AI app builder reference: link wraps the card; cover bound, 16:10, object-fit cover, alt; title bound; category hidden; 15 per page; Load more with Finsweet intact; hover interaction "within"; focus from the global outline.
  - **Duplicate carousel 86e5ccd1:** absent.
  - **Step 7:** checks pass with no write: the OG image is bound; the FAQ heading comes from the item; tables scroll; mockups render; JSON-LD has no entities. There is no FAQPage JSON-LD (not needed on child templates; DECISIONS).
  - **Step 5:** skipped; the cause is GTM.
  - **Hub FAQ refit:** appended to our own page-level embed on 2 hubs:
    - Form hub, embed 9dd01394 (ce51c631): Data read-back byte-identical; Designer check done.
    - LP hub, embed 25e43d56 (5eace122): Data read-back byte-identical; **post-write Designer check not done. Do it first.**
    - Before-value is CSS-only; after-value is `hub-embed-faq-refit.after.html`. Headless test: 0 of 14 loads clipped, against 2 of 14 without the refit.
  - **Unhide batch plan:** `childedits/2026-10-14/template-run/unhide-batch.json` (3300bec9): 8 carousels and 4 Learn sections, with IDs and order.
- **Visibility now, as last read back:** every section is **hidden**: all 8 section_build carousels (4 templates, 4 hubs) and all 4 Learn sections, including the SurveyQuiz template's `ba847d5e-...-f7d9` (hidden today, aae24f51). The carousel unhide and re-hide nets to no change (733f23ef). Keep them hidden while working (standing rule: a teammate publish ships whatever is staged).
- **Left, in order:**
  1. **Designer check of the LP hub embed 25e43d56.**
  2. **FAQ refit on the Automation hub embed b8a2c5a1 and the SurveyQuiz hub embed 3b7963ef**, the same append.
  3. **Quiz embed on the SurveyQuiz template**, between the hero `ba847d5e-85b3-fe51-eadf-ad4eebacf5cb` and section_stats `...f630`, under main `...f5ca`. Use `ops/quiz/embed.min.html`. The zero-footprint check passed.
  4. **SurveyQuiz Learn:** staging showed Blog cards linking to /blog/, but the staged source already reads Learn, newest 3. Find the cause (an older staged version?) and recheck after the next staging publish. The createdOn tie-break is not applied.
  5. **Empty zero-width `<p>` (U+200D) after feature 1:** it sits inside the shared section_features component. Do not edit the component. Find out whether it is a bound CMS field (if so, fix it through the API) or static (if so, ask Divit or KS).
  6. **Unhide batch:** run it from unhide-batch.json in one quick batch, only immediately before Divit's staging publish, and read it back.
  7. **Ask Divit for the staging publish.** KS allows staging publishes; Divit clears KS for the domain. Claude never publishes.
  8. **Staging check:** `.venv/bin/python3 ops/staging_check.py` (44a6df06; about 32 min). The baseline is in `.cache/staging/baseline/` in A's clone (531 MB, git-ignored): copy it to B's clone or recapture it with `--baseline`. On any failure, re-hide at once, read back, fix, and ask for another staging publish.
  9. **Screenshots** in `divit/` (one hub carousel, one template carousel plus Learn, one quiz page; 1440 and 390 px at true size), then "done: production-safe".
  10. **After KS's domain publish:** live audit and verify-live on all live pages.

## 2. Ship queue (API script only: `hubctl api-*`; ruling 19)

**Live:** 128 child pages (drip-campaign, content-workflow and payroll-automation shipped tonight).

| Page | State | Blocks |
|---|---|---|
| compliance-automation, product-launch-landing-page | reviewed, review_ok | Divit's go to ship (flags approved tonight) |
| sales-automation (live) | "reviewed" after its slim review | HubSpot cell PATCH: payload `ops/out/ship/hubspot-cell-2026-10-14.json` (git-ignored; rebuild in B's clone from 0aa79ba3 / 09cc19b9). The live write was denied by the permission classifier; it needs Divit at the prompt. Then item publish, verify-live, and state back to published. Then add HubSpot back to the CRM default set. |
| accounting-automation | rework (B) | Q8 swap (1 code-built candidate), then a B-s slim review |
| accounts-receivable-automation | rework (B) | FAQ 6 unsourced (spot check), then a B-s slim review |
| it-automation | images, held by B-w-63 | alt:tab_image_2 unlocked; B's rework, then a slim review |
| crm-automation, healthcare-automation | parked r18-swap-short | auto re-check on new data |
| Form: cookie-order, daily-report, fundraiser-order, risk-assessment; SQB: likert-questionnaire | reviewed, review_ok | Divit's go to ship |
| Form (4) and SQB (3) held by B-w-7x/8x | reviewed | B's batch; check the holds before shipping |
| funny-survey-questions, style-quiz | reviewed | B-s slim review due (`overnight_b next` step 2b) |
| vocabulary-quiz, style-quiz | quiz canary | no quiz page ships until the quiz template is live and the canary passes (`status/quiz-canary.json` pending) |

## 3. Open decisions for Divit

1. **Emergent-column cells** for the compliance, healthcare and RPA tables, plus the new payroll variant. The draft table (approved claim IDs only) is in A's chat of 2026-10-14 night. It needs a one-line approval, then goes into `rules/competitors/aab.json` (new writing only).
2. **Navbar `<svg width="2o">`** on the /ai-contests dropdown icon: a shared component owned by KS. It logs a console error on every page. Either KS fixes it, or it becomes a named exception.
3. **Console exception scope:** does `www.clarity.ms/tag/uet/...` (the Bing UET Clarity loader, source of the "reading 'unshift'" error) count as the "GTM Clarity loader"?
4. **Live audit:** drop the old text-based `console_ignore` list and keep only the source exception?
5. **Ship go** for the reviewed, review_ok pages in section 2.
6. **Overnight API shipping proposal**, after 2 clean daytime runs (so far: the 2-page canary and tonight's 3 pages).
7. **Next 2 hubs** (recommended: Checklist and Portal).
8. **B's 2000 report:** fix the code-built field shortener, or let B set explore_cta and faq_heading by hand?

## 4. Loops and schedules

- **Live audit:** `sh.emergent.live-audit` (09:00) and `sh.emergent.publish-watch` (every 30 min, runs the live audit on each new publish stamp). The plists in `ops/schedule/` now point at `~/emergent-hubs-a`. `live_audit_daily.sh` uses `CLAUDE_CONFIG_DIR=~/.claude` and skips in any other clone. The installed copies in `~/Library/LaunchAgents` still point at A's clone until Divit reloads them (commands in the report). B's clone has no `.cache/live/last_published.txt`, so the first tick sees a "new publish" and runs the smoke check and a full live audit once. The live audit allows `mcp__webflow__data_cms_tool` (live fixes), so B's `~/.claude` needs the Webflow MCP authorized. Ruling 19 routes CMS writes through the API script, so review that allowance.
- **Overnight:**
  - B's loop: `ops/schedule/overnight_run_b.sh`. Start, watch and stop commands are in `plan/overnight-run-b.md`. `next` now includes step 2b, the slim reviews.
  - A's loop: `ops/schedule/overnight_run.sh`, not running. Under ruling 20, A writes nothing.
- **A's remaining roles that move to B:** AlsoAsked and Semrush pulls and re-ranks (keys in the macOS keychain, the same for both accounts), the advisor flag list (`ops/flag_packet.py list`), the daily report, and tooling and rules. Semrush spend at the last check: 1,057,370 (14.5% of the starting balance; the line is 25%).

## 5. Half-done

- **HubSpot cell:** prepared and reviewed, not written (see section 2).
- **Staging check:** built, baseline captured, but no post-publish run yet.
- **Quiz canary pages:** not created in the CMS. Their 404 on staging is expected until they are created and staged.
- **Swap-short and N-kinds:** C6/C7 (31900a61) apply to new writing only. 6 sentences on r15 pages are known misses, left unchanged under ruling 15 (`plan/truth-gap-2026-10-14.md`).
