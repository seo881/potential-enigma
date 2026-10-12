# /ai-form-builder/liability-waiver-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-liability-waiver-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-liability-waiver-form-B-DECISIONS202-1 (P1, B-DECISIONS202, proposed)
- field: image_brief.tabs[0], image_brief.tabs[2] (uc-1, uc-3)
- caught by: B-DECISIONS202 (Layer B): The live images reuse persona first names that recur across the hub: Dana Kerrigan (Dana on 79 other specs), Maya Singh (28), Owen Stroud (21), Ava Kerrigan (17).
- live text: Signed by Dana Kerrigan for Ava / Cyrus, Maya and Owen are cleared

## 20261012-liability-waiver-form-B-HUBRULES8aso-1 (P1, B-HUBRULES8aso, fix-by-writer, fixed)
- field: howto_step_7_des
- caught by: B-HUBRULES8aso (Layer B): The legal source (Rocket Lawyer) says a waiver can fail when its language is vague; the copy turns that into a frequency claim ('a common reason') that the source does not make.
- live text: Vague language is a common reason waivers fail.
- faq before: window.awbFAQ = {"heading": "Liability Waiver Questions, Answered", "items": [{"q": "What is a liability waiver form?", "a": "A liability waiver form is a document a participant signs before an activity to accept its risks and give up certain claims against the organizer. It is also called a liability release form. At its core it pairs a description of the hazards with a signed release."}, {"q": "How do I create a liability waiver form?", "a": "Start by writing down the activity and its hazards 
- faq after: window.awbFAQ = {"heading": "Liability Waiver Questions, Answered", "items": [{"q": "What is a liability waiver form?", "a": "A liability waiver form is a document a participant signs before an activity to accept its risks and give up certain claims against the organizer. It is also called a liability release form. At its core it pairs a description of the hazards with a signed release."}, {"q": "How do I create a liability waiver form?", "a": "Start by writing down the activity and its hazards 
- howto_step_7_des before: Vague language is a common reason waivers fail. Ask an attorney to review the text before the first real participant sees it. Then sign it yourself as a made-up participant, open the PDF and check every initials box came through.
- howto_step_7_des after: Vague language is one reason a court can refuse to enforce a waiver. Ask an attorney to review the text before the first real participant sees it. Then sign it yourself as a made-up participant, open the PDF, and check every initials box came through.

## 20261012-liability-waiver-form-B-HUBRULES8-1 (P2, B-HUBRULES8, backlog)
- field: faq (item 4)
- caught by: B-HUBRULES8 (Layer B): The source says notarization can add a layer of protection; the reason given ('easier to prove if someone later disputes it') is not in the source.
- live text: A notary can still add protection, because it makes the signature easier to prove if someone later disputes it.

## 20261012-liability-waiver-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: image_brief.tabs[3] (uc-4)
- caught by: B-CONTENTDEFEC (Layer B): The copy says any contractor within 30 days of expiry gets an email, but the image shows Ironvale Plumbing at 26 days with no request sent; only Thornbury Electric's request is drawn.
- live text: Ironvale Plumbing, Plumbing, 26 days

## 20261012-liability-waiver-form-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: features_subheading
- caught by: B-CONTENTDEFEC (Layer B): The intro promises six parts a signed waiver depends on, but feature 6 (custom domain and code export) is not part of a waiver.
- live text: Six parts every signed waiver depends on: the clauses, the people who sign and the record you keep afterward.

## 20261012-liability-waiver-form-B-DECISIONS202-2 (P1, B-DECISIONS202, proposed)
- field: template
- caught by: B-DECISIONS202 (Layer B): The shared 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp' on every page; this sits outside the child collections, so it needs Divit.
- live text: AI CRM Builder card: AC Acme Corp $24,000 Proposal

## 20261012-liability-waiver-form-B-DECISIONS202-3 (P1, B-DECISIONS202, proposed)
- field: template
- caught by: B-DECISIONS202 (Layer B): The template testimonials use generic persona names and companies (Maya Chen of BrightSuite, Jordan Patel of LoopDesk, Alex Rivera of TaskFlow); if they are not real customers they read as stock personas, and the first names recur across the child pages' images. Needs Divit to confirm they are real.
- live text: Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founder, LoopDesk / Alex Rivera, Founder, TaskFlow
