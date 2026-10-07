# Keyword plan: source, overrides and known issues (2026-10-06)

Source workbook: `Emergent_Hub_Child_Pages_Final_v3.xlsx` (Divit, Semrush US, Oct 2026). It lives in the Claude Project context, never in this public repo: Semrush data cannot be redistributed. `plan/build_map.py` regenerates `plan/keyword_map.json` and `plan/queue.csv` (both git-ignored) from it.

## Verified claims
601 child pages (Form 278, LP 118, SurveyQuiz 116, Auto 89); 0 duplicate slugs; 0 duplicate primaries; 0 keywords on two URLs; Build plan matches the final map URL-for-URL and primary-for-primary; waves 246 / 65 / 242 / 48.

## Decisions by Divit (2026-10-06)
- The 4 live child pages stay as they are (primaries, slugs, content). Overrides in `plan/overrides.json`:
  - CSAT cluster (25 keywords) moved from the sheet's `/customer-feedback-survey` page back to the live `/customer-satisfaction` page. Both pages share part of one SERP (4 of 10 URLs); angles must stay distinct (feedback = any customer feedback; CSAT = the transactional score).
  - `/approval-workflow` keeps "approval workflow" (590) as primary; "approval workflow software" (720) is its first secondary (same URL in the sheet, only the label differs).
  - `/creator-application` stays live although the sheet cut it (app-builder SERP). Excluded from the build queue.
- Build order: descending total volume (primary + all secondaries), lowest-volume pages last. Wave 4 (needs a playable quiz) at the end.
- Survey hub path normalised to the live `/ai-survey-and-quiz-builder` (the sheet wrote `/ai-survey-quiz-builder` on all 155 rows).

## Known issues in the workbook (read the data with these in mind)
1. "SERP fit (pass 3)" says "Not pulled" on 304 pages whose top 10 WAS pulled. The verdict is in the Build plan and in "Pass 3 action".
2. Build plan "Total MSV targeted" excludes the Semrush secondaries on 457 of 601 pages; the queue here uses the full totals from the final map.
3. 43 pages carry a secondary that out-searches the primary (e.g. work order form 880 vs a 1,900 secondary), against the sheet's own primary-fix rule. Check intent per page before writing.
4. 137 primaries under 50 MSV, 6 at 0, 87 with no Semrush intent data (Tier 2 tail).
5. 87 queue pages (mostly Form) sit on document-template SERPs (eForms, LegalTemplates, DMV PDFs): searchers expect a printable or downloadable document. 8 of the top 50 are such pages, including #1, #2, #6. Flagged in queue.csv as "generated document (template SERP)". Wave 4 pages need a playable quiz. Neither capability exists on the child templates today.
6. AI Overviews appear on 61% of Automation and 39% of LP primary SERPs: those pages need a definition block near the top (the template's definition sits in the FAQ at the bottom).
7. 28 unassigned clusters in "Pass 3 new page ideas" (attachment style quiz 63,900; child travel consent form 29,860; rsvp website 9,000; email automation 7,720) are not in the queue.

## Wave 3 SERP report (Emergent_Wave3_SERP_Report.xlsx, Project context)
Merged by `build_map.py` (PE_WAVE3 env or /mnt/project or private/). Verdicts: 119 builder-fit, 25 AMBER (angle carried into the brief), 87 with no Semrush data (`serp_needed`: DataForSEO at brief time), 8 cut Rule A and 3 merges held as `needs-decision`:
cut Rule A: citizen-complaint-form, whistleblower-form, dependent-verification-form, wire-transfer-request-form, 401k-rollover-form, financial-assistance-form, hsa-reimbursement-form, dealer-application-form.
merge: agency-landing-page into design-agency-landing-page; author-landing-page into book-landing-page; business-coaching-intake-form into life-coaching-intake-form.
