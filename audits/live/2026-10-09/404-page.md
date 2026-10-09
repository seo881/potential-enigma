# /ai-landing-page-builder/404-page: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-404-page-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-404-page-A6-entity-1 (P1, A6-entity, proposed)
- field: template
- caught by: A6-entity (Layer A): broken HTML entity shown as text in jsonld text
- live text: age tells visitors a URL doesn&#39;t exist. See 404 page examples

## 20261009-404-page-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-404-page-B-HUBRULES2cop-1 (P1, B-HUBRULES2cop, fix-by-writer, fixed)
- field: faq
- caught by: B-HUBRULES2cop (Layer B): FAQ 10 writes the acronym in lowercase in the link anchor, next to 'SEO' in the same sentence.
- live text: pages built to rank deserve the same care as any landing page seo work.
- faq before: window.awbFAQ = {"heading": "404 Page Questions, Answered", "items": [{"q": "What is a 404 page?", "a": "A 404 page is what a website shows when someone requests a URL that does not exist on it, sent along with the HTTP 404 status code. The page itself can be anything the site designs, from one line of plain text to a full layout with links back in."}, {"q": "How do I create a 404 page for my website?", "a": "Check your host's documentation for its error page setting. On GitHub Pages, a file nam
- faq after: window.awbFAQ = {"heading": "404 Page Questions, Answered", "items": [{"q": "What is a 404 page?", "a": "A 404 page is what a website shows when someone requests a URL that does not exist on it, sent along with the HTTP 404 status code. The page itself can be anything the site designs, from one line of plain text to a full layout with links back in."}, {"q": "How do I create a 404 page for my website?", "a": "Check your host's documentation for its error page setting. On GitHub Pages, a file nam
- howto_step_3_des before: Under whatever leads the page, add two or three plain links: the homepage, your most visited section and a way to contact you.
- howto_step_3_des after: Put a search box under the heading for visitors who know the page they want. Add two or three plain links below it: the homepage, your most visited section, and a way to contact you. Label each link with where it goes.

## 20261009-404-page-B-HUBRULES5how-1 (P1, B-HUBRULES5how, fix-by-writer, fixed)
- field: howto_step_3_des
- caught by: B-HUBRULES5how (Layer B): Step 3 is 23 words, below the 35-50 word range, and never mentions the search its title promises.
- live text: Under whatever leads the page, add two or three plain links: the homepage, your most visited section and a way to contact you.

## 20261009-404-page-B-HUBRULES6cla-1 (P1, B-HUBRULES6cla, proposed)
- field: feature_1
- caught by: B-HUBRULES6cla (Layer B): States that an Emergent-hosted site answers unknown URLs with a real 404 status; that hosting capability is not in rules/claims.json or rules/capabilities.json and has been pending with Divit since review.
- live text: Your prompt asks for every unknown URL to answer with a 404 and the designed page. Crawlers read the code; people read the page.

## 20261009-404-page-B-HUBRULES5com-1 (P1, B-HUBRULES5com, proposed)
- field: why_table
- caught by: B-HUBRULES5com (Layer B): The Emergent build cell falls back to the LP hub default and calls a 404 page a campaign page; no LP variant fits, so the library needs a new cell.
- live text: How you build | Prompt for a campaign page | Prompt for a full site

## 20261009-404-page-B-HUBRULES5FAQ-1 (P2, B-HUBRULES5FAQ, backlog)
- field: faq
- caught by: B-HUBRULES5FAQ (Layer B): FAQ 4 reads 'access a 404 page' as getting past one while FAQ 6 answers the viewing reading, so the two items overlap.
- live text: How do I access a 404 page? Most people reach one by accident, and getting past it takes a minute.
