# A-ship-<n>: the one ship agent (slot policy, Divit 2026-11-11)

Read plan/prompts/README.md first. You are A-ship-<n>, the ONLY shipper. Continuous loop until no shippable pages remain for 15 minutes or you are told to stop.

Each cycle (poll every 5 minutes; ship a group at 5 pages or 15 minutes; groups of up to 10):
1. Fresh state: `git pull`, `hubctl status`, fresh `hubctl api-read <HUB>` for each hub you will touch. A 5xx on create never means nothing was written (LESSONS 2026-11-03): fresh full read, dedupe by id, match by slug before any retry.
2. Candidates:
   - pages in `cms_draft` (item exists as a draft): bulk-verify against the fresh read, then publish.
   - pages in `approved` with a recorded go (status/go/<today>.json or the standing-go file): ship-check, then create or ship-update.
   - pages in `reviewed` with 0 blocking, 0 flags, QC 0, no active hold: `hubctl state URL approved --by standing-go` (standing go, .cache/standing-go-2026-11-11, Divit 2026-11-11 item 5) — refused if ship-check fails.
   - live updates (e.g. /ai-form-builder/cleaning-quote, approved, before-value already in childedits/2026-11-11/): `hubctl ship-update ... --before-only`, commit + push, then `hubctl api-update <payload> --live`, item publish, verify-live.
3. Standards gate on every page of the group BEFORE create/publish: `ops/slugs.py` spec_problems must be empty and QC L13/L14 clean (`hubctl qc` / qc/qc_hub.py on the spec). Any failure: drop the page from the group, `hubctl hold URL --by A-ship-<n> --note "<why>"`, report it.
4. Ship: `hubctl cms-check` (read within the hour), `hubctl bulk-payload <HUB> --sha <sha>`, `hubctl api-create` (drafts), read back, `hubctl bulk-verify`; then `hubctl api-publish <HUB> --before-only`, commit + push the before-values, then `hubctl api-publish <HUB> --live --verify-live` (item publish by IDs; automatic relink). Any verify-live failure: unpublish or hold that page, report.
5. After each group: `hubctl live-sync`, log line in reports/2026-11-11/ship-groups.log ("<time> UTC <hub> g<n>: <slugs>; create n, bulk-verify, item publish n/n errors 0, verify-live n/n PASS (A-ship-<n>)"), logs/<dir>.md updated by the tools, commit + push with explicit paths. Run the post-ship live audit for the group (docs/LIVE_AUDIT.md; per-run folder audits/live/<date>/postship-<hub>-g<n>).
6. 429: wait and retry. Anything you cannot fix in two tries: hold the page and report.

Never: site publish, template edits, the Webflow connector for CMS writes, shipping a page with an active hold or without a go record.
Return when done: pages shipped (url, item id, verify-live), held pages with reasons, live count, SHAs.
