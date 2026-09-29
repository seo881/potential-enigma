from helpers import *
import xml.dom.minidom, cairosvg
from PIL import Image
PAL={"lp":("#eaf2ff","#c7dbff","#2563eb","#dbeafe"),"form":("#eafbf4","#c4efdc","#059669","#d1fae5"),
     "aab":("#f3efff","#ddd3ff","#7c3aed","#ede9fe"),"sqb":("#fff6ec","#ffe2c4","#ea580c","#ffedd5")}
def conn(d,c,w=5): return f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-dasharray="2 13"/>'
def check(cx,cy,r,c="#16a34a",bg="#dcfce7"):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/><path d="M{cx-r*.42} {cy} l{r*.3} {r*.3} l{r*.55} -{r*.6}" stroke="{c}" stroke-width="{max(3,r*.16):.0f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
def browser(x,y,w,h,url):
    b=card(x,y,w,h)+f'<rect x="{x}" y="{y}" width="{w}" height="70" rx="28" fill="#f3f5f9"/><rect x="{x}" y="{y+40}" width="{w}" height="30" fill="#f3f5f9"/>'+dots(x+40,y+36)
    b+=f'<rect x="{x+130}" y="{y+16}" width="{w-260}" height="40" rx="20" fill="#fff" stroke="#e3e8f2"/>'+t(x+156,y+43,url,18,600,"#374151")
    return b
def row_head(x,y,w,title,tag,acc):
    return f'<rect x="{x}" y="{y}" width="{w}" height="70" rx="26" fill="#0a0a0a"/><rect x="{x}" y="{y+36}" width="{w}" height="34" fill="#0a0a0a"/>'+t(x+30,y+45,title,22,700,"#fff")+pill(x+w-190,y+14,170,42,"#1f2937",tag,tc="#e5e7eb",size=16,dot=acc)
def stars(x,y,n,size=30,c="#f59e0b"):
    s=""
    for i in range(5):
        cx=x+i*(size+8)+size/2; cy=y
        import math
        pts=[]
        for k in range(10):
            r=size/2 if k%2==0 else size/4.6
            a=math.pi/2+k*math.pi/5
            pts.append(f"{cx+r*math.cos(a):.1f},{cy-r*math.sin(a):.1f}")
        s+=f'<polygon points="{" ".join(pts)}" fill="{c if i<n else "#e5e7eb"}"/>'
    return s

# ================= LP: Thank You Page =================
def lp1():
    g1,g2,A,L=PAL["lp"]
    b=browser(90,90,1020,640,"yourbrand.com/thank-you")
    b+=check(600,250,52)+t(600,360,"You're in! Your playbook is ready.",38,800,anchor="middle")
    b+=t(600,404,"Check your inbox in the next two minutes for a copy.",21,500,"#6b7280","middle")
    b+=pill(380,440,440,70,"#0a0a0a","↓  Download the playbook (PDF)",size=21)
    b+=f'<rect x="250" y="560" width="700" height="130" rx="22" fill="{L}"/>'+t(290,610,"One more thing",18,700,A)+t(290,650,"Book a 15-minute walkthrough",23,700)
    b+=pill(780,604,140,50,A,"Book now",size=18)
    b+=card(560,780,550,130)+t(600,832,"Lead saved to your database",22,700)+t(600,868,"utm_source=linkedin · referrer=blog",18,500,"#6b7280")+check(1060,845,24)
    b+=pill(90,812,390,62,"#ffffff","Conversion goal · pixel fired",tc="#111827",size=19,dot="#22c55e")
    return svg(b,g1,g2)
