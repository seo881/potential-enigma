# Two Claude Code accounts on one Mac (Divit, 2026-10-13)

> **TEMPORARY HANDOVER (Divit, 2026-10-26): A is coordinator and the only shipper for all 4 hubs today; B makes no writes to this repo or the hub collections. Handback to B on 2026-10-27 after B's weekly reset, via reports/2026-10-26/handback-to-B.md.** No Webflow MCP or Designer work; CMS writes through the API script only.

> **Ruling 22 (Divit, 2026-10-14 night): B is the coordinator and the only Webflow writer.** It overrides the A-side list in ruling 20 below. A makes no Webflow calls until a new ruling. The live audit and the publish watch run in `~/emergent-hubs-a` on `~/.claude`. Handover state: `docs/COORDINATOR_HANDOFF.md`.

> **Ruling 20 (Divit, 2026-10-14): rebalance to B.** This overrides ruling 9 and the review split in section 1 below.
> - **B (`~/emergent-hubs-a`) writes all 4 hubs, LP included:** `.hub` = `B:LP,Form,Auto,SurveyQuiz`.
> - **B does every full and slim review** with B-r and B-s agents. A reviewer never reviews a page any part of which it wrote; hubctl refuses a match against the recorded writers.
> - **A (`~/emergent-hubs`, `.hub` = `A:none`) keeps:**
>   - Webflow and all shipping (`hubctl api-*`, ruling 19);
>   - tooling, rules and QC;
>   - the quiz template;
>   - all AlsoAsked and Semrush pulls, and re-ranks;
>   - the advisor flag list and the daily report.
>   - A spot-checks reviews only when B's blocking rate goes over 20% on a day.
> - **Overnight:** B runs ops/schedule/overnight_run_b.sh, following plan/overnight-run-b.md.

Target: 500 pages live by 2026-10-27. Two accounts work in parallel, each in its own clone of this repo. CLAUDE.md, DECISIONS.md, RUNBOOK.md, HUB_RULES and LESSONS.md apply to both; this file only splits the work.

> **Ruling 9 (Divit, 2026-10-13):** SurveyQuiz writing moved from A to B. A writes LP only; every review stays with A.
>
> **Naming (Divit, 2026-10-13, ruling 0):** **Account A = the coordinator** (`~/emergent-hubs`). **Account B = the writer** (`~/emergent-hubs-a`). Agent-id prefixes follow the account: coordinator agents use `A-`, writer agents use `B-`.
> Before this ruling the letters were the other way round, from about 08:00 to 11:30 UTC on 2026-10-13. Those ids stay in history as written:
> - `A-w-<n>`, `writer-a-*` and `proposals/account-a.md` were the **writer**;
> - `B-w-b3-*` and `B-coord` were the **coordinator**.
>
> Holds and ownership are checked by clone (the `.hub` file), not by the letter in an id.

## 1. Who owns what

