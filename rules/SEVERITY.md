# Severity table (Divit, 2026-10-07)

The one table the reviewer uses to decide whether a finding blocks. Every finding names its `class` from this table; `hubctl review` rejects a blocking finding whose class is not blocking here, and a note whose class is blocking. There is one review and one rework per page, then Divit reviews the previews. Notes ship: they are kept in `spec.review_notes` and feed the proposed-rules queue (`hubctl metrics`), and no one edits a page for a note.

| class | severity | what it covers | typical citations |
|---|---|---|---|
| untrue | blocking | A claim that is false: about Emergent (beyond `rules/capabilities.json`), about a competitor, about the world, or about the page's own content (a heading that one tab contradicts). | HUB_RULES 8; CONTENT_DEFECTS #8, #14 |
| unsourced | blocking | A statement of fact about the world (law, a third-party system, a professional standard, a statistic) with no matching `spec.domain_sources` entry, or a source that does not say it. A soft quantifier ("most", "many", "usually") blocks only when it states a fact about a named third party ("Many survey platforms log IP" sourced for one platform). | HUB_RULES 8; CONTENT_DEFECTS #7, #27 |
| wrong-fact | blocking | A wrong number, date, price, plan or competitor fact; numbers that disagree between fields or between copy and image; a weekday that does not match its date; a stale image date. | CONTENT_DEFECTS #10, #12, #13, #15 |
| structure | blocking | A required field, section, FAQ item or link missing or malformed; the FAQ not exactly 10 items; the hub link missing from FAQ 2; a table cell falling back to the hub default; a heading or field the template cannot render. Anything QC already blocks is structure. | HUB_RULES 5, 6; CONTENT_DEFECTS #11, #26 |
| image-contradiction | blocking | An image that tells a different story from its tab copy on names, numbers or outcomes; one company playing incompatible roles across tabs; an alert drawn to a channel when the copy names a person. | CONTENT_DEFECTS #20, #24, #25 |
| sibling-keyword | blocking | The page targets, headlines or answers a keyword or topic another page in the plan owns (`hubctl brief` lists the siblings). | CONTENT_DEFECTS #1 |
| missing-intent | blocking | The page does not deliver what the top 10 and PAA show searchers want (comparison, how-to, examples, template), or an FAQ answer never answers its question. | HUB_RULES 5 |
| repeated-idea | note | The same idea or phrase in several fields with words swapped. | CONTENT_DEFECTS #18, #21, #22 |
| soft-quantifier | note | "Most", "many", "usually", "often" in advice or about no named third party. | CONTENT_DEFECTS #7 |
| unsourced-advice | note | A recommendation (what the reader should do), not a statement of fact. | HUB_RULES 8 |
| craft | note | Tacked-on endings, run-on lists, from-to ranges, sentence rhythm, an FAQ answer that arrives in its second sentence. | HUB_RULES 2a, 5; CONTENT_DEFECTS #4, #6, #19 |
| voice | note | Wording that reads machine-written or could be sharper. | HUB_RULES 2b |
| openers | note | A paragraph or feature body that opens on a label or fragment. | CONTENT_DEFECTS #2, #16 |
| image-polish | note | Image layout or wording that could be better without contradicting the copy (engine gates already block empty panels, overflow, hero space, reserved domains and code covers). | CONTENT_DEFECTS #5, #28 |
| other | note | Anything else. | the rule it breaks |

**Not findings at all.** Template slots: the hero pitch restated in FAQ 2 (the hub-link answer), the hub name and the primary keyword where the template places them. These are never repeated ideas.

**How a reviewer uses it.** Read the page cold, decide the class of each defect, then the severity follows from the table; never argue a note up to blocking. A criterion in `rules/rubric.json` fails exactly when a blocking finding cites it.
