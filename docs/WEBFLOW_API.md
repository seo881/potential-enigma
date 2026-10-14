# Webflow API and MCP behaviours we learned the hard way

One row per behaviour: what the call does, what it actually publishes, and the rule we follow. Add a row whenever a read-back looked right and the published page did not.

| Date | Call | Read-back says | Published page does | Rule |
|---|---|---|---|---|
| 2026-10-13 | `data_element_settings_tool` set_settings `link` = `{mode: collectionPage, to: <pageSlug>}` on a Link Block inside a Collection List (carousel `build_link`, Learn `blog_link`) | `{mode: collectionPage, to: {pageSlug: detail_...}}`, exactly as written | renders the slug as a literal relative href (`/<hub>/detail_ai-<hub>-builder`, `/<hub>/detail_learn`), which 404s on every card | A collectionPage link is not proven by its read-back. Staging must resolve every card href and get HTTP 200 before any production go. Until a working API shape is confirmed, set these links in the Designer (Link Settings, collection page of the current item). |
| 2026-10-13 | `publish_collection_items` on CMS items | `publishedItemIds`, `errors: []` | items go live on emergent.sh without a site publish; template (Designer) changes stay staged | CMS changes go live only this way (no site publish, Divit 2026-10-10). |
| 2026-10-13 | MCP reads (`query_elements`, `get_settings`, `list_collection_items`) in quick succession | HTTP 429 `too_many_requests` | n/a | Wait about 75 s and retry the same read; never treat a 429 as a pass. |

## Direct Data API v2 for CMS item writes (Divit, 2026-10-14)

From the next batch on, CMS item writes go through `ops/webflow_api.py` (called only by `ops/ship.py`, through `hubctl api-*`), not the connector. The connector stays for Designer-level reads and anything this script must not do.

**Token:** macOS keychain, service `webflow`, read at call time with `security find-generic-password -s webflow -w`. Never printed, logged, written, put in an exception or in the repo; Authorization is redacted in debug output (`WEBFLOW_API_DEBUG=1`); redirects are refused so the header never leaves api.webflow.com. Golden `api-no-token` proves a sentinel token never reaches stdout, stderr or an exception, even when the server echoes it.

**Allowlist** (one function, `webflow_api.check`, runs before any token read or network call; everything else raises `Refused`):

| Method | Path | Limits |
|---|---|---|
| GET | `/collections/{cid}/items` | query `offset`, `limit` (1-100) only; staged read, drafts included |
| GET | `/collections/{cid}/items/{item_id}` | none |
| POST | `/collections/{cid}/items` | `{items: [1-100]}`, each `isDraft: true` with a name and a slug; no duplicate slugs |
| PATCH | `/collections/{cid}/items` | `{items: [1-100]}`, each with an id; never a slug, `isArchived`, or `isDraft: false` |
| POST | `/collections/{cid}/items/publish` | `{itemIds: [1-100]}` (item publish only) |

`{cid}` must be one of the 4 child collection IDs in `config/collections.json`. Site publish (`/sites/...`), delete, unpublish (`.../live`), schema reads, pages, components, other collections and every other path are refused in code (golden `api-refuse-*`, 16 cases; `api-allow-*`, 5 cases).

**Rate limits:** a 429 honours `Retry-After` (else 2, 4, 8 ... s, cap 60), up to 6 tries. GET also retries 5xx and network errors; a write whose outcome is unknown is never retried blind: the command re-reads the collection, and creates are idempotent by slug.

**Commands** (dry run is the default and sends nothing; `--live` is required for every network write):

| Command | What it does |
|---|---|
| `hubctl api-read HUB [--out FILE]` | Full paginated read to `.cache/readback/<dir>-api-<time>.json` (the read-back shape `cms-check`, `bulk-verify`, `ship-update` and `relink-payload` parse). Prints the count only |
| `hubctl api-create HUB --sha SHA [--limit N] [--readback F]` | The `bulk-payload` list (approved, no item ID, review hash current, approval fingerprint, slug check within the hour, not held by the other account). Dry run: the planned POSTs (100 per call) with slugs, existing slugs skipped against the newest stored read |
| `... --before-only` | Fresh read; writes `childedits/<date>/<dir>.api-create.<sha7>.before.json` (the slugs to create, absent in that read). Commit and push it |
| `... --live` | Refuses unless the before-value is committed, pushed and covers every slug, and SHA is on origin/main. Fresh read, skips every slug that exists, POSTs drafts in batches of 100, writes `childedits/<date>/<dir>.api-create.<sha7>.<time>.rollback.json` (IDs created) after each batch, reads the collection back and runs bulk-verify (isDraft true too) on the batch -> `cms_draft` |
| `hubctl api-update PAYLOAD.json [--live]` | Runs a `ship-update` / `relink-payload` payload (`ops/out/ship/*.json`): each item needs a committed and pushed before-value in `childedits/` covering its fields. Writes the rollback payload (the before-values, same format: `hubctl api-update <rollback> --live` restores) before the write; PATCH 100 per call; reads back and diffs every sent field; a mismatch stops before any item publish |
| `hubctl api-publish HUB [--limit N] [--before-only\|--live] [--verify-live]` | Item publish of exactly the verified `cms_draft` pages' IDs (fingerprint unchanged since approval), 100 per call. `--before-only` writes their before-state (isDraft, lastPublished, lastUpdated) to `childedits/<date>/<dir>.api-publish.<key>.before.json`; `--live` refuses unless it is committed, pushed and still current. `--verify-live` waits 15 s, runs verify-live per URL (one retry after 30 s), and sets `published` on a pass |

Every request is logged as one JSON line in `logs/api/<date>.jsonl` (op, collection, count, IDs, slugs; never a response body or the token), and every write as one line in `logs/<dir>.md`. Rollback: created drafts and published items are listed in the rollback files; deleting or unpublishing is not on the allowlist and is done in the Webflow CMS on Divit's go.

**Ship order for a batch:** `api-read` + `cms-check` -> `api-create --before-only` -> `ops/sync.sh` -> `api-create --live` -> `ops/sync.sh` (item IDs, states) -> Divit's go -> `api-publish --before-only` -> `ops/sync.sh` -> `api-publish --live --verify-live` -> `ops/sync.sh`. First real run: `--limit 2` (canary), checked in the Designer, then scale.

**UNVERIFIED until the 2-item canary** (record the result here): the create response shape for a list body (`{items: [...]}` assumed; the read-back is authoritative either way), the publish body `{itemIds}` (the connector sent `{items: [{id}]}`), and the time Webflow takes to import 6 image URLs per created item. Verified 2026-10-14: the keychain token authenticates and `GET /collections/{cid}/items` paginates (SurveyQuiz read, 1 call, 1.9 s).