def lp2():
    g1,g2,A,L=PAL["lp"]
    b=browser(90,90,1020,820,"shop.yourbrand.com/order/10482")
    b+=check(170,230,34)+t(225,222,"Order #10482 confirmed",34,800)+t(225,258,"Thanks, Maya. A receipt is on its way.",20,500,"#6b7280")
    steps=[("Ordered","Mon"),("Shipped","Tue"),("Arrives","Thu")]
    for i,(s,d) in enumerate(steps):
        x=190+i*380
        b+=f'<circle cx="{x}" cy="340" r="16" fill="{A if i<2 else "#e5e7eb"}"/>'+t(x,385,s,20,700,anchor="middle")+t(x,412,d,18,500,"#6b7280","middle")
        if i<2: b+=f'<line x1="{x+22}" y1="340" x2="{x+358}" y2="340" stroke="{A if i<1 else "#e5e7eb"}" stroke-width="5"/>'
    b+=f'<rect x="150" y="460" width="900" height="200" rx="22" fill="#f8fafc" stroke="#eef1f6"/>'+t(190,510,"Pairs well with your order",18,700,A)
    b+=f'<rect x="190" y="530" width="100" height="100" rx="16" fill="{L}"/><rect x="215" y="560" width="50" height="40" rx="8" fill="{A}" opacity="0.5"/>'
    b+=t(320,570,"Travel case for your headphones",23,700)+t(320,606,"$29 · ships with your order",19,500,"#6b7280")+pill(840,556,170,52,"#0a0a0a","Add to order",size=18)
    b+=f'<rect x="150" y="700" width="900" height="110" rx="22" fill="{L}" stroke="{A}" stroke-dasharray="8 8"/>'+t(190,748,"10% off your next order",24,800)+t(190,782,"Use code THANKS10 within 30 days",19,500,"#374151")
    b+=pill(860,730,150,50,"#fff","Copy code",tc=A,size=18)
    return svg(b,g1,g2)
def lp3():
    g1,g2,A,L=PAL["lp"]
    b=browser(90,90,1020,600,"yourbrand.com/webinar/registered")
    b+=check(170,230,34)+t(225,222,"You're registered",34,800)+t(225,258,"We saved your seat for the live session.",20,500,"#6b7280")
    b+=f'<rect x="150" y="300" width="900" height="150" rx="22" fill="{L}"/>'
    b+=f'<rect x="185" y="325" width="100" height="100" rx="18" fill="#fff"/>'+t(235,362,"OCT",18,800,A,"middle")+t(235,408,"14",40,800,anchor="middle")
    b+=t(315,365,"Scaling onboarding with AI",26,800)+t(315,402,"Tue · 10:00 AM PT · 45 minutes",20,500,"#374151")
    for i,l in enumerate(["Google Calendar","Outlook","Apple"]):
        b+=(f'<rect x="{150+i*305}" y="480" width="285" height="58" rx="29" fill="#fff" stroke="#d6dce8" stroke-width="2"/>' if i else "")+pill(150+i*305,480,285,58,"#0a0a0a" if i==0 else "none","+ "+l,tc="#fff" if i==0 else "#111827",size=18)
    b+=t(150,600,"Invite a colleague",20,700)+f'<rect x="150" y="615" width="620" height="54" rx="14" fill="#f6f8fc" stroke="#e3e8f2"/>'+t(172,650,"colleague@company.com",19,500,"#9ca3af")+pill(790,615,260,54,A,"Send invite",size=18)
    b+=card(90,740,1020,170)+t(130,792,"Reminder schedule",22,700)
    for i,(when,ch) in enumerate([("1 day before","Email"),("1 hour before","Email + SMS"),("Starting now","Join link")]):
        x=130+i*330
        b+=f'<rect x="{x}" y="815" width="300" height="70" rx="16" fill="#f8fafc" stroke="#eef1f6"/>'+t(x+20,845,when,19,700)+t(x+20,872,ch,16,500,"#6b7280")
    return svg(b,g1,g2)
