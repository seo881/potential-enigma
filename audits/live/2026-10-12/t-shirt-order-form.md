# /ai-form-builder/t-shirt-order-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-t-shirt-order-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-t-shirt-order-form-B-HUBRULES2bQC-1 (P1, B-HUBRULES2bQC, fix-by-writer, fixed)
- field: tab_content_4
- caught by: B-HUBRULES2bQC (Layer B): Stock placeholder company name Northwind in the New Hire Kits tab copy.
- live text: New hires at Northwind get a welcome kit link with their offer letter.
- mockup before: window.awbMockup = { schoolSpiritWear: "I run the PTO at Lincoln Middle School and we sell spirit shirts: youth sizes at $15 and adult sizes at $18. Build an order form where parents pick a size and quantity, enter the student's homeroom and pay by card. Close it Friday at 3 pm, email Bayside Printing one count per size, and give me a handout list grouped by homeroom.", reunionShirts: "I'm organizing the Delgado family reunion and 41 relatives are coming. Build a shirt order form with navy or he
- mockup after: window.awbMockup = { schoolSpiritWear: "I run the PTO at Lincoln Middle School and we sell spirit shirts: youth sizes at $15 and adult sizes at $18. Build an order form where parents pick a size and quantity, enter the student's homeroom and pay by card. Close it Friday at 3 pm, email Bayside Printing one count per size, and give me a handout list grouped by homeroom.", reunionShirts: "I'm organizing the Delgado family reunion and 41 relatives are coming. Build a shirt order form with navy or he
- share_image before: Build a T-shirt order form that counts every size, with Emergent
- share_image after: Build a T-shirt order form that counts every size, with Emergent
- tab_content_4 before: Welcome shirts ship in the right size New hires at Northwind get a welcome kit link with their offer letter. Each picks a size, a classic or relaxed fit, and confirms a shipping address. Nobody pays. Every Monday the fulfillment vendor receives the week's list as a CSV, and the people team gets a Slack message naming anyone who has not answered.
- tab_content_4 after: Welcome shirts ship in the right size New hires at Merrick Robotics get a welcome kit link with their offer letter. Each picks a size, a classic or relaxed fit, and confirms a shipping address. Nobody pays. Every Monday the fulfillment vendor receives the week's list as a CSV, and the people team gets a Slack message naming anyone who has not answered.
- tab_image_4 before: A new hire picks a medium relaxed-fit shirt and a shipping address on a welcome kit form, and the people team's Slack channel shows the Monday list sent to the fulfillment vendor with two new hires still to answer.
- tab_image_4 after: A new hire picks a medium relaxed-fit shirt and a shipping address on a welcome kit form, and the people team's Slack channel shows the Monday list sent to the fulfillment vendor with two new hires still to answer.

## 20261012-t-shirt-order-form-B-HUBRULES2bQC-2 (P1, B-HUBRULES2bQC, proposed)
- field: mockup
- caught by: B-HUBRULES2bQC (Layer B): Stock placeholder name Northwind in the newHireKits mockup prompt.
- live text: My people team at Northwind sends new hires a welcome kit.

## 20261012-t-shirt-order-form-B-HUBRULES2bQC-3 (P1, B-HUBRULES2bQC, proposed)
- field: image_brief.tabs[3].main.blocks[0].title
- caught by: B-HUBRULES2bQC (Layer B): Northwind is drawn in the tab 4 image (form title); re-render after the rename.
- live text: Northwind

## 20261012-t-shirt-order-form-B-HUBRULES2bre-1 (P1, B-HUBRULES2bre, proposed)
- field: image_brief.tabs[3].hero.blocks[1].text
- caught by: B-HUBRULES2bre (Layer B): Reused persona names drawn in the tab 4 image: Jordan Lee appears in 10 other specs, Sam Patel in 4.
- live text: Not answered yet: Jordan Lee, Sam Patel

## 20261012-t-shirt-order-form-B-HUBRULES2bre-2 (P1, B-HUBRULES2bre, proposed)
- field: image_brief.tabs[1].hero.blocks[0].sub
- caught by: B-HUBRULES2bre (Layer B): Rosa Delgado is drawn in the tab 2 image and is reused in 5 other specs.
- live text: Rosa Delgado, navy, size L

## 20261012-t-shirt-order-form-B-HUBRULES2bre-3 (P2, B-HUBRULES2bre, backlog)
- field: image_brief.tabs[2].main.blocks[1].rows
- caught by: B-HUBRULES2bre (Layer B): Captain names in the tab 3 image recur on other pages (M. Chen 4 specs, J. Alvarez 4, L. Brandt 2); 14 Elm Street in tab 4 recurs in 9 specs.
- live text: M. Chen | L. Brandt | J. Alvarez | 14 Elm Street, Apt 3

## 20261012-t-shirt-order-form-B-HUBRULES5FAQ-1 (P2, B-HUBRULES5FAQ, backlog)
- field: faq
- caught by: B-HUBRULES5FAQ (Layer B): FAQ 10 ends on a sentence about race entries that does not answer whether the forms are free; it exists to carry the registration form link.
- live text: When the shirt comes with a race entry, ask for the size on the registration form instead of a separate one.

## 20261012-t-shirt-order-form-B-HUBRULES2are-1 (P2, B-HUBRULES2are, backlog)
- field: tab_content_2
- caught by: B-HUBRULES2are (Layer B): Tab 2 H3 drops the article: 'a name on back'.
- live text: Printing a name on back adds $5

## 20261012-t-shirt-order-form-B-layoutat390p-1 (P2, B-layoutat390p, backlog)
- field: faq
- caught by: B-layoutat390p (Layer B): At 390 px FAQ questions 5 and 7 break the line inside 'T-shirt' at the hyphen ('T-' / 'shirt').
- live text: How do I count sizes from T- / shirt order forms? | How do I make an editable T- / shirt order form template?

## 20261012-t-shirt-order-form-B-HUBRULES2bQC-4 (P1, B-HUBRULES2bQC, proposed)
- field: template
- caught by: B-HUBRULES2bQC (Layer B): The 'More things you can build' carousel's AI CRM Builder card draws the stock name Acme Corp (hub cover asset outside the four hubs' collections).
- live text: Acme Corp $24,000 Proposal

## 20261012-t-shirt-order-form-B-HUBRULES2bre-4 (P2, B-HUBRULES2bre, backlog)
- field: template
- caught by: B-HUBRULES2bre (Layer B): Sitewide testimonial strip uses generic placeholder personas (Alex Rivera, Maya Chen, Jordan Patel) with invented companies, repeated 4 times in the DOM.
- live text: Alex Rivera Founder, TaskFlow | Maya Chen Product Lead, BrightSuite | Jordan Patel Co-founder, LoopDesk
