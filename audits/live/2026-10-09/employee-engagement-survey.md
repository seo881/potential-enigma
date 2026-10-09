# /ai-survey-and-quiz-builder/employee-engagement-survey: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-employee-engagement-survey-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-employee-engagement-survey-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-employee-engagement-survey-B-DECISIONS202-1 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: meta_description
- caught by: B-DECISIONS202 (Layer B): Four-item list without the serial comma.
- live text: with confidential team results, eNPS, driver analysis and manager action plans. Free to start.
- feature_1 before: Questions grouped by engagement driver Core items on pride, intent to stay, advocacy and extra effort come first. Driver sections on managers, growth, recognition, and workload follow. Reword any item with one sentence.
- feature_1 after: Questions grouped by engagement driver Core items on pride, intent to stay, advocacy, and extra effort come first. Driver sections on managers, growth, recognition, and workload follow. Reword any item with one sentence.
- feature_5 before: Org data synced from your HRIS Department, location, tenure and manager sync from your HRIS, such as BambooHR or Workday. Results split along those lines without a single demographic question in the survey.
- feature_5 after: Org data synced from your HRIS Department, location, tenure, and manager sync from your HRIS, such as BambooHR or Workday. Results split along those lines without a single demographic question in the survey.
- howto_step_7_des before: Publish company results within two weeks of close, while people still remember answering. Each manager then meets their team, reads out its focus driver and agrees two actions, each with one owner and a date.
- howto_step_7_des after: Publish company results within two weeks of close, while people still remember answering. Each manager then meets their team, reads out its focus driver, and agrees two actions, each with one owner and a date.
- meta_description before: Build an employee engagement survey with confidential team results, eNPS, driver analysis and manager action plans. Free to start.
- meta_description after: Build an employee engagement survey with confidential team results, eNPS, driver analysis, and manager action plans. Free to start.

## 20261009-employee-engagement-survey-B-DECISIONS202-2 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: feature_1
- caught by: B-DECISIONS202 (Layer B): The first list drops the serial comma while the next sentence uses it (body 180 -> 181 chars, spread 12).
- live text: Core items on pride, intent to stay, advocacy and extra effort come first. Driver sections on managers, growth, recognition, and workload follow.

## 20261009-employee-engagement-survey-B-DECISIONS202-3 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: feature_5
- caught by: B-DECISIONS202 (Layer B): Four-item list without the serial comma.
- live text: Department, location, tenure and manager sync from your HRIS, such as BambooHR or Workday.

## 20261009-employee-engagement-survey-B-DECISIONS202-4 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: howto_step_7_des
- caught by: B-DECISIONS202 (Layer B): Three-verb list without the serial comma.
- live text: Each manager then meets their team, reads out its focus driver and agrees two actions, each with one owner and a date.

## 20261009-employee-engagement-survey-B-DECISIONS202-5 (P2, B-DECISIONS202, backlog)
- field: mockup
- caught by: B-DECISIONS202 (Layer B): Visible tab prompts drop the serial comma in four lists (annualCensus x3, frontlineStaff x1). (mockup prompts are not rendered since the hero redesign; fix at next rework)
- live text: managers, growth, recognition and workload | remind only people who have not answered and hide results | eNPS, the driver most tied to its engagement and an act

## 20261009-employee-engagement-survey-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: why_description
- caught by: B-CONTENTDEFEC (Layer B): Category-wide claim that the table beside it qualifies: SurveyMonkey is shown with per-user pricing, not per employee.
- live text: Engagement platforms price per employee and hold your results.

## 20261009-employee-engagement-survey-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: tab_image_1
- caught by: B-CONTENTDEFEC (Layer B): Sales eNPS +9 with 84 answers is reachable only by truncating (8/84 = 9.5), not by rounding.
- live text: Sales 84 69 +9 Recognition

## 20261009-employee-engagement-survey-H3-sweep-1 (P1, H3-sweep, fix-by-writer, fixed)
- field: mockup, tab_image_1 alt
- caught by: H3-sweep (Layer sweep): serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix
- explore_cta before: Build My Employee Engagement Survey
- explore_cta after: Build My Engagement Survey
- mockup before: window.awbMockup = { annualCensus: "Build an annual employee engagement survey for my company of 600 people. Use 40 statements on a 1-5 agreement scale, with core engagement items first and sections on managers, growth, recognition and workload. Keep it open two weeks, remind only people who have not answered and hide results for any group with fewer than five answers. Give each manager a dashboard with their team's index, eNPS, the driver most tied to its engagement and an action log.", frontli
- mockup after: window.awbMockup = { annualCensus: "Build an annual employee engagement survey for my company of 600 people. Use 40 statements on a 1-5 agreement scale, with core engagement items first and sections on managers, growth, recognition and workload. Keep it open two weeks, remind only people who have not answered and hide results for any group with fewer than five answers. Give each manager a dashboard with their team's index, eNPS, the driver most tied to its engagement, and an action log.", frontl
- tab_image_1 before: An annual engagement census shows each team's response count, engagement index, eNPS and focus driver, hides Legal at three answers and asks the Support manager to log actions on workload.
- tab_image_1 after: An annual engagement census shows each team's response count, engagement index, eNPS and focus driver, hides Legal at three answers, and asks the Support manager to log actions on workload.

## 20261009-employee-engagement-survey-D3-1 (P1, D3, fix-by-writer, fixed)
- field: explore_cta
- caught by: D3 (Layer sweep): explore CTA 35 chars (max 34, QC D3): 'Build My Engagement Survey'
