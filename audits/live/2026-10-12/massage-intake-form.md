# /ai-form-builder/massage-intake-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-massage-intake-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-massage-intake-form-B-DECISIONS202-1 (P1, B-DECISIONS202, proposed)
- field: tab_content_4; image_brief.tabs[3].main.blocks[0].text; plan.openers[3]
- caught by: B-DECISIONS202 (Layer B): The live tab copy and the uc-4 image use the stock placeholder company 'Globex'; QC on the spec now fails at TOTAL 2.
- live text: On the Globex wellness day, employees scan a QR code at the break room door and answer three screening questions on their phones.

## 20261012-massage-intake-form-B-DECISIONS202-2 (P1, B-DECISIONS202, proposed)
- field: tab_content_2; images.tab_image_2.alt; image_brief.tabs[0..3]
- caught by: B-DECISIONS202 (Layer B): The live copy and images reuse names that recur across the hub: Dana Ellis in tab 2's copy and alt (Dana on 79 other specs), Sam Okafor and Sam Ortiz drawn on the same page (Sam on 51 specs), Grace Tully (20), Mia Porter (15), Chris Vale (8). The businesses Juniper (18 other specs) and Kestrel (13) 
- live text: A guest at 24 weeks moves from the open Swedish booking to Dana Ellis, who is trained in prenatal massage.

## 20261012-massage-intake-form-B-HUBRULES2agr-1 (P1, B-HUBRULES2agr, fix-by-writer, fixed)
- field: features_subheading
- caught by: B-HUBRULES2agr (Layer B): 'Each one' has no antecedent under the H2, and 'your therapist' addresses a spa owner, while the page speaks to therapists themselves (solo practitioners included).
- live text: Each one answers a question your therapist would otherwise ask with the client already on the table.
- features_subheading before: Each one answers a question your therapist would otherwise ask with the client already on the table.
- features_subheading after: Each of these six parts answers a question you would otherwise ask with the client already on the table.
- share_image before: Build a massage intake form that acts on answers, with Emergent
- share_image after: Build a massage intake form that acts on answers, with Emergent
- tab_content_4 before: Each signed form takes the next 15-minute chair slot On the Globex wellness day, employees scan a QR code at the break room door and answer three screening questions on their phones. Each signed form takes the next open 15-minute slot. Hana Kim works down the list on a tablet, with each person's areas to avoid beside their name.
- tab_content_4 after: Each signed form takes the next 15-minute chair slot On the Kinloch wellness day, employees scan a QR code at the break room door and answer three screening questions on their phones. Each signed form takes the next open 15-minute slot. Hana Kim works down the list on a tablet, with each person's areas to avoid beside their name.
- tab_image_4 before: An employee signs a chair massage intake on a phone after three screening questions and takes the next open 15-minute slot, which appears on the therapist's tablet list with the areas to avoid.
- tab_image_4 after: An employee signs a chair massage intake on a phone after three screening questions and takes the next open 15-minute slot, which appears on the therapist's tablet list with the areas to avoid.

## 20261012-massage-intake-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: image_brief.tabs[2].hero; image_brief.cover
- caught by: B-CONTENTDEFEC (Layer B): The Slack card to Owen Tate draws a channel '#' glyph, so a message to one therapist reads as a channel named after him.
- live text: # Owen Tate · Emergent APP · Call Grace Tully before her session

## 20261012-massage-intake-form-B-DECISIONS202-3 (P1, B-DECISIONS202, proposed)
- field: template
- caught by: B-DECISIONS202 (Layer B): The shared 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp' on every page; this sits outside the child collections, so it needs Divit.
- live text: AI CRM Builder card: AC Acme Corp $24,000 Proposal

## 20261012-massage-intake-form-B-DECISIONS202-4 (P1, B-DECISIONS202, proposed)
- field: template
- caught by: B-DECISIONS202 (Layer B): The template testimonials use generic persona names and companies (Maya Chen of BrightSuite, Jordan Patel of LoopDesk, Alex Rivera of TaskFlow); if they are not real customers they read as stock personas, and the first names recur across the child pages' images. Needs Divit to confirm they are real.
- live text: Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founder, LoopDesk / Alex Rivera, Founder, TaskFlow
