# Ship run, 2026-11-06 (B-ship-8, the only ship agent)

## Request
Coordinator brief (B-c-1), relaying Divit 2026-11-06. The absolute rule: "no sitewide publish ever from your end, only publish the cms items".

The brief:
1. Ship the 7 rulings-1-2 fixes Divit re-approved (2f9007e7):
   - 5 live pages get a changed-fields update and an item publish.
   - patient-intake's existing draft is updated, then item-published.
   - cleaning-quote is excluded.
2. Run the post-ship audit and the auto-relink.
3. Stay as ship agent for 4 hours. Ship new reviewed pages that pass ship-check under the standing go (go-record, then approved --by standing-go), in groups of up to 10, with verify-live and a post-ship audit.

Later relays from B-c-1:
- cleaning-quote cleared.
- The quiz canary: style first, a production CLS proof, then vocabulary.
- Holds on health-coaching-intake and home-insurance-quote.
- Six more Form pages to add.
- massage-booking and cleaning-quote wait for Divit's R3 re-approval.
- Vocabulary held.

## Actions and results
- **Item publishes: 21 pages, 0 publish errors, verify-live 21/21 PASS.**
  - No site or domain publish. The Webflow sites tool was not used, and no slug changed.
  - Every write went through `hubctl api-*`. Each before-value was committed and pushed before its `--live` call.

| Group | Hub | Pages | Kind |
|---|---|---|---|
| r12 fixes | LP | solar, telehealth | live pages, changed fields only |
| r12 fixes | Form | chiropractic-intake, acupuncture-intake, coaching-application | live pages, changed fields only |
| r12 fixes | Auto | patient-intake | existing 11-05 draft updated (no second item), first publish |
| g1 | Form | event-booking, family-law-intake, financial-planning-intake, guest-list, gym-membership-cancellation, landscaping-quote, moving-quote | new |
| g2 | Form | makeup-consultation, mentorship-application, influencer-application, event-waiver, little-league-registration, nutrition-intake | new |
| quiz canary | SurveyQuiz | style | draft updated (hero prompt), first publish |

- **Auto-relink:** after g2, liability-waiver's FAQ got a link to event-waiver. The item was published and verify-live passed.
- **Quiz canary:** the production CLS test FAILED at 390 px.
  - Style at 390: max 0.06127; all 5 runs were over the 0.01 limit.
  - Style at 1440: max 0.00074, a pass.
  - The control page passed at both widths.
  - Data: reports/2026-11-06/quiz-cls-production-style.json.
  - I stopped there, as the brief said: vocabulary was not published and status/quiz-canary.json stays "pending". Style is still live (unpublish is not on the API allowlist). I reported this to B-c-1. B-quiz-3 has since traced the shift to the hero font swap (reports/2026-11-06/quiz-cls-390-investigation.md).
- **Post-ship audits:** every page shipped today was covered, and all were clean.

| Run | Pages | P0 | P1 | P2 |
|---|---|---|---|---|
| postship-2026-11-06-r12 | 6 | 0 | 0 | 6 |
| postship-2026-11-06-form-g1 | 7 | 0 | 0 | 7 |
| postship-2026-11-06-form-g2 (with liability-waiver and style) | 8 | 0 | 0 | 8 |

- **Watch loop:** I polled every 10 minutes until the 4-hour window closed. The only candidates were held pages, so nothing new shipped after g2. Writing was stopped by Divit.

## Numbers
- **Live** (status/live.json): LP 110, Form 197, Auto 80, SurveyQuiz 64, **total 451**. That is the morning's 436 plus 15 first publishes. The other 6 publishes re-published pages that were already live.
- **Create counts on fresh reads:**
  - Form 185 -> 192 -> 198. Each step equals the number created; bulk-verify mismatches: 0.
  - LP 110, Auto 80 and SurveyQuiz 65 are unchanged; I updated drafts there and created nothing.
- **Drafts left in Webflow:** Form creator-application, and SurveyQuiz vocabulary (updated; held by B-c-1).

## Decisions
- **Approvals:**
  - The 6 fix pages: Divit's own re-approval (status/go/2026-11-06.json, 2f9007e7).
  - The 13 new Form pages: the standing go (.cache/standing-go-2026-11-06), go-record by B-c-1, then `--by standing-go`. This follows DECISIONS 2026-10-26.
  - style: Divit's named go, recorded by B-c-1.
