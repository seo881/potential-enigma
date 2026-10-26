# Resume note, B, 2026-10-26 (graceful stop by Divit)

## State
- SLUG MIGRATION IS LIVE on emergent.sh (Divit published 2026-10-23 16:02 UTC). Full verification (ops/slug_migrate.py verify-site --base https://emergent.sh):
  - every check passed: 336 new URLs (200, H1, canonical, carousel, Learn, FAQ); 291 old URLs as single-hop 301s; 843 redirect rows; sitemap (291 new listed, 291 old absent);
  - the "0 links to old URLs" check had 21 failures, all HTTP 0 (fetch errors on news and non-hub pages, not old links). 10 were re-checked: all OK. The other 11 are not re-checked yet; re-run only those pages.
  - Sitemap and Cloudflare: green, nothing to purge (B-qa-5).
- The full production AUDIT is UNRELIABLE: it ran 2026-10-23 21:43 to 10-24 06:03 while the Mac slept, and 252 pages failed on network errors. Re-run `bash ops/schedule/live_audit_checks.sh` with the Mac awake (about 50 to 95 min).
- FREEZE IS STILL ACTIVE (status/freeze.json). Do NOT lift it until the audit re-run is green and the 11 pages are re-checked.
- Ship queue: 43 pages (LP 12, Auto 3, Form 22, SQ 6) pass slug-check and ship-check on the new slugs (B-ship-4). They ship in groups of 5 once the freeze lifts (scratchpad ship5.sh per hub, explicit args).

## Close the migration (after green, in this order)
1. Apply the WIP patch .cache/migration/close-migration-WIP.patch (git apply; the agent died mid-task when the Mac slept). Or redo it: remove the TEMPORARY slug-guard (--migration) and rollback (--rollback) exceptions from ops/webflow_api.py and ops/ship.py; set status/freeze.json active=false (keep _freeze_check); make A2-slug blocking in verify-live and the audit; update the golden cases. Run tests/golden/run.py; only the known failures may remain.
2. Commit, lift the freeze, ship the 43 in groups of 5 with verify-live.
3. Divit: Search Console steps in reports/2026-10-23/search-console-steps.md (the sitemap is fresh, so resubmit any time).

## Rollback (emergency only)
`slug_migrate.py rollback-full`, then `hubctl api-update ops/out/migration/rollback-full.json --live --migration --rollback`. This needs the exceptions, so roll back BEFORE closing the migration. Glossary restore: childedits/2026-10-23/glossary-3-links.before.json. Redirects: re-import reports/2026-10-23/redirects-original-553.csv.

## Still open from earlier
- Skip-proof audit remainder (reports/2026-10-23/resume-note.md): stable-path launchd shim, GitHub Actions split rewrite, watchdog, post-ship hook; the dirty-tree skip in live_audit_daily.sh still exists.
- Navbar svg width="2o" (G1) and the Learn title en dash (G2): Divit's call.
- SurveyQuiz quiz canary: staging passed; the production canary is still to run.
- The default LP hero prompt "saves every signup" (56 specs); the assemble provenance bug.
