# Webflow API and MCP behaviours we learned the hard way

One row per behaviour: what the call does, what it actually publishes, and the rule we follow. Add a row whenever a read-back looked right and the published page did not.

| Date | Call | Read-back says | Published page does | Rule |
|---|---|---|---|---|
| 2026-10-13 | `data_element_settings_tool` set_settings `link` = `{mode: collectionPage, to: <pageSlug>}` on a Link Block inside a Collection List (carousel `build_link`, Learn `blog_link`) | `{mode: collectionPage, to: {pageSlug: detail_...}}`, exactly as written | renders the slug as a literal relative href (`/<hub>/detail_ai-<hub>-builder`, `/<hub>/detail_learn`), which 404s on every card | A collectionPage link is not proven by its read-back. Staging must resolve every card href and get HTTP 200 before any production go. Until a working API shape is confirmed, set these links in the Designer (Link Settings, collection page of the current item). |
| 2026-10-13 | `publish_collection_items` on CMS items | `publishedItemIds`, `errors: []` | items go live on emergent.sh without a site publish; template (Designer) changes stay staged | CMS changes go live only this way (no site publish, Divit 2026-10-10). |
| 2026-10-13 | MCP reads (`query_elements`, `get_settings`, `list_collection_items`) in quick succession | HTTP 429 `too_many_requests` | n/a | Wait about 75 s and retry the same read; never treat a 429 as a pass. |
