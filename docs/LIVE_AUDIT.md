# Live audit: every live page checked, every character, issues fixed and documented

Decided by Divit 2026-10-09 (DECISIONS). Divit spot-checks 2-3 URLs; this system checks all of them, fixes what it is allowed to fix, and documents everything with a rollback.

## When it runs
- **Right after every publish** (all newly live URLs), then **daily** on every live child page and the 4 hubs.
- Layer A (deterministic, no LLM) can run unattended as a GitHub Action (`.github/workflows/live-audit.yml`, GITHUB_TOKEN only, no API keys). It writes `audits/live/YYYY-MM-DD/findings.json`.
- Layer B (judgment + fixes) runs in Claude Code with one command: `hubctl live-audit [--since-publish | --all]`.

## What is checked on each live URL (rendered page, after scripts run)
**Layer A, deterministic:**
- **Held pages first (Divit 2026-10-09):** every page held in `status/ship/*.json` is fetched on emergent.sh and on staging; HTTP 200 anywhere is a P0 (A0-held-live): unpublish the item at once (even in a dry run), verify `isDraft` true, and put it at the top of the digest.
- HTTP 200, canonical = self, no `noindex`, in the sitemap; title and meta description present, within pixel and character limits, matching the spec exactly.
- Every spec field rendered exactly once; nothing rendered that is not in the spec (stray template text, "Lorem", "This is some text", empty sections, "No items found").
- Character hygiene on all visible text, alt text, meta and JSON-LD: zero-width and control characters, broken entities (`&amp;amp;`), double spaces, em dashes, curly or straight quote mixing, UK spellings, repeated words, unclosed brackets.
- Links: every internal link 200 and live; hub link present exactly once; no link to a non-live page; external source links 200 (weekly).
- Images: load 200; correct format (SVG for use-case and covers, WebP og:image); og:image 1200x630 at most 300 KB; non-empty alt; use-case images exactly 3:2.
- Scripts: hero prompt prefilled, chips switch it, FAQ rendered with 10 items, first tab active, carousel covers present.
- JSON-LD parses; FAQ items in schema match the visible FAQ word for word.
- Console (A9-console, P1): 0 error-level console messages and page errors in Chromium. Only Divit's named exception is ignored (rules/live_audit.json `console_ignore_sources`, applied by `ops/console_filter.py`, shared with `ops/staging_check.py`); every run prints the exceptions in force and each error they ignored. See "Console-error exception" below.
- Screenshots at 1440 and 390 px saved to `.cache/live/` for Layer B.
- **Drift:** live text differs from the spec and the change is not in our logs = a human edited it in Webflow. Report it; never overwrite it automatically.

**Layer B, judgment (reviewer agent per 4 pages):** reads the full rendered text and the screenshots against HUB_RULES, the claims ledger, DECISIONS and LESSONS: wrong or unsourced claims, stale figures, off-topic or junk FAQ, grammar, tone, audience narrowing, broken sentences where template and CMS text meet, layout breaks on mobile.

## Severity and what may be auto-fixed
| Severity | Examples | Action |
|---|---|---|
| P0 | False or unsourced claim, legal/medical risk, broken page, wrong page content, 404 link | Fix immediately. If not fixable in one pass: unpublish the item (rollback file) and report at the top of the digest |
| P1 | Rule violation (QC/HUB_RULES), typo, grammar, junk FAQ item, bad alt, stray characters, link to a non-live page | Fix in the same run |
| P2 | Style preference, improvement idea | Backlog only, no change |

**Allowed automatically (child CMS items only):** text fields, FAQ data, meta title and description, alt text, links inside CMS fields, image fields (re-render via the pipeline).
**Never automatic, propose and wait for Divit's go** (`hubctl live-fix approve ISSUE --by divit` once he says go; an approved sweep adds findings with `live-fix add`): slugs, the primary keyword in H1 or meta, deleting items, template or component edits, classes, sitewide elements, hub pages, anything another person edited (drift).

## How a fix is made (one path, no shortcuts)
**Item publish only, never a site publish (DECISIONS 2026-10-10, NO SITE PUBLISH).**
1. Save the field's live before-value to `childedits/YYYY-MM-DD/<slug>.<issue-id>.before.json`, then commit and push it. `live-fix prepare` refuses to write the payload until that file is in HEAD, unchanged and on origin/main (Divit 2026-10-10): no Webflow write without a pushed before-value.
2. Edit the spec; QC TOTAL 0; PAA gate 10/10 if FAQ changed; images re-rendered if drawn text changed.
3. Update the CMS item (changed fields only), publish that item only (item publish, never a site publish), read back.
4. Re-run Layer A on that URL. If it fails, roll back automatically and mark the issue `rolled-back`.
5. Log it (below). Every human-or-audit catch that the gates missed also becomes a golden test case (LESSONS.md rule 3).

