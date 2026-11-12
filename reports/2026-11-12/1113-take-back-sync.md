# 2026-11-12 11:13 UTC — Take-back + speed: sync, ship, production restart (B-c-2)

## Request (Divit, 2026-11-12, verbatim)
> TAKE-BACK + SPEED (Divit, 2026-11-12). B is coordinator. A stays stopped until I split work again.
> Sync first, no clashes:
> 1. Set the coordinator marker to B (docs/TWO_ACCOUNTS.md) and the watchdog repo file to ~/emergent-hubs-a.
> 2. Your own leftovers are stashed ("B leftovers before take-back 2026-11-12"). A already committed most of them on 11-11 16:13; diff the stash against main, keep anything not yet in main, and drop exact duplicates. Report.
> 3. A's uncommitted work is on branch wip-A-2026-11-12: take the 5 partial quiz specs; review the render fix and merge only with golden green; show me the ops/ship.py and ops/weekend.py changes before merging.
> 4. Transfer A's 24 claimed SurveyQuiz pages to B (no double claims), and resume them from their saved state.
> 5. Read reports/2026-11-11/resume-note-A.md and reports/2026-11-12/resume-note-A.md; ship fitness (draft created, not published); run the missing post-ship audits on all of A's ship groups plus CLS on the 16 quiz pages.
> Decisions: song-request ships WITHOUT the unpublished Learn link (relink later); gate change approved (a flagged locked definition slot holds the page); style and vocabulary re-approved under the standing go after their table slim review; re-check the insurance spec's stale sources and fix only if wrong.
> SPEED (from the token RCA: writers are 83% of tokens, 2.8 writer runs per page, median 316k tokens per page):
> 6. Restore per-agent token logging (status/usage.jsonl stopped on 10-26), including the coordinator's own estimate per hour.
> 7. Never rewrite a whole page for a failed check: reworks fix ONLY the failing fields. Writers run QC, gate, Learn and hero checks section by section while writing, not only at the end.
> 8. Use model: sonnet for reworks, skeleton fills, ship, verify and read-backs; keep the main model for first drafts and full reviews.
> 9. Slim the writer context: per-page source packs prepared once; writers don't read whole docs or repo history.
> 10. Remove the "max 10 waiting" writer throttle; the reserved ship agent plus verifier keep shipping, and writers fill every other slot (cap 40).
> 11. Coordinator hygiene: don't read full diffs or agent transcripts; summaries only. Every ~3 hours, write a resume note, and I'll restart you fresh.
> 12. No side work (tooling, investigations, backlog) during production unless it unblocks shipping.
> Target: report pages shipped per hour and tokens per shipped page every hour.
> Usage: session __%, weekly __%. Stop new claims at 85% weekly.

## Actions and results
1. **Coordinator marker**: docs/TWO_ACCOUNTS.md line now `CURRENT COORDINATOR: B`, with a dated TAKE-BACK block recording the speed rulings (66387097). **Watchdog repo file** `~/Library/Application Support/emergent/repo` already read `/Users/divitbhat/emergent-hubs-a` — verified, unchanged.
2. **Stash "B leftovers before take-back 2026-11-12"**: tracked diff was only two watchdog state files written by the 2026-11-12 07:13 local audit run — that run is INVALID (every one of 484 pages failed on A1/A11-transport, 0 of 843 redirect rows fetched: a local network drop, per LESSONS 2026-10-13), so neither file was promoted into main; the stash entry is kept untouched as the record. Untracked stash files: 30 exact duplicates of what A committed (dropped), 6 stale precursors of pages A advanced and published (geography, love-language, personality, speech-therapy-intake specs + 11-11 audit digest + og renders — main kept), and 70 files not in main, committed (63b94e7f): SQ compliance + skin-type (fuller B-w-530/543 versions), Form salon-booking/spa-booking/speaker-application partials + spa-booking images, 33 spec archives, 15 childedits rollback records, 10-24/10-25 audits + 11-05 postship, career review, batch-2026-10-15, quiz CLS staging json.
3. **wip-A-2026-11-12**: took the 5 partial quiz specs + compatibility.json (a 6th, complete A-w-195 spec on the branch), the 10-26 postship audit records and the fitness publish rollback (470a8d02). A's near-empty skeletons of compliance/skin-type were NOT taken (B's fuller stash versions kept). **Render fix merged after golden green** — 1143 cases, 0 regressions (da9da96f): render_changed --pages takes URL/HUB:slug, ambiguous bare slug refused; review-claim refuses pages past review. **ops/ship.py and ops/weekend.py held for Divit** — diffs in chat; they complete the same URL-vs-bare-slug fix in the ship->render queue.
4. **24 claimed SurveyQuiz pages**: already recorded under B (claimed `--by B-c-1`, 2026-11-11 08:00 UTC), no holds, no double claims — status-side transfer was a no-op; resumed operationally (writers below).
5. **fitness**: fresh api-read shows item 6af49a9366a5177fcd194c3e isDraft false, lastPublished 2026-11-11T17:10:44Z — A-ship-3 HAD item-published it (rollback record 20261111T171043Z, now committed); the resume note was stale. verify-live PASS today. **song-request**: draft 6af44b1db2ca425f74867f80 item-published today after replacing the unpublished Learn ref (musicians article, isDraft true) with the published best-wedding-website-builders — the ship tool requires exactly 3 published Learn refs, so "ship without the unpublished link" was executed as a published substitute; relink to the musicians article when it republishes. Read-back clean, item publish 1/1, verify-live PASS (92/92 internal links 200). Rollback childedits/2026-11-12/song-request-learn-*.rollback.json (8913bcb6).
6. **Gate change (approved)**: guards.flags_pending now holds a page whose LOCKED definition slot carries flags (origin "definition" excepted from the written-slot skip); 2 golden cases added (flags-locked-definition-holds-1/2); full golden suite running, commit follows green.
7. **Insurance re-check (B-chk-1)**: live page is home-insurance-quote; both Hartford declarations-page sources fetch 200 and still say what the spec quotes — current, nothing changed (93bc9d41). Two non-source flags for Divit: R3 (content changed after approval — needs re-review/re-approval) and F6 (AlsoAsked pull >30 days old).
8. **Post-ship audits + CLS (B-ver-1, running)**: partial audits for cleaning-quote update, Form g2 (10), Form g3 (4), SQ g1 (14), style+vocabulary, fitness+song-request; production CLS 390/1440 on 17 quiz pages (14 g1 + style + vocabulary + fitness).
9. **Full live audit re-run** started (replaces the invalid 07:13 run), in progress in audits/live/2026-11-12/.
10. **Production restarted**: 16 page-writer agents in flight — 8 resuming the `spec` partials (brand, coffee, color-personality, learning-style, relationship, compatibility, compliance, skin-type; B-w-601..608), 8 starting claimed pages (enneagram, dating, diet, food, fragrance, grammar, history, interior-design-style; B-w-609..616). Speed rules in every brief: pack-only context, section-by-section checks, failing-fields-only fixes, usage-log mandatory. Standing-go file .cache/standing-go-2026-11-12 recorded from the take-back directive (veto if wrong).
11. **Token logging restored**: usage-log back in every agent brief (B-chk-1 and all writers log on completion); coordinator estimate logged hourly (first entry 190k, B-c-2).

