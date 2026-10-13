# Account A: Form and Automation rework day (2026-10-13)

## Request

> You are the writer for Form and Automation on account A, working in ~/emergent-hubs-a alongside the coordinator (account B, in ~/emergent-hubs). Read docs/TWO_ACCOUNTS.md first, then RUNBOOK.md, DECISIONS.md, LESSONS.md and the latest entries in reports/INDEX.md. You never touch Webflow and never edit rules/, qc/, ops/, templates or DECISIONS.md; put any proposals in the file TWO_ACCOUNTS.md names. Work order for your hubs: rework pages first, then queued, then parked pages the coordinator has marked for rescue. Every page reaches QC 0 and PAA gate 10/10, and every commit goes through ops/sync.sh. Be token-light: summaries only. Report your plan and how many pages you'll finish today, then start.

Two follow-ups in the same session also apply:
- Divit's advisor addendum (8 items): fold it into TWO_ACCOUNTS and this report.
- Divit's rulings of 2026-10-13 (7 items): gate pass means 0 rejects, verbatim AlsoAsked questions are never reworded, and the other items listed under Decisions.

## Actions and results

The day's work, in order:
1. **Setup.** `docs/TWO_ACCOUNTS.md` was missing at the start; it arrived mid-session as fa071de8. The A clone was then brought into line with TWO_ACCOUNTS s2:
   - `.hub` set to `Form,Auto`;
   - the Webflow MCP disabled, and both Webflow tool names denied in `.claude/settings.local.json` (git-ignored);
   - `private/` was already a symlink to B's.
2. **Pilot of 4 (batch 3).** consent-form, photo-release-form, ach-form and social-media-automation were reworked to `reviewed` and committed in 075d9a83. One rule came out of it: writers run `ops/render_changed.py` last, because 2 pilot pages had changed their brief after rendering.
3. **Wave 2 (8 batch-3 pages).** The work was done in A's clone, but B committed its own rework of the same pages (fabcde3a, "B batch files win"). A took B's versions. A's copies sit in a session scratch backup, and about 518k writer tokens were spent on them.
4. **Wave 3 (10 pages).** 9 were A6 rescues with no review record and 1 was a ratchet rework. Results:
   - accident-report-form went to `reviewed`;
   - 6 went to `images` for B's review;
   - brand-questionnaire, employee-referral-form and shipping-address-form were parked for a PA12 ruling. Their writers had added keyword ideas to `secondaries_used` to pass the gate.
5. **Waves 4, 5 and 6 (36 pages, including report-automation).** 30 went to `reviewed` and 5 to `images`. The other wave-4 page, expense-report-form, is also `reviewed` and counted there. From the middle of wave 5, writers worked under the new ruling: verbatim AlsoAsked questions are kept and the flags are listed.
6. **Ruling 2 retro-fix.** A script compared every FAQ item against `faq_sources[].prov.original` and found AlsoAsked questions reworded today on 6 non-batch pages. Those items were restored to their verbatim wording, except 3 items where the verbatim question is a PA3 reject:
   - church-membership-form items 6 and 10;
   - employee-referral-form item 5.
7. **Proposals.** 8 lines were added to `proposals/account-a.md` (0d18b2c1 and the earlier proposals commit).

## Numbers

