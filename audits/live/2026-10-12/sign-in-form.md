# /ai-form-builder/sign-in-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-sign-in-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-sign-in-form-B-QCA1Divit202-1 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The testimonial strip credits quotes to stock AI persona names (Alex Rivera, Maya Chen, Jordan Patel) at made-up-sounding companies, identical on every hub page; if these are not real customers the quotes are fabricated.
- live text: We saved over $10K and built a functional MVP in just days... Alex Rivera, Founder, TaskFlow / Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founde...

## 20261012-sign-in-form-B-HUBRULES2apu-1 (P1, B-HUBRULES2apu, proposed)
- field: template
- caught by: B-HUBRULES2apu (Layer B): The third testimonial quote has no closing full stop, unlike the other two.
- live text: We tested our idea with real users early and used that feedback to avoid building features no one needed

## 20261012-sign-in-form-B-QCA1Divit202-2 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The AI CRM Builder card image in "More things you can build" draws the stock company name Acme Corp.
- live text: Lead / Proposal / Won ... AC Acme Corp $24,000 Proposal

## 20261012-sign-in-form-B-HUBRULES2bai-1 (P2, B-HUBRULES2bai, backlog)
- field: template
- caught by: B-HUBRULES2bai (Layer B): The pricing block uses AI-tell and hype phrasing (unlock, elegant, we've got you covered) and "we", which the child copy bans.
- live text: Choose the plan that fits your building ambitions. From weekend projects to enterprise applications, we've got you covered. ... Unlock all core platform feat...

## 20261012-sign-in-form-B-QCA1Divit202-3 (P1, B-QCA1Divit202, fix-by-writer, fixed)
- field: tab_content_1
- caught by: B-QCA1Divit202 (Layer B): The visitor's company is the stock name Northwind Freight, in the tab copy, the tab 1 image and its alt text (Northwind appears on 10 live pages).
- live text: Sam gets a Slack direct message at 2:04 PM naming her and Northwind Freight, and he walks out to meet her.
- feature_1 before: The questions a front desk needs Asks for the visitor's name and company, then the host from a dropdown list. The form stamps the time in, and a returning visitor's details fill in from their email address.
- feature_1 after: The questions a front desk needs Asks for the visitor's name, email, and company, then the host from a dropdown list. The form stamps the time in, and a returning visitor's details fill in from their email.
- share_image before: Build a sign in form for your lobby or job site, with Emergent
- share_image after: Build a sign in form for your lobby or job site, with Emergent
- tab_content_1 before: Sam Keller hears about his visitor in Slack Visitors at Fieldstone Architects sign in on a tablet in the lobby. Lena Ortiz types her name and company, picks Sam Keller from the host list, and taps Sign in. Sam gets a Slack direct message at 2:04 PM naming her and Northwind Freight, and he walks out to meet her.
- tab_content_1 after: Sam Loftus hears about his visitor in Slack Visitors at Fieldstone Architects sign in on a tablet in the lobby. Lena Marchetti types her name and company, picks Sam Loftus from the host list, and taps Sign in. Sam gets a Slack direct message at 2:04 PM naming her and Ludlow Freight, and he walks out to meet her.
- tab_content_3 before: Buyers without an agent make the follow-up list Linden Realty holds an open house at 18 Alder Lane on a Sunday afternoon. Each group signs in at the door and says whether they already work with an agent. In all, 14 groups came through, and the five with no agent reach listing agent Dana Whitfield by email at 5:00 PM.
- tab_content_3 after: Buyers without an agent make the follow-up list Mapleton Realty holds an open house at 18 Lennox Lane on a Sunday afternoon. Each group signs in at the door and says whether they already work with an agent. In all, 14 groups came through, and the five with no agent reach listing agent Dana Mercado by email at 5:00 PM.
- tab_image_1 before: A lobby tablet at Fieldstone Architects shows Lena Ortiz of Northwind Freight signing in to see Sam Keller, who gets a Slack direct message at 2:04 PM.
- tab_image_1 after: A lobby tablet at Fieldstone Architects shows Lena Marchetti of Ludlow Freight signing in to see Sam Loftus, who gets a Slack direct message at 2:04 PM.
- tab_image_3 before: An open house sign-in list at 18 Alder Lane shows 14 groups, and the 5 with no agent go to listing agent Dana Whitfield by email at 5:00 PM.
- tab_image_3 after: An open house sign-in list at 18 Lennox Lane shows 14 groups, and the 5 with no agent go to listing agent Dana Mercado by email at 5:00 PM.
- tab_image_4 before: A volunteer hours table for an animal rescue totals 312 hours across five volunteers this month and flags Jordan Lee's visit, open for 14 hours, for the coordinator to correct.
- tab_image_4 after: A volunteer hours table for an animal rescue totals 312 hours across five volunteers this month and flags Jordan Mosley's visit, open for 14 hours, for the coordinator to correct.

## 20261012-sign-in-form-B-QCA1Divit202-4 (P1, B-QCA1Divit202, fix-by-writer, fixed)
- field: tab_content_1
- caught by: B-QCA1Divit202 (Layer B): The visitor Lena Ortiz is a persona reused in 14 specs and live on task-automation and employee-information-form; also in the tab 1 image and alt.
- live text: Lena Ortiz types her name and company, picks Sam Keller from the host list, and taps Sign in.

## 20261012-sign-in-form-B-QCA1Divit202-5 (P1, B-QCA1Divit202, fix-by-writer, fixed)
- field: tab_content_3
- caught by: B-QCA1Divit202 (Layer B): The listing agent Dana Whitfield is reused in 14 specs and live on ecommerce-automation, booking-form and event-landing-page; "18 Alder Lane" is also live on feedback-form.
- live text: Linden Realty holds an open house at 18 Alder Lane ... reach listing agent Dana Whitfield by email at 5:00 PM.

## 20261012-sign-in-form-B-QCA1Divit202-6 (P1, B-QCA1Divit202, fix-by-writer, fixed)
- field: tab_image_4
- caught by: B-QCA1Divit202 (Layer B): The volunteer table reuses personas from other live pages: Ana Ruiz (25 specs, 3 other live pages), Jordan Lee (11 specs, live on job-application-form and t-shirt-order-form), Leo Grant (8 specs).
- live text: Ana Ruiz 12 64 / Mei Tan 11 58 / Leo Grant 13 71 / Jordan Lee 10 49 Open visit; alt "flags Jordan Lee's visit, open for 14 hours"

## 20261012-sign-in-form-B-HUBRULES2awr-1 (P1, B-HUBRULES2awr, fix-by-writer, fixed)
- field: feature_1
- caught by: B-HUBRULES2awr (Layer B): The form described asks for name, company and host only, then says returning visitors prefill from their email address, a field it never asks for.
- live text: Asks for the visitor's name and company, then the host ... a returning visitor's details fill in from their email address.

## 20261012-sign-in-form-B-HUBRULES5CON-1 (P2, B-HUBRULES5CON, backlog)
- field: feature_1
- caught by: B-HUBRULES5CON (Layer B): All six feature bodies open on a subjectless verb fragment: "Asks for", "Records the sign-out time", "Sends the host", "Shows everyone", "Totals each person's hours", "Exports the full sign-in app".
- live text: Asks for the visitor's name and company... / Records the sign-out time... / Sends the host... / Shows everyone... / Totals... / Exports...

## 20261012-sign-in-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: faq
- caught by: B-CONTENTDEFEC (Layer B): FAQ 9 states a soft generalization about gyms and climbing walls with no source.
- live text: Gyms and climbing walls often have guests sign a liability waiver form during the same visit.

## 20261012-sign-in-form-B-HUBRULES2ane-1 (P2, B-HUBRULES2ane, backlog)
- field: h1
- caught by: B-HUBRULES2ane (Layer B): The keyword form "sign in form" is used as an unhyphenated compound modifier throughout (H1, breadcrumb, FAQ), while the same page writes "sign-in record", "sign-in app" and the chip "Visitor Sign-In"; standard English is "sign-in form".
- live text: Build a Sign in Form That Tracks Who Comes and Goes / A sign in form records who arrived ... the core of any sign-in record
