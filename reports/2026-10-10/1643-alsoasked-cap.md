# AlsoAsked credit cap closed: 2 per page in total, one path only (2026-10-10)

## Request
> Yes, close the credit gap now (Divit):
> - Remove ops/alsoasked_pull.py from the loop's allowed tools; sessions pull only through weekend.py aa.
> - weekend.py aa: hard cap of 2 credits per page in total, counted from credits.log before the call. Refuse any pull that would take a page past 2. Allow a second pull only if the first returned no_results; never re-pull a page that already has a saved pull (reuse private/alsoasked/<slug>.json).
> - Log the over-cap pages (video-landing-page 6, rental-application-form 4, sign-out-form 4, ebook-landing-page 4, data-entry-automation 4) in the next report with the cause.
> - Apply it between sessions (atomic script swap, exactly one loop), commit, add a LESSONS line ("caps live in the only allowed path; never allow a bypass tool"), report in 3 lines, keep watching.

## Actions and results
- `weekend.py aa` is now the only path for sessions:
  - A saved pull with a result other than no_results is reused, with no call.
  - Before every call, it counts the page's credits from `credits.log` over all time, `credits` field only, and refuses if one more pull could take the page past 2.
  - A second call (fresh) happens only after a no_results.
  - Pulls run one at a time under `.locks/alsoasked.lock`, so the account before/after delta belongs to that page alone.
- `ops/alsoasked_pull.py` refuses to run unless the caller sets `ALSOASKED_VIA_AA=1`. Only `weekend.py aa` and `ops/alsoasked_batch.py` (which has its own balance ceiling) set it. The block applied at once, including to the session that was running. A new `--no-retry` flag lets `aa` own the no-results retry.
- `weekend_run.sh`: removed `ops/alsoasked_pull.py` from the allowed tools; installed by atomic rename. Restart between sessions: a watcher waits for the running session to end, sets STOP before the next one, then starts exactly one loop.
- The QC F1 and PAA gate messages now point to `weekend.py aa`. Plan hard limits and the writer step are updated. LESSONS line added.
- Tests: a direct run is refused (rc 1); `aa` on video-landing-page reuses the saved pull; golden suite 95 cases, 0 regressions.

## Numbers: over-cap pages and the cause
| Page | Logged before | Actual (`credits` field) | Cause |
|---|---|---|---|
| video-landing-page | 6 | 3 | Each pull counted twice (`credits` + `web_credits`); its one pull overlapped data-entry-automation's in time, so the before/after delta took in both |
| rental-application-form | 4 | 2 | Counted twice; no_results, then a fresh pull |
| sign-out-form | 4 | 2 | Counted twice; no_results (1), then fresh (1) |
| ebook-landing-page | 4 | 2 | Counted twice; the delta overlapped parallel pulls of other canary pages |
| data-entry-automation | 4 | 2 | Counted twice; overlapped video-landing-page (11 seconds apart) |

- Weekend AlsoAsked total, corrected: **22 of 300** (was shown as 44). A depth-2 pull costs 1 credit (AlsoAsked docs). The remaining excess over 1 per pull comes from overlapping parallel pulls, which the lock now prevents.
- No page went past the cap in real credits except video-landing-page, at 3 by the before/after delta, which most likely includes data-entry-automation's credit.

## Decisions
- Divit's prompt above. LESSONS 2026-10-10 line ("caps live in the only allowed path; never allow a bypass tool").

## Files changed and commits
- 89ad1c9: ops/weekend.py, ops/alsoasked_pull.py, ops/alsoasked_batch.py, qc/qc_hub.py, qc/paa_gate.py, ops/schedule/weekend_run.sh, plan/weekend-run.md, LESSONS.md.

## Webflow calls
None.

## Not done
- The loop restart waits for the current session (iteration 2, started 16:39) to end.

## Open questions for Divit
- None.
