# Handback to B, 2026-10-26 (A was coordinator and only shipper today; DECISIONS 2026-10-26)

## State at handback
- **LIVE: 361 child pages** (339 this morning + 22 today: LP beta, church, click-through, consulting, crypto, holiday, local-business, minimalist, news, pest-control, plumber, subscription; Form botox-consent, equipment-rental-agreement, legal-intake, silent-auction, wedding-rsvp, copyright-release, insurance-verification, interior-design-questionnaire, it-request, lash-extension-consent).
  - All 22 pass verify-live (200, H1, canonical, meta, FAQ, images, hero prompt, carousel links, 3 Learn cards, 91 internal links all 200).
  - All 22 pass the slug rule, with no links to old URLs, and appear in their hub carousel.
  - Console: 0 real errors on all 22.
  - Sitemap: the 5 Form group-2 pages were missing at 14:4x IST; see the recheck line at the end.
- **SHIPPING IS STOPPED by Divit.** No create or publish until he says go.
  - 5 Form pages are unpublished CMS drafts and stay drafts: payroll-change, drug-test-consent, surgery-consent, sublease, personal-injury-intake (items 6adf208c2497f015bc9bf5a7/…5a9/…5ab/…5ad/…5af).
  - surgery-consent is held: its Q1 PA7 decision is Divit's, and it waits until shipping restarts. The same applies to food-bank-application's Q1.
- **Slug migration closed, freeze lifted** (6720cf63), on the full production audit run #19. The temporary --migration and --rollback exceptions are removed. G1 is closed: KS fixed the navbar svg, and the element exception is removed (97c2d88b).
- **Golden: 1034 cases.** The only regressions are the 3 known pre-existing ones: r15-brand-plus-moat, quiz-ship-block-quiz-page, pa9-donation-q9-still-rejected.
- **New guards (9c0f79f5):**
  - Every ship, create, update and publish path refuses a held page.
  - `approved` needs a recorded go: a dated standing-go file, or `hubctl go-record DATE --urls … --quote "…" --by <coordinator>` (status/go/DATE.json). A typed `--by divit` no longer approves.
  - ship-check also refuses post-review edits without a slim review (golden ship-postreview-*, e74ece1a).

## For B, in order
1. **approval-workflow:** record A-s-13's slim review and clear the hold. Run `hubctl slim-review /ai-automation-builder/approval-workflow .cache/review/slim/approval-workflow-A-s-13.json --by A-s-13` from A's clone, or copy the file over; all 3 fields pass with no findings. Then `hubctl unhold … --by B-…`. Then **clear the 42 resolved B holds** listed in status/hold-clearances-2026-10-26.md: each page is published, audited clean, and its text is unchanged since review. `unhold` refuses another account, so only B's clone can remove them.
2. **Backlog, low priority:** for the 35 live pages reviewed before 2026-10-13 (no review hash), compare their spec text at the review commit (git history) with today's live text, and report any differences. For all other live pages, live CMS text equals the spec (358 compared today, 0 differ) and the spec equals the reviewed text, except approval-workflow (item 1).
3. **Watchdog repo file:** switch it to B's clone with `echo "$HOME/emergent-hubs-a" > "$HOME/Library/Application Support/emergent/repo"`. launchd runs the watchdog through the stable shim `~/Library/Application Support/emergent/run.sh`, which reads that file (94768fac).
4. **Shipping is stopped by Divit.** The 18 approvals need a recorded go in the new format before anything ships: 11 Form, 6 SurveyQuiz, plus payroll-change. They are A-ship-3's approvals that fall inside Divit's morning go. Without a go record, ship-check and api-create refuse them. Record a go only when Divit gives one.
5. **Redirect check in the daily audit (Divit, both runners):** check all 843 rows of reports/2026-10-23/redirects-final.csv daily on the Mac script and the GitHub Actions matrix. Each source must return a single 301 to its target, and each target must return 200. Alert on any change: add it to the digest, and to the watchdog's real-failure count.

## Also open (from today)
- **Unlock is B-coordinator only:**
  - wedding-photography-questionnaire's rework is saved at A's .cache/wip-2026-10-21/wedding-photography-rework.patch and needs 5 fields unlocked (proposal in plan/proposals-from-A.md).
  - food-bank-application's why_intro fix waits for an unlock too. FAQ 5 is fixed (996bf355). The ready why_intro text: "A printed food bank application form PDF is typed up after the line clears. A built form saves each family to a database you own." That page is held for Q1.
- **Slug-migration tool gap:** `slug_migrate.py repo-rewrite` updated `fields.slug` only when it equalled the old slug exactly. 7 A drafts kept a stale slug, which trips QC K3. All 7 are fixed by hand and logged in history. Fix the tool for future migrations.
- **Mac full audit:** the 09:13 launchd run (B's clone) stalled. The Mac slept, then all 336 pages were re-run serially. A's caffeinated run is queued behind its lock. Divit accepted run #19 (GitHub Actions) as today's green full audit. Report the Mac result only if it disagrees.
  - B's clone ran it with uncommitted changes and did not pull. Clean that tree.
  - Stopping the stalled process was denied by the permission system.
- **Backup audit Action:** rewritten as a matrix (3c33fc8b). Manual run #19 succeeded: shards 21–29 min against a 45 min limit, score 11 min. The old serial job had hit its 40 min limit every day since 10-17.
- **Watchdog:** it now alerts on a failed or cancelled backup run, counts only real failures (known open issues in rules/live_audit.json), and its dialog opens the report.
- **Held-page audit false positive fixed** (67051ed5; golden audit-held-*). Old ledger URLs that 301 to a published page are no longer P0, and a fix run would no longer propose unpublishing live pages.
- **Open Divit calls:**
  - surgery-consent Q1 and food-bank-application Q1 (PA7 definitions).
  - G2: the Learn title en dash on 42 pages.
- **A's state:**
  - No writers, claims or reviews running.
  - A's Form claims: 13 written and reviewed, 4 in rework or slim review (see above).
  - A weekly at about 27% this morning; new claims were paused at Divit's stop.

## Commits (today, A)
ccbb480a, 80ec9e46, 3c33fc8b, 98aaac4b, 94768fac, 023f177a, 4934d819, c918f33f, 67051ed5, 6720cf63, 97c2d88b, 2d19a277, 9c0f79f5, 06a9128d, e74ece1a, and the writers', reviewers' and ship agent's commits in between.
