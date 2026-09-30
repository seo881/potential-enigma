# AI Survey and Quiz Builder hub: pre-launch audit

**Page:** `/ai-survey-and-quiz-builder` (page ID `6ab246c3897d1c09d9d320ec`, Draft)  
**Audited:** 30 Sep 2026, against live Designer content, live schema, and vendor pricing checked this week.

## Scorecard

| Priority | Count |
| --- | --- |
| P0 fact | 5 |
| P1 SEO | 3 |
| P1 readability | 4 |
| P2 polish | 2 |

P0 = factually wrong or unverifiable claim (must fix before launch). P1 = ranking or readability. P2 = polish.

## 1. Meta title, description, OG

| Field | Current | Chars | Proposed | Chars | Why |
| --- | --- | --- | --- | --- | --- |
| SEO title | AI Survey Maker, Quiz Maker & Poll Maker in One / Emergent | 58 | Free AI Survey Maker, Quiz Maker & Poll Maker / Emergent | 56 | 'Free' is the dominant modifier on 'survey maker' SERPs; 'in One' adds no search value. |
| Meta description | Build a survey, quiz, or poll from a prompt. Emergent generates the questions, the logic, and a database you own. No response caps. Free to start. | 146 | Keep |  | 145 chars, good. Keep. |
| OG title | AI Survey, Quiz & Poll Builder / Emergent | 41 | Keep |  | Fine. |

## 2. Findings, section by section

| # | Priority | Section / element | Current text | Issue | Proposed text | Len |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | P1 SEO | Hero H1 | Every response you collect is yours. No caps, no per-response fee. | No keyword ('survey maker' or 'quiz maker'), and it repeats the subhead's last line nearly word for word. | The AI survey and quiz maker with no response caps | ✅ (50) |
| 2 | P1 readability | Hero subhead: ending | …to a database you own. No response caps. No per-response fees. | With the new H1, 'No response caps' would repeat. | …to a database you own. No per-response fees. | 45 |
| 3 | P1 readability | 3-column cards: heading | Three things you get on day one that SurveyMonkey, Typeform, and Interact don't ship together. | 94 chars, 4 lines. | Three things other survey tools cap or split | ✅ (44) |
| 4 | P0 fact | Value card 1: text | SurveyMonkey Advantage caps at 15,000 responses per year, then charges $0.15 per extra. Typeform Basic stops collecting at 100/month. Interact Lite stops at 500 leads. Emergent writes every response to a Postgres table… | The 'Interact Lite stops' behaviour at the cap is unverified (only the Free plan is confirmed to pause), and 'Postgres' is unverified. | SurveyMonkey Advantage includes 15,000 responses a year, then charges $0.15 per extra. Typeform Basic stops collecting at 100 a month. Interact Lite includes 500 leads a month. Emergent writes every response to a database in your project. No cap. No overage. | 258 |
| 5 | P2 polish | Value card 3: text | No SurveyMonkey logo in the footer. No Typeform subdomain in the URL… | It depends on the plan (paid tiers remove branding and add custom domains), so it's safer generalised. | No vendor logo in the footer, no vendor subdomain in the URL. Publish the survey, quiz, or poll on your own domain (built in, uses credits), keep every result in your own database, and export the whole codebase whenever you want to leave. | 238 |
| 6 | P1 readability | Features: heading | Everything a survey maker, quiz maker, or poll maker should ship with, in one build. | 83 chars, 4 lines. | Everything a survey, quiz, or poll needs | ✅ (40) |
| 7 | P0 fact | Features: Feature 2 | Postgres table in your Emergent project… | 'Postgres' is unverified. | A database in your Emergent project that you own. No response cap, no annual limit, no per-response overage, no upgrade to see your last thousand responses. | 156 |
| 8 | P0 fact | Features: Feature 3 | …not gated behind a $46/mo Advantage plan or a $53/mo Growth plan. | False on both counts: SurveyMonkey skip logic starts on Standard, and Interact branching starts on Lite ($27/mo), not Growth. | Show questions by earlier answer, weight answers toward result buckets, calculate a score, and route by outcome. Included from the free tier, with no upgrade to unlock advanced logic. | 183 |
| 9 | P1 readability | Integrations: H2 | Every tool your survey, quiz, and poll [line break] results feed into | The first line is 38 chars, which re-wraps to 3 lines. | Every tool your results feed into | ✅ (33) |
| 10 | P1 SEO | Comparison: H2 | Survey makers, quiz makers, and poll tools compared | 51 chars, 3 lines. | Survey, quiz, and poll makers compared | ✅ (38) |
| 11 | P0 fact | Comparison: subheading | Based on each vendor's published 2026 plans. Each use-case page compares… | The second sentence is now false. | Based on each vendor's published plans, checked September 2026. | ✅ (63) |
| 12 | P0 fact | Comparison: Interact cells | Response limits: 'Lite 500 leads/mo, Growth 2,000 leads/mo (quiz stops at cap)' · Behavior at cap: 'Quiz stops collecting' | Paid-plan behaviour at the cap is not published by Interact; only the Free plan (100 completions) is confirmed to pause. This also appears on the Customer Satisfaction Survey child page. | Response limits: 'Free 100 completions/mo, Lite 500 leads/mo, Growth 2,000 leads/mo' · Behavior at cap: 'Free plan quiz pauses; paid plans cap leads' | 149 |
| 13 | P2 polish | How-to: Step 01 description | Satisfaction, engagement, fit, preference, or knowledge… (62 words) | About 50% longer than the other steps and breaks the rhythm. | Satisfaction, engagement, fit, preference, or knowledge. A CSAT survey and a product quiz look alike but answer different questions, and a poll is a survey cut to one or two questions with live results. The measurement decides the questions and the scale. | 255 |
| 14 | P1 SEO | Related articles: sort | Publishing date: ascending (oldest first) | It should be newest first, matching the LP and Form hubs. | Publishing date: descending | 27 |

