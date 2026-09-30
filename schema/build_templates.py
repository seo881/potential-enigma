import json, re
LOGO="https://cdn.prod.website-files.com/6a0edf12ef1a8562ed56d806/6a0ef94db7f0a045fab57060_logo.svg"
def B(path): return '{{wf {&quot;path&quot;:&quot;%s&quot;,&quot;type&quot;:&quot;PlainText&quot;\\} }}' % path
HUBS={ # template page id: (hub path, hub name)
 "lp":  ("6aaaa937fe1a8d180b7c9f90","ai-landing-page-builder","AI Landing Page Builder"),
 "form":("6aaaaa03995bb2f9f4d6a3c2","ai-form-builder","AI Form Builder"),
 "aab": ("6ab2470540448c8f7d1ccc1c","ai-automation-builder","AI Automation Builder"),
 "sqb": ("6ab24754757025d10940d06a","ai-survey-and-quiz-builder","AI Survey and Quiz Builder")}
def graph(hub, name, slug, title, desc, crumb):
    base=f"https://emergent.sh/{hub}/{slug}"
    return {"@context":"https://schema.org","@graph":[
     {"@type":"Organization","@id":"https://emergent.sh/#organization","name":"Emergent","url":"https://emergent.sh/","logo":LOGO},
     {"@type":"WebSite","@id":"https://emergent.sh/#website","url":"https://emergent.sh/","name":"Emergent","publisher":{"@id":"https://emergent.sh/#organization"}},
     {"@type":"WebPage","@id":base+"#webpage","url":base,"name":title,"description":desc,"inLanguage":"en",
      "isPartOf":{"@id":"https://emergent.sh/#website"},"breadcrumb":{"@id":base+"#breadcrumb"},"publisher":{"@id":"https://emergent.sh/#organization"}},
     {"@type":"BreadcrumbList","@id":base+"#breadcrumb","itemListElement":[
       {"@type":"ListItem","position":1,"name":"Home","item":"https://emergent.sh/"},
       {"@type":"ListItem","position":2,"name":name,"item":f"https://emergent.sh/{hub}"},
       {"@type":"ListItem","position":3,"name":crumb,"item":base}]}]}
out={}
for k,(pid,hub,name) in HUBS.items():
    # Build with sentinel values, then swap sentinels for Webflow CMS bindings (keeps JSON structure machine-built)
    g=graph(hub,name,"@@SLUG@@","@@TITLE@@","@@DESC@@","@@CRUMB@@")
    s=json.dumps(g,indent=2,ensure_ascii=False)
    for sent,path in [("@@SLUG@@","slug"),("@@TITLE@@","meta-title"),("@@DESC@@","meta-description"),("@@CRUMB@@","acrm---breadcrumb")]:
        s=s.replace(sent,B(path))
    raw='<script type="application/ld+json">\n'+s+'\n</script>'
    out[k]={"page_id":pid,"raw":raw}
    open(f"template_{k}.jsonld.html","w").write(raw)
json.dump(out,open("templates.json","w"),indent=1)
# Validate: render each template with the REAL live item values, as Webflow would, and check it
REAL={
 "lp":("thank-you-page","Thank You Page: Examples, Templates, Builder | Emergent","What a thank you page is, real examples, templates you can build in minutes. Custom thank you page for WooCommerce, Shopify or a standalone URL, free.","Thank You Page"),
 "aab":("approval-workflow","Approval Workflow: Build and Automate Approvals | Emergent","Build an approval workflow from a prompt: request form, multi-level routing, Slack and email alerts, escalation, and an audit log you own. Free to start.","Approval Workflow"),
}
for k,(slug,t,d,c) in REAL.items():
    r=out[k]["raw"]
    for path,val in [("slug",slug),("meta-title",t),("meta-description",d),("acrm---breadcrumb",c)]:
        r=r.replace(B(path),val)
    j=json.loads(re.sub(r'</?script[^>]*>','',r))
    ids={n["@id"] for n in j["@graph"]}
    refs=re.findall(r'"@id": "([^"]+)"',json.dumps(j,indent=1))
    dangling=[x for x in refs if x not in ids]
    bl=[n for n in j["@graph"] if n["@type"]=="BreadcrumbList"][0]["itemListElement"]
    assert [i["position"] for i in bl]==[1,2,3] and all(i["name"] and i["item"].startswith("https://emergent.sh") for i in bl)
    assert not dangling, dangling
    print(k,"OK: parses, 4 nodes, breadcrumb", " > ".join(i["name"] for i in bl), "| dangling refs: none (FAQ node added by script)")
print(open("template_aab.jsonld.html").read()[:1400])
