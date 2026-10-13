# Batch 3 staging: links FAILED, 11 sections re-hidden and read back; batch 3 pages pass; ruling 14 and claim fixes

## Digest for Divit
- **Staging check FAILED, on one point.** On every child template and every hub, the carousel card links and the Learn card links render as the literal href `detail_ai-<hub>-builder` or `detail_learn`, which resolve to `/<hub>/detail_…` and return 404.
  - The `collectionPage` link setting written on 10-12 and 10-13 reads back "as set" but publishes as a slug.
  - The hub's own Learn list (the Blog component) links correctly. Its link setting is the shape to copy; the read was rate-limited.
- **Per your amendment, all 11 sections were re-hidden at once and read back `false` on all 11.** The Survey template's Learn section stays visible as always; it was never one of the 11. Nothing was published by Claude.
- **Everything else passes on all 60 pages (40 live + 20 batch 3):**
  - HTTP 200, H1, title, meta description, canonical and share image (WebP 1200x630);
  - 10 FAQ items; chips prefill and switch; first tab active; 4 use-case images; comparison table; hub link; no link to a page that isn't live;
  - Learn: 3 cards on all 60;
  - carousel: every card title sits inside its card at 1440 and 390 px, and every cover has alt text;
  - hub cards: the CRM cover is "Halberd Co" (v6b) and the Schedule cover is "Thursday, Oct 15" (v6b) on all 128 page loads;
  - FAQ 1 is not clipped on any child page at either width;
  - no horizontal overflow; no console errors.
- **Hubs: FAQ 1 is clipped by 24 px** on the Form and Automation hubs at 1440 px (sometimes at 390 px). The same clip exists on production, so this publish didn't cause it. The refit script only runs on child templates, not hub pages, so it's outside scope until you say so.
- **Ruling 14 is in** (one variant list feeds H2, PA3 and the K checks; verbatim allows the US-spelling display only).
  - A read-only QC scan of 110 passed pages shows 0 new failures from it.
  - 2 pages fail on an unrelated dead source: the FTC CAN-SPAM guide now returns 404 (coming-soon-page in batch 3, and live ecommerce-automation). It's a source link inside the spec; the rendered page doesn't change.
- **Item 4:** `hubctl claim` takes syn-pending rows, and `hubctl state … claimed` now refuses queued pages. Metrics count sales-workflow's writer run once (154,868 tokens).
- **Knock-on:** employee-handbook-acknowledgment-form is 9/10 now. Its UK-spelled secondaries used to count as separate keywords.

## Request
> staging published (webflow.io only, just now). 1. Run the batch 3 staging checks on all 60 pages and 4 hubs, including Learn on all 4 templates and the carousel (links, title inside the card at 1440 and 390 px, cover alt, live pages only). Then re-hide all 11 sections, read the hide back, and report before anything else. 2. If every check passes, ask me in one message for two goes: (a) production publish of batch 3, and (b) Learn + carousel to production. If I give both, unhide (staged), read back, then tell me to publish production once. If I give only (a), I publish with the sections hidden. 3. Ruling 14 (spelling variants): treat "acknowledgement" as a spelling variant of "acknowledgment" for PA3 matching, and normalise the display text of any verbatim AlsoAsked question to US spelling, keeping the original in provenance (same as the 2026-10-09 T-shirt ruling). This is a spelling normalisation, not a reword; ruling 4 still forbids rewording a verbatim question. Build it as a general variant list in rules/us_spelling.json with golden cases, so H2 and PA3 agree. Answer B's proposal with this. 4. hubctl claim: accept pages in class syn-pending in plan/queue-ranked.txt (split-write), so B claims through claim, not hubctl state. Count sales-workflow's tokens once in metrics. Report per CLAUDE.md, under 15 lines in chat.
>
> Amendment: if EVERY check passes (batch 3, Learn on all 4 templates, carousel on 4 templates and 4 hubs), do not re-hide; ask me for both goes in one message and wait. If I give both, I publish production with them visible. If any single check fails, or I give only the batch 3 go, re-hide all 11 at once, read back, and I publish with them hidden. / The amendment overrides step 1's re-hide: if every check passes, leave the sections visible and ask me for both goes; if any check fails, re-hide at once and read back.

