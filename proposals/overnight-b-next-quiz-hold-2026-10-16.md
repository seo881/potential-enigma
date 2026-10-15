# Proposal: `overnight_b.py next` should not list held quiz pages under "0 ship" (B, 2026-10-16)

**Seen:** style-quiz and vocabulary-quiz pass `hubctl ship-check` (after learn_refs were added, 473e63f3) and are `approved`, but `hubctl api-create SurveyQuiz --before-only` holds both: "quiz page: the quiz template is not live yet (config quiz_template_live)". `overnight_b.py next` still lists them under "0 ship", so `next` never exits 3 ("nothing left") and the loop keeps starting sessions that cannot ship them.

**Proposed fix (default):** `overnight_b.py next` uses the same filter as `_create_candidates` (quiz pages excluded while `quiz_template_live` is false, and while `status/quiz-canary.json` is not `pass`), so the ship list and the create list agree. Golden case: an approved quiz page with quiz_template_live false is not in `next`'s ship list.

**Also seen tonight (for Divit, no change made):**
- gdpr-consent-form parked: FAQ slot 7's secondary contains "gdpr-compliant"; K8 requires it verbatim in the question and QC C2 blocks it. Recommended default: exempt question text that only repeats a secondary keyword from C2.
- check-request-form parked: feasibility counted 10, the writer judged at most 8 honest (one off-intent, one brand, two obscure named forms). The feasibility count does not apply the judgment a writer applies.
