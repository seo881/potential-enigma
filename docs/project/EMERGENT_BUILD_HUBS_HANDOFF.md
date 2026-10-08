# Emergent.sh Build Hubs: complete handoff

**Written:** 2026-09-29 at the end of chat session 5. It covers every session from 2026-09-23 to 2026-09-29.
**Purpose:** a new chat reads this and continues as if it were the same conversation. Nothing here is a guess unless it's marked **UNVERIFIED**; those items must be checked live before anyone relies on them.
**Owner:** Divit Bhat (Emergent), who is "the user" throughout.

---

## 0. Read this first: how to work with Divit (non-negotiable)

These rules come from Divit's own words across the sessions. Follow them exactly.

1. **No change to the live site without explicit approval.** Plan first, show the plan, wait for "go". Approval for one thing doesn't extend to the next thing.
2. **Always be ready to roll back.** Before any write, read and record the current value. After the write, read it back to verify. Log IDs and old values in the repo (`INTERACTIONS.md`, `COVERS.md`, `manifest.json`).
3. **Touch nothing outside the pages in scope.** Never edit a **component definition** (it changes every instance site-wide; the use-case component alone has 11 instances, including live CRM pages). **Never modify an existing class.** Only create new classes. Divit explicitly refused a site-wide style change (`build-usecase_image` object-fit) and said *"no, don't make any site-wide style change"*.
4. **Be surgical and meticulous.** Divit says "no margin of error", "everything should be perfect", "no room for mess ups". Verify everything yourself, including from screenshots he sends.
5. **Don't assume. Ask when something is borderline.** In his words: *"if you are stuck anywhere, come back to me and ask, dont assume and go ahead w it"*. Only look things up or verify from the live site.
6. **Copy must be "operator grade" with no fluff.** It must never narrow the audience. Examples: carousel headings end "for you" or "for you and your business", never "for your campaign" or "for your team", unless the subject genuinely targets a group (surveys go to people, so "for your team" is OK). No vendor numbers in hero subheads or meta descriptions. Write "Emergent's", never "our".
7. **Quality bar: world class, not placeholders.** Visuals are held to the Linear, Stripe and Vercel level. Divit rejected "substandard work" and pushed for "your best work". When asked "is this your best?", answer honestly.
8. **Pace:** Divit wants momentum ("lets fucking go", "fuck these timelines"), but never at the expense of rule 1 or rule 4. Plain, direct reporting is welcome; he's fine with casual language.
9. **Asking for approval:** give options with a recommendation, and ask **one** clear question at the end.
10. **Divit does the manual Designer steps** (things the API can't do). Give him exact click-by-click steps, then verify his work from your end.
11. **Show visuals at true display size**, and give before/after comparisons for visual work.

---

## 1. The project

**Emergent** (emergent.sh) is an AI app builder: prompt to working app. Divit runs the SEO programme for the "Build" hubs on the Webflow site.

**Scope right now: 4 "build hubs"**, each a hub page plus a CMS collection of child pages:

| Hub | Code | URL | Colour (v5 visuals) |
|---|---|---|---|
| AI Landing Page Builder | **LP** | `/ai-landing-page-builder` | Blue |
| AI Form Builder | **Form** | `/ai-form-builder` | Emerald |
| AI Automation Builder | **AAB** (collection prefix "AATB") | `/ai-automation-builder` | Violet |
| AI Survey and Quiz Builder | **SQB** (collection prefix "ASQB") | `/ai-survey-and-quiz-builder` | Burnt orange |

**Scale ahead:**
- **More than 800 child pages** across these 4 hubs.
- **About 3,000–4,000 images**: 4 use-case images per page, 1 card cover and 1 share (OG) image.
- **After these 4, two more hubs follow**, not yet named. Divit: *"we need to pick the next 2 hubs and work on that, that is also a ton of work"*.
- **Child pages to pick:** Divit said he'd name 5 child pages per hub initially. Only 1 exists per hub so far.

**The Webflow developer** (Kruthivas Sarma) built the original page and collection structure, but kept stalling. Divit, on 2026-09-29: *"fuck that guy, he just keeps stalling"*. **We now do the dev work ourselves via the API**, within the rules above.

---

## 2. Access, IDs and tools

### Webflow
- **Site ID:** `6a0edf12ef1a8562ed56d806`
- **Designer URL:** `emergent-sh.design.webflow.com`
- **CDN hosts:**
  - CMS files: `cdn.prod.website-files.com/6a0f028de6df6a6fd88c3f89/…`
  - Site assets: `cdn.prod.website-files.com/6a0edf12ef1a8562ed56d806/…`
- **Locale IDs:** CMS locale `6a0f028de6df6a6fd88c3f87`; page locale `6a0f028de6df6a6fd88c4019`
- **MCP tools used:**
  - `data_cms_tool`, `data_element_tool`, `data_element_settings_tool`, `data_element_builder`, `data_style_tool`
  - `data_interactions_tool`, `data_pages_tool`, `data_component_tool`, `data_component_props_tool`
  - Load a deferred tool with `tool_search` first.
- **Session ID:** every call needs `session_id`. The old chat used `ses_3JizjfbFdjh6S4LbXuyCOojLxGf`. **A new chat must send `start` on its first call** and then reuse the ID it gets back. It should also choose its own `agent_id` (the format is `model|harness|suffix`).
- **Rate limit:** `GET /v2/pages returned 429` happens after bursts. **Wait about 65 seconds and retry.** Pace element calls, since each hits `/v2/pages`.

### GitHub (image pipeline repo)
- **Repo:** `seo881/potential-enigma`. It's **public**, so never commit secrets.
- **Latest commit:** `f7563a3` (bootstrap added). The one before, `3a65695`, is where covers, share images, motion and unhidden carousels went live.
- **Token:** fine-grained, scoped to **potential-enigma only**, with **Contents: Read and write** and Metadata read-only. **Expires 2026-12-28.** The old no-expiry token was deleted by Divit.
  - Token: `[REDACTED: token is in the Project file EMERGENT_BUILD_HUBS_HANDOFF.md, never in this public repo]`
  - ⚠️ This doc contains the token. Keep it inside the private Claude Project. **Never commit it** to the repo.
- **How to push without storing the token** (the method used every time):
  ```bash
  T='<token>'; B=$(printf 'x-access-token:%s' "$T" | base64 -w0)
  git -c http.extraheader="AUTHORIZATION: basic $B" push -q origin main 2>&1 | sed "s/$T/[token]/g"; unset T B
  ```
  Commit as `-c user.name="seo881" -c user.email="seo881@users.noreply.github.com"`.
- **Clone in a new chat:** `git clone https://github.com/seo881/potential-enigma.git /home/claude/pe`. The repo is public, so no token is needed to clone.

### Sandbox bootstrap (the file system resets between chats)
Run: `cd /home/claude/pe && bash pipeline/bootstrap.sh`. It:
- installs cairosvg, uharfbuzz, fonttools, pillow and librsvg;
- installs **Inter 4.1** from `github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip` to `/root/.fonts/Inter-{Regular,Medium,SemiBold,Bold,ExtraBold}.ttf`;
- installs **Lucide icons** (`npm pack lucide-static`) to `/home/claude/lucide/package/icons/`;
- creates the working copy `/home/claude/pipe/`, with import aliases `ds5.py`, `hubs5.py`, `covers5.py` and `scenes32.py`, plus `/home/claude/cards/helpers.py`;
- smoke-tests every approved scene through every gate.

**Verified 2026-09-29 from a wiped state:** *"BOOTSTRAP OK: 20 scenes/covers built, all gates clean"*. Rebuilt files are **byte-identical** to the live ones.

### Other environment facts
- The bash network allowlist includes github.com, raw.githubusercontent.com, release-assets.githubusercontent.com, npm and pypi. The Webflow CDN is **not reachable** from bash.
- `web_fetch` can only open URLs that appeared in search results or messages. It **cannot** open the Webflow CDN, so ask Divit to open CDN URLs in his browser when you need real-browser verification.
- **Webflow imports CMS images from public URLs:** set an image field to `{"url": "<raw github url pinned to a commit SHA>", "alt": "..."}`. Webflow copies the file to its CDN and returns a new `fileId`. Always pin to a **commit SHA**, never `main`.
- **Webflow accepts SVG in CMS image fields** and serves it unchanged. `<defs>` and `<use>` survive, so outlined glyphs render; Divit verified this by opening the CDN URL at 5× zoom.

---

## 3. Site structure: every ID that matters

### 3.1 Hub pages (all four are currently `draft: true`)
| Hub | Page ID | SEO title (live in CMS/page settings) |
|---|---|---|
| LP | `6aaa658ea6d39733443fe69b` | AI Landing Page Builder: Prompt to Live Page \| Emergent |
| Form | `6aabb4c5789871e91d60f6f9` | AI Form Builder: Free Online Form Builder \| Emergent |
| AAB | `6ab2464303ee70548366671e` | Workflow Automation Software, from a Prompt \| Emergent |
| SQB | `6ab246c3897d1c09d9d320ec` | AI Survey Maker, Quiz Maker & Poll Maker in One \| Emergent |

**Meta descriptions (current):**
- **LP:** "Emergent is an AI landing page builder that turns one prompt into a live page, a working form, and a database you own, on your domain. Free to start."
- **Form:** "The online form builder that writes every response to a database you own. Describe the form, get the fields, logic, and integrations. Free to start."
- **AAB:** "Workflow automation software that builds itself from a prompt: the workflow, trigger form, database, and dashboard. No task cap. Free to start."
- **SQB:** "Build a survey, quiz, or poll from a prompt. Emergent generates the questions, the logic, and a database you own. No response caps. Free to start."

**OG image on all 4 hubs:** the generic `…6a169f29b54acd56f5308b9b_emergent.webp`. Custom ones are optional.

**Key hub elements** (the same IDs across hubs, because they were cloned):
- **Internal-linking carousel section:** `acd0c79f-f838-9a2e-53c7-b22c5244fdb6` (class `section_build`). **Unhidden on all 4 hubs on 2026-09-29.**
  - Inside it: list wrapper `…fdbe` (`build_list-wrapper`); list `…fdbf` (`build_list`, attributes `fs-list-element=list`, `fs-list-load=more` for Finsweet load-more); item `…fdc0`; card link `…fdc1`.
  - Card link class: `build_link Copy` on LP, AAB and SQB; `build_link` on Form.
  - Pagination element `46e019d5-…-fe34` (class `load-more_pagination`): 15 per page, "Load more" button, arrow hidden.
- **Duplicate carousel from the first draft:** `86e5ccd1-891e-bb61-1762-8591adc90744`. It exists on AAB and SQB, is **hidden**, and is safe to delete (housekeeping).
- **§11 "More things you can build":** class `section_build-hub`, with 8 cards linking to other hubs. Section IDs: LP `f350b269-7ea7-1a0f-3cd9-5ce3e33898bd`, Form `5175601b-006f-1460-b96d-c84aa9968d64`, AAB `fdfbf8cf-c309-6002-0123-486847fc1192`. Divit: *"whatever layout the dev has created we will be sticking to"*. Don't add the doc's 9-card version.
- **Hero:** component "Build page hero" (component `20c1b760-6736-130c-e34b-872d2c8dc715`). On the Form hub its instance is `75898b28-2a0c-840d-96c5-586b4ac9483c`, with props Title, Description, tabs and prompts. The H1 carries class `heading-style-h1` + combo `is-product`; the prompt box is `.build_input-block`.
- **Value cards:** component "Global / 3 Column (Cards)" (`763a7c4c-b59b-8f66-0ea0-1eee69ea26cd`). On AAB its instance is `b108c07e-ed5e-74a1-e374-3b1f52439262`, with props Title, Text and Image × 3, plus Heading, Subheading and Label.
  - Image class `product-integrations_image`: aspect **3/2.5 (6:5)**, object-fit cover. So value-card visuals are 1200×1000.
- **Integrations section on hubs:** class `section_product-integrations`. It has 3 cards of chips; chips use `.integration_chip`, `_icon`, `_text` and `_wrap`, with **4 chips per card (2×2)**.
  - **UNVERIFIED:** whether the hubs also have the "wide dark card" banner ("If it has an API, your page can use it." with 8 logo tiles). It was in the original hub spec (§5), but it may never have been built. Check it live.

### 3.2 Collections (child pages)
| Hub | Collection ID | Slug | Template page ID |
|---|---|---|---|
| LP | `6aaaa937fe1a8d180b7c9f83` | (LP) | `6aaaa937fe1a8d180b7c9f90` |
| Form | `6aaaaa02995bb2f9f4d6a36c` | (Form) | `6aaaaa03995bb2f9f4d6a3c2` |
| AAB | `6ab2470540448c8f7d1ccbf0` | `ai-automation-builder` | `6ab2470540448c8f7d1ccc1c` |
| SQB | `6ab24754757025d10940d04e` | (SQB) | `6ab24754757025d10940d06a` |

**Other collections:**
- **Learn:** `6a0f028d0bfe272031dbddb8`
- **FAQs:** `6a1985abca24e8ec3a22bf2e`
- **Integrations:** `6a16bd81135c15917a38b1d6`, with **235 items**. Fields: brand-name, description, category (option), hover-text, thumbnail-image (a wide "Brand + Emergent" banner, **not** a clean logo), about-brand, FAQ Q/A 1–5, rating, name, slug.
- **Tutorials:** `6a1580d5afc748a524142a53`
- **Case studies:** `6a16b2e576dae3dc70771717`
- **CRM builder (legacy):** `6a3a6beafcbf2114d556f4f4`

**Field slugs are shared across the 4 child collections** (cloned from the CRM template; the display names use AATB, ASQB and similar prefixes):
- **SEO:** `meta-title`, `meta-description`, `name` (used as the H1), `slug`, `acrm---product-name`, `description`, `acrm---breadcrumb`, `category` (option), `explore-cta`.
- **Images:**
  - `thumbnail-image`: now the **social share / OG image**, a PNG at 1200×630.
  - **New 2026-09-29:** a **Cover Image** field per collection: AAB `aatb---cover-image` (`330a718a68d16a849a62a15bba7e9123`), SQB `asqb---cover-image` (`92be997ab328a707a4e20915a1da796a`), LP `alpb---cover-image` (`b42f5db743e2e051b5be1fca7d6c3a99`), Form `afb---cover-image` (`aef8e5a8fbe2df6814bd702f11ab8890`).
- **Features:** `awb---integrations-heading` (despite the name, it holds the **features** H2), `acrm---key-feature-sub-heading`, `acrm---key-feature-1..6-content` (rich text: h3 plus p).
- **Use-case tabs:**
  - Heading: `acrm---usecase-heading`
  - Tab labels: `acrm---key-feature-filter-1..4`
  - Tab content: tab 1 `awb---key-feature-1-content`, tab 2 `awb---integration-feature-1`, tab 3 `awb---integration-feature-2`, tab 4 `acrm---integration-feature-4`
  - Tab images: tab 1 `awb---key-feature-1-image`, tabs 2–4 `acrm---key-feature-2/3/4-image`
- **Other content fields:**
  - `awb---mockup-data` (window.awbMockup prompts per tab)
  - How-to: `awb---how-to-title`, `awb---how-to-description`, `awb---how-to-step-1..4-title` and `-des`
  - FAQ: `awb---faq-data` (a `<script>window.awbFAQ={heading,items:[{q,a}]}</script>` inside a rich-text embed)
  - Why Emergent: `acrm---why-emergent-title`, `acrm---why-emergent-description`, `acrm---why-emergent-table` (an HTML table embed, classes `cmp`, `col-other`, `col-brand`, `col-brand-head`)
  - Prompt chips under the hero: `alpb---prompt-filter-1..4` on LP, AAB and SQB; `afb---prompt-filter-1..4` on Form
  - Hero prompt text: `alpb---prompt` or `afb---prompt`
- **Multi-references:**
  - `acrm---learn` → Learn
  - `acrm---tutorials` → Tutorials
  - `acrm---case-study` → Case studies
  - `acrm---integration` → **Integrations** (currently empty on all items; see §9, pending item P1)
  - Legacy CRM refs, unused
- **Category option:** 100 options max (a Webflow limit). Divit renamed options to "Standalone Pages" (LP) and "Applications" (by replacing "CDK"). **Caution:** option IDs are shared across the cloned collections, but names differ per collection. The AAB collection still shows `a3f1c6d3f1f5b72e83814b483a0ac3d5` as "CDK". Current child categories: Thank You and Creator use `a3f1c6d3…`; Approval `a33cd4fb124ec86a130809893b2b3896` ("Operational"); CSAT `c727c2a1303d35e116ff59cd12aa3f74` ("Customer Service"). The category isn't displayed visually, but it's used for filtering. Clean it up before scaling (housekeeping).

### 3.3 The 4 child pages (all CMS items are `isDraft: true`)
| Hub | Item ID | Slug / URL | Primary keyword (MSV, KD) |
|---|---|---|---|
| LP | `6ab5158e23395050bc86ca79` | `/ai-landing-page-builder/thank-you-page` | thank you page |
| Form | `6ab505a8d621dc692561a85a` | `/ai-form-builder/creator-application` | creator application (390, KD 55) |
| AAB | `6aba7ac40efe4e6ac8693159` | `/ai-automation-builder/approval-workflow` | approval workflow (590, KD 24) |
| SQB | `6aba7afb6271de33629b812c` | `/ai-survey-and-quiz-builder/customer-satisfaction` | customer satisfaction survey (5,400, KD 31); secondary csat survey (2,400) |

**Page-level SEO:**

**LP: Thank You Page**
- **Meta title:** "Thank You Page: Examples, Templates, Builder | Emergent"
- **Meta description:** "What a thank you page is, real examples, templates you can build in minutes. Custom thank you page for WooCommerce, Shopify or a standalone URL, free."
- **H1:** "Build a Custom Thank You Page in Minutes"
- **Tabs:** Lead Magnet, Ecommerce Order, Webinar or Event, Contact and Booking
- **Prompt chips:** Instant Download, Next-Step Booking, Conversion Pixel, Order Upsell
- **FAQs:** 14
- **Learn:** 3 references

**Form: Creator Application**
- **Meta title:** "Creator Application Form: Build Yours With AI | Emergent"
- **Meta description:** "Build a creator application form for your creator, ambassador or UGC program. Score every applicant and save each one to a database you own. Free to start."
- **H1:** "Build a Creator Application Form Using AI in Minutes"
- **Tabs:** Brand Ambassadors, UGC Creators, Affiliate Programs, Creator Hiring
- **Prompt chips:** Platform Questions, Fit Scoring, Sample Uploads, Approval Emails
- **FAQs:** 12
- **Learn:** 3 references

**AAB: Approval workflow**
- **Meta title (58 characters):** "Approval Workflow: Build and Automate Approvals | Emergent"
- **Meta description (153 characters):** "Build an approval workflow from a prompt: request form, multi-level routing, Slack and email alerts, escalation, and an audit log you own. Free to start."
- **H1:** "Build an Approval Workflow Your Team Actually Uses"
- **Tabs:** Purchase Order, Invoice, Contract, Expense
- **Prompt chips:** Multi-level Routing, Slack Approvals, Escalation Rules, Audit Trail
- **FAQs:** 12
- **Comparison table:** 8 rows
- **Learn:** empty (Option A)

**SQB: Customer satisfaction survey**
- **Meta title (55 characters):** "Customer Satisfaction Survey Template & CSAT | Emergent"
- **Meta description (146 characters):** "Build a customer satisfaction survey with CSAT, NPS, and CES questions. Tie every response to the customer and alert on low scores. Free to start."
- **H1:** "Build a Customer Satisfaction Survey That Feeds Your Whole Product"
- **Tabs:** SaaS Onboarding, Post-Purchase, B2B Quarterly, Support Ticket
- **Prompt chips:** CSAT Survey, NPS Survey, CES Survey, Post-Purchase
- **FAQs:** 12
- **Learn:** empty

**The slug decision:** Divit chose `customer-satisfaction`, not `customer-satisfaction-survey`.

### 3.4 Child templates: sections, in order
From the AAB template, verified 2026-09-29; the others are the same structure:
1. Hero section `section_ai-hero` (AAB `cadd555f-249f-2bfd-b8af-165dc634d7cb`): H1 `…d7da` (classes `heading-style-h1 is-product`), subhead `…d7dd` (`text-size-medium text-color-alternate-secondary`, **a generic class, so don't target it**), then the prompt box and chips.
2. Features component, bound to the features fields.
3. **Use-case tabs component:** component `4a1e2fed-ef87-6e00-ca2d-e0d8e5150c66` "section_usecase", **11 instances site-wide**. On the AAB template its instance is `cadd555f-…-d95c`, bound to the tab fields.
   - Tabs wrapper `build-usecase_tabs`: native fade **300ms in, 100ms out, ease**. Verified by Divit's screenshot.
   - Image class `.build-usecase_image` (`455d8a8a-bf35-3333-ac1c-7e7489513e97`): **aspect 3/2, object-fit FILL**. Every use-case image must be exactly 3:2, or it gets stretched. **Don't change this class** (Divit refused).
4. How-to component "Global / Sticky List (Icons)" (`7a11ed6a-ab12-c739-dba4-4e0c0eca1e46`), with instance `cadd555f-…-d976`. Steps are `.sticky_list_wrapper`, each holding `.icon_wrapper.light` and `.sticky_item`.
5. Why Emergent comparison (table embed from the CMS).
6. FAQ component, bound to `awb---faq-data`.
7. §11 section `section_build-hub` (`cadd555f-…-d979`), button text "Start building free".
8. Related articles `section_blog-related` (`…d9d9`), showing the newest Learn articles site-wide (**Option A**, because there are no hub-specific articles yet).
9. **Carousel** `section_build` (`…d9f6`), visible, sourced from its own collection, 15 per page, Load more.
   - Card links: AAB `cadd555f-249f-2bfd-b8af-165dc634da01`, SQB `ba847d5e-85b3-fe51-eadf-ad4eebacf801`, LP `d8a90b8f-142b-5c77-eae7-a06e09b0895c`, Form `24cd8ebc-23b4-d766-1f9f-0d648fc06687`.
10. CTA ("Start building free").

**There is NO integrations section on child templates.** See pending item P1.

**Template SEO bindings:**
- Meta title and description are bound to the item fields; OG copies them from SEO.
- **The OG image binding is Designer-only** (the API won't set it). It was done for AAB and SQB via Divit's screenshot. **UNVERIFIED for the LP and Form templates.** Check Page settings → Open Graph → image = Thumbnail Image.

### 3.5 Classes and style IDs used by our work
| Class | Style ID | Notes |
|---|---|---|
| `build-usecase_image` | `455d8a8a-bf35-3333-ac1c-7e7489513e97` | 3/2, fill. Don't touch. |
| `section_usecase` | `28c47271-bae1-96ca-ef0d-e6e7cece646c` | Reveal trigger |
| **`build_cover`** (NEW, ours) | `40f4cb8f-74aa-83d6-a9b4-10fe25fba9f2` | Card cover: display block; width `calc(100% - 1rem)`; margin 0.5rem 0.5rem 0; aspect-ratio 16/10; object-fit cover; radius 8px; background #F4F3F8 |
| `build_link` | `0ba6ab63-6c94-0ff9-007e-e7dcce8d4f0b` | Card link (Form hub, LP/Form templates) |
| `build_link Copy` | `e837214e-2003-2ea5-863c-f12f76197151` | Card link (LP, AAB and SQB hubs; AAB/SQB templates) |
| `build-arrow_wrapper` | `540dc6c7-bb92-5ba7-c6d7-160374daf225` | Card arrow |
| `heading-style-h1` / combo `is-product` | `f7323f4e-d4f6-57ff-a593-03073e766fb2` / `eff8df5d-f28f-1ce3-d05b-7be97cef2a53` | Hero H1 |
| `build_input-block` | `688f234b-bcd5-e6e2-1b37-15e750ae70a8` | Hero prompt box |
| `sticky_list_wrapper` | `2ce035d7-f3ec-ea2d-6329-6581382527d8` | How-to step |
| `integration_chip` (+ `_wrap`, `_icon`, `_text`) | `a7e4fc03-ca0f-4e4c-621c-899aee3a0746` (`8b83a4b3-…`, `90830412-…`, `e534c5da-…`) | Chips |
| `product-integrations_image` | `f60aac1b-173c-8f09-ac59-e84951be9315` | Value-card image, 3/2.5 |

**Card layout:** `build_list` is a 3-column grid, gap 1.5rem; `build_link` is white with 12px radius; `build_content_wrapper Copy` has 0.5rem padding. **Covers display at about 360×225 CSS px.**

---

## 4. What's done: hub pages

**LP and Form hubs (sessions 1–3):**
- **Copy:** fully rewritten to Divit's SEO doc, then two full copy audits (P0/P1/P2 items), all implemented.
  - **Form H1:** "Build any form in minutes. Own every response." (approved 2026-09-24)
  - **Carousel headings:** LP "Find the right landing page / for you" (Divit changed "for your campaign" to "for you"); Form "Find the right form / for whatever you're collecting". The line break is made with Shift+Enter in the Designer.
- **Claims settled by Divit:**
  - "SOC 2 Type I and ISO 27001" is correct.
  - Custom domain wording: "built into Emergent, no third-party hosting to set up; custom domains use credits". In tables: "Built in, uses credits".
  - A "conversational one-question-per-screen flow" is claimable, because the agent can do anything explicitly asked.
  - For rolling vendor numbers, use wording that doesn't need monthly updates.
- **FAQs:** 14 per hub, stored in the FAQs collection or the component.
- **Schema:** in the **Schema markup field** (`jsonLdSchema` via `data_pages_tool`), **not** custom code. Types: **WebPage + FAQPage (exact live Q&As, word for word) + BreadcrumbList**, following the AI Website Builder and AI App Builder pages. SoftwareApplication and Product were **deliberately excluded**, because they fail Rich Results without reviews or prices. **Whenever FAQ text changes, rebuild the schema to match.**
- **Comparison tables:**
  - **Emergent is the first column** after the row labels.
  - The Emergent column is darker grey, alternating by row: `#F2F2F2` and `#E6E6E6`, with header `#EBEBEB`.
  - This is scoped to these two tables only; Global Styles are untouched.
  - Only change made to cell text: the approved "No per-visitor pricing".
- **Integration chips:** 4 per card (2×2), 12 different brands per hub, with logos (16 logos imported and attached to 19 chips).
  - **Brand links only go to brands that have an integration page.** Pages exist for HubSpot, Mailchimp, Stripe, PayPal, Calendly, Airtable, Notion, Excel, Attio and Slack.
  - **No page exists** for GA4, Meta Pixel, PostHog, Hotjar, Brevo, Kit, Cal.com, Postgres, Zapier or Webhook, so those chips don't link.
  - The chips button reads "Explore integrations".
- **Value cards:** 6 visuals at 1200×1000, blue for LP and mint for Form, uploaded by Divit.
- **Related articles:** heading "Explore more articles", sorted **newest first**.
- **§11:** placed between the FAQ and the CTA.
- **Status:** these hubs were prepared for launch (staging reviewed), but **both still show `draft: true`**. **UNVERIFIED** whether they ever went live, so check `publishedPath` and the live URLs.

**AAB and SQB hubs (sessions 4–5):**
- **Copy:** built with the same structure and a copy audit.
  - **Hero subheads:** AAB "…integrations it needs. No code. No task cap."; SQB "…to a database you own. No response caps. No per-response fees."
  - **Carousel headings:** AAB "Find the right workflow automation / for you and your business"; SQB "Find the right survey, quiz, or poll / for your team" (surveys go to people, so the group framing is right).
- **Chips:** Option B, 4 per card (2×2), each linking to its brand's integration page where one exists.
  - **AAB:** Triggers (Slack, HubSpot, Webhook, Stripe); Data (Airtable, Postgres, Google Sheets, Excel); Ops (Slack, Gmail, Notion, Asana).
  - **SQB:** CRM (HubSpot, Klaviyo, Salesforce, Attio); Data (Airtable, Notion, Google Sheets, Excel); Alerts (Slack, Zapier, Webhook, Gmail).
- **Value cards:** 6 visuals, violet for AAB and amber for SQB. Asset IDs:
  - AAB: `6aba7575772048bdd244bde9`, `6aba7575aa2a192197559c8b`, `6aba757585a024c46830a103`
  - SQB: `6aba7575f2d973473c48388b`, `6aba757577f53da6b233fd42`, `6aba757535531b017a7c96f0`
- **Carousels:** rebuilt and bound to their own collections, 15 per page, Load more.
- **Breadcrumbs:** fixed on all 4 hubs. They'd said "This is some text inside of a div block".
- **Other QC:** the Feature 2 stray line break fixed, and the hidden filter text bound to the item name.

---

## 5. What's done: child pages and templates

- **Templates:** all 4 child templates are fully bound (they were CRM clones with Lorem text). This covers SEO, features, use-case tabs (14 props), how-to (10 props), the comparison (3 props), FAQ, carousel (own collection, 15 per page, Load more), the §11 button, the CTA button and related articles.
- **Content:** all 4 child items have their full copy in place (see §3.3).
- **Use-case images:** **all 16 are live on the v5 design system** (vector SVG, 3:2, with in-image motion). See §6.
- **Card covers and share images:** all 4 child items have a Cover (SVG) and a Thumbnail/OG image (PNG). See §7.
- **Motion (IX3):** 6 interactions scoped to the 8 build-hub pages. See §8.
- **Carousels on hubs:** unhidden 2026-09-29.

---

## 6. The image pipeline and v5 design system (approved standard)

### 6.1 History: lessons that must never be repeated
1. **v1, 6:5 WebP:** the images were stretched in the Webflow slot. **Cause:** I didn't read the slot's CSS (`.build-usecase_image` is 3/2 with object-fit fill). Divit: "that's just plain dumb". **Rule: read the slot's actual CSS (aspect ratio, object-fit, display width) BEFORE designing any image.** A shape gate now enforces it.
2. **v2, 3:2 raster:** the shape was right, but the images looked soft, because Webflow serves downsized responsive copies of CMS raster images and upscales them.
3. **v3, vector:** SVG with every glyph outlined (Inter, shaped by HarfBuzz with kerning), `<defs>` plus `<use>`. Razor-sharp, and Webflow never resizes SVGs. **Verified in a real browser by Divit.**
4. **v4 and v5, "world class":**
   - a prompt chip flowing into the app;
   - three depth levels plus a spotlight on the hero card;
   - one 60/1140 grid and real product chrome;
   - a moment in progress rather than a diagram;
   - WCAG AA contrast on every text element;
   - in-SVG motion (the cursor press with ripple, pulses, a scan sweep, a blinking caret, a bell ring, a glowing bar).
   **Approved by Divit:** "these outclass the placeholder images in every domain".
5. **Size facts, measured:** an SVG averages about 102 KB (about 23 KB if the CDN gzips it; **UNVERIFIED**, ask Divit to check `content-encoding` in DevTools). The alternatives: PNG about 826 KB, JPEG about 461 KB, the old `Default.png` 1,565 KB.

### 6.2 Repo layout (`seo881/potential-enigma`)
- **`images/<hub>/<slug>/uc-1..4.svg`:** the live use-case images, v5.
- **`uc-1..4.webp`:** the v2 raster fallbacks.
- **`cover.svg`:** the card cover, 800×500 (16:10).
- **`og.png`:** the share image, 1200×630.
- **Hub and slug folders:** `lp/thank-you-page`, `form/creator-application`, `aab/approval-workflow`, `sqb/customer-satisfaction`.
- **`masters/`:** the old v2 SVG masters (legacy).
- **`pipeline/`:**
  - **`scenes_v5.py`** (imported as `ds5`): the design-system primitives and the **AAB** scenes `po`, `invoice`, `contract`, `expense`, plus `SCENES`. The primitives are `T` (text), `icon` (Lucide), `rect`, `chip`, `button`, `avatar`, `cursor`, `window`, `prompt` (the chip with caret and ⌘↵ keycaps, with a build-time guard) and `spot`. It also defines the defs, gradients, filters `e1`/`e2`, the motion `STYLE` and `canvas()` (which adds a title and description).
  - **`hubs_v5.py`** (imported as `hubs5`): palette-aware versions for **LP, Form and SQB** (4 scenes each), plus the `aab` palette. `PALS`, `set_hub()`, `browser()`, `appmsg()`, `mini()`, `stars()`, `field()`, `click()`.
  - **`covers_v5.py`** (imported as `covers5`): the 4 card covers.
  - **`outline.py`:** converts `<text>` into glyph outlines. Kerning and ligatures are on; `data-tnum` enables tabular figures.
  - **`qa.py`:** font metrics (`width()`) and the legacy layout check.
  - **`qa3.py`:** the current gates. WCAG AA contrast against each text's real background (circles count as backgrounds; gradients are scored at their **lightest** stop); occlusion-aware overlap and edge checks; off-canvas.
  - **`scenes.py`** (v2, legacy), **`helpers.py`** (legacy primitives), **`run.py`** (the v2 runner) and **`bootstrap.sh`**.
- **`manifest.json`:** maps every use-case image to its item, collection, field, alt text, `source_url` (pinned SHA), `webflow_file_id` and status.
- **`README.md`**, **`INTERACTIONS.md`** (the IX3 log with rollback) and **`COVERS.md`** (the cover setup, IDs and rollback).

### 6.3 Palettes (tuned so white button text passes WCAG AA)
| Hub | Accent gradient | Accent dark | Accent soft |
|---|---|---|---|
| AAB, violet | #7C3AED → #4F46E5 | #5B21B6 | #F1ECFF |
| LP, blue | #2563EB → #1D4ED8 | #1E40AF | #EAF1FF |
| Form, emerald | #047857 → #0F766E | #065F46 | #E6F7EF |
| SQB, burnt orange | #C2410C → #9A3412 | #9A3412 | #FFF1E6 |

**Shared colours:**
- **Ink:** #0F172A; **sub:** #475569; **muted:** #64748B (never lighter for small text).
- **Status:** OK #15803D on #DCFCE7; Warn #B45309 on #FEF3C7; Bad #B91C1C on #FEE2E2.
- **Avatars:** deep gradients only, e.g. #C2410C→#9F1239, #2563EB→#4338CA, #047857→#115E59.

### 6.4 Rules for every image (the gates enforce these)
- **Use-case images:**
  - **Canvas:** 1200×800 (3:2), matching the slot.
  - **Minimum text:** 16 design px, which is 11px or more on screen at the 830px desktop slot.
  - **Grid:** left edge 60, right edge 1140.
  - **Prompt chip:** text must stay clear of the keycaps (a build-time assert).
- **Card covers:**
  - **Canvas:** 800×500 (16:10), shown at about 360px.
  - **Minimum text:** 26 design px (11.7px or more on screen).
  - **Content:** one bold product moment, almost no text.
- **Share (OG) images:**
  - **Format:** 1200×630 **PNG**. Platforms reject SVG.
  - **Content:** headline word-wrapped to a measured 480px column, no orphaned last line, card composited without its background.
- **Contrast:** every text element meets AA (4.5, or 3.0 for text of 24px or more, or bold text of 18.66px or more), against its real background.
- **The stories must be true:** numbers add up; statuses are consistent with each other; no claim that's false at that moment; cursors sit on button edges, never on labels.
- **Always review visually at true display size** before shipping, in addition to the gates.
- **Verify the vector output in two renderers** (cairosvg and librsvg / `rsvg-convert`).
- **Delivery:**
  1. Commit.
  2. Push.
  3. Verify the raw URLs are byte-identical, pinned to the SHA.
  4. Update the CMS image fields by URL (up to 100 items per call), **touching only the image fields**.
  5. Record the returned `fileId`s in `manifest.json`.
  6. Push the audit trail.

### 6.5 Live file IDs (current)
- **Use-case v5, AAB:** uc1 `6abba58e85926d9cd515b37f`, uc2 `…b374`, uc3 `…b37a`, uc4 `…b382`. These are the 4 approved reference scenes: purchase order, invoice, contract, expense.
- **LP:** `6abbb0caac422a048331d970`, `…d97b`, `…d96a`, `…d978`.
- **Form:** `6abbb0cb9a445d8d6d247d56`, `6abbb0cc9a445d8d6d247d5f`, `…d62`, `…d5c`.
- **SQB:** `6abbb0da1c58063f412db282`, `…288`, `…27c`, `…285`.
- **The full list is in `manifest.json`.**

---

## 7. Card covers and share images (internal-linking carousel)

- **What "covers" means to Divit:** the **card images in the internal-linking carousel**, the section listing the other child pages with Load more, **not** OG images. The goal is visual cards instead of grey text blocks.
- **Built 2026-09-29, by us rather than the developer:**
  - The 4 Cover Image fields (see §3.2).
  - The `build_cover` class.
  - **8 bound slots:**
    - **Hubs:** LP, AAB and SQB card image `9f4d88f4-ceaf-1458-dbf0-806d04fab049` (class added, rebound from Thumbnail to Cover); Form hub new image `33868d6a-3fc7-6604-2cb6-77b778111efb`.
    - **Templates:** new images prepended in the card link: AAB `480f5f8b-9230-9135-8e64-03c51439863a`, SQB `a6ca094c-1ae8-29b1-c970-b0f54002b4b6`, LP `ca16aadc-bdbd-248b-7432-d38ccc8614cb`, Form `1d9a132d-a8db-49d1-e945-f554512eedc9`.
- **Live covers (SVG):** AAB `6abbb81095974b2ce616fe7c`, SQB `6abbb8123311c47795024674`, LP `6abbb81e7da1d9fc3027518a`, Form `6abbb81f9fee69e3212d1b7b`.
- **Live share images (PNG, in Thumbnail Image):** AAB `6abbb81095974b2ce616fe70`, SQB `6abbb8113311c4779502466f`, LP `6abbb81e7da1d9fc3027518e`, Form `6abbb81f9fee69e3212d1b77`.
  - **Previous value** (to restore when rolling back): placeholder `6a901aa8cda440349cd42c6c`.
- **Cover designs:**
  - **AAB:** a Slack approval card with the cursor on Approve.
  - **LP:** a "You're in." browser with a Download button.
  - **Form:** "Approved" with the referral code MAYA15.
  - **SQB:** "How did we do?" with 5 stars, CSAT 4.6 and a "+0.4 this month" chip.
- **Share images:** "emergent" wordmark text, the headline, "From a prompt to a working app. Free to start." and the cover card on the right.

---

## 8. Motion: the IX3 layer (all interactions are ours; 24 older ones exist and must not be touched)

**Scope for all of them:** pages = the 4 hubs plus the 4 child templates: `6aaa658ea6d39733443fe69b`, `6aabb4c5789871e91d60f6f9`, `6ab2464303ee70548366671e`, `6ab246c3897d1c09d9d320ec`, `6ab2470540448c8f7d1ccc1c`, `6ab24754757025d10940d06a`, `6aaaa937fe1a8d180b7c9f90`, `6aaaaa03995bb2f9f4d6a3c2`.
- The first two interactions below (reveal and tilt) are scoped to the **4 templates only**.
- **Never scope site-wide.** The components are shared with live CRM pages.

| ID | Name | What it does | Conditions |
|---|---|---|---|
| `i-54e50d55` | Use-case image reveal | Scroll trigger on `.section_usecase` at "top 85%" (end "bottom top"). The image goes opacity 0→100%, y 64→0, scale 0.96→1, over 1.0s with ease 26 (expo.out). Strengthened 2026-09-29, because Preview opens on the section and the original 36px/0.7s was missed. | Reduced motion: off. Tiny and small breakpoints: skip to end. Templates only. |
| `i-af43ffd6` | Use-case image 3D tilt | Mouse-move on `.build-usecase_image`, with timelines for the mouseX and mouseY roles. rotationY −3→3 and rotationX 2.5→−2.5, perspective 1400, smoothness 0.8. **Verified working by Divit.** | Reduced motion, medium, small, tiny: off. Templates only. |
| `i-680a5d1a` | Hero entrance | Load trigger. The H1 (`.heading-style-h1.is-product`) splits into words that rise in (From: opacity 0, y 28; 0.8s; stagger 0.045). Then the prompt box (`.build_input-block`) settles in (From: opacity 0, y 36, scale 0.97; 0.9s; position 0.45). | Reduced motion: off. |
| `i-dcb777ac` | How-to steps come into focus | Scroll scrub 0.6 on each `.sticky_list_wrapper`, from "top 85%" to "top 50%". The trigger element itself goes opacity 35%→100% and y 24→0. | Reduced motion: off. Phones: skip to end. |
| `i-4fd60c05` | Carousel card hover | Split hover (groups g-in and g-out) on `build_link` or `build_link Copy`. The card lifts −4px (trigger-only), **its** `.build_cover` scales to 1.03 and **its** arrow moves x +4. Both use `filterContext: relationship "within"` the card classes. Ease 8, 0.35 to 0.5s. | Reduced motion: off. **UNVERIFIED that "within" limits the effect to the hovered card.** Divit must hover one card in Preview; if all cards move, fix the target. |
| `i-a9d6f7ac` | Integration chip hover | Split hover on `.integration_chip`. It lifts −2px and the border colour goes to rgba(15,23,42,0.28); on hover out it returns to rgba(0,0,0,0.12). | Reduced motion: off. |

**Tab cross-fade:** handled by the native Webflow Tabs fade (300 in, 100 out), **not** IX3. An IX3 fade-in holds its target invisible until it's triggered, which would hide images.

**Hero subhead is not animated on purpose:** its classes are generic and used elsewhere.

**Rollback:** delete an interaction by its ID (one call each). Everything is logged in `INTERACTIONS.md`.

**IX3 API gotchas** (from Webflow's `guide` action; read it with `data_interactions_tool` → `guide`):
- **Timing:** `duration` is in seconds. `ease` is a preset index, not a string (2 = power1.out, 8 = power3.out, 26 = expo.out). `timing.delay` is rejected; use `position`.
- **Reveals must carry a start value.** Use `tt 2` with `[from, to]`, or `tt 1` with a `[from]` value. `tt 0` with a to-only value can be a silent no-op. A reveal holds its target invisible until the trigger fires.
- **Opacity** goes under `wf:transform`, not `wf:style`. `wf:style` allows only backgroundColor, borderColor, color, zIndex, position, overflow and pointerEvents.
- **Scroll triggers** need `start` and `end`. Use "top 85%" and 0.5s or longer for a reveal that's actually seen.
- **Mouse-move timelines** use `triggerMetadata.role` = `mouseX` or `mouseY`, and `canvasDuration: 1`.
- **`update_interaction`:** `timelines` is a **full replace**. Read the interaction back first with `get_interaction`.
- **API success doesn't prove it plays.** Verify in Designer Preview (the ▶ icon) or on a published page. Preview reopens at the section you were viewing.
- **Scope:** page scope needs `[pageId, elementId]` for `wf:inst` targets. Class targets (`wf:class` plus a style ID array) work with page scope, and a combo class is resolved to its chain automatically.

---

## 9. Current status and the plan ahead (ordered)

### Current status
- **All 4 hubs are in Draft.** All 4 child items are drafts. **Nothing from this work is public yet.**
- **Divit will "take them live in a bit".** He paused because he noticed the missing integrations section.
- **Divit confirmed working in Preview:** the in-image animations and the tilt. The strengthened reveal and the 4 newest interactions haven't been confirmed yet.
- **Live preview artifact** (motion demo of the Approval scenes): https://claude.ai/artifact/GhKBQ9Z9Tv6d4x82A5Qd9R

### P1: Integrations section on child pages (in discussion; **awaiting Divit's "go"**)
Divit showed his proposed design (a local file `hub-preview_5.html`, "Landing Page Hub" preview). It has two parts:
- **(A)** An eyebrow "CONNECT", the H2 "Every tool your landing page needs", and 3 category cards. Each card has an icon, a title, a description and 4–5 chips with coloured dots. Examples: Analytics & attribution (GA4, Meta Pixel, PostHog, Segment); Email & CRM (HubSpot, Mailchimp, ConvertKit, ActiveCampaign, Klaviyo); Payments & booking (Stripe, PayPal, Calendly, Cal.com).
- **(B)** A dark banner: "200+ integrations. Full API access." with "If it has an API, your landing page can talk to it. Emergent is open by design, no closed ecosystem.", an **Explore integrations** button, and 8 white tiles (Stripe, HubSpot, GA4, Meta, Slack, Mailchimp, PostHog, Segment).

**The "200+" claim is verified true:** the Integrations collection has 235 items.

**My recommendation, presented and awaiting a decision:**
1. **Child pages get (B), and skip (A).** (A) duplicates the hub, and per-page cards would need about 9 extra fields per page across 800 pages.
2. **Tiles come from each page's own `acrm---integration` multi-reference.** That gives page-specific tools, and each tile links to its integration page (`/integrations/<slug>`), up to 8 internal links per page.
3. **Real logos instead of dots:** add a new **"Logo"** image field to the Integrations collection (additive) and fill it with **Simple Icons** (CC0) SVG marks, verified per brand. The existing thumbnails are wide "Brand + Emergent" banners.
4. **A page-specific headline:** a new CMS field, e.g. "Connects to the tools your approval workflow runs on", next to "200+ integrations. Full API access." and the CTA to /integrations.
5. **Placement:** directly after the use-case tabs, on all 4 templates.
6. **Build method:** new, additive classes for the banner; the existing chip hover extended to the tiles if wanted.
7. **The one step I can't do by API:** pointing the tile Collection List at the item's own multi-reference field. It's **1 Designer click per template** (4 total). This is the same API limitation as related articles: a list source's `fieldId` is dropped.
8. **Only link to integrations that already have a page** in the collection, so no chip or tile ever goes to a dead page.

**Open question 1:** go ahead with B on the 4 child templates?
**Open question 2:** add the banner to the 4 hubs too, under the existing cards? First verify whether it already exists there (see §3.1).

**Implementation order once approved:**
1. Read the Integrations items and pick 8 relevant ones per child page from those that exist.
2. Add the Logo field.
3. Build the logo SVGs through the pipeline with gates.
4. Import them by URL.
5. Build the section with the element builder: new classes, a CollectionList, tiles with a logo image, name text and a link to the integration page.
6. Divit sets the list source (4 clicks, with exact steps).
7. Bind the tile fields.
8. Fill each item's `acrm---integration` references.
9. Verify in Preview, with screenshots.

### P2: Divit's Preview checks (pending his report)
1. Reload a hub and watch the H1 assemble word by word.
2. Scroll the how-to: the steps should brighten in turn.
3. **Hover one carousel card:** *only that card* should lift and zoom. If all cards move, fix `i-4fd60c05`'s target filter.
4. The reveal should now be noticeable.

### P3: Go live (only after P1, if Divit wants it first, and P2)
1. **I:** switch the 4 child items to published. That's `isDraft: false`, via `update_collection_items`, or `publish_collection_items` if needed.
2. **Divit:** turn off Draft on the 4 hub pages in Page settings. (The API may support `draft` via `bulk_update_pages`, but Divit has been doing it himself; ask.)
3. **Divit:** check no teammate is mid-edit, then Publish the site. This also makes the IX3 motion live.
4. **Both, post-launch:**
   - Rich Results Test on all 8 URLs.
   - **Confirm the FAQ schema on the child templates.** UNVERIFIED that the templates output FAQPage JSON-LD; the hubs do. If it's missing, add a template-level schema.
   - Sitemap and Search Console submission.
   - Check that the SVGs are served compressed (content-encoding).
   - Check mobile.
   - Check that the carousel cards show covers and Load more works.

### P4: Pending decisions and housekeeping (not blocking)
- **Child comparison tables put Emergent in the LAST column** ("Other Tools" first). The hubs have Emergent first. Open question from the earlier session: *should the child tables match the hubs?* Divit never answered, so ask.
- **Delete the hidden first-draft duplicate carousel** `86e5ccd1-891e-bb61-1762-8591adc90744` on the AAB and SQB hubs.
- **Clean up the category options per collection** ("CDK" leftovers; options shared across the cloned collections).
- **Test files `python.png` and `github.svg`:** used in the URL-import test on a draft item and then reverted. Clean them up if they appear in Assets. UNVERIFIED whether they're in Assets or only in CMS file storage.
- **Renew the GitHub token before 2026-12-28.**
- **Custom OG images for the 4 hubs:** optional.
- **Phase 2 automation:** a GitHub Action that renders and gates on every push (built-in GITHUB_TOKEN only). **Divit said: no Anthropic API key in the process.**
  - Image specs are written in-chat alongside page content.
  - QA is deterministic, plus a contact sheet for review.
  - Optional: a Webflow site token as a repo secret for hands-off CMS writes. Otherwise CMS writes happen in chat via MCP.
- **Next:** Divit names 5 child pages per hub, then the pipeline produces their 4 use-case images, cover and share image each. After that come **the next 2 hubs**.

---

## 10. Webflow workarounds and limitations (hard-won)

1. **A Collection List source can be locked.** This happens when elements in the card are bound to the old collection. Fix:
   1. Turn pagination off.
   2. In the Navigator, expand everything under the Collection Item, including hidden `hide` blocks.
   3. Clear every binding: Get text from; links (Collection page / Get URL from); images (Get image from); visibility conditions; dynamic styles; purple attributes.
   4. **Key trick, discovered by Divit:** change the `build_link` **link type from URL to Page**. That unlocked the source.
   5. Change the Source, re-bind everything, and re-add pagination: 15 per page, "Load more", plus the Finsweet attributes `fs-list-element=list` and `fs-list-load=more`.
   6. The API can also clear bindings. I did it once, to Divit's surprise ("wait how did you change it by yourself???").
2. **The API can't set a list source to a multi-reference field** (the `fieldId` is dropped). That needs a Designer click: Collection List settings → Source → the item's reference field. It applies to related articles and the integrations tiles.
3. **The OG image binding on collection templates is Designer-only.**
4. **Component edits change every instance.** The use-case component has 11 instances and "Global / Sticky List (Icons)" is shared site-wide. Change content through **instance props or CMS bindings only**, never the definition.
5. **`get_settings` can't read inside a component definition** ("Element not found"). Use `query_elements` with `scope_component_id` to read structure.
6. **The Designer caches images.** Hard-refresh (Cmd+Shift+R) after image swaps.
7. **Interactions only run in Preview or on a published page**, never on the Designer canvas.
8. **`data_cms_tool` action names:** `create_collection_static_field` (for an image field), `create_collection_option_field`, `create_collection_reference_field`, `update_collection_items`, `publish_collection_items` and so on. There's no generic `create_collection_field`.
9. **`data_element_builder`:** `settings` at creation only apply to DOM elements. For an image, create it with `set_style` first, then bind `assetId` with `set_settings`: `binding: {source_type: "cms", collection_id, field_id}`.
10. **`set_style` replaces all classes** on the element. That's safe only on elements that have no class, or when you pass the full list.
11. **Webflow Tabs have native fade settings** (Settings → Tabs settings → Fade in / Fade out / Easing).

---

## 11. Session timeline (condensed)

- **2026-09-23:** the developer created the AAB and SQB index pages and collections; the LP and Form pages already existed. Divit set the ground rules (approval, a plan first, rollback, touch nothing else, batches of 2 hubs). LP and Form copy work began from Divit's SEO docs.
- **2026-09-24:**
  - The Form carousel source lock was fixed (the developer unlinked a missed element; Divit then found the URL→Page trick).
  - The categories "Applications" and "Standalone Pages" were set up.
  - Child items were created: Creator Application and Thank You Page.
  - Templates were linked, and the §11 section placed.
- **2026-09-25:**
  - QC of the LP and Form hubs and child pages.
  - Learn links added; "Explore more articles", newest first.
  - Schema moved to the Schema markup field: WebPage + FAQPage + BreadcrumbList.
  - Carousels hidden for launch; staging reviewed.
- **2026-09-28:**
  - Copy audits (P0, P1, P2) implemented; the claims #1, #2 and #8 settled.
  - Tables restyled (Emergent first, darker alternating grey).
  - Chip logos and brand links done; 6 LP and Form value-card visuals.
  - AAB and SQB hubs built in full (copy, FAQs, schema, tables, chips, §11, carousel headings, value cards).
  - Keywords given: approval workflow; customer satisfaction survey. Divit: "fuck semrush, just create the content using logic".
- **2026-09-29:**
  - The AAB and SQB carousels were wired.
  - Two child items created (Approval, CSAT) and both templates bound.
  - The image pipeline was designed, since the scale is about 4,000 images. Divit created the GitHub repo and token.
  - Image versions v1 → v5: stretched, then soft, then vector, then world class.
  - Divit removed the Anthropic API key from the pipeline plan.
  - The IX3 reveal and tilt were added and strengthened; Divit confirmed the tabs fade.
  - The v5 system was rolled out to all 16 use-case images.
  - Carousel cover infrastructure was built by us (fields, class, 8 slots).
  - 4 covers and 4 share images went live; 4 more interactions were added; carousels were unhidden.
  - Divit noticed the child pages have no integrations section, which led to P1.
  - This handoff was written.

---

## 12. First moves in the new chat

1. `git clone https://github.com/seo881/potential-enigma.git /home/claude/pe && cd /home/claude/pe && bash pipeline/bootstrap.sh`. Expect "BOOTSTRAP OK".
2. Make the first Webflow MCP call with `session_id: "start"`, then reuse the issued ID.
3. **Re-read the live state before any write.** Things may have changed since this doc (Divit or the developer may have edited). At minimum:
   - the 4 hub pages' `draft` state;
   - the 4 child items;
   - the 6 interactions (`list_interactions`);
   - the integrations collection count.
4. Ask Divit for:
   - his decision on P1 (B on the child pages? the banner on the hubs?);
   - the results of his P2 Preview checks;
   - whether the child tables should put Emergent first (P4).
5. Then continue with P1 → P3, following §0 exactly.
