# Resume note, B, 2026-11-03 (SHIP FIRST, Divit)

FIRST LINE: ship the waiting queue. No new writing until everything written and QC-passing is live, held, or in Divit's packet.

## State (HEAD 8254922e)
- Go: status/go/2026-11-02.json (+2026-11-03.json) records Divit's standing go; .cache/standing-go-2026-11-03.
- Shipped today: payroll-change (verify-live PASS). Ship agent B-ship-5 resumed on: Form 22 approved + SQ 6 approved, then Auto 3 reviewed + CMS drafts that pass ship-check.
- CORRECTED (B-c-1, 11:57 UTC): the Form api-create at 25fc1343 DID write all 22 drafts despite its 504 (created 08:29 UTC, isDraft true, never published; fresh read form-api-20261103T115706Z: 168 unique items). My earlier "0 written" came from form-api-20261103T082910Z, a read taken mid-create that held 168 rows but only 146 unique ids (22 duplicate rows from pagination). B-ship-5 records them with bulk-verify from the fresh read; NEVER retry that create. Lesson: count unique ids, never rows, and re-read after a 5xx on a create.
- Writers: 60 empty claims released; 18 LP specs are PARTIAL (skeleton + plan; freelancer has its hero). They are not in review. They resume first when the ship queue is empty.
- The redirect-check agent (B-dev-20) was resumed to finish; its files are uncommitted until it does (ops/redirect_check.py, live_audit*, workflow, golden). A dirty tree makes the daily audit skip, so commit or patch them before the next audit run.
- Never ship: drug-test-consent, sublease, personal-injury-intake (Divit 10-26). Held: surgery-consent, food-bank-application (Q1), approval-workflow (A-s-13 slim review to record from A's clone). Canaries style and vocabulary untouched.
