# /ai-landing-page-builder/video-landing-page: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-video-landing-page-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-video-landing-page-B-QCA1Divit202-1 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The sitewide testimonial strip uses stock AI-style personas (Alex Rivera of TaskFlow, Maya Chen of BrightSuite, Jordan Patel of LoopDesk), repeated four times in the carousel on every child page.
- live text: We saved over $10K and built a functional MVP in just days... Alex Rivera, Founder, TaskFlow / Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founder, 

## 20261012-video-landing-page-B-QCA1Divit202-2 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The AI CRM Builder card image in the "More things you can build" section draws the stock company name "Acme Corp".
- live text: AI CRM Builder card image: "AC Acme Corp $24,000 Proposal"

## 20261012-video-landing-page-B-CONTENTDEFEC-1 (P1, B-CONTENTDEFEC, proposed)
- field: image_brief.tabs[3]
- caught by: B-CONTENTDEFEC (Layer B): The copy says Owen is messaged once Edda passes the one-minute mark of a two-minute video, but the drawn DM and step both report 1:24, so the alert fires 24 seconds late in the picture.
- live text: Copy: "Once she passes the one-minute mark, Owen gets a direct message" / Image: "Watched 1:24 of 2:00 so far"

## 20261012-video-landing-page-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: image_brief.tabs[3]
- caught by: B-CONTENTDEFEC (Layer B): The DM header carries a "#" channel glyph while the copy and mini card say a direct message to Owen only; the mockup also asks for a book-a-call button but the DM button reads "Open her page".
- live text: # Owen Castillo ... Direct message in Slack, Sent to Owen only ... Open her page

## 20261012-video-landing-page-B-QCA1reusedpe-1 (P2, B-QCA1reusedpe, backlog)
- field: tab_content_4
- caught by: B-QCA1reusedpe (Layer B): Quillfield Analytics is also the company in lead-capture-form tab 1 (not live yet); it will repeat across pages once that page ships.
- live text: Two minutes of video sit at the top of a page that Quillfield Analytics rep Owen Castillo made for one prospect

## 20261012-video-landing-page-B-HUBRULES2aco-1 (P2, B-HUBRULES2aco, backlog)
- field: howto_step_2_des
- caught by: B-HUBRULES2aco (Layer B): Step 2 says the call to action must work without playback, while tab 1, feature 3 and FAQ 3 hide the order button until a timestamp; the VSL exception is only explained in the FAQ.
- live text: Put the headline and the main call to action beside or under the video... The video adds proof; the page carries the ask.

## 20261012-video-landing-page-B-CONTENTDEFEC-3 (P2, B-CONTENTDEFEC, backlog)
- field: faq
- caught by: B-CONTENTDEFEC (Layer B): FAQ 9 opens on a fragment instead of a full answer sentence.
- live text: As long as its one job takes. A demo that shows a single task can finish in about a minute

## 20261012-video-landing-page-B-CONTENTDEFEC-4 (P2, B-CONTENTDEFEC, backlog)
- field: feature_6
- caught by: B-CONTENTDEFEC (Layer B): The feature 6 H3 is word for word the ebook landing page feature 6 H3.
- live text: Code you can take elsewhere