## Documentation
- `audits/live/LEDGER.md` (committed, public-safe): one row per issue: id, date found, URL, field, severity, rule, short description, fix commit SHA, CMS item, published at, verified, rollback file, status (`fixed`, `rolled-back`, `proposed`, `backlog`, `drift-reported`).
- `audits/live/YYYY-MM-DD/<slug>.md`: per page, the exact before and after text of every change and the check that caught it.
- `reports/YYYY-MM-DD/HHMM-live-audit.md`: the run report; its first lines are the **digest for Divit**: pages checked, issues found by severity, fixes made, rollbacks, proposals waiting for a go, drift found.
- Rollback any single fix: `hubctl live-rollback <issue-id>` re-sends the before-value and publishes the item.

## Limits
- At most 10 field changes per page per run; more means the page needs a rework batch, so it is proposed instead.
- A fix that would change the primary keyword, the page's intent or a claim not in the claims ledger is proposed, not made.

## Implementation (2026-10-09)
- Layer A: `ops/live_audit.mjs` (browser half: reuses `ops/verify_launch.mjs` checks, Playwright 1.48.2 render, screenshots, link and image status) and `ops/live_audit.py` (findings, severity, drift, fix plan, ledger, report). Settings: `rules/live_audit.json`.
- Commands: `hubctl live-audit [--since-publish | --all | --urls U,U | --set launch] [--base URL] [--dry] [--external] [--no-shots]`; `hubctl live-audit record|drift|plan|report DATE ...`; `hubctl live-fix apply|brief|prepare|verify ISSUE ...`; `hubctl live-rollback ISSUE [--done RESPONSE]`.
- Webflow is reached only through the MCP: the orchestrating session (or the scheduled headless run) sends the payloads in `ops/out/live/` (update, item publish, read back) and feeds the responses back to `live-fix verify`.
- Drift: a field not rendered as approved is classified with a CMS read (`live-audit drift`): CMS differs from the spec while the spec equals our last write = drift (reported only).
- Layer B state: `audits/live/state.json` (content hash at the last full read); briefs in `.cache/live/DATE/layerB-N.md`.
- Golden cases: `tests/golden/cases.jsonl`, runner `tests/golden/run.py` (open = known miss, guarded = must stay caught).
- Schedule: RUNBOOK section 7. Backup Action: `ops/github/live-audit.yml`.

## Console-error exception (Divit 2026-10-14, widened 2026-10-15)
Applies identically in the live audit and the staging check. An error is ignored only when one named entry covers it; any other console error fails, and the exception is never matched on message text.
- **By source** (the reporting script URL or the top stack frame, captured through CDP by `ops/console_capture.mjs`): `clarity.js` (Microsoft Clarity, any version); `bing-uet-clarity-loader` (`www.clarity.ms/tag/uet/...`, the Bing UET automatic Clarity loader and the source of the "reading 'unshift'" page error; counts as the Clarity exception, 2026-10-15); `gtm-clarity-loader` (`www.clarity.ms/tag/...`, or GTM's inline code with a clarity.ms frame in the stack); `clarity-beacon` (Clarity's collect beacon `https://c.clarity.ms/c.gif` as a failed request or unreachable host, kind `log`, that URL as the source; counts as the Clarity exception, 2026-10-15); `adwire` (`client.adwire.io/clarity/molecule.js`). The same message from any other source still fails (a failed request to any other URL, c.clarity.ms included, still counts).
- **By element** (2026-10-15): `navbar-ai-contests-svg-width`, the `<svg width="2o">` dropdown icon on the /ai-contests link (`a.nav_dropdown-item`) in KS's shared navbar component, until KS fixes it. On every main-frame load (hooked by `captureErrors`) and once more at the end, `tieElements` in `ops/console_capture.mjs` marks errors the page document itself reported (`doc`, kind `log`, no script in the stack) and ties a markup error to its element (tag, attribute, value, inside the navbar, link href and class). The entry matches only when every one of those fields matches; an svg width error from any other element, another attribute or value, or the same text logged by a script still fails. Each document is tied while it is still open, and the element lookup must come back from the document that reported the error (otherwise the error stays untied and counts). Fixed 2026-10-15 (B-dev-9): before, the tie ran once at the end, after load more had replaced the first document with `?xxxx_page=2`, so the first-load error (source = the first URL) no longer matched the current document and counted (16 errors on the 4 child templates in run 20261015-110859Z).
- **Removed (2026-10-15):** the live audit's old text-based `console_ignore` list. The jsdom-only launch check (`ops/verify_launch.mjs`, no error sources in jsdom) keeps its own list under `verify_launch_console_ignore`; neither the live audit nor the staging check reads it.
- Golden cases: `console-*` in `tests/golden/cases.jsonl` (kind `console-source`): each exception matched by source or element, the same text from a different source failing, an svg width error from another element failing, and errors the old text list hid now failing; kind `console-capture` runs the real capture in Chromium on `tests/golden/fixtures/console/*.html` (first load, then a `?e3324f32_page=2` document, as load more does) and checks how many errors each load leaves counted.
