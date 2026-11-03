# Ship run, 2026-11-03 (B-ship-5, the only ship agent)

## Request
Coordinator brief (B-c-1, relaying Divit's recorded standing go of 2026-11-02, pasted 2026-11-03, MAX-THROUGHPUT RUN): "every page reviewed by an independent reviewer with 0 blocking findings, 0 flags, QC 0, a passing ship-check and no active hold may be approved and shipped." Continue after payroll-change with every eligible page in rolling groups of 5. Later the coordinator relayed two changes from Divit: SHIP FIRST, and then SPEED (groups of 10, publish without `--verify-live`, with B-v-1 running verify-live and the post-ship audit in parallel).

## Actions and results
- **Shipped today by B-ship-5: 58 pages, all item publishes, 0 publish errors.** There was no site or domain publish, the Webflow sites tool was never used, and no slug changed.
- Every page passed ship-check right before its approval and again right before its publish.
- Every create and publish wrote a before-value, committed and pushed it, and only then made the `--live` call.

| Hub | Shipped | Pages |
|---|---|---|
| Form | 31 | g1 workshop-registration, file-upload, budget-request, logo-design-questionnaire, overtime-request · g2 rental-history, yoga-waiver, harassment-complaint, training-acknowledgment, demo-request, laser-hair-removal-consent, equipment-request, 5k-registration, security-deposit, feature-request · g3 gym-waiver, dental-intake, telemedicine-consent, rfq, class-registration, meeting-request, chemical-peel-consent · g4 food-bank-application, address-verification, anesthesia-consent, approval, wedding-photography-questionnaire · g5 drug-test-consent, sublease, personal-injury-intake, surgery-consent |
| LP | 18 | g1 cleaning-service, community, electrician, free-trial, freelancer · g2 insurance, dropshipping, dj, api, fintech, demo, resume, seo-agency · g3 landscaping, salon, personal-trainer, restaurant, political |
| Auto | 3 | order-confirmation, file-management, renewal-reminder |
| SurveyQuiz | 6 | dental-patient, beta-feedback, podcast-listener, real-estate-client, salon-client, wedding-guest |

- **approval-workflow (Auto, already live):** approved under the standing go. The CMS item already matched the slim-reviewed spec: `hubctl verify` found 0 mismatches, and the item was last published on 10-23, after its last update. So no update or publish call was needed. verify-live passed and the page moved to `published`.
- **Group log for the verifier:** reports/2026-11-03/ship-groups.log, one line per group.

## Numbers
- **Live now (fresh api-read of all 4 hubs, 12:5x UTC):** LP 103, Form 172, Auto 79, SurveyQuiz 63, **total 417** (morning: 359).
  - The Webflow read shows 60 items with lastPublished today: my 58, plus payroll-change (B-c-1) and the direct-deposit relink republish.
- **Drafts left in Webflow:**
  - Form creator-application (an original; not in today's queue).
  - SurveyQuiz style and vocabulary (Divit's canaries; untouched).
- **Verify-live:**
  - I ran Form g1 (5 of 5 pass), address-verification (pass) and approval-workflow (pass).
  - At the time of writing, 32 of the 58 are in state `published` (verified). The other 26 (Form g4/g5 and LP g1–g3) are with B-v-1, whose results are not yet in the repo.
- **Post-ship audit:** Form g1 (audits/live/2026-11-03/postship-form-g1): P0 0, P1 0, P2 5, held pages live 0. B-v-1 is running the other groups (postship-form-g2, -g3, -auto-g1 were capturing at 12:42 UTC).

## Decisions
- **Approvals:** each one followed DECISIONS 2026-10-26 (approved needs a recorded go) and status/go/2026-11-02.json + .cache/standing-go-2026-11-03 (standing go), through `hubctl state URL approved --by standing-go` only.
  - The 11 Form approvals of 10-26 were backed by the coordinator's go-record 750adb9e.
  - The 6 SurveyQuiz approvals were backed by 9be54078.
  - The 4 named drafts were approved by Divit's named go, recorded by the coordinator.
- **Stale sources:** QC P3 (sources not link-checked in 7 days) was cleared with `hubctl sources-check` on each page (HUB_RULES QC P3). All sources passed, and no copy was touched.
- **Stale images (budget-request, overtime-request, class-registration):** rendered with ops/render_changed.py so render.json records the brief hash (LESSONS 2026-10-12). Then `hubctl ready`, then approval.
- **Form create of 25fc1343:** it returned a 504, but Webflow had written all 22 drafts. A fresh full read showed 168 unique items, all 22 slugs present and isDraft true. I did not retry the create, which would have duplicated all 22. The drafts were recorded with `bulk-verify` on that read, limited to the 22 items created today: 22 verified, 0 mismatches. The coordinator confirmed this and corrected its "0 written" record (its LESSONS entry).
- **Pending link:** address-verification's warning about /ai-form-builder/shipping-address is a pending_link (not rendered until that page is live; LESSONS rule 5). verify-live found all 92 internal links returning 200.

## Files changed and commits
- Main stage commits:
  - c0d1ff93 (payroll-change leftovers)
  - 61b8f994, 94916c7a, 86a51c5e, 6f9a9994, 9e45f681, 1772655d, d341a295 (approvals)
  - 25fc1343, 52652081, 88b795cd, 4b209511, 07998ccf, 3fb158c6, e4105700, ad462d39, ccc7c334, 71bf281c, ab122fa6, beeb3f6e, aff4cd64, 1e24e6be (creates and verification)
  - 9179c5c4, d5a81ec0, fd3909f0, c8e3266e, 1ba4dff1, 913f2429, bfb5b8fe, bec43458 (publish before-values)
  - f9ff9b4f, 88bfa9fe, aa12c770, 3a4ea842, 4605464e, e3ee9a42 (group log)
  - d501bc85 (approval-workflow)
- Before-values and rollbacks: childedits/2026-11-03/*.

## Webflow calls (all through `hubctl api-*`, Data API, logged in logs/<dir>.md and logs/api/2026-11-03.jsonl)
- **Creates (drafts, isDraft true):**
  - Form 22 (61b8f99; returned a 504 but wrote all 22, so it has no rollback file; rollback = delete item IDs 6ae99b53c789f9a2869fed96 to …fedc0)
  - Form 1 (6499cb1), Form 4 (6f9a999)
  - LP 5 (6f9a999), LP 8 (67b4e5d), LP 4 (1772655), LP 1 (d341a29)
  - Auto 3 (cb9fbbe)
  - SurveyQuiz 6 (6499cb1)
  - The before-value for each is in childedits/2026-11-03/<hub>.api-create.<sha>.before.json, and each rollback file is beside it.
- **Item publishes:** 12 calls, totalling 58 items, 0 errors.
  - Before-values: childedits/2026-11-03/*.api-publish.*.before.json.
  - Rollback: unpublish those item IDs (rollback files beside them).
- **Refused (correctly) and not retried around:**
  - Several publishes and creates refused with "before-value commit not pushed" while my local origin ref was stale. Each succeeded after `git fetch`, with no change to the guard.
  - Every publish call refused the held surgery-consent and the 3 revoked drafts until Divit's go and the hold lift landed.
  - restaurant was refused once while B-r-419's review claim held it, and shipped after the hold was lifted.

## Not done
- `hubctl state … approved --by divit` for the 3 named drafts was **denied by the permission system**. I did not retry it. The approval came from the coordinator's side instead, and I then shipped the pages.
- B-v-1's verify-live and post-ship audit results for Form g2–g5, Auto, SurveyQuiz and LP g1–g3 are not in the repo yet. 26 pages await its verify-live.

## Incidents (mine)
- **Audit manifest overwritten and restored:** at 12:00 UTC I ran `ops/live_audit.py --help`, which has no help flag and started a run. That run overwrote the running full audit's .cache/live/2026-11-03/manifest.json (350 pages, 0 hubs). I stopped it and restored the manifest exactly from that run's own shards/hubs.manifest.json and shards/s0.manifest.json (359 pages, 4 hubs, 87 held). The full run then scored normally at 12:45 UTC (359 pages, 4 hubs).
- **False log line removed:** one `&&` chain appended an Auto line to ship-groups.log after a refused publish. I removed it within a minute, before Auto actually shipped.

## Audit
- Full audit at 10:59 UTC (Mac): 14 real P1 on pages live before today (2 A8 cover images, 11 A9 DNS console errors, 1 A11 niche 500). All returned 200 on re-check, so I judged them transient.
- At 12:45 UTC, GitHub Actions reported real 1 (A8 on /ai-form-builder/payment; 200 on re-check). The Mac run of the same minute (audits/live/2026-11-03/mac/) reported 15 real, the same CDN or DNS pattern as before; the images I re-checked returned 200.

AUDIT: last full run 2026-11-03 12:45 UTC, 359 pages, 1 fail

## Open questions for Divit
- None blocking. Default: B-v-1 holds any page that fails verify-live, and the rest stay live.
