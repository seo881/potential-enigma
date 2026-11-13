# Resume note B-c-2, 2026-11-13 ~09:10 UTC (session ~55%, weekly ~60%; claims stop at 85% weekly)

Live 519 (LP 110, Form 230, Auto 82, SurveyQuiz 97). Shipped today: 29 (+ rsvp in flight). Post-live backlog: see `hubctl postlive-backlog`.

## Running / next
1. AlsoAsked wave for the 110 approved keywords + 11 older queued pages: `ops/pull_wave.py run --run wave-r1113` (cap 200), log /tmp/wave-r1113.log. When done: `.venv/bin/python3 ops/queue_rank.py`, commit plan/queue-ranked.txt, then `hubctl claim <HUB> 25 --by B-c-<n>` per hub, commit status, spawn one page-writer per page (pack-only context, section checks as you write, commit per section, never pull AlsoAsked, ship-first for non-YMYL).
2. B-ship-15: rsvp (a/an display fix -> ship-first) and the bug-report live mockup fix; after it reports, run `hubctl postlive-restamp /ai-form-builder/bug-report --by B-c-<n>`.
3. Post-live reviews due within 24 h for every SHIP-FIRST page (`hubctl postlive-backlog`); blocking -> CMS item update via `hubctl ship-update ... --before-only` + `hubctl api-update` (payload MUST carry the publish action) + verify-live, then `hubctl postlive-restamp`.

## Rules landed today (all golden-tested; golden 1171 cases, 0 regressions)
- SHIP-FIRST: `hubctl state URL approved --by ship-first` (automated checks; YMYL refused via rules/ymyl.json); post-live review via `hubctl postlive-review`; QC R1 uses it.
- Approval paths clear stale R3; `hubctl postlive-restamp` restamps after a post-live fix (coordinator only).
- F6 applies only to FAQs carrying AlsoAsked questions. Authorised refresh runs: diet-r1113, revive-r1113 (weekend.py REFRESH_RUNS).
- Ship-check blocks a quiz page with the general survey table (decision 3).
- a/an agreement is display normalization for verbatim AlsoAsked questions (qc/spelling.articles).
- Per-hub status reconciled with live.json (280 pages -> published).

## Known gaps (Monday rule window, plan/backlog.md)
- No automated cross-field number/label check: 4 of ~25 ship-first pages had one (all fixed live).
- `hubctl images` moves a page to images without QC 0 (ship-check still blocks).
- SERP saves: some writers filled redirect URLs by inference; save exactly what the API returns.
- Live-audit invalid-run detection misses per-page transport timeouts.

## Permissions
private/ reads are denied in-session by rule (Divit: don't change it). Tools that read private/ internally (build_map, pull_wave, queue_rank, weekend aa) are approved. Anything that must read private/proposals is run by Divit with `!`.
