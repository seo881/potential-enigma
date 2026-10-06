# 2026-10-06 child-page Phase 1 edits (approved by Divit)

Scope: 4 draft child items, 11 fields, text only. No templates, components, classes, images or hub pages touched.
`before.json` holds the exact prior value of every field changed, plus the collection and item IDs.
`full_snapshot_before.json` is the full read of all 4 items taken immediately before the writes.

Rollback for one item: data_cms_tool update_collection_items on that collection with
items: [{id, isDraft: true, fieldData: before.json[page].fields}]. Only those fields are sent.

Edits: LP meta description, feature 5, how-to step 6, 4 FAQ answers (Shopify claim, examples, templates, hub link), mockup "our"→"my";
Form FAQ application-limit answer (vendor numbers removed); AAB chip "Multi-Level Routing"; SQB hero (35→30 words) and feature 3 (unconfirmed free-tier claim removed, band kept).
