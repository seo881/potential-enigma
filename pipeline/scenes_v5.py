"""Design system v4 — reference quality. 1200x800 (3:2 slot), vector-only output."""
import re, math, os
ICON_DIR='/home/claude/lucide/package/icons/'
# ---------- tokens ----------
INK="#0F172A"; SUB="#475569"; MUTED="#64748B"; LINE="#E6E3F0"; HAIR="#EEEBF5"
ACC="#7C3AED"; ACC2="#6366F1"; ACC_D="#5B21B6"; ACC_S="#F1ECFF"; ACC_M="#DDD3FF"
OK="#15803D"; OK_S="#DCFCE7"; WARN="#B45309"; WARN_S="#FEF3C7"; BAD="#B91C1C"; BAD_S="#FEE2E2"
W,H=1200,800
_ic={}
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def T(x,y,s,size=18,w=500,fill=INK,anchor="start",ls=0,tnum=False,op=None):
    a=f' data-tnum="1"' if tnum else ''
    o=f' opacity="{op}"' if op is not None else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}"{a}{o}>{esc(s)}</text>'
def icon(name,x,y,size=20,color=INK,sw=2,fill="none"):
    if name not in _ic:
        s=open(ICON_DIR+name+'.svg').read(); _ic[name]=re.sub(r'<!--.*?-->','',s.split('>',1)[1].rsplit('</svg>',1)[0].split('>',1)[1],flags=re.S)
    k=size/24
    return f'<g transform="translate({x} {y}) scale({k:.4f})" fill="{fill}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{_ic[name]}</g>'
def rect(x,y,w,h,r=16,fill="#fff",stroke=None,sw=1,f=None,op=None):
    s=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}{f" filter=\"url(#{f})\"" if f else ""}{f" opacity=\"{op}\"" if op is not None else ""}/>'
def chip(x,y,label,kind="acc",w=None,h=36,size=16,dot=True):
    bg,fg={"acc":(ACC_S,ACC_D),"ok":(OK_S,OK),"warn":(WARN_S,WARN),"bad":(BAD_S,BAD),"n":("#F1F5F9","#475569")}[kind]
    w=w or int(len(label)*size*0.56+ (38 if dot else 28))
    d=f'<circle cx="{x+16}" cy="{y+h/2}" r="4" fill="{fg}"/>' if dot else ''
    return rect(x,y,w,h,h/2,bg)+d+T(x+(28 if dot else w/2),y+h/2+size*0.36,label,size,600,fg,"start" if dot else "middle")
def button(x,y,w,h,label,primary=True,ic=None):
    if primary:
        b=rect(x,y,w,h,12,"url(#gAcc)")
        fg="#fff"
    else:
        b=rect(x,y,w,h,12,"#fff",LINE,1.5); fg=INK
    tw=len(label)*17*0.56; ox=x+w/2-(tw+(26 if ic else 0))/2
    if ic: b+=icon(ic,ox,y+h/2-10,20,fg,2.4)
    return b+T(ox+(26 if ic else 0),y+h/2+6,label,17,600,fg)
def avatar(cx,cy,r,ini=None,c1="#A78BFA",c2="#6366F1",gid=None):
    g=gid or f"av{abs(hash((c1,c2)))%9999}"
    s=f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="{r+2}" fill="#fff"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{g})"/>'
    if ini: s+=T(cx,cy+r*0.3,ini,max(16,int(r*0.8)),700,"#fff","middle")
    return s
def cursor(x,y):
    return (f'<g filter="url(#e1)"><path d="M{x} {y} l0 30 l8 -7 l6 13 l6 -3 l-6 -13 l11 -1 z" fill="{INK}" stroke="#fff" stroke-width="2" stroke-linejoin="round"/></g>')
