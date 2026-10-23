# Slug migration canary (2026-10-23)

**Status: the canary is prepared but NOT staged.** The staged write (`hubctl api-update ... --live --migration`) was blocked by Claude Code's permission check, so nothing has been written to Webflow. Divit runs the one command below himself, or approves it. Nothing is published either way.

## Canary

| | |
|---|---|
| Page | Form `accident-report-form` (live, item `6acf52edf6ceb166b92077bc`, not a quiz) |
| Old URL | /ai-form-builder/accident-report-form |
| New URL | /ai-form-builder/accident-report (`slugs.slug_for("Form", "accident report form")`; the new URL returns 404 today) |
| Inbound links | 1: the FAQ (`awb---faq-data`) of `daily-report-form` (item `6ad09f43e35e19e82573e41f`) |
| Payload | `ops/out/migration/canary-accident-report-form.json`: 1 PATCH, 2 items. It sets the slug on 6acf52ed... and the FAQ field with the one link rewritten on 6ad09f43.... It has no publish action. |
| Before-values | `childedits/2026-10-23/slug-migration.before.json` (committed and pushed in 7106fca5) |
| Rollback | `ops/slug_migrate.py rollback --canary accident-report-form` writes `ops/out/migration/rollback-canary-accident-report-form.json`. The FAQ restore runs through api-update. The old slug goes back by hand in the CMS editor, because the approved guard exception covers only the new slug. |

Command to stage it (staged only):

    .venv/bin/python3 ops/hubctl.py api-update ops/out/migration/canary-accident-report-form.json --live --migration
    .venv/bin/python3 ops/slug_migrate.py verify ops/out/migration/canary-accident-report-form.json .cache/readback/form-api-<newest>.json

The first command reads the collection back and diffs every sent field itself. The second repeats that diff from a fresh `hubctl api-read Form`.

## Staged vs live, before the canary (all 4 collections and the 4 hub pages)

- **CMS items:** read at 13:42 UTC, 339 items. **0 items** have `lastUpdated` later than `lastPublished`. No draft or archived item carries a pending change. The Data API exposes no published copy of an item to diff field by field (`ops/webflow_api.py` refuses the live-item endpoints), so the check is per item. Per item it is exact.
- **Hub pages:** each page's `lastUpdated` (pages API) is older than the site's last publish, which is "Last Published: Fri Oct 23 2026 12:52:10 GMT" in the live HTML of all 4 hubs and both canary pages.

| Hub page | lastUpdated |
|---|---|
| /ai-landing-page-builder | 2026-10-20 14:12 |
| /ai-form-builder | 2026-10-19 16:00 |
| /ai-automation-builder | 2026-10-19 15:59 |
| /ai-survey-and-quiz-builder | 2026-10-19 15:48 |

  So no hub page has a pending change.
- **After the canary is staged,** exactly 2 items will be pending: 6acf52ed... (slug) and 6ad09f43... (FAQ).
- **Nothing else is staged.** That includes the full set, wedding-rsvp, and every other link rewrite.
- **Limit:** template, style and component changes elsewhere on the site are not visible through the API. Check that the Designer's Publish dialog lists no other changes before clicking.

## For Divit, in this order (after the staged write and its clean read-back)

1. **Add the redirect.** Do NOT use CSV import: an import replaces every existing 301 on the site.
   - Webflow Dashboard > the site > **Site settings** > **Publishing** tab > **301 redirects**
   - **Old path:** `/ai-form-builder/accident-report-form`
   - **Redirect to path:** `/ai-form-builder/accident-report`
   - Click **Add redirect path**, then **Save changes**.
2. **Publish the custom domain only.** Open the Designer, click **Publish** (top right), and in the dialog:
   - Tick **emergent.sh**, plus **www.emergent.sh** if it is listed: it is the same production domain.
   - Untick the **\*.webflow.io** staging subdomain.
   - Then click **Publish to selected domains**.
3. Tell the coordinator. Verification follows:
   - the old URL returns a single-hop 301 to the new one;
   - the new URL returns 200 and passes verify-live;
   - daily-report-form's FAQ link points to the new URL;
   - the sitemap lists the new URL.

The same row is in `reports/2026-10-23/canary-redirect.csv`.
