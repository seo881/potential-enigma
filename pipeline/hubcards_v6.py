"""Hub-card covers v6 for 'More things you can build': 1000x400 (5:2), shown at ~400x160 CSS px.
Real v5 product moments (outlined Inter text >= 28 design px = 11.2px on screen), one hero per cover, calm left zone
(the card's icon tile overlaps the bottom-left)."""
import ds5 as L, hubs5 as H
from qa import width as tw
T,rect,icon,avatar=L.T,L.rect,L.icon,L.avatar
INK,SUB,MUTED=L.INK,L.SUB,L.MUTED
NEW={ # new hub-grade palettes; white text on acc passes AA at the lighter stop
 "amber":dict(acc="#B45309",acc2="#92400E",accd="#92400E",accs="#FEF3C7",accm="#FDE68A",bg1="#FFFCF0",bg2="#FCE7B0",glow="#FDE68A",grid="#B45309",spot="#F59E0B",sh="#78350F",line="#F0E7D2",hair="#F6EFDF",stroke1="#FCD34D",stroke2="#FBBF24"),
 "cyan":dict(acc="#0E7490",acc2="#155E75",accd="#155E75",accs="#E0F7FB",accm="#A5E9F4",bg1="#F5FDFF",bg2="#C9F0F8",glow="#BDEFF8",grid="#0E7490",spot="#06B6D4",sh="#164E63",line="#D8ECF0",hair="#E6F4F7",stroke1="#67E8F9",stroke2="#22D3EE"),
 "rose":dict(acc="#BE123C",acc2="#9F1239",accd="#9F1239",accs="#FFE4E8",accm="#FECDD5",bg1="#FFF7F8",bg2="#FFD6DD",glow="#FFC9D2",grid="#BE123C",spot="#F43F5E",sh="#881337",line="#F2DEE2",hair="#F8EAED",stroke1="#FDA4AF",stroke2="#FB7185"),
 "indigo":dict(acc="#4F46E5",acc2="#4338CA",accd="#3730A3",accs="#EEF0FF",accm="#C7C9FF",bg1="#F8F8FF",bg2="#DAD9FF",glow="#CFCDFF",grid="#4338CA",spot="#6366F1",sh="#312E81",line="#E2E1F3",hair="#ECEBF8",stroke1="#A5B4FC",stroke2="#818CF8"),
 "teal":dict(acc="#0F766E",acc2="#115E59",accd="#115E59",accs="#DDF7F0",accm="#A7EBDB",bg1="#F4FFFC",bg2="#C6F0E5",glow="#B5ECDD",grid="#0F766E",spot="#14B8A6",sh="#134E4A",line="#D6ECE6",hair="#E5F4F0",stroke1="#5EEAD4",stroke2="#2DD4BF"),
}
H.PALS.update(NEW)
PAL={"website":"lp","app":"amber","webapp":"form","saas":"cyan","dashboard":"aab","crm":"rose","agent":"indigo","schedule":"sqb","chatbot":"teal"}
def cv(b,title,desc):
    L.W,L.H=1000,400
    try: return L.canvas(b,title=title,desc=desc)
    finally: L.W,L.H=1200,800
A=lambda: L.ACC
def card(x,y,w,h,r=20,f="e1"): return rect(x,y,w,h,r,"#fff",L.LINE,1,f)
def hero(x,y,w,h,r=22): return L.spot(x,y,w,h)+rect(x,y,w,h,r,"#fff",L.LINE,1,"e2")
def pill(x,y,label,fg,bg,size=28,w=None,h=46):
    w=w or int(tw(label,size,600)+44); return rect(x,y,w,h,h/2,bg)+T(x+w/2,y+h/2+size*0.36,label,size,600,fg,"middle")
def btn(x,y,label,size=28,h=58):
    w=int(tw(label,size,600)+60); return rect(x,y,w,h,14,"url(#gAcc)")+T(x+w/2,y+h/2+size*0.36,label,size,600,"#fff","middle"),w
OK,OKB,WARN,WARNB="#15803D","#DCFCE7","#B45309","#FEF3C7"

def website():
    H.set_hub("lp"); b=card(380,36,580,328,22)
    b+=rect(380,36,580,56,22,"#F8FAFC")+rect(380,70,580,22,0,"#F8FAFC")+"".join(f'<circle cx="{410+i*22}" cy="64" r="7" fill="#CBD5E1"/>' for i in range(3))
    b+=rect(490,48,300,32,16,"#EEF2F7")+icon("lock",506,56,16,MUTED)+T(530,71,"bloomstudio.co",28,500,SUB) if False else rect(490,48,300,32,16,"#EEF2F7")
    b+=T(420,142,"Bloom Studio",28,700,INK)+T(420,210,"Plants, delivered.",40,800,INK,ls=-0.8)
    s,w=btn(420,238,"Shop now"); b+=s
    b+=rect(808,122,124,168,16,L.ACC_S)+icon("sprout",836,172,68,A(),2.2)
    b+=hero(700,300,262,64,18)+'<circle cx="732" cy="332" r="14" fill="#DCFCE7"/>'+icon("check",723,323,18,OK,3)+T(756,342,"Published",28,700,INK)
    return cv(b,"AI Website Builder cover","A published website for Bloom Studio with the headline Plants, delivered and a Shop now button.")
