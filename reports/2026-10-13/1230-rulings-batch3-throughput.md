# Rulings 0 to 10 applied; batch 3 staged (20 of 20); AlsoAsked blocker fixed; throughput plan (superseded by 1400)

## Digest for Divit
- **Ruling 0 was pushed first (941ce5b2).**
  - Account A = this coordinator (`~/emergent-hubs`); Account B = the writer (`~/emergent-hubs-a`).
  - hubctl checks agent ids against the clone (`.hub` = `A:LP` / `B:Form,Auto,SurveyQuiz` after ruling 9); holds record the clone's account.
  - TWO_ACCOUNTS and DECISIONS were rewritten, with a dated mapping note for the old ids.
- **Review rule (1):**
  - each review stores a text hash;
  - `hubctl review-diff` lists the fields changed since review;
  - `hubctl slim-review` records a slim review;
  - payload builds and pre-flight refuse any page whose text is not the reviewed text.
- **Reviews (2):**
  - 52 slim reviews: 47 pass, 5 rework (ach-form, photo-release-form, model-release-form, hotel-booking-form, address-verification-form, driver-application-form; ach-form and photo-release-form were both reworded verbatim AlsoAsked questions).
  - 10 full reviews: 7 pass, 3 rework (conference-registration-form, consultation-form, tenant-screening-form). church-membership-form was not recorded because B holds it.
- **Batch 3 (3):** 20 of 20 CMS items were created with the Learn refs and verified 20 of 20. All 20 are set to isDraft false: staged, not published.
  - Pre-flight: 20 of 20 pass, the L12 and reviewed-text columns included.
  - lead-generation-landing-page had the grouped "Landingi / Leadpages / Instapage" column (the 2026-10-12 P0 pattern). It now uses Unbounce, Leadpages and MailerLite, and its FAQ cost line was fixed after a slim review blocked it. It then passed a second slim review.
  - ach-form and photo-release-form came back from B with the verbatim AlsoAsked questions restored (each equals prov.original), passed slim review (A-s-12) and were created last (32dd3688).
- **Gate and PA6 (4):** owner-intent patterns were added ("do I need a…", "who fills out…", "is a … legally binding"), so 161 verbatim pull questions are no longer flagged. 4 golden cases.
- **PA12 (5):** a page with no Semrush secondaries now needs 4 on-topic workbook keyword ideas. The workbook has **none** for brand-questionnaire or shipping-address-form (or for 7 other parked pages), so they fail PA12 and stay parked. See open question 1.
- **Collisions, Learn refs and re-run (6, 7, 8):**
  - `hubctl batch-check` and the ship payload step take only `reviewed` pages and never a held page.
  - Learn refs are unchanged; the tie-break is by date, then createdOn.
  - recheck skips B's held, claimed and rework pages.
- **AlsoAsked blocker:** B's 3 calls got HTTP 403 (no key in B's session) and were **not charged** (balance 743 unchanged).
  - They are reconciled in credits.log and were re-pulled once by A, 3 credits in total.
  - `aa` now checks the key before any POST, saves before logging, refuses a charge in the last 24 h with no saved pull, and refuses a clone not on the shared store. 5 golden cases.
  - The pulls are thin: 0, 0 and 1 usable questions.
- **Golden suite:** 331 cases, 0 regressions.

## Throughput plan (ruling 9; summaries only)
- **Where we are:** 40 live and 20 staged, so **60** after this publish. **440 more** are needed for 500.
- **Supply (planned 581):**
  - reviewed and not yet in the CMS: 35 (batch 4 is ready now);
  - rework 22; images 4;
  - queued, not yet written: 313 (LP 85, SurveyQuiz 86, Form 85, Automation 57);
  - parked 141.
  - So at most about 440 non-parked pages can ship, which means **at least 60 rescues or replacements** to reach 500.
- **Cost per page** (status/usage.jsonl):

  | Stage | Tokens per page |
  |---|---|
  | B: rule-change rework | 58k |
  | B: rescue | 106k |
  | New page | about 113k |
  | A: full review | 47k (10 today; 43k all-time median) |
  | A: slim review | 19k (52 today) |
  | A: ship (payload, create, verify, transcribed through the MCP) | about 15–20k |

