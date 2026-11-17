# Redirect CSV verification: reports/2026-11-17/redirects-final-v3.csv

Run 2026-11-17 07:32 UTC by `ops/redirect_set_check.py verify` against https://emergent.sh (read-only HEAD, GET fallback, redirects not followed), 102.1s.

## Totals

- Rows: 843 (+ header `source,target`); distinct sources 843; distinct targets 771
- Live child pages checked against (status/live.json): 646; hub paths: 4
- Targets returning 200 directly: 771 of 771 (5 needed a re-fetch after a 5xx/transport error: /ai-automation-builder/manufacturing-workflow x1, /ai-form-builder/employee-availability x1, /ai-form-builder/esthetician-intake x1, /ai-form-builder/identity-verification x1, /news/anthropic-launches-claude-haiku-5-5-multimodal x1)
- Against reports/2026-10-23/redirects-final.csv: sources kept 843, added 0, dropped 0; targets changed 30
- Findings: S1-header 0; S2-path 0; S3-dup 0; S4-self 0; S5-chain 0; S6-shadow 0; S7-notlive 0; T1-target 0; **total 0**

## Changed rows (30)

| # | source | old target (status today) | new target (status today) |
|---|---|---|---|
| 1 | /build/healthcare-website-builder | /ai-website-builder/healthcare (301 -> /ai-website-builder/medical) | /ai-website-builder/medical (200) |
| 2 | /build/mobile-website-builder | /ai-website-builder/custom (301 -> /ai-website-builder) | /ai-website-builder (200) |
| 3 | /build/car-dealer-website-builder | /ai-website-builder/dealer (301 -> /ai-website-builder/car-dealer) | /ai-website-builder/car-dealer (200) |
| 4 | /build/interactive-website-builder | /ai-website-builder/interactive (301 -> /ai-website-builder) | /ai-website-builder (200) |
| 5 | /build/reseller-website-builder | /ai-website-builder/reseller (301 -> /ai-website-builder/white-label) | /ai-website-builder/white-label (200) |
| 6 | /build/hospitality-website-builder | /ai-website-builder/hospitality (301 -> /ai-website-builder/hotel) | /ai-website-builder/hotel (200) |
| 7 | /build/web3-website-builder | /ai-website-builder/blockchain (301 -> /ai-website-builder/crypto) | /ai-website-builder/crypto (200) |
| 8 | /build/website-builder-for-tradesmen | /ai-website-builder/contractor (301 -> /ai-website-builder/construction) | /ai-website-builder/construction (200) |
| 9 | /build/betting-website-builder | /ai-website-builder/betting (301 -> /ai-website-builder/casino) | /ai-website-builder/casino (200) |
| 10 | /build/react-website-builder | /ai-website-builder/custom (301 -> /ai-website-builder) | /ai-website-builder (200) |
| 11 | /build/no-code-website-builder | /ai-website-builder/no-code (301 -> /ai-website-builder) | /ai-website-builder (200) |
| 12 | /build/custom-website-builder | /ai-website-builder/custom (301 -> /ai-website-builder) | /ai-website-builder (200) |
| 13 | /build/property-management-website-builder | /ai-website-builder/property (301 -> /ai-website-builder/real-estate) | /ai-website-builder/real-estate (200) |
| 14 | /build/instant-website-builder | /ai-website-builder/instant (301 -> /ai-website-builder) | /ai-website-builder (200) |
| 15 | /build/cloud-based-website-builder | /ai-website-builder/cloud-based (301 -> /ai-website-builder) | /ai-website-builder (200) |
| 16 | /build/dealership-website-builder | /ai-website-builder/dealer (301 -> /ai-website-builder/car-dealer) | /ai-website-builder/car-dealer (200) |
| 17 | /build/contractor-website-builder | /ai-website-builder/contractor (301 -> /ai-website-builder/construction) | /ai-website-builder/construction (200) |
| 18 | /build/gym-website-builder | /ai-website-builder/gym (301 -> /ai-website-builder/fitness) | /ai-website-builder/fitness (200) |
| 19 | /build/responsive-website-builder | /ai-website-builder/custom (301 -> /ai-website-builder) | /ai-website-builder (200) |
| 20 | /build/online-course-website-builder | /ai-website-builder/course (301 -> /ai-website-builder/lms) | /ai-website-builder/lms (200) |
| 21 | /build/conference-website-builder | /ai-website-builder/conference (301 -> /ai-website-builder/event) | /ai-website-builder/event (200) |
| 22 | /build/funnel-website-builder | /ai-website-builder/leadpages (404) | /ai-landing-page-builder (200) |
| 23 | /build/charity-website-builder | /ai-website-builder/charity (301 -> /ai-website-builder/non-profit) | /ai-website-builder/non-profit (200) |
| 24 | /build/attorney-website-builder | /ai-website-builder/attorney (301 -> /ai-website-builder/law-firm) | /ai-website-builder/law-firm (200) |
| 25 | /build/dating-website-builder | /ai-website-builder/dating (404) | /ai-web-app-builder/dating (200) |
| 26 | /build/lawyer-website-builder | /ai-website-builder/lawyer (301 -> /ai-website-builder/law-firm) | /ai-website-builder/law-firm (200) |
| 27 | /build/subscription-website-builder | /ai-website-builder/subscription (301 -> /ai-website-builder/membership) | /ai-website-builder/membership (200) |
| 28 | /build/automotive-website-builder | /ai-website-builder/automotive (301 -> /ai-website-builder/auto) | /ai-website-builder/auto (200) |
| 29 | /build/property-website-builder | /ai-website-builder/property (301 -> /ai-website-builder/real-estate) | /ai-website-builder/real-estate (200) |
| 30 | /build/ai-website-builder/resume | /ai-website-builder/resume (404) | /ai-landing-page-builder/resume (200) |

## Findings

None: 0 failures.
