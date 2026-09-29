"""Scene library v2 — built for the use-case slot: 3:2 (build-usecase_image aspect-ratio 3/2, object-fit fill).
Design canvas 1200x800 -> render 3000x2000. Min text 16 design px (>=11px on screen at an 830px slot)."""
import sys, math; sys.path.insert(0,'/home/claude/cards')
import helpers as h
h.W,h.H=1200,800
from helpers import card,t,pill,dots
PAL={"lp":("#eaf2ff","#c7dbff","#2563eb","#dbeafe"),"form":("#eafbf4","#c4efdc","#059669","#d1fae5"),
     "aab":("#f3efff","#ddd3ff","#7c3aed","#ede9fe"),"sqb":("#fff6ec","#ffe2c4","#ea580c","#ffedd5")}
def svg(b,hub): g1,g2,_,_=PAL[hub]; return h.svg(b,g1,g2)
def conn(d,c): return f'<path d="{d}" stroke="{c}" stroke-width="5" fill="none" stroke-linecap="round" stroke-dasharray="2 12"/>'
def check(cx,cy,r): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#dcfce7"/><path d="M{cx-r*.42:.1f} {cy} l{r*.3:.1f} {r*.3:.1f} l{r*.55:.1f} -{r*.6:.1f}" stroke="#16a34a" stroke-width="{max(3,r*.16):.0f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
def field(x,y,w,label,val,hh=52): return t(x,y-10,label,17,600,"#6b7280")+f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="12" fill="#f6f8fc" stroke="#e3e8f2"/>'+t(x+18,y+hh/2+8,val,21,600,"#111827")
def browser(x,y,w,hh,url):
    b=card(x,y,w,hh)+f'<rect x="{x}" y="{y}" width="{w}" height="64" rx="28" fill="#f3f5f9"/><rect x="{x}" y="{y+36}" width="{w}" height="28" fill="#f3f5f9"/>'+dots(x+36,y+33)
    b+=f'<rect x="{x+120}" y="{y+13}" width="{w-240}" height="38" rx="19" fill="#fff" stroke="#e3e8f2"/>'+t(x+144,y+39,url,17,600,"#374151")
    return b