def lp4():
    g1,g2,A,L=PAL["lp"]
    b=browser(90,90,660,820,"yourbrand.com/contact/thanks")
    b+=check(170,230,34)+t(225,222,"Thanks, we got it",30,800)+t(225,256,"We reply within 24 hours.",20,500,"#6b7280")
    b+=t(130,330,"Rather talk now? Pick a time.",22,700)+t(130,362,"Thursday, October 16",18,600,"#6b7280")
    for i,s in enumerate(["9:30 AM","11:00 AM","1:30 PM","3:00 PM","4:30 PM","5:00 PM"]):
        x=130+(i%2)*290; y=390+(i//2)*84; sel=i==2
        b+=f'<rect x="{x}" y="{y}" width="270" height="64" rx="14" fill="{A if sel else "#fff"}" stroke="{A if sel else "#e3e8f2"}" stroke-width="2"/>'+t(x+135,y+40,s,20,700,"#fff" if sel else "#111827","middle")
    b+=pill(130,660,560,64,"#0a0a0a","Confirm 1:30 PM",size=20)
    b+=t(130,790,"Your enquiry is with the sales team.",19,500,"#6b7280")
    b+=card(790,200,330,190,22,"#fff","sh2")+pill(815,222,150,38,L,"# sales",tc=A,size=16)+t(815,295,"New enquiry",21,700)+t(815,328,"Priya · Acme Corp",18,500,"#374151")+t(815,358,"Demo request · 50 seats",17,500,"#6b7280")
    b+=card(790,440,330,190,22,"#fff","sh2")+pill(815,462,150,38,L,"CRM",tc=A,size=16)+t(815,535,"Deal created",21,700)+t(815,568,"Stage: New lead",18,500,"#374151")+t(815,598,"Owner assigned",17,500,"#6b7280")
    b+=conn("M750 300 L 790 300",A)+conn("M750 540 L 790 540",A)
    return svg(b,g1,g2)

# ================= FORM: Creator Application =================
def form1():
    g1,g2,A,L=PAL["form"]
    b=card(80,110,560,780)+t(120,180,"Brand ambassador application",26,800)+t(120,214,"Tell us why you love the brand",18,500,"#6b7280")
    b+=field(120,270,480,"Instagram handle","@maya.moves")+field(120,390,480,"Favorite product","Trail runner 2")
    b+=t(120,498,"Why do you love us?",18,600,"#6b7280")+f'<rect x="120" y="510" width="480" height="150" rx="14" fill="#f6f8fc" stroke="#e3e8f2"/>'
    b+=t(140,550,"I've run three marathons in them",20,500)+t(140,580,"and recommend them to my club.",20,500)
    b+=pill(120,700,480,64,"#0a0a0a","Apply to the program",size=20)
    b+=conn("M640 420 L 690 420",A)
    b+=card(690,250,430,420)+check(760,330,34)+t(820,322,"Approved",28,800)+t(820,354,"Audience 18k · US West",18,500,"#6b7280")
    b+=f'<rect x="730" y="400" width="350" height="110" rx="18" fill="{L}" stroke="{A}" stroke-dasharray="8 8"/>'+t(760,445,"Your referral code",17,700,A)+t(760,488,"MAYA15",34,800)
    b+=t(730,560,"Welcome kit ships Friday",20,700)+t(730,592,"Tracked link sent by email",18,500,"#6b7280")
    b+=pill(690,720,300,60,"#fff","Saved to creators table",tc="#111827",size=17,dot="#22c55e")
    return svg(b,g1,g2)
def form2():
    g1,g2,A,L=PAL["form"]
    b=card(80,100,1040,800)+t(120,170,"UGC samples · review board",28,800)+pill(880,135,200,48,L,"12 to review",tc=A,size=17)
    for i,(name,tag,r,niche) in enumerate([("Jordan","Unboxing",5,"Skincare"),("Aisha","Talking head",4,"Fitness"),("Leo","Voiceover",3,"Tech")]):
        x=120+i*330
        b+=f'<rect x="{x}" y="215" width="300" height="360" rx="20" fill="#0f172a"/>'
        b+=f'<circle cx="{x+150}" cy="370" r="40" fill="#ffffff" opacity="0.9"/><path d="M{x+140} 350 l30 20 l-30 20 z" fill="#0f172a"/>'
        b+=t(x+20,540,"0:{:02d}".format([28,34,19][i]),16,700,"#e5e7eb")
        b+=t(x,625,name,22,700)+t(x,655,niche+" · 3-day turnaround",17,500,"#6b7280")
        b+=stars(x,695,r,26)+pill(x,730,170,40,L,tag,tc=A,size=15)
    b+=pill(120,810,300,56,"#0a0a0a","Book for next brief",size=18)+t(450,845,"Jordan tagged Unboxing · rated 5 by 2 reviewers",18,500,"#6b7280")
    return svg(b,g1,g2)
def form3():
    g1,g2,A,L=PAL["form"]
    b=card(80,110,1040,200)+t(120,170,"Auto-approve rule",18,700,A)
    b+=f'<rect x="120" y="190" width="960" height="84" rx="18" fill="{L}"/>'+t(150,242,"If monthly reach ≥ 10,000 → approve, send tracked link, assign tier",23,700)
    b+=card(80,350,1040,550)+row_head(80,350,1040,"affiliates","Database",A)
    b+=t(120,455,"CREATOR",15,700,"#9ca3af",ls=1.5)+t(420,455,"REACH",15,700,"#9ca3af",ls=1.5)+t(600,455,"TIER",15,700,"#9ca3af",ls=1.5)+t(780,455,"TRACKED LINK",15,700,"#9ca3af",ls=1.5)
    rows=[("@runwithsam","48,200","Gold","yourbrand.co/r/sam"),("@techwithtara","22,900","Silver","yourbrand.co/r/tara"),("@homecafe.kim","12,400","Silver","yourbrand.co/r/kim"),("@minimal.nate","6,100","Waitlist","—")]
    for i,(c,r,tr,l) in enumerate(rows):
        y=480+i*96
        b+=t(120,y+40,c,21,700)+t(420,y+40,r,21,600,"#374151")
        col={"Gold":("#fef3c7","#92400e"),"Silver":("#f1f5f9","#334155"),"Waitlist":("#fee2e2","#b91c1c")}[tr]
        b+=pill(600,y+12,140,42,col[0],tr,tc=col[1],size=16)+t(780,y+40,l,19,600,A if l!="—" else "#9ca3af")
        b+=f'<line x1="120" y1="{y+78}" x2="1080" y2="{y+78}" stroke="#eef1f6"/>'
    return svg(b,g1,g2)
def form4():
    g1,g2,A,L=PAL["form"]
    b=card(80,100,700,800)+t(120,170,"Content creator role · shortlist",26,800)+t(120,204,"Scored by fit on arrival",18,500,"#6b7280")
    for i,(n,det,s) in enumerate([("Riya Patel","TikTok, YouTube · 4 yrs",94),("Sam Ortiz","Instagram · 3 yrs",88),("Chen Wei","YouTube · 5 yrs",81),("Ada Brooks","TikTok · 2 yrs",67)]):
        y=250+i*150
        b+=f'<rect x="120" y="{y}" width="620" height="126" rx="18" fill="#f8fafc" stroke="#eef1f6"/>'
        b+=f'<circle cx="170" cy="{y+63}" r="28" fill="{L}"/>'+t(170,y+72,n[0],24,800,A,"middle")
        b+=t(215,y+52,n,22,700)+t(215,y+84,det,17,500,"#6b7280")
        b+=f'<rect x="520" y="{y+50}" width="150" height="14" rx="7" fill="#e5e7eb"/><rect x="520" y="{y+50}" width="{150*s/100:.0f}" height="14" rx="7" fill="{A}" opacity="{1 if s>=80 else .45}"/>'+t(710,y+64,str(s),22,800,anchor="end")
    b+=conn("M780 420 L 830 420",A)
    b+=card(830,290,300,260,22,"#fff","sh2")+pill(855,312,220,38,L,"# creative-hiring",tc=A,size=15)
    b+=t(855,390,"Shortlist ready",22,700)+t(855,424,"3 candidates above 80",18,500,"#374151")+t(855,456,"Interviews: book from",17,500,"#6b7280")+t(855,480,"the application",17,500,"#6b7280")
    return svg(b,g1,g2)

# ================= AAB: Approval Workflow =================
def aab_uc1():
    g1,g2,A,L=PAL["aab"]
    b=card(80,110,440,400)+t(115,170,"Purchase request",24,800)
    b+=field(115,220,370,"Item","Design licenses ×12",h=56)+field(115,320,370,"Vendor","Figma · approved list",h=56)
    b+=t(115,432,"$4,800",40,800)+pill(300,400,185,46,L,"Marketing",tc=A,size=17)
    b+=conn("M520 310 L 580 310",A)
    tiers=[("Manager","Under $500","not needed","#f1f5f9","#64748b"),("Department head","$500 to $5,000","approved","#dcfce7","#15803d"),("CFO","Over $5,000","not needed","#f1f5f9","#64748b")]
    for i,(who,rng,st,bg,tc) in enumerate(tiers):
        y=110+i*135; hot=i==1
        b+=card(580,y,540,112,20,"#fff","sh2",A if hot else "#e6ebf5")+f'<circle cx="625" cy="{y+56}" r="14" fill="{A if hot else "#cbd5e1"}"/>'
        b+=t(660,y+48,who,22,700)+t(660,y+80,rng,18,500,"#6b7280")+pill(930,y+34,165,44,bg,st,tc=tc,size=16)
    b+=card(80,570,1040,330)+row_head(80,570,1040,"approvals · audit log","Database",A)
    b+=t(120,675,"REQUESTER",15,700,"#9ca3af",ls=1.5)+t(390,675,"AMOUNT",15,700,"#9ca3af",ls=1.5)+t(560,675,"APPROVER",15,700,"#9ca3af",ls=1.5)+t(840,675,"TIME TO APPROVE",15,700,"#9ca3af",ls=1.5)
    for i,(r,a,ap,tm) in enumerate([("Nina · Marketing","$4,800","Dept head","2h 14m"),("Omar · Ops","$320","Manager","18m"),("Lee · Eng","$12,500","CFO","1d 3h")]):
        y=700+i*62
        b+=t(120,y+36,r,20,600)+t(390,y+36,a,20,700)+t(560,y+36,ap,20,500,"#374151")+t(840,y+36,tm,20,600,A)
    return svg(b,g1,g2)
def aab_uc2():
    g1,g2,A,L=PAL["aab"]
    b=card(80,100,470,800)+t(120,165,"INVOICE",20,800,"#9ca3af",ls=3)+t(120,215,"Northwind Supplies",26,800)
    for i,(k,v,hl) in enumerate([("Invoice #","INV-7731",False),("PO reference","PO-2231",True),("Vendor","Northwind Supplies",True),("Amount due","$2,340.00",True),("Due","Nov 12",False)]):
        y=270+i*78
        if hl: b+=f'<rect x="108" y="{y-8}" width="414" height="62" rx="12" fill="{L}" stroke="{A}" stroke-width="2"/>'
        b+=t(128,y+22,k,16,600,"#6b7280")+t(128,y+46,v,21,700)
    for i in range(4): b+=f'<rect x="120" y="{690+i*38}" width="{390-i*60}" height="14" rx="7" fill="#eef1f6"/>'
    b+=pill(300,120,220,44,A,"AI extracted",size=16)
    b+=conn("M550 420 L 610 420",A)
    items=[("Matched to PO-2231","Amounts agree",True),("Routed to finance","Over $1,000 · cost center 410",True),("Approved","by J. Alvarez · 3h",True),("Written to Xero","Bill created with PDF link",True)]
    for i,(ti,su,ok) in enumerate(items):
        y=130+i*150
        b+=card(610,y,510,118,20,"#fff","sh2")+check(662,y+59,26)+t(705,y+52,ti,22,700)+t(705,y+84,su,18,500,"#6b7280")
        if i<3: b+=f'<line x1="662" y1="{y+118}" x2="662" y2="{y+150}" stroke="{A}" stroke-width="4"/>'
    return svg(b,g1,g2)
def aab_uc3():
    g1,g2,A,L=PAL["aab"]
    b=card(80,100,1040,170)+f'<rect x="120" y="135" width="80" height="100" rx="10" fill="{L}" stroke="{A}"/>'+t(160,195,"PDF",18,800,A,"middle")
    b+=t(230,175,"Master services agreement · v3",26,800)+t(230,212,"Routed to three reviewers in parallel",19,500,"#6b7280")+pill(900,150,190,48,"#fef3c7","SLA: 2 days",tc="#92400e",size=17)
    lanes=[("Legal","Approved · 1 red-line resolved","#dcfce7","#15803d","approved"),("Finance","Approved · payment terms OK","#dcfce7","#15803d","approved"),("Executive","Waiting · reminder in 2 days","#fef3c7","#92400e","pending")]
    for i,(who,su,bg,tc,st) in enumerate(lanes):
        x=80+i*355
        b+=conn(f"M600 270 C 600 300, {x+165} 300, {x+165} 330",A)
        b+=card(x,330,330,230,20,"#fff","sh2")+t(x+30,390,who,24,800)+pill(x+30,410,150,42,bg,st,tc=tc,size=16)
        b+=t(x+30,495,su.split(" · ")[0],18,700,"#374151")+t(x+30,525,su.split(" · ")[1],17,500,"#6b7280")
    b+=conn("M600 560 L 600 620",A)
    b+=card(250,620,700,280)+t(290,680,"When all three approve",18,700,A)
    for i,(ti,su) in enumerate([("Send for e-signature","Counterparty signs online"),("Save signed PDF","Google Drive · Contracts"),("Log every version","Approvers, timestamps, notes")]):
        y=705+i*62
        b+=check(310,y+22,18)+t(345,y+30,ti,20,700)+t(640,y+30,su,17,500,"#6b7280")
    return svg(b,g1,g2)
def aab_uc4():
    g1,g2,A,L=PAL["aab"]
    b=card(80,100,500,420)+t(115,160,"Submit an expense",24,800)
    b+=f'<rect x="115" y="190" width="160" height="200" rx="14" fill="#f8fafc" stroke="#e3e8f2" stroke-dasharray="6 6"/>'
    for i in range(6): b+=f'<rect x="135" y="{215+i*26}" width="{120-(i%3)*25}" height="10" rx="5" fill="#e5e7eb"/>'
    b+=t(300,215,"Client dinner",22,700)+t(300,248,"Project: Atlas",18,500,"#6b7280")+t(300,300,"$180",40,800)+pill(300,330,170,42,L,"Meals",tc=A,size=16)
    b+=pill(115,430,430,58,"#0a0a0a","Submit for approval",size=19)
    b+=card(620,100,500,420)+t(655,160,"Atlas budget · this month",20,700)
    b+=t(655,230,"$3,380",40,800)+t(830,230,"of $4,000",22,600,"#6b7280")
    b+=f'<rect x="655" y="262" width="430" height="26" rx="13" fill="#ede9fe"/><rect x="655" y="262" width="{430*3200/4000:.0f}" height="26" rx="13" fill="{A}"/><rect x="{655+430*3200/4000:.0f}" y="262" width="{430*180/4000:.0f}" height="26" fill="#a78bfa"/>'
    b+=pill(655,320,300,46,"#dcfce7","Within policy",tc="#15803d",size=17,dot="#22c55e")+t(655,420,"→ Manager approval",22,700)+t(655,456,"Out of policy → finance review",18,500,"#6b7280")
    b+=card(80,570,1040,330)+row_head(80,570,1040,"expense decisions","Database",A)
    for i,(w,a,st,bg,tc,note) in enumerate([("Client dinner","$180","approved","#dcfce7","#15803d","Added to export queue"),("Conference pass","$1,250","escalated","#fef3c7","#92400e","Over policy · finance"),("Taxi receipts","$64","declined","#fee2e2","#b91c1c","Missing receipt · returned")]):
        y=665+i*72
        b+=t(120,y+38,w,21,700)+t(420,y+38,a,21,700)+pill(560,y+10,150,42,bg,st,tc=tc,size=16)+t(740,y+38,note,18,500,"#6b7280")
    return svg(b,g1,g2)

# ================= SQB: Customer Satisfaction =================
def sqb_uc1():
    g1,g2,A,L=PAL["sqb"]
    b=card(80,100,1040,430)+t(120,165,"Onboarding survey · Acme Corp",26,800)+t(120,200,"CSAT and effort at each touch",18,500,"#6b7280")
    b+=f'<line x1="200" y1="310" x2="1000" y2="310" stroke="#e5e7eb" stroke-width="6"/>'
    for i,(d,cs,ok) in enumerate([("Day 7","CSAT 5 · easy",True),("Day 30","CSAT 4 · easy",True),("Day 90","CSAT 2 · hard",False)]):
        x=200+i*400
        b+=f'<circle cx="{x}" cy="310" r="24" fill="{A if ok else "#ef4444"}"/>'+t(x,265,d,22,800,anchor="middle")
        b+=pill(x-110,360,220,50,"#fff7ed" if ok else "#fee2e2",cs,tc=A if ok else "#b91c1c",size=17)
    b+=t(120,480,"Tied to: account · plan · CSM",18,600,"#6b7280")
    b+=conn("M1000 410 C 1000 500, 800 520, 760 570",A)
    b+=card(380,570,740,300,22,"#fff","sh2")+pill(410,595,190,40,"#fff7ed","# cs-alerts",tc=A,size=16)
    b+=t(410,675,"Low score from Acme Corp",24,800)+t(410,712,"Day 90 · CSAT 2 · effort: hard",19,600,"#374151")
    b+=f'<rect x="410" y="740" width="680" height="96" rx="14" fill="#f8fafc"/>'+t(435,780,"“Setting up SSO took our IT team a week.”",19,500,"#374151")+t(435,812,"CSM: Dana · plan: Business · previous scores 5 and 4",17,500,"#6b7280")
    return svg(b,g1,g2)
def sqb_uc2():
    g1,g2,A,L=PAL["sqb"]
    b=card(80,100,560,800)+t(120,165,"How did we do?",30,800)+t(120,200,"Order #10482 · delivered Thursday",18,500,"#6b7280")
    b+=f'<rect x="120" y="240" width="480" height="150" rx="18" fill="#fff7ed"/>'+f'<rect x="145" y="265" width="100" height="100" rx="14" fill="#fdba74"/>'+t(270,305,"Trail runner 2",22,700)+t(270,338,"SKU TR2-BLK-9",17,500,"#6b7280")
    b+=t(120,450,"Product",20,700)+stars(120,490,5,40)+t(120,580,"Delivery",20,700)+stars(120,620,4,40)
    b+=t(120,710,"Did it match what you expected?",19,600,"#6b7280")+f'<rect x="120" y="725" width="480" height="70" rx="14" fill="#f6f8fc" stroke="#e3e8f2"/>'+t(140,768,"Exactly, and it arrived early.",19,500)
    b+=pill(120,815,480,56,"#0a0a0a","Submit",size=19)
    b+=conn("M640 350 L 690 350",A)+conn("M640 640 L 690 640",A)
    b+=card(690,230,430,240,22,"#fff","sh2")+pill(715,252,120,40,"#dcfce7","5 stars",tc="#15803d",size=16)+t(715,335,"Review request sent",22,700)+t(715,370,"Link to the product page",18,500,"#6b7280")+t(715,420,"Customer: M. Chen",17,500,"#6b7280")
    b+=card(690,520,430,240,22,"#fff","sh2")+pill(715,542,120,40,"#fee2e2","2 stars",tc="#b91c1c",size=16)+t(715,625,"Returns team flagged",22,700)+t(715,660,"Order #10377 · sizing",18,500,"#6b7280")+t(715,710,"Follow-up within a day",17,500,"#6b7280")
    return svg(b,g1,g2)
def sqb_uc3():
    g1,g2,A,L=PAL["sqb"]
    b=card(80,100,1040,520)+row_head(80,100,1040,"Q3 customer satisfaction · by account","Database",A)
    b+=t(120,205,"ACCOUNT",15,700,"#9ca3af",ls=1.5)+t(430,205,"ACCOUNT EXEC",15,700,"#9ca3af",ls=1.5)+t(660,205,"CSAT",15,700,"#9ca3af",ls=1.5)+t(780,205,"NPS",15,700,"#9ca3af",ls=1.5)+t(900,205,"VS Q2",15,700,"#9ca3af",ls=1.5)
    for i,(a,ae,cs,nps,tr) in enumerate([("Northwind","J. Alvarez","4.6","+52","▲ 6"),("Globex","R. Singh","4.2","+31","▲ 2"),("Initech","M. Rossi","3.1","−8","▼ 24"),("Umbrella Co","J. Alvarez","4.4","+40","▲ 4")]):
        y=235+i*90; bad=tr.startswith("▼")
        if bad: b+=f'<rect x="100" y="{y}" width="1000" height="74" rx="14" fill="#fef2f2"/>'
        b+=t(120,y+46,a,21,700)+t(430,y+46,ae,20,500,"#374151")+t(660,y+46,cs,21,700)+t(780,y+46,nps,21,700)+t(900,y+46,tr,20,700,"#b91c1c" if bad else "#15803d")
    b+=conn("M600 620 L 600 670",A)
    b+=card(80,670,640,230,22,"#fff","sh2")+pill(105,692,200,40,"#fff7ed","HubSpot · Initech",tc=A,size=15)
    b+=t(105,770,"QBR summary written",22,700)
    for i,l in enumerate(["• Support response time is the top theme","• Two users flagged onboarding effort"]):
        b+=t(105,810+i*32,l,17,500,"#374151")
    b+=card(760,670,360,230,22,"#fff","sh2")+pill(785,692,160,40,"#fee2e2","AE alert",tc="#b91c1c",size=15)+t(785,770,"NPS dropped 24",22,700)+t(785,806,"Sent to M. Rossi",18,500,"#6b7280")
    return svg(b,g1,g2)
def sqb_uc4():
    g1,g2,A,L=PAL["sqb"]
    b=card(80,100,520,440)+pill(110,125,220,40,"#dcfce7","Ticket #8841 closed",tc="#15803d",size=15)
    b+=t(110,220,"How satisfied are you",24,800)+t(110,252,"with the help you got?",24,800)
    for i in range(5):
        x=110+i*92; sel=i==3
        b+=f'<rect x="{x}" y="285" width="78" height="78" rx="16" fill="{"#0a0a0a" if sel else "#f6f8fc"}" stroke="#e3e8f2"/>'+t(x+39,335,str(i+1),26,800,"#fff" if sel else "#374151","middle")
    b+=t(110,405,"Agent: Sofia · Billing · resolved in 38m",17,500,"#6b7280")+pill(110,440,460,58,"#0a0a0a","Send feedback",size=19)
    b+=card(640,100,480,440)+t(675,160,"CSAT by agent · this week",20,700)
    for i,(n,v) in enumerate([("Sofia",4.7),("Marcus",4.5),("Priya",4.1),("Tom",3.2)]):
        y=195+i*80
        b+=t(675,y+32,n,19,700)+f'<rect x="790" y="{y+14}" width="240" height="24" rx="12" fill="#ffedd5"/><rect x="790" y="{y+14}" width="{240*v/5:.0f}" height="24" rx="12" fill="{A if v>=4 else "#ef4444"}"/>'+t(1090,y+33,f"{v}",19,800,anchor="end")
    b+=card(80,590,1040,310,22,"#fff","sh2")+pill(110,615,210,40,"#fff7ed","# support-leads",tc=A,size=16)
    b+=t(110,700,"Low score on ticket #8790",24,800)+t(110,738,"CSAT 2 · Tom · Billing · resolved in 2d 4h",19,600,"#374151")
    b+=f'<rect x="110" y="765" width="980" height="100" rx="14" fill="#f8fafc"/>'+t(135,808,"“I had to explain the refund issue three times.”",20,500,"#374151")+t(135,842,"Open ticket →",18,700,A)
    return svg(b,g1,g2)

files={"uc-lp-1-lead-magnet":lp1,"uc-lp-2-ecommerce-order":lp2,"uc-lp-3-webinar-event":lp3,"uc-lp-4-contact-booking":lp4,
"uc-form-1-brand-ambassadors":form1,"uc-form-2-ugc-creators":form2,"uc-form-3-affiliate-programs":form3,"uc-form-4-creator-hiring":form4,
"uc-aab-1-purchase-order":aab_uc1,"uc-aab-2-invoice":aab_uc2,"uc-aab-3-contract":aab_uc3,"uc-aab-4-expense":aab_uc4,
"uc-sqb-1-saas-onboarding":sqb_uc1,"uc-sqb-2-post-purchase":sqb_uc2,"uc-sqb-3-b2b-quarterly":sqb_uc3,"uc-sqb-4-support-ticket":sqb_uc4}
import os; os.makedirs('uc',exist_ok=True)
for n,fn in files.items():
    s=fn(); p=f'uc/{n}.svg'; open(p,'w').write(s); xml.dom.minidom.parse(p); cairosvg.svg2png(url=p,write_to=p.replace('.svg','.png'),output_width=900)
for hub in ["lp","form","aab","sqb"]:
    fs=[n for n in files if n.startswith(f'uc-{hub}-')]; ims=[Image.open(f'uc/{n}.png') for n in fs]; w,h=ims[0].size
    sh=Image.new('RGB',(w*2+20,h*2+20),'white')
    for i,im in enumerate(ims): sh.paste(im,((i%2)*(w+20),(i//2)*(h+20)))
    sh.save(f'uc/sheet-{hub}.png')
print('ok',len(files))
