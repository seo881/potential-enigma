# 2026-10-21: full-throttle run to 316 (account B)

## Request
Divit, 2026-10-21 (from the session record; the prompt was pasted in chat):
1. Standing go for today (`.cache/standing-go-2026-10-21`): pages reviewed by an independent reviewer with 0 blocking, 0 flags and QC 0 are approved "by: standing-go (Divit 2026-10-21)"; re-check and ship the approved and reviewed pages in rolling batches.
2. Resume the writers and reworks.
3. Brand ruling: brand use cases may use the brand in FAQ questions, builder intent only, no implied partnership, and any statement about the brand's rules must be sourced.
4. "best ..." ruling: drop best/top/examples from the H1 and CTA, keep the full keyword in the meta and intro; golden tests.
5. Target 316 live, gates unchanged; A writes Form and SurveyQuiz, B writes LP and Automation and ships everything.
6. Live QC: confirm the live audit and publish watch run from this clone; full read-only live audit.
7. Token efficiency: pre-review gates, a rework-causes checklist, Sonnet for mechanical agents, no side investigations, easy pages first.
8. Session limits: don't end the run; resume after the reset.

Later the same day: approve contract-approval Q1 (PA7); allow "pdf" on pdf-automation; ship first with no new claims at about 80% session; write a resume note at about 95%; ship A's 11 reviewed pages; make every rework get a slim review; compare A's and B's writer setups; shipping was stalled, so ship in groups of 5; a SCIM ruling; then "gracefully stop" and "stop everything saving current work".

## Actions and results
- **Shipping:** item creates and item publishes ran in rolling groups, each with verify-live, through the ship agent B-ship-3 until it stalled at 11:43 IST. After that a group-of-5 script (`ship5.sh`) ran per hub; it is logged in `reports/2026-10-21/ship-groups.log`. No site publish.
- **Rules:**
  - PA7: Divit's flag decisions recorded in `rules/flag_decisions.json`; contract-approval Q1 added (11699e47).
  - PA15: "pdf" allowed on pdf-automation only (17034b26; golden cases pa15-pdf-*).
  - Skeleton: brand casing (b27f619c); acronyms NFT and HVAC with their articles (26dc3784).
  - `ship-check` now requires state reviewed or approved (c895982b).
- **Live audit:** the launchd jobs were repointed to this clone. The full read-only audit run hung and was stopped without results. The daily job has failed since 10-21 with "Not logged in" (see Open questions).
- **Writers and reviews:** about 45 B pages were written. Each got one independent review, and every rework got a slim review of the changed fields. `rules/rework-checklist.md` was created.
- **Recovered from three failures:**
  - A `hubctl recheck` run on a half-edited skeleton moved 23 Form pages to rework and re-stamped 81 specs. All of it was reverted; no state was kept.
  - The ship agent got stuck in a loop and was stopped.
  - The first run of the ship script hit a zsh argument bug.
- **artist-landing-page:** its draft held an unpublished Learn ref. The ref was swapped, the draft updated (api-update), and the page item-published.

## Numbers
- Live: 216 at the start of 10-21, 305 at the stop (+89; the target was 316).
- Commits on 10-21: 610. Item-publish commits with verify-live: 18. Rollback files: 45 (`childedits/2026-10-21/`).
- Golden: 967 cases, 3 regressions, all of them the long-standing allowed ones.

## Decisions (each with its source)
- Standing go: DECISIONS 2026-10-21; RUNBOOK section 5.
- Brand ruling: DECISIONS 2026-10-21; HUB_RULES section 8 (sourcing); `qc/paa_gate.py` PA14 exempts the page's own primary.
- "best" ruling: DECISIONS 2026-10-21; skeleton head_phrase (fb37278c).
- PA7 approvals: `rules/flag_decisions.json` (Divit, 2026-10-16 and 2026-10-21).
- Grouped table entry banned, single-vendor cells only: `rules/rework-checklist.md` item 4; `rules/competitors/lp.json`.
- Account split: `docs/TWO_ACCOUNTS.md` "2026-10-21 split".

## Files changed and commits
The rule and code commits are 11699e47, 17034b26, b27f619c, 26dc3784, c895982b and fb37278c. The final saves are b6442b53 (shipping records and the resume note) and 45c07257 (on 10-23).

Other files changed:
- `rules/rework-checklist.md`, `rules/flag_decisions.json`, `rules/paa_blocklist.json`, `rules/paa_patterns.json`.
- `qc/paa_gate.py`, `ops/skeleton.py`, `ops/hubctl.py`.
- `tests/golden/cases.jsonl`, `DECISIONS.md`, `docs/TWO_ACCOUNTS.md`.
- About 45 specs under `specs/lp/` and `specs/aab/`, with their images.

## Webflow calls
- **Types:** Data API item create (`isDraft: true`), item publish (`publish_collection_items` of the changed items only), item update (artist Learn ref; relinks).
- **IDs and before/after:** each call's before-value is committed in `childedits/2026-10-21/*.before.json` and its rollback in `*.rollback.json`. Calls are logged in `logs/{lp,aab,form,sqb}.md` and `logs/api/2026-10-21.jsonl`.
- **Rollback:** `hubctl api-update <rollback.json> --live` for updates; unpublish, then delete the draft for creates.
- **No site publish.** style-quiz and vocabulary-quiz were never touched.

## Not done
- 316 live was not reached on 10-21.
- At the stop, 14 B pages had passed ship-check but were not shipped. They shipped on 10-23 under Divit's resume go.
- The full live audit has no results, and the daily audit job is broken by its login.
- The skeleton default hero prompt ("saves every signup") and the related-link picker (off-topic sibling links) are logged but not fixed.

## Open questions for Divit
- The daily live-audit job fails with "Not logged in" under `CLAUDE_CONFIG_DIR=~/.claude`. Run `CLAUDE_CONFIG_DIR=~/.claude claude /login`, or should it use another account?
- Should the default hero prompt be rewritten per hub (service pages say "request", not "signup")?
