Run the live audit per docs/LIVE_AUDIT.md (DECISIONS 2026-10-09). Arguments for this run: {{ARGS}}

Read LESSONS.md and docs/LIVE_AUDIT.md first. Then, in order, without asking anything (this is an unattended run):
1. `.venv/bin/python3 ops/hubctl.py live-audit {{ARGS}}` (Layer A). Note the date it prints.
   FIRST, before anything else and even in a dry run (Divit 2026-10-09): if the digest starts with "P0 HELD PAGE LIVE", send each
   ops/out/live/ID.unpublish.json it names with data_cms_tool (unpublish_collection_items, then the read back), save the response, run
   `hubctl live-audit held-done ID RESPONSE`, and keep that line at the top of your reply.
2. Layer B: for each `.cache/live/DATE/layerB-N.md` it lists, spawn one page-reviewer agent with that file as its brief (4 pages per agent);
   when each finishes, run `.venv/bin/python3 ops/hubctl.py live-audit record DATE .cache/live/DATE/layerB-N.json`.
3. If any finding has action drift-check and this is not a dry run: read those CMS items with the Webflow MCP
   (list_collection_items filtered by id; session_id start, agent_id opus|claude-code|audit), save the result to
   .cache/live/DATE/drift-readback.json and run `hubctl live-audit drift DATE .cache/live/DATE/drift-readback.json`.
4. If this is NOT a dry run, for each finding with action fix or fix-by-writer (P0 first):
   a. fix-by-writer: `hubctl live-fix brief ID`, spawn one page-writer agent with that brief; fix: `hubctl live-fix apply ID`.
   b. commit and push via `bash ops/sync.sh "<msg>" specs images`.
   c. read the item with the Webflow MCP into .cache/live/DATE/ID.readback.json; `hubctl live-fix prepare ID --readback that file`.
   d. send ops/out/live/ID.json with data_cms_tool exactly as written (update, publish that item only, read back); save the response;
      `hubctl live-fix verify ID RESPONSE`. If it prints VERIFY FAILED, send the rollback file it names at once, then
      `hubctl live-rollback ID --done RESPONSE`.
   Only these Webflow actions are allowed: list_collection_items, update_collection_items, publish_collection_items, and
   unpublish_collection_items for a held page that is live (A0). Never a site publish,
   never create, delete or unpublish, never a template, component, class, page or hub change.
5. `hubctl live-audit report DATE` (add --dry for a dry run), then `.venv/bin/python3 tests/golden/run.py`.
6. `bash ops/sync.sh "Live audit DATE" audits reports tests/golden childedits specs images status`.
7. Reply with the digest line only.
