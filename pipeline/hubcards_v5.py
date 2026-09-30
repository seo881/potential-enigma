"""Hub-card covers for the 'More things you can build' component. 1000x400 (5:2), no text, v5 language.
One calm left zone (the icon tile overlaps bottom-left), one bold motif on the right, depth via e1/e2-style shadows."""
W, H = 1000, 400
PAL = {  # bg1, bg2, glow, deep (strokes/shadows), accent (highlights)
 "website":  ("#EEF3FF", "#C9DAFF", "#DCE6FF", "#1E3A8A", "#2563EB"),
 "app":      ("#FFF8DC", "#F8DE7E", "#FFEFA8", "#78350F", "#D97706"),
 "webapp":   ("#EAFBEF", "#B4EFC6", "#D2F7DD", "#14532D", "#16A34A"),
 "saas":     ("#E8FAFD", "#AEE8F4", "#D3F4FA", "#164E63", "#0891B2"),
 "dashboard":("#F5EEFF", "#D9C2FB", "#EADBFF", "#4C1D95", "#7C3AED"),
 "crm":      ("#FFF0F0", "#F6BCBC", "#FCDADA", "#7F1D1D", "#DC2626"),
 "agent":    ("#EFEFFF", "#C4C1FF", "#DEDCFF", "#312E81", "#4F46E5"),
 "schedule": ("#FFF3EA", "#FFCBA4", "#FFE2CC", "#7C2D12", "#EA580C"),
 "chatbot":  ("#E9FBF6", "#A9EAD8", "#CFF5EA", "#134E4A", "#0D9488"),
}
def defs(k):
    b1,b2,gl,deep,acc = PAL[k]
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{b1}"/><stop offset="1" stop-color="{b2}"/></linearGradient>
<radialGradient id="glA" cx=".78" cy=".2" r=".6"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".85"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
<radialGradient id="glB" cx=".15" cy="1" r=".6"><stop offset="0" stop-color="{gl}" stop-opacity=".9"/><stop offset="1" stop-color="{gl}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{deep}" stroke-opacity=".07" stroke-width="1"/></pattern>
<radialGradient id="gm" cx=".72" cy=".45" r=".55"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="fade"><rect width="{W}" height="{H}" fill="url(#gm)"/></mask>
<filter id="e1" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="{deep}" flood-opacity=".10"/><feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="{deep}" flood-opacity=".16"/></filter>
<filter id="e2" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="{deep}" flood-opacity=".12"/><feDropShadow dx="0" dy="24" stdDeviation="26" flood-color="{deep}" flood-opacity=".24"/></filter>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{acc}"/><stop offset="1" stop-color="{deep}"/></linearGradient>
</defs>'''
def bg():
    return (f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#glA)"/>'
            f'<rect width="{W}" height="{H}" fill="url(#glB)"/><rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#fade)"/>')
R = lambda x,y,w,h,r=14,f="#fff",o=1,extra="": f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}" fill-opacity="{o}" {extra}/>'
def M(k):
    b1,b2,gl,deep,acc = PAL[k]; s=""
    line = lambda x,y,w,o=.16,h=10: R(x,y,w,h,5,deep,o)
    if k=="website":   # browser window with hero + cards
        s+=f'<g filter="url(#e2)">{R(470,70,470,300,18)}</g>{R(470,70,470,44,18,"#F8FAFC")}{R(470,96,470,18,0,"#F8FAFC")}'
        s+="".join(f'<circle cx="{500+i*20}" cy="92" r="6" fill="{deep}" fill-opacity=".18"/>' for i in range(3))
        s+=R(570,82,270,20,10,deep,.07)+R(498,136,414,96,12,"url(#acc)",.9)+line(522,160,180,.9*0+.5,14).replace(deep,"#fff")+line(522,186,120,.35).replace(deep,"#fff")
        s+="".join(R(498+i*142,248,130,96,12,deep,.06) for i in range(3))
    elif k=="app":     # phone with app grid, gently tilted, fully inside the canvas
        s+=f'<g transform="rotate(-6 700 205)"><g filter="url(#e2)">{R(605,52,190,306,32,"#111827")}</g>{R(616,63,168,284,24)}'
        s+=R(662,74,76,12,6,"#111827")
        cols=["url(#acc)",acc,deep,acc]
        s+="".join(R(638+(i%3)*50,104+(i//3)*52,36,36,10,cols[i%4],.18+.2*((i*7)%3)) for i in range(12))
        s+=R(638,318,124,14,7,deep,.12)+'</g>'
    elif k=="webapp":  # globe + floating app panel
        cx,cy,r=760,210,150
        s+=f'<g filter="url(#e1)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" fill-opacity=".9"/></g>'
        s+=f'<g fill="none" stroke="{deep}" stroke-opacity=".22" stroke-width="3"><circle cx="{cx}" cy="{cy}" r="{r}"/>'
        s+="".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{r}"/>' for rx in (40,95))
        s+="".join(f'<path d="M{cx-r+8} {cy+dy} H{cx+r-8}"/>' for dy in (-75,0,75))+'</g>'
        s+=f'<g filter="url(#e2)">{R(520,230,230,120,16)}</g>'+R(540,252,40,40,10,"url(#acc)")+line(596,258,120,.25,12)+line(596,280,80,.12,10)+line(540,310,190,.08,14)
    elif k=="saas":    # stacked layers + cloud
        for i,(y,o) in enumerate(((250,.55),(205,.75),(160,1))):
            s+=f'<g filter="url(#e1)">{R(540+i*20,y,360-i*40,110,18,"#fff",o)}</g>'
        s+=R(596,184,56,56,14,"url(#acc)")+line(670,192,160,.22,14)+line(670,220,110,.12,10)
        s+=f'<g filter="url(#e2)"><path d="M790 120a52 52 0 0 1 100 10a40 40 0 0 1-4 80H760a44 44 0 0 1 30-90z" fill="#fff"/></g>'
    elif k=="dashboard": # bars + line chart card
        s+=f'<g filter="url(#e2)">{R(500,60,440,300,20)}</g>'+line(528,88,140,.2,14)+line(528,112,90,.1,10)
        hs=[90,140,110,190,160,220]
        s+="".join(R(540+i*62,330-h,38,h,8,"url(#acc)" if i==5 else acc,1 if i==5 else .25) for i,h in enumerate(hs))
        pts=" ".join(f"{559+i*62},{300-h*.55}" for i,h in enumerate(hs))
        s+=f'<polyline points="{pts}" fill="none" stroke="{deep}" stroke-opacity=".55" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    elif k=="crm":     # kanban columns with deal cards
        for c in range(3):
            x=500+c*150; s+=R(x,60,134,300,16,"#fff",.45)+line(x+14,78,70,.22,10)
            for j in range(3-c%2):
                y=104+j*84; s+=f'<g filter="url(#e1)">{R(x+10,y,114,70,12)}</g>'+f'<circle cx="{x+32}" cy="{y+24}" r="10" fill="url(#acc)" fill-opacity="{.9 if j==0 else .35}"/>'+line(x+50,y+18,60,.2,9)+line(x+22,y+46,86,.1,9)
    elif k=="agent":   # hub node connected to tool nodes
        cx,cy=740,200; nodes=[(565,120),(600,295),(895,112),(915,288),(770,330),(725,76)]
        s+=f'<g stroke="{deep}" stroke-opacity=".25" stroke-width="3" stroke-dasharray="6 8" fill="none">'+"".join(f'<path d="M{cx} {cy} L{x} {y}"/>' for x,y in nodes)+'</g>'
        s+="".join(f'<g filter="url(#e1)">{R(x-34,y-34,68,68,18)}</g>'+R(x-14,y-14,28,28,8,acc,.35) for x,y in nodes)
        s+=f'<g filter="url(#e2)"><circle cx="{cx}" cy="{cy}" r="62" fill="url(#acc)"/></g>'
        s+=f'<path d="M{cx} {cy-30} l8 22 22 8 -22 8 -8 22 -8 -22 -22 -8 22 -8z" fill="#fff"/>'
    elif k=="schedule": # calendar grid with booked slot
        s+=f'<g filter="url(#e2)">{R(500,50,440,320,20)}</g>'+R(500,50,440,64,20,"url(#acc)")+R(500,94,440,20,0,"url(#acc)")
        s+=line(528,74,120,.9,14).replace(deep,"#fff")
        for r_ in range(4):
            for c in range(7):
                x=524+c*58; y=132+r_*56; hi=(r_,c)==(1,4)
                s+=R(x,y,46,44,10,"url(#acc)" if hi else deep,1 if hi else .06)
        s+=f'<g filter="url(#e1)">{R(760,300,200,70,14)}</g>'+f'<circle cx="790" cy="335" r="12" fill="url(#acc)"/>'+line(812,324,120,.22,11)+line(812,344,80,.12,9)
    elif k=="chatbot":  # chat bubbles
        s+=f'<g filter="url(#e1)">{R(520,70,300,84,22)}</g>'+line(548,98,220,.18,12)+line(548,122,150,.1,10)
        s+=f'<g filter="url(#e2)">{R(640,176,300,90,22,"url(#acc)")}</g>'+line(668,204,230,.9,12).replace(deep,"#fff")+line(668,228,160,.55,10).replace(deep,"#fff")
        s+=f'<g filter="url(#e1)">{R(520,290,190,64,22)}</g>'+"".join(f'<circle cx="{560+i*28}" cy="322" r="8" fill="{deep}" fill-opacity="{.2+.15*i}"/>' for i in range(3))
    return s
def cover(k, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">'
            f'<title>{title}</title>{defs(k)}{bg()}{M(k)}</svg>')
NAMES={"website":"AI Website Builder","app":"AI App Builder","webapp":"AI Web App Builder","saas":"AI SaaS Builder",
 "dashboard":"AI Dashboard Builder","crm":"AI CRM Builder","agent":"AI Agent Builder","schedule":"AI Schedule Builder","chatbot":"AI Chatbot Builder"}