- **cleaning-quote:** `state approved` accepts only `--by divit` (R3) or the standing go. I did not run `--by divit` in Divit's name, and I did not stretch the standing go (new pages only) to cover a live page. It is on Divit's re-approval list, as his own quote anticipates.
- **massage-booking:** approved at 07:53. At 07:55 B-c-1 unlocked its FAQ for ruling-2 fixes, so I held it before its create. The fix (df6bedbc) and slim review (8675cdbd) have landed, but it now fails ship-check on R3. It stays held by B-ship-8 until Divit re-approves it, as B-c-1 asked.
- **home-insurance-quote / health-coaching-intake:** held by B-c-1 (Q1). api-create refused home-insurance-quote, which is correct. It is still in state approved, with no item.
- **Image base sha:** api-create never records `cms_draft`, so ship-update could not see re-rendered images on these 8 pages. I recorded the create's bulk-payload sha as `cms_draft.sha` (r12: cef8b3c7 and 8ad75669; quiz: 7d1d6cee). This field is outside the fingerprint. ship-update then sent exactly the images that changed since the create.
- **Quiz image "mismatches":** api-update reported 12 image mismatches on the two quiz drafts because Webflow kept the same fileIds. The CDN bytes of all 12 images match the repo files (md5). So the images were unchanged, and the hero prompt went through. I re-based `cms_draft.sha` to the then HEAD; ship-update found 0 changes and `--verify` passed 2/2.

## Files changed and commits
- B-ship-8 commits:
  - r12 fixes: e17fade9, f3d0451a, 2969129e, 969ae575
  - Form g1: 5bec760a, 898c27fe, ebb7421f, 78ad672f, 52634647, 8fc34b96, 1ac4ebae
  - Quiz canary: a6d44820, 456bbeee, bac7b4fa, 0e82bddd
  - Form g2: bf996f2f, 082f37ff, 9924410a, dcb856cd, da4942fc
  - massage-booking re-hold: 91e12412
  - Audits: 9dce7614, 7c1cb544
- Batch files: plan/batches/fix-2026-11-06-r12-{lp,form,aab}.txt and plan/batches/quiz-canary-2026-11-06.txt.
- Group log: reports/2026-11-06/ship-groups.log.

## Webflow calls (Data API through hubctl; logged in logs/<dir>.md and logs/api/2026-11-06.jsonl)
- **Updates (changed fields only, status kept):**
  - LP 2, Form 3, Auto 1 (patient-intake draft 6aec581430e7165c1ab2d82d), SurveyQuiz 2 (drafts 6ad1d94e15d6a1e8ebe0b148 and …146).
  - Before-values: childedits/2026-11-06/*.fix-2026-11-06-r12-*.before.json and *.quiz-canary-2026-11-06.before.json.
  - Rollback: childedits/2026-11-06/fix-2026-11-06-r12-*.rollback.json and quiz-canary-2026-11-06-update-*.rollback.json.
- **Creates (isDraft true):**
  - Form 7: 6aed88599b4f2e9cac9aad4f to …ad5b.
  - Form 6: 6aed8b85218b52d7afea01a2 to …01ac.
  - Rollback: delete the IDs in childedits/2026-11-06/form.api-create.{520956c,bf996f2}.*.rollback.json.
- **Item publishes:** 7 calls, 21 items, 0 errors, plus the 1 relink publish.
  - Before-values: childedits/2026-11-06/*.api-publish.*.before.json.
  - Rollback: unpublish those IDs in the CMS on Divit's go (unpublish is not on the API allowlist).
- **Relink:** liability-waiver (6accba1c29454f1af2f01f0f), FAQ field. Rollback: childedits/2026-11-06/relink-auto-20261106T081539Z.20261106T081541Z.rollback.json.

## Not done
- cleaning-quote and massage-booking: waiting for Divit's R3 re-approval. After it lands: changed-fields update (before-only, sync, live), then item publish, verify-live and post-ship audit.
- vocabulary: not published, because the canary failed and B-c-1 holds it.
- home-insurance-quote and health-coaching-intake: held for Divit's Q1 decision.

## Audit
- **GitHub Actions full run, 12:42 UTC (the valid run):** 451 pages, 305 fail, 2 real.
  - P0 A1-http on security-deposit (500). Transient: it returned 200 on 3 re-fetches.
  - cleaning-quote A3/A4. Expected: the spec is ahead of the live page until R3.
  - The rest are the hero backlog (on hold) and known redirect issues.
- **This Mac's 12:53 UTC full run is invalid** (LESSONS 2026-10-13): all 953 "real" fails are transport errors (A1-transport, A11-transport) from a network loss during the run.
  - Its uncommitted last_success.json (780 real) is still in the working tree. I did not commit it.
  - The next run will replace it.

## Open questions for Divit
- Style is live with CLS 0.061 at 390 px. Do you want it unpublished until the hero font fix lands, or kept live? Recommended default: keep it live. The shift is a one-time hero rewrap that B-quiz-3 measured on 18 of 64 live SurveyQuiz heroes, not something the quiz causes.
- Re-approve cleaning-quote and massage-booking with your command, so they can ship.

AUDIT: last full run 2026-11-06 12:42 UTC, 451 pages, 305 fail (2 real; the 12:53 Mac run is invalid, transport only)
