# Redirects v3 and site-publish checklist (B-redir-3)

## Request
Divit 2026-11-17: "Redirects: prepare the final CSV (843 rows plus the 30 fixes, all targets 200) and a pre-publish checklist for my site publish this week."

## Actions and results
- Reconciled "the 30 fixes". They are the 30 rows of reports/2026-11-03/redirects-final-v2.csv whose target differs from the live set reports/2026-10-23/redirects-final.csv. Those rows point at exactly the 24 old targets behind the `redir-*` known issues: 21 are chains and 3 are 404s. Today's audit adds nothing. The other 813 targets return 200, and no target is a renamed or non-live child slug.
- Built reports/2026-11-17/redirects-final-v3.csv: the v1 bytes format (CRLF, header `source,target`, v1 row order) with the v2 targets. Its content is identical to v2.
- Added ops/redirect_set_check.py, a file-level pre-import check: header, paths, duplicate, self-loop, chain, shadowing of a live child or hub page, a hub target that is not live, and every target 200 with no redirect followed. Golden kind `redirect-set` covers it with 8 cases. Full suite: 1254 cases, 0 regressions.
- Verified v3 against production: 0 failures (reports/2026-11-17/redirects-v3-verify.md).
- Wrote reports/2026-11-17/site-publish-checklist.md.

## Numbers
843 rows, 843 distinct sources, 771 distinct targets, 771/771 returning 200 (5 after one re-fetch of a transient 5xx), 30 targets changed, 0 added, 0 dropped, 0 findings. Child CMS staged: 0 of 646. Learn staged: 0 of 769.

## Decisions
- v3 content = v2: DECISIONS 2026-11-03 (repoint the 21 chains; leadpages -> LP hub; dating and resume -> the closest live page) and reports/2026-11-03/redirects-v2-changes.md. The resume condition is now met (200).
- Not asking Divit to import, only preparing: DECISIONS 2026-11-06 (parked housekeeping) and CLAUDE.md NO PLAN DEPENDS ON A SITE PUBLISH. This order came from Divit himself.
- rules/live_audit.json not edited: this was the coordinator's instruction.

## Files changed and commits
ops/redirect_set_check.py, tests/golden/run.py, tests/golden/cases.jsonl, reports/2026-11-17/{redirects-final-v3.csv, redirects-v3-verify.md, site-publish-checklist.md, this report}, reports/INDEX.md. SHA in INDEX and the handback.

## Webflow calls
None. Only public HTTPS HEAD and GET requests to emergent.sh, plus read-backs other agents had already cached today.

## Not done
- The staged state of the other collections and of Designer pages and styles: not readable without a Webflow call. Divit checks the publish dialog (checklist D1).

## Open questions for Divit
- Should the font-loading head fix (reports/2026-11-11/font-loading-proposal.md) go into this publish? It is optional.

AUDIT: last full run 2026-11-16 14:11 UTC, 646 pages, 270 real fail
