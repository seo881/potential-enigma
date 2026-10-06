"""Convert every <text> in an SVG into vector glyph outlines (Inter, shaped by HarfBuzz with kerning).
Each glyph is defined once in <defs> and reused with <use>, so files stay small. Output has zero font dependency."""
import re, xml.etree.ElementTree as ET
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
NS='http://www.w3.org/2000/svg'; ET.register_namespace('',NS); XL='http://www.w3.org/1999/xlink'
from paths import FONT_DIR as FD
WEIGHTS={400:'Regular',500:'Medium',600:'SemiBold',700:'Bold',800:'ExtraBold'}
_F={}
def fnt(w):
    w=min(WEIGHTS,key=lambda k:abs(k-int(w)))
    if w not in _F:
        p=FD+f'Inter-{WEIGHTS[w]}.ttf'; blob=hb.Blob.from_file_path(p); face=hb.Face(blob)
        tt=TTFont(p); _F[w]=(hb.Font(face),tt,tt.getGlyphSet(),tt['head'].unitsPerEm,tt.getGlyphOrder())
    return w,_F[w]
def convert(svg_text):
    root=ET.fromstring(svg_text); defs=root.find(f'{{{NS}}}defs'); used={}
    parent={c:p for p in root.iter() for c in p}
    for el in list(root.iter(f'{{{NS}}}text')):
        runs=[]  # (string, fill)
        if el.text: runs.append((el.text,el.get('fill','#000')))
        for sp in el.findall(f'{{{NS}}}tspan'):
            runs.append((sp.text or '',sp.get('fill',el.get('fill','#000'))))
        s=''.join(r[0] for r in runs)
        if not s.strip(): parent[el].remove(el); continue
        size=float(el.get('font-size',16)); w,(hf,tt,gs,upm,order)=fnt(el.get('font-weight','400'))
        ls=float(el.get('letter-spacing',0) or 0); op=el.get('opacity','1'); anchor=el.get('text-anchor','start')
        feats={"kern":True,"liga":True}
        if el.get("data-tnum"): feats["tnum"]=True
        buf=hb.Buffer(); buf.add_str(s); buf.guess_segment_properties(); hb.shape(hf,buf,feats)
        sc=size/upm; pen_x=0; glyphs=[]
        # map clusters back to run colors
        bounds=[]; pos=0
        for txt,fill in runs: bounds.append((pos,pos+len(txt),fill)); pos+=len(txt)
        for info,p in zip(buf.glyph_infos,buf.glyph_positions):
            ch=len(s[:info.cluster].encode('utf-16-le'))//2 if False else info.cluster
            fill=next((f for a,b,f in bounds if a<=ch<b),runs[0][1])
            gname=order[info.codepoint]
            glyphs.append((gname,pen_x+p.x_offset*sc,-p.y_offset*sc,fill))
            pen_x+=p.x_advance*sc+ls
        total=pen_x-ls if glyphs else 0
        x=float(el.get('x')); y=float(el.get('y'))
        x0=x-total/2 if anchor=='middle' else x-total if anchor=='end' else x
        g=ET.Element(f'{{{NS}}}g'); 
        if op!='1': g.set('opacity',op)
        for gname,gx,gy,fill in glyphs:
            key=f'g{w}_{re.sub(r"[^A-Za-z0-9]","_",gname)}'
            if key not in used:
                pen=SVGPathPen(gs); gs[gname].draw(pen); d=pen.getCommands()
                used[key]=d
            if not used[key]: continue   # spaces
            u=ET.SubElement(g,f'{{{NS}}}use'); u.set('href',f'#{key}'); u.set(f'{{{XL}}}href',f'#{key}')
            u.set('transform',f'translate({x0+gx:.2f} {y+gy:.2f}) scale({sc:.5f} {-sc:.5f})'); u.set('fill',fill)
        idx=list(parent[el]).index(el); parent[el].remove(el); parent[el].insert(idx,g)
    for key,d in used.items():
        if d:
            pe=ET.SubElement(defs,f'{{{NS}}}path'); pe.set('id',key); pe.set('d',d)
    root.attrib.pop('font-family',None)
    out=ET.tostring(root,encoding='unicode')
    if 'xmlns:xlink' not in out: out=out.replace('<svg ','<svg xmlns:xlink="http://www.w3.org/1999/xlink" ',1)
    return out
