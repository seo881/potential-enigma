import json,re
LOGO="https://cdn.prod.website-files.com/6a0edf12ef1a8562ed56d806/6a0ef94db7f0a045fab57060_logo.svg"
T=lambda p:'{{wf {&quot;path&quot;:&quot;%s&quot;,&quot;type&quot;:&quot;PlainText&quot;\\} }}'%p
HUBS=[("lp","ai-landing-page-builder","AI Landing Page Builder"),("form","ai-form-builder","AI Form Builder"),
      ("aab","ai-automation-builder","AI Automation Builder"),("sqb","ai-survey-and-quiz-builder","AI Survey and Quiz Builder")]
def graph(p,h,slug,title,desc,crumb):
    u=f"https://emergent.sh/{p}/{slug}"
    return {"@context":"https://schema.org","@graph":[
     {"@type":"Organization","@id":"https://emergent.sh/#organization","name":"Emergent","url":"https://emergent.sh/","logo":LOGO},
     {"@type":"WebSite","@id":"https://emergent.sh/#website","url":"https://emergent.sh/","name":"Emergent","publisher":{"@id":"https://emergent.sh/#organization"}},
     {"@type":"WebPage","url":u,"name":title,"description":desc,"inLanguage":"en","isPartOf":{"@id":"https://emergent.sh/#website"},"publisher":{"@id":"https://emergent.sh/#organization"}},
     {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":"https://emergent.sh/"},
      {"@type":"ListItem","position":2,"name":h,"item":f"https://emergent.sh/{p}"},
      {"@type":"ListItem","position":3,"name":crumb,"item":u}]}]}
REAL={"lp":("thank-you-page","Thank You Page: Examples, Templates, Builder | Emergent","What a thank you page is, real examples, templates you can build in minutes. Custom thank you page for WooCommerce, Shopify or a standalone URL, free.","Thank You Page"),
 "form":("creator-application","Creator Application Form: Build Yours With AI | Emergent","Build a creator application form for your creator, ambassador or UGC program. Score every applicant and save each one to a database you own. Free to start.","Creator Application"),
 "aab":("approval-workflow","Approval Workflow: Build and Automate Approvals | Emergent","Build an approval workflow from a prompt: request form, multi-level routing, Slack and email alerts, escalation, and an audit log you own. Free to start.","Approval Workflow"),
 "sqb":("customer-satisfaction","Customer Satisfaction Survey Template & CSAT | Emergent","Build a customer satisfaction survey with CSAT, NPS, and CES questions. Tie every response to the customer and alert on low scores. Free to start.","Customer Satisfaction Survey")}
out=[]
for k,p,h in HUBS:
    s=json.dumps(graph(p,h,"@S@","@T@","@D@","@C@"),indent=2,ensure_ascii=False)
    for a,b in [("@S@","slug"),("@T@","meta-title"),("@D@","meta-description"),("@C@","acrm---breadcrumb")]: s=s.replace(a,T(b))
    raw='<script type="application/ld+json">\n'+s+'\n</script>'
    assert raw.count('{{wf')==5
    # render exactly as Webflow would with the live item values, then validate
    r=raw
    for f,v in zip(["slug","meta-title","meta-description","acrm---breadcrumb"],REAL[k]): r=r.replace(T(f),v)
    j=json.loads(re.sub(r'</?script[^>]*>','',r)); bl=j["@graph"][3]["itemListElement"]
    assert bl[2]["item"]==f"https://emergent.sh/{p}/{REAL[k][0]}" and all(i["name"] for i in bl)
    refs=set(re.findall(r'"@id": "([^"]+)"',json.dumps(j,indent=1))); ids={n.get("@id") for n in j["@graph"]}
    assert refs<=ids, refs-ids
    open(f"paste_{k}.txt","w").write(raw); out.append(k)
    print(k,"OK |",len(raw),"chars | 5 CMS fields | rendered breadcrumb:"," > ".join(i["name"] for i in bl))
