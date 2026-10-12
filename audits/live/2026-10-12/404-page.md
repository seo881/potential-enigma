# /ai-landing-page-builder/404-page: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-404-page-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-404-page-B-HUBRULES2bQC-1 (P1, B-HUBRULES2bQC, fix-by-writer, fixed)
- field: tab_content_1
- caught by: B-HUBRULES2bQC (Layer B): Stock placeholder name Northwind in the Online Store tab copy (visible on load).
- live text: A shopper who follows an old link to Northwind's retired linen camp shirt lands on a page that keeps the store open.
- share_image before: Build a 404 page that finds the next page, with Emergent
- share_image after: Build a 404 page that finds the next page, with Emergent
- tab_content_1 before: A dead product link that still sells A shopper who follows an old link to Northwind's retired linen camp shirt lands on a page that keeps the store open. Search sits at the top, with the store's bestsellers below it and an add-to-cart button on each. An add from the error page is saved with the missed URL attached.
- tab_content_1 after: A dead product link that still sells A shopper who follows an old link to Ostlund's retired linen camp shirt lands on a page that keeps the store open. Search sits at the top, with the store's bestsellers below it and an add-to-cart button on each. An add from the error page is saved with the missed URL attached.
- tab_content_2 before: Search seeded from the broken URL Acme's API docs collect mistyped links from forum posts and old emails. When /docs/api/webhoks misses, the 404 splits the path into words and searches the docs. The closest article comes first: Webhooks: retries and signatures. A link to the docs home and a support email sit under the result.
- tab_content_2 after: Search seeded from the broken URL Nettlepay's API docs collect mistyped links from forum posts and old emails. When /docs/api/webhoks misses, the 404 splits the path into words and searches the docs. The closest article comes first: Webhooks: retries and signatures. A link to the docs home and a support email sit under the result.
- tab_content_4 before: Which old URLs need a redirect this week Site migrations leave old addresses alive in newsletters and other people's posts. After Globex moved its marketing site, each 404 hit lands in a table with the URL, the referrer, and a seven-day count. Every Monday, a Slack post to the web team lists the URLs with 20 or more hits as candidates for a 301 redirect.
- tab_content_4 after: Which old URLs need a redirect this week Site migrations leave old addresses alive in newsletters and other people's posts. After Oldfield moved its marketing site, each 404 hit lands in a table with the URL, the referrer, and a seven-day count. Every Monday, a Slack post to the web team lists the URLs with 20 or more hits as candidates for a 301 redirect.
- tab_image_1 before: A Northwind store page for a retired linen shirt offers search and two other bestsellers to add to the cart, and the add is saved with the missed URL.
- tab_image_1 after: An Ostlund store page for a retired linen shirt offers search and two other bestsellers to add to the cart, and the add is saved with the missed URL.
- tab_image_2 before: Acme's docs answer a mistyped webhooks URL with a 404 page that searches the words in the path and offers the Webhooks: retries and signatures article first.
- tab_image_2 after: Nettlepay's docs answer a mistyped webhooks URL with a 404 page that searches the words in the path and offers the Webhooks: retries and signatures article first.
- tab_image_4 before: Globex's 404 log after a site migration lists missed URLs with referrers and seven-day hit counts, and a Monday Slack post names the three with 20 or more hits.
- tab_image_4 after: Oldfield's 404 log after a site migration lists missed URLs with referrers and seven-day hit counts, and a Monday Slack post names the three with 20 or more hits.

## 20261012-404-page-B-HUBRULES2bQC-2 (P1, B-HUBRULES2bQC, fix-by-writer, fixed)
- field: tab_content_2
- caught by: B-HUBRULES2bQC (Layer B): Stock placeholder name Acme in the Developer Docs tab copy.
- live text: Acme's API docs collect mistyped links from forum posts and old emails.

