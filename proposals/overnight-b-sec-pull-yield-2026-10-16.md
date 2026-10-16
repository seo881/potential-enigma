# Proposal: step 6b secondary pulls should stop when they lift no page (B, 2026-10-16)

**Seen:** in one session, `overnight_b.py next` listed 6b twice (8 pages, then 8 more). All 16 were relevance-checked and pulled with `weekend.py aa URL --kw secondary --run night-r1015`. 11 returned questions (1 credit each), 5 returned no_results (0 credits). Run total: 12 of 60. After `queue_rank.py`, every one of the 16 kept its feasibility (9, 8 or 7). None reached ready, so nothing could be claimed. The gate does read the `--sec` file (`qc/paa_gate.py` `pulls`), so the secondary-pull questions are being rejected or merged as near-duplicates of questions the page already has.

**Effect:** the queue has no non-quiz ready page, quizzes wait on the quiz template, and `next` lists 6b until the 60 credits are gone. Each later session would spend about 8 credits on rows that need more questions (feasibility 7 needs +3) with 0 of 16 lifted so far.

**Proposed fix (default):** `overnight_b.py next` stops listing 6b for the run once a round of at least 8 secondary pulls lifts no page to ready (count kept in `.cache/overnight-b/`). It then exits 3 ("nothing left") unless other work is listed. Golden case: a run with 8 sec pulls and 0 lifts lists no 6b rows.

**Done this session:** I stopped pulling after the second round and left the remaining 48 credits unspent. No rule or tooling change was made.