## 3. FAQ changes (the FAQPage schema must be rebuilt word-for-word after these land)

| # | Question | Current (excerpt) | Issue | Proposed answer |
| --- | --- | --- | --- | --- |
| 1 | What is the best free survey maker in 2026? | …Google Forms is free with no cap but has no branded domain, no scoring logic, and no database you can query. | False: Google Forms quiz mode scores answers with point values. | It depends on what you need to own. Emergent's free tier has no response cap, and custom domains are built in, using credits: the two things most free plans hold back. SurveyMonkey Basic is free but caps at 10 questions and 25 responses per survey. Typeform's free plan is 10 responses per month. Google Forms is free with no cap, but it has no custom domain, scores quizzes by points only with no personalized result screens, and keeps responses in your Google account rather than a database you own. |
| 2 | Is there a response cap? | …Interact Lite stops at 500 leads. Typeform and Interact stop collecting when the cap is reached… | Interact paid-plan behaviour at the cap is unverified. | No. Emergent does not meter responses. SurveyMonkey Advantage includes 15,000 responses per year and charges $0.15 per extra. Typeform Basic stops collecting at 100 per month. Interact Lite includes 500 leads per month, and its free plan pauses quizzes at 100 completions. |
| 3 | How much does a survey maker, quiz maker, or poll maker cost? | …ScoreApp Starter is $29/mo annual, up to $797/mo for the Scale tier. Poll Everywhere and Slido price per active audience. | The ScoreApp figures were not verifiable this week; remove them rather than risk a wrong price. | Emergent starts free, with paid plans priced on usage rather than response or lead counts. SurveyMonkey Advantage is $46/mo billed annually ($552/year). Typeform Basic is $28/mo annual. Interact Lite is $27/mo annual for 500 leads. Poll Everywhere and Slido price by audience size. |

## 4. Verified as accurate (no change)

- SurveyMonkey: Basic (free) 10 questions and 25 responses per survey; Advantage 15,000 responses/yr at $46/mo annual ($552/yr, US); Team Advantage 50,000/yr; $0.15 per extra response (vendor pricing page).
- Typeform: Free 10/mo, Basic 100/mo at $28/mo annual; stops collecting at the cap.
- Interact: Lite 500 leads/mo ($27/mo annual), Growth 2,000 ($53/mo annual); the free plan pauses at 100 completions.
- The 'Does the survey, quiz, or poll have real skip logic?' FAQ is accurate: SurveyMonkey's 'more logic features' are on Advantage, and Typeform logic is from Basic.

## 5. Housekeeping

- Delete the hidden first-draft duplicate carousel section `86e5ccd1-891e-bb61-1762-8591adc90744`.