def head(x,y,w,title,acc,tag="Database"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="68" rx="26" fill="#0a0a0a"/><rect x="{x}" y="{y+36}" width="{w}" height="32" fill="#0a0a0a"/>'+t(x+32,y+44,title,23,700,"#fff")+pill(x+w-184,y+13,164,42,"#1f2937",tag,tc="#e5e7eb",size=17,dot=acc)
def outline_pill(x,y,w,hh,label,size=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="{hh/2}" fill="#fff" stroke="#d6dce8" stroke-width="2"/>'+t(x+w/2,y+hh/2+size*0.36,label,size,600,"#111827","middle")
def stars(x,y,n,size=36):
    s=""
    for i in range(5):
        cx=x+i*(size+8)+size/2; pts=[]
        for k in range(10):
            r=size/2 if k%2==0 else size/4.6; a=math.pi/2+k*math.pi/5; pts.append(f"{cx+r*math.cos(a):.1f},{y-r*math.sin(a):.1f}")
        s+=f'<polygon points="{" ".join(pts)}" fill="{"#f59e0b" if i<n else "#e5e7eb"}"/>'
    return s
def status(x,y,w,label,kind,size=17):
    bg,tc={"ok":("#dcfce7","#15803d"),"wait":("#fef3c7","#92400e"),"bad":("#fee2e2","#b91c1c"),"na":("#f1f5f9","#64748b")}[kind]
    return pill(x,y,w,42,bg,label,tc=tc,size=size)

# ---------------- LP · Thank you page ----------------
def lp1():
    _,_,A,L=PAL["lp"]
    b=browser(56,56,700,688,"yourbrand.com/thank-you")
    b+=check(406,222,44)+t(406,322,"You're in! Your playbook is ready.",29,800,anchor="middle")
    b+=t(406,362,"Check your inbox in two minutes for a copy.",19,500,"#6b7280","middle")
    b+=pill(166,400,480,64,"#0a0a0a","↓  Download the playbook (PDF)",size=20)
    b+=f'<rect x="96" y="520" width="620" height="124" rx="20" fill="{L}"/>'+t(126,566,"One more thing",17,700,A)+t(126,606,"Book a 15-minute walkthrough",22,700)+pill(566,558,126,52,A,"Book now",size=18)
    b+=card(796,170,348,196)+check(846,228,26)+t(888,222,"Lead saved",24,700)+t(888,252,"to your database",18,500,"#6b7280")
    b+=pill(826,292,288,42,L,"utm_source: linkedin",tc=A,size=17)
    b+=card(796,420,348,150)+t(830,478,"Conversion goal",23,700)+pill(830,500,276,42,"#dcfce7","Pixel fired on load",tc="#15803d",size=17,dot="#22c55e")
    b+=conn("M756 268 L 796 268",A)+conn("M756 495 L 796 495",A)
    return svg(b,"lp")
def lp2():
    _,_,A,L=PAL["lp"]
    b=browser(56,56,1088,688,"shop.yourbrand.com/order/10482")
    b+=check(130,180,32)+t(180,176,"Order #10482 confirmed",30,800)+t(180,208,"Thanks, Maya. Your receipt is on its way.",19,500,"#6b7280")
    for i,(s,d) in enumerate([("Ordered","Monday"),("Shipped","Tuesday"),("Arrives","Thursday")]):
        x=190+i*410
        if i<2: b+=f'<line x1="{x+20}" y1="276" x2="{x+390}" y2="276" stroke="{A if i==0 else "#e5e7eb"}" stroke-width="6"/>'
        b+=f'<circle cx="{x}" cy="276" r="16" fill="{A if i<2 else "#e5e7eb"}"/>'+t(x,322,s,20,700,anchor="middle")+t(x,348,d,17,500,"#6b7280","middle")
    b+=f'<rect x="96" y="392" width="500" height="312" rx="22" fill="#f8fafc" stroke="#eef1f6"/>'+t(126,436,"Pairs well with your order",17,700,A)
    b+=f'<rect x="126" y="460" width="120" height="120" rx="18" fill="{L}"/><rect x="156" y="494" width="60" height="52" rx="10" fill="{A}" opacity="0.5"/>'
    b+=t(270,504,"Travel case",25,700)+t(270,538,"$29 · ships with your order",18,500,"#6b7280")+pill(126,616,220,56,"#0a0a0a","Add to order",size=19)
    b+=f'<rect x="624" y="392" width="480" height="312" rx="22" fill="{L}" stroke="{A}" stroke-width="2" stroke-dasharray="10 8"/>'
    b+=t(656,448,"10% off your next order",26,800)+t(656,482,"Use it within 30 days",19,500,"#374151")
    b+=f'<rect x="656" y="512" width="416" height="84" rx="16" fill="#fff"/>'+t(864,568,"THANKS10",36,800,anchor="middle",ls=2)
    b+=pill(656,620,190,52,A,"Copy code",size=19)
    return svg(b,"lp")
def lp3():
    _,_,A,L=PAL["lp"]
    b=browser(56,56,1088,688,"yourbrand.com/webinar/registered")
    b+=check(130,180,32)+t(180,176,"You're registered",30,800)+t(180,208,"We saved your seat for the live session.",19,500,"#6b7280")
    b+=f'<rect x="96" y="250" width="580" height="150" rx="22" fill="{L}"/><rect x="124" y="275" width="100" height="100" rx="18" fill="#fff"/>'
    b+=t(174,312,"OCT",18,800,A,"middle")+t(174,358,"14",40,800,anchor="middle")+t(252,316,"Scaling onboarding with AI",23,800)+t(252,352,"Tue · 10:00 AM PT · 45 min",19,500,"#374151")
    b+=pill(96,430,180,54,"#0a0a0a","+ Google",size=18)+outline_pill(296,430,180,54,"+ Outlook")+outline_pill(496,430,180,54,"+ Apple")
    b+=t(96,550,"Invite a colleague",20,700)+f'<rect x="96" y="568" width="400" height="56" rx="14" fill="#f6f8fc" stroke="#e3e8f2"/>'+t(118,603,"colleague@company.com",18,500,"#9ca3af")+pill(512,568,164,56,A,"Send invite",size=18)
    b+=t(724,272,"Reminder schedule",22,700)
    for i,(w,c) in enumerate([("1 day before","Email"),("1 hour before","Email and SMS"),("Starting now","Join link")]):
        y=296+i*124
        b+=f'<rect x="724" y="{y}" width="380" height="104" rx="18" fill="#f8fafc" stroke="#eef1f6"/>'+f'<circle cx="760" cy="{y+52}" r="10" fill="{A}"/>'+t(788,y+46,w,21,700)+t(788,y+76,c,18,500,"#6b7280")
    return svg(b,"lp")
def lp4():
    _,_,A,L=PAL["lp"]
    b=browser(56,56,700,688,"yourbrand.com/contact/thanks")
    b+=check(130,180,32)+t(180,176,"Thanks, we got it",29,800)+t(180,208,"We'll reply within 24 hours.",19,500,"#6b7280")
    b+=t(96,280,"Rather talk now? Pick a time.",22,700)+t(96,310,"Thursday, October 16",18,600,"#6b7280")
    for i,s in enumerate(["9:30 AM","11:00 AM","1:30 PM","3:00 PM","4:30 PM","5:00 PM"]):
        x=96+(i%2)*320; y=334+(i//2)*80; sel=i==2
        b+=f'<rect x="{x}" y="{y}" width="300" height="62" rx="14" fill="{A if sel else "#fff"}" stroke="{A if sel else "#e3e8f2"}" stroke-width="2"/>'+t(x+150,y+39,s,20,700,"#fff" if sel else "#111827","middle")
    b+=pill(96,600,620,62,"#0a0a0a","Confirm 1:30 PM",size=20)
    for j,(tag,ti,l1,l2,y) in enumerate([("# sales","New enquiry","Priya · Acme Corp","Demo request · 50 seats",150),("CRM","Deal created","Stage: new lead","Owner assigned",400)]):
        b+=card(796,y,348,200,22,"#fff","sh2")+pill(826,y+24,130,40,L,tag,tc=A,size=17)+t(826,y+106,ti,24,700)+t(826,y+140,l1,19,500,"#374151")+t(826,y+170,l2,17,500,"#6b7280")
        b+=conn(f"M756 {y+100} L 796 {y+100}",A)
    return svg(b,"lp")

# ---------------- FORM · Creator application ----------------
def form1():
    _,_,A,L=PAL["form"]
    b=card(56,56,520,688)+t(88,116,"Brand ambassador application",26,800)+t(88,150,"Tell us why you love the brand",18,500,"#6b7280")
    b+=field(88,214,456,"Instagram handle","@maya.moves")+field(88,322,456,"Favorite product","Trail runner 2")
    b+=t(88,418,"Why do you love us?",17,600,"#6b7280")+f'<rect x="88" y="428" width="456" height="150" rx="12" fill="#f6f8fc" stroke="#e3e8f2"/>'
    b+=t(106,472,"I've run three marathons in them",19,500)+t(106,502,"and recommend them to my club.",19,500)
    b+=pill(88,630,456,62,"#0a0a0a","Apply to the program",size=20)
    b+=conn("M576 380 L 636 380",A)
    b+=card(636,166,508,430)+check(690,230,32)+t(740,226,"Approved",30,800)+t(740,258,"Audience 18k · US West",19,500,"#6b7280")
    b+=f'<rect x="668" y="302" width="444" height="124" rx="18" fill="{L}" stroke="{A}" stroke-width="2" stroke-dasharray="10 8"/>'+t(698,346,"Your referral code",17,700,A)+t(698,398,"MAYA15",40,800,ls=2)
    b+=t(668,482,"Welcome kit ships Friday",22,700)+t(668,516,"Tracked link sent by email",18,500,"#6b7280")
    b+=pill(636,636,340,56,"#fff","Saved to creators table",tc="#111827",size=18,dot="#22c55e")
    return svg(b,"form")
def form2():
    _,_,A,L=PAL["form"]
    b=card(56,56,1088,688)+t(96,120,"UGC samples · review board",28,800)+pill(924,86,180,46,L,"12 to review",tc=A,size=17)
    for i,(n,niche,r,tag,d) in enumerate([("Jordan","Skincare",5,"Unboxing","0:28"),("Aisha","Fitness",4,"Talking head","0:34"),("Leo","Tech",3,"Voiceover","0:19")]):
        x=96+i*344
        b+=f'<rect x="{x}" y="156" width="320" height="300" rx="20" fill="#0f172a"/><circle cx="{x+160}" cy="306" r="42" fill="#fff" opacity="0.92"/><path d="M{x+148} 284 l32 22 l-32 22 z" fill="#0f172a"/>'+t(x+20,436,d,17,700,"#e5e7eb")
        b+=t(x,500,n,24,700)+t(x,530,niche+" · 3-day turnaround",18,500,"#6b7280")+stars(x,572,r,30)+pill(x,600,190,42,L,tag,tc=A,size=17)
    b+=pill(96,666,280,54,"#0a0a0a","Book for next brief",size=19)+t(400,700,"Jordan: tagged Unboxing, rated 5 by 2 reviewers",18,500,"#6b7280")
    return svg(b,"form")
def form3():
    _,_,A,L=PAL["form"]
    b=card(56,56,1088,150)+t(88,98,"Auto-approve rule",18,700,A)+f'<rect x="88" y="114" width="1024" height="68" rx="16" fill="{L}"/>'+t(116,157,"If monthly reach ≥ 10,000 → approve, send a tracked link, assign a tier",22,700)
    b+=card(56,238,1088,506)+head(56,238,1088,"affiliates",A)
    for x,l in [(88,"CREATOR"),(430,"REACH"),(600,"TIER"),(790,"TRACKED LINK")]: b+=t(x,346,l,16,700,"#9ca3af",ls=1.2)
    for i,(c,r,tr,k,l) in enumerate([("@runwithsam","48,200","Gold","wait","yourbrand.co/r/sam"),("@techwithtara","22,900","Silver","na","yourbrand.co/r/tara"),("@homecafe.kim","12,400","Silver","na","yourbrand.co/r/kim"),("@minimal.nate","6,100","Waitlist","bad","—")]):
        y=366+i*90
        b+=t(88,y+46,c,22,700)+t(430,y+46,r,22,600,"#374151")+status(600,y+18,140,tr,k)+t(790,y+46,l,20,600,A if l!="—" else "#9ca3af")
        if i<3: b+=f'<line x1="88" y1="{y+84}" x2="1112" y2="{y+84}" stroke="#eef1f6" stroke-width="2"/>'
    return svg(b,"form")
def form4():
    _,_,A,L=PAL["form"]
    b=card(56,56,700,688)+t(96,114,"Content creator role · shortlist",26,800)+t(96,146,"Scored by fit on arrival",18,500,"#6b7280")
    for i,(n,det,s) in enumerate([("Riya Patel","TikTok, YouTube · 4 yrs",94),("Sam Ortiz","Instagram · 3 yrs",88),("Chen Wei","YouTube · 5 yrs",81),("Ada Brooks","TikTok · 2 yrs",67)]):
        y=176+i*140
        b+=f'<rect x="96" y="{y}" width="620" height="120" rx="18" fill="#f8fafc" stroke="#eef1f6"/><circle cx="154" cy="{y+60}" r="30" fill="{L}"/>'+t(154,y+70,n[0],26,800,A,"middle")
        b+=t(202,y+52,n,23,700)+t(202,y+84,det,18,500,"#6b7280")
        b+=f'<rect x="520" y="{y+52}" width="130" height="16" rx="8" fill="#e5e7eb"/><rect x="520" y="{y+52}" width="{130*s/100:.0f}" height="16" rx="8" fill="{A}" opacity="{1 if s>=80 else .45}"/>'+t(696,y+68,str(s),24,800,anchor="end")
    b+=conn("M756 400 L 796 400",A)
    b+=card(796,270,348,260,22,"#fff","sh2")+pill(826,294,234,40,L,"# creative-hiring",tc=A,size=17)
    b+=t(826,382,"Shortlist ready",24,700)+t(826,416,"3 candidates above 80",19,500,"#374151")+t(826,452,"Interviews booked from",18,500,"#6b7280")+t(826,478,"the application",18,500,"#6b7280")
    return svg(b,"form")

# ---------------- AAB · Approval workflow ----------------
def aab1():
    _,_,A,L=PAL["aab"]
    b=card(56,56,440,340)+t(88,110,"Purchase request",28,800)
    b+=field(88,158,376,"Item","Design licenses ×12")+field(88,256,376,"Vendor","Figma · approved list")
    b+=t(88,372,"$4,800",44,800)+pill(312,340,152,42,L,"Marketing",tc=A,size=18)
    b+=conn("M496 226 L 536 226",A)
    for i,(who,rng,st,k) in enumerate([("Manager","Under $500","not needed","na"),("Department head","$500 to $5,000","approved","ok"),("CFO","Over $5,000","not needed","na")]):
        y=56+i*116; hot=i==1
        b+=card(536,y,608,100,20,"#fff","sh2",A if hot else "#e6ebf5")+f'<circle cx="578" cy="{y+50}" r="13" fill="{A if hot else "#cbd5e1"}"/>'
        b+=t(608,y+44,who,24,700)+t(608,y+76,rng,19,500,"#6b7280")+status(956,y+29,164,st,k)
    b+=card(56,436,1088,308)+head(56,436,1088,"approvals · audit log",A)
    for x,l in [(88,"REQUESTER"),(420,"AMOUNT"),(600,"APPROVER"),(860,"TIME TO APPROVE")]: b+=t(x,544,l,16,700,"#9ca3af",ls=1.2)
    for i,(r,a,ap,tm) in enumerate([("Nina · Marketing","$4,800","Dept head","2h 14m"),("Omar · Ops","$320","Manager","18m"),("Lee · Eng","$12,500","CFO","1d 3h")]):
        y=566+i*56; b+=t(88,y+34,r,22,700)+t(420,y+34,a,22,700)+t(600,y+34,ap,22,500,"#374151")+t(860,y+34,tm,22,700,A)
    return svg(b,"aab")
def aab2():
    _,_,A,L=PAL["aab"]
    b=card(56,56,470,688)+t(88,108,"INVOICE",18,800,"#9ca3af",ls=3)+pill(318,78,180,42,A,"AI extracted",size=17)+t(88,152,"Northwind Supplies",28,800)
    for i,(k,v,hl) in enumerate([("Invoice number","INV-7731",False),("PO reference","PO-2231",True),("Vendor","Northwind Supplies",True),("Amount due","$2,340.00",True),("Due date","Nov 12",False)]):
        y=192+i*84
        if hl: b+=f'<rect x="76" y="{y}" width="430" height="70" rx="14" fill="{L}" stroke="{A}" stroke-width="2"/>'
        b+=t(98,y+28,k,17,600,"#6b7280")+t(98,y+56,v,22,700)
    for i in range(3): b+=f'<rect x="88" y="{636+i*30}" width="{380-i*70}" height="14" rx="7" fill="#eef1f6"/>'
    b+=conn("M526 400 L 586 400",A)
    for i,(ti,su) in enumerate([("Matched to PO-2231","Amounts agree"),("Routed to finance","Over $1,000 · cost center 410"),("Approved","By J. Alvarez in 3 hours"),("Written to Xero","Bill created with the PDF attached")]):
        y=56+i*172
        b+=card(586,y,558,140,20,"#fff","sh2")+check(642,y+70,28)+t(690,y+62,ti,24,700)+t(690,y+96,su,19,500,"#6b7280")
        if i<3: b+=f'<line x1="642" y1="{y+140}" x2="642" y2="{y+172}" stroke="{A}" stroke-width="4"/>'
    return svg(b,"aab")
def aab3():
    _,_,A,L=PAL["aab"]
    b=card(56,56,1088,140)+f'<rect x="88" y="80" width="72" height="92" rx="10" fill="{L}" stroke="{A}" stroke-width="2"/>'+t(124,134,"PDF",18,800,A,"middle")
    b+=t(184,118,"Master services agreement · v3",28,800)+t(184,154,"Routed to three reviewers in parallel",19,500,"#6b7280")+status(944,105,176,"SLA: 2 days","wait",18)
    for i,(who,st,k,l1,l2) in enumerate([("Legal","approved","ok","Approved","One red-line resolved"),("Finance","approved","ok","Approved","Payment terms confirmed"),("Executive","pending","wait","Waiting","Reminder in 2 days")]):
        x=56+i*372
        b+=conn(f"M600 196 C 600 222, {x+172} 222, {x+172} 250",A)
        b+=card(x,250,344,210,20,"#fff","sh2")+t(x+30,308,who,26,800)+status(x+30,330,150,st,k)+t(x+30,410,l1,20,700,"#374151")+t(x+30,440,l2,18,500,"#6b7280")
    b+=conn("M600 460 L 600 506",A)
    b+=card(212,506,776,238)+t(248,552,"When all three approve",18,700,A)
    for i,(ti,su) in enumerate([("Send for e-signature","Counterparty signs online"),("Save the signed PDF","Google Drive · Contracts"),("Log every version","Approvers and timestamps")]):
        y=576+i*54; b+=check(266,y+22,18)+t(300,y+30,ti,21,700)+t(620,y+30,su,18,500,"#6b7280")
    return svg(b,"aab")
def aab4():
    _,_,A,L=PAL["aab"]
    b=card(56,56,520,340)+t(88,106,"Submit an expense",26,800)
    b+=f'<rect x="88" y="130" width="150" height="170" rx="14" fill="#f8fafc" stroke="#e3e8f2" stroke-dasharray="6 6"/>'
    for i in range(5): b+=f'<rect x="108" y="{154+i*26}" width="{110-(i%3)*22}" height="10" rx="5" fill="#e5e7eb"/>'
    b+=t(262,160,"Client dinner",24,700)+t(262,190,"Project: Atlas",18,500,"#6b7280")+t(262,252,"$180",44,800)+pill(262,270,150,40,L,"Meals",tc=A,size=17)
    b+=pill(88,322,456,54,"#0a0a0a","Submit for approval",size=19)
    b+=card(620,56,524,340)+t(652,104,"Atlas budget · this month",20,700)+t(652,168,"$3,380",44,800)+t(820,168,"of $4,000",22,600,"#6b7280")
    b+=f'<rect x="652" y="192" width="460" height="28" rx="14" fill="{L}"/><rect x="652" y="192" width="{460*3200/4000:.0f}" height="28" rx="14" fill="{A}"/><rect x="{652+460*3200/4000:.0f}" y="192" width="{460*180/4000:.0f}" height="28" fill="#a78bfa"/>'
    b+=pill(652,244,236,44,"#dcfce7","Within policy",tc="#15803d",size=18,dot="#22c55e")+t(652,336,"→ Manager approval",23,700)+t(652,368,"Out of policy → finance review",18,500,"#6b7280")
    b+=card(56,436,1088,308)+head(56,436,1088,"expense decisions",A)
    for i,(w,a,st,k,note) in enumerate([("Client dinner","$180","approved","ok","Added to the export queue"),("Conference pass","$1,250","escalated","wait","Over policy · finance"),("Taxi receipts","$64","declined","bad","Receipt missing · returned")]):
        y=526+i*70; b+=t(88,y+36,w,22,700)+t(420,y+36,a,22,700)+status(560,y+8,150,st,k)+t(740,y+36,note,19,500,"#6b7280")
    return svg(b,"aab")

# ---------------- SQB · Customer satisfaction ----------------
def sqb1():
    _,_,A,L=PAL["sqb"]
    b=card(56,56,1088,330)+t(96,116,"Onboarding survey · Acme Corp",28,800)+t(96,148,"CSAT and effort at each touch",19,500,"#6b7280")
    b+=f'<line x1="200" y1="236" x2="1000" y2="236" stroke="#e5e7eb" stroke-width="6"/>'
    for i,(d,cs,ok) in enumerate([("Day 7","CSAT 5 · easy",True),("Day 30","CSAT 4 · easy",True),("Day 90","CSAT 2 · hard",False)]):
        x=200+i*400
        b+=t(x,204,d,22,800,anchor="middle")+f'<circle cx="{x}" cy="236" r="22" fill="{A if ok else "#ef4444"}"/>'
        b+=pill(x-110,280,220,48,"#fff7ed" if ok else "#fee2e2",cs,tc=A if ok else "#b91c1c",size=18)
    b+=t(96,366,"Tied to each account, plan, and CSM",18,600,"#6b7280")
    b+=conn("M1000 328 L 1000 430",A)
    b+=card(56,430,1088,314,22,"#fff","sh2")+pill(88,456,176,42,"#fff7ed","# cs-alerts",tc=A,size=17)
    b+=t(88,548,"Low score from Acme Corp",27,800)+t(88,584,"Day 90 · CSAT 2 · effort: hard",20,600,"#374151")
    b+=f'<rect x="88" y="610" width="1024" height="104" rx="16" fill="#f8fafc"/>'+t(116,652,"“Setting up SSO took our IT team a week.”",21,500,"#374151")+t(116,688,"CSM: Dana · Business plan · previous scores 5 and 4",18,500,"#6b7280")
    return svg(b,"sqb")
def sqb2():
    _,_,A,L=PAL["sqb"]
    b=card(56,56,560,688)+t(88,116,"How did we do?",32,800)+t(88,150,"Order #10482 · delivered Thursday",19,500,"#6b7280")
    b+=f'<rect x="88" y="176" width="496" height="116" rx="18" fill="#fff7ed"/><rect x="110" y="190" width="88" height="88" rx="14" fill="#fdba74"/>'+t(222,226,"Trail runner 2",23,700)+t(222,258,"SKU TR2-BLK-9",17,500,"#6b7280")
    b+=t(88,338,"Product",21,700)+stars(88,378,5,40)+t(88,442,"Delivery",21,700)+stars(88,482,4,40)
    b+=t(88,548,"Did it match what you expected?",18,600,"#6b7280")+f'<rect x="88" y="562" width="496" height="62" rx="14" fill="#f6f8fc" stroke="#e3e8f2"/>'+t(108,601,"Exactly, and it arrived early.",19,500)
    b+=pill(88,652,496,58,"#0a0a0a","Submit",size=20)
    b+=conn("M616 260 L 660 260",A)+conn("M616 540 L 660 540",A)
    b+=card(660,150,484,230,22,"#fff","sh2")+status(690,174,130,"5 stars","ok")+t(690,266,"Review request sent",25,700)+t(690,300,"Link to the product page",19,500,"#374151")+t(690,340,"Customer: M. Chen",18,500,"#6b7280")
    b+=card(660,430,484,230,22,"#fff","sh2")+status(690,454,130,"2 stars","bad")+t(690,546,"Returns team flagged",25,700)+t(690,580,"Order #10377 · sizing",19,500,"#374151")+t(690,620,"Follow-up within a day",18,500,"#6b7280")
    return svg(b,"sqb")
def sqb3():
    _,_,A,L=PAL["sqb"]
    b=card(56,56,1088,440)+head(56,56,1088,"Q3 satisfaction · by account",A)
    for x,l in [(88,"ACCOUNT"),(400,"ACCOUNT EXEC"),(650,"CSAT"),(790,"NPS"),(930,"VS Q2")]: b+=t(x,160,l,16,700,"#9ca3af",ls=1.2)
    for i,(a,ae,cs,nps,tr) in enumerate([("Northwind","J. Alvarez","4.6","+52","▲ 6"),("Globex","R. Singh","4.2","+31","▲ 2"),("Initech","M. Rossi","3.1","−8","▼ 24"),("Umbrella Co","J. Alvarez","4.4","+40","▲ 4")]):
        y=180+i*76; bad=tr.startswith("▼")
        if bad: b+=f'<rect x="76" y="{y}" width="1048" height="66" rx="14" fill="#fef2f2"/>'
        b+=t(88,y+42,a,22,700)+t(400,y+42,ae,21,500,"#374151")+t(650,y+42,cs,22,700)+t(790,y+42,nps,22,700)+t(930,y+42,tr,21,700,"#b91c1c" if bad else "#15803d")
    b+=conn("M386 496 L 386 540",A)+conn("M950 496 L 950 540",A)
    b+=card(56,540,660,204,22,"#fff","sh2")+pill(86,564,220,42,"#fff7ed","HubSpot · Initech",tc=A,size=17)+t(86,646,"QBR summary written",24,700)
    b+=t(86,682,"• Support response time is the top theme",18,500,"#374151")+t(86,712,"• Two users flagged onboarding effort",18,500,"#374151")
    b+=card(756,540,388,204,22,"#fff","sh2")+status(786,564,150,"AE alert","bad")+t(786,646,"NPS dropped 24",24,700)+t(786,682,"Sent to M. Rossi",19,500,"#6b7280")
    return svg(b,"sqb")
def sqb4():
    _,_,A,L=PAL["sqb"]
    b=card(56,56,520,380)+status(86,80,236,"Ticket #8841 closed","ok",16)
    b+=t(86,172,"How satisfied are you",26,800)+t(86,206,"with the help you got?",26,800)
    for i in range(5):
        x=86+i*94; sel=i==3
        b+=f'<rect x="{x}" y="230" width="80" height="80" rx="16" fill="{"#0a0a0a" if sel else "#f6f8fc"}" stroke="#e3e8f2"/>'+t(x+40,280,str(i+1),26,800,"#fff" if sel else "#374151","middle")
    b+=t(86,346,"Agent: Sofia · Billing · resolved in 38 min",17,500,"#6b7280")+pill(86,364,460,52,"#0a0a0a","Send feedback",size=19)
    b+=card(620,56,524,380)+t(652,104,"CSAT by agent · this week",21,700)
    for i,(n,v) in enumerate([("Sofia",4.7),("Marcus",4.5),("Priya",4.1),("Tom",3.2)]):
        y=134+i*72
        b+=t(652,y+30,n,20,700)+f'<rect x="760" y="{y+11}" width="300" height="26" rx="13" fill="#ffedd5"/><rect x="760" y="{y+11}" width="{300*v/5:.0f}" height="26" rx="13" fill="{A if v>=4 else "#ef4444"}"/>'+t(1112,y+32,f"{v}",21,800,anchor="end")
    b+=card(56,476,1088,268,22,"#fff","sh2")+pill(86,500,210,42,"#fff7ed","# support-leads",tc=A,size=17)
    b+=t(86,590,"Low score on ticket #8790",26,800)+t(86,626,"CSAT 2 · Tom · Billing · resolved in 2d 4h",20,600,"#374151")
    b+=f'<rect x="86" y="650" width="1028" height="70" rx="14" fill="#f8fafc"/>'+t(112,693,"“I had to explain the refund issue three times.”",20,500,"#374151")+t(1090,693,"Open ticket →",18,700,A,"end")
    return svg(b,"sqb")

SCENES={"uc-lp-1-lead-magnet":lp1,"uc-lp-2-ecommerce-order":lp2,"uc-lp-3-webinar-event":lp3,"uc-lp-4-contact-booking":lp4,
"uc-form-1-brand-ambassadors":form1,"uc-form-2-ugc-creators":form2,"uc-form-3-affiliate-programs":form3,"uc-form-4-creator-hiring":form4,
"uc-aab-1-purchase-order":aab1,"uc-aab-2-invoice":aab2,"uc-aab-3-contract":aab3,"uc-aab-4-expense":aab4,
"uc-sqb-1-saas-onboarding":sqb1,"uc-sqb-2-post-purchase":sqb2,"uc-sqb-3-b2b-quarterly":sqb3,"uc-sqb-4-support-ticket":sqb4}
