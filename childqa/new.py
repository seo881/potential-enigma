import json, textwrap
N = {
"lp": {
 "description":"Describe the thank you page you need and Emergent builds it in minutes: a real URL on your domain, a database write per submission, and the retargeting pixel set on publish.",
 "awb---integrations-heading":"Everything a thank you page needs, in one build",
 "acrm---key-feature-sub-heading":"Describe what happens after a visitor converts. Emergent builds the page, the next step, and the analytics and CRM wiring around it.",
 "acrm---usecase-heading":"Thank You Pages You Can Build in Minutes",
 "acrm---why-emergent-title":"Why Build Your Thank You Page With Emergent?",
 "acrm---why-emergent-description":"Confirm the action, deliver the promise, and move every visitor to one clear next step, on a URL you control and can track.",
 "feats":[
  ("A real thank you page URL","Every thank you page ships on its own URL on your domain, tracked as a conversion goal and targetable by a pixel. An inline form message can't be tracked or retargeted that way."),
  ("A database write per submission","Every visitor who lands on the page becomes a row in a database you own, with source, campaign, and referrer attached. Feed it to HubSpot, Mailchimp, or a dashboard the same day."),
  ("Any next step, generated to match","A demo booking after a lead magnet, a related product after a purchase, a calendar link after a form. Describe the next step and Emergent builds the block that leads to it."),
  ("Pixel and analytics set on publish","Meta Pixel, a GA4 conversion event, and any custom script fire when the page loads, all set up from the prompt. The page becomes a conversion goal and a retargeting source."),
  ("Works everywhere your form does","A custom thank you page for WooCommerce, a Shopify redirect, a WordPress form, or a standalone URL for any form. One build, every surface, one set of submissions in your database."),
  ("Full code export","The thank you page and the database it writes to both export to your GitHub. Keep hosting on Emergent or take it anywhere. Nothing is locked inside a plugin, theme, or vendor CRM.")],
 "faq_heading":"Thank You Page Questions, Answered"},
"form": {
 "description":"Describe your creator program and Emergent builds the application form, the screening logic, and the creator database behind it. Review, approve, and onboard creators in one place.",
 "awb---integrations-heading":"Everything a creator application form needs",
 "acrm---key-feature-sub-heading":"Describe the creators you want and how you vet them. Emergent builds the form, the scoring, the review queue, and the database behind it.",
 "acrm---usecase-heading":"Creator Applications You Can Build in Minutes",
 "acrm---why-emergent-title":"Why Build Creator Applications With Emergent?",
 "acrm---why-emergent-description":"A creator program runs on who you accept. Emergent builds the form, the screening, and the creator roster as one build you own.",
 "feats":[
  ("Fields built for creator vetting","Handle, platform, follower count, engagement rate, niche, audience location, rate card, and portfolio links, generated from your prompt. Add brand questions by describing them."),
  ("Questions that change by platform","Ask for TikTok, Instagram, or YouTube details only when a creator picks that platform. Multi-platform creators get one section per channel, so nobody sees questions that don't apply."),
  ("Fit scoring the moment they apply","Score each application on follower range, engagement, niche, and region as it arrives. Creators above your bar land in an approve queue; the rest get a waitlist or decline email."),
  ("Content samples and media kits","Accept portfolio links, video samples, and media kit PDFs in the same form. Every file is stored with its application, so reviewers see the creator's work right next to the numbers."),
  ("A creator database you own","Every application writes to a table in your project with status, score, and source. Push approved creators to Slack, HubSpot, or Airtable in the same prompt, with no response cap."),
  ("Onboarding that starts on approval","Approved creators get the next step automatically: a contract to sign, an affiliate link or discount code, or a product seeding request. The full code exports to your GitHub.")],
 "faq_heading":"Creator Application Questions, Answered"},
"aab": {
 "description":"Describe what triggers the approval, who signs off, and how it escalates. Emergent builds the request form, the routing, the Slack and email alerts, and the audit log. No per-approver seats.",
 "awb---integrations-heading":"Everything an approval workflow needs",
 "acrm---key-feature-sub-heading":"Purchase orders, invoices, contracts, and expenses. Emergent builds the request form, routing, alerts, and audit database behind them.",
 "acrm---usecase-heading":"Approval Workflows You Can Build in Minutes",
 "acrm---why-emergent-title":"Why Build Your Approval Workflow With Emergent?",
 "acrm---why-emergent-description":"Most approval tools charge per user and keep your audit trail in their app. Emergent includes every approver, and the audit log is yours.",
 "feats":[
  ("Request form generated with the workflow","The intake form is built with the approval workflow, not bolted on after. Every field maps to a routing rule, so the form and the process stay in sync when your policy changes."),
  ("Sequential, parallel, or multi-level routing","One approver at a time, several in parallel, tiers by amount, or branches by department. Describe a multi-level approval rule in one sentence and it becomes the routing logic."),
  ("Approve from Slack, Teams, or email","Every approver gets the request details and a one-click approve or reject in the channel they already use. The decision writes back to the workflow, with no separate portal."),
  ("Escalation timers and fallback approvers","If an approver hasn't acted within your SLA, send a reminder, escalate to their manager, or hand off to a fallback approver. Set the timing in the prompt and every step follows it."),
  ("An audit trail in a database you own","Every decision, reminder, and escalation lands in a table with requester, approver, amount, reason, and time to approve. Finance and audit query it directly, with no PDF exports."),
  ("Full code export","The request form, the approval routing, the alerts, and the audit database all export to your GitHub. Nothing is locked inside a per-seat tool or a proprietary workflow canvas.")],
 "faq_heading":"Approval Workflow Questions, Answered"},
"sqb": {
 "description":"Describe what you want to measure and who you are asking. Emergent builds the CSAT, NPS, and CES questions, the follow-ups by score, and a live dashboard, with every response in a database you own.",
 "awb---integrations-heading":"Everything a customer satisfaction survey needs",
 "acrm---key-feature-sub-heading":"CSAT, NPS, CES, or all three. Emergent builds the questions, the branching by score, the alerts, and the database behind them.",
 "acrm---usecase-heading":"Satisfaction Surveys You Can Build in Minutes",
 "acrm---why-emergent-title":"Why Build Your CSAT Survey With Emergent?",
 "acrm---why-emergent-description":"A survey only pays off when a low score reaches someone who can act. Emergent ties every response to the customer and alerts the owner.",
 "feats":[
  ("CSAT, NPS, CES, and open text in one survey","Every question type satisfaction research uses: a 1-5 CSAT scale, a 0-10 NPS question, a 1-7 CES scale, and open follow-ups. Add or remove a question by describing it."),
  ("Every response tied to the customer","Pass the customer ID, account, plan, or ticket ID with the survey link and every response is saved with that context. A low CSAT score becomes an account your team can call today."),
  ("Follow-up questions that change by score","Promoters get a review request, passives a feature question, and detractors an open follow-up. CSAT and effort scores branch the same way, included from the free tier."),
  ("Alerts on low scores","A Slack alert on every detractor, a HubSpot task on every low CSAT, and an email to the owner for key accounts. Every alert carries the score, the comment, and the customer."),
  ("A live CSAT, NPS, and CES dashboard","Generated with the survey and reading from the response database. Filter by segment, plan, or time window, and share one live view with your team instead of a monthly report."),
  ("Responses in a database you own","Every response lands in a table in your project, with no response cap. The survey, the dashboard, and every historical response export to your GitHub whenever you want.")],
 "faq_heading":"CSAT Survey Questions, Answered"},
}
lim={"description":205,"awb---integrations-heading":48,"acrm---key-feature-sub-heading":135,"acrm---usecase-heading":48,"acrm---why-emergent-title":48,"acrm---why-emergent-description":135}
bad=0
for p,d in N.items():
    out=[]
    for k,L in lim.items():
        n=len(d[k]); ok=n<=L; bad+=not ok; out.append(f"{k.split('---')[-1][:14]}={n}{'' if ok else '!'}")
    b=[len(x) for _,x in d["feats"]]; t=[len(textwrap.wrap(x,24)) for x,_ in d["feats"]]
    sp=max(b)-min(b); okf= sp<=15 and min(b)>=160 and max(b)<=190 and max(t)<=2; bad+=not okf
    for s in [v for v in d.values() if isinstance(v,str)]+[x for f in d["feats"] for x in f]:
        assert "\u2014" not in s and "\u2013" not in s and "Postgres" not in s
    print(p, " ".join(out), "| bodies", b, "spread", sp, "title lines", t, "OK" if okf else "FIX")
json.dump(N,open("new.json","w"),ensure_ascii=False)
print("problems:",bad)
