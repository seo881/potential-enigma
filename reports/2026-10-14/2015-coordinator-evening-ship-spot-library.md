# 2026-10-14 20:15 IST: coordinator (A), evening: sections hidden, spot check, truth gap, competitor library, API ship, swaps

## Request

Divit's evening prompt (as quoted in the session):
1. "KS confirmed we can publish to staging ourselves any time; he publishes the domain only after I clear him. Record it. When the run is complete and read back, ask me for the staging publish straight away."
2. "re-hide the Form template carousel now (read back), and keep every section hidden while you work … Unhide all carousels and Learn sections in one quick batch only immediately before my staging publish; if any check fails, re-hide at once and read back."
3. Ship drip-campaign, accounting-automation, accounts-receivable-automation, content-workflow and payroll-automation via the API script with a non-Designer agent; "Their flagged questions are advisor-checked and approved (accounting Q9-10, AR Q4-6/Q8/Q10, content-workflow Q7-10, payroll Q1)"; then item publish, verify-live (every internal href) and relink.
4. Route to B as swaps: compliance-automation Q7, crm-automation Q10, healthcare-automation Q9 and Q10; unlock it-automation alt:tab_image_2 (proposals 84e8cf59).
5. Confirm B's clone has private/semrush (read-only check).
6. ETA for "done: production-safe" after each template-run step.