## 20261012-404-page-B-HUBRULES2bQC-3 (P1, B-HUBRULES2bQC, fix-by-writer, fixed)
- field: tab_content_4
- caught by: B-HUBRULES2bQC (Layer B): Stock placeholder name Globex in the Site Migration tab copy.
- live text: After Globex moved its marketing site, each 404 hit lands in a table with the URL, the referrer, and a seven-day count.

## 20261012-404-page-B-HUBRULES5alt-1 (P1, B-HUBRULES5alt, proposed)
- field: images.tab_image_1.alt
- caught by: B-HUBRULES5alt (Layer B): Alt text carries Northwind.
- live text: A Northwind store page for a retired linen shirt offers search and two other bestsellers to add to the cart, and the add is saved with the missed URL.

## 20261012-404-page-B-HUBRULES5alt-2 (P1, B-HUBRULES5alt, proposed)
- field: images.tab_image_2.alt
- caught by: B-HUBRULES5alt (Layer B): Alt text carries Acme.
- live text: Acme's docs answer a mistyped webhooks URL with a 404 page that searches the words in the path

## 20261012-404-page-B-HUBRULES5alt-3 (P1, B-HUBRULES5alt, proposed)
- field: images.tab_image_4.alt
- caught by: B-HUBRULES5alt (Layer B): Alt text carries Globex.
- live text: Globex's 404 log after a site migration lists missed URLs with referrers and seven-day hit counts

## 20261012-404-page-B-HUBRULES2bQC-4 (P1, B-HUBRULES2bQC, proposed)
- field: image_brief.tabs[0].main.chrome; image_brief.tabs[1].main.chrome
- caught by: B-HUBRULES2bQC (Layer B): Stock names drawn in the images: the tab 1 browser bar reads northwind.example, tab 2 carries Acme.
- live text: northwind.example/products/linen-camp-shirt

## 20261012-404-page-B-HUBRULES2apr-1 (P2, B-HUBRULES2apr, backlog)
- field: faq
- caught by: B-HUBRULES2apr (Layer B): FAQ 9's last sentence implies exporting the code is how you confirm the status code, which step 6 says you check by requesting a missing URL.
- live text: On paid plans, Emergent exports the full code to your GitHub repository, so you can confirm that status yourself.

## 20261012-404-page-B-HUBRULES5que-1 (P2, B-HUBRULES5que, backlog)
- field: faq
- caught by: B-HUBRULES5que (Layer B): Two FAQ questions read as broken English on the page.
- live text: What causes 404 page not found? | How to find a website 404 page?

## 20261012-404-page-B-HUBRULES5CON-1 (P2, B-HUBRULES5CON, backlog)
- field: faq
- caught by: B-HUBRULES5CON (Layer B): FAQ 5 closes on a thank-you-page sentence that only carries a link; FAQ 10 does the same for landing page SEO.
- live text: The same rule applies to a thank you page: the next step matters more than the art.

## 20261012-404-page-B-HUBRULES2are-1 (P2, B-HUBRULES2are, backlog)
- field: feature_1
- caught by: B-HUBRULES2are (Layer B): Feature 1 opens by narrating the user's prompt; the semicolon joins two unrelated instructions.
- live text: Your prompt asks for the designed page on every unknown URL; check its status code with your host before launch.

## 20261012-404-page-B-HUBRULES2bQC-5 (P1, B-HUBRULES2bQC, proposed)
- field: template
- caught by: B-HUBRULES2bQC (Layer B): The carousel's AI CRM Builder card draws the stock name Acme Corp.
- live text: Acme Corp $24,000 Proposal

## 20261012-404-page-B-HUBRULES2bre-1 (P2, B-HUBRULES2bre, backlog)
- field: template
- caught by: B-HUBRULES2bre (Layer B): Sitewide testimonial strip uses generic placeholder personas.
- live text: Alex Rivera Founder, TaskFlow | Maya Chen Product Lead, BrightSuite | Jordan Patel Co-founder, LoopDesk
