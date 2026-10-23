# Search Console steps after the slug migration (2026-10-23)

Property: the emergent.sh property in Google Search Console, either the Domain property `emergent.sh` or the URL-prefix property `https://emergent.sh/`.

## 1. Resubmit the sitemap (do this first)
1. Open Search Console and select the emergent.sh property.
2. In the left menu, go to Indexing > Sitemaps.
3. Under "Add a new sitemap", enter `sitemap.xml` and click Submit. Resubmitting the same URL makes Google fetch it again.
4. If the site lists sub-sitemaps (e.g. `page-sitemap.xml`), submit each one the same way. Check that "Last read" changes to today and that "Status" says Success.
5. Do this only AFTER the Cloudflare cache for the sitemaps is purged (see the B-qa-5 result), so Google reads the new URLs.

## 2. Ask Google to recrawl the 4 hub pages
1. Paste each hub URL into the URL Inspection bar at the top:
   - https://emergent.sh/ai-landing-page-builder
   - https://emergent.sh/ai-form-builder
   - https://emergent.sh/ai-automation-builder
   - https://emergent.sh/ai-survey-and-quiz-builder
2. Click "Test live URL" and confirm it shows "URL is available to Google".
3. Click "Request indexing". The hubs link to every child page's new URL, so this speeds up discovery of all of them.
4. Optionally do the same for your 10 highest-traffic child pages at their NEW URLs. The daily request quota is roughly 10 to 12 URLs, so don't submit all 291.

## 3. Don't do these
- Don't use the Removals tool on old URLs. The 301s handle them; a removal would hide the new page too.
- Don't use the Change of Address tool. That is only for moving to a new domain.

## 4. Watch over the next 2 to 4 weeks
1. Indexing > Pages. "Page with redirect" will rise as old URLs are recrawled. That is expected and correct.
2. Watch "Not found (404)" for any old child URL. There should be none; if one appears, its 301 row is missing. Send me the URL.
3. Performance > Search results, filtered by Page "contains" one of the hub paths. Clicks and impressions should move from the old URLs to the new ones within about 2 to 4 weeks.
4. Look for any "Duplicate, Google chose different canonical" entries on the new URLs. There should be none, because each new page's canonical points at itself.