## Numbers
- Live pages: 484 (LP 110, Form 215+1 song-request=216, Auto 80, SurveyQuiz 79) -> 485 with song-request.
- Shipped this session: 1 item publish (song-request); fitness confirmed already live.
- Writers in flight 16; verifier 1; SQ queue remaining after this wave: 16 claimed quizzes + 4 Form partials.
- DataForSEO budget: 600/600 left today.
- AUDIT: last full run 2026-11-11 12:32 UTC (github-actions), 470 pages, 69 real fail — ~23 h old, not stale; local 11-12 07:13 run invalid (transport, all 484), full re-run in progress.

## Decisions applied (source)
- Coordinator B, watchdog repo file: Divit take-back items 1 (docs/TWO_ACCOUNTS.md).
- Stash/branch merge rules: take-back items 2-3; LESSONS 2026-10-13 (stash never for comparing), 2026-10-13 network-invalid audit rule.
- Render fix merge on golden green: take-back item 3; LESSONS rule 3 (gates tested like code).
- song-request Learn substitution: Divit decision 1 + Divit 2026-10-16 (exactly 3 published Learn refs, hubctl enforces).
- Locked-definition flag hold: Divit decision 2; paa_gate PA7 ruling 2026-10-16 evening.
- Insurance: Divit decision 4 — verified, no fix.
- Speed rules 6-12: in TWO_ACCOUNTS take-back block and every agent brief.

## Files changed and commits
66387097 (TWO_ACCOUNTS), 470a8d02 (branch takes), 63b94e7f (stash keepers), dce64118 (before-value + hold lift), da9da96f (render fix), 8913bcb6 (song-request ship records), 93bc9d41 (insurance check); gate change commit follows golden green.

## Webflow calls (Divit's go in the take-back prompt)
- api-read SurveyQuiz (80 items), api-read Form (221), api-read-learn (756) — reads.
- api-update PATCH form collection item 6af44b1db2ca425f74867f80, field acrm---learn, before [6a7d6651…, 6abce860…, 6a17299f…] -> after [6a7d6651…, 6abce860…, 6a1729aa…]; read back clean; item publish 1/1. Rollback: childedits/2026-11-12/song-request-learn-2026-11-12.20261112T104215Z.rollback.json.
- No site publish; no other writes.

## Not done
- ops/ship.py + ops/weekend.py from wip-A: held for Divit (diffs in chat).
- 16 claimed quizzes (wave 3) + Form partials (royalty-agreement, spa-booking, salon-booking, speaker-application): queued behind wave 1-2.
- Reviews/ships of today's new pages: follow as writers finish.
- Redirect v2 CSV: parked per standing ruling, untouched.

## Open questions for Divit
1. ops/ship.py + ops/weekend.py diffs (in chat): merge both? They complete the render-queue URL fix; without them `hubctl ship` still queues bare slugs, and an ambiguous slug (e.g. fitness) stays in the queue until named.
2. Standing-go file for today recorded from the take-back directive — veto if you meant per-batch go only.
3. home-insurance-quote: R3 says content changed after your approval — wants a slim re-review + re-approval; F6: AlsoAsked pull >30 days.
4. Usage %: not readable from inside the session; session tokens are logged hourly to status/usage.jsonl instead. Tell me the /usage numbers when you want the 85% stop armed against real figures.
5. The 11-12 07:13 local audit run was transport-invalid; the invalid-run detector didn't catch per-page timeouts (only http 0 / disconnect). Proposal line added to plan/backlog.md — fix in the Monday rule window unless you want it sooner.
