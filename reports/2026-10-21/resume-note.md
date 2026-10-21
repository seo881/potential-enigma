**FIRST: ship the waiting queue.** Run the group-of-5 ship script (scratchpad ship5.sh, logic: standing-go approve reviewed pages that pass ship-check and aren't held, then api-read, cms-check, api-create --limit 5, api-publish --only <drafts> --verify-live, a sync after each step) for Auto, LP, SurveyQuiz, Form until no approved page is left. Progress: reports/2026-10-21/ship-groups.log. The ship agent B-ship-3 got stuck at 11:43 IST and was stopped. Nothing else runs before the queue is empty.

# Resume note, B session, 2026-10-21 (written at about 90% session)

Live: 243 of 316. Rulings applied this session: contract-approval Q1 approved (rules/flag_decisions.json, 11699e47); PA15 allows "pdf" on pdf-automation only (17034b26, golden cases in b27f619c); brand casing in skeleton (b27f619c).

## Mid-flight when the session ended
- Ship agent B-ship-3 (sonnet, rolling): ships every page that is reviewed or approved and passes ship-check, A's 11 included. HELD until cleared: custom-order-form, remote-work-survey, instagram-landing-page, linkedin-landing-page. If it stopped, restart one sonnet ship agent with the same rules (CLAUDE.md 7 and 7b; no site publish; never style-quiz or vocabulary-quiz).
- B-fix-1 (sonnet): custom-order-form, "built into Emergent" changed to the approved "included" wording (unlocked fields only).
- B-r-107 reviewer, in order: full review of budget-approval-workflow and linkedin-landing-page; slim review of instagram-landing-page (faq and hero_prompt casing); slim review of remote-work-survey (A's rework: numbers and chart); full review of whitepaper-landing-page; slim review of custom-order-form once B-fix-1 has committed. Pages that pass go to the ship agent.
- B writers still running: podcast-landing-page, chiropractic-landing-page, coaching-landing-page, user-provisioning-automation, interview-scheduling-automation, pdf-automation (B-w-277). Each one that reaches state images needs one independent full review.
- The live audit (hubctl live-audit --all --dry) was running; its log is in the session scratchpad. Re-run it into audits/live/2026-10-21 if its results are missing, and fix real P0/P1 first.

## Next after the reset (Divit 2026-10-21 items 4 and 5)
1. Check git log, status/*.json and logs/; recommit anything uncommitted, but only after reading it. Never run hubctl recheck while a rules or skeleton edit is uncommitted: that is how 23 Form pages were wrongly moved to rework this session (I reverted them).
2. First-pass yield (Divit item 2): A passed 11 of 12 reviews today, B 2 of 9. Compare A's writer setup (prompt, pre-review checklist, the QC and gate run before review) with B's, apply A's to every B writer prompt, and report the difference in one line.
3. Scale up to at least 15 writers on LP and Automation (claims: easy builder-intent first), with matching reviewers and continuous shipping toward 316.
4. Post-sprint fixes: the skeleton default hero prompt drops its article ("Build low stock alert..."); the related-link picker offers off-hub anchors (low-stock got proposal automation, leadership survey and likert questionnaire); lowercase anchors ("likert", "it automation" in calendar-automation FAQ 4).

## Update (later, same session)
- Cleared for shipping since the note: budget-approval, instagram, remote-work-survey, whitepaper, custom-order, interview-scheduling, podcast, chiropractic, microsite, lead-routing, calendar.
- Rework writer B-w-278: linkedin-landing-page (FAQ 5 and 6, LinkedIn scope) and user-provisioning-automation (FAQ 3, Okta SCIM scope), then `hubctl ready`. coaching-landing-page howto_step_7_des changed from "built into Emergent" to "included" (Divit's custom-order rule).
- After B-w-278: a DIFFERENT agent slim-reviews the changed fields on all 3 pages (Divit item 3); then ship.
- pdf-automation writer (B-w-277) still running; it needs one full review.
- Proposal: add a QC check for the "built into Emergent" wording, which QC doesn't catch (found on 2 pages).
- SCIM ruling (Divit 2026-10-21): user-provisioning-automation may name SCIM as the provisioning standard, sourced (RFC 7644 or the IdP docs). Never claim Emergent has built-in SCIM support unless it is in rules/claims.json; say an app built with Emergent can connect to identity providers. QC C2 currently blocks the word SCIM, so C2 needs an exception (standard named with a source, no Emergent claim) plus a golden test, then rework FAQ 3, slim review, ship. The page is held until then.
- Holds (B-c-1): coaching, linkedin (slim reviews, B-r-110), user-provisioning (SCIM).
- artist-landing-page: draft item 6ad86401 exists (recorded). Learn ref 6a17299f is an unpublished Learn article, so verify failed. Swap it for a published ref (learn-match), slim review, ship-update the draft, unhold, publish. Held by B-c-1.
- After the ship chain: rerun ship5.sh for LP (chiropractic, podcast, whitepaper) and Auto (pdf-automation).
