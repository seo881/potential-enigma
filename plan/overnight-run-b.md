# B's overnight run, 2026-10-15 night (DECISIONS 2026-10-15 night; ruling 20 and 22)

Account B runs the loop in its own clone `~/emergent-hubs-a` (CLAUDE_CONFIG_DIR=~/.claude). Every headless session starts with "Continue the overnight run per plan/overnight-run-b.md". Read CLAUDE.md, LESSONS.md, DECISIONS.md (the "2026-10-15 (night)" section first) and this file.

- start (coordinator): `cd ~/emergent-hubs-a && git pull -q --rebase origin main && rm -f STOP && mkdir -p .cache/overnight-b && touch .cache/overnight-b/ruling19-lift-2026-10-15 && nohup bash ops/schedule/overnight_run_b.sh >/dev/null 2>&1 &`
- watch: `tail -f ~/Library/Logs/emergent-overnight-run-b.log`
- stop: `touch ~/emergent-hubs-a/STOP` (a clean stop after the current session)

## Tonight's frame (code-enforced)

- **Ruling 19 is lifted for this loop only** while `.cache/overnight-b/ruling19-lift-2026-10-15` exists (under 18 hours old). Then `hubctl api-create | api-update | api-publish` are allowed and `webflow_api` lets exactly those write under EMG_HEADLESS. ops/ship.py, webflow_api.py direct calls, every Webflow MCP tool, the Designer and any site publish stay denied. The loop's exit trap deletes the lift file (ruling 19 restored; time in `.cache/overnight-b/ruling19-restored`).
- **Stops:** 200 live child pages (status/live.json; `overnight_b.py next` exits 6 and the loop touches STOP; after that no shipping, writing or reviewing), 24,000,000 tokens (`.cache/overnight-b/tokens.jsonl`), the second 5-hour session limit (the first resumes after its reset), STOP.
- **Ship stop:** any verify-live failure holds the page (state cms_draft, note HOLD) and writes `.cache/overnight-b/ship-stop`; every API write then refuses for the night. Unpublish is not on the API allowlist, so nothing is unpublished. Writing and reviewing continue.
- **AlsoAsked:** at most 60 credits, run `night-r1015`: `.venv/bin/python3 ops/weekend.py aa URL --run night-r1015` (the key comes from the keychain inside that run; never exported, never printed; credits.log as usual).

## Order of work

Run `.venv/bin/python3 ops/overnight_b.py next` and work its list in order. One page per writer subagent, up to 10 in parallel; ruling-15 pipeline only (`ops/skeleton.py build`, the section checks, `assemble`, `check all`).

0. **Ship** (when `next` lists pages under "0 ship"): see "Shipping" below. Shipping first keeps the night moving toward 200.
1. **Reworks:** every page in `rework`. Fix only the blocking findings named in its note or latest review; keep every other field byte-identical. QC to 0, gate 0 rejects, re-render if the images changed (`hubctl images`), then `hubctl ready URL --by B-w-<n>`. One rework per page, by a writer who did not write the page's reviewed version.
2. **In-flight B pages:** finish them (claimed or spec). 2b. **Slim reviews:** every `reviewed` page whose text changed after its review gets a B-s slim review of the changed fields (`hubctl review-diff`, `hubctl slim-review URL FILE --by B-s-<n>`, never by a writer of the page).
3. **Render** every `qc_pass` page (`hubctl images URL`) and read its contact sheet: one hero, readable text, numbers that add up.
4. **Review** every `images` page with an independent **B-r** agent (page-reviewer), up to 4 pages each, severity from rules/SEVERITY.md only. Slim reviews (B-s) for changed fields. Blocking -> `rework` (one rework, then `hubctl ready`); no second full review.
5. **Claim** from the top of `plan/queue-ranked.txt` (`hubctl claim HUB N --by B-w-<n>`), all 4 hubs. Quiz pages only once `status/quiz-canary.json` says `pass`. **Relevance check before writing:** the primary keyword must be a build intent for the hub (someone who wants to make this page, form, automation or survey). A doubtful page is parked, not written: `hubctl state URL parked --note "relevance: <one line why>" --by B-w-<n>`.
6. **Pulls** (only when `next` lists them, keychain ok): `weekend.py aa URL --run night-r1015` for the listed no-pull rows, then `.venv/bin/python3 ops/queue_rank.py` and commit plan/queue-ranked.txt.

