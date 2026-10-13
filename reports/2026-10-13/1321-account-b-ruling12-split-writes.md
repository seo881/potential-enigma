# Account B: ruling 12 split writes, pilot pages, A's slim-review reworks (2026-10-13)

## Request

> Ruling 12: you never run AlsoAsked pulls; A runs them all and you reuse saved pulls (0 credits). Do not debug the 403.
> 1. Now: for the pilot pages in your hubs that reach 10 with their top-2 PA3 synonyms (reports/2026-10-13/1400-yield-pilot-throughput.md), claim them and write everything except the FAQ (plan, hero, features, tabs, how-to, table, image brief). Leave them claimed; fill the FAQ the moment Divit approves the phrases and A lands them in rules/paa_synonyms.json, then QC 0, 0 rejects, images, hand to A.
> 2. Then claim only from the top of plan/queue-ranked once A publishes it; same split-write for pages pending synonyms.
> 3. Parked pages: only those A releases.
> 4. Append a corrected usage row for sales-workflow (the real token count, note "corrects 0 row").
> Up to 10 writer subagents in parallel. Report per CLAUDE.md, under 15 lines in chat.

## Actions and results

1. **Pilot pages claimed.** These are the 13 pages in B's hubs that the 1400 report puts at 10 or more with their top-2 synonyms.
   - `hubctl claim` takes pages only from the top of the queue and skips any that fail feasibility, so each page was claimed directly with `hubctl state <url> claimed --by B-w-<n>`, then held.
   - shipping-automation and automated-loan-processing-system were held too (7e436c97).
2. **Split writes: 12 pages written except the FAQ.** In each, QC's only P0/P1 is S1, the empty FAQ. Each is one commit, and the page stays claimed and held:
   - Form: check-in-form (4e54b3a1), check-request-form (cf7bd8bd), home-inspection-form (9ae0f801), attendance-form (0b9a7aba);
   - SurveyQuiz: dei-survey (7fc136b4), pricing-survey (8fb74201), culture-survey (f9c11309), restaurant-survey (d280cfe9);
   - Auto: order-processing-automation (2648e2e8), recruitment-automation (432fbd93), property-management-automation (70691cd4), automated-loan-processing-system (e04c613d), restaurant-automation (56c417b4).

   `hubctl init` moved most of these pages from `claimed` to `spec`. hubctl still refuses `qc_pass` while the FAQ is pending. shipping-automation already had its spec from earlier.
3. **content-approval-workflow** reaches 10 today without synonyms. It was written in full: QC 0, gate 7/0/3 with PA6 flags on Q4, Q7 and Q10. It went to `images` for A's review (6d8e2620).
4. **A's slim-review reworks**, both now `reviewed` and checked with `hubctl verbatim`:
   - hotel-booking-form: FAQ 2's verbatim original fails PA3, so it was re-sourced as a keyword question (ed29968c).
   - model-release-form: FAQ 7 restored to verbatim (e00703d6). It has 1 flag, Q5 PA6.
5. **Ranked queue.** Claimed queue-ranked #1, employee-handbook-acknowledgment-form, the only `ready` page in B's hubs (24f34284).
   - The writer stopped before writing: QC cannot reach 0 under the current rules.
   - Cause: the workbook spells "acknowledgement", H2 requires "acknowledgment", and there is no variant group linking them. Both passing AlsoAsked questions use the UK spelling.
   - The rules ask is in proposals (5b44780d). The page stays claimed and held.
   - Every other B page in the queue is `no-pull` and waits for A's pull wave.
6. **Usage correction.** A row was appended for sales-workflow with B-w-7's real count, noted "corrects 0 row" (7e436c97). That count is the same run as the 11:18 UTC row, so it should be counted once.

## Numbers

| | Count |
|---|---|
| Split-write specs committed, waiting on synonyms | 13 (12 today plus shipping-automation's earlier spec) |
| Pages to `images` for A's review | 1 (content-approval-workflow) |
| Reworks to `reviewed` | 2 |
| Blocked by rules | 1 (employee-handbook-acknowledgment-form) |
| AlsoAsked pulls or credits by B | 0 |
| Writer tokens | split writes 125-158k each (median about 135k); full new page 172k; reworks 50-53k; blocked page 79k |

## Decisions

- **Split write until synonyms are approved.** Source: ruling 12 part 5; TWO_ACCOUNTS 3d.
- **Pilot pages claimed with `hubctl state` rather than `hubctl claim`.** `claim` reads the queue top-down and skips these pages, and the request named them explicitly.
- **content-approval-workflow written in full.** Its feasibility is 10/10 today, so it needs no synonyms.
- **Rules conflicts go to proposals.** B never edits rules/ (TWO_ACCOUNTS).
- **Webflow:** none.

## Files changed and commits

- **Paths:** `specs/form/*`, `specs/sqb/*`, `specs/aab/*`, `images/aab/content-approval-workflow`, `images/form/{hotel-booking,model-release}-form`, `status/{form,sqb,aab}.json`, `status/usage.jsonl` and `proposals/account-b.md`.
- **Commits:** 7e436c97, 4e54b3a1, cf7bd8bd, 7fc136b4, 9ae0f801, 8fb74201, 2648e2e8, 0b9a7aba, f9c11309, d280cfe9, 6d8e2620, 432fbd93, 70691cd4, 24f34284, e04c613d, 56c417b4, ed29968c, e00703d6 and 5b44780d.

## Webflow calls

None.

## Not done

- **FAQs for the 13 split-write pages.** They wait on Divit approving phrases and A landing them in `rules/paa_synonyms.json`.
- **No further claims.** The rest of B's ranked queue is `no-pull`.
- **No parked rescues.** A has released none to B by name.
- **`faq_pending` not set.** The pilot pages were claimed through `hubctl state`, so they don't carry `faq_pending`. hubctl still blocks `qc_pass` because their FAQ is empty.

## Open questions for Divit

1. **employee-handbook-acknowledgment-form.** It needs a spelling variant group, and an H2 exemption for verbatim AlsoAsked text, before it can be written. Approve both?