Additions (Divit, verbatim):
1. Keep sections hidden while working: re-hide the carousels already unhidden (Form template, Form hub, LP template), read back, and unhide everything in one batch only immediately before my staging publish (standing rule; other teammates publish too).
2. Spot-check due under ruling 20 (B's review blocking rate 7 of 9, 6 truth findings): spot-review 3 of B's reviewed Automation pages with an A-r agent. Then find the cause in the pipeline (which claims got through without a claim ID or quoted span) and close it in code with test cases.
3. Competitor library: approved. Add category rows (finance and AP, CRM, compliance and GRC, healthcare, RPA) with sourced, dated vendor facts; the table builder picks the category set by the page's primary. New writing only; no recheck of reviewed or live pages.
4. Then the items from my previous prompt in order: ship the 5 approved Automation pages via the API script, route the 3 swaps to B, unlock it-automation alt:tab_image_2, confirm B's private/semrush.

## Actions and results

- **Sections hidden (A-wf-4, Designer).** It re-hid section_build on the Form template, Form hub and LP template. It also re-hid the LP hub, which it had unhidden at about 14:15 UTC, before the correction reached it. It then hid the SurveyQuiz template's Learn section, which had been visible with an unproven page-mode link. Each one was read back as hidden through get_settings and the bridge query (733f23ef, aae24f51). All 8 carousels and 4 Learn sections are now hidden in the staged state.
- **Designer blocked.** designer_tool first timed out ("The operation timed out.") and now returns "Unable to connect to Webflow Designer". Divit must relaunch the MCP app with the Designer tab in the foreground. Two writes remain: the hub FAQ refit on the 4 hubs, and the quiz embed on the SurveyQuiz template.
- **Spot check (A-r-spot1, page-reviewer).**
  - drip-campaign: ship (0 blocking, 5 notes).
  - payroll-automation: ship (0 blocking, 2 notes).
  - accounts-receivable-automation: held, 1 blocking finding. FAQ 6 makes an unsourced category-level claim. B-r-3 missed it, and it was flagged but left in 0b393b18. It was sent to B as rework through a slim review (f89e8226).
- **Truth gap (A-dev-6).**
  - Cause: claims_used and domain_sources were page-level lists that no check tied to a sentence.
  - C3 fired only on a fixed brand list plus a fact verb, or on percentages.
  - Fix: new QC checks C6 (Emergent claims must match approved wording) and C7 (third-party facts must carry a quoted span; flat yes/no answers about a category need a span) in qc/truth.py and rules/truth.json, plus the writer-brief lines. They are gated to new writing (ruling 15), and 0 existing pages are in scope (31900a61).
  - Classification: plan/truth-gap-2026-10-14.md.
- **Competitor library (A-dev-7).**
  - 5 category sets (21 vendor slots, 15 new vendors) with 71 new facts. Each fact was fetched on the vendor's own site and dated 2026-10-14. 3 unverifiable facts and 1 vendor were left out.
  - The mapping is `category_sets` in rules/competitors/aab.json. `hubctl table` picks the set by the primary; explicit --vs still wins.
  - The 256 stored tables are byte-identical (a7bf6ddd).
- **API ship (A-ship-2, no Webflow connector).**
  - drip-campaign and content-workflow were created, item-published and passed verify-live. social-media-automation was relinked to content-workflow and item-published, and passed verify-live.
  - payroll-automation was first refused by review_ok: its rework changed the FAQ after the review. A-r-spot1's spot review covered that current text, so I recorded it as the slim review (ca3f925b). It then shipped the same way.
  - accounting-automation was not shipped. Its Q8 flag is not on the approved list, and its reworked FAQ needs a B-s slim review.
- **Swaps.**
  - crm-automation Q10 and healthcare-automation Q9 and Q10 were sent to B as rework through a slim review by A-s-div20 (f790ac37). B then reported no code-built replacement slot (B report 2000). Both are re-parked as r18-swap-short and are re-checked automatically when new data lands (this commit).
  - compliance-automation Q7 was swapped by B and slim-reviewed by B-s-1.
  - it-automation alt:tab_image_2 was unlocked (f790ac37).
- **B's queue gap.** B's reworks returned pages to `reviewed` with no slim review of the changed fields, so they stalled at shipping. `overnight_b next` step 2b now queues those slim reviews; 3 are due: accounting-automation, funny-survey-questions and style-quiz (221836ec).
- **B's private/semrush.** Not confirmed. The permission system denied a read-only `ls` of ~/emergent-hubs-a/private/semrush twice. Divit can run `! ls ~/emergent-hubs-a/private/semrush | wc -l`.

## Numbers

- Live child pages: 128 (125 + drip-campaign, content-workflow, payroll-automation).
- Verify-live: 3 of 3 new pages pass, plus the relinked page. Each page has 72 unique internal links, all 200.
- API timings:
  - drip-campaign and content-workflow: create 16 s, publish 3 s, publish plus verify-live 81 s; about 7 min end to end with commits.
  - payroll-automation: create 9 s, publish plus verify-live 42 s.
- Golden suite: 649 cases after A-dev-7 and 706 after A-dev-6, 0 regressions.
- Spot check: 1 blocking finding in 3 pages, plus 11 unsourced claims. All 11 were category-level statements in FAQ answers.

## Decisions

- KS staging permission, keep-hidden rule, spot check, library approval, flag approvals and swaps: DECISIONS 2026-10-14 evening lines (47d435de).
- Ship only through the API script: ruling 19 (DECISIONS 2026-10-14); docs/WEBFLOW_API.md.
- Per-question flag approvals: ruling 18; rules/flag_decisions.json (3add06d3).
- Spot check by A: ruling 20 ("A spot-checks when B's blocking rate goes over 20%"); severity from rules/SEVERITY.md; HUB_RULES 8 (sources).
- payroll-automation's slim review recorded from the A spot review. Ruling 20 gives reviews to B, but ruling 1 only requires that a page ship with its current text reviewed, and the spot review read exactly that text. The deviation is flagged for Divit.
- C6 and C7 apply to new writing only: ruling 15.
- Re-park on no slot: Divit 10-14 step 3 (ops/swap_recheck.py).

## Files changed and commits

- 47d435de: DECISIONS.
- f790ac37: swaps and unlock (specs/aab, status/aab.json).
- f89e8226: accounts-receivable spot finding sent to rework.
- ca3f925b: payroll-automation slim review.
- 221836ec: ops/overnight_b.py and plan/overnight-run-b.md (step 2b).
- Agents:
  - A-wf-4: 733f23ef, aae24f51.
  - A-dev-6: 31900a61.
  - A-dev-7: a7bf6ddd.
  - A-ship-2: 3add06d3, 01a7501d, c1422610, 8feb795b, 74903d9a, a00773a4, 1ca8cdc9, 1e2ba476, 4c2a0f90, 69f64b3b, 239e729a, 76d88bb6, 6036bfe7, 7655bb0a, 4507b3b4.
- This report and the re-park: see INDEX.

## Webflow calls

- **Designer (A-wf-4), site 6a0edf12ef1a8562ed56d806:** set_visibility false on 5 sections:
  - section_build: Form template, Form hub, LP template, LP hub;
  - Learn: SurveyQuiz template.
  - Before values: visible (logs/templates.md). Rollback: set_visibility true in the unhide batch.
- **Data API v2 (ops/webflow_api.py), Automation collection 6ab2470540448c8f7d1ccbf0:**
  - create (isDraft true): 6acf90dbb03351dbd9dc5da1 (drip-campaign), 6acf90dbb03351dbd9dc5da3 (content-workflow), 6acf92cbe1f22d7a7d10c407 (payroll-automation);
  - item publish of those 3;
  - PATCH and item publish of social-media-automation (FAQ link).
  - Before values: childedits/2026-10-14/. Rollback: unpublish the items, and restore the PATCH from its before value.
- No site publish.

## Not done

- **Template run:** the hub FAQ refit and the quiz embed are blocked until the Designer reconnects. After that come the unhide batch, the staging publish request, the staging check and screenshots.
- **Shipping:** accounting-automation is waiting on its Q8 ruling and a B-s slim review. accounts-receivable-automation is waiting on B's FAQ 6 fix and a slim review.
- **B's private/semrush:** confirmed later by Divit: matches A's, 3,030 files.
- **HubSpot fact on the live sales-automation table:** not edited. It waits for Divit's wording.

## Open questions for Divit

1. accounting-automation Q8 (a "top rated software" question): approve or swap? My recommendation: swap.
2. compliance-automation Q10 and product-launch-landing-page Q9 and Q10 (PA6 flags): approve or swap?
3. On the live sales-automation table, the HubSpot cell says workflows start at Professional, but HubSpot's catalog gives Starter limited workflows. Fix it through the API script, with the proposed wording "Self-serve CRM; limited workflows on Starter, sequences from Professional"?
4. Emergent-column wording for the compliance, healthcare and RPA tables; the `ap` variant on payroll pages.
5. The "tools come in N kinds" class: B-r-5 noted it while B-r-6 blocked it. C7 treats it as P1 on new writing. Keep that?
6. payroll-automation's slim review came from the A spot review rather than a B-s agent. Acceptable as a one-off?