- **Capacity per account per day** (B measured about 4.7M tokens today with no limit hit; A's limit is unverified):
  - B writes about 40 new pages, or about 75 reworks.
  - A can review about 40 (1.9M), write about 10 LP/SurveyQuiz pages (1.1M) and ship about 40 (0.8M).
  - **Realistic ship rate: 35–40 a day**, capped by one staging-then-production publish cycle per day and A's review.
- **500 date:** 442 at 35 a day is about 13 working days, so **2026-10-26** if supply holds and the 60 rescues land by about 10-22. At 30 a day it is 10-28. Two publish cycles a day lands it by 10-27 even at 30 a day.
- **What stops a batch going above 20:**
  1. the MCP payload has to be transcribed by the model, about 37 KB per 2 pages;
  2. each image set must be on a pushed SHA;
  3. one review per page before shipping;
  4. a single daily publish window.
  - Proposal: a **ship script that sends the payload files with a Webflow API token from the keychain**, run only on your go, with the MCP still used for reads and checks. That removes item 1 and saves about 15k tokens a page.
- **Token cuts:**
  - script-based CMS writes (-15k a page);
  - slim review instead of full for rule-change reworks (-28k);
  - B's fix lists from `qc --json` (-15k);
  - batched one-class reworks (-20k);
  - chip_adds from a template plus a voice pass (-10k).
  - Target: rework about 30k, new page about 90k, review about 20–45k.
- **Rescue plan (60 or more):**
  - B: 31–45 from Form/Automation (PA12-clean A6 with 6+ sources: 13; with 5: 16; with 3–4 plus one credit: 35);
  - A: up to 19 parked in LP/SurveyQuiz;
  - replacements from the workbook's "Pass 3 new page ideas" (29 rows) and "AMBER pages & angles" (116 rows).
  - **Defaults:** the A6 order above, plus the AMBER list for replacements.
- **Daily rhythm:**
  - **06:00** B writes and reworks (holds first).
  - **10:00** A runs slim and full reviews, then batch-check, then CMS drafts with L12, then pre-flight.
  - **12:00** one approval packet for you: flags and PA13, the batch list, staging check results.
  - **12:30** your staging publish, then A's checks, then the re-hide rule.
  - **15:00** your production publish, then verify, relink and live audit.
  - **18:00** a second, smaller cycle if supply allows.

## Since the 12:30 draft (rulings 9 and 10)
- **Ruling 9 (SurveyQuiz to B):** recorded in DECISIONS, TWO_ACCOUNTS, `.hub` and hubctl (`WRITER_HUBS`). customer-experience-survey, onboarding-survey and wellness-survey were released to B with the note "ruling 9: B". The stale culture, dei and restaurant claims went back to queued. B was told in proposals.
- **Ruling 10 tooling (99e4356a):**
  - `hubctl feasibility` and `defer`; claim skips infeasible pages that already have a pull;
  - review lock (`ops/review_lock.py`, `lock_hash` on every review event, `hubctl unlock` for A only), checked at `ready` and in `sync.sh`;
  - `hubctl daily-batch`; `weekend.py preflight` for B's loop;
  - read-only `qc` and `paa` (`--stamp`, `--log`).
  - Golden suite: 337 cases, 0 regressions.
- **sync.sh fix (dc485620):** the review-lock step refused every commit without spec files (grep exit 1 under pipefail). Fixed; LESSONS line added.
- **Yield pilot and the throughput numbers:** see `1400-yield-pilot-throughput.md`, which supersedes the throughput plan above (the 500 date there assumed supply that the pilot does not support).

## Request
> (Divit's rulings 2026-10-13, 0-9, and the AlsoAsked blocker from Account B; quoted in full in the session: naming switch; review hash and slim review; reviews today; batch 3 to staging; gate 0 rejects and PA6 patterns; PA12 workbook ideas; collisions and holds; Learn refs; rule re-run around holds; throughput report.)

## Actions and results
- Commits, in order:
  - 941ce5b2: ruling 0;
  - abf26776: ruling 1;
  - 7c892597: reviews, PA6, PA12, collisions and re-run;
  - 4c59d4c5: the AlsoAsked fix;
  - 5edabbac, c0a5b1c8 and 32dd3688: batch 3;
  - 99e4356a: ruling 10 tooling; dc485620: sync.sh fix.
- Webflow: 20 creates in 10 calls (2 items each), each read back; isDraft-false updates read back (20 of 20 isDraft false, unpublished, Learn refs 20 of 20).
- Contact sheets regenerated for the 20 pages; the images were byte-identical.

## Numbers
- Slim reviews: 52 pages. Full reviews: 10 pages. Blocking findings: 9 pages.
- Golden suite: 331 cases. Batch 3: 20 staged; pre-flight 20 of 20.
- AlsoAsked: 3 credits, balance 740.

## Decisions
Every action above follows the matching ruling in DECISIONS 2026-10-13. The ship payload step also refuses pages that are not `reviewed` (ruling 6).

## Files changed and commits
ops/hubctl.py, ops/guards.py, ops/ship.py, ops/launch.py, ops/weekend.py, ops/alsoasked_pull.py, qc/paa_gate.py, qc/qc_hub.py, rules/paa_patterns.json, tests/golden/*, docs/TWO_ACCOUNTS.md, DECISIONS.md, LESSONS.md, proposals/account-b.md, .gitattributes, specs/*, status/*, logs/*. SHAs as listed above.

## Webflow calls
- Creates: 20 items, IDs in status/ship/batch-3.json.
- isDraft false: the same 20. Rollback: isDraft true, or delete (never published).
- Unhide for staging: 11 sections, done just before this report, then read back. Re-hide right after your staging checks.

## Not done
- Staging checks: after your publish.
- Production go: yours.
- church-membership-form review (held by B).
- Rework pages: B's 7 are back as reviewed; A's lead-generation-landing-page is done.
- recheck on B's pages: at the end of B's wave.

## Open questions for Divit
1. PA12: the workbook has no keyword ideas for 9 pages with no Semrush secondaries, including both golden pages. Should they stay parked (default), or may their gate-passing AlsoAsked questions count as their secondaries?
2. A ship script with a Webflow API token, run only on your go: yes or no?
3. Hero prompts naming an industry: about 40 Form/Auto pages, plus 3 in batch 3 (intake-form, rental-application-form, sign-up-form) that were outside slim scope. A sweep through B is the default. Fix the batch-3 three before production, or ship them?