| | Count |
|---|---|
| Form/Auto pages A worked today | 58 (4 pilot, 8 wave 2, 10, 12, 12, 12) |
| A pages now `reviewed` (ready for Divit) | 36 (35 Form, 1 Auto) |
| A pages now `images` (waiting for B's one review) | 11 (10 Form, plus report-automation) |
| Parked for a PA12 ruling | 3 |
| Taken over by B (batch 3, fabcde3a) | 8 |
| QC TOTAL on every A page committed | 0 |
| PAA rejects on every A page committed | 0 |
| A writer runs logged | 58 |
| Median tokens, ratchet rework | 57.7k (n=61, including B's batch-3 rows) |
| Median tokens, A6 rescue rework | 105.8k (n=9) |
| Median tokens, verbatim restore pass | 44.9k (n=6) |
| Writer and restore tokens on Form/Auto today | 4.67M |
| All-history median, writer | 72.8k |
| All-history median, reviewer | 43.0k |
| AlsoAsked credits spent by A | 0 |
| Form state now | reviewed 35, images 10, rework 7 (B's batch-3 copies), queued 85, parked 109, published 16 |
| Auto state now | reviewed 1, images 1, rework 1 (B's), claimed 3 (stale weekend), queued 57, parked 16, published 9 |

## Decisions

- **Work order.** Rework first, starting with batch 3 (`plan/batches/batch-3.txt`, Divit 2026-10-13). Source: the request and TWO_ACCOUNTS s1.
- **Overlap with B.** B's batch-3 versions were taken instead of contesting them. This keeps one rework per page (CLAUDE.md step 5; RUNBOOK 4b).
- **A6 rescue pages stop at `images`, not `reviewed`.** They have no review record, so `hubctl ready` refuses them (TWO_ACCOUNTS s6).
- **Pages padded for PA12 were parked.** The padding is DataForSEO keyword ideas in `secondaries_used`, which is meant for Semrush secondaries (writer agent rule 1). They were parked with a proposal note, per TWO_ACCOUNTS s5. The ruling to accept keyword ideas (rule 5) came later; once B ships it, A releases them through B.
- **Gate pass means 0 rejects, flags allowed, verbatim AlsoAsked never reworded.** This follows Divit's ruling 2 of 2026-10-13, applied to running writers by message and retroactively to 6 pages.
- **One commit per page** (TWO_ACCOUNTS s4) from wave 2 onward. The 4-page pilot went in as one commit, before the doc existed.
- **`audit/paa/summary.md` is no longer committed** after the pilot (TWO_ACCOUNTS s1 path list; addendum item 2).
- **Webflow:** none.

## Files changed and commits

- `specs/form/*`, `specs/aab/*`, `images/form/*`, `images/aab/*`, `status/form.json`, `status/aab.json`, `status/usage.jsonl` and `proposals/account-a.md`.
- Commits:
  - pilot: 075d9a83;
  - wave 3: e445778f through 2bffba6f;
  - proposals: 0d18b2c1;
  - wave 4: through 13f7d8e8;
  - wave 5: through 32f17027;
  - wave 6 and the verbatim restores: through e0cb3a78.

## Webflow calls

None. A has no Webflow access.

## Addendum (Divit, advisor review): A's answers and where each item lives

1. **Cross-clone safety.** A claims only via commit and push (TWO_ACCOUNTS s3). Rework pages have no claim, and the batch-3 overlap shows that gap. Proposal: a hold marker on origin (accepted in ruling 5). A spent 0 AlsoAsked credits, and its `private/` is B's store through the symlink.
2. **Path ownership.** A committed only its own paths after the pilot. The pilot commit included `audit/paa/summary.md` once. `hubctl qc` and `paa` still rewrite `qc_passed.date` and the PAA summary on read-only runs (proposal accepted in ruling 5).
3. **rules_version.** Every A page committed today carries the `qc_passed.rules_version` current at commit (`bae2ab9babe0` at the pilot). A pulled through `ops/sync.sh` before each page commit. It did not pull mid-wave, because autostash with live writers is unsafe (see Not done).
4. **Capacity truth.**
   - Measured per page:
     - writer: 57.7k for a ratchet rework, 105.8k for an A6 rescue, about 113k for a new page (LESSONS);
     - reviewer: 43k (all-history median).
   - A spent about 4.7M tokens today without hitting a limit.
   - Per-account weekly capacity is not in the logs: no limit hit or plan cap is recorded, so it is UNVERIFIED.
   - A's realistic daily rate at today's spend: about 40 new pages a day (113k each), or about 75 ratchet reworks. A plus B at about 33 new pages a day is feasible if B's review keeps pace (43k per page).
   - Proposed per-page token cuts:
     - a pre-computed fix list per page from `hubctl qc --json`, so writers skip re-reading HUB_RULES and CONTENT_DEFECTS for 1-class fixes: about -15k per ratchet rework;
     - a batched writer, 3 to 4 one-class reworks per agent, sharing the rules read: about -20k per page;
     - generating `chip_adds` with a code template plus a human-voice pass, since they were the only fix on half of today's pages: about -10k per page.
   - Estimated effect: ratchet reworks about 25-30k, new pages about 90k.
5. **Supply (A side, Form parked 109).** Rescue levers ranked by pages per token and per credit:
   1. PA12 ruling applied: 2 pages (brand-questionnaire, shipping-address-form), about 0 tokens, 0 credits.
   2. A6 with 6 or more on-topic sources: 13 pages, about 106k each, 0 credits.
   3. A6 with 5 sources: 16 pages, about 110k each, 0 to 1 credit.
   4. A6 with 4 or 3 sources: 35 pages, 1 credit plus about 110k each.
   5. Library gap: 20 pages, which need B's library research first.
   6. A6 with 2 or fewer sources: 40 pages, low yield.

   Levers 1 to 3 give about 31 Form pages. With Automation's 16 parked (not yet ranked), A's side reaches about 45. The rest of the about 70 has to come from B's hubs.
6. **Approval packet: flagged items for Divit, by page and item number** (question text stays in `private/`):
   - FAQ flags kept verbatim:
     - tenant-screening-form: 4 flags;
     - contact-form: items 5 and 8;
     - address-verification-form: item 10;
     - church-membership-form: item 8;
     - multi-step-form: item 3;
     - new-employee-form: items 5, 9 and 10;
     - home-care-intake-form: items 4, 5, 7 and 10;
     - permanent-makeup-consent-form: items 4 and 6 to 10;
     - model-release-form: items 5 and 6;
     - nda-form: items 1, 9 and 10;
     - proposal-form: items 4 to 7;
     - independent-contractor-agreement: items 3, 6 and 8 to 10;
     - referral-form: items 6 and 7;
     - volunteer-form: items 4 and 7;
     - restaurant-reservation-form: items 8 and 9;
     - quote-form: items 4, 5 and 8 to 10;
     - requisition-form: items 3, 6, 8 and 9.
   - Kept reworded because the verbatim question is a PA3 reject: church-membership-form items 6 and 10, employee-referral-form item 5.
   - Other things to look at:
     - address-verification-form item 10 names a federal agency;
     - field-trip-permission-slip has a review note that one image count disagrees (5 versus 4);
     - checkout-form: 4 FAQ items come from keyword ideas, and part of the page reads as equipment checkout.
7. **readiness.md T3.** B's item.
8. **Learn/carousel production go.** B's item; A has no Webflow access.

## Not done

- **The 3 stale Automation claims** (automated-loan-processing-system, sales-workflow, shipping-automation) have not been released on origin yet (ruling 4, B's action). A will claim them after the release.
- **No new Form claims.** All reworks came first.
- **Batch-3 pages.** A did not touch the 8 batch-3 pages B holds after fabcde3a. 6 of them showed gate flags, which ruling 1's slim review covers.
- **`docs/TWO_ACCOUNTS.md`.** A did not edit it; it is B's file. The addendum and rulings are for B to fold in.
- **A leftover autostash in A's clone.** The permission check blocked `git stash drop`, so a resolved autostash from a `status/usage.jsonl` union merge is still in the stash list. Remove it with `git -C ~/emergent-hubs-a stash drop`.
- **Pulls.** A did not pull while writers were running: `ops/sync.sh` autostashes the whole tree, which races live writers. Every commit went in between waves.

## Open questions for Divit

1. **Rework hold.** Accepted in ruling 5. Until hubctl supports it, should A commit a `rework` state with `--by A-...` as the hold? Default: yes, starting tomorrow.
2. **The 3 PA12-parked pages.** brand-questionnaire and shipping-address-form have 0 Semrush secondaries and qualify under ruling 5 once B ships it. Their writers used DataForSEO keyword ideas, and ruling 5 says workbook ideas. Default: A swaps in workbook ideas (at least 4, on-topic) when it releases them. employee-referral-form has 2 Semrush secondaries plus padding. Default: drop the padding and keep the page parked until PA12 counts it fairly.
3. **Rewording rejected AlsoAsked questions.** The 3 PA3-rejected AlsoAsked questions were reworded rather than replaced. Default: replace them with sourced secondaries in A's next pass.
