# /ai-form-builder/interest-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-interest-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-interest-form-B-DECISIONS202-1 (P1, B-DECISIONS202, proposed)
- field: image_brief.tabs[2].main.blocks[1].items
- caught by: B-DECISIONS202 (Layer B): The live uc-3 image reuses persona names from other pages: 'Dana Kim' (also on training-request-form and grievance-form; 'Dana' is on 79 other specs) and 'Luis Ortega' (on 5 other specs).
- live text: Dana Kim, Two bedrooms, move-in April / Luis Ortega, Two bedrooms, move-in May

## 20261012-interest-form-B-DECISIONS202-2 (P1, B-DECISIONS202, proposed)
- field: tab_content_1, tab_content_2, tab_content_4 (and matching image_brief/alt)
- caught by: B-DECISIONS202 (Layer B): The example businesses are recurring fictional names used across the hub: Fernhill (15 other specs), Brightwater (10), Pine Hollow (5).
- live text: Fernhill Community College has a woodshop... / Pine Hollow Youth Lacrosse sets its teams... / Brightwater Logistics is starting a mentoring program

## 20261012-interest-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: image_brief.tabs[0].kpi.sub
- caught by: B-CONTENTDEFEC (Layer B): The image shortens the copy's 'Fernhill Community College' to 'Fernhill College'.
- live text: Replies 23 Fernhill College

## 20261012-interest-form-B-HUBRULES5lin-1 (P2, B-HUBRULES5lin, backlog)
- field: faq (item 6)
- caught by: B-HUBRULES5lin (Layer B): The last sentence exists to carry a sibling link and shifts to brands and creators, which no other part of the answer or page addresses.
- live text: Brands gauge creator demand before a creator application goes public.

## 20261012-interest-form-B-HUBRULES5moc-1 (P2, B-HUBRULES5moc, backlog)
- field: mockup
- caught by: B-HUBRULES5moc (Layer B): Tab 4 is labelled 'Staff Mentoring' but its mockup key is workplaceMentoring (the template appears to map keys by position, so nothing visibly breaks).
- live text: workplaceMentoring: "I work in HR at a logistics company...

## 20261012-interest-form-B-HUBRULES5com-1 (P2, B-HUBRULES5com, backlog)
- field: why_table
- caught by: B-HUBRULES5com (Layer B): Typeform is in the table but not in the page's top 10, while Microsoft Forms (#7) is left out.
- live text: Google Forms | Jotform | Typeform

## 20261012-interest-form-B-DECISIONS202-3 (P1, B-DECISIONS202, proposed)
- field: template
- caught by: B-DECISIONS202 (Layer B): The shared 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp' on every page; this sits outside the child collections, so it needs Divit.
- live text: AI CRM Builder card: AC Acme Corp $24,000 Proposal

## 20261012-interest-form-B-DECISIONS202-4 (P1, B-DECISIONS202, proposed)
- field: template
- caught by: B-DECISIONS202 (Layer B): The template testimonials use generic persona names and companies (Maya Chen of BrightSuite, Jordan Patel of LoopDesk, Alex Rivera of TaskFlow); if they are not real customers they read as stock personas, and the first names recur across the child pages' images. Needs Divit to confirm they are real.
- live text: Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founder, LoopDesk / Alex Rivera, Founder, TaskFlow
