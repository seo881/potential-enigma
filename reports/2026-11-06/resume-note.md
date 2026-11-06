# Resume note 2026-11-06 (B-c-1)

FIRST: read reports/2026-11-06/ship-run.md (B-ship-8's tally). Writing is STOPPED (Divit, session at 65%); no new claims.

## Shipping (CMS item publishes only; never a site/staging/domain publish)
- B-ship-8 was shipping: the 6 rulings-1-2 live fixes (solar, telehealth, chiropractic-intake, acupuncture-intake, coaching-application; patient-intake draft update + publish), cleaning-quote once Divit re-approves it, then new Form pages under the 2026-11-06 standing go: event-booking, family-law-intake, financial-planning-intake, guest-list, gym-membership-cancellation, landscaping-quote, moving-quote, makeup-consultation, mentorship-application, influencer-application, event-waiver, little-league-registration, nutrition-intake.
- Quiz canary: style + vocabulary approved on Divit's recorded go (by name). B-ship-8: item-publish style, production CLS (ops/quiz/cls.mjs, 5 runs at 1440 and 390, < 0.01), then vocabulary, then status/quiz-canary.json -> pass, which opens the 47 quizzes.

## Waiting on Divit
- cleaning-quote: `state approved --by divit` (go recorded cda5256f).
- massage-booking: re-approval command (slim review passed 8675cdbd; R3 only).
- Q1 PA7 definition flags: health-coaching-intake, home-insurance-quote (both held by B-c-1; ship-check does not count gate flags: tool gap).
- job-posting: failed its slim review after the one rework (tab 1 clinic + pay basis in image only); Divit: allow a second fix or park.

## Partial specs (state spec; resume with skeleton.py build URL --by <id> --adopt; scripts in the scratchpad B-w-<n>/ folders are session-local)
royalty-agreement (skeleton only), paypal-donation (hero/features/why), roofing-quote (hero/features/why), occupational-therapy-intake (+ usecases, 7 P1 left), podcast-application (+ usecases, 2 P0 mockup), password-reset (+ usecases, tab 4 image), pest-control-quote (hero/features/why), painting-quote (+ usecases, 1 P1), personal-training-intake (usecases 39 P0/P1), photo-contest (usecases failing).
Never started (claimed by B-c-1): salon-booking, solar-quote, song-request, spa-booking, speaker-application, speech-therapy-intake, stay-interview, stripe-donation, team-registration, tour-booking, walk-through, wellness-intake.

## Rules added this session
QC L15 (features all-six claim, new writing), QC M1 (health details in transit), review refuses #10/#20 notes, rules/keyword_forms.json (hyphenation), render_changed --pages exclusive, Divit 2026-11-06 no plan depends on a site publish (DECISIONS + CLAUDE.md), redirect v2 parked (known issues to 2027-02-01).

## Tool gaps
- ship-check passes with a pending gate flag (Q1 PA7): add the gate's flag count to ship-check.
- The review lock reads only a finding's field key: fields named in the finding text need coordinator unlocks.
- `hubctl images` moves an approved/published page's state to images.
- The FAQ link plan puts loosely related sibling links into FAQs (spa links on a gym page).

AUDIT: today's 07:28 UTC Mac run was a network failure (552 transport errors); the 13:01 re-run was in progress.
