# Resume note, B, 2026-10-21 (stopped by Divit, 11:33 UTC)

Live: 305 of 316 (today +89). Everything is committed; no agent, ship script, monitor or cron is running (cron 7300f1a1 deleted).

## Ready to ship (ship-check passes; run scratchpad ship5.sh LP lp, then Auto aab, in groups of 5)
- LP approved: developer, interactive. LP reviewed: contractor, membership, nft, roofing, wedding.
- Auto reviewed: abandoned-cart, appointment-reminder, data-sync, leave-approval, manufacturing-workflow, nonprofit-workflow, review-request.

## Needs review (state images, QC 0, gate 10/10): e-signature-workflow, vendor-onboarding-workflow.
## Rework: notification-automation. FAQ 3's 153-character segment figure is GSM-7 only, but it sits after the UCS-2 sentence (67). Keep Twilio's scope. Then a slim review.
## Divit decisions
- mental-health-landing-page: Q1 (PA7 definition) and the quoted 988 Lifeline mention. Reviewed 10/10.
- coaching-landing-page: re-approve (step 7 "included" only; slim review passed; the standing go can't clear QC R3).
- user-provisioning-automation: held for the SCIM exception to QC C2 (ruling in DECISIONS 2026-10-21).
## Claimed, no writer: insurance-landing-page, patient-intake-automation (YMYL, deferred).
## Fixes logged
- Skeleton default hero prompt "saves every signup" fits no service page (fixed by hand on hvac and roofing).
- The related-link picker gives off-topic sibling links.
- ship5.sh: zsh word-splitting broke the first run. Always call it with explicit args. sync now retries until pushed.
- NFT and HVAC acronyms added (26dc3784).
