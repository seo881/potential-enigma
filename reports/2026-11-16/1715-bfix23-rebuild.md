# bfix23 rebuild and image slot guard (B-c-2)

## Request
"Don't run bfix23 as built; advisor review found errors: 1. dermaplaning-consent ... target awb---key-feature-1-image ... leave tab 2 untouched. 2. driver-application: add the cover-image and thumbnail-image fields ... 3. employment-verification-letter: add the thumbnail-image field. 4. employee-feedback: include the tab 4 fix if it's done and reviewed; otherwise ship it separately. 5. Prevent this: generate image payloads ... with the fixed slot map ..., never by hand; add a check that every changed image file has a matching field in the payload, with golden tests. Rebuild, run the dry run, and show me per item: field(s) written, old file -> new file. Then I'll run it."

## Actions and results
- The old payload (ops/out/ship/bfix23-form-update-6aaaaa02995bb2f9f4d6a36c.json) had already been run with --live at 10:31 UTC, outside any agent transcript (the B-fix-23 agent's own attempt at 10:25 was denied). It staged the 11 updates, stopped on 1 read-back mismatch (dermaplaning tab 2: Webflow kept the same file) and published nothing. Rollback: childedits/2026-11-16/bfix23-form-update-6aaaaa02995bb2f9f4d6a36c.20261116T103125Z.rollback.json.
- Guard added (ops/ship.py): fixed SLOT_FILE map; ship-update generates image fields from the slot files changed in git since the image base (--images-since now takes precedence over cms_draft.sha) and refuses when a changed slot file is left out, a field sends another slot's or page's file, or an unchanged file is re-sent (--allow-unshipped slug/file for deliberate exceptions). api-update runs the same check on every payload, hand-built or not; an image file sent with no image base is refused. The old bfix23 payload is now refused by api-update --dry-run.
- render.json is not used as the change signal: dermaplaning's render.json did not change in 910b6234 although uc-1.svg did; the git diff of the image files is the ground truth.
- Rebuilt as B-fix-23b with ship-update against the pre-write read-back (published values, so the before-values are the true rollback). Dry run clean.
- employee-feedback tab 4: not done (tab_content_4 and the mockup still say "after 2 weeks"); ships separately.

## Numbers
11 items, 15 fields: 12 image fields, 2 FAQ fields. Golden: 16 new image-slots cases pass. Full suite run pending at report time.

## Decisions
- Divit 2026-11-16 (this request), slot map and coverage check. CLAUDE.md non-negotiables: read before write, before-values committed first, item publish only.

## Files changed and commits
1b2e60ec: ops/ship.py, tests/golden/run.py, tests/golden/cases.jsonl, batches/B-fix-23b-form.txt, childedits/2026-11-16/*.B-fix-23b-form.before.json.

## Webflow calls
None by B-c-2 in this task. Pending Divit: `hubctl api-update ops/out/ship/B-fix-23b-form-update-6aaaaa02995bb2f9f4d6a36c.json --live` (11 updates and an item publish of the same 11).

## Not done
employee-feedback tab 4 fix; restamp and slim reviews of the 11 pages after the publish.

## Open questions for Divit
Run B-fix-23b.

## Update 18:15 IST: verification, rebuilt batches, full audit
- B-fix-23b (Divit's run): verify-live 11/11 PASS; every new file (dermaplaning tab 1; driver tab 3, cover, og; EVL tab 2, og) is byte-identical to its render on the CDN; tab 2 on dermaplaning is unchanged; file IDs are recorded in the specs (7937b647).
- B-fix-21r/22r/24r/34r rebuilt with the guard (36d2209b), run by Divit: verify-live 34/34 PASS, 36 image files byte-checked (0f5b5833).
- B-fix-29 (LP, now 11 items including chiropractic tab 2, dec57bc8/ec9a2392) and B-fix-45a (anesthesia-consent, 5146320a): dry runs clean, waiting for Divit.
- Full live audit full647 scored: last_success 2026-11-16 12:00 UTC, 644 pages + 4 hubs, P0 0. P1 by cause:
  - A7-link 648: LinkedIn company link returns 403 to the audit client on every page (bot block, not a broken link).
  - A9-chip-fight 282 / A9-prompt 280: known hero-backlog (known issue expires 2026-11-19).
  - A11-target 24: the known redirect issues (expire 2027-02-01).
  - A4-missing / A3-meta / A8-alt 40 on 25 pages: 21 are today's post-live fixes (approval stamp predates the fix), 2 clear with B-fix-29 (404-page, app), airline-questions has the same stale-stamp cause (fixed 11-13), LP chiropractic needed its fix shipped (now in B-fix-29).
  - A9-console 4: net::ERR_SOCKET_NOT_CONNECTED (network).
  - P2: A5-empty-p 648 (Webflow placeholder), A4-repeat 3 (since 11-10).
- 392 live pages carry a stale approval fingerprint: 140 changed today (7 slim reviewers B-s-901..907 running), 252 older (mostly the held hero-prompt rewrite).
- Morning daily run (pid 7341, started 09:07 on the pre-fix code) is still re-checking 497 pages serially and holds the lock; not killed (post-live QC never stops). Question for Divit.
