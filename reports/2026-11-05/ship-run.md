# Ship run, 2026-11-05 (B-ship-7, the only ship agent)

## Request
Coordinator brief (B-c-1), relaying Divit 2026-11-05: "Independent reviews as pages land; ship each the moment it passes (standing go for 0-flag pages recorded with go-record; groups of 10; verify-live in parallel; post-ship audit). Flags to me in one packet." Scope: new pages only (today's claims); the hero-prompt backlog on live pages is on hold. Later relays: Divit's session limit at 10% (ship every passing new page now, no 10-minute re-check loop); a ruling to hold 9 pages for rework (cross-field mismatch, patient health details over Slack/DM); and then the release of benefits-enrollment, bankruptcy-intake and employee-training after their fixes.

## Actions and results
- **Shipped: 19 new pages, all item publishes, 0 publish errors, verify-live 19/19 PASS.** No site or domain publish, no use of the Webflow sites tool, no slug change, no update to any page that was already live.
- Each page passed ship-check, then got go-record (standing go, by B-c-1) and `state approved --by standing-go`. After that: a fresh api-read, cms-check, bulk-payload at the approval SHA, and an api-create before-value that was committed and pushed before `--live`. The publish followed the same before-value step, using `--live --verify-live`.

| Hub | Shipped | Pages |
|---|---|---|
| LP | 7 | g1 yoga, telehealth, tiktok · g2 solar, youtube · g3 short-form, spa |
| Form | 12 | g1 acupuncture-intake, calculator, candidate-screening, case-study, chiropractic-intake, cleaning-quote, coaching-application · g2 dj-booking, construction-quote · g3 benefits-enrollment, bankruptcy-intake, employee-training |
| Auto | 0 | patient-intake was created as a draft; the publish was refused by its hold |

- **Auto-relink** (inside api-publish): /ai-form-builder/job-application had its FAQ field updated to link to candidate-screening and was item-published. Read-back was clean and verify-live passed. Rollback: childedits/2026-11-05/relink-auto-20261105T102319Z.20261105T102320Z.rollback.json.
- **Group log:** reports/2026-11-05/ship-groups.log.

## Numbers
- **Live** (status/live.json after the last publish): LP 110, Form 184, Auto 79, SurveyQuiz 63, **total 436**. The morning count was 417; 417 + 19 = 436.
- **Drafts in Webflow:**
  - Auto patient-intake (held; its draft holds the OLD content and needs an update, not a create)
  - Form creator-application
  - SurveyQuiz style and vocabulary (untouched)
- **Create counts on fresh reads:**
  - LP 103 -> 106 -> 108 -> 110
  - Form 173 -> 180 -> 182 -> 185
  - Auto 79 -> 80
  - Each step equals the number created, and each create was bulk-verified with 0 mismatches.

## Decisions
- Approvals follow DECISIONS 2026-10-26 (a recorded go): status/go/2026-11-05.json plus .cache/standing-go-2026-11-05, through `--by standing-go` only.
- **Divit's ruling on holds arrived after 5 of the 9 named pages were live:** chiropractic-intake, acupuncture-intake, cleaning-quote, coaching-application (Form) and solar (LP). I did not unpublish them, as the ruling says, and reported them to B-c-1 at once. Their spec fixes wait for Divit's go; I made no live updates.
- **patient-intake:** the publish was refused by B-c-1's active hold. This refusal is correct; I recorded it and did not retry around it.
- **Push race:** the shared clone's HEAD kept moving with other agents' local commits, so the before-value guard ("commit is not pushed") refused several `--live` calls. I retried each one after `git push`, with no change to the guard.

## Files changed and commits
- B-ship-7 commits: c19f7830, 8ad75669, 286ee230, 6cc10aa9, 44e8f742, 7075fcfc, cef8b3c7, aac3aa08, ea345696, 76d02007, 58ac0a7d, c95dc137, 73c63001, cc0f8076, f8f84014, f8ca3626, 72ea3fea, 801d04a7, 8aa332c5, 6c20d647, f4c4903c, 9aad61f2.
- Before-values and rollbacks: childedits/2026-11-05/*.

## Webflow calls (all through `hubctl api-*`, Data API, logged in logs/<dir>.md and logs/api/2026-11-05.jsonl)
- **Creates (drafts, isDraft true):**
  - LP 3 (8ad7566), LP 2 + Form 7 + Auto 1 (cef8b3c), LP 2 + Form 2 (c95dc13), Form 3 (801d04a).
  - Rollback: delete the item IDs in childedits/2026-11-05/*.api-create.*.rollback.json.
- **Item publishes:** 6 calls, 19 items, 0 errors.
  - Before-values are in *.api-publish.*.before.json; rollback = unpublish the IDs in the rollback files beside them.
  - The Auto publish before-value (49a47757) was written, but the publish was refused (hold), so nothing was sent.
- **Update:** 1 relink (job-application FAQ field), followed by an item publish.

## Post-ship audit
- **Not yet scored.** The full daily run (pid 26582, started 09:00 local) is still in its serial transport-retry phase: 144 of 375 pages by 16:21 local. Almost every retry failure is the known hero-prompt chip backlog, which is on hold. The checks lock makes every post-ship run wait for it.
- I replaced my three queued post-ship runs with one detached run covering all 19 shipped pages plus job-application: `postship-2026-11-05`, log .cache/live/postship-2026-11-05.log, output audits/live/2026-11-05/postship-2026-11-05/. It starts when the full run releases the lock. Its results are not in this report.

AUDIT: last full run 2026-11-04 12:45 UTC, 417 pages, 304 fail (280 real; the hero-prompt backlog)

## Not done
- patient-intake: waits for B-c-1's word, then needs an update of the existing draft (not a create) and a publish.
- The post-ship audit result for today's 19 pages is pending (see above).

## Open questions for Divit
- Do the 5 pages that went live before the hold ruling (chiropractic-intake, acupuncture-intake, cleaning-quote, coaching-application, solar) get their spec fixes pushed live now, or stay as they are until your go?