def app():
    H.set_hub("amber"); b=L.spot(520,30,300,340)
    b+=rect(560,24,232,352,38,"#0F172A","none",1,"e2")+rect(572,36,208,328,28,"#FFFFFF")+rect(642,46,68,16,8,"#0F172A")
    b+=T(596,112,"Morning run",28,700,INK)+T(596,176,"5.2 km",48,800,INK,ls=-1,tnum=True)
    b+=f'<circle cx="676" cy="268" r="58" fill="none" stroke="{L.ACC_S}" stroke-width="16"/>'
    b+=f'<circle cx="676" cy="268" r="58" fill="none" stroke="url(#gAcc)" stroke-width="16" stroke-linecap="round" stroke-dasharray="{2*3.1416*58*0.72:.1f} 999" transform="rotate(-90 676 268)"/>'
    b+=T(676,279,"72%",30,800,INK,"middle",tnum=True)
    b+=card(812,96,160,112,18)+icon("flame",834,114,30,A())+T(834,186,"12 days",28,700,INK)
    return cv(b,"AI App Builder cover","A running app on a phone showing a 5.2 km morning run and a 72 percent daily goal ring.")
def webapp():
    H.set_hub("form"); b=card(380,40,580,320,22)
    b+=T(412,98,"Sprint 14",30,700,INK)+pill(928-int(tw("On track",28,600)+44),66,"On track",OK,OKB)
    rows=[("Design review","Done",OK,OKB),("API auth","Review",WARN,WARNB)]
    for i,(t,s,fg,bg) in enumerate(rows):
        y=128+i*84; b+=rect(412,y,516,70,14,"#F8FAFC",L.LINE)+T(440,y+45,t,28,600,INK)+pill(928-int(tw(s,28,600)+44)-14,y+12,s,fg,bg)
    b+=hero(556,294,392,70,18)+icon("user-plus",582,314,30,A())+T(628,341,"3 teammates joined",28,600,INK)
    return cv(b,"AI Web App Builder cover","A project web app showing Sprint 14 on track, with design review done and API auth in review.")
def saas():
    H.set_hub("cyan"); b=card(380,40,330,320,22)+T(412,98,"Pro plan",30,700,INK)+T(412,168,"$49",56,800,INK,ls=-1.2,tnum=True)+T(532,168,"/mo",28,500,MUTED)
    for i,t in enumerate(["Unlimited seats","Priority support"]):
        y=214+i*46; b+='<circle cx="426" cy="%d" r="12" fill="%s"/>'%(y-9,L.ACC_S)+icon("check",418,y-17,16,A(),3)+T(450,y,t,28,500,SUB)
    s,w=btn(412,282,"Upgrade",h=54); b+=s if False else ""
    b+=hero(700,110,264,180,22)+T(728,160,"MRR",28,600,MUTED)+T(728,224,"$18.4k",48,800,INK,ls=-1,tnum=True)+pill(728,238,"+9%",OK,OKB)
    return cv(b,"AI SaaS Builder cover","A SaaS pricing card for a 49 dollar Pro plan beside a revenue card showing 18.4k MRR, up 9 percent.")
def dashboard():
    H.set_hub("aab"); b=hero(380,36,580,328,22)
    b+=T(412,92,"Revenue",28,600,MUTED)+T(412,158,"$48.2k",52,800,INK,ls=-1,tnum=True)+pill(620,120,"+12%",OK,OKB)
    hs=[70,110,90,150,126,190]
    for i,h in enumerate(hs):
        x=412+i*84; b+=rect(x,338-h,56,h,10,"url(#gAcc)" if i==5 else L.ACC_M,None,1,None,None if i==5 else 0.9)
    pts=" ".join(f"{440+i*84},{318-h*0.9}" for i,h in enumerate(hs))
    b+=f'<polyline points="{pts}" fill="none" stroke="{L.ACC_D}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" stroke-opacity=".7"/>'
    b+=f'<circle cx="{440+5*84}" cy="{318-190*0.9}" r="8" fill="#fff" stroke="{L.ACC_D}" stroke-width="4"/>'
    return cv(b,"AI Dashboard Builder cover","A revenue dashboard showing 48.2k dollars, up 12 percent, with a rising bar and trend chart.")
