# Two Claude Code accounts on one Mac (Divit, 2026-10-13)

Target: 500 pages live by 2026-10-27. Two accounts work in parallel, each in its own clone of this repo. CLAUDE.md, DECISIONS.md, RUNBOOK.md, HUB_RULES and LESSONS.md apply to both; this file only splits the work.

## 1. Who owns what

| | Account B (coordinator) | Account A (writer) |
|---|---|---|
| Clone | `~/emergent-hubs` | `~/emergent-hubs-a` |
| Hubs it writes | LP, SurveyQuiz | Form, Auto |
| Stages | write and rework (LP, SurveyQuiz); **review of every page** (A's included); images check; create, stage, item publish, verify, relink, live audit, retro; rules and tooling; rescue marking; the daily approval packet | write, rework, re-render images (Form, Auto), in this order: rework pages first, then queued pages, then parked pages B has released for rescue |
| Webflow | the **only** Webflow writer (every call per CLAUDE.md) | **none**: no Webflow MCP, every Webflow tool denied |
| Schedulers (launchd, publish watcher, live audit, weekend loop) | B only | none |
| May edit | everything, per CLAUDE.md | only `specs/form/`, `specs/aab/`, `images/form/`, `images/aab/`, `status/form.json`, `status/aab.json`, `status/usage.jsonl` (append only), `proposals/account-a.md` |
| Never edits | A's pages while A holds them (states `claimed`, `rework`) | `rules/`, `qc/`, `ops/`, `pipeline/`, `tests/`, `config/`, templates, `DECISIONS.md`, `LESSONS.md`, `RUNBOOK.md`, `CLAUDE.md`, `status/ship/`, `plan/`, other hubs' files |

A page is held by one account at a time, by state:
- **A holds** a Form/Auto page in `claimed` and `rework`.
- **B holds** it from `images` onward (`images` → review → `reviewed`/`rework` → `approved` → CMS → `published`).
- **B's batches win:** any page listed in a ship batch file (`plan/batches/batch-*.txt`) is B's from the moment the file is pushed, whatever its state. A never edits or claims it (2026-10-13: A and B both fixed 4 batch-3 pages; B kept A's commit and added the name sweep).
- `rework` goes back to A, which fixes the blocking findings only, re-renders, then runs `hubctl ready <url> --by A-<id>` → `reviewed`. One review per page and one rework (CLAUDE.md step 5). The writer and the reviewer are always different agents; hubctl refuses otherwise.

## 2. One-time setup of A's clone (Divit or A, before A starts)
1. Start from a clean tree: `cd ~/emergent-hubs-a && git status` must show nothing modified (discard local changes, then `git pull --rebase`).
2. `echo "Form,Auto" > ~/emergent-hubs-a/.hub`. `hubctl claim` then refuses LP and SurveyQuiz in that clone. B's clone gets `LP,SurveyQuiz`. `.hub` is git-ignored.
3. No Webflow:
   - in `~/emergent-hubs-a/.claude/settings.local.json`, add `"deny": ["mcp__webflow", "mcp__claude_ai_Webflow"]`;
   - do not connect the Webflow MCP in that account.
4. AlsoAsked shared with B, so the credit caps hold across both clones:
   - `rm -rf ~/emergent-hubs-a/private/alsoasked && ln -s ~/emergent-hubs/private/alsoasked ~/emergent-hubs-a/private/alsoasked`. Do this only while A has no pulls of its own.
   - The `alsoasked` lock is machine-wide (`~/.emergent-hubs/locks/`, ops/guards.py).
   - Pull only through `weekend.py aa` (key from the keychain). Never run ops/alsoasked_pull.py directly.
5. `bash ops/setup.sh` in A's clone (A renders images locally).

## 3. Claim protocol
1. `git pull --rebase` **immediately before** every claim.
2. Claim only in your own hubs: A uses `.venv/bin/python3 ops/hubctl.py claim Form|Auto N --by A-<id>`, B uses `claim LP|SurveyQuiz N --by B-<id>`. At most 25 per claim.
3. Commit and push the status file at once: `bash ops/sync.sh "claim: <hub> N (A)" status/form.json`. A claim is not valid until it is on origin.
4. Rework pages are not claimed; they are already A's (state `rework`). Parked pages are claimable only after B releases them (`hubctl release <url> --note "<reason>"`, then the state is queued). A never releases a parked page itself.
5. Agent IDs:
   - A uses the prefix `A-` (writers `A-w-<n>`);
   - B uses `B-` (writers `B-w-<n>`, reviewers `B-r-<n>`).

## 4. Commit protocol
- Always use `bash ops/sync.sh "<message>" <explicit paths>`. It pulls with rebase and autostash, refuses conflict markers, then commits and pushes. Never `git add -A`, never force-push, never `git reset --hard`.
- **One page = one commit**, as soon as it reaches its stage: `specs/<hub>/<slug>.json`, `images/<hub>/<slug>/` and `status/<hub>.json`.
- Before any hubctl command that changes state (claim, images, ready, review), pull. Push right after it. Both accounts write `status/form.json` and `status/aab.json`, A for claims and rework, B for review and ship. Keep that window short.
- If sync.sh refuses (conflict markers): for a file you do not own, take upstream (`git checkout --theirs <file>`). For your own page, keep yours. Then rerun sync.sh. Log anything unusual in your proposals file (A) or LESSONS (B).
- Render images locally before pushing (`ops/render_changed.py HEAD HEAD --pages <slug> --no-commit`). render.json is then current, and the render Action skips the page instead of racing your next push (LESSONS 2026-10-12).

## 5. Rule proposals from A
- A never changes a rule, a checker or the library. If a rule blocks a page wrongly, or a library cell is missing or wrong, A appends one line to **`proposals/account-a.md`**: `YYYY-MM-DD | rule or file | proposal | example page(s) | why`.
- The page stays in its state, or A parks it with the proposal line as the note (`hubctl state <url> parked --note "proposal YYYY-MM-DD #n" --by A-<id>`). A moves on to the next page.
- B reads the file at the start of each day. B applies accepted proposals that need no ruling, with golden cases. Anything needing a ruling goes into Divit's daily approval packet. B marks each line `accepted <SHA>`, `rejected: <why>` or `asked Divit`.

## 6. How A's finished pages reach B's review and ship queue
1. A's definition of done, per page:
   - QC TOTAL 0 (`ship.qc_total`);
   - PAA gate 10/10 with no page-level problems;
   - chip_adds present (L11);
   - no stock or reused names (A1);
   - images rendered with every gate passing, and A has read the contact sheet;
   - `hubctl images <url>` (state `images`), committed through sync.sh.
2. Every page in state `images` in Form/Auto is in B's review queue automatically; there is no hand-off message. B reviews them in batches of up to 4 per page-reviewer (`hubctl review`, severity from rules/SEVERITY.md only).
3. **No blocking finding:** `reviewed`, and B builds ship batches from `reviewed` pages across all 4 hubs. **Blocking:** `rework`, back to A (section 1).
4. Ship (B only): Divit's daily approval packet, then create the CMS items with the 3 newest published Learn refs (L12), pre-flight, staging, Divit's publish, then verify, relink and live audit.
5. A logs its token use per page: `hubctl usage-log <url> <tokens> --role writer --agent A-w-<n>`, committed with the page (`status/usage.jsonl`, append only). B does the same for review and ship.
