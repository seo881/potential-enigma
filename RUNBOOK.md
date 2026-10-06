# RUNBOOK: Emergent build-hub child pages

**Start here, in every new chat.** This repo is the only place state lives. A chat that ends mid-task loses nothing if it committed; a new chat reads this file, runs setup, and continues.

## 0. Read in this order (10 minutes)
1. Project file `EMERGENT_BUILD_HUBS_HANDOFF.md`, sections 0 (how to work with Divit) and 2 (access, IDs, GitHub token). The token lives only there.
2. This file.
3. `DECISIONS.md`: every ruling Divit has made. Never re-ask these.
4. `rules/HUB_RULES.md`: how a page is written.
5. `SETUP_STATUS.md`: what is built and what is not yet.
6. Your role's section below, then `logs/<hub>.md` (latest entries) and `python3 ops/hubctl.py status`.
7. For image work: Project file `IMAGE_PIPELINE_KT.md`.

## 1. Setup (every new chat, about 3 minutes)
```bash
git clone https://github.com/seo881/potential-enigma.git /home/claude/pe && cd /home/claude/pe
bash ops/setup.sh        # fonts, Python deps, image pipeline bootstrap, keyword map, QC smoke test
```
Expect `SETUP OK`. The keyword map is rebuilt from the Semrush workbook in the Project (`/mnt/project/Emergent_Hub_Child_Pages_Final_v3.xlsx`). Semrush data never goes into this public repo (`.gitignore` covers `plan/keyword_map.json` and `plan/queue.csv`).

Webflow: first MCP call of the chat uses `session_id: "start"`; reuse the issued ID. Pick one `agent_id` for the whole chat: `<model>|claude-ai|<hub>-<4 chars>`.

Push (never store the token, never force-push):
```bash
T='<token from handoff>'; B=$(printf 'x-access-token:%s' "$T" | base64 -w0)
git pull -q --rebase origin main
git -c user.name="seo881" -c user.email="seo881@users.noreply.github.com" commit -qm "<msg>"
git -c http.extraheader="AUTHORIZATION: basic $B" push -q origin main 2>&1 | sed "s/$T/[token]/g"; unset T B
```
If the push is rejected: `git pull --rebase origin main`, inspect what came in, push again.

## 2. Roles and ownership

| Role | Writes | Never touches |
|---|---|---|
| **Coordinator** (one chat) | `qc/`, `ops/`, `plan/`, `rules/`, `config/`, `skills/`, `pipeline/`, `DECISIONS.md`, `RUNBOOK.md`, `SETUP_STATUS.md`; publishing; cross-hub QC | Page copy for hubs that have a hub chat |
| **Hub chat** (one per hub: LP, Form, Auto, SurveyQuiz) | Its own collection in Webflow; `specs/<dir>/`, `images/<dir>/`, `status/<dir>.json`, `logs/<dir>.md` | Other hubs' files and collections; templates, components, classes, pages, interactions; shared code (ask the coordinator) |

Repo dirs: LP `lp`, Form `form`, Auto `aab`, SurveyQuiz `sqb`. Because each chat writes only its own files, parallel pushes never conflict.

When a small hub finishes its queue, its chat moves to Form by taking a queue range the coordinator assigns in `logs/form.md`.

## 3. The page lifecycle (hub chat)

