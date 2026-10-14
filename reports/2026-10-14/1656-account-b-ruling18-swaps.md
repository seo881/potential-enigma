# Account B: ruling-18 FAQ swaps (2026-10-14)

## Request

> Restart. Pull first and read DECISIONS rulings 15 to 18, docs/PREVENTION.md and the updated page-writer and page pack. Set .hub to B:Form,Auto,SurveyQuiz.
> 1. First: the ruling-18 swap reworks A routed to you. For each page, hold it, replace only the listed FAQ questions from the page's passing set (code-built skeleton slots, no hand-picked questions), keep every other field unchanged, QC 0, 0 rejects, hubctl ready, unhold, one commit per page. If a page cannot reach 10 without a rejected or dropped question, say so in the commit and leave it for A to re-park.
> 2. Then claim through hubctl claim from the top of plan/queue-ranked.txt as pages become writable (Automation pulls and new keywords land today; quiz pages only after A's quiz canary passes and the pack includes the quiz JSON); never A-held pages; ruling-15 pipeline only.
> 3. No AlsoAsked or Semrush calls.
> Up to 10 writer subagents in parallel. Report under 15 lines when the swaps are done, then at 18:00 IST.

## Actions and results

1. **Setup.** Pulled. `.hub` is `B:Form,Auto,SurveyQuiz`. The old local edits went to a stash.
2. **Replacement candidates.** For each of the 20 pages, `ops/skeleton.py plan_slots` built the code-built candidate list. It drops any candidate that is a near-duplicate of a kept question or a dropped one. The helper script is in the session scratchpad and writes nothing to the repo. Writers took candidates in slot order.
3. **Swapped and `reviewed`: 7 pages, one commit each.**
   - requisition-form (537dd98c)
   - contact-form (0439eeb0)
   - multi-step-form (927eeed2)
   - compensation-survey (e6f49b23)
   - safety-survey (836bd49b)
   - parent-survey (e6dc0f5f)
   - customer-service-automation (076541ef)
4. **Left in `rework` for A to re-park: 12 pages.**
   - **Too few code-built slots** (available/needed), not held or edited (b485a205):
     - address-verification-form 0/1, church-membership-form 0/1, proposal-form 0/3, vendor-application 0/2, identity-verification-form 1/2;
     - proposal-automation 0/2, returns-automation 0/1;
     - community-survey 3/4, mental-health-survey 1/4, school-climate-survey 0/1.
   - **petition-form** (64f01e00): the only candidate is off-sense. The kept Q3 now rejects under PA4 because of its answer source. The writer's edits were discarded.
   - **grievance-form** (d94ea185): its candidates pass the gate, but two are off-intent (one place-specific, one about a single union contract). Q1 still has a page-level PA12 problem from before the swap. The writer's edits were discarded.
   - **invoice-approval-workflow** (d0dacca4): the Q10 casing is fixed and Q1's answer is reworded, which clears PA1b. Q2 still rejects under PA5, and the only slot for it is the same question.
5. **Holds.** All pages were held before any edit (0af7a635) and unheld at handoff.

## Numbers

| | Count |
|---|---|
| Swap pages routed | 20 (19 swaps + invoice) |
| Reviewed | 7 |
| Left for A | 12 + invoice-approval-workflow |
| QC TOTAL / rejects on shipped pages | 0 / 0 |
| Flags on new items | PA6 on requisition Q3, compensation Q10, safety Q10, parent Q7 and Q9; invoice Q10 PA14 (from the casing) |
| AlsoAsked or Semrush calls | 0 |
| Writer tokens | 54k to 85k per page |

## Decisions

- **Replacements come only from code-built slots, in slot order.** Source: the request; DECISIONS ruling 18.3; ruling 15.2.
- **A gate pass is not enough when the candidate repeats a class Divit just removed.** Grievance-form was not shipped. Source: ruling 18.4 (sense and named-program checks).
- **Webflow:** none.

## Webflow calls

None.

## Not done

- 13 pages wait for A to re-park.
- **Notes for A's slim reviews:**
  - 5 shipped pages lost one related FAQ link along with the swapped item (QC passes).
  - 2 pages now have orphaned domain_sources entries (compensation, parent).
  - safety-survey's new Q10 answer is sourced to an exam-prep site.

## Open questions for Divit

1. The skeleton's `candidates()` admits questions that `paa --spec` then rejects through answer-source checks (invoice Q2 PA5, petition Q3 PA4). Should the skeleton apply the same source checks?
