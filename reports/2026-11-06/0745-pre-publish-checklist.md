# 2026-11-06 0745 pre-publish checklist (B-pub-1)

## Request
Divit 2026-11-05 (pasted): "No Domain publish ever from your end, before I import or publish anything, give me the single pre-publish checklist, all green: a) the quiz height fix proven on staging (if not done yet, stage it and ask me for a staging-only publish; CLS proof: 5 runs at 1440 and 390, under 0.01); b) a staged-vs-live diff across all collections: exactly the intended changes and NOTHING from the held hero-prompt backlog (if any hero updates are staged, unstage them); c) the redirect CSV: every row's target returns 200 (including the resume target), 0 chains, existing rows kept, final row count; d) any other staged template or page changes listed. Then the steps for my CSV import and the one domain publish. After it's live: I give the go for the style and vocabulary quiz items."

## Actions and results
- a: served embed byte-identical on both hosts; staging CLS 5x1440 + 5x390 PASS (all under 0.01). GREEN.
- b: GET-only read of all 32 collections, staged and live, compared field by field. Hero backlog 280/280 identical, so nothing was unstaged. Child collections: only intended drafts. RED: 14 published Learn items carry staged content edits that a domain publish would ship (not ours).
- c: v2 CSV 843 rows, 0 chains, 0 duplicate sources, all v1 sources kept, 30 changed targets; production 0 A11-target. Staging showed one transient 500 per run, which was 200 on recheck. GREEN.
- d: not readable (the token lacks pages:read; the Webflow MCP is denied in this session). Site lastUpdated is later than the domain publish. RED pending Divit's Designer check.
- The first pass ran on 2026-11-05 at about 10:40 UTC; the session paused, and every check was re-run fresh on 2026-11-06 at 07:30-07:45 UTC. The checklist uses the fresh numbers.

## Numbers
Quiz CLS max 0.00059 (1440) and 0.00089 (390) for both stand-ins. Redirects: 843 rows, 771 targets, 813/843 pass on production today, and the 30 that fail are exactly the changed rows. Staged-vs-live: 37 live items with changes in draft, 49 never-live drafts, 14 Learn items with staged changes, 0 in child collections.

## Decisions
- No unstaging write: there was nothing to unstage (task b; CLAUDE.md "read before every write").
- Learn items not touched: config/collections.json covers child collections only (CLAUDE.md non-negotiables).
- No publish of any kind (CLAUDE.md NO SITE PUBLISH).

## Files changed and commits
reports/2026-11-05/pre-publish-checklist.md, reports/2026-11-05/pre-publish-staged-diff.json, reports/2026-11-05/quiz-cls-staging-prepublish.json, this report, reports/INDEX.md. SHA in INDEX.

## Webflow calls
REST GET only: /sites/{id}, /sites/{id}/collections, /collections/{cid}/items and /items/live for 32 collections; /sites/{id}/pages returned 403. No write, no publish. Rollback: none needed.

## Not done
- d1 (page and template staged state): needs Divit in the Designer.
- b3 (Learn staged edits): needs KS or Divit.

## Open questions for Divit
- Are the 14 staged Learn edits OK to ship with the domain publish? Default: ask KS to item-publish them first, so the publish is a no-op for the CMS.
- Should the GET-only all-collections diff script go into ops/ (read only, outside the write allowlist)? Default: yes, as a separate read-only module.
- The 07:28 Mac audit run hit a network drop (552 transport errors): re-run it whole.

AUDIT: last full run 2026-11-06 07:28 UTC, 436 pages, 563 fail (552 transport; run invalid)
