# Slug migration: mapping for Divit (2026-10-23, redo)

**Rule** (Divit, 2026-10-23; the AI App Builder collection works the same way): the slug is the target keyword as it appears in the page's H1, with only the hub's category word removed, then lowercased and hyphenated. Nothing else changes.

- **Category words:** "landing page" for LP, "form" for Form, "automation" for Automation, and "survey" and "quiz" for SurveyQuiz (plurals count as the same word).
- **Everything else stays,** including workflow, page, questionnaire, sheet, template, automated and questions.
- **This redo replaces the earlier packet.** All of its recommendations and class rulings are discarded.

**Map:** `plan/slug-migration.json`, built by `ops/slug_migrate.py map`. Webflow was read only (GET); nothing was written or published, and the freeze stays on.

**How the H1 phrase is found:** `skeleton.h1_phrase_for(primary)` is looked up in the H1. The H1 comes from the spec's `fields.h1`, or from the CMS name when there is no spec. The lookup ignores case and hyphens and allows a plural. Pages with no H1 yet use the primary keyword, and the row records that as `slug_source`.

## Counts (619 rows: 339 live + 280 planned)

| Hub | Live: change | Live: unchanged | Live: collision | Planned: change | Planned: unchanged | Planned: collision |
|---|---|---|---|---|---|---|
| LP | 65 | 8 | 0 | 43 | 2 | 0 |
| Form | 118 | 13 | 0 | 153 | 6 | 0 |
| Auto | 54 | 22 | 0 | 15 | 0 | 0 |
| SurveyQuiz | 52 | 4 | 3 | 58 | 0 | 3 |

**Where the slugs come from:**
- Taken from the H1: 421 (all 339 live pages and 82 planned).
- Taken from the primary keyword, because there is no H1 yet: 219. This includes 21 pages that appear only in the git-ignored keyword map; they are mapped in `private/migration/`.
- In every row, the new slug equals the old slug with the category word removed. No page's H1 phrase moves its slug any further than that.

## H1 phrase vs primary keyword: 2 pages differ (not fixed; your call)

| Hub | Page | Phrase in the H1 | Primary keyword | New slug |
|---|---|---|---|---|
| LP | startup-landing-page | Startup Landing Page | best startup landing pages | startup |
| Form | hipaa-release-form | HIPAA Release Forms (plural) | hipaa release form | hipaa-release |

## Collisions: 3 (the same new slug twice in one collection)

| Hub | New slug | Page 1 (live) | Page 2 (planned, no H1 yet) |
|---|---|---|---|
| SurveyQuiz | safety | safety-survey: "Build a Safety Survey That Sends Each Manager Their Own Results" | safety-quiz |
| SurveyQuiz | team | team-survey: "Build a Team Survey That Shows How Your Team Works" | team-quiz |
| SurveyQuiz | wellness | wellness-survey: "Build a Wellness Survey That Shows Which Group Needs What" | wellness-quiz |

No other collection has a collision.

## 15 random rows (seed 20261023: `ops/slug_migrate.py sample 15 --seed 20261023`)

| Hub | Old | H1 | New |
|---|---|---|---|
| Form | demo-request-form | Build a Demo Request Form That Books the Call on Submit | demo-request |
| Form | event-waiver-form | (no H1 yet: primary) | event-waiver |
| Form | tenant-screening-form | Build a Tenant Screening Form That Records Every Decision | tenant-screening |
| SQ | stakeholder-survey | Build a Stakeholder Survey That Compares Every Group | stakeholder |
| Form | stay-interview-form | (no H1 yet: primary) | stay-interview |
| Form | chemical-peel-consent-form | Build a Chemical Peel Consent Form That Records Every Peel | chemical-peel-consent |
| SQ | love-language-quiz | (no H1 yet: primary) | love-language |
| Form | wedding-rsvp | Build Your Own Wedding RSVP Website | wedding-rsvp |
| Auto | document-approval-workflow | Build a Document Approval Workflow That Tracks Every Version | document-approval-workflow |
| LP | lead-magnet-landing-page | Build a Lead Magnet Landing Page That Delivers the Offer | lead-magnet |
| Auto | excel-automation | (no H1 yet: primary) | excel |
| LP | high-converting-landing-page | Build a High-Converting Landing Page, Then Test What Works | high-converting |
| Form | time-off-request-form | Build a Time Off Request Form That Checks PTO Balances | time-off-request |
| Form | move-out-form | (no H1 yet: primary) | move-out |
| Form | silent-auction-form | Build a Silent Auction Form That Checks Bids and Names Winners | silent-auction |

## For steps 3 to 5 (unchanged from the first pass)

- **Redirects by API: no on this site.** `data_enterprise_tool` has `create_301_redirect`, but a read-only `list_301_redirects` returned: "This site does not have an Enterprise hosting plan." The 301s go in by hand under Site settings > Publishing > 301 redirects (CSV import).
- **Hard-coded internal links:**
  - **Live CMS:** 891, all in FAQ answers (`awb---faq-data`), across 335 items. 759 of them point at a slug that changes.
  - **Specs** (non-archived): 1,133 rendered FAQ links and 908 link-plan entries (`faq_plan.link.url`, `pending_links.target`).
  - **Hub pages:** they link only through dynamic collection lists, so they update by themselves.
  - **Not checked:** links from other collections and from pages outside the 4 hubs.

## Tightened check (step A): the H1 adds words to the keyword. 6 new pages; work stopped here

Method: the H1 noun phrase around the keyword was compared with the primary for all 421 rows whose slug comes from the H1. This catches words added before or after the keyword inside the same noun phrase.
- `ops/slug_migrate.py map` sets the flag `h1_adds_*`.
- 49 H1s had some word after the keyword. Each was read by hand: in the other 43, that word opens a clause ("Around Your...", "Clients Sign...", "Driven by..."). That is not an addition.
- Already ruled, so not counted: startup, hipaa-release, and wedding-rsvp (its H1 is now "Wedding RSVP Form", per the ruling).

The six new pages split by whether the addition changes the slug.

**The addition would change the slug (4):**

| Hub | Page | H1 | Primary | Slug from the primary | Slug from the full H1 phrase |
|---|---|---|---|---|---|
| Form | employment-verification-letter | Build an Employment Verification Letter **Generator** for HR | employment verification letter | employment-verification-letter | employment-verification-letter-generator |
| Form | independent-contractor-agreement | Build an Independent Contractor Agreement **Generator** | independent contractor agreement | independent-contractor-agreement | independent-contractor-agreement-generator |
| Form | nda-form | Build an NDA Form **Generator** and Signing App | nda form | nda | nda-generator |
| LP | thank-you-page | Build a **Custom** Thank You Page With One Clear Next Step | thank you page | thank-you-page | custom-thank-you-page |

**The slug is the same either way, because the added word is the category word (2):**

| Hub | Page | H1 | Primary | Slug |
|---|---|---|---|---|
| Form | creator-application (draft) | Build a Creator Application **Form** Using AI in Minutes | creator application | creator-application |
| SurveyQuiz | customer-effort-score | Build a Customer Effort Score **Survey** That Finds the Hard Step | customer effort score | customer-effort-score |

Steps B (staging prep) and C (canary) have not started; they wait on these calls.
