import sys,io,os,re; sys.path.insert(0,'/home/claude/pipe')
import scenes32, cairosvg
from qa import check_v2
from PIL import Image
SLOT_RATIO=3/2      # read from Webflow: .build-usecase_image { aspect-ratio: 3/2 }
SLOT_CSS_W=830      # typical desktop display width of the slot
MIN_PX=11
os.makedirs('r32',exist_ok=True); fails={}
assert len(scenes32.SCENES)==16
for name,fn in scenes32.SCENES.items():
    s=fn(); issues=check_v2(s)
    W=float(re.search(r'width="([\d.]+)"',s).group(1)); H=float(re.search(r'height="([\d.]+)"',s).group(1))
    if abs(W/H-SLOT_RATIO)>1e-6: issues.append(f"SHAPE {W/H:.3f} != slot {SLOT_RATIO:.3f}")
    small=[float(x) for x in re.findall(r'font-size="([\d.]+)"',s) if float(x)*SLOT_CSS_W/W<MIN_PX]
    if small: issues.append(f"LEGIBILITY {len(small)} text(s) under {MIN_PX}px on screen")
    if issues: fails[name]=issues; continue
    im=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(),output_width=3000))).convert('RGB')
    assert im.size==(3000,2000)
    im.save(f'r32/{name}.webp','WEBP',lossless=True,method=6); open(f'r32/{name}.svg','w').write(s)
    im.resize((1660,1107),Image.LANCZOS).save(f'r32/{name}.disp.png')   # true on-screen size, retina desktop
print("FAILED:",fails if fails else "none", "| passed:",16-len(fails))
