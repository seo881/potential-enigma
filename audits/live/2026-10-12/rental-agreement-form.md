# /ai-form-builder/rental-agreement-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-rental-agreement-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-rental-agreement-form-B-QCA1Divit202-1 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The testimonial strip credits quotes to stock AI persona names (Alex Rivera, Maya Chen, Jordan Patel) at made-up-sounding companies, identical on every hub page; if these are not real customers the quotes are fabricated.
- live text: We saved over $10K and built a functional MVP in just days... Alex Rivera, Founder, TaskFlow / Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founde...

## 20261012-rental-agreement-form-B-HUBRULES2apu-1 (P1, B-HUBRULES2apu, proposed)
- field: template
- caught by: B-HUBRULES2apu (Layer B): The third testimonial quote has no closing full stop, unlike the other two.
- live text: We tested our idea with real users early and used that feedback to avoid building features no one needed

## 20261012-rental-agreement-form-B-QCA1Divit202-2 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The AI CRM Builder card image in "More things you can build" draws the stock company name Acme Corp.
- live text: Lead / Proposal / Won ... AC Acme Corp $24,000 Proposal

## 20261012-rental-agreement-form-B-HUBRULES2bai-1 (P2, B-HUBRULES2bai, backlog)
- field: template
- caught by: B-HUBRULES2bai (Layer B): The pricing block uses AI-tell and hype phrasing (unlock, elegant, we've got you covered) and "we", which the child copy bans.
- live text: Choose the plan that fits your building ambitions. From weekend projects to enterprise applications, we've got you covered. ... Unlock all core platform feat...

## 20261012-rental-agreement-form-B-HUBRULES2awr-1 (P1, B-HUBRULES2awr, fix-by-writer, fixed)
- field: feature_2
- caught by: B-HUBRULES2awr (Layer B): The feature names three follow-up questions (breed, weight, plate number) and then says "those two questions".
- live text: A tenant who says they have a dog is asked its breed and weight. ... Everyone else never sees those two questions.
- feature_2 before: Follow-up questions where they apply A tenant who says they have a dog is asked its breed and weight. One who parks on site gives a plate number for the permit. Everyone else never sees those two questions.
- feature_2 after: Follow-up questions where they apply A tenant who says they have a dog is asked its breed and weight. One who parks on site gives a plate number for the permit. Anyone with no pet and no car never sees them.
- howto_step_1_des before: Write down what stays the same for every tenant at this property, from the rent figure to who fixes a leaking tap. These become fixed text in the agreement, and no tenant can edit them when they fill in the form.
- howto_step_1_des after: Write down what stays the same for every tenant at this property, from the rent figure to who fixes a leaking faucet. These become fixed text in the agreement, and no tenant can edit them when they fill in the form.

## 20261012-rental-agreement-form-B-QCHUSspellin-1 (P1, B-QCHUSspellin, fix-by-writer, fixed)
- field: howto_step_1_des
- caught by: B-QCHUSspellin (Layer B): "tap" is the British word for the fixture; the page is US English (faucet). Flagged in review notes twice and still live.
- live text: from the rent figure to who fixes a leaking tap.

## 20261012-rental-agreement-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: faq
- caught by: B-CONTENTDEFEC (Layer B): FAQ 3 (free rental agreement form) and FAQ 4 (free lease agreement form) give the same answer with the words swapped.
- live text: County housing offices and state agencies publish free rental agreement forms as PDFs... / State and city agencies post free ones.

## 20261012-rental-agreement-form-B-HUBRULES8-1 (P2, B-HUBRULES8, backlog)
- field: faq
- caught by: B-HUBRULES8 (Layer B): FAQ 3 says county housing offices publish free rental agreement forms; only the Oklahoma state PDF is in domain_sources (true per the top 10, e.g. kitsap.gov, but unrecorded).
- live text: County housing offices and state agencies publish free rental agreement forms as PDFs you print and fill by hand.

## 20261012-rental-agreement-form-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: tab_image_1
- caught by: B-CONTENTDEFEC (Layer B): The tab 1 image draws a house rule (No smoking indoors) the tab copy never names.
- live text: House rules: Quiet after 10 pm / Guests: 3 nights max / Rent $950, due the 1st / No smoking indoors

## 20261012-rental-agreement-form-B-CONTENTDEFEC-3 (P2, B-CONTENTDEFEC, backlog)
- field: tab_image_3
- caught by: B-CONTENTDEFEC (Layer B): The image adds a landlord countersignature after the roommates, while the copy calls the lease final once the last roommate signs.
- live text: Copies to all three, After the last signature / Landlord countersigns after all three

## 20261012-rental-agreement-form-B-HUBRULES2b-1 (P2, B-HUBRULES2b, backlog)
- field: why_description
- caught by: B-HUBRULES2b (Layer B): "ends at the blank page" is unclear: a template starts with blanks, so the intended contrast does not land.
- live text: A downloaded template ends at the blank page, and each signed copy still gets typed into your records by hand.

## 20261012-rental-agreement-form-B-HUBRULES2b-2 (P2, B-HUBRULES2b, backlog)
- field: feature_6
- caught by: B-HUBRULES2b (Layer B): Same "included and billed in credits" formula as the order and registration pages.
- live text: Publish the form on a custom domain, included and billed in credits, or link it from a listing.
