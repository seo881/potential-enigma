# Live audit: every live page checked, every character, issues fixed and documented

Decided by Divit 2026-10-09 (DECISIONS). Divit spot-checks 2-3 URLs; this system checks all of them, fixes what it is allowed to fix, and documents everything with a rollback.

## When it runs
- **Right after every publish** (all newly live URLs), then **daily** on every live child page and the 4 hubs.
- Layer A (deterministic, no LLM) can run unattended as a GitHub Action (`.github/workflows/live-audit.yml`, GITHUB_TOKEN only, no API keys). It writes `audits/live/YYYY-MM-DD/findings.json`.
- Layer B (judgment + fixes) runs in Claude Code with one command: `hubctl live-audit [--since-publish | --all]`.

## What is checked on each live URL (rendered page, after scripts run)
**Layer A, deterministic:**
- HTTP 200, canonical = self, no `noindex`, in the sitemap; title and meta description present, within pixel and character limits, matching the spec exactly.
- Every spec field rendered exactly once; nothing rendered that is not in the spec (stray template text, "Lorem", "This is some text", empty sections, "No items found").
- Character hygiene on all visible text, alt text, meta and JSON-LD: zero-width and control characters, broken entities (`&amp;amp;`), double spaces, em dashes, curly or straight quote mixing, UK spellings, repeated words, unclosed brackets.
- Links: every internal link 200 and live; hub link present exactly once; no link to a non-live page; external source links 200 (weekly).
- Images: load 200; correct format (SVG for use-case and covers, WebP og:image); og:image 1200x630 at most 300 KB; non-empty alt; use-case images exactly 3:2.
- Scripts: hero prompt prefilled, chips switch it, FAQ rendered with 10 items, first tab active, carousel covers present.
- JSON-LD parses; FAQ items in schema match the visible FAQ word for word.
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
**Never automatic, propose and wait for Divit's go:** slugs, the primary keyword in H1 or meta, deleting items, template or component edits, classes, sitewide elements, hub pages, anything another person edited (drift).

## How a fix is made (one path, no shortcuts)
1. Save the field's live before-value to `childedits/YYYY-MM-DD/<slug>.<issue-id>.before.json`.
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
