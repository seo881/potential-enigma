# B-side fixes Account A was waiting on: --by, holds, F2, PA12, AlsoAsked access, L12, releases

## Digest for Divit
- **Your message was addressed to Account A, but it landed in B's session (this one).** I did not act as A. I did the B-side items it presupposes, all pushed in f0a338f6:
  - `--by` is now required on claim, state, images, ready, review, release, hold and unhold;
  - hold markers (`hubctl hold` / `unhold`) are refused across accounts. B holds the 20 batch-3 pages;
  - **F2** accepts `alsoasked` on legacy-capture pages that have a pull;
  - **PA12** counts only the page's Semrush workbook secondaries, with a bar of min(6, that count);
  - `hubctl brief` prints the gated AlsoAsked candidates, so writers never read `private/`;
  - **L12**: the 3 Learn refs go into every new item's payload, and pre-flight has a column for them;
  - automated-loan-processing-system, sales-workflow and shipping-automation are released for A;
  - DECISIONS 2026-10-13, LESSONS, TWO_ACCOUNTS (holds, `--by`, gate, F2, PA12) and the Learn doc are updated.
  - Golden suite: 321 cases, 0 regressions.
- **I never received your 7 rulings or the 8-item advisor addendum.** A's report (1625) paraphrases them. Two of them change my work:
  - Ruling 1 apparently answers my batch-3 question (a "slim review").
  - Ruling 5 apparently says PA12 should accept **workbook keyword ideas** when a page has no secondaries. My PA12 fix lets such pages pass at 0, so it is more lenient.
  - **Please paste both texts here.** I'll align PA12 and run batch 3 on them.
- Batch 3 is still not in the CMS. Nothing is unhidden.

## Request
> (Addressed to Account A) git pull first (TWO_ACCOUNTS.md is the source of truth; rulings in DECISIONS 2026-10-13). Every state change and claim: --by A-w-<n> (hubctl will refuse without it after B's fix lands). Before working any rework page, put the hold marker on origin (per the updated doc). Gate: 0 rejects required. Never reword a verbatim AlsoAsked question to clear a flag... Wait for B's fixes to F2 / PA12 / read access before reworking the 3 pages parked for PA12... After B releases them: claim automated-loan-processing-system, sales-workflow, shipping-automation (Auto)... Report digest first.

## Actions and results
- **hubctl:**
  - `need_by` refuses missing IDs.
  - `hold` / `unhold` record `hold {by, t, note}` in status. `set_state`, `images` and `release` refuse the other account while a hold stands. Account = the `A-` prefix, otherwise B.
  - Every scripted caller already passes `--by`, so nothing breaks.
- **F2** (qc_hub): on a page with a legacy capture, the source `alsoasked` is accepted when the page has a pull, and raises F2 otherwise. Golden: f2-aa-legacy-pull and f2-aa-legacy-nopull.
- **PA12** (paa_gate): the bar is min(6, the page's Semrush workbook secondaries), and items labelled `secondary` count, since F2 checks the label against the workbook. Diff across 202 pages with pulls:
  - 6 pages with 0 workbook secondaries now pass that test (creator-application, credit-application-form, drug-test-consent-form, maintenance-request-form, refund-request-form, service-request-form);
  - employee-referral-form now fails honestly (1 of 2; it had been padded);
  - medical-history-form fails (5 of 6; already stopped).
  - Golden: pa12-no-workbook-secondaries.
- **AlsoAsked access:** `hubctl brief` prints the page's AlsoAsked candidates from both pulls, gated in memory (+ use, ? flag, x reject with codes). Nothing is written.
- **L12:**
  - `config/learn_refs.json` holds your 3 IDs.
  - `_field_data` fills `acrm---learn` when the spec has none.
  - `launch.py preflight` has a "Learn refs (L12)" column.
  - `hubctl learn-refs READBACK` refreshes the list from a Learn read. Tested: it would pick best-no-code-chatbot-builder as third; not applied.
- **Releases:** the 3 Auto pages went from claimed (weekend, 2026-10-10) to queued. No partial specs exist in either clone.
- **Holds:** B-coord holds the 20 batch-3 pages.
- **Docs:**
  - DECISIONS 2026-10-13 (Learn design, the unhide condition, two accounts, IDs/holds/gate, the F2/PA12/access fixes);
  - 2 LESSONS lines;
  - TWO_ACCOUNTS: the hold rule (replacing "B's batches win") and section 3b;
  - docs/LEARN_CAROUSEL_FIX.md correction box; plan/template-status T3 corrected; readiness regenerated;
  - the Designer checklist marked superseded;
  - A's 8 proposals answered in proposals/account-a.md.

## Numbers
- Golden: 321 cases, 0 regressions.
- PA12 changes: 8 pages (6 pass, 2 fail honestly).
- Holds: 20 (B).
- Released: 3.
- Webflow calls: 0 this step.

## Decisions
- PA12 bar "min(6, workbook secondaries)": my reading of A's proposal plus your "B's fixes to PA12". It may differ from your ruling 5 (open question 1).
- Hold markers replace "B's batches win": your message ("Before working any rework page, put the hold marker on origin").
- No recheck run after the F2/PA12 changes: a ratchet run now would rewrite state on A's live pages mid-wave. It runs at the next quiet point.

## Files changed and commits
- f0a338f6: ops/hubctl.py, ops/launch.py, qc/qc_hub.py, qc/paa_gate.py, tests/golden/*, config/learn_refs.json, DECISIONS.md, LESSONS.md, docs/TWO_ACCOUNTS.md, docs/LEARN_CAROUSEL_FIX.md, plan/template-status.json, proposals/account-a.md, status/*.json, status/readiness.md, logs/aab.md
- this commit: this report and the INDEX line

## Webflow calls
None.

## Not done
- Batch 3 into the CMS: waiting on your ruling 1 text, or a yes to my 1043 question.
- The read-only checks (`hubctl qc` / `paa`) still write files (A's proposal 4): backlog.
- `hubctl recheck` after today's rule changes.
- The throughput plan.

## Open questions for Divit
1. Please paste the 7 rulings and the advisor addendum into this session. They went to A's session only.
2. Your A-instructions also landed here twice. Please send them to the A session; I stay B.
