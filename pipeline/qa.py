"""Automated QA: measure every <text> with real Inter metrics, flag overlaps and off-canvas text."""
import re, xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from paths import FONT_DIR as FD
_F={}
def font(w):
    w=int(w); name={400:'Regular',500:'Medium',600:'SemiBold',700:'Bold',800:'ExtraBold'}.get(min([400,500,600,700,800],key=lambda k:abs(k-w)))
    if name not in _F:
        f=TTFont(FD+f'Inter-{name}.ttf'); _F[name]=(f.getBestCmap(),f['hmtx'],f['head'].unitsPerEm)
    return _F[name]
def width(s,size,w,ls=0):
    cmap,hmtx,upm=font(w)
    return sum(hmtx[cmap.get(ord(c),cmap.get(32))][0] for c in s)*size/upm + ls*max(len(s)-1,0)
NS='{http://www.w3.org/2000/svg}'
def boxes(svg_text):
    root=ET.fromstring(svg_text); W=float(root.get('width')); H=float(root.get('height')); out=[]
    for el in root.iter(NS+'text'):
        s=''.join(el.itertext())
        if not s.strip(): continue
        size=float(el.get('font-size',16)); w=el.get('font-weight','400'); ls=float(el.get('letter-spacing',0) or 0)
        x=float(el.get('x')); y=float(el.get('y')); tw=width(s,size,w,ls); a=el.get('text-anchor','start')
        x0=x-tw/2 if a=='middle' else x-tw if a=='end' else x
        out.append(dict(s=s,x0=x0,x1=x0+tw,y0=y-size*0.74,y1=y+size*0.2))
    return out,W,H
def check(svg_text,pad=2):
    bx,W,H=boxes(svg_text); issues=[]
    for b in bx:
        if b['x0']<0 or b['x1']>W or b['y0']<0 or b['y1']>H: issues.append(f"off-canvas: '{b['s'][:40]}'")
    for i in range(len(bx)):
        for j in range(i+1,len(bx)):
            a,b=bx[i],bx[j]
            ox=min(a['x1'],b['x1'])-max(a['x0'],b['x0']); oy=min(a['y1'],b['y1'])-max(a['y0'],b['y0'])
            if ox>pad and oy>pad: issues.append(f"overlap: '{a['s'][:32]}' × '{b['s'][:32]}'")
    return issues

def rects(svg_text):
    root=ET.fromstring(svg_text); out=[]
    for el in root.iter(NS+'rect'):
        try:
            x=float(el.get('x',0)); y=float(el.get('y',0)); w=float(el.get('width')); h=float(el.get('height'))
        except (TypeError,ValueError): continue
        out.append((x,y,x+w,y+h))
    return out
def check_all(svg_text,pad=3):
    issues=check(svg_text,pad); bx,_,_=boxes(svg_text)
    for b in bx:
        for (x0,y0,x1,y1) in rects(svg_text):
            ox=min(b['x1'],x1)-max(b['x0'],x0); oy=min(b['y1'],y1)-max(b['y0'],y0)
            if ox<=pad or oy<=pad: continue                      # no real contact
            inside=b['x0']>=x0-pad and b['x1']<=x1+pad and b['y0']>=y0-pad and b['y1']<=y1+pad
            if not inside: issues.append(f"text crosses a shape edge: '{b['s'][:40]}' (by {ox:.0f}px)")
    return sorted(set(issues))

def rects_f(svg_text):
    root=ET.fromstring(svg_text); out=[]
    for el in root.iter(NS+'rect'):
        try: x=float(el.get('x',0)); y=float(el.get('y',0)); w=float(el.get('width')); h=float(el.get('height'))
        except (TypeError,ValueError): continue
        out.append(((x,y,x+w,y+h),(el.get('fill') or '').lower()))
    return out
def _touch(a,b): return min(a[2],b[2])>=max(a[0],b[0]) and min(a[3],b[3])>=max(a[1],b[1])
def check_v2(svg_text,pad=3):
    """Text must not partly cross a visual shape. Touching same-fill rects count as ONE shape."""
    issues=check(svg_text,pad); bx,_,_=boxes(svg_text); R=rects_f(svg_text)
    for b in bx:
        for (r,fill) in R:
            ox=min(b['x1'],r[2])-max(b['x0'],r[0]); oy=min(b['y1'],r[3])-max(b['y0'],r[1])
            if ox<=pad or oy<=pad: continue
            # visual shape = r merged with every touching rect of the same fill
            grp=[q for (q,f) in R if f==fill and fill not in('','none') and _touch(q,r)] or [r]
            ux0=min(q[0] for q in grp); uy0=min(q[1] for q in grp); ux1=max(q[2] for q in grp); uy1=max(q[3] for q in grp)
            if b['x0']>=ux0-pad and b['x1']<=ux1+pad and b['y0']>=uy0-pad and b['y1']<=uy1+pad: continue
            issues.append(f"text crosses a shape edge: '{b['s'][:40]}' (by {ox:.0f}px)")
    return sorted(set(issues))
