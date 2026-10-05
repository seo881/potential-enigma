import json, re, html, sys
src="/mnt/user-data/tool_results/mcp__Webflow__data_localization_tool_toolu_01DaruaQaWk53jYxc1NXUtVA.json"
d=json.load(open(src))
pages={}
for e in d:
    r=json.loads(e["text"]); lab=r["label"].split()[0]
    pages.setdefault(lab,[]).extend(r.get("result",{}).get("nodes",[]))
def strip(h): 
    h=re.sub(r'<style.*?</style>','',h,flags=re.S); h=re.sub(r'<script.*?</script>','',h,flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>',' ',h)).strip()
BRIT=r'\b(enquir\w*|colour\w*|favourit\w*|organis\w*|behaviour\w*|analys(e|ed|ing)\b|optimis\w*|customis\w*|recognis\w*|centre\w*|catalogue|licence|cancell\w*|prioritis\w*|personalis\w*|visualis\w*|categoris\w*|standardis\w*|utilis\w*|summaris\w*|minimis\w*|maximis\w*|emphasis(e|ed|ing)|programme)\b'
checks=[
 ("em/en dash", r'[\u2014\u2013]'),
 ("Postgres", r'Postgres'),
 ("first person we/our/us", r"\b([Ww]e|[Ww]e've|[Ww]e're|[Oo]ur|[Oo]urs|[Uu]s)\b"),
 ("British spelling", BRIT),
 ("double space", r'\S  +\S'),
 ("space before punctuation", r'\s[,.;:!?](\s|$)'),
 ("missing space after punct", r'[a-z][,;:][A-Za-z]|[a-z]\.[A-Z][a-z]'),
 ("repeated word", r'\b(\w+)\s+\1\b'),
 ("placeholder", r'(?i)lorem|ipsum|todo|tbd|placeholder|this is some text|xxx'),
 ("curly quote/apostrophe", r'[\u2018\u2019\u201c\u201d]'),
]
for p,nodes in pages.items():
    strings=[]
    for n in nodes:
        t=n.get("type")
        if t=="text": strings.append(("text:"+n["id"][-6:], strip(n.get("text",{}).get("html","") if isinstance(n.get("text"),dict) else n.get("html",""))))
        elif t=="component-instance":
            for po in n.get("propertyOverrides",[]):
                txt=po.get("text") or {}
                val = txt.get("html") if isinstance(txt,dict) else txt
                if val: strings.append((f"prop:{n['componentId'][:8]}/{po.get('propertyId','')[:8]}", strip(val)))
        elif t=="html-embed":
            s=strip(n.get("html",""))
            if s: strings.append(("embed:"+n["id"][-6:], s))
    print(f"\n######## {p}: {len(strings)} strings scanned")
    hits=0
    for name,rx in checks:
        for loc,s in strings:
            for m in re.finditer(rx,s):
                a=max(0,m.start()-45); hits+=1
                print(f"  [{name}] {loc}: …{s[a:m.end()+45]}…")
    # serial comma heuristic
    for loc,s in strings:
        for m in re.finditer(r'\b[\w/-]+(?: [\w/-]+)?, [\w/-]+(?: [\w/-]+){0,2} (and|or) [\w/-]+',s):
            seg=s[m.start():m.end()]
            if ', and ' in seg or ', or ' in seg: continue
            print(f"  [serial comma?] {loc}: {seg}")
    print(f"  total flagged (excl. serial-comma heuristic): {hits}")
json.dump({p:[(l,s) for l,s in []] for p in pages},open("pages_index.json","w"))
