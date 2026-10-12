# /ai-landing-page-builder/mobile-landing-page: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-mobile-landing-page-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-mobile-landing-page-B-QCA1stocknam-1 (P1, B-QCA1stocknam, proposed)
- field: template
- caught by: B-QCA1stocknam (Layer B): The "More things you can build" AI CRM Builder card draws the stock placeholder company "Acme Corp", now a listed AI tell; the card is a sitewide component outside the child collections.
- live text: AI CRM Builder card: AC Acme Corp $24,000 Proposal

## 20261012-mobile-landing-page-B-CONTENTDEFEC-1 (P1, B-CONTENTDEFEC, proposed)
- field: template
- caught by: B-CONTENTDEFEC (Layer B): The AI Schedule Builder card in "More things you can build" shows "Thursday, Oct 16", but 16 October 2026 is a Friday; it is a sitewide component outside the child collections.
- live text: Thursday, Oct 16 9:30 Team standup 1:30 Demo call Booked

## 20261012-mobile-landing-page-B-HUBRULES5com-1 (P1, B-HUBRULES5com, fix-by-writer, fixed)
- field: why_table
- caught by: B-HUBRULES5com (Layer B): The Wix "Where submissions go" cell understates Wix: Wix Forms keeps submissions in the site dashboard with export, not only an email. The library fact (lp.json Wix.data, 2026-09-28) cites only "vendor pricing page".
- live text: Where submissions go | ... | Wix: Basic contact form to email
- mockup before: window.awbMockup = { callAndText: "Build a landing page for my mobile dog grooming business, Paws on Wheels. Most people find us on their phones, so put two large buttons in a sticky footer: one starts a text to our booking number with a request half written, the other rings the van. Log each tap with the button pressed and the utm_campaign value, and give me monthly totals per button.", socialAdQualifiers: "My solar company, Brightway Solar, runs Facebook ads to a quote page. Ask four questions
- mockup after: window.awbMockup = { callAndText: "Build a landing page for my mobile dog grooming business, Paws on Wheels. Most people find us on their phones, so put two large buttons in a sticky footer: one starts a text to our booking number with a request half written, the other rings the van. Log each tap with the button pressed and the utm_campaign value, and give me monthly totals per button.", socialAdQualifiers: "My solar company, Pellmore Solar, runs Facebook ads to a quote page. Ask four questions,
- tab_content_2 before: Solar leads, qualified one tap at a time Brightway Solar's Facebook ad opens a qualifier with four questions, a question per screen, each answered by tapping a large button. Only the ZIP code step opens the number pad. Homeowners are saved as leads, and a sales rep calls each one by 9 AM the next day. Renters see a page about community solar.
- tab_content_2 after: Solar leads, qualified one tap at a time Pellmore Solar's Facebook ad opens a qualifier with four questions, a question per screen, each answered by tapping a large button. Only the ZIP code step opens the number pad. Homeowners are saved as leads, and a sales rep calls each one by 9 AM the next day. Renters see a page about community solar.
- tab_content_3 before: Pickup windows that close at 25 orders Every Thursday at noon, Fern and Field Florist texts subscribers a link to its weekend bouquet. Saturday pickup windows show as large buttons, with payment at the counter. Each window holds 25 orders and drops off the page once full. This week the 10 AM window closed first, and the prep list shows 76 bouquets.
- tab_content_3 after: Pickup windows that close at 25 orders Every Thursday at noon, Rosehill Florist texts subscribers a link to its weekend bouquet. Saturday pickup windows show as large buttons, with payment at the counter. Each window holds 25 orders and drops off the page once full. This week the 10 AM window closed first, and the prep list shows 76 bouquets.
- tab_content_4 before: How the demo page restacks on a phone On a laptop, Fieldnote's demo page shows its plans for inspection teams side by side in a pricing table. On a handset the plans stack as cards, and the demo form moves up under the headline. Each request is saved with the device it came from. Phones sent 94 of last month's 162 demo requests.
- tab_content_4 after: How the demo page restacks on a phone On a laptop, Pinlog's demo page shows its plans for inspection teams side by side in a pricing table. On a handset the plans stack as cards, and the demo form moves up under the headline. Each request is saved with the device it came from. Phones sent 94 of last month's 162 demo requests.
- tab_image_2 before: Brightway Solar's quote page asks one question per screen with large answer buttons, and a homeowner's answers are saved as a lead with a sales call set for 9 AM the next day.
- tab_image_2 after: Pellmore Solar's quote page asks one question per screen with large answer buttons, and a homeowner's answers are saved as a lead with a sales call set for 9 AM the next day.
- tab_image_3 before: Fern and Field Florist's text offer page closes each Saturday pickup window at 25 orders, and the prep list totals 76 bouquets.
- tab_image_3 after: Rosehill Florist's text offer page closes each Saturday pickup window at 25 orders, and the prep list totals 76 bouquets.
- tab_image_4 before: Fieldnote's demo page stacks its plans as cards on a phone and moves the form under the headline, and phones sent 94 of last month's 162 demo requests.
- tab_image_4 after: Pinlog's demo page stacks its plans as cards on a phone and moves the form under the headline, and phones sent 94 of last month's 162 demo requests.

## 20261012-mobile-landing-page-B-HUBRULES5lay-1 (P1, B-HUBRULES5lay, proposed)
- field: template
- caught by: B-HUBRULES5lay (Layer B): At 1440 px the default-open first FAQ panel is one line too short, so the end of the answer ("of a thumb.") is hidden. The 390 px render shows it in full.
- live text: It loads quickly on a cellular connection and keeps its main button within reach

## 20261012-mobile-landing-page-B-QCA1reusedpe-1 (P1, B-QCA1reusedpe, fix-by-writer, fixed)
- field: tab_content_2
- caught by: B-QCA1reusedpe (Layer B): "Brightway" is reused from consultation-form.
- live text: Brightway Solar's Facebook ad opens a qualifier with four questions, a question per screen

## 20261012-mobile-landing-page-B-QCA1reusedpe-2 (P1, B-QCA1reusedpe, fix-by-writer, fixed)
- field: tab_content_4
- caught by: B-QCA1reusedpe (Layer B): "Fieldnote" is reused in 4 other specs (affiliate-, b2b- and webinar-landing-page, file-upload-form), three of them in this hub.
- live text: On a laptop, Fieldnote's demo page shows its plans for inspection teams side by side in a pricing table.

## 20261012-mobile-landing-page-B-HUBRULES2a-1 (P2, B-HUBRULES2a, backlog)
- field: feature_3
- caught by: B-HUBRULES2a (Layer B): Calling a visitor who quits early "a lead" overstates it, since a partial answer set may hold no contact detail.
- live text: Answers save as they are tapped, and a visitor who quits early is a lead.
