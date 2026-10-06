# Image brief (written by the page writer, rendered by the recipe library)

Content-first means the writer, who already knows each tab's story, writes a small structured brief for the six images in the same pass as the copy. The image stage then renders all briefs in bulk through the v5 recipe library, runs the gates, and produces one contact sheet per page. No image is designed by hand per page.

The brief lives in the spec under `image_brief`. Every number, name and status must agree with the tab copy (QC checks this when the recipe library lands).

```json
"image_brief": {
  "tabs": [
    {
      "tab": 1,
      "recipe": "R1",
      "moment": "The department head approves a $4,800 purchase request from Slack while the stepper shows 'In review'.",
      "prompt_chip": "Route purchase requests by amount and post each one to #approvals",
      "context": {"title": "PR-2041 Design licenses x12", "lines": ["$4,800.00 · Marketing", "Rule: $500-$5,000 to department head"],
                  "steps": [["Submitted", "done", "9:12 AM"], ["Manager", "skipped", "Not required"], ["Dept head", "live", "Priya Shah"], ["Sync to Xero", "next", ""]]},
      "hero": {"kind": "slack", "channel": "approvals", "title": "$4,800 purchase request", "lines": ["Design licenses x12", "Requested by Maya Chen"], "button": "Approve", "button2": "Decline", "click": true},
      "support": {"icon": "database", "title": "Every decision is logged", "sub": "Approver, amount and time saved"},
      "alt": "An Emergent prompt generates an approvals app that routes a $4,800 purchase request to the department head, who approves it from Slack."
    }
  ],
  "cover": {"moment": "One bold card: the $4,800 request with Approve clicked", "big_text": "$4,800 request", "sub": "Design licenses", "button": "Approve", "alt": "..."},
  "og": {"headline": "Build an approval workflow your team actually uses", "lines": null, "alt": "..."}
}
```

## Recipes (from IMAGE_PIPELINE_KT.md Part 7)
| Recipe | Layout | Use when the tab is about |
|---|---|---|
| R1 | App window + floating message hero | an approval, alert or notification arriving in Slack/email |
| R2 | Document + extraction + match | reading a document (invoice, receipt, form upload) |
| R3 | Document + parallel review | review, redlines, multiple reviewers |
| R4 | Phone + check + decision | mobile submission, a customer on a phone |
| R5 | Browser page + side cards | a page the customer sees (landing, thank you, booking) |
| R6 | Form + result | a form and what happens on submit |
| R7 | Wide board + bottom hero | a list or board of many entries |
| R8 | Rule bar + table + side hero | rules applied to rows (scoring, tiers, routing) |
| R9 | List + Slack hero | a scored shortlist delivered to a channel |
| R10 | Timeline + wide alert | something tracked over time (touchpoints, journey) |
| R11 | Table + alert + summary | per-account or per-agent metrics with an outlier |

## Rules for the brief
- One moment per tab, frozen at its most informative point; one hero.
- Fictional people and companies (Northwind, Globex, Initech, Acme are fine); real brands only as tools (Slack, Xero, HubSpot).
- Numbers add up, counts match rows, statuses agree, dates are in 2026.
- The prompt chip is one sentence in the user's voice, 60-85 characters.
- Alt text: specific, one or two sentences, no "image of".
- Text lengths are checked by the gates; if a value does not fit, the render fails and the brief is shortened (never the type size).

Status: schema draft. The recipe library that renders it is the next setup item (`SETUP_STATUS.md`). Until it lands, writers still write the brief so pages do not wait.
