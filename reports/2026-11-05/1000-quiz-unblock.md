# 2026-11-05 1000 quiz unblock: height fix state, CLS proof, one pre-publish checklist (B-quiz-2)

## Request
Divit 2026-11-05 item 3: "Quiz unblock in parallel: stage the style-quiz height fix; I'll publish staging (webflow.io) when you ask; CLS proof; then fold it into the one planned domain publish with the redirect CSV, which unlocks the 47 quizzes."

## Actions and results
- Read the state the dead 2026-11-03 agent left: the height reservation was written on 2026-10-23 (B-dev-23, logs/sqb.md; reports/2026-10-23/1504-quiz-embed-cls-reservation.md) into HtmlEmbed 117b49c2-044f-e98e-503d-a5470f7713be on the SurveyQuiz template 6ab24754757025d10940d06a. The 11-03 agent left only ops/quiz/cls.mjs (untracked) and two CLS runs in .cache/quiz/.
- Webflow, read-only: get_settings query_settings code on that embed. It contains the reservation rule (438 px, 435 px at 479 px and below), the same text as ops/quiz/embed.min.html.
- Both hosts serve the embed byte for byte (sha256 77032c85af45a950..., 15243 bytes) on /ai-survey-and-quiz-builder/team. The fix is already staged AND live; nothing to restage. **No Webflow write was made**, so no before-value was needed under childedits/2026-11-05/.
- ops/quiz/cls.mjs reviewed (stand-in method: the canaries are drafts and 404 on both hosts; carrier injected into the live team page exactly as exported; --direct for the real pages once item-published; --negative cancels the reservation). It is complete as written; committed unchanged.
- CLS on staging (BEFORE Divit's staging publish), 5 runs at 1440 and 390: PASS. Negative control FAILS as expected, so the measure sees the shift.
- Redirect v2 pre-check against production (read-only): 813/843 ok, 30 A11-redirect = exactly the 30 changed rows, 0 A11-target; /ai-landing-page-builder/resume is 200 (the v2 condition is met).
- Wrote the one checklist: reports/2026-11-05/planned-domain-publish-checklist.md.

## Numbers
- style stand-in: 1440 max 0.00059, 390 max 0.00089. vocabulary stand-in: 1440 max 0.00253, 390 max 0.00089. Control survey: 0.00089, mount display none, gap 0. Threshold < 0.01. Data reports/2026-11-05/quiz-cls-before.json.
- Negative (reservation cancelled), style: 1440 0.055-0.061, 390 0.0115 (FAIL, expected). reports/2026-11-05/quiz-cls-negative-control.json.

## Decisions
- No restage: the read-back equals the intended fix (task item 1: "if it is not staged or incomplete, restage"). DECISIONS 2026-10-23 "embed read-back must be hash-identical to ops/quiz/embed.min.html" (served bytes match; the API read contains the same rule text).
- No publish of any kind: CLAUDE.md NO SITE PUBLISH (Divit 2026-10-10).
- Redirect import by hand in Site settings (no Enterprise API): reports/2026-10-23/slug-migration-packet.md.

## Files changed and commits
- ops/quiz/cls.mjs, reports/2026-11-05/planned-domain-publish-checklist.md, quiz-cls-before.json, quiz-cls-negative-control.json, this report, reports/INDEX.md, logs/sqb.md. SHA in INDEX.

## Webflow calls
- webflow_guide_tool (session), data_element_settings_tool get_settings query_settings code on 6ab24754757025d10940d06a / 117b49c2-...: read only. No write, no item publish, no site publish. Rollback: none needed.

## Not done
- Staging publish, v2 import, production publish (Divit's).
- Canary item publish of style (6ad1d94e15d6a1e8ebe0b148) and vocabulary (6ad1d94e15d6a1e8ebe0b146): needs Divit's go after the domain publish.
- status/quiz-canary.json stays "pending".

## Open questions for Divit
- The quiz fix is already live on both hosts, so the staging publish is needed for the redirect v2 proof, not the quiz. Publish staging when the v2 CSV is imported?

AUDIT: last full run 2026-11-04 12:45 UTC, 417 pages, 280 fail (expected hero-backlog drift; 24 redir known issues)
