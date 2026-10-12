# /ai-form-builder/booking-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-booking-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-booking-form-B-QCA1AItellsr-1 (P1, B-QCA1AItellsr, proposed)
- field: image_brief
- caught by: B-QCA1AItellsr (Layer B): Meeting Rooms image (uc-4.svg) draws member Dana Whitfield twice; the persona is reused on 13 other specs (contact-form, payment-form, nda-form, ...). Re-render after renaming.
- live text: Member: Dana Whitfield | Room B for Dana Whitfield

## 20261012-booking-form-B-QCA1AItellsr-2 (P1, B-QCA1AItellsr, fix-by-writer, fixed)
- field: tab_content_2
- caught by: B-QCA1AItellsr (Layer B): Brightline is reused on 15 other specs and is also a real US rail brand (earlier review note).
- live text: Brightline Appliance Repair has three vans and caps each 4-hour arrival window at three jobs.
- mockup before: window.awbMockup = { equipmentRentals: "I run Foundry Makerspace. Build a booking form for our laser cutter in 2-hour blocks. Members enter their member number first. Check it against our training records, and show open blocks only to members who have the laser safety course on file. Anyone without it should see the next class date and a sign-up link instead.", repairVisits: "My appliance repair company, Brightline, has three vans. Build a booking form with 4-hour arrival windows that each take 
- mockup after: window.awbMockup = { equipmentRentals: "I run Foundry Makerspace. Build a booking form for our laser cutter in 2-hour blocks. Members enter their member number first. Check it against our training records, and show open blocks only to members who have the laser safety course on file. Anyone without it should see the next class date and a sign-up link instead.", repairVisits: "My appliance repair company, Crandall, has three vans. Build a booking form with 4-hour arrival windows that each take at
- share_image before: Build a booking form that only offers open times, with Emergent
- share_image after: Build a booking form that only offers open times, with Emergent
- tab_content_2 before: Up to three jobs in every arrival window Brightline Appliance Repair has three vans and caps each 4-hour arrival window at three jobs. Customers enter a ZIP code and the appliance, then choose a window with room left. Full windows drop off the form. Addresses outside the 14 ZIP codes Brightline covers get the office phone number instead of a slot.
- tab_content_2 after: Up to three jobs in every arrival window Crandall Appliance Repair has three vans and caps each 4-hour arrival window at three jobs. Customers enter a ZIP code and the appliance, then choose a window with room left. Full windows drop off the form. Addresses outside the 14 ZIP codes Crandall covers get the office phone number instead of a slot.
- tab_content_4 before: The 11th room hour shows its $25 price first Every desk at Harbor Street Commons comes with 10 meeting-room hours a month. Each room request shows the member how many of those hours are left. Time past the allowance is priced at $25 an hour before the member confirms, and it goes on their account for the month.
- tab_content_4 after: The 11th room hour shows its $25 price first Every desk at Dellaway Commons comes with 10 meeting-room hours a month. Each room request shows the member how many of those hours are left. Time past the allowance is priced at $25 an hour before the member confirms, and it goes on their account for the month.
- tab_image_2 before: Brightline Appliance Repair's arrival windows show one 4-hour window full at 3 of 3 jobs and hidden, and a dryer repair booked into the Thursday 12 to 4 PM window inside the 14 ZIP codes the 3 vans cover.
- tab_image_2 after: Crandall Appliance Repair's arrival windows show one 4-hour window full at 3 of 3 jobs and hidden, and a dryer repair booked into the Thursday 12 to 4 PM window inside the 14 ZIP codes the 3 vans cover.
- tab_image_3 before: A Wren Hollow Photography client books a Saturday family session by paying a $150 deposit through Stripe, with the $450 balance of the $600 session emailed 7 days before the shoot.
- tab_image_3 after: A Wren Hollow Photography client books a Saturday family session by paying a $150 deposit through Stripe, with the $450 balance of the $600 session emailed 7 days before the shoot.
- tab_image_4 before: A Harbor Street Commons member with 1 of 10 included room hours left requests 2 hours, and the form prices hour 11 at $25 before the member confirms.
- tab_image_4 after: A Dellaway Commons member with 1 of 10 included room hours left requests 2 hours, and the form prices hour 11 at $25 before the member confirms.

## 20261012-booking-form-B-QCA1AItellsr-3 (P1, B-QCA1AItellsr, fix-by-writer, fixed)
- field: tab_image_2
- caught by: B-QCA1AItellsr (Layer B): Brightline in the tab 2 alt; the image_brief heading 'Brightline windows' draws it in uc-2.svg too.
- live text: Brightline Appliance Repair's arrival windows show one 4-hour window full at 3 of 3 jobs and hidden

## 20261012-booking-form-B-QCA1AItellsr-4 (P1, B-QCA1AItellsr, proposed)
- field: mockup
- caught by: B-QCA1AItellsr (Layer B): Brightline in the repairVisits mockup prompt.
- live text: My appliance repair company, Brightline, has three vans.

## 20261012-booking-form-B-HUBRULES5lib-1 (P2, B-HUBRULES5lib, backlog)
- field: why_table
- caught by: B-HUBRULES5lib (Layer B): Google Forms 'Where responses live: Google Sheets' simplifies: responses are stored in the form, and a linked Sheet is optional. Library cell approved 2026-09-28, so Divit's call.
- live text: Where responses live | ... | Google Sheets

## 20261012-booking-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: faq#5
- caught by: B-CONTENTDEFEC (Layer B): The question compares reservation and booking forms, but the answer's contrast is reservation vs appointment form, so the reader never learns where 'booking form' sits.
- live text: A reservation form counts down a fixed stock of seats or rooms until none are left. An appointment form treats each hour of one person's time

## 20261012-booking-form-B-HUBRULES5-1 (P2, B-HUBRULES5, backlog)
- field: faq#3
- caught by: B-HUBRULES5 (Layer B): Question kept in headline form; light grammar edits to PAA questions are allowed.
- live text: How to write a reservation form?

## 20261012-booking-form-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: faq#4
- caught by: B-CONTENTDEFEC (Layer B): Soft quantifiers about unnamed third parties: 'Most booking forms' (faq#4) and 'most cost nothing to copy' (faq#8).
- live text: Most booking forms take a few short screens on a phone.

## 20261012-booking-form-B-HUBRULES1Num-1 (P2, B-HUBRULES1Num, backlog)
- field: tab_content_3
- caught by: B-HUBRULES1Num (Layer B): Duration spelled out; numerals for all durations (the alt already says 7 days).
- live text: the remaining $450 is requested by email seven days before the shoot.
