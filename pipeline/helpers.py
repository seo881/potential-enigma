W,H=1200,1000
FONT="Inter, 'SF Pro Display', 'Segoe UI', Helvetica, Arial, sans-serif"
def defs(g1,g2):
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/></linearGradient>
<radialGradient id="glow" cx="0.75" cy="0.2" r="0.7"><stop offset="0" stop-color="#ffffff" stop-opacity="0.75"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#0b1b3f" flood-opacity="0.16"/></filter>
<filter id="sh2" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0b1b3f" flood-opacity="0.14"/></filter>
<linearGradient id="flow" gradientUnits="userSpaceOnUse" x1="450" y1="0" x2="700" y2="0"><stop offset="0" stop-color="#3b82f6"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient>
</defs>'''
def svg(body,g1="#eaf2ff",g2="#c7dbff"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">{defs(g1,g2)}<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#glow)"/>{grid()}{body}</svg>'
def grid():
    s=''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="#0b1b3f" opacity="0.06"/>' for x in range(40,W,48) for y in range(40,H,48))
    return s
def card(x,y,w,h,r=28,fill="#fff",f="sh",stroke="#e6ebf5"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" filter="url(#{f})"/>'
def t(x,y,s,size=28,w=500,fill="#0a0a0a",anchor="start",op=1,ls=0):
    s=s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" opacity="{op}" letter-spacing="{ls}">{s}</text>'
def pill(x,y,w,h,fill,label,tc="#fff",size=22,dot=None):
    if dot:
        d=f'<circle cx="{x+26}" cy="{y+h/2}" r="6" fill="{dot}"/>'
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}"/>{d}'+t(x+44,y+h/2+size*0.36,label,size,600,tc,"start")
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}"/>'+t(x+w/2,y+h/2+size*0.36,label,size,600,tc,"middle")
def field(x,y,w,label,val,h=62):
    return t(x,y-12,label,18,600,"#6b7280")+f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#f6f8fc" stroke="#e3e8f2"/>'+t(x+20,y+h/2+8,val,22,500,"#111827")
def dots(x,y):
    return ''.join(f'<circle cx="{x+i*22}" cy="{y}" r="7" fill="{c}"/>' for i,c in enumerate(["#ff5f57","#febc2e","#28c840"]))

