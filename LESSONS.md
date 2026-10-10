# LESSONS.md: how this programme fails, and the rules that stop it repeating

Read this at the start of every session (CLAUDE.md points here). Every incident adds a row to the log at the bottom AND an automated check; a lesson without a check is not done.

## 1. The six failures that cost 2026-10-07 to 2026-10-09

| # | What happened | Root cause | Rule now |
|---|---|---|---|
| 1 | 170 pages written overnight; then every FAQ needed re-gating, ~170 pages reworked | Scaled before one page had gone end to end (write, review, Webflow, live). The FAQ data source (DataForSEO PAA) was never validated before 170 pages were built on it | **Canary rule:** a new hub, template, data source or rule set ships 3 pages to staging and passes verify_launch before more than 10 pages are written. **Source rule:** any data source is validated on 5 real samples (human-read) before it feeds a writer |
| 2 | New rules landed after pages were written (hub link, serial comma, PA3, A6 ...) and each one re-QC'd every page | Rules were discovered in review instead of in the canary | Rules freeze per batch (DECISIONS 2026-10-08). New rules go to `plan/backlog.md` and are applied between batches, in one combined pass |
| 3 | F4 and the PAA gate demanded opposite things; 6 pages blocked | A replaced rule was kept "until later" | **Supersede now:** a rule that replaces another retires it in the same commit. The rule registry (`rules/registry.json`) records `supersedes`; QC refuses to run two rules marked as conflicting |
| 4 | Plan priced at 17.1M tokens from one 89k review measurement; real review cost 45k a page | Planned from a single data point | **Measure on a pilot of 4** before pricing a batch. Writer about 113k and review about 45k a page are the current measured costs (2026-10-09) |
| 5 | Sessions crashed (safety check), stale context, keys pasted into chats | Long sessions; a prompt asked the model to write out its own reasoning; secrets typed into terminals | Fresh session (`/clear`) per task; reports carry outcomes and sources, never "explain your reasoning"; keys live in the macOS keychain only |
| 6 | Steps marked "Designer-only" were already done or doable by API (T3, T6, T11); the hubs were assumed to be drafts; placeholder testimonials were assumed fake | Plans written from memory instead of the live state | **Read live state before planning any manual step or flagging anything.** Unverified claims are labelled UNVERIFIED. Check DECISIONS.md before raising an issue Divit already settled |

## 2. Operating rules (in addition to CLAUDE.md and DECISIONS.md)

1. **End to end before breadth.** No batch starts until its first page is verified on staging.
2. **One pass per page.** Code applies every deterministic fix; one writer pass; one QC; one review; one rework. Never several sweeps over the same pages.
3. **Gates are tested like code.** Every question, sentence or claim a human rejects becomes a case in `tests/golden/` that the gate must catch. The golden suite runs on every rules change and must stay green.
4. **Default, don't ask.** Reports give a recommended default for every open question. Divit's time goes to the publish decision and the PA13 read, not to choosing between options Claude can rank.
5. **Links ship only to live pages** (link-to-live). The hub link (K4) is always present.
6. **Staging first, always:** webflow.io, then verify_launch, then emergent.sh. Nothing reaches the public that a script has not checked.
7. **Never leave items non-draft without publishing soon:** any full-site publish by anyone takes them live.
8. **API capability table:** `docs/WEBFLOW_API.md` lists what the API can and cannot do (verified). Update it whenever a call proves or disproves a capability. Do not mark a step Designer-only without checking it.
10. **No site publish, ever, by Claude.** Item publishes only; Divit publishes the site from the Designer (DECISIONS 2026-10-10).
9. **Live pages are audited, not trusted.** `docs/LIVE_AUDIT.md` runs after every publish and daily; Divit spot-checks, the audit checks everything.

## 3. The learning loop (runs after every batch)

`hubctl retro <batch>` writes `status/metrics.md` and appends to the log below:
- first-pass QC rate, gate pass rate, review blocking-finding rate, rework rate;
- **human catches vs gate catches** at PA13 (2026-10-09: 5 human catches in 210 questions, about 2.4%): each human catch becomes a golden case and a backlog fix;
- tokens per page (writer, review), wall-clock per page, credits used;
- pages parked and why.
A metric that worsens two batches running is a P1 item for the next batch.

## 4. Image formats (decided 2026-10-09)

| Image | Format | Why |
|---|---|---|
| Use-case images, card covers | **SVG** (keep) | Vector: sharp at any size; Webflow serves SVG unchanged (raster CMS images get downsized and look soft, lesson v2); about 23 KB gzipped |
| Share image (Thumbnail / og:image) | **WebP** (Divit, 2026-10-09; was PNG) | Accepted by Facebook, LinkedIn, X, Slack, Discord, iMessage, WhatsApp. Not AVIF: AVIF previews fail on LinkedIn, Slack, iMessage, X and Discord. Keep at most 300 KB (WhatsApp cap) and 1200x630 |
| Raster images visitors actually load (hub value cards, photos) | **AVIF** | This is where AVIF pays off: real bytes on real page loads |

