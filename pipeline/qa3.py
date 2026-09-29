"""QA v3: occlusion-aware layout + WCAG contrast. Works on the pre-outline SVG (real <text>)."""
import re, xml.etree.ElementTree as ET
from qa import width
NS='{http://www.w3.org/2000/svg}'
def _hex(c):
    c=(c or '').strip()
    if not c.startswith('#') or len(c) not in (4,7): return None
    if len(c)==4: c='#'+''.join(ch*2 for ch in c[1:])
    return tuple(int(c[i:i+2],16)/255 for i in (1,3,5))
def _lum(rgb):
    f=lambda v: v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    r,g,b=map(f,rgb); return 0.2126*r+0.7152*g+0.0722*b
def contrast(a,b):
    la,lb=_lum(a),_lum(b); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)
def run(svg, grad_fallback="#7C3AED", page_bg="#F6F3FF"):
    root=ET.fromstring(svg); order=[]; parent={c:p for p in root.iter() for c in p}
    def in_defs(el):
        while el in parent:
            el=parent[el]
            if el.tag==NS+'defs' or el.tag==NS+'pattern' or el.tag==NS+'mask': return True
        return False
    grads={}
    for gtag in ('linearGradient','radialGradient'):
        for g in root.iter(NS+gtag):
            stops=[_hex(s.get('stop-color')) for s in g.iter(NS+'stop') if _hex(s.get('stop-color'))]
            if stops: grads[g.get('id')]=max(stops,key=_lum)
    def solid(fill):
        if not fill: return None
        m=re.match(r'url\(#([^)]+)\)',fill)
        if m: return grads.get(m.group(1))
        return _hex(fill)
    for el in root.iter():
        if in_defs(el): continue
        if el.tag==NS+'circle':
            try: cx=float(el.get('cx')); cy=float(el.get('cy')); r=float(el.get('r'))
            except: continue
            if el.get('fill') in (None,'none'): continue
            order.append(('r',(cx-r,cy-r,cx+r,cy+r),el.get('fill'),float(el.get('opacity',1))))
            continue
        if el.tag==NS+'rect':
            try: x=float(el.get('x',0)); y=float(el.get('y',0)); w=float(el.get('width')); h=float(el.get('height'))
            except: continue
            if w>=1150 and h>=780: continue          # full-canvas background layers
            fill=el.get('fill'); op=float(el.get('opacity',1))
            order.append(('r',(x,y,x+w,y+h),fill,op))
        elif el.tag==NS+'text':
            s=''.join(el.itertext())
            if not s.strip(): continue
            size=float(el.get('font-size')); wt=el.get('font-weight','400'); ls=float(el.get('letter-spacing',0) or 0)
            tw=width(s,size,wt,ls); x=float(el.get('x')); y=float(el.get('y')); a=el.get('text-anchor','start')
            x0=x-tw/2 if a=='middle' else x-tw if a=='end' else x
            order.append(('t',(x0,y-size*0.74,x0+tw,y+size*0.2),el.get('fill'),s,size,int(wt)))
    issues=[]; texts=[(i,o) for i,o in enumerate(order) if o[0]=='t']
    def inside(b,r,p=3): return b[0]>=r[0]-p and b[2]<=r[2]+p and b[1]>=r[1]-p and b[3]<=r[3]+p
    def touch(b,r,p=3): return min(b[2],r[2])-max(b[0],r[0])>p and min(b[3],r[3])-max(b[1],r[1])>p
    for i,(_,bx,fill,s,size,wt) in texts:
        if bx[0]<0 or bx[2]>1200 or bx[1]<0 or bx[3]>800: issues.append(f"off-canvas: {s[:30]}")
        prior=[(k,o) for k,o in enumerate(order[:i]) if o[0]=='r']
        conts=[(k,o) for k,o in prior if inside(bx,o[1])]
        top=conts[-1][0] if conts else -1
        for k,o in prior:
            if k<=top and conts: continue                       # hidden under the container the text sits in
            if touch(bx,o[1]) and not inside(bx,o[1]):
                # same-fill merged shapes (header strips) count as one
                grp=[p for _,p in prior if p[2]==o[2] and o[2] not in (None,'none') and min(p[1][2],o[1][2])>=max(p[1][0],o[1][0]) and min(p[1][3],o[1][3])>=max(p[1][1],o[1][1])]
                u=(min(g[1][0] for g in grp),min(g[1][1] for g in grp),max(g[1][2] for g in grp),max(g[1][3] for g in grp)) if grp else o[1]
                if not inside(bx,u): issues.append(f"crosses shape: {s[:30]}")
        for j,(_,bx2,_,s2,_,_) in texts:
            if j>i and touch(bx,bx2,2): issues.append(f"overlap: {s[:20]} × {s2[:20]}")
        # contrast against the topmost solid container
        fg=_hex(fill); bgc=None
        for k,o in reversed(conts):
            if o[3]<0.5: continue
            bgc=solid(o[2])
            if bgc: break
        bgc=bgc or _hex(page_bg)
        if fg:
            need=3.0 if (size>=24 or (size>=18.66 and wt>=700)) else 4.5
            cr=contrast(fg,bgc)
            if cr<need: issues.append(f"contrast {cr:.2f}<{need}: {s[:30]}")
    return sorted(set(issues))