def crm():
    H.set_hub("rose"); b=""
    for i,(t,x) in enumerate([("Lead",380),("Proposal",580),("Won",780)]):
        b+=rect(x,40,180,320,18,"#fff",L.LINE,1,None,0.55)+T(x+20,84,t,28,700,SUB)
    b+=card(392,108,156,86,14)+rect(412,132,70,14,7,L.HAIR)+rect(412,160,110,12,6,L.HAIR)
    b+=card(792,108,156,86,14)+'<circle cx="826" cy="150" r="16" fill="#DCFCE7"/>'+icon("check",817,141,18,OK,3)+rect(852,142,76,14,7,L.HAIR)
    b+=hero(540,150,300,196,22)+'<circle cx="590" cy="204" r="32" fill="url(#gAcc)"/>'+T(590,214,"AC",28,700,"#fff","middle")+T(634,214,"Acme Corp",30,700,INK)
    b+=T(572,284,"$24,000",46,800,INK,ls=-1,tnum=True)+pill(572,300,"Proposal",L.ACC_D,L.ACC_S)
    return cv(b,"AI CRM Builder cover","A CRM pipeline with the Acme Corp deal for 24,000 dollars moving through the proposal stage.")
def agent():
    H.set_hub("indigo"); b=hero(380,36,580,328,22)
    b+=rect(412,68,56,56,16,"url(#gAcc)")+icon("sparkles",424,80,32,"#fff")+T(488,108,"Lead research agent",30,700,INK)
    steps=[("Searched 3 sources",True),("Enriched 42 leads",True),("Drafting outreach",False)]
    for i,(t,done) in enumerate(steps):
        y=176+i*62
        if done: b+='<circle cx="428" cy="%d" r="16" fill="#DCFCE7"/>'%(y-10)+icon("check",419,y-19,18,OK,3)
        else: b+=f'<circle class="pulse" cx="428" cy="{y-10}" r="16" fill="{A()}" opacity=".35"/><circle cx="428" cy="{y-10}" r="10" fill="{A()}"/>'
        b+=T(460,y,t,28,600 if done else 700,SUB if done else INK)
    b+=pill(928-int(tw("Running",28,600)+44),176+2*62-40,"Running",L.ACC_D,L.ACC_S)
    return cv(b,"AI Agent Builder cover","An AI lead research agent run: 3 sources searched, 42 leads enriched, outreach being drafted.")
def schedule():
    H.set_hub("sqb"); b=card(380,36,580,328,22)
    b+=T(412,92,"Thursday, Oct 16",30,700,INK)
    for i,(tm,ev,hl) in enumerate([("9:30","Team standup",False),("1:30","Demo call",True)]):
        y=124+i*110
        if hl: b+=L.spot(400,y-10,540,110)
        b+=rect(412,y,516,92,16,"url(#gAcc)" if hl else "#F8FAFC",None if hl else L.LINE,1,"e2" if hl else None)
        c="#fff" if hl else INK; c2="#fff" if hl else MUTED
        b+=T(440,y+56,tm,30,800,c,tnum=True)+T(530,y+56,ev,30,700,c)
        if hl: b+=pill(768,y+23,"Booked",L.ACC_D,"#fff")
    return cv(b,"AI Schedule Builder cover","A booking calendar for Thursday, October 16 with a team standup at 9:30 and a demo call booked at 1:30.")
def chatbot():
    H.set_hub("teal"); b=card(380,36,580,328,22)
    b+=rect(380,36,580,70,22,L.ACC_S)+rect(380,84,580,22,0,L.ACC_S)+'<circle cx="420" cy="71" r="8" fill="#16A34A"/>'+T(440,82,"Support",28,700,INK)
    q="Where is my order?"; qw=int(tw(q,28,500)+48)
    b+=rect(928-qw,128,qw,62,20,"#F1F5F9")+T(928-qw+24,169,q,28,500,INK)
    a1="Arriving Thursday,"; a2="2 to 4 pm."; aw=int(max(tw(a1,28,600),tw(a2,28,600))+48)
    b+=L.spot(412,210,aw,112)+rect(412,210,aw,112,20,"url(#gAcc)",None,1,"e2")+T(436,254,a1,28,600,"#fff")+T(436,296,a2,28,600,"#fff")
    return cv(b,"AI Chatbot Builder cover","A support chatbot answering where is my order with: arriving Thursday, 2 to 4 pm.")
COVERS={"website":website,"app":app,"webapp":webapp,"saas":saas,"dashboard":dashboard,"crm":crm,"agent":agent,"schedule":schedule,"chatbot":chatbot}
