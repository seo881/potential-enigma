# /ai-form-builder/job-application-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-job-application-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-job-application-form-B-DECISIONS202-1 (P1, B-DECISIONS202, proposed)
- field: image_brief.tabs[0].main.blocks[0].title; images.cover_image.alt; image_brief.cover.alt
- caught by: B-DECISIONS202 (Layer B): The live uc-1 image and the cover alt use the stock placeholder company 'Northwind'; QC on the spec now fails at TOTAL 3.
- live text: Apply at Northwind Market / the confirmation screen a cashier sees after applying at Northwind Market

## 20261012-job-application-form-B-DECISIONS202-2 (P1, B-DECISIONS202, proposed)
- field: image_brief.tabs[0..3] (uc-1 to uc-4)
- caught by: B-DECISIONS202 (Layer B): The live images draw persona first names that recur across the hub: Dana Ruiz (Dana on 79 other specs), Priya Shah (50), Lena Fox (44), Tom Baker (35), Jordan Lee (33), Maya Ortiz (28), Leo Park (22), Grace Liu (20), Ben Walsh (19), Omar Haddad (16). 'Elm Street' is on 9 other specs, and Jordan and 
- live text: Maya Ortiz applied / To Leo Park / Ben Walsh, RN / Dana Ruiz / To Priya Shah / Jordan Lee has a final interview / Lena Fox / Tom Baker

## 20261012-job-application-form-B-DECISIONS202-3 (P1, B-DECISIONS202, proposed)
- field: template
- caught by: B-DECISIONS202 (Layer B): The shared 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp' on every page; this sits outside the child collections, so it needs Divit.
- live text: AI CRM Builder card: AC Acme Corp $24,000 Proposal

## 20261012-job-application-form-B-DECISIONS202-4 (P1, B-DECISIONS202, proposed)
- field: template
- caught by: B-DECISIONS202 (Layer B): The template testimonials use generic persona names and companies (Maya Chen of BrightSuite, Jordan Patel of LoopDesk, Alex Rivera of TaskFlow); if they are not real customers they read as stock personas, and the first names recur across the child pages' images. Needs Divit to confirm they are real.
- live text: Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founder, LoopDesk / Alex Rivera, Founder, TaskFlow

## 20261012-job-application-form-A1-1 (P1, A1, fix-by-writer, fixed)
- field: image_brief
- caught by: A1 (Layer sweep): stock company names live (QC A1, Divit 2026-10-12 ruling)
- cover_image before: Job application form: the confirmation screen a cashier sees after applying at Northwind Market
- cover_image after: Job application form: the confirmation screen a cashier sees after applying at Ollerton Market
- feature_4 before: A filled PDF of every application Keep each application as a filled PDF laid out like your paper form, typed signature included, for the personnel file. Name each file by applicant and role, like Haddad_RN.pdf.
- feature_4 after: A filled PDF of every application Keep each application as a filled PDF laid out like your paper form, typed signature included, for the personnel file. Name each file by applicant and role, like Oduro_RN.pdf.
- share_image before: Build a job application form you own, with Emergent
- share_image after: Build a job application form you own, with Emergent
- tab_image_1 before: An hourly job application asks for a store, a start date and the shifts the applicant can work, then messages that store's manager in Slack and saves the applicant with weekend availability.
- tab_image_1 after: An hourly job application asks for a store, a start date and the shifts the applicant can work, then messages that store's manager in Slack and saves the applicant with weekend availability.
- tab_image_2 before: A clinical job application table lists nurses and a medical assistant with their credential expiry dates and flags one RN whose license expires within 60 days for the recruiter.
- tab_image_2 after: A clinical job application table lists nurses and a medical assistant with their credential expiry dates and flags one RN whose license expires within 60 days for the recruiter.
- tab_image_3 before: An internal job application checks tenure before submit, 18 months in role against a 12-month minimum, keeps the application confidential, and messages the employee's current manager in Slack only once a final interview is booked.
- tab_image_3 after: An internal job application checks tenure before submit, 18 months in role against a 12-month minimum, keeps the application confidential and messages the employee's current manager in Slack only once a final interview is booked.
- tab_image_4 before: Product designer applications are sorted by must-haves: three who are authorized and within the posted band go to the design hiring channel in Slack, and one without work authorization goes to the hold list.
- tab_image_4 after: Product designer applications are sorted by must-haves: three who are authorized and within the posted band go to the design hiring channel in Slack, and one without work authorization goes to the hold list.
