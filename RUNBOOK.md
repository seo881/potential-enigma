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

## 2. The production pipeline (content-first, staged; target 200 pages/day)

Every stage runs in bulk and in parallel. A page moves through states in `status/<dir>.json`:

| Stage | Who | What | Exit state |
|---|---|---|---|
| 1. Claim | Orchestrator | `hubctl claim <HUB> 25 --by <id>` per hub in today's plan; commit and push status | claimed |
| 1b. Live SERP | Writer (or orchestrator in bulk) | DataForSEO Google organic SERP for the primary (United States, English, PAA click depth 2), saved with `hubctl serp-save <url> <raw.json>`; `hubctl serp-status` lists pages still missing it | claimed |
| 2. Write | **Writer** (one page per writer, fresh context) | Brief (now with PAA and related searches) → spec (all fields, FAQ sourced from PAA with `faq_sources`) → `hubctl qc` until TOTAL = 0. While images are on hold, no `image_brief` | qc_pass |
| 3. Review | **Reviewer** (independent; never its own pages) | Code QC re-run + judgment pass (hub-qc skill) against the brief | reviewed or rework |
| 4. Images (ON HOLD: brand palette pending) | Orchestrator (any machine) | `hubctl images-batch reviewed`: the image engine renders every reviewed page's brief (6 images, gates, one contact sheet per page); a brief that fails goes back to `rework` | images |
| 5. Divit's review | Divit | Daily review page. First batch per hub (calibration): every page in full. Then: a random 10% of the day plus everything flagged. Rejections become rule fixes, re-run on all pending pages | approved |
| 6. Create drafts | Orchestrator | Commit + push, `hubctl bulk-payload <HUB> --sha <sha>` → `data_cms_tool` (100 drafts per call), read back to disk, `hubctl bulk-verify` | cms_draft |
| 7. Publish | Orchestrator, on Divit's go | `hubctl publish-payload <HUB>` (100 per call) | published |

Quality is layered so volume never lowers it: code QC (zero tolerance), an independent reviewer per page, pre-approved image recipes with code gates, and Divit's calibration plus sampling. A defect Divit finds becomes a QC rule or a `HUB_RULES.md` line (ratchet), then QC re-runs on every page not yet published.

### Mode A (recommended): Claude Code
One orchestrator session in the repo (`CLAUDE.md` loads automatically) spawns `page-writer` and `page-reviewer` subagents (`.claude/agents/`), each in its own context, many in parallel. Setup once: clone the repo, put the Semrush workbook at `private/Emergent_Hub_Child_Pages_Final_v3.xlsx`, connect the Webflow MCP server (`claude mcp add`, then authorise), run `bash ops/setup.sh`. Skills load from `.claude/skills/`. Git uses Divit's own credentials. The image engine runs on macOS and Linux alike (`ops/setup.sh` installs it; output SVGs are byte-identical on both).

### Mode B (works today): Claude.ai Project chats
Same stages, more chats: about 8 writer chats a day (2 per hub, 25 pages each, two rounds), 2 reviewer chats, 1 image-and-publish chat, 1 coordinator. Start each with its prompt in `KICKOFF.md`. A writer chat writes copy only (no images, no Webflow read-backs), so 25 pages fit in one chat.

### Ownership (both modes)
| Role | Writes | Never touches |
|---|---|---|
| Orchestrator / coordinator | `qc/`, `ops/`, `plan/`, `rules/`, `config/`, `.claude/`, `pipeline/`, `docs/`, `DECISIONS.md`, `RUNBOOK.md`, `SETUP_STATUS.md`; Webflow creates and publishes | Page copy it did not write (other than reviewer-approved fixes) |
| Writer | `specs/<dir>/<its pages>`, `status/<dir>.json` (its pages), `logs/<dir>.md` | Webflow, shared code, rules, other pages |
| Reviewer | State and notes of the pages it reviews; small certain fixes | Webflow, pages it wrote |
| Image stage | `images/<dir>/`, image fields of specs, manifest | Copy fields |

Repo dirs: LP `lp`, Form `form`, Auto `aab`, SurveyQuiz `sqb`. Writers in the same hub claim disjoint pages, and every push rebases first, so parallel work does not collide.

## 3. Throughput (daily plan for 200 pages)
- Claim 50 per hub per day (Form can take more as smaller hubs finish).
- Writers: about 200 specs. Reviewers: about 200. Images: about 1,200 renders, all from briefs.
- Drafts: 2 create calls per hub (100 each). Publish: same.
- Divit: about 1 hour (calibration days: more).
- Dependencies that cap the rate: plan usage limits for the model; Divit's daily review; the Wave 3 top-10 pull before queue rank 208.

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
Before the context runs long (a writer chat: about 25 pages; a coordinator: when replies slow down), stop at a clean state:
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
| `.claude/skills/`, `.claude/agents/`, `CLAUDE.md` | The two skills (also packaged for Claude.ai), writer and reviewer subagents, Claude Code context |
| `docs/IMAGE_BRIEF.md`, `pipeline/engine.py`, `pipeline/engine_blocks.py`, `pipeline/briefs/` | Image brief guide; the image engine (11 recipes, 44 blocks, covers, share images); 4 worked briefs that rebuild the 16 approved scenes |
| `MORE_THINGS.md`, `childedits/`, `audit/`, `tables/`, `schema/` | History of earlier sessions |
