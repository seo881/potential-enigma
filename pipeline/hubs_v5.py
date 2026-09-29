"""v5 design system, palette-aware, for the LP, Form and Survey & Quiz hubs (same language as the approved Approval set)."""
import ds5 as L, math
from qa import width as tw
PALS={
 "aab": dict(acc="#7C3AED",acc2="#4F46E5",accd="#5B21B6",accs="#F1ECFF",accm="#DDD3FF",bg1="#FCFBFF",bg2="#EFE9FF",glow="#E2D6FF",grid="#6D28D9",spot="#8B5CF6",sh="#2E1065",line="#E6E3F0",hair="#EEEBF5",stroke1="#A78BFA",stroke2="#818CF8"),
 "lp":  dict(acc="#2563EB",acc2="#1D4ED8",accd="#1E40AF",accs="#EAF1FF",accm="#BFD7FF",bg1="#FBFCFF",bg2="#E6EEFF",glow="#D3E2FF",grid="#1D4ED8",spot="#3B82F6",sh="#1E3A8A",line="#E2E7F2",hair="#ECF0F7",stroke1="#93C5FD",stroke2="#818CF8"),
 "form":dict(acc="#047857",acc2="#0F766E",accd="#065F46",accs="#E6F7EF",accm="#BCEBD5",bg1="#FAFFFC",bg2="#E1F6EC",glow="#CBF0DE",grid="#047857",spot="#10B981",sh="#064E3B",line="#E0EDE7",hair="#EBF4EF",stroke1="#6EE7B7",stroke2="#5EEAD4"),
 "sqb": dict(acc="#C2410C",acc2="#9A3412",accd="#9A3412",accs="#FFF1E6",accm="#FED7B0",bg1="#FFFCF8",bg2="#FFEDDC",glow="#FFE0C4",grid="#C2410C",spot="#F97316",sh="#7C2D12",line="#F0E6DD",hair="#F6EEE7",stroke1="#FDBA74",stroke2="#FB923C"),
}
def set_hub(h):
    p=PALS[h]; L.ACC=p["acc"]; L.ACC2=p["acc2"]; L.ACC_D=p["accd"]; L.ACC_S=p["accs"]; L.ACC_M=p["accm"]; L.LINE=p["line"]; L.HAIR=p["hair"]
    def defs(extra=""):
        return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p['bg1']}"/><stop offset="1" stop-color="{p['bg2']}"/></linearGradient>
