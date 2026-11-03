# Redirects v2 changes (2026-11-03)

Source: `reports/2026-10-23/redirects-final.csv` (843 rows). Output: `reports/2026-11-03/redirects-final-v2.csv` (843 rows, same header).
Not imported anywhere: it ships with the next planned domain publish (Divit 2026-11-03). Until Divit says it is imported, `ops/redirect_check.py`
keeps checking the live site against redirects-final.csv, with the 24 failing targets listed as known issues in `rules/live_audit.json`
(known_open_issues ids redir-*, expires 2026-11-17: from that date they count as real fails again).

Found by the daily redirect check (B-dev-20, 2026-11-03): 24 targets not returning 200, covering 30 rows. 21 targets are a second hop
(the target itself 301s to a live page), so the row becomes a 2-hop chain; 3 targets return 404.

## Decisions applied

1. The 21 chains point straight at their terminal URL (followed live, each returns 200).
2. /ai-website-builder/leadpages -> /ai-landing-page-builder (Divit).
3. /ai-website-builder/dating and /ai-website-builder/resume: the closest live page (200, same topic), proposed for Divit's check below.

## Changed rows (30)

| source | old target | new target | reason |
|---|---|---|---|
| /build/healthcare-website-builder | /ai-website-builder/healthcare | /ai-website-builder/medical | chain: /ai-website-builder/healthcare now 301s to /ai-website-builder/medical (200) |
| /build/mobile-website-builder | /ai-website-builder/custom | /ai-website-builder | chain: /ai-website-builder/custom now 301s to /ai-website-builder (200) |
| /build/car-dealer-website-builder | /ai-website-builder/dealer | /ai-website-builder/car-dealer | chain: /ai-website-builder/dealer now 301s to /ai-website-builder/car-dealer (200) |
| /build/interactive-website-builder | /ai-website-builder/interactive | /ai-website-builder | chain: /ai-website-builder/interactive now 301s to /ai-website-builder (200) |
| /build/reseller-website-builder | /ai-website-builder/reseller | /ai-website-builder/white-label | chain: /ai-website-builder/reseller now 301s to /ai-website-builder/white-label (200) |
| /build/hospitality-website-builder | /ai-website-builder/hospitality | /ai-website-builder/hotel | chain: /ai-website-builder/hospitality now 301s to /ai-website-builder/hotel (200) |
| /build/web3-website-builder | /ai-website-builder/blockchain | /ai-website-builder/crypto | chain: /ai-website-builder/blockchain now 301s to /ai-website-builder/crypto (200) |
| /build/website-builder-for-tradesmen | /ai-website-builder/contractor | /ai-website-builder/construction | chain: /ai-website-builder/contractor now 301s to /ai-website-builder/construction (200) |
| /build/betting-website-builder | /ai-website-builder/betting | /ai-website-builder/casino | chain: /ai-website-builder/betting now 301s to /ai-website-builder/casino (200) |
| /build/react-website-builder | /ai-website-builder/custom | /ai-website-builder | chain: /ai-website-builder/custom now 301s to /ai-website-builder (200) |
| /build/no-code-website-builder | /ai-website-builder/no-code | /ai-website-builder | chain: /ai-website-builder/no-code now 301s to /ai-website-builder (200) |
| /build/custom-website-builder | /ai-website-builder/custom | /ai-website-builder | chain: /ai-website-builder/custom now 301s to /ai-website-builder (200) |
| /build/property-management-website-builder | /ai-website-builder/property | /ai-website-builder/real-estate | chain: /ai-website-builder/property now 301s to /ai-website-builder/real-estate (200) |
| /build/instant-website-builder | /ai-website-builder/instant | /ai-website-builder | chain: /ai-website-builder/instant now 301s to /ai-website-builder (200) |
| /build/cloud-based-website-builder | /ai-website-builder/cloud-based | /ai-website-builder | chain: /ai-website-builder/cloud-based now 301s to /ai-website-builder (200) |
| /build/dealership-website-builder | /ai-website-builder/dealer | /ai-website-builder/car-dealer | chain: /ai-website-builder/dealer now 301s to /ai-website-builder/car-dealer (200) |
| /build/contractor-website-builder | /ai-website-builder/contractor | /ai-website-builder/construction | chain: /ai-website-builder/contractor now 301s to /ai-website-builder/construction (200) |
| /build/gym-website-builder | /ai-website-builder/gym | /ai-website-builder/fitness | chain: /ai-website-builder/gym now 301s to /ai-website-builder/fitness (200) |
| /build/responsive-website-builder | /ai-website-builder/custom | /ai-website-builder | chain: /ai-website-builder/custom now 301s to /ai-website-builder (200) |
| /build/online-course-website-builder | /ai-website-builder/course | /ai-website-builder/lms | chain: /ai-website-builder/course now 301s to /ai-website-builder/lms (200) |
| /build/conference-website-builder | /ai-website-builder/conference | /ai-website-builder/event | chain: /ai-website-builder/conference now 301s to /ai-website-builder/event (200) |
| /build/funnel-website-builder | /ai-website-builder/leadpages | /ai-landing-page-builder | Divit 2026-11-03: the funnel/Leadpages intent goes to the landing page hub |
| /build/charity-website-builder | /ai-website-builder/charity | /ai-website-builder/non-profit | chain: /ai-website-builder/charity now 301s to /ai-website-builder/non-profit (200) |
| /build/attorney-website-builder | /ai-website-builder/attorney | /ai-website-builder/law-firm | chain: /ai-website-builder/attorney now 301s to /ai-website-builder/law-firm (200) |
| /build/dating-website-builder | /ai-website-builder/dating | /ai-web-app-builder/dating | closest live page: a dating site is a browser dating product (title "Dating Web App Builder"); /ai-app-builder/dating already takes the dating-app row |
| /build/lawyer-website-builder | /ai-website-builder/lawyer | /ai-website-builder/law-firm | chain: /ai-website-builder/lawyer now 301s to /ai-website-builder/law-firm (200) |
| /build/subscription-website-builder | /ai-website-builder/subscription | /ai-website-builder/membership | chain: /ai-website-builder/subscription now 301s to /ai-website-builder/membership (200) |
| /build/automotive-website-builder | /ai-website-builder/automotive | /ai-website-builder/auto | chain: /ai-website-builder/automotive now 301s to /ai-website-builder/auto (200) |
| /build/property-website-builder | /ai-website-builder/property | /ai-website-builder/real-estate | chain: /ai-website-builder/property now 301s to /ai-website-builder/real-estate (200) |
| /build/ai-website-builder/resume | /ai-website-builder/resume | /ai-landing-page-builder/resume | Divit 2026-11-03: a personal resume site for job seekers = the resume landing page ("Build a Resume Landing Page That Gets Recruiters to Write Back"). CONDITION: that page is not live yet (in rework on 2026-11-03); it must return 200 before this CSV is imported. Was proposed: /ai-web-app-builder/resume |

All other rows are unchanged.

## Before import (checklist)
- /ai-landing-page-builder/resume must be live (200): run `python3 ops/redirect_check.py check --csv reports/2026-11-03/redirects-final-v2.csv` against staging after the import and confirm 843/843.