## 5. Incident log (newest first; one line each: date, what, check added)
- 2026-10-10 · 5 pages logged 4-6 AlsoAsked credits against a 2-per-page cap: the counter summed `credits` and `web_credits` (each pull counted twice), parallel pulls shared before/after balance windows, and sessions could run ops/alsoasked_pull.py directly past `weekend.py aa` · Caps live in the only allowed path; never allow a bypass tool. The pull script refuses direct runs (ALSOASKED_VIA_AA), `aa` counts `credits` only, caps 2 per page in total under a lock, reuses saved pulls; the loop no longer allows the pull script
- 2026-10-10 · The weekend loop idled for hours on render waits for the Action while it fed one hub at a time · Unattended runs must keep all hubs busy; never idle on a single queue or a render wait. `weekend.py next` deals up to 4 units round-robin across hubs (LP, Automation, SurveyQuiz canaries in parallel); images render locally in the background (`weekend.py render`); one bad brief no longer stops the render queue
- 2026-10-10 · The weekend run held every new page for about 12 hours because the DataForSEO MCP was not authenticated, discovered only mid-run · Before any unattended run, preflight every external dependency it needs (logins, tools, credits) and fail at start, not mid-run. DataForSEO retired (DECISIONS 2026-10-10); QC F1 now needs only the AlsoAsked pull (golden f1-*)
- 2026-10-10 · First live-audit fixes (2026-10-09): before-values were saved to disk before each Webflow write but committed only after the writes · `live-fix prepare` now writes the before-value and refuses to write the payload until that file is in HEAD, unchanged and on origin/main (ops/live_audit.py before_committed; docs/LIVE_AUDIT.md step 1)
- 2026-10-10 · QC H3 filed real serial-comma misses as ambiguous P2 (verb series, noun phrases with clauses, 4-item lists), so 41 shipped on 18 live pages; a writer's fix also put a comma between subject and verb · H3 widened with parallel-structure rules and traps (golden h3-gap-* guarded, h3-noflag-1..9); the orchestrator reads every writer payload before sending
- 2026-10-10 · A 40-character explore CTA clipped at 390 px on client-onboarding-questionnaire · QC D3 (explore_cta <= 34 chars, P1) in QC, HUB_RULES and the writer brief
- 2026-10-09 · retro batch-1: 21 shipped, 5 held; first-pass QC 21/25 (84%); review blocking 6/21 (28%); launch-day gate misses (brands, file formats, descriptions) on 20/20 pages · PA14, PA15, D1, D2, F9 and golden cases added (status/metrics.md)
- 2026-10-09: two production publishes (11:38 and 13:14 UTC) happened outside the plan and shipped unverified content · the daily live audit runs at once whenever get_site lastPublished has changed since its last run (ops/schedule/live_audit_daily.sh + prompt)
- 2026-10-09 · Launch review (Divit): FAQ questions naming brands (Google, ChatGPT, Word, ADP...) and asking for file formats (PDF, printable, Word) passed every gate; hero and how-to descriptions too long and metaphorical · gate PA14 (brands, PA8 cap 0) and PA15 (formats), QC D1 (hero <= 130 chars, primary, plain) and D2 (how-to one sentence <= 140 chars); 11 golden cases
- 2026-10-09 · All 20 launch pages 404 on staging: the 4 cloned child templates had "Publish this Collection Template page" OFF (API field shouldPublish false; Designer-only switch in Template settings > Publish settings) · pre-flight must assert shouldPublish true on the hub's template before any publish; new hubs: switch it on when the template is created
- 2026-10-09 · 5 held CMS items (4 originals + contact-form) published by hand from the CMS because "Not Published" looked like an error · unpublished within minutes; live audit Layer A must also assert that no held/draft-state page is live (reads status/ship ledger), and reports flag held items explicitly
- 2026-10-09 · PA13 read caught 5 gate misses (near-duplicate pair, plugin brand, two drift questions, spelling variants) · golden cases to be added (backlog)
- 2026-10-09 · F4 vs PAA gate conflict blocked 6 pages · F4 retired; rule registry with `supersedes` (backlog)
- 2026-10-08 · Report rule wording tripped the safety check, 3 sessions lost · report sections are outcomes and sources only
- 2026-10-08 · 172/183 pages parked by strict PA3 · PA3 widened with a full human read of what it admits
- 2026-10-07 · 170 pages written on unvalidated PAA data · canary rule and source rule
