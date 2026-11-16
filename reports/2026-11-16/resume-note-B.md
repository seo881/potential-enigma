# Resume note B-c-2, 2026-11-16 ~08:10 UTC: FINISH EVERYTHING (no claim stop; ship-only, no fixing until the comprehensive QC)

Every approved addition is claimed. Remaining ~96 pages: 68 newly claimed + 12 resumed specs + ship-ready pages + automotive (gate decision).
Briefs: scratchpad writer-brief.md (items 1-13) and ship-brief.md. Standing go: .cache/standing-go-2026-11-16.

## Running (40 slots)
- Ship: B-ship-19 Form, B-ship-20 SurveyQuiz, B-ship-21 Automation+LP (Sonnet). Form queue includes medical-waiver and medical-consent-for-minor (YMYL, reviewed, standing-go).
- Writers B-w-707..718: resumed specs (bake-sale, delivery-receipt, hvac-inspection, jha, pip, talent-show, artwork-approval-process, reconciliation, copywriter, lessons-learned, matrix-question, pre-training-questions).
- Writers B-w-719..743: language, movie, music, pet, science, spelling, sports, trivia, travel, wine, agent-open-house-feedback, all-about-me-questionnaire, cookie-exchange, fantasy-football, meal-train, mystery-reader, time-slot, trade-show-lead, white-elephant, field-service, gmail, lead-generation, affiliate, conversational, business-travel-questions.

## Not started yet (claimed): give each a writer as slots free
Form: boat-rental-waiver, bounce-house-waiver, dermaplaning-consent, employee-coaching, employee-termination, forklift-operator-evaluation, haunted-house-waiver, payroll-deduction-authorization, real-estate-buyer-intake, recruiting-intake, return-authorization, scope-of-work, sermon-evaluation, spray-tanning-consent, trip-report, valentines-day-party-sign-up-sheet, wine-tasting.
SurveyQuiz: clothes-questions, drag-and-drop, fill-in-the-blank, flashcard, internal-communications-questions, library, loyalty-program-questions, makeup, map, mattress, media-consumption-questions, persona-questions, retail, safety-quiz, scored, supplement, true-and-false, wellness-quiz, yearbook-questions.
Automation: dsar-workflow, prior-authorization, tax, underwriting. LP: home-valuation, pay-per-call, web-hosting.
YMYL ones (`hubctl ymyl`) need one review (page-reviewer) before ship.

## Landed since 11-13 (golden green except api-before-gate-committed = unpushed-commit artefact)
- QC S6: no HTML in plain-text fields. verify-live and live audit A5-raw-tag: no raw tag text on a page (Divit approved 2026-11-13).
- Link planner: relevant-only (skeleton.link_relevance; same hub 1 shared topic word, cross-hub 2; zero links fine).
- Held for QC: plan/qc-later-2026-11-16.md.

## Update ~08:30 UTC (usage limit reached; resume from here)
- Live ~573. Ship agents: Form (long queue incl. reviewed YMYL medical-waiver, medical-consent-for-minor, pip, haunted-house-waiver under standing-go), SurveyQuiz (music, wine, science, movie, language, spelling, business-travel, pet), Auto+LP (copywriter, lead-generation, affiliate, conversational, field-service, gmail, reconciliation + home-valuation under standing-go).
- Ship rules learned: single commands only (no chaining/$(...)); "before-value not pushed" = HEAD ahead of origin -> sync.sh then retry; verify-live 500 right after publish is cache lag (re-run standalone).
- Blocked, need Divit: F6 stale AlsoAsked (Oct-13 pulls) on locked slots: makeup, sports, trivia (+ likely mattress, safety-quiz, supplement, wellness-quiz) -> asked for <=20 credit refresh; automotive PA4 "car" vs PA12 secondary.
- Writers running B-w-750..785 (see agent list); unstarted claims: mattress, safety-quiz, supplement, wellness-quiz (F6 risk), underwriting.
- Writer brief items 14-15 added (ship-check before done; F6 handling). PIP acronym added to rules/paa_patterns.json.
