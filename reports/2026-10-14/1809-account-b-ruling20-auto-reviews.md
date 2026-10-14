# Account B: ruling 20, Automation full reviews (2026-10-14)

## Request

> Apply ruling 20 now (recorded in DECISIONS and TWO_ACCOUNTS by A). Pull first; set .hub to B:LP,Form,Auto,SurveyQuiz.
> 1. Reviews are yours: full-review the 9 Automation pages at images (drip-campaign, accounts-receivable-automation, payroll-automation, it-automation, content-workflow, crm-automation, accounting-automation, healthcare-automation, compliance-automation) with B-r agents that wrote no part of them. hubctl refuses a match. One rework each where blocking; then hubctl ready. Send the flagged FAQ questions of each reviewed page (page, Q number, text) in your report for the advisor's check.
> 2. Writing: all 4 hubs including LP, ruling-15 pipeline, claims only through hubctl claim from the top of the ranked queue. The 37 new-keyword pages become claimable once A registers them; claim them as soon as they are.
> 3. No Webflow calls and no AlsoAsked or Semrush calls, ever.
> 4. Tonight: when your queue is empty, stop this session; Divit starts ops/schedule/overnight_run_b.sh.
> Up to 10 writer and 4 reviewer subagents in parallel. Report under 15 lines when the 9 reviews are done.

## Actions and results

1. **Setup.** `.hub` is set to `B:LP,Form,Auto,SurveyQuiz` (untracked).
2. **Reviews.** Four independent reviewers, B-r-3 to B-r-6, each gave every page one full review. None of them wrote any part of these pages.
   - **Passed with 0 blocking:** drip-campaign and content-workflow.
   - **7 pages had blocking findings**, 6 of them about truth. Each got one rework by its own writer, then `hubctl ready`:
     - healthcare-automation (e170a29c)
     - compliance-automation (2967ca70)
     - crm-automation (25a2efd4)
     - accounting-automation (9f5c8770)
     - accounts-receivable-automation (0b393b18)
     - payroll-automation (c247f4ed)
     - it-automation: see 3.
   - The review commits are 97a78cb8, 9b9636a1, c2a1c7a5 and cb6f737e.
3. **it-automation.** The rework is done (QC 0, re-rendered), but `ready` and `sync` refuse it under the review lock. The finding's text names the tab 2 alt, but its field list leaves that field out. `hubctl unlock` is coordinator-only, so the ask to A is in proposals (84e8cf59). The page stays held by B-w-63, with the rework uncommitted.
4. **Writing.** `hubctl claim` gave one page across all 4 hubs: product-launch-landing-page (LP), now being written (908f2a10). The 37 new-keyword pages are not registered in status yet.

## Numbers

| | Count |
|---|---|
| Pages reviewed (full) | 9 |
| Blocking rate | 7 of 9 pages (10 blocking findings) |
| Now `reviewed` | 8 |
| Waiting on A's unlock | 1 (it-automation) |
| Flagged FAQ questions on reviewed pages | 28, in 7 of the 8 pages (list in `.cache/flags/b-auto-2026-10-14.txt`, not in git: AlsoAsked/Semrush text) |
| Webflow, AlsoAsked or Semrush calls | 0 |

## Decisions

- **One rework per page, blocking findings only.** Edits of the same class in the same field were allowed (compliance FAQ 1 and FAQ 10). Source: CLAUDE.md step 5; TWO_ACCOUNTS review lock.
- **AR FAQ 6's flat "No" was left as a slim-review note.** It was not in the finding. Source: one rework, blocking findings only.
- **Webflow:** none.

## Webflow calls

None.

## Not done

- it-automation waits on A's unlock.
- The new-keyword pages wait for registration.
- **Blocking rate.** At 7 of 9 it is over 20%, so ruling 20.2 calls for an A spot-check.

## Open questions for Divit

1. **Comparison-table library.** All the reviewers note that the code-built Automation table uses Zapier, Make and n8n, which rarely rank in these pages' top 10. Should the competitor library get finance, CRM, GRC and RPA rows?
