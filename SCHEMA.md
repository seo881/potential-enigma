# Structured data (JSON-LD) for the build hubs

Written 2026-09-30. Owner: Divit Bhat.

## Hubs (4 static pages): unchanged, verified
The Schema markup field (`jsonLdSchema`) on the 4 hubs holds WebPage + FAQPage + BreadcrumbList.
All 56 FAQ Q&As were verified word for word against the live FAQs collection items (filtered by `featured`) on 2026-09-30, and every item is published. **No edit made.**
If any hub FAQ text changes, rebuild that hub's FAQPage to match.

## Child templates (4 CMS templates): NEW runtime schema embed
The API only accepts `jsonLdSchema` objects. CMS-bound `rawJsonLdSchema` is Designer-only, so an HTML embed builds the graph at runtime from what the page renders:
- WebPage name comes from `document.title`.
- The description comes from the meta description.
- BreadcrumbList is read from the visible `.build_breadcrumbs`.
- FAQPage comes from `window.awbFAQ`, the same data the accordion renders.

Nodes: Organization, WebSite, WebPage, BreadcrumbList, FAQPage (when there are FAQs). All `@id` values are rooted at https://emergent.sh, and every reference resolves.

The source is `schema/page-schema.html`. The stored code is byte-identical (sha256 prefix `aea62a63b06e`); tests are in `schema/test2.js`.

| Template | Page ID | Embed element ID (appended to main-wrapper, class `hide`) |
|---|---|---|
| LP | 6aaaa937fe1a8d180b7c9f90 | 4c65422b-02e8-7e99-53ab-c0c84ad62c9a (parent d8a90b8f-142b-5c77-eae7-a06e09b0872a) |
| Form | 6aaaaa03995bb2f9f4d6a3c2 | a5b8153d-74b0-a6c6-d470-fae1e7e2bc90 (parent 24cd8ebc-23b4-d766-1f9f-0d648fc0644a) |
| AAB | 6ab2470540448c8f7d1ccc1c | bd810f03-cb97-27fa-815e-3fe09b44bfe3 (parent cadd555f-249f-2bfd-b8af-165dc634d7ca) |
| SQB | 6ab24754757025d10940d06a | 422d1795-6f21-9e96-4894-05d9d9ae6d38 (parent ba847d5e-85b3-fe51-eadf-ad4eebacf5ca) |

**Rollback:** remove the embed element (one `remove_element` per template). The previous state had no schema on these templates.

**Google note:** FAQ rich results were retired on 2026-05-07, and the Rich Results Test dropped FAQ in June 2026. The expected Rich Results Test result is "Breadcrumbs: valid", with FAQ not shown. FAQPage is still valid schema.org for Bing and AI engines.
SoftwareApplication and Product are deliberately excluded: Google's Software App result requires aggregateRating or review.

**Post-publish check:** on a live child URL, run the Rich Results Test. You can also run `JSON.parse(document.getElementById('awb-jsonld').text)` in the DevTools console.