| | Account A (coordinator) | Account B (writer) |
|---|---|---|
| Clone, `.hub` | `~/emergent-hubs`, `.hub` = `A:LP` | `~/emergent-hubs-a`, `.hub` = `B:Form,Auto,SurveyQuiz` |
| Hubs it writes | LP | Form, Auto, SurveyQuiz (ruling 9, 2026-10-13) |
| Stages | write and rework (LP); **every review** (B's pages included, SurveyQuiz too), full and slim; images check; create, stage, item publish, verify, relink, live audit, retro; rules and tooling; rescue marking; the daily approval packet | write, rework and re-render images (Form, Auto, SurveyQuiz), in this order: rework pages first, then queued pages, then parked pages A has released for rescue |
| Webflow | the **only** Webflow writer (every call per CLAUDE.md) | **none**: no Webflow MCP, every Webflow tool denied |
| Schedulers (launchd, publish watcher, live audit, weekend loop) | A only | none |
| May edit | everything, per CLAUDE.md | only `specs/form/`, `specs/aab/`, `specs/sqb/`, `images/form/`, `images/aab/`, `images/sqb/`, `status/form.json`, `status/aab.json`, `status/sqb.json`, `status/usage.jsonl` (append only), `proposals/account-b.md` |
| Never edits | a page B holds | `rules/`, `qc/`, `ops/`, `pipeline/`, `tests/`, `config/`, templates, `DECISIONS.md`, `LESSONS.md`, `RUNBOOK.md`, `CLAUDE.md`, `status/ship/`, `plan/`, other hubs' files |

Who holds a page:
- **B holds** a Form/Auto/SurveyQuiz page in `claimed` and `rework`. **A holds** it from `images` onward (`images` → review → `reviewed`/`rework` → `approved` → CMS → `published`).
- **Hold markers decide.** Before working any page it did not just claim (a rework, a rescue, a ship batch, a rule re-run fix), an account runs `hubctl hold <url> --by <ID> --note "<why>"` and pushes the status file; only then does it start.
  - The hold records the clone's account.
  - hubctl refuses state changes, `images`, `release` and `claim` from the other clone while the hold stands.
  - Run `hubctl unhold <url> --by <ID>` when the page leaves your hands.
- **Collisions (ruling 6):** a ship batch file takes only pages in state `reviewed`, and nothing is claimed or batched over a hold. A puts its holds (`A-coord`) on every page of a batch when the batch file is pushed.
- `rework` goes back to B, which fixes the blocking findings only, re-renders, then runs `hubctl ready <url> --by B-w-<n>` → `reviewed`. Each page gets one review and one rework (CLAUDE.md step 5). The writer and the reviewer are always different agents; hubctl refuses otherwise.

## 2. One-time setup of B's clone (Divit or B)
1. Start from a clean tree: `git status` in `~/emergent-hubs-a` must show nothing modified.
2. `.hub` = `B:Form,Auto,SurveyQuiz` (git-ignored). A's clone has `A:LP` (ruling 9). `hubctl claim` refuses other hubs; holds and `--by` prefixes are checked against the clone's letter.
3. No Webflow:
   - in `~/emergent-hubs-a/.claude/settings.local.json`, add `"deny": ["mcp__webflow", "mcp__claude_ai_Webflow"]`;
   - do not connect the Webflow MCP in that account.
4. AlsoAsked is shared with A, so the credit caps hold across both clones:
   - `private/alsoasked` in B's clone is a symlink to A's;
   - the `alsoasked` lock is machine-wide (`~/.emergent-hubs/locks/`);
   - pull only through `weekend.py aa`.
   - Writers never read `private/`: `hubctl brief <url>` prints the gated AlsoAsked candidates.
5. `bash ops/setup.sh` in B's clone (B renders images locally).
6. Pages added outside the workbook (ruling 13 new keywords, 2026-10-14) reach B's clone through the tracked `plan/additions.json` (url, hub, primary, status, wave, queue_rank; no Semrush data): `hubctl` merges it into B's own `plan/keyword_map.json` (`plan/kmap_load.py`), so `hubctl claim` hands them out after a plain `git pull`.
   - Their secondaries come from `private/semrush/plan-additions-*.json` and their Semrush questions from `private/semrush/questions/derived/`: Divit's local rsync. Without it `hubctl brief` prints a PLAN DATA line and `skeleton.py build` refuses most of them (under 10 FAQ slots).

## 3. Claim protocol and ids
1. `git pull --rebase` **immediately before** every claim.
2. Claim only in your own hubs:
   - B: `hubctl claim Form|Auto|SurveyQuiz N --by B-w-<n>`;
   - A: `hubctl claim LP N --by A-w-<n>`.
   - At most 25 per claim.
3. Commit and push the status file at once (`bash ops/sync.sh "claim: <hub> N (B)" status/form.json`). A claim is not valid until it is on origin.
4. Rework pages are not claimed; B puts a hold on each before working it. Parked pages are claimable only after A releases them. B never releases a parked page itself.
5. **`--by` on every claim and state change** (claim, state, images, ready, review, release, hold, unhold); hubctl refuses without it.
   - A, the coordinator, uses `A-w-<n>` (LP writers), `A-r-<n>` (reviewers), `A-s-<n>` (slim reviewers) and `A-coord`.
   - B, the writer, uses `B-w-<n>`.
   - An id whose letter does not match the clone is refused.

## 3b. Gate, sources and the review rule (Divit 2026-10-13)
- **Gate (ruling 4):** a page passes with **0 rejects**.
  - Flags are allowed only when every flagged question is in Divit's daily packet.
  - **Never reword a verbatim AlsoAsked question to clear a flag.** A fixes the PA6 patterns instead.
- **F2:** pages with a legacy DataForSEO capture accept the source `alsoasked` when the page has an AlsoAsked pull. Use true labels.
- **PA12 (ruling 5):** a page's secondaries are its Semrush workbook secondaries. A page with **none** uses the workbook's keyword ideas for the page as its secondaries: at least 4, on-topic. Never DataForSEO keyword ideas, and never padding.
- **Review rule (ruling 1):** a page ships only if its current text was reviewed.
  - The review stores a hash of the reviewable text fields.
  - If text changed after review, beyond mechanical autofixes (H3 commas, J1), the changed fields need a **slim review** by an A reviewer who did not write them.
  - `hubctl ship` refuses a page whose hash does not match.
- **Rule re-run (ruling 8):** `hubctl recheck` runs only on pages not held by B. It runs on B's pages at the end of B's wave, coordinated through holds. It never changes a held page's state.

## 3c. Ruling 10 (Divit 2026-10-13): speed without lowering the bar
- **Feasibility before writing.** After the page's one pull, run `hubctl feasibility <url>`. Under 10, do not write: `hubctl defer <url> --by B-w-<n>` sends it back to the queue (not parked). `hubctl claim` skips infeasible pages that already have a pull.
- **Review lock.** After review, change only the fields named in a blocking finding. `hubctl ready` and `ops/sync.sh` refuse anything else. Mechanical H3/J1 fixes are exempt; a same-day factual fix needs the coordinator's `hubctl unlock`.
- **Weekly rule window.** New rule ideas go to `proposals/account-b.md` or `plan/backlog.md`. Rules land once a week, on Mondays, in one combined pass plus a recheck. Factual errors are still fixed the same day.
- **Daily ship.** A ships every `reviewed`, unheld, hash-matching page each day (`hubctl daily-batch`).
- **Headless loop.** B may run a writer loop in its own clone with 6–8 writer subagents. Divit starts it, and it refuses to start unless `weekend.py preflight` passes.
- **Read-only checks.** `hubctl qc` and `hubctl paa` no longer write anything. Stamp `qc_passed` with `hubctl qc <url> --stamp` (or `state qc_pass`); `--log` writes the PAA summary.
- **Pilot hold.** No new Auto pages for B until the AlsoAsked yield pilot lands. (Lifted by ruling 12: Auto pages are claimed from the ranked queue.)

## 3d. Ruling 12 (Divit 2026-10-13): synonyms, pulls, ranked queue, split write
- **AlsoAsked: A only.** A runs every pull (`ops/pull_wave.py`, `weekend.py aa`); B never pulls (aa refuses outside A) and reads saved pulls through `hubctl brief`. B asks A for a pull in `proposals/account-b.md`.
- **Claim from the top only.** `plan/queue-ranked.txt` ranks every queued page: `ready` (10 or more now), `syn-pending` (10 with its tranche's top 2 phrases, awaiting Divit), `no-pull`, `short`. `hubctl claim` takes the first unclaimed ready or syn-pending rows of the hub, in order. A regenerates it after every pull wave and every synonym approval.
- **Split write.** A syn-pending claim carries `faq_pending`. B writes everything but the FAQ (plan, copy, table, image brief) and stops in state `spec`. hubctl refuses qc_pass, images and reviewed until Divit decides. On approval, A clears `faq_pending` and B writes the FAQ from `hubctl brief` (the approved phrases now pass the gate), then QC, gate, images and review as usual. If he rejects every phrase, the page goes back to the queue end with its draft kept.
- **Synonyms.** Approved phrases are in `rules/paa_synonyms.json`; questions Divit struck are on the page's PA4 skip list (by hash). Use admitted questions verbatim, like every AlsoAsked question; a question that drifts from the page's intent is a blocking review finding.
- **Verbatim check.** Every reviewer runs `hubctl verbatim <url>`: each AlsoAsked-sourced FAQ item must equal its prov.original (or, ruling 14, its US-spelling display: `qc/spelling.py display`), and the original must be in the saved pull.
- **Claims go through `hubctl claim` only** (ruling 12 addendum): it takes ready rows, then syn-pending split writes; `hubctl state … claimed` refuses a queued page.
- **Released parked pages.** Parked Form/Auto/SurveyQuiz pages whose feasibility reaches 10 are released to B by A, and then rank like any other queued page.

## 3e. Rulings 16 and 17 (Divit 2026-10-13): daily cadence; A alone overnight
- **B is stopped** (from 2026-10-13 evening). A runs alone overnight on the ruling-15 pipeline, in all 4 hubs, through a temporary `.hub` override recorded in plan/overnight-run.md. A never touches a page B holds. Writers are A-w-<n>; reviewers are A-r-<n> who wrote none of the page.
- **Headless overnight loop:** `ops/schedule/overnight_run.sh` with `CLAUDE_CONFIG_DIR=~/.claude-b` (account A's config dir; ~/.claude is B's). No Webflow tools, and nothing ships overnight.
- **Daily from 10-14:**
  - 10:00 report + packet; 12:00 Divit's answers; 14:00 create items; 16:00 item publish, verify-live, audit, relink; 18:00 daily line.
  - Item publishes have a standing go for pages that are reviewed, hash-matching, at 0 rejects and pre-flight passing (never a site publish). Flagged pages wait for the packet tick. A page failing verify-live is unpublished at once.

## 4. Commit protocol
- Always use `bash ops/sync.sh "<message>" <explicit paths>`, naming only the files you changed. It commits exactly those paths (`git add -- <paths>`, `git commit --only -- <paths>`, diffstat printed first), refuses conflict markers and review-lock violations in them, then fetches, rebases (autostash) only if origin moved, and pushes. Many agents share one clone and one index: anything else staged or modified stays out of your commit (Divit 2026-10-15, after d5109889 swept another agent's half-done tests/golden/run.py). Never `git add -A`, never `git commit -a`, never force-push, never `git reset --hard`.
- sync.sh refuses: no paths, `.`, globs, absolute paths, `..`, `private/`, `.cache/`, and any directory except `images/<hub>/<slug>` and `audits/live/<date>`. Shared files (`status/<hub>.json`, `status/usage.jsonl`, `reports/INDEX.md`, `tests/golden/cases.jsonl`) are committable, but the whole file goes in: pass only the shared files you changed, right after you change them. Test: `bash tests/test_sync.sh` (temp repos with a local bare origin).
- **One page = one commit**, as soon as it reaches its stage: `specs/<hub>/<slug>.json`, `images/<hub>/<slug>/` and `status/<hub>.json`.
- Before any hubctl command that changes state, pull; push right after it. Both accounts write `status/form.json`, `status/aab.json` and `status/sqb.json`: B for claims, holds and rework; A for review and ship.
- If sync.sh warns that the autostash pop conflicted, your commit is already pushed and clean; the conflicted files belong to other sessions (their changes stay in `git stash list`).
- If sync.sh refuses (conflict markers): for a file you do not own, take upstream. For your own page, keep yours. Then rerun sync.sh.
- Render images locally before pushing (`ops/render_changed.py HEAD HEAD --pages <slug> --no-commit`), and render last, after the final brief change.

## 5. Rule proposals from B
- B never changes a rule, a checker or the library. It appends one line to **`proposals/account-b.md`**: `YYYY-MM-DD | rule or file | proposal | example page(s) | why`. B either leaves the page in its state or parks it with the proposal as the note (`hubctl state <url> parked --note "proposal YYYY-MM-DD #n" --by B-w-<n>`).
- A reads the file at the start of each day and marks each line `accepted <SHA>`, `rejected: <why>` or `asked Divit`. Anything needing a ruling goes into Divit's daily approval packet.

## 6. How B's finished pages reach A's review and ship queue
1. B's definition of done, per page:
   - QC TOTAL 0;
   - PAA gate with 0 rejects and no page-level problems, and every flag noted in the commit;
   - chip_adds (L11);
   - no stock or reused names (A1);
   - images rendered with every gate passing, and the contact sheet read;
   - `hubctl images <url> --by B-w-<n>` (state `images`), committed, and the hold removed.
2. Pages in state `images` (Form, Auto, SurveyQuiz) are A's full-review queue. Reworked pages that come back through `hubctl ready` get A's slim review when their text changed after review (section 3b).
3. **No blocking finding:** `reviewed`, and A builds ship batches only from `reviewed` pages. **Blocking:** `rework`, back to B.
4. Ship (A only):
   - Divit's daily approval packet;
   - CMS items with the 3 Learn refs (L12, `config/learn_refs.json`), then pre-flight;
   - staging (unhide for staging only, re-hide right after the checks, no production publish while anything is unhidden);
   - Divit's production go, then verify, relink and live audit.
5. Token log per page: `hubctl usage-log <url> <tokens> --role writer --agent B-w-<n>` (B). A does the same for review and ship.

## 2026-10-21 split (Divit, 2026-10-21; this section wins over older ones)
| Account | Clone | Writes and reviews | Webflow | Rules, templates, code |
|---|---|---|---|---|
| A | ~/emergent-hubs (CLAUDE_CONFIG_DIR=~/.claude-b) | Form, SurveyQuiz | none | none; proposals to plan/proposals-from-A.md |
| B | ~/emergent-hubs-a | LP, Automation | ships everything (A's pages too), live QC | owns them; coordination |
- Reviewer independence holds across accounts: no reviewer reviews a page any part of which it wrote (writer ids carry the account letter: A-w-*, B-w-*).
- A marks a page ready for B to ship by moving it to `reviewed` (0 blocking, 0 flags, QC 0) and pushing; B's ship loop picks it up after ship-check.
- Holds (`hubctl hold`) before work, as before. A's week ends Saturday (heavy writing); B's runs to Tuesday.

## 2026-10-23: Account A paused (Divit)
Account A (~/emergent-hubs) is paused until further notice. Account B (this clone) writes, reviews and ships all 4 hubs: LP, Automation, Form, SurveyQuiz. Pages A reviewed with 0 flags are shipped by B. Pages A claimed or left mid-write stay claimed by A; B does not touch them and claims new pages from the top of the queue across all 4 hubs. Reviewer independence holds across accounts.

## READ FIRST (both accounts): slug rule, 2026-10-23
Before writing or claiming anything, read the PERMANENT SLUG RULE in CLAUDE.md (it loads automatically) and DECISIONS 2026-10-23. Account A's resume prompt adds this line: "Before writing, run the slug check on your claimed pages: `.venv/bin/python3 ops/hubctl.py slug-check <HUB>`; fix the slug or H1 per the rule before any prose."