<radialGradient id="glowA" cx="0.12" cy="0.08" r="0.55"><stop offset="0" stop-color="{p['glow']}" stop-opacity="0.95"/><stop offset="1" stop-color="{p['glow']}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowB" cx="0.92" cy="0.96" r="0.5"><stop offset="0" stop-color="{p['glow']}" stop-opacity="0.85"/><stop offset="1" stop-color="{p['glow']}" stop-opacity="0"/></radialGradient>
<linearGradient id="gAcc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p['acc']}"/><stop offset="1" stop-color="{p['acc2']}"/></linearGradient>
<linearGradient id="gStroke" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{p['stroke1']}"/><stop offset="1" stop-color="{p['stroke2']}"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{p['grid']}" stroke-opacity="0.07" stroke-width="1"/></pattern>
<radialGradient id="fade" cx="0.5" cy="0.45" r="0.65"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="gridMask"><rect width="1200" height="800" fill="url(#fade)"/></mask>
<filter id="e1" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-color="#0F172A" flood-opacity="0.07"/><feDropShadow dx="0" dy="12" stdDeviation="18" flood-color="{p['sh']}" flood-opacity="0.08"/></filter>
<filter id="e2" x="-15%" y="-15%" width="130%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.10"/><feDropShadow dx="0" dy="28" stdDeviation="34" flood-color="{p['sh']}" flood-opacity="0.20"/></filter>
<radialGradient id="spot" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{p['spot']}" stop-opacity="0.24"/><stop offset="1" stop-color="{p['spot']}" stop-opacity="0"/></radialGradient>
{extra}</defs>
{L.STYLE}'''
    L.defs=defs
T,rect,chip,button,avatar,icon,spot=L.T,L.rect,L.chip,L.button,L.avatar,L.icon,L.spot
INK,SUB,MUTED=L.INK,L.SUB,L.MUTED
def A(): return L.ACC
def AD(): return L.ACC_D
def AS(): return L.ACC_S
def prompt(text):
    w=min(1080,int(tw(text,19,500)+230)); return L.prompt(60,40,w,text)
def hair(x1,y,x2): return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{L.HAIR}" stroke-width="1.5"/>'
def panel(x,y,w,h,f="e1"): return rect(x,y,w,h,18,"#fff",L.LINE,1,f)
def browser(x,y,w,h,url):
    b=panel(x,y,w,h)+f'<path d="M{x} {y+52} V{y+18} a18 18 0 0 1 18 -18 H{x+w-18} a18 18 0 0 1 18 18 V{y+52} Z" fill="#FBFBFD"/>'+hair(x,y+52,x+w)
    for i in range(3): b+=f'<circle cx="{x+24+i*18}" cy="{y+26}" r="6" fill="#E3E6EE"/>'
    b+=rect(x+110,y+11,w-220,30,15,"#fff",L.LINE,1)+icon("lock",x+124,y+18,16,MUTED,2)+T(x+148,y+32,url,16,500,SUB)
    return b
def click(x,y): return f'<circle class="ripple" cx="{x}" cy="{y}" r="14" fill="{A()}"/><g class="press">'+L.cursor(x,y)+'</g>'
def appmsg(x,y,w,h,channel,title,lines,btn=None,btn2=None,cur=True,when="now"):
    b=spot(x,y,w,h)+rect(x,y,w,h,20,"#fff",L.LINE,1,"e2")
    b+=icon("hash",x+24,y+22,20,SUB,2.2)+T(x+50,y+38,channel,18,700,INK)+T(x+w-24,y+38,when,16,600,MUTED,"end")+hair(x,y+60,x+w)
    b+=rect(x+24,y+80,44,44,12,"url(#gAcc)")+icon("sparkles",x+35,y+91,22,"#fff",2)
    b+=T(x+82,y+98,"Emergent",18,700,INK)+rect(x+172,y+81,48,24,6,"#F1F5F9")+T(x+196,y+98,"APP",16,700,SUB,"middle")
    b+=T(x+82,y+130,title,18,600,INK)
    for i,l in enumerate(lines): b+=T(x+82,y+158+i*26,l,16,500,MUTED)
    if btn:
        by=y+h-74; bw=int(tw(btn,17,600)+72)
        b+=button(x+82,by,bw,50,btn,True,"check" if btn2 is None else None)
        if btn2: b+=button(x+82+bw+12,by,int(tw(btn2,17,600)+48),50,btn2,False)
        if cur: b+=click(x+82+bw-16,by+40)
    return b
def mini(x,y,w,h,ic,title,sub,kind="ok"):
    bg,fg={"ok":(L.OK_S,L.OK),"acc":(AS(),AD()),"warn":(L.WARN_S,L.WARN)}[kind]
    return panel(x,y,w,h)+rect(x+22,y+h/2-24,48,48,12,bg)+icon(ic,x+34,y+h/2-12,24,fg,2)+T(x+86,y+h/2-4,title,18,700,INK)+T(x+86,y+h/2+22,sub,16,500,MUTED)
def stars(x,y,n,size=28,gap=8):
    s=""
    for i in range(5):
        cx=x+i*(size+gap)+size/2; pts=[]
        for k in range(10):
            r=size/2 if k%2==0 else size/4.6; a=math.pi/2+k*math.pi/5; pts.append(f"{cx+r*math.cos(a):.1f},{y-r*math.sin(a):.1f}")
        s+=f'<polygon points="{" ".join(pts)}" fill="{"#F59E0B" if i<n else "#E5E7EB"}"/>'
    return s
def field(x,y,w,label,val,h=52):
    return T(x,y-10,label,16,600,MUTED)+rect(x,y,w,h,12,"#F8FAFC",L.LINE,1.2)+T(x+16,y+h/2+7,val,18,600,INK)
def canvas(b,title,desc): return L.canvas(b,title=title,desc=desc)

# ================= LP · Thank you page (blue) =================
def lp1():
    set_hub("lp"); b=prompt("“Build a thank-you page that delivers the playbook and offers a demo”")
    X,Y,Wd=60,164,700; b+=browser(X,Y,Wd,596,"yourbrand.com/thank-you"); cx=X+Wd/2
    b+=f'<circle cx="{cx}" cy="{Y+124}" r="36" fill="{L.OK_S}"/>'+icon("check",cx-18,Y+106,36,L.OK,2.6)
    b+=T(cx,Y+206,"You're in. Your playbook is ready.",28,700,INK,"middle",-0.4)+T(cx,Y+240,"A copy is on its way to your inbox.",17,500,MUTED,"middle")
    b+=button(cx-170,Y+272,340,56,"Download the playbook",True,"download")
    b+=rect(X+40,Y+376,Wd-80,132,16,AS())+T(X+68,Y+418,"Next step",16,700,AD())+T(X+68,Y+454,"Book a 15-minute walkthrough",22,700,INK)+T(X+68,Y+484,"Pick a time that suits you",16,500,SUB)
    b+=button(X+Wd-208,Y+424,140,48,"Pick a time",False)
    b+=click(cx+152,Y+314)
    H=(800,214,340,272); b+=spot(*H)+rect(*H,20,"#fff",L.LINE,1,"e2")
    b+=T(H[0]+24,H[1]+44,"New lead",19,700,INK)+chip(H[0]+H[2]-116,H[1]+22,"Just now","acc",96,34)
    b+=avatar(H[0]+50,H[1]+108,24,"MC","#2563EB","#1E40AF",gid="lpa")+T(H[0]+86,H[1]+104,"Maya Chen",19,700,INK)+T(H[0]+86,H[1]+128,"Head of Growth, Lumen",16,500,MUTED)
    b+=chip(H[0]+24,H[1]+162,"utm_source: linkedin","acc",210,36)
    b+=icon("database",H[0]+24,H[1]+224,20,L.OK,2)+T(H[0]+52,H[1]+240,"Saved to your leads table",16,600,SUB)
    b+=mini(800,520,340,120,"gauge","Conversion tracked","GA4 and Meta pixel fired")
    return canvas(b,"Lead magnet thank you page","A thank you page delivers a playbook download, offers a demo booking, saves the lead with its source, and fires conversion tracking.")
def lp2():
    set_hub("lp"); b=prompt("“After checkout, confirm the order, upsell one product, and give 10% off the next”")
    X,Y,Wd=60,164,720; b+=browser(X,Y,Wd,596,"shop.yourbrand.com/order/10482")
    b+=f'<circle cx="{X+62}" cy="{Y+100}" r="22" fill="{L.OK_S}"/>'+icon("check",X+51,Y+89,22,L.OK,2.6)
    b+=T(X+100,Y+96,"Order #10482 confirmed",26,700,INK,ls=-0.3,tnum=True)+T(X+100,Y+124,"Thanks, Maya. Your receipt is on its way.",17,500,MUTED)
    xs=[X+90,X+Wd/2,X+Wd-90]; ty=Y+184
    for i,(lab,d) in enumerate([("Ordered","Monday"),("Shipped","Tuesday"),("Arrives","Thursday")]):
        if i<2: b+=f'<line x1="{xs[i]+16}" y1="{ty}" x2="{xs[i+1]-16}" y2="{ty}" stroke="{A() if i==0 else L.HAIR}" stroke-width="4" stroke-linecap="round"/>'
        b+=(f'<circle cx="{xs[i]}" cy="{ty}" r="14" fill="url(#gAcc)"/>'+icon("check",xs[i]-8,ty-8,16,"#fff",2.8)) if i<2 else f'<circle class="pulse" cx="{xs[i]}" cy="{ty}" r="12" fill="{A()}" opacity="0.3"/><circle cx="{xs[i]}" cy="{ty}" r="12" fill="#fff" stroke="{A()}" stroke-width="3"/>'
        b+=T(xs[i],ty+42,lab,18,700,INK,"middle")+T(xs[i],ty+66,d,16,500,MUTED,"middle")
    U=(X+40,Y+280,Wd-80,150); b+=rect(*U,16,"#F8FAFC",L.HAIR,1.5)
    b+=rect(U[0]+24,U[1]+25,100,100,16,AS())+icon("package",U[0]+50,U[1]+51,48,A(),1.6)
    b+=T(U[0]+148,U[1]+50,"Pairs well with your order",16,700,AD())+T(U[0]+148,U[1]+84,"Travel case",22,700,INK)+T(U[0]+148,U[1]+112,"$29, ships in the same box",16,500,MUTED)
    b+=button(U[0]+U[2]-184,U[1]+51,160,48,"Add to order",True)+click(U[0]+U[2]-40,U[1]+87)
    for i,(k,v) in enumerate([("Trail runner 2 · size 9","$129.00"),("Shipping","Free")]):
        yy=Y+478+i*36; b+=T(X+40,yy,k,17,500,SUB)+T(X+Wd-40,yy,v,17,600,INK,"end",tnum=True)
    b+=hair(X+40,Y+532,X+Wd-40)+T(X+40,Y+568,"Total paid",18,700,INK)+T(X+Wd-40,Y+568,"$129.00",20,800,INK,"end",tnum=True)
    H=(820,200,320,286); b+=spot(*H)+rect(*H,20,"#fff",L.LINE,1,"e2")
    b+=rect(H[0]+24,H[1]+26,44,44,12,AS())+icon("tag",H[0]+34,H[1]+36,24,AD(),2)+T(H[0]+84,H[1]+56,"Next order",19,700,INK)
    b+=T(H[0]+24,H[1]+110,"10% off within 30 days",18,600,SUB)
    b+=rect(H[0]+24,H[1]+130,H[2]-48,70,14,AS(),A(),2)+T(H[0]+H[2]/2,H[1]+176,"THANKS10",30,800,INK,"middle",4)
    b+=button(H[0]+24,H[1]+216,H[2]-48,48,"Copy code",False,"copy")
    b+=mini(820,520,320,120,"database","Order saved","Source: Instagram ad","acc")
    return canvas(b,"Ecommerce order thank you page","An order confirmation page shows delivery progress, upsells a related product, and gives a discount code for the next order.")
def lp3():
    set_hub("lp"); b=prompt("“Confirm webinar signups, add them to calendars, and send reminders before it starts”")
    X,Y,Wd=60,164,720; b+=browser(X,Y,Wd,596,"yourbrand.com/webinar/registered")
    b+=f'<circle cx="{X+62}" cy="{Y+100}" r="22" fill="{L.OK_S}"/>'+icon("check",X+51,Y+89,22,L.OK,2.6)
    b+=T(X+100,Y+96,"You're registered",26,700,INK,ls=-0.3)+T(X+100,Y+124,"We saved your seat for the live session.",17,500,MUTED)
    E=(X+40,Y+164,Wd-80,140); b+=rect(*E,16,AS())
    b+=rect(E[0]+24,E[1]+24,92,92,16,"#fff")+T(E[0]+70,E[1]+58,"OCT",16,700,AD(),"middle",1)+T(E[0]+70,E[1]+100,"14",36,800,INK,"middle",tnum=True)
    b+=T(E[0]+140,E[1]+62,"Scaling onboarding with AI",22,700,INK)+T(E[0]+140,E[1]+92,"Tuesday, 10:00 AM PT, 45 minutes",17,500,SUB)
    by=Y+334; b+=button(X+40,by,236,52,"Add to Google",True,"calendar")+button(X+288,by,150,52,"Outlook",False)+button(X+450,by,130,52,"Apple",False)
    b+=click(X+260,by+40)
    b+=T(X+40,Y+440,"Invite a colleague",18,700,INK)+rect(X+40,Y+460,420,54,12,"#F8FAFC",L.LINE,1.2)+T(X+58,Y+494,"colleague@company.com",16,500,MUTED)+button(X+472,Y+460,Wd-512,54,"Send invite",False,"send")
    H=(820,196,320,340); b+=spot(*H)+rect(*H,20,"#fff",L.LINE,1,"e2")
    b+=rect(H[0]+24,H[1]+24,44,44,12,L.WARN_S)+'<g class="ring">'+icon("bell",H[0]+34,H[1]+34,24,L.WARN,2)+'</g>'+T(H[0]+84,H[1]+54,"Reminders",19,700,INK)
    for i,(w,c) in enumerate([("1 day before","Email"),("1 hour before","Email and SMS"),("Starting now","Join link")]):
        y=H[1]+106+i*76
        if i==2: b+=f'<circle class="pulse" cx="{H[0]+38}" cy="{y+12}" r="8" fill="{A()}" opacity="0.3"/>'
        b+=f'<circle cx="{H[0]+38}" cy="{y+12}" r="8" fill="{A() if i==2 else L.ACC_M}"/>'+T(H[0]+62,y+10,w,18,700,INK)+T(H[0]+62,y+36,c,16,500,MUTED)
        if i<2: b+=f'<line x1="{H[0]+38}" y1="{y+24}" x2="{H[0]+38}" y2="{y+72}" stroke="{L.ACC_M}" stroke-width="2"/>'
    b+=mini(820,570,320,120,"user-plus","Seat saved","Synced to your email tool","acc")
    return canvas(b,"Webinar thank you page","A webinar confirmation page adds the event to calendars, invites a colleague, and schedules reminder emails and texts.")
def lp4():
    set_hub("lp"); b=prompt("“After the contact form, promise a reply in 24 hours and let them book a call instead”")
    X,Y,Wd=60,164,700; b+=browser(X,Y,Wd,596,"yourbrand.com/contact/thanks")
    b+=f'<circle cx="{X+62}" cy="{Y+100}" r="22" fill="{L.OK_S}"/>'+icon("check",X+51,Y+89,22,L.OK,2.6)
    b+=T(X+100,Y+96,"Thanks, we got it",26,700,INK,ls=-0.3)+T(X+100,Y+124,"We reply within 24 hours.",17,500,MUTED)
    b+=T(X+40,Y+188,"Rather talk now? Pick a time.",20,700,INK)+T(X+40,Y+214,"Thursday, October 16",16,500,MUTED)
    for i,s in enumerate(["9:30 AM","11:00 AM","1:30 PM","3:00 PM","4:30 PM","5:00 PM"]):
        x=X+40+(i%2)*318; y=Y+238+(i//2)*72; sel=i==2
        b+=rect(x,y,302,58,14,"url(#gAcc)" if sel else "#fff",None if sel else L.LINE,1.5)+T(x+151,y+36,s,18,700,"#fff" if sel else INK,"middle",tnum=True)
    b+=button(X+40,Y+470,Wd-80,56,"Confirm 1:30 PM",True,"check")+click(X+Wd-80,Y+514)
    b+=appmsg(790,196,350,300,"sales","New enquiry",["Priya Nair, Acme Corp","Demo request, 50 seats"],None)
    b+=chip(872,440,"Call booked, Thu 1:30 PM","ok",236,36)
    b+=mini(790,540,350,120,"database","Deal created in HubSpot","Stage: new lead","acc")
    return canvas(b,"Contact form thank you page","A contact thank you page promises a reply within 24 hours, lets the visitor book a call, and posts the enquiry to Slack and HubSpot.")

# ================= FORM · Creator application (emerald) =================
def form1():
    set_hub("form"); b=prompt("“Build a brand ambassador application that scores fans and sends a referral code”")
    F=(60,164,520,596); b+=panel(*F)
    b+=T(F[0]+36,F[1]+64,"Brand ambassador application",24,700,INK,ls=-0.3)+T(F[0]+36,F[1]+92,"Tell us why you love the brand",16,500,MUTED)
    b+=field(F[0]+36,F[1]+148,F[2]-72,"Instagram handle","@maya.moves")+field(F[0]+36,F[1]+246,F[2]-72,"Favorite product","Trail runner 2")
    b+=T(F[0]+36,F[1]+334,"Why do you love us?",16,600,MUTED)+rect(F[0]+36,F[1]+344,F[2]-72,130,12,"#F8FAFC",L.LINE,1.2)
    b+=T(F[0]+54,F[1]+384,"I've run three marathons in them",18,500,INK)+T(F[0]+54,F[1]+412,"and recommend them to my club.",18,500,INK)
    b+=button(F[0]+36,F[1]+504,F[2]-72,56,"Apply to the program",True,"send")
    b+=f'<path d="M580 360 C 600 360, 600 330, 620 330" stroke="{A()}" stroke-opacity="0.55" stroke-width="2" fill="none" stroke-dasharray="4 5"/>'
    H=(620,196,520,330); b+=spot(*H)+rect(*H,20,"#fff",L.LINE,1,"e2")
    b+=f'<circle cx="{H[0]+56}" cy="{H[1]+62}" r="30" fill="{L.OK_S}"/>'+icon("check",H[0]+40,H[1]+46,32,L.OK,2.6)
    b+=T(H[0]+104,H[1]+58,"Approved",26,800,INK,ls=-0.4)+T(H[0]+104,H[1]+86,"Fit score 92, 18k audience, US West",16,500,SUB)
    b+=rect(H[0]+28,H[1]+122,H[2]-56,120,16,AS(),A(),2)+T(H[0]+54,H[1]+160,"Your referral code",16,700,AD())+T(H[0]+54,H[1]+214,"MAYA15",40,800,INK,ls=5)
    b+=T(H[0]+28,H[1]+290,"Welcome kit ships Friday",18,700,INK)
    b+=mini(620,570,520,120,"database","Saved to the creators table","Status: approved, score 92")
    return canvas(b,"Brand ambassador application","A brand ambassador application scores each applicant, approves the best fans, and sends a referral code and welcome kit.")
def form2():
    set_hub("form"); b=prompt("“Collect UGC samples, let my team rate them, and book the best creators”")
    P=(60,164,1080,420); b+=panel(*P)
    b+=T(P[0]+36,P[1]+56,"UGC samples, review board",22,700,INK,ls=-0.3)+chip(P[0]+P[2]-172,P[1]+32,"12 to review","acc",140,36)
    for i,(n,niche,r,tag,d) in enumerate([("Jordan","Skincare",5,"Unboxing","0:28"),("Aisha","Fitness",4,"Talking head","0:34"),("Leo","Tech",3,"Voiceover","0:19")]):
        x=P[0]+36+i*344; y=P[1]+86
        b+=rect(x,y,320,180,14,"#0F172A")+f'<circle cx="{x+160}" cy="{y+90}" r="30" fill="#fff" opacity="0.94"/><path d="M{x+151} {y+74} l24 16 l-24 16 z" fill="#0F172A"/>'
        b+=rect(x+14,y+140,62,28,8,"#1E293B")+T(x+45,y+160,d,16,700,"#F1F5F9","middle",tnum=True)
        b+=T(x,y+222,n,20,700,INK)+T(x,y+248,f"{niche}, 3-day turnaround",16,500,MUTED)+stars(x+2,y+282,r,24,6)+chip(x+160,y+266,tag,"acc",160,34)
    H=(420,612,720,150); b+=spot(*H)+rect(*H,20,"#fff",L.LINE,1,"e2")
    b+=rect(H[0]+24,H[1]+28,44,44,12,"url(#gAcc)")+icon("sparkles",H[0]+35,H[1]+39,22,"#fff",2)
    b+=T(H[0]+84,H[1]+46,"Emergent",18,700,INK)+rect(H[0]+174,H[1]+29,48,24,6,"#F1F5F9")+T(H[0]+198,H[1]+46,"APP",16,700,SUB,"middle")+T(H[0]+238,H[1]+46,"in #ugc-bookings",16,500,MUTED)
    b+=avatar(H[0]+48,H[1]+108,20,"JD","#047857","#115E59",gid="fjd")+T(H[0]+84,H[1]+104,"Jordan Diaz is ready to book",18,700,INK)+T(H[0]+84,H[1]+128,"Unboxing, rated 5 by 2 reviewers",16,500,MUTED)
    b+=button(H[0]+H[2]-204,H[1]+76,180,50,"Send the brief",True,"send")+click(H[0]+H[2]-40,H[1]+114)
    b+=mini(60,612,330,150,"star","Top rated this week","Jordan, Aisha, Leo","warn")
    return canvas(b,"UGC creator review board","A UGC creator application collects sample videos, lets the team rate and tag them, and books the best creators for the next brief.")
def form3():
    set_hub("form"); b=prompt("“Auto-approve affiliates with 10k+ monthly reach and give each a tracked link”")
    b+=rect(60,164,1080,90,18,AS(),L.ACC_M,1.5)+icon("git-branch",90,196,26,AD(),2)+T(132,218,"If monthly reach ≥ 10,000 → approve, create a tracked link, assign a tier",20,700,AD())
    Tb=(60,284,720,476); b+=panel(*Tb)
    b+=T(Tb[0]+32,Tb[1]+50,"affiliates",20,700,INK)+chip(Tb[0]+Tb[2]-152,Tb[1]+28,"Database","acc",128,36)+hair(Tb[0],Tb[1]+82,Tb[0]+Tb[2])
    for x,l in [(32,"CREATOR"),(330,"MONTHLY REACH"),(560,"TIER")]: b+=T(Tb[0]+x,Tb[1]+122,l,16,700,MUTED,ls=1)
    for i,(h,r,t,k) in enumerate([("@runwithsam","48,200","Gold","warn"),("@techwithtara","22,900","Silver","n"),("@homecafe.kim","12,400","Silver","n"),("@minimal.nate","6,100","Waitlist","bad")]):
        y=Tb[1]+150+i*78
        if i==0: b+=rect(Tb[0]+14,y,Tb[2]-28,64,12,AS())
        b+=avatar(Tb[0]+54,y+32,20,h[1].upper(),"#047857","#115E59",gid=f"fa{i}")+T(Tb[0]+86,y+39,h,19,700,INK)+T(Tb[0]+330,y+39,r,19,600,SUB,tnum=True)+chip(Tb[0]+560,y+14,t,k,120,36)
    H=(820,300,320,300); b+=spot(*H)+rect(*H,20,"#fff",L.LINE,1,"e2")
    b+=rect(H[0]+24,H[1]+24,44,44,12,AS())+icon("link",H[0]+34,H[1]+34,24,AD(),2)+T(H[0]+84,H[1]+54,"Tracked link created",18,700,INK)
    b+=T(H[0]+24,H[1]+114,"@runwithsam",20,700,INK)+T(H[0]+24,H[1]+140,"48,200 monthly reach",16,500,MUTED,tnum=True)
    b+=rect(H[0]+24,H[1]+162,H[2]-48,48,12,"#F8FAFC",L.LINE,1.2)+T(H[0]+40,H[1]+192,"yourbrand.co/r/sam",17,600,AD())
    b+=button(H[0]+24,H[1]+228,H[2]-48,48,"Copy link",False,"copy")
    b+=mini(820,630,320,120,"mail","Welcome email sent","Gold tier assets attached","acc")
    return canvas(b,"Affiliate creator application","An affiliate application auto-approves creators above 10,000 monthly reach, creates a tracked link, and assigns a commission tier.")
def form4():
    set_hub("form"); b=prompt("“Score content creator applicants by fit and post the shortlist to Slack”")
    S=(60,164,660,596); b+=panel(*S)
    b+=T(S[0]+36,S[1]+60,"Content creator role, shortlist",22,700,INK,ls=-0.3)+T(S[0]+36,S[1]+88,"Scored by fit as they apply",16,500,MUTED)
    for i,(ini,n,det,s) in enumerate([("RP","Riya Patel","TikTok and YouTube, 4 years",94),("SO","Sam Ortiz","Instagram, 3 years",88),("CW","Chen Wei","YouTube, 5 years",81),("AB","Ada Brooks","TikTok, 2 years",67)]):
        y=S[1]+118+i*112
        b+=rect(S[0]+24,y,S[2]-48,96,16,"#F8FAFC" if s<80 else "#fff",L.HAIR,1.5)
        b+=avatar(S[0]+72,y+48,24,ini,"#047857","#115E59",gid=f"fh{i}")+T(S[0]+112,y+42,n,20,700,INK)+T(S[0]+112,y+68,det,16,500,MUTED)
        bx=S[0]+S[2]-210; b+=rect(bx,y+42,120,12,6,"#E5E7EB")+rect(bx,y+42,120*s/100,12,6,"url(#gAcc)" if s>=80 else "#94A3B8")+T(S[0]+S[2]-48,y+56,str(s),22,800,INK if s>=80 else MUTED,"end",tnum=True)
    b+=appmsg(760,196,380,300,"creative-hiring","Shortlist ready",["3 candidates scored above 80"],"View shortlist",cur=True)
    b+=mini(760,540,380,120,"calendar","Interview booked","Riya Patel, Thursday 2:00 PM","acc")
    return canvas(b,"Content creator job application","A content creator job application scores applicants by fit, posts the shortlist to Slack, and books interviews.")

# ================= SQB · Customer satisfaction (burnt orange) =================
def sqb1():
    set_hub("sqb"); b=prompt("“Survey new accounts on day 7, 30, and 90, and alert the CSM on any low score”")
    P=(60,164,1080,300); b+=panel(*P)
    b+=T(P[0]+36,P[1]+58,"Onboarding satisfaction, Acme Corp",22,700,INK,ls=-0.3)+T(P[0]+36,P[1]+86,"CSAT and effort at each touch",16,500,MUTED)
    y=P[1]+172; xs=[260,600,940]
    b+=f'<line x1="{xs[0]}" y1="{y}" x2="{xs[2]}" y2="{y}" stroke="{L.HAIR}" stroke-width="5" stroke-linecap="round"/><line x1="{xs[0]}" y1="{y}" x2="{xs[1]}" y2="{y}" stroke="{L.ACC_M}" stroke-width="5" stroke-linecap="round"/>'
    for i,(d,c,k) in enumerate([("Day 7","CSAT 5, easy","ok"),("Day 30","CSAT 4, easy","ok"),("Day 90","CSAT 2, hard","bad")]):
        x=xs[i]; col=L.BAD if k=="bad" else A()
        if k=="bad": b+=f'<circle class="pulse" cx="{x}" cy="{y}" r="16" fill="{L.BAD}" opacity="0.3"/>'
        b+=T(x,y-34,d,20,700,INK,"middle")+f'<circle cx="{x}" cy="{y}" r="16" fill="{col}"/>'+chip(x-84,y+30,c,k,168,38,16)
    H=(300,500,840,260); b+=spot(*H)+rect(*H,20,"#fff",L.LINE,1,"e2")
    b+=icon("hash",H[0]+24,H[1]+22,20,SUB,2.2)+T(H[0]+50,H[1]+38,"cs-alerts",18,700,INK)+T(H[0]+H[2]-24,H[1]+38,"now",16,600,MUTED,"end")+hair(H[0],H[1]+60,H[0]+H[2])
    b+=T(H[0]+24,H[1]+104,"Low score from Acme Corp",22,700,INK)+T(H[0]+24,H[1]+132,"Day 90, CSAT 2, effort: hard",17,500,SUB)
    b+=rect(H[0]+24,H[1]+152,H[2]-260,84,14,"#FAFAFA",L.HAIR,1.5)+T(H[0]+44,H[1]+188,"“Setting up SSO took our IT team a week.”",18,500,INK)+T(H[0]+44,H[1]+216,"CSM: Dana Ruiz, previous scores 5 and 4",16,500,MUTED)
    b+=button(H[0]+H[2]-216,H[1]+170,192,50,"Schedule a call",True)+click(H[0]+H[2]-40,H[1]+208)
    b+=panel(60,500,210,260)+icon("chart-column",88,528,24,A(),2)+T(88,590,"Replies",18,700,INK)+T(88,648,"64%",40,800,INK,ls=-1,tnum=True)+T(88,680,"this quarter",16,500,MUTED)
    return canvas(b,"SaaS onboarding satisfaction survey","A three-touch onboarding survey tracks CSAT and effort at day 7, 30 and 90, and alerts the customer success manager on a low score.")
def sqb2():
    set_hub("sqb"); b=prompt("“A week after delivery, ask for ratings, request reviews from 5-star buyers, flag the rest”")
    Ph=(60,164,300,600); b+=f'<g filter="url(#e2)">'+rect(*Ph,46,"#111827")+'</g>'+rect(Ph[0]+10,Ph[1]+10,Ph[2]-20,Ph[3]-20,37,"#fff")
    b+=rect(Ph[0]+Ph[2]/2-44,Ph[1]+22,88,24,12,"#111827")+T(Ph[0]+40,Ph[1]+42,"9:41",16,700,INK,tnum=True)
    X=Ph[0]+30; RX=Ph[0]+Ph[2]-30
    b+=T(X,Ph[1]+98,"How did we do?",24,800,INK,ls=-0.4)+T(X,Ph[1]+124,"Delivered Thursday",16,500,MUTED)
    b+=rect(X,Ph[1]+146,RX-X,84,14,AS())+rect(X+14,Ph[1]+160,56,56,12,"#FDBA74")+T(X+84,Ph[1]+184,"Trail runner 2",17,700,INK)+T(X+84,Ph[1]+208,"Black, size 9",16,500,SUB)
    b+=T(X,Ph[1]+270,"Product",17,700,INK)+stars(X,Ph[1]+302,5,30,6)+T(X,Ph[1]+354,"Delivery",17,700,INK)+stars(X,Ph[1]+386,4,30,6)
    b+=T(X,Ph[1]+432,"Anything to add?",16,600,MUTED)+rect(X,Ph[1]+442,RX-X,54,12,"#F8FAFC",L.LINE,1.2)+T(X+14,Ph[1]+475,"Arrived early, love them",16,500,INK)
    b+=button(X,Ph[1]+514,RX-X,52,"Submit",True)
    b+=f'<path d="M360 330 C 390 330, 390 300, 420 300" stroke="{A()}" stroke-opacity="0.55" stroke-width="2" fill="none" stroke-dasharray="4 5"/><path d="M360 600 C 390 600, 390 600, 420 600" stroke="{A()}" stroke-opacity="0.55" stroke-width="2" fill="none" stroke-dasharray="4 5"/>'
    C=(420,196,720,214); b+=panel(*C)
    b+=chip(C[0]+28,C[1]+28,"5 stars","ok",112,36)+T(C[0]+28,C[1]+108,"Review request sent",22,700,INK)+T(C[0]+28,C[1]+136,"Link to the Trail runner 2 product page",16,500,MUTED)
    b+=avatar(C[0]+C[2]-160,C[1]+120,24,"MC","#C2410C","#9A3412",gid="sqa")+T(C[0]+C[2]-124,C[1]+116,"M. Chen",18,700,INK)+T(C[0]+C[2]-124,C[1]+140,"5 and 5",16,500,MUTED)
    H=(420,450,720,300); b+=spot(*H)+rect(*H,20,"#fff",L.LINE,1,"e2")
    b+=chip(H[0]+28,H[1]+28,"2 stars","bad",112,36)+T(H[0]+28,H[1]+110,"Returns team flagged",24,700,INK)+T(H[0]+28,H[1]+140,"Order #10377, sizing issue",17,500,SUB)
    b+=rect(H[0]+28,H[1]+164,H[2]-56,58,14,"#FAFAFA",L.HAIR,1.5)+T(H[0]+48,H[1]+200,"“Runs small, I need a size up.”",18,500,INK)
    b+=button(H[0]+28,H[1]+236,200,48,"Start exchange",True)+click(H[0]+212,H[1]+272)+T(H[0]+252,H[1]+266,"Follow-up within a day",16,500,MUTED)
    return canvas(b,"Post-purchase satisfaction survey","A post-purchase survey rates product and delivery, sends a review request to five-star buyers, and flags low ratings to the returns team.")
def sqb3():
    set_hub("sqb"); b=prompt("“Survey every account each quarter and write a per-account summary to HubSpot”")
    P=(60,164,1080,360); b+=panel(*P)
    b+=T(P[0]+32,P[1]+50,"Q3 satisfaction by account",20,700,INK)+chip(P[0]+P[2]-152,P[1]+28,"Database","acc",128,36)+hair(P[0],P[1]+82,P[0]+P[2])
    for x,l in [(32,"ACCOUNT"),(330,"ACCOUNT EXEC"),(600,"CSAT"),(740,"NPS"),(880,"VS Q2")]: b+=T(P[0]+x,P[1]+118,l,16,700,MUTED,ls=1)
    for i,(a,ae,cs,n,tr,bad) in enumerate([("Northwind","J. Alvarez","4.6","+52","+6",False),("Globex","R. Singh","4.2","+31","+2",False),("Initech","M. Rossi","3.1","−8","−24",True),("Umbrella Co","J. Alvarez","4.4","+40","+4",False)]):
        y=P[1]+136+i*54
        if bad: b+=rect(P[0]+14,y,P[2]-28,48,10,L.BAD_S)
        b+=T(P[0]+32,y+32,a,19,700,INK)+T(P[0]+330,y+32,ae,18,500,SUB)+T(P[0]+600,y+32,cs,19,700,INK,tnum=True)+T(P[0]+740,y+32,n,19,700,INK,tnum=True)
        b+=T(P[0]+880,y+32,tr,19,700,L.BAD if bad else L.OK,tnum=True)
    H=(560,560,580,200); b+=spot(*H)+rect(*H,20,"#fff",L.LINE,1,"e2")
    b+=chip(H[0]+28,H[1]+26,"AE alert","bad",112,36)+T(H[0]+28,H[1]+100,"NPS dropped 24 at Initech",22,700,INK,tnum=True)+T(H[0]+28,H[1]+128,"Sent to M. Rossi with every survey comment",16,500,SUB)
    b+=button(H[0]+H[2]-212,H[1]+28,184,50,"Review account",True)+click(H[0]+H[2]-44,H[1]+66)
    Q=(60,560,460,200); b+=panel(*Q)+rect(Q[0]+24,Q[1]+26,44,44,12,AS())+icon("file-text",Q[0]+34,Q[1]+36,24,AD(),2)+T(Q[0]+84,Q[1]+56,"QBR summary in HubSpot",18,700,INK)
    b+=T(Q[0]+24,Q[1]+112,"• Support response time is the top theme",16,500,SUB)+T(Q[0]+24,Q[1]+142,"• Two users flagged onboarding effort",16,500,SUB)+T(Q[0]+24,Q[1]+172,"• Renewal owner: M. Rossi",16,500,SUB)
    return canvas(b,"B2B quarterly customer satisfaction survey","A quarterly B2B survey scores CSAT and NPS per account, writes a summary to HubSpot, and alerts the account executive when NPS drops.")
def sqb4():
    set_hub("sqb"); b=prompt("“When a ticket closes, send a CSAT survey and alert the lead on any score of 1 or 2”")
    S=(60,164,500,340); b+=panel(*S)
    b+=chip(S[0]+28,S[1]+26,"Ticket #8841 closed","ok",210,36)+T(S[0]+28,S[1]+104,"How satisfied are you",24,800,INK,ls=-0.4)+T(S[0]+28,S[1]+134,"with the help you got?",24,800,INK,ls=-0.4)
    for i in range(5):
        x=S[0]+28+i*90; sel=i==3
        b+=rect(x,S[1]+166,76,76,16,"url(#gAcc)" if sel else "#F8FAFC",None if sel else L.LINE,1.5)+T(x+38,S[1]+214,str(i+1),26,800,"#fff" if sel else SUB,"middle",tnum=True)
    b+=T(S[0]+28,S[1]+296,"Agent: Sofia, Billing, resolved in 38 minutes",16,500,MUTED)
    Dd=(600,164,540,340); b+=panel(*Dd)+T(Dd[0]+28,Dd[1]+50,"CSAT by agent this week",19,700,INK)
    for i,(n,v) in enumerate([("Sofia",4.7),("Marcus",4.5),("Priya",4.1),("Tom",3.2)]):
        y=Dd[1]+90+i*60; low=v<4
        b+=T(Dd[0]+28,y+26,n,18,700,INK)+rect(Dd[0]+130,y+10,300,22,11,AS())+rect(Dd[0]+130,y+10,300*v/5,22,11,L.BAD if low else "url(#gAcc)")+T(Dd[0]+Dd[2]-28,y+28,f"{v}",19,800,L.BAD if low else INK,"end",tnum=True)
    H=(60,540,1080,220); b+=spot(*H)+rect(*H,20,"#fff",L.LINE,1,"e2")
    b+=icon("hash",H[0]+24,H[1]+22,20,SUB,2.2)+T(H[0]+50,H[1]+38,"support-leads",18,700,INK)+T(H[0]+H[2]-24,H[1]+38,"now",16,600,MUTED,"end")+hair(H[0],H[1]+60,H[0]+H[2])
    b+=T(H[0]+24,H[1]+104,"Low score on ticket #8790",22,700,INK,tnum=True)+T(H[0]+24,H[1]+132,"CSAT 2, Tom, Billing, resolved in 2 days",17,500,SUB)
    b+=rect(H[0]+24,H[1]+150,700,52,14,"#FAFAFA",L.HAIR,1.5)+T(H[0]+44,H[1]+183,"“I had to explain the refund issue three times.”",18,500,INK)
    b+=button(H[0]+H[2]-208,H[1]+130,184,50,"Open ticket",True)+click(H[0]+H[2]-40,H[1]+168)
    return canvas(b,"Support ticket CSAT survey","A CSAT survey fires when a support ticket closes, feeds a per-agent dashboard, and alerts the support lead on a low score.")
SCENES={"lp":[lp1,lp2,lp3,lp4],"form":[form1,form2,form3,form4],"sqb":[sqb1,sqb2,sqb3,sqb4]}