| # | Step | Command / action | State after |
|---|---|---|---|
| 1 | Claim the next pages (5 by default, max 10) | `python3 ops/hubctl.py claim <HUB> 5 --by <chat-id>`, then commit and push status | claimed |
| 2 | Read the brief | `python3 ops/hubctl.py brief <url>` (Wave 3: get the live top 10 first; apply the cut rules) | |
| 3 | Create the spec | `python3 ops/hubctl.py init <url>`, then write every field per `rules/HUB_RULES.md` | spec |
| 4 | QC until clean | `python3 ops/hubctl.py qc <url>`; fix root causes; TOTAL must be 0 | qc_pass |
| 5 | Images | Write the image spec from the tab copy; build, gate and review at true size (`IMAGE_PIPELINE_KT.md`; recipe library per `SETUP_STATUS.md`) | images |
| 6 | Review | One review page per batch: copy, image contact sheet, QC report. Wait for Divit's go | review → approved |
| 7 | Commit and push | Images and specs; then verify raw URLs at the SHA (`pipeline/build.py verify`) | |
| 8 | Create the CMS item as a draft | `python3 ops/hubctl.py payload <url> --sha <sha>`; pass `ops/out/<slug>.payload.json` as the `actions` of `data_cms_tool` | |
| 9 | Verify and record | Read the item back (see 4.3), `hubctl verify`, then `hubctl record <url> --item-id <id> --file-id <field>=<id> ...`; commit | cms_draft |
| 10 | Publish (coordinator, after Divit's go) | `python3 ops/hubctl.py publish-payload <HUB>` → `data_cms_tool` | published |

Log every step that changes Webflow: `python3 ops/hubctl.py log <HUB> "<what, item ID, rollback>"`.

## 4. Webflow facts (hard-won; do not relearn)
1. **IDs and field slugs** are in `config/collections.json`. Never write a slug that is not there. The child collections are at Webflow's field cap: no new fields.
2. **Drafts only.** Every create or update sends `isDraft: true`. Bulk updates on already-published items go live immediately; touch published items only with Divit's go.
3. **Read-backs are large.** To get one onto disk for `hubctl verify`, read the item together with a large list in the same call (for example `list_collection_items` on the Learn collection `6a0f028d0bfe272031dbddb8`, limit 8); the tool then stores the whole result as a file under `/mnt/user-data/tool_results/`. Never paste read-backs into the conversation.
4. **Rate limit:** a 429 on `/v2/pages` means wait 65 seconds. Hub chats make CMS calls only, about 3 per page, far below the limit.
5. **Images import by URL** pinned to a commit SHA (`raw.githubusercontent.com/seo881/potential-enigma/<sha>/...`). SVGs are served unchanged; rasters get resized, which is why use-case images are SVG.
6. **The FAQ field** is one rich-text embed holding `window.awbFAQ` JSON with escaped quotes. Edit it in code and assert that only the intended spans changed.
7. **Interactions and the page design** only show in Designer Preview or on a published page.

## 5. Quality gates (none optional)
- `qc/qc_hub.py`: TOTAL (P0 + P1) = 0. Frozen live pages report but do not count.
- Image gates (shape, legibility, overlap, contrast, off-canvas, keycap guard, vector integrity, determinism), then a review at true display size.
- Divit's go before any create, and again before publish.

## 6. Ending a chat (always)
Before the context runs long (about 10 pages), stop at a clean state:
1. Commit and push everything (specs, images, status, log).
2. Add a line to `logs/<hub>.md`: what is done, what is in progress and its exact state, the next step.
3. Tell Divit to open a new chat with the kickoff prompt from `KICKOFF.md`.

## 7. Where things are
| Path | What |
|---|---|
| `config/collections.json` | Hub, collection and template IDs; logical field name → CMS slug |
| `plan/build_map.py`, `plan/overrides.json`, `plan/ISSUES.md` | Keyword plan generator, live-page reconciliation, known issues in the workbook |
| `specs/<dir>/<slug>.json` | One spec per page: every field, keywords, images |
| `status/<dir>.json` | Lifecycle state per page (each hub chat owns its own) |
| `logs/<dir>.md` | Append-only hub logs |
| `qc/qc_hub.py`, `rules/claims.json`, `rules/HUB_RULES.md` | QC engine, claims register, writing rules |
| `ops/hubctl.py`, `ops/setup.sh` | Operations CLI, setup |
| `pipeline/`, `images/`, `manifest.json`, `assets.json` | v5 image pipeline and outputs |
| `skills/` | Sources of the two skills (`hub-content`, `hub-qc`) |
| `MORE_THINGS.md`, `childedits/`, `audit/`, `tables/`, `schema/` | History of earlier sessions |
