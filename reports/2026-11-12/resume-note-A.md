# Resume note (A-c-1), session limit 2026-11-11 ~21:00 UTC; resets 02:20 IST 2026-11-12

Live ~484 (455 at handover). All agents stopped at the limit; their work is saved and each can be resumed with SendMessage (same agent ids/context).

On resume, in this order:
1. git pull; check `git status` (uncommitted, owned by stopped agents — never discard: ops/hubctl.py + ops/render_changed.py + tests/golden/* = render-fix agent; ops/ship.py, ops/weekend.py = unknown owner, inspect before anything; specs/sqb/{brand,coffee,color-personality,learning-style,relationship}.json = writers).
2. Ship agent A-ship-3: SQ fitness draft 6af49a9366a5177fcd194c3e is CREATED, NOT item-published (before-value d08570a5). Fresh api-read, then item publish, verify-live, log (live before/after).
3. Verifier A-ver-2: post-ship audits (only form-g1b done) for cleaning-quote update, Form g2, Form g3, SQ g1 (14 quizzes), style+vocabulary updates; quiz CLS on 16 quiz pages. No audit yet on most of today's ships.
4. Writers (WIP limit 10 waiting): A-w-187 compliance, 188 learning-style, 189 color-personality, 190 skin-type, 191 relationship, 193 brand, 194 coffee, 195 compatibility; then enneagram onward (see reports/2026-11-11/resume-note-A.md).
5. Render-fix agent: render_changed --pages + review-claim refuses pages past review; golden green.
Open for Divit: song-request (draft 6af44b1db2ca425f74867f80, unpublished Learn ref), flags_pending gap for locked Q1 PA7 flags, style/vocabulary R3, live insurance spec QC, usage figures.