## Actions and results
1. **Staging checks on https://emergent-sh.webflow.io:**
   - `node ops/verify_launch.mjs ops/out/launch-batch-3/staging-manifest.json --base …` across 60 pages and 4 hubs. Its only failures are the two launch-state expectations from earlier batches (carousel hidden, Learn hidden), which this publish reversed on purpose, plus the hubs' "missing cards", which is the link failure.
   - Playwright at 1440 and 390 px: carousel title inside card, cover alt, Learn card count, hub-card cover assets, FAQ 1 clip, overflow (128 page loads).
   - Every card href resolved and fetched: all 404 on the child templates and hubs.
2. **Re-hide:** 11 set_visibility false calls, then read-back queries. Three read-backs hit 429 and were retried after a wait; all 11 read false. Logged in logs/templates.md (efccb2c7).
3. **Ruling 14:**
   - `qc/spelling.py` uses `rules/us_spelling.json` `map` (it already held acknowledgement → acknowledgment) for:
     - H2, unchanged;
     - PA3, through `paa_gate.norm`; question hashes use `norm0`, so they stay stable;
     - the K checks, through `qc_hub.kwmap`;
     - `hubctl verbatim`, which accepts the original or `display(original)` (US spelling plus keyword house forms such as T-shirt) and checks the original is in the pull.
   - 8 golden cases r14-*.
   - B's two asks were answered in proposals: (1) done by the shared list; (2) declined in favour of display normalisation, per your ruling.
4. **Item 4:** claim already reads plan/queue-ranked.txt (ready, then syn-pending). `hubctl state … claimed` refuses a queued page. `guards.usage_rows()` drops 0-token rows and a "corrects" row that repeats an earlier identical row, and is used by metrics, ship cost, the weekend and retro.
5. **Recovery:** a `git stash` with nothing to stash, followed by a pop, applied a stale autostash. The 33 paths were restored to HEAD one by one; nothing was lost; LESSONS line added.

## Numbers
- Pages checked: 60, plus 4 hubs and 4 templates. Page-level content failures: 0. Link failures: every carousel and Learn card on the templates and hubs.
- Sections re-hidden: 11/11, read back 11/11.
- Golden suite: 345 cases, 0 regressions. QC scan: 110 pages, 0 new failures from ruling 14, 2 dead-source P1s.
- Pull wave (running): 98 pulls, 70 credits at 13:50 UTC.

## Decisions
- Divit's staging amendment (DECISIONS 2026-10-13).
- Ruling 14 and the claim/metrics change (DECISIONS 2026-10-13).
- The scope rule (memory, DECISIONS): hub-page FAQ is outside the child templates.

## Files changed and commits
- efccb2c7: staging failure and re-hide log.
- 116b243e: ruling 14, claim and metrics, golden, DECISIONS, TWO_ACCOUNTS, LESSONS, answer to B.
- This report: see INDEX.

## Webflow calls
- **Reads:**
  - section visibility on 8 pages (before: true on all 11);
  - read-only diagnosis: the Form hub's build_link setting `{mode collectionPage, to {pageSlug detail_ai-form-builder}}` and the Blog component's links.
- **Writes:** set_visibility false on the 11 sections (IDs in logs/templates.md). Rollback: set_visibility true on the same IDs, only on your go.
- **Publishes:** none by Claude.

## Not done
- Asking for both goes: the checks did not all pass.
- The link fix needs your go: copy the Blog component's working card-link shape onto the 8 carousel links and 4 Learn links, staged, then a new staging cycle.
- FTC source replacement on 4 specs (coming-soon-page, ecommerce-automation, squeeze-page, lead-capture-form): next, through a source lookup.

## Open questions for Divit
1. **Batch 3 to production with the sections hidden?** The 20 pages pass every page check; the sections are hidden in the Designer, so a production publish ships them hidden.
2. **The link fix:** may I read the working Blog component's link setting and write that shape onto the 12 broken card links (staged), then ask you for another staging publish?
3. **Hub FAQ 1 clip** (24 px, already on production, hub pages): should I prepare a fix, or leave it out of scope?