**Learn references (every new page):** the writer picks 3 topic-relevant published Learn articles from `.cache/learn/inventory.json` (`published: true`) into `spec.learn_refs` (a list of 3 item IDs). Never the old default trio (`hubctl.OLD_LEARN_TRIO`); a create refuses missing refs or the trio. Check with `hubctl learn-check URL`. A reviewed page without refs gets them from a B-w writer before shipping (learn_refs is outside the review hash and the approval fingerprint).

After each review batch, list flagged FAQ questions: `.venv/bin/python3 ops/flag_packet.py list <reviewed URLs> --batch b-<HHMM>` (writes to .cache; note its path and counts in the commit message).

## Shipping (standing go; batches of at most 10)

Every command is one plain `.venv/bin/python3 ops/hubctl.py ...` call (or `bash ops/sync.sh ...`); no pipes, no `&&`, no other scripts.

1. `.venv/bin/python3 ops/overnight_b.py cap`: the room left under 200. The batch is at most 10 and at most the room, so the last batch lands on exactly 200 (`api-create` and `api-publish` cut the list themselves while the lift holds).
2. For each candidate: `hubctl ship-check URL` (QC 0, gate 10/10, review current, no pending flag, images current, Learn refs, hero prompt: QC L10 plus the generic-default rule of DECISIONS 2026-10-09). Read the hero prompt yourself too: generic, primary keyword, no industry, name or scenario. PASS -> `hubctl state URL approved --by standing-go` (accepted only while the lift file exists; logged "standing-go (Divit 2026-10-15 night)"). FAIL -> leave it and note why.
3. **New pages (no item ID):** `hubctl api-read HUB` -> `hubctl cms-check HUB <readback>` -> commit and push the specs and images (`bash ops/sync.sh`) -> `hubctl api-create HUB --sha <pushed HEAD> --before-only` -> commit the before file -> `hubctl api-create HUB --sha <same sha> --live` (drafts, read back, bulk-verify, file IDs recorded, state cms_draft).
4. **Old drafts (item ID, approved):** write the URLs to `.cache/overnight-b/batch-<HHMM>.txt` -> `hubctl api-read HUB` -> `hubctl ship-update <batch> <readback> --before-only` -> commit the before files -> `hubctl ship-update <batch> <readback>` -> `hubctl api-update ops/out/ship/<batch>-update-<cid>.json --live` -> `hubctl api-read HUB` -> `hubctl ship-update <batch> <new readback> --verify` (file IDs recorded from the read-back; approved -> cms_draft).
5. **Publish:** `hubctl api-publish HUB --before-only` -> commit the before file -> `hubctl api-publish HUB --live --verify-live` (item publish only; verify-live on every page, PASS -> published; automatic relink). A FAIL holds the page and stops all shipping (ship-stop): do not retry, do not work around it.
6. Flagged pages are never shipped and never block a batch: every ship command prints `HOLD <url>: flags pending (morning packet)` and adds the page, Q number and flag subtype to `.cache/review/morning-packet-<date>.md`.
7. Commit after every step with `bash ops/sync.sh "<msg>" <exact paths>` (specs, status, logs, childedits, status/live.json, status/ship): only the files you changed.

## What B never does tonight

- No site publish, no Designer, no Webflow MCP, no ops/ship.py or webflow_api.py calls; no unpublish.
- No rule, QC, tooling, template or config changes; propose them in `proposals/`.
- No question text, SERP data or anything from `private/` or `.cache/` in commits or reports.
- Each agent commits only its own files via ops/sync.sh. The message names the page, the agent id and the result (QC, gate, review, ship).
- Log tokens per page with `hubctl usage-log URL TOKENS --role writer|review --agent <id>`.

## The morning (08:00 IST)

When the loop ends (cap, budget, second session limit, STOP or nothing left at 08:00 IST), the last session writes `reports/<date>/0800-overnight.md`, under 15 lines: pages written, reviewed, approved by standing go, created, published and verified (live count against 200), holds (flags, verify-live), tokens used (tokens.jsonl), session limits hit, AlsoAsked credits (run night-r1015), the morning packet path, and that ruling 19 was restored (time). Add a line to `reports/INDEX.md` (newest first) and commit both with `bash ops/sync.sh`. The coordinator records the restore in DECISIONS.md.
