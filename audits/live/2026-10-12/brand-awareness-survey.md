# /ai-survey-and-quiz-builder/brand-awareness-survey: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-brand-awareness-survey-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-brand-awareness-survey-B-QCA1Divit202-1 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The sitewide testimonial strip uses stock AI-style personas (Alex Rivera of TaskFlow, Maya Chen of BrightSuite, Jordan Patel of LoopDesk), repeated four times in the carousel on every child page.
- live text: We saved over $10K and built a functional MVP in just days... Alex Rivera, Founder, TaskFlow / Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founder, 

## 20261012-brand-awareness-survey-B-QCA1Divit202-2 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The AI CRM Builder card image in the "More things you can build" section draws the stock company name "Acme Corp".
- live text: AI CRM Builder card image: "AC Acme Corp $24,000 Proposal"

## 20261012-brand-awareness-survey-B-LEARNCAROUSE-1 (P1, B-LEARNCAROUSE, proposed)
- field: template
- caught by: B-LEARNCAROUSE (Layer B): The Learn list renders live on the survey template with three off-topic AI-model articles whose cards link to "#", although the section is meant to be hidden.
- live text: Explore more articles / 12 Best AI Tools for Nonprofits in 2026 / Haiku 5.5 vs Opus 5.5: Pricing, Benchmarks & Differences

## 20261012-brand-awareness-survey-B-QCA1Divit202-3 (P1, B-QCA1Divit202, fix-by-writer, fixed)
- field: tab_content_2
- caught by: B-QCA1Divit202 (Layer B): Fernway, the insurer whose recall is tracked, is also the company in tab 1 of the live pricing page.
- live text: In the Midwest, 6 of 150 named Fernway unprompted, and the regional manager got that number by email.
- tab_content_2 before: Four regions, one made-up insurer in the list Every quarter, 600 pet owners type every pet insurer they can name into a blank box. Only then do they see a list that hides Hollis Pet Cover, a made-up insurer, among the real ones. Thirty claimed to know it. In the Midwest, 6 of 150 named Fernway unprompted, and the regional manager got that number by email.
- tab_content_2 after: Four regions, one made-up insurer in the list Every quarter, 600 pet owners type every pet insurer they can name into a blank box. Only then do they see a list that hides Tarbell Pet Cover, a made-up insurer, among the real ones. Thirty claimed to know it. In the Midwest, 6 of 150 named Tillwick unprompted, and the regional manager got that number by email.
- tab_content_4 before: The logo without the name, in a new city Before the first truck rolls in Phoenix, 300 homeowners there see the Copperline Movers logo on their phones, name blurred, and type whose they think it is. Only 27 of the 300 named Copperline. In Tucson, its home city, 132 of 300 did. The first Phoenix mailers print the name in large type beside the logo.
- tab_content_4 after: The logo without the name, in a new city Before the first truck rolls in Phoenix, 300 homeowners there see the Selby Movers logo on their phones, name blurred, and type whose they think it is. Only 27 of the 300 named Selby. In Tucson, its home city, 132 of 300 did. The first Phoenix mailers print the name in large type beside the logo.
- tab_image_2 before: A quarterly recall table for Fernway shows unprompted and listed recall across four regions of 150 pet owners each, with the Midwest lowest at 6 unprompted, and 30 people ticking the made-up insurer Hollis.
- tab_image_2 after: A quarterly recall table for Tillwick shows unprompted and listed recall across four regions of 150 pet owners each, with the Midwest lowest at 6 unprompted, and 30 people ticking the made-up insurer Tarbell.
- tab_image_4 before: A phone survey shows Phoenix homeowners the Copperline Movers logo with the name blurred; 27 of 300 named the company, against 132 of 300 in Tucson.
- tab_image_4 after: A phone survey shows Phoenix homeowners the Selby Movers logo with the name blurred; 27 of 300 named the company, against 132 of 300 in Tucson.

## 20261012-brand-awareness-survey-B-QCA1Divit202-4 (P1, B-QCA1Divit202, fix-by-writer, fixed)
- field: tab_content_4
- caught by: B-QCA1Divit202 (Layer B): Copperline Movers reuses "Copperline", the company in tab 3 of the live event landing page.
- live text: Before the first truck rolls in Phoenix, 300 homeowners there see the Copperline Movers logo on their phones

## 20261012-brand-awareness-survey-B-CONTENTDEFEC-1 (P1, B-CONTENTDEFEC, proposed)
- field: image_brief.tabs[3]
- caught by: B-CONTENTDEFEC (Layer B): The copy runs the test in Phoenix before the first truck arrives, yet the drawn Phoenix respondent answers "Seen it on a truck"; the screen also asks about a logo that is not drawn.
- live text: Copy: "Before the first truck rolls in Phoenix" / Image: "Phoenix homeowners ... Seen it on a truck"

## 20261012-brand-awareness-survey-B-HUBRULES2apr-1 (P2, B-HUBRULES2apr, backlog)
- field: tab_content_3
- caught by: B-HUBRULES2apr (Layer B): The copy names search as the comparison point, but the image shows Friend or family second at 312 and search third at 276.
- live text: a home design podcast led with 384 of 1,200 answers, ahead of search at 276

## 20261012-brand-awareness-survey-B-HUBRULES2asa-1 (P2, B-HUBRULES2asa, backlog)
- field: feature_4
- caught by: B-HUBRULES2asa (Layer B): The survey cycle is called a "round" in features 4-6 and the FAQ but a "wave" in how-to steps 6 and 7.
- live text: stored against the market and the survey round / Run the next wave with the same wording

## 20261012-brand-awareness-survey-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: faq
- caught by: B-CONTENTDEFEC (Layer B): FAQ 1, 4 and 9 use soft quantifiers.
- live text: and often where they first heard of each one / usually the smaller number / quarterly fits most brands
