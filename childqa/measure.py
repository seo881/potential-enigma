import textwrap, re
P = {
"LP (Thank You Page)": {
 "H1":"Build a Custom Thank You Page in Minutes",
 "Hero subhead":"Describe the thank you page you need and Emergent generates it in minutes. A real page URL, a database write per submission, and the retargeting pixel injected on publish. Works after any form, on your own domain.",
 "Features H2":"Build, customize, and publish your thank you page with ease",
 "Features subhead":"Describe what should happen after a visitor converts and Emergent generates the whole thank you page: confirmation, delivery, next step, and the analytics and CRM wiring around it. Nothing bolted on later.",
 "Use-case H2":"Thank You Page Use Cases You Can Build in Minutes",
 "Why H2":"Why Choose Emergent for Building Your Thank You Page?",
 "Why subhead":"Build a thank you page that confirms the action, delivers on the promise, and moves the visitor to one clear next step, on a URL you control.",
 "feats":[("A real thank you page URL",232),("A database write per submission",214),("Any next step, generated to match",232),("Retargeting pixel and analytics injected",214),("Works everywhere your form does",225),("Full code export",181)]},
"Form (Creator Application)": {
 "H1":"Build a Creator Application Form Using AI in Minutes",
 "Hero subhead":"Describe your creator program and Emergent builds the application form, the screening logic and the creator database behind it. Review, approve and onboard creators without a spreadsheet in the middle.",
 "Features H2":"Everything a creator application form needs, in one build",
 "Features subhead":"Describe the creators you want and how you vet them. Emergent generates the form, the scoring, the review queue and the database behind it, with no response cap and nothing bolted on later.",
 "Use-case H2":"Creator Application Forms You Can Build in Minutes",
 "Why H2":"Why Build Your Creator Application Form With Emergent?",
 "Why subhead":"A creator program runs on who you accept. Emergent gives you the form, the screening and the creator roster in one build, with every application saved to a database you own.",
 "feats":[("Fields built for creator vetting",164),("Questions that change by platform",189),("Fit scoring the moment they apply",175),("Content samples and media kits",158),("A creator database you own",172),("Onboarding that starts on approval",176)]},
"AAB (Approval Workflow)": {
 "H1":"Build an Approval Workflow Your Team Actually Uses",
 "Hero subhead":"Describe the approval: what triggers it, who approves what, how it escalates, and where the record lands. Emergent builds the request form, the approval routing, the Slack and email alerts, and the audit log in one build. No code. No per-approver seats.",
 "Features H2":"Everything an approval workflow needs, in one build",
 "Features subhead":"Purchase order, invoice, contract, expense, or document approval. Emergent generates the request form, the routing rules, the alerts, and the audit database behind them, with every approver included and nothing bolted on later.",
 "Use-case H2":"Approval Workflows You Can Build in Minutes",
 "Why H2":"Why Build Your Approval Workflow With Emergent?",
 "Why subhead":"Most approval tools charge per user and keep the audit trail inside their own app. Emergent builds the approval workflow, the request form, and the audit log in one build, with every approver included.",
 "feats":[("Request form generated with the workflow",187),("Sequential, parallel, or multi-level routing",209),("Approve from Slack, Teams, or email",178),("Escalation timers and fallback approvers",174),("An audit trail in a database you own",174),("Full code export",165)]},
"SQB (Customer Satisfaction)": {
 "H1":"Build a Customer Satisfaction Survey That Feeds Your Whole Product",
 "Hero subhead":"Describe what you want to measure and who you are asking. Emergent builds the CSAT survey, the NPS and CES questions, the follow-ups by score, and a live dashboard, with every response tied to the customer in a database you own. No response caps.",
 "Features H2":"Everything a customer satisfaction survey needs, in one build",
 "Features subhead":"CSAT, NPS, CES, or all three. Emergent generates the questions, the branching by score, the alerts, and the response database behind them, with no response cap and nothing bolted on later.",
 "Use-case H2":"Customer Satisfaction Surveys You Can Build in Minutes",
 "Why H2":"Why Build Your Customer Satisfaction Survey With Emergent?",
 "Why subhead":"A customer satisfaction survey only pays off when a low score reaches someone who can act on it. Emergent ties every response to the customer, alerts on the scores that matter, and keeps every reply in a database you own.",
 "feats":[("CSAT, NPS, CES, and open text in one survey",201),("Every response tied to the customer",170),("Follow-up questions that change by score",160),("Alerts on low scores",170),("A live CSAT, NPS, and CES dashboard",162),("Responses in a database you own",170)]},
}
# limits proven on the hubs: section H2 <=48 (2 lines), subhead <=135 (2 lines); feature title must fit 2 lines @24ch, bodies within ~15 chars
for page,d in P.items():
    print(f"\n### {page}")
    for k in ["H1","Hero subhead","Features H2","Features subhead","Use-case H2","Why H2","Why subhead"]:
        s=d[k]; n=len(s)
        lim = 135 if "subhead" in k and k!="Hero subhead" else (48 if "H2" in k else None)
        flag = "" if lim is None else ("OK" if n<=lim else f"TOO LONG (>{lim})")
        print(f"  {k:17} {n:4}  {flag}")
    t=[(x,len(textwrap.wrap(x,24))) for x,_ in d["feats"]]; b=[y for _,y in d["feats"]]
    print("  feature titles >2 lines:", [x for x,l in t if l>2] or "none")
    print(f"  feature bodies: {b}  spread {max(b)-min(b)}")