STYLE='''<style>
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s cubic-bezier(.2,.7,.3,1) infinite}
@keyframes pulse{0%{transform:scale(1);opacity:.30}75%{transform:scale(2.1);opacity:0}100%{transform:scale(2.1);opacity:0}}
.caret{animation:blink 1.1s steps(1) infinite}
@keyframes blink{0%,55%{opacity:1}56%,100%{opacity:0}}
.press{transform-box:fill-box;transform-origin:0 0;animation:press 3.2s ease-in-out infinite}
@keyframes press{0%,58%,100%{transform:translate(0,0) scale(1)}66%{transform:translate(1.5px,2px) scale(.9)}74%{transform:translate(0,0) scale(1)}}
.ripple{transform-box:fill-box;transform-origin:center;opacity:0;animation:ripple 3.2s ease-out infinite}
@keyframes ripple{0%,62%{opacity:0;transform:scale(.4)}68%{opacity:.5}100%{opacity:0;transform:scale(2.4)}}
.sweep{animation:sweep 4.8s cubic-bezier(.45,0,.2,1) infinite}
@keyframes sweep{0%{transform:translateY(-470px);opacity:0}8%{opacity:1}72%{transform:translateY(0);opacity:1}100%{transform:translateY(0);opacity:1}}
.ring{transform-box:fill-box;transform-origin:50% 12%;animation:ring 4s ease-in-out infinite}
@keyframes ring{0%,70%,100%{transform:rotate(0)}74%{transform:rotate(14deg)}78%{transform:rotate(-12deg)}82%{transform:rotate(8deg)}86%{transform:rotate(-4deg)}90%{transform:rotate(0)}}
.glow{animation:glow 2.6s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:1}50%{opacity:.45}}
.float{animation:float 6s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
</style>'''
def defs(extra=""):
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FCFBFF"/><stop offset="1" stop-color="#EFE9FF"/></linearGradient>
<radialGradient id="glowA" cx="0.12" cy="0.08" r="0.55"><stop offset="0" stop-color="#E2D6FF" stop-opacity="0.95"/><stop offset="1" stop-color="#E2D6FF" stop-opacity="0"/></radialGradient>
<radialGradient id="glowB" cx="0.92" cy="0.96" r="0.5"><stop offset="0" stop-color="#E7DDFF" stop-opacity="0.9"/><stop offset="1" stop-color="#E7DDFF" stop-opacity="0"/></radialGradient>
<linearGradient id="gAcc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7C3AED"/><stop offset="1" stop-color="#4F46E5"/></linearGradient>
<linearGradient id="gStroke" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#A78BFA"/><stop offset="1" stop-color="#818CF8"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#6D28D9" stroke-opacity="0.07" stroke-width="1"/></pattern>
<radialGradient id="fade" cx="0.5" cy="0.45" r="0.65"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="gridMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<filter id="e1" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-color="#1E1B4B" flood-opacity="0.07"/><feDropShadow dx="0" dy="12" stdDeviation="18" flood-color="#2E1065" flood-opacity="0.08"/></filter>
<filter id="e2" x="-15%" y="-15%" width="130%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#1E1B4B" flood-opacity="0.10"/><feDropShadow dx="0" dy="28" stdDeviation="34" flood-color="#2E1065" flood-opacity="0.20"/></filter>
<radialGradient id="spot" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#8B5CF6" stop-opacity="0.26"/><stop offset="1" stop-color="#8B5CF6" stop-opacity="0"/></radialGradient>
{extra}</defs>
{STYLE}'''
def canvas(body,extra="",title="",desc=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Inter" role="img"><title>{esc(title)}</title><desc>{esc(desc)}</desc>{defs(extra)}'
            f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#glowA)"/><rect width="{W}" height="{H}" fill="url(#glowB)"/>'
            f'<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridMask)"/>{body}</svg>')
def window(x,y,w,h,title,active=0,icons=("inbox","workflow","chart-column","settings"),avatars=True):
    b=rect(x,y,w,h,18,"#fff",LINE,1,"e1")
    b+=f'<path d="M{x} {y+48} V{y+18} a18 18 0 0 1 18 -18 H{x+w-18} a18 18 0 0 1 18 18 V{y+48} Z" fill="#FBFAFE"/><line x1="{x}" y1="{y+48}" x2="{x+w}" y2="{y+48}" stroke="{HAIR}" stroke-width="1.5"/>'
    for i in range(3): b+=f'<circle cx="{x+24+i*18}" cy="{y+24}" r="6" fill="#E4E1EC"/>'
    b+=icon("workflow",x+w/2-72,y+14,20,ACC,2.2)+T(x+w/2-44,y+30,title,17,600,"#334155")
    if avatars:
        for i,(c1,c2) in enumerate([("#F9A8D4","#A78BFA"),("#2563EB","#4338CA"),("#047857","#115E59")]):
            b+=avatar(x+w-78+i*20,y+24,11,None,c1,c2,gid=f"wav{i}{x}")
    b+=f'<rect x="{x}" y="{y+48}" width="64" height="{h-48}" fill="#FAF9FD"/><path d="M{x} {y+h-18} a18 18 0 0 0 18 18 H{x+64} V{y+h-18} Z" fill="#FAF9FD"/><line x1="{x+64}" y1="{y+48}" x2="{x+64}" y2="{y+h}" stroke="{HAIR}" stroke-width="1.5"/>'
    for i,ic in enumerate(icons):
        cy=y+80+i*52
        if i==active: b+=rect(x+12,cy-20,40,40,11,ACC_S)
        b+=icon(ic,x+22,cy-10,20,ACC if i==active else "#94A3B8",2)
    return b
def spot(x,y,w,h):
    return f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w*0.78}" ry="{h*0.95}" fill="url(#spot)"/>'
def prompt(x,y,w,text,h=84):
    b=rect(x,y,w,h,18,"#fff","url(#gStroke)",1.5,"e2")
    b+=f'<circle cx="{x+40}" cy="{y+h/2}" r="21" fill="url(#gAcc)"/>'+icon("sparkles",x+29,y+h/2-11,22,"#fff",2)
    b+=T(x+76,y+h/2-8,"Emergent prompt",16,600,ACC_D)+T(x+76,y+h/2+20,text,19,500,INK)
    from qa import width as _w
    cx=x+76+_w(text,19,500)+4
    b+=f'<rect class="caret" x="{cx:.1f}" y="{y+h/2+2}" width="2.5" height="24" rx="1.25" fill="{ACC}"/>'
    kx=x+w-96
    assert cx+26<=kx, f'prompt too long for chip: caret at {cx:.0f}, keycaps at {kx}'
    for i,ic in enumerate(["command","corner-down-left"]):
        b+=rect(kx+i*40,y+h/2-16,32,32,8,"#F6F4FC","#E2DDF0",1.2)+icon(ic,kx+i*40+7,y+h/2-9,18,SUB,2)
    return b

# ---------------- 1 · Purchase order ----------------
def po():
    b=prompt(60,40,860,"“Route purchase requests by amount and post each one to #approvals”")
    b+=f'<path d="M104 124 V164" stroke="url(#gStroke)" stroke-width="2" stroke-dasharray="3 6" stroke-linecap="round"/>'
    b+=window(60,164,700,596,"Approvals",0)
    X=156; R=696
    b+=T(X,250,"PR-2041 · MARKETING",16,600,MUTED,ls=1)
    b+=T(X,288,"Design licenses ×12",28,700,INK,ls=-0.4)+T(X,318,"Requested by Nina Park · Figma, approved vendor",17,500,SUB)
    b+=T(R,288,"$4,800.00",30,700,INK,"end",-0.3,True)+T(R,318,"USD",16,600,MUTED,"end")
    b+=rect(X,342,R-X,46,12,ACC_S)+icon("git-branch",X+14,353,22,ACC_D,2)+T(X+46,371,"Rule matched: $500 to $5,000 → Department head",17,600,ACC_D)
    steps=[("done","Submitted","Nina Park · Design licenses ×12"),("skip","Manager review","Not required for this amount"),("live","Department head","Priya Shah · decision requested in #approvals"),("next","Sync to Xero","Bill created after approval")]
    for i,(st,ti,su) in enumerate(steps):
        cy=448+i*78
        if i<3: b+=f'<line x1="{X+18}" y1="{cy+18}" x2="{X+18}" y2="{cy+60}" stroke="{ACC_M if i<2 else HAIR}" stroke-width="2.5" {"stroke-dasharray=\"4 6\"" if i==0 else ""}/>'
        if st=="done": b+=f'<circle cx="{X+18}" cy="{cy}" r="16" fill="{OK_S}"/>'+icon("check",X+8,cy-10,20,OK,2.6)
        if st=="skip": b+=f'<circle cx="{X+18}" cy="{cy}" r="15" fill="#fff" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="3 4"/>'
        if st=="live": b+=f'<circle class="pulse" cx="{X+18}" cy="{cy}" r="18" fill="{ACC}" opacity="0.3"/><circle cx="{X+18}" cy="{cy}" r="24" fill="{ACC}" opacity="0.12"/><circle cx="{X+18}" cy="{cy}" r="16" fill="url(#gAcc)"/><circle cx="{X+18}" cy="{cy}" r="5" fill="#fff"/>'
        if st=="next": b+=f'<circle cx="{X+18}" cy="{cy}" r="15" fill="#fff" stroke="#CBD5E1" stroke-width="2"/>'
        col=MUTED if st in("skip","next") else INK
        b+=T(X+52,cy-4,ti,20,600,col)+T(X+52,cy+22,su,16,500,MUTED)
        if st=="live": b+=chip(R-112,cy-18,"In review","acc",112)
        if st=="done": b+=T(R,cy+2,"9:12 AM",16,600,MUTED,"end",tnum=True)
    # hero: approval message
    N=(730,196,410,300)
    b+=spot(*N)+rect(*N,20,"#fff",LINE,1,"e2")
    b+=icon("hash",N[0]+24,N[1]+22,20,SUB,2.2)+T(N[0]+50,N[1]+38,"approvals",18,700,INK)+T(N[0]+N[2]-24,N[1]+38,"now",16,600,MUTED,"end")
    b+=f'<line x1="{N[0]}" y1="{N[1]+60}" x2="{N[0]+N[2]}" y2="{N[1]+60}" stroke="{HAIR}" stroke-width="1.5"/>'
    b+=rect(N[0]+24,N[1]+80,44,44,12,"url(#gAcc)")+icon("sparkles",N[0]+35,N[1]+91,22,"#fff",2)
    b+=T(N[0]+82,N[1]+98,"Emergent",18,700,INK)+rect(N[0]+172,N[1]+81,48,24,6,"#F1F5F9")+T(N[0]+196,N[1]+98,"APP",16,700,SUB,"middle")
    b+=T(N[0]+82,N[1]+130,"Nina Park requested $4,800",18,500,INK,tnum=True)+T(N[0]+82,N[1]+156,"for Design licenses ×12",18,500,INK)
    b+=T(N[0]+82,N[1]+186,"Marketing · approved vendor",16,500,MUTED)
    b+=button(N[0]+82,N[1]+214,150,50,"Approve",True,"check")+button(N[0]+244,N[1]+214,130,50,"Decline",False)
    b+=f'<circle class="ripple" cx="{N[0]+206}" cy="{N[1]+250}" r="14" fill="{ACC}"/>'
    b+='<g class="press">'+cursor(N[0]+206,N[1]+250)+'</g>'
    # secondary floating: audit trail
    A=(770,540,370,104)
    b+=rect(*A,18,"#fff",LINE,1,"e1")+rect(A[0]+20,A[1]+28,48,48,12,OK_S)+icon("database",A[0]+32,A[1]+40,24,OK,2)
    b+=T(A[0]+84,A[1]+46,"Every decision is logged",18,700,INK)+T(A[0]+84,A[1]+74,"Approver chain and timestamps",16,500,MUTED)
    return canvas(b,title='Purchase order approval workflow',desc='An Emergent prompt generates an approvals app that routes a $4,800 request to the department head, who approves it from a Slack message.')

# ---------------- 2 · Invoice ----------------
def invoice():
    b=prompt(60,40,960,"“Read each invoice, match it to its PO, and route anything over $1,000 to finance”")
    P=(60,164,440,596)
    b+=rect(*P,14,"#fff",LINE,1,"e1")
    b+=rect(P[0]+32,P[1]+34,52,52,14,"url(#gAcc)")+T(P[0]+58,P[1]+67,"NS",18,800,"#fff","middle")
    b+=T(P[0]+100,P[1]+56,"Northwind Supplies",20,700,INK)+T(P[0]+100,P[1]+80,"billing@northwind.co",16,500,MUTED)
    b+=T(P[0]+P[2]-32,P[1]+56,"INVOICE",16,700,MUTED,"end",2.5)
    rows=[("Invoice no.","INV-7731",False),("PO reference","PO-2231",True),("Due date","Nov 12, 2026",False)]
    for i,(k,v,hl) in enumerate(rows):
        y=P[1]+128+i*62
        if hl: b+=rect(P[0]+20,y-8,P[2]-40,56,12,ACC_S,ACC,2)
        b+=T(P[0]+36,y+16,k,16,500,SUB if hl else MUTED)+T(P[0]+36,y+40,v,19,700,INK,tnum=True)
    ty=P[1]+334
    b+=f'<line x1="{P[0]+32}" y1="{ty}" x2="{P[0]+P[2]-32}" y2="{ty}" stroke="{HAIR}" stroke-width="1.5"/>'
    for i,(it,amt) in enumerate([("Packaging supplies","$1,420.00"),("Label printing","$640.00"),("Freight","$280.00")]):
        y=ty+36+i*38; b+=T(P[0]+36,y,it,17,500,SUB)+T(P[0]+P[2]-36,y,amt,17,600,INK,"end",tnum=True)
    b+=rect(P[0]+20,ty+140,P[2]-40,62,12,ACC_S,ACC,2)+T(P[0]+36,ty+178,"Total due",18,700,INK)+T(P[0]+P[2]-36,ty+178,"$2,340.00",22,800,INK,"end",-0.2,True)
    # scan beam
    b+=f'<defs><linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACC}" stop-opacity="0"/><stop offset="1" stop-color="{ACC}" stop-opacity="0.16"/></linearGradient></defs>'
    b+=f'<g class="sweep"><rect x="{P[0]+1}" y="{P[1]+476}" width="{P[2]-2}" height="84" fill="url(#beam)"/><line x1="{P[0]+1}" y1="{P[1]+560}" x2="{P[0]+P[2]-1}" y2="{P[1]+560}" stroke="{ACC}" stroke-width="2.5" stroke-opacity="0.7"/></g>'
    b+=rect(P[0]+P[2]-150,P[1]+545,128,30,15,ACC)+icon("scan-line",P[0]+P[2]-140,P[1]+550,20,"#fff",2)+T(P[0]+P[2]-114,P[1]+566,"Scanned",16,600,"#fff")
    # extraction panel
    E=(560,164,580,330)
    b+=rect(*E,18,"#fff",LINE,1,"e1")+icon("sparkles",E[0]+26,E[1]+24,22,ACC,2)+T(E[0]+58,E[1]+42,"Extracted fields",19,700,INK)+chip(E[0]+E[2]-148,E[1]+20,"4 of 4 found","ok",128)
    b+=f'<line x1="{E[0]}" y1="{E[1]+70}" x2="{E[0]+E[2]}" y2="{E[1]+70}" stroke="{HAIR}" stroke-width="1.5"/>'
    for i,(k,v,c) in enumerate([("Vendor","Northwind Supplies",99),("PO reference","PO-2231",100),("Total","$2,340.00",99),("Due date","Nov 12, 2026",97)]):
        y=E[1]+112+i*56
        b+=T(E[0]+28,y,k,17,500,MUTED)+T(E[0]+200,y,v,18,700,INK,tnum=True)
        b+=rect(E[0]+E[2]-176,y-11,76,8,4,"#EDE9FE")+rect(E[0]+E[2]-176,y-11,76*c/100,8,4,"url(#gAcc)")+T(E[0]+E[2]-28,y,f"{c}%",16,600,SUB,"end",tnum=True)
    for (py,ey) in [(P[1]+218,E[1]+162),(P[1]+505,E[1]+218)]:
        b+=f'<path d="M{P[0]+P[2]} {py} C {P[0]+P[2]+34} {py}, {E[0]-34} {ey}, {E[0]} {ey}" stroke="{ACC}" stroke-opacity="0.55" stroke-width="2" fill="none" stroke-dasharray="4 5"/><circle cx="{E[0]}" cy="{ey}" r="4" fill="{ACC}"/>'
    # hero: match + route
    M=(560,524,580,236)
    b+=spot(*M)+rect(*M,20,"#fff",LINE,1,"e2")
    b+=chip(M[0]+28,M[1]+28,"INV-7731","n",126,40,17,False)+rect(M[0]+168,M[1]+28,40,40,20,OK_S)+icon("check",M[0]+178,M[1]+38,20,OK,2.6)+chip(M[0]+222,M[1]+28,"PO-2231","n",120,40,17,False)
    b+=T(M[0]+M[2]-28,M[1]+55,"Amounts agree",18,700,OK,"end")
    b+=f'<line x1="{M[0]+28}" y1="{M[1]+92}" x2="{M[0]+M[2]-28}" y2="{M[1]+92}" stroke="{HAIR}" stroke-width="1.5"/>'
    b+=icon("git-branch",M[0]+28,M[1]+116,22,ACC_D,2)+T(M[0]+62,M[1]+134,"Over $1,000 → Finance",19,700,INK)
    b+=avatar(M[0]+48,M[1]+188,20,"JA","#C2410C","#9F1239",gid="avja")+T(M[0]+82,M[1]+184,"Approved by J. Alvarez",17,600,INK)+T(M[0]+82,M[1]+208,"3 hours after arrival",16,500,MUTED)
    b+=chip(M[0]+M[2]-184,M[1]+170,"Synced to Xero","ok",160,40,17)
    return canvas(b,title='Invoice approval workflow',desc='Emergent reads an invoice, extracts vendor, PO and total, matches the purchase order, routes it to finance and syncs it to Xero.')

# ---------------- 3 · Contract ----------------
def contract():
    b=prompt(60,40,1080,"“Route contracts to legal, finance, and the sponsor in parallel, and nudge after two days”")
    D=(60,164,510,596)
    b+=rect(*D,14,"#fff",LINE,1,"e1")
    b+=rect(D[0]+32,D[1]+32,48,48,12,ACC_S)+icon("file-text",D[0]+44,D[1]+44,24,ACC_D,2)
    b+=T(D[0]+96,D[1]+54,"Master services agreement",21,700,INK,ls=-0.2)+T(D[0]+96,D[1]+78,"Version 3 · 14 pages",16,500,MUTED)
    def bars(y,n,wid=(420,390,405,300)):
        return ''.join(rect(D[0]+36,y+i*22,wid[i%len(wid)],9,4.5,"#EEF0F5") for i in range(n))
    b+=bars(D[1]+118,4)
    b+=T(D[0]+36,D[1+0]+232,"§ 4.2  Payment terms",18,700,INK)
    from qa import width as tw
    b+=T(D[0]+36,D[1]+266,"Invoices are payable within",18,500,SUB)
    x=D[0]+36; y=D[1]+302; w45=tw("45 days",18,600)
    b+=T(x,y,"45 days",18,600,BAD)+f'<line x1="{x-1}" y1="{y-6}" x2="{x+w45+1}" y2="{y-6}" stroke="{BAD}" stroke-width="2"/>'
    x2=x+w45+12; w30=tw("30 days",18,700)
    b+=rect(x2-8,y-23,w30+16,32,8,OK_S)+T(x2,y,"30 days",18,700,OK)+T(x2+w30+16,y,"of receipt.",18,500,SUB)
    b+=rect(D[0]+36,D[1]+334,D[2]-72,88,14,"#FAFAFC",HAIR,1.5)+avatar(D[0]+68,D[1]+368,20,"LG","#C2410C","#9F1239",gid="avlg")
    b+=T(D[0]+100,D[1]+362,"Lena Grant · Legal",16,700,INK)+T(D[0]+100,D[1]+388,"Aligned with our finance policy.",16,500,SUB)
    b+=bars(D[1]+446,3)
    b+=rect(D[0]+36,D[1]+520,D[2]-72,48,12,"#fff","#D6D3E6",1.5)+icon("signature",D[0]+52,D[1]+532,24,MUTED,2)+T(D[0]+88,D[1]+550,"E-signature unlocks when all three approve",16,500,MUTED)
    # review panel
    R=(610,164,530,372)
    b+=rect(*R,18,"#fff",LINE,1,"e1")+T(R[0]+28,R[1]+46,"Parallel review",20,700,INK)+T(R[0]+28,R[1]+72,"Sent Tuesday · 9:04 AM",16,500,MUTED)
    cx,cy,r=R[0]+R[2]-58,R[1]+56,28
    ang=2/3*2*math.pi; ex,ey=cx+r*math.sin(ang),cy-r*math.cos(ang)
    b+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACC_S}" stroke-width="8"/><path d="M{cx} {cy-r} A{r} {r} 0 1 1 {ex:.2f} {ey:.2f}" fill="none" stroke="url(#gAcc)" stroke-width="8" stroke-linecap="round"/>'+T(cx,cy+6,"2/3",16,800,INK,"middle",tnum=True)
    b+=f'<line x1="{R[0]}" y1="{R[1]+100}" x2="{R[0]+R[2]}" y2="{R[1]+100}" stroke="{HAIR}" stroke-width="1.5"/>'
    for i,(ini,nm,role,st,k,c1,c2) in enumerate([("LG","Lena Grant","Legal","Approved","ok","#C2410C","#9F1239"),("OA","Omar Aziz","Finance","Approved","ok","#2563EB","#4338CA"),("DK","David Kim","Executive sponsor","Waiting","warn","#047857","#115E59")]):
        y=R[1]+146+i*76
        b+=avatar(R[0]+50,y,22,ini,c1,c2,gid=f"avr{i}")+T(R[0]+86,y-4,nm,19,600,INK)+T(R[0]+86,y+20,role,16,500,MUTED)
        b+=chip(R[0]+R[2]-(126 if k=="ok" else 112)-26,y-18,st,k,126 if k=="ok" else 112)
    # hero: reminder
    Q=(610,568,530,176)
    b+=spot(*Q)+rect(*Q,20,"#fff",LINE,1,"e2")+rect(Q[0]+26,Q[1]+30,52,52,14,WARN_S)+'<g class="ring">'+icon("bell",Q[0]+40,Q[1]+44,24,WARN,2)+'</g>'
    b+=T(Q[0]+96,Q[1]+52,"Reminder scheduled",20,700,INK)+T(Q[0]+96,Q[1]+80,"David Kim · Thursday, 9:00 AM",17,500,SUB)
    b+=f'<line x1="{Q[0]+26}" y1="{Q[1]+110}" x2="{Q[0]+Q[2]-26}" y2="{Q[1]+110}" stroke="{HAIR}" stroke-width="1.5"/>'
    b+=icon("calendar-clock",Q[0]+26,Q[1]+126,22,MUTED,2)+T(Q[0]+58,Q[1]+143,"Two days without a reply triggers it",16,500,MUTED)
    return canvas(b,title='Contract approval workflow',desc='A contract goes to legal, finance and the executive sponsor in parallel, with a redline, two approvals and an automatic reminder.')

# ---------------- 4 · Expense ----------------
def expense():
    b=prompt(60,40,1080,"“Check expenses against the budget: managers approve in policy, finance reviews the rest”")
    Ph=(60,164,300,600)
    b+=f'<g filter="url(#e2)">'+rect(*Ph,46,"#111827")+'</g>'+rect(Ph[0]+10,Ph[1]+10,Ph[2]-20,Ph[3]-20,37,"#fff")
    b+=rect(Ph[0]+Ph[2]/2-44,Ph[1]+22,88,24,12,"#111827")+T(Ph[0]+40,Ph[1]+42,"9:41",16,700,INK,tnum=True)
    for i,hgt in enumerate([6,9,12,15]): b+=rect(Ph[0]+Ph[2]-92+i*6,Ph[1]+42-hgt,4,hgt,1,INK)
    b+=rect(Ph[0]+Ph[2]-60,Ph[1]+29,26,13,4,"#fff",INK,1.5)+rect(Ph[0]+Ph[2]-57,Ph[1]+32,18,7,2,INK)+rect(Ph[0]+Ph[2]-32,Ph[1]+33,2.5,5,1,INK)
    X=Ph[0]+30; RX=Ph[0]+Ph[2]-30
    b+=T(X,Ph[1]+96,"New expense",22,700,INK,ls=-0.3)
    RC=(X,Ph[1]+116,RX-X,226)
    b+=rect(*RC,14,"#FAFAFC",HAIR,1.5)+icon("receipt",RC[0]+18,RC[1]+18,22,MUTED,2)
    b+=T(RC[0]+50,RC[1]+36,"Bistro Nord",17,700,INK)+T(RC[0]+18,RC[1]+68,"Oct 14 · 2 guests",16,500,MUTED)
    for i,wd in enumerate([150,120,160]): b+=rect(RC[0]+18,RC[1]+90+i*20,wd,8,4,"#E9EBF2")
    b+=f'<line x1="{RC[0]+18}" y1="{RC[1]+168}" x2="{RC[0]+RC[2]-18}" y2="{RC[1]+168}" stroke="#D9DCE6" stroke-width="1.5" stroke-dasharray="4 5"/>'
    b+=T(RC[0]+18,RC[1]+204,"Total",17,600,SUB)+T(RC[0]+RC[2]-18,RC[1]+204,"$180.00",22,800,INK,"end",-0.2,True)
    for i,(k,v) in enumerate([("Category","Client dinner"),("Project","Atlas")]):
        y=Ph[1]+372+i*56; b+=T(X,y,k,16,500,MUTED)+T(X,y+24,v,18,600,INK)
    b+=button(X,Ph[1]+508,RX-X,52,"Submit",True,"send")
    b+=rect(Ph[0]+Ph[2]/2-50,Ph[1]+Ph[3]-24,100,5,2.5,"#111827")
    b+=f'<path d="M{Ph[0]+Ph[2]} 470 C 396 470, 396 330, 430 330" stroke="{ACC}" stroke-opacity="0.55" stroke-width="2" fill="none" stroke-dasharray="4 5"/><circle cx="430" cy="330" r="4" fill="{ACC}"/>'
    # budget card
    B=(430,164,710,304)
    b+=rect(*B,18,"#fff",LINE,1,"e1")+icon("chart-column",B[0]+28,B[1]+26,22,ACC,2)+T(B[0]+60,B[1]+44,"Atlas · October budget",19,700,INK)
    b+=T(B[0]+28,B[1]+112,"$3,380",42,800,INK,ls=-0.8,tnum=True)+T(B[0]+188,B[1]+112,"of $4,000",20,500,MUTED,tnum=True)
    bx,by,bw=B[0]+28,B[1]+136,B[2]-56
    s1=bw*3200/4000; s2=bw*180/4000
    b+=rect(bx,by,bw,16,8,ACC_S)+rect(bx,by,s1+8,16,8,"url(#gAcc)")+f'<rect class="glow" x="{bx+s1}" y="{by}" width="{s2}" height="16" fill="#C4B5FD"/>'+f'<line x1="{bx+s1}" y1="{by-4}" x2="{bx+s1}" y2="{by+20}" stroke="#fff" stroke-width="2"/>'
    for i,(lab,col) in enumerate([("Spent $3,200",ACC),("This expense $180","#C4B5FD"),("Left $620","#DDD6FE")]):
        lx=bx+i*210; b+=f'<circle cx="{lx+6}" cy="{by+42}" r="6" fill="{col}"/>'+T(lx+20,by+48,lab,16,600,SUB,tnum=True)
    for i,lab in enumerate(["Receipt attached","Under the $250 meal limit","Within the budget"]):
        cxp=B[0]+28+[0,196,452][i]
        b+=icon("circle-check",cxp,B[1]+234,20,OK,2.2)+T(cxp+28,B[1]+250,lab,16,600,SUB)
    # hero: decision
    Dc=(430,500,710,260)
    b+=spot(*Dc)+rect(*Dc,20,"#fff",LINE,1,"e2")
    b+=avatar(Dc[0]+56,Dc[1]+58,26,"ML","#2563EB","#4338CA",gid="avml")+T(Dc[0]+96,Dc[1]+54,"Marcus Lee",20,700,INK)+T(Dc[0]+96,Dc[1]+80,"Engineering manager",16,500,MUTED)
    b+=chip(Dc[0]+Dc[2]-170,Dc[1]+38,"Within policy","ok",146,40,17)
    b+=f'<line x1="{Dc[0]+28}" y1="{Dc[1]+112}" x2="{Dc[0]+Dc[2]-28}" y2="{Dc[1]+112}" stroke="{HAIR}" stroke-width="1.5"/>'
    b+=T(Dc[0]+28,Dc[1]+150,"Approved in 12 minutes, added to the export queue",18,500,INK)
    b+=rect(Dc[0]+28,Dc[1]+176,190,48,12,OK_S)+icon("check",Dc[0]+46,Dc[1]+190,20,OK,2.6)+T(Dc[0]+74,Dc[1]+206,"Approved",17,700,OK)
    b+=icon("arrow-right",Dc[0]+240,Dc[1]+190,20,MUTED,2)+T(Dc[0]+268,Dc[1]+206,"Over policy goes to finance review",16,500,MUTED)
    return canvas(b,title='Expense approval workflow',desc='An expense submitted from a phone is checked against the project budget and policy, then approved by the manager.')
SCENES={"uc-aab-1-purchase-order":po,"uc-aab-2-invoice":invoice,"uc-aab-3-contract":contract,"uc-aab-4-expense":expense}
