import json
HEAD='''<style>
  .cmp--emg-first thead th.col-brand-head { background: #ebebeb; }
  .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; }
  .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; }
</style>
<div class="cmp cmp--emg-first">
  <table>
    <colgroup>
      <col class="col-feature" />
      <col class="col-brand" />
      <col class="col-other" />
      <col class="col-other" />
      <col class="col-other" />
    </colgroup>
    <thead>
      <tr>
        <th class="col-feature" scope="col"><span class="visually-hidden"></span></th>
        <th class="col-brand-head" scope="col">
          <img class="brand-logo" src="https://cdn.prod.website-files.com/6a0edf12ef1a8562ed56d806/6a0ef94db7f0a045fab57060_logo.svg" alt="emergent" />
        </th>
{comps}
      </tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
</div>'''
def table(comps, rows):
    c="\n".join(f'        <th scope="col">{x}</th>' for x in comps)
    r="\n".join(f'      <tr>\n        <th scope="row">{k}</th>\n        <td class="col-brand">{e}</td>\n'+"".join(f'        <td class="col-other">{o}</td>\n' for o in others)+'      </tr>' for k,e,*others in rows)
    return HEAD.replace("{comps}",c).replace("{rows}",r)
D={
"aab":{"comps":["Zapier","Make (Integromat)","n8n"],"rows":[
 ("How you build","Prompt for the workflow and the app around it","Templates and editor, AI copilot","Visual canvas","Visual canvas, self-hosted or cloud"),
 ("What you get","Workflow + trigger form + database + dashboard","The workflow only","The workflow only","The workflow only"),
 ("Metering unit","Usage credits, shared across every build","Per task — one action per run","Per credit — one module execution","Per execution — one full workflow run"),
 ("Free tier","Free tier with monthly credits","100 tasks/mo, 2-step Zaps only","1,000 credits/mo, 2 active scenarios","Cloud is paid-only; Community Edition self-hosted is free"),
 ("Entry paid plan","Free tier, then usage-based credits","Professional $19.99/mo annual for 750 tasks","Core $9/mo for 10,000 credits","Cloud Starter $24/mo for 2,500 executions"),
 ("Behavior at cap","No task or execution cap","Overage billed at up to 1.25× the base rate","Runs pause","Cloud runs stop entirely until the next reset"),
 ("AI and agent steps","Native, share the same credit pool","Priced by model tier, drawn from the task pool","AI modules cost variable credits","AI nodes count as executions"),
 ("Self-hosted option","Yes, exported to your repo","No","No","Yes (Community Edition)"),
 ("Code ownership","Full export to your repo","None","None","Yes on Community Edition")],
 "keep":["How you build","What you get","Behavior at cap","AI and agent steps","Code ownership"]},
"sqb":{"comps":["SurveyMonkey","Typeform","Interact (quiz specialist)"],"rows":[
 ("How you build","Prompt for the survey, quiz, or poll and the app around it","Templates and editor","Templates and editor, AI assist","Templates and AI quiz maker"),
 ("Response limits","None","Basic 25/survey, Advantage 15,000/year, Team Advantage 50,000/year","Free 10/mo, Basic 100/mo (form stops at cap)","Lite 500 leads/mo, Growth 2,000 leads/mo (quiz stops at cap)"),
 ("Behavior at cap","No cap","Overage billed at $0.15 per extra response","Form stops collecting","Quiz stops collecting"),
 ("Skip logic and branching","Included from the free tier","Advantage and up","Basic and up","Included"),
 ("Weighted scoring for quizzes","Native, generated with the quiz","Not designed for it","Manual to build","Native"),
 ("Custom domain","Built in, uses credits","Enterprise only","Custom subdomain from Plus","Paid plans"),
 ("Where responses live","A database table you own, plus any integration","SurveyMonkey account","Typeform account","Interact account"),
 ("Code ownership","Full export to your repo","None","None","None"),
 ("Starting price","Free tier, then credits","Free (10 questions, 25 responses/survey), Advantage $46/mo annual","Free (10 responses/mo), Basic $28/mo annual","$27/mo annual for 500 leads")],
 "keep":["How you build","Response limits","Behavior at cap","Where responses live","Code ownership"]},
"lp":{"comps":["Unbounce","Landingi / Leadpages / Instapage","AI site builders (Wix, Framer)"],"rows":[
 ("How you build","Prompt for a campaign page","Templates and drag-and-drop, AI copy assist","Templates and drag-and-drop, AI assist","Prompt for a full site"),
 ("Where submissions go","A database table you own, plus integrations","Unbounce lead storage and integrations","Vendor lead storage and integrations","Basic contact form to email"),
 ("Visitor limits","No per-visitor pricing","500/mo on Starter, 20,000/mo on Build, 30,000/mo on Experiment","Tiered by traffic on most plans","Site plan bandwidth"),
 ("Page limits","Unlimited","5 pages on Starter, unlimited from Build","Tiered on lower plans","Unlimited within the site"),
 ("Multi-step and conditional forms","Included","Form builder included, logic varies by plan","Varies by plan","Not built for it"),
 ("A/B testing","Generate variants by prompt","From Experiment plan ($112/mo annual)","Higher plans","Limited or add-on"),
 ("Code ownership","Full export to your repo","Hosted only","Hosted only","Hosted only"),
 ("Custom domain","Built in, uses credits","Not on Starter","On paid plans","On paid plans"),
 ("Starting price","Free tier, then credits","$22/mo annual, $29 monthly","Varies","Site plan")],
 "keep":["How you build","Where submissions go","Visitor limits","A/B testing","Code ownership"]},
"form":{"comps":["Google Forms","Typeform","Jotform"],"rows":[
 ("How you build","Prompt","Manual, field by field","Templates, editor, AI assist","Templates, editor, AI generator"),
 ("Response limits","None","None","10/mo free, 100 Basic, 1,000 Plus, 10,000 Business (form closes at cap)","100/mo free, 1,000 Bronze, 2,500 Silver, 10,000 Gold (form stops at cap)"),
 ("Form limits","Unlimited","None","Unlimited forms","5 free, 25 Bronze, 50 Silver, 100 Gold"),
 ("Where responses live","A database table you own, plus any integration","Google Sheets","Typeform account","Jotform account"),
 ("Conditional logic","Included","Basic section branching","Included from Basic","Included"),
 ("Payments in the form","Included","No","Paid plans","Included, metered per plan"),
 ("Custom domain","Built in, uses credits","No","Custom subdomain from Plus","Paid plans"),
 ("Code ownership","Full export to your repo","None","None","None"),
 ("Starting price","Free tier, then credits","Free","$28/mo annual, $39 monthly","$34/mo annual, $39 monthly")],
 "keep":["How you build","Response limits","Where responses live","Payments in the form","Code ownership"]},
}
out={}
for k,v in D.items():
    keep=[r for r in v["rows"] if r[0] in v["keep"]]; assert len(keep)==5,k
    out[k]={"new":table(v["comps"],keep),"old":table(v["comps"],v["rows"])}
    open(f"{k}_hub_5row.html","w").write(out[k]["new"]); open(f"{k}_hub_original.html","w").write(out[k]["old"])
json.dump({k:v["new"] for k,v in out.items()},open("new_tables.json","w"))
for k in out: print(k, [r[0] for r in D[k]["rows"] if r[0] in D[k]["keep"]], len(out[k]["new"]),"chars")
