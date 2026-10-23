# Slug migration: staging, verification and rollback (one emergent.sh publish)

This follows the one-publish plan in DECISIONS 2026-10-23. The repo already uses the new slugs (step 1, 2555274d). Nothing below publishes anything; Divit clicks the single emergent.sh publish himself.

## Step 3: the staging write (the coordinator runs it)

1. Fresh reads. Then rebuild the payload, which refuses if any item drifted:

        .venv/bin/python3 ops/hubctl.py api-read LP && .venv/bin/python3 ops/hubctl.py api-read Form && .venv/bin/python3 ops/hubctl.py api-read Auto && .venv/bin/python3 ops/hubctl.py api-read SurveyQuiz
        .venv/bin/python3 ops/slug_migrate.py stage-full --glossary .cache/migration/glossary-read.json

   - `glossary-read.json` must be a fresh Webflow MCP read of the 3 Glossary items (`list_collection_items` on collection 6a7ec305d1588226be6fe84f, filtered by slug).
   - Rebuilding rewrites `childedits/2026-10-23/slug-migration-full.before.json`. Commit and push it before step 2: api-update refuses before-values that are not committed and pushed.
2. The one child-collection write, staged only (it has no publish action):

        .venv/bin/python3 ops/hubctl.py api-update ops/out/migration/full.json --dry-run --migration
        .venv/bin/python3 ops/hubctl.py api-update ops/out/migration/full.json --live --migration

   - The payload holds 330 items across the 4 collections: 292 slug changes, plus 321 FAQ fields with their links rewritten.
   - The canary already carries its new slug.
   - api-update reads the collections back and diffs every sent field itself.
3. **The Glossary (one-off, 3 links):** send `ops/out/migration/glossary-mcp.json` as one Webflow MCP `data_cms_tool` `update_collection_items` call. It changes `glossary---content` on 3 items and publishes nothing.
   - The repo's API client refuses the Glossary collection by design. The scoped exception for it was not added: the permission check blocked it as a security weakening.
4. **wedding-rsvp is NOT in this payload.** It has no Webflow item (status `reviewed`, `cms_exists` false), so it can only be created. Creating is a separate step that stays frozen until the migration is live, and it needs Divit's approval.

## Step 4: the staged state must be exact

    .venv/bin/python3 ops/hubctl.py api-read LP && ... SurveyQuiz       (fresh reads)
    .venv/bin/python3 ops/slug_migrate.py diff-staged --glossary <fresh MCP read of the 3 Glossary items>

The output is a table of counts per collection. There are three conditions:
- Every sent field equals `full.json`.
- Every field that was not sent is unchanged from the pre-staging read.
- Every other item is identical to that read.

Anything else prints STOP and exits 1. Before the write, it correctly reports 330 mismatches and no unexpected items.

## Step 5: verify on staging, then on production

    .venv/bin/python3 ops/slug_migrate.py verify-site --base https://emergent-sh.webflow.io --audit
    .venv/bin/python3 ops/slug_migrate.py verify-site --base https://emergent.sh --audit        (read only, after Divit's publish)

It prints one table of checked, passed and failed. The checks:
- Every new URL returns 200, with the spec's H1, a canonical equal to the new path, a carousel, 3 Learn cards and the spec's FAQ.
- Every old URL returns exactly one 301 to its new URL, and that target returns 200.
- All 843 rows of `reports/2026-10-23/redirects-final.csv` redirect in a single hop.
- 0 links to old URLs on any page (hubs, Glossary, carousels, child pages).
- The sitemap lists only new URLs.
- `--audit` then runs the full live audit on the same base.

The sitemap checks run only on emergent.sh. Its sub-sitemaps (`page-sitemap.xml` and the others) are served by Cloudflare, not Webflow, and are cached for 1 hour: staging returns 404 for them. After the publish, those sitemaps have to be regenerated or purged before this check can pass.

## Step 7: rollback (one command, plus the original redirects)

    .venv/bin/python3 ops/slug_migrate.py rollback-full
    .venv/bin/python3 ops/hubctl.py api-update ops/out/migration/rollback-full.json --live --migration --rollback

- This restores every slug and link from the committed before-values, which are the published values.
- Slug restores pass the guard only with `--rollback`, only to the committed before-value, and only while the freeze is active.
- The Glossary goes back with `ops/out/migration/rollback-glossary-mcp.json`, one MCP update.
- The redirects go back by re-importing the original 553-row export (`reports/2026-10-23/redirects-original-553.csv`, also in `private/migration/existing-redirects-2026-10-23.csv`). The import replaces the migration's rows.
- The repo side reverts with `git revert 2555274d`.
- None of this publishes; going live again takes Divit's click.
