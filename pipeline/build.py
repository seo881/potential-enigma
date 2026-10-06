"""Emergent build-hub image pipeline: one CLI for every image type.
Run from the repo root after `bash pipeline/bootstrap.sh`:
  python3 pipeline/build.py usecase <hub/slug>      # 4 use-case SVGs -> images/<hub>/<slug>/uc-1..4.svg + review sheet
  python3 pipeline/build.py cover   <hub/slug>      # card cover SVG  -> images/<hub>/<slug>/cover.svg + review at card size
  python3 pipeline/build.py og      <hub/slug>      # share image PNG -> images/<hub>/<slug>/og.png + review
  python3 pipeline/build.py all     <hub/slug>      # all three
  python3 pipeline/build.py check                   # rebuild everything in memory and compare byte-for-byte with the repo
  python3 pipeline/build.py verify  <sha> <hub/slug>          # raw.githubusercontent URLs at <sha> == local files
  python3 pipeline/build.py payload <sha> <hub/slug> [usecase,cover,og]   # JSON for Webflow update_collection_items
  python3 pipeline/build.py record  <hub/slug> <kind> <fileId> [<fileId>...]  # kind: usecase (4 ids in uc order) | cover | og
Every build step runs the gates and REFUSES to write a file that fails."""
import sys, os, re, io, json, hashlib, base64, subprocess, importlib, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _alias  # noqa: F401  (ds5/hubs5/covers5 names)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from paths import REVIEW
PAGES = json.load(open(os.path.join(REPO, 'pipeline', 'pages.json')))
UC_FIELDS = ["awb---key-feature-1-image", "acrm---key-feature-2-image", "acrm---key-feature-3-image", "acrm---key-feature-4-image"]
RAW = "https://raw.githubusercontent.com/seo881/potential-enigma/{sha}/{path}"

def page(key):
    if key not in PAGES: sys.exit(f"unknown page '{key}'. Add it to pipeline/pages.json first. Known: {', '.join(k for k in PAGES if not k.startswith('_'))}")
    return PAGES[key]
def fn(ref):
    mod, name = ref.split(':'); m = importlib.import_module(mod)
    if mod == 'covers5': return m.COVERS[name]
    return getattr(m, name)
def gates_usecase(svg):
    import qa3
    issues = qa3.run(svg)
    W = float(re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).group(1)); H = float(re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).group(2))
    if abs(W / H - 1.5) > 1e-6: issues.append(f"SHAPE {W}x{H} is not 3:2 (.build-usecase_image is aspect-ratio 3/2, object-fit fill)")
    small = [s for s in map(float, re.findall(r'font-size="([\d.]+)"', svg)) if s * 830 / W < 11]
    if small: issues.append(f"LEGIBILITY {len(small)} text(s) under 11px at the 830px desktop slot (min {min(small)} design px; need >=16)")
    return issues
def gates_cover(svg):
    import qa3
    issues = [i for i in qa3.run(svg) if not i.startswith('off-canvas')]   # qa3's off-canvas bounds are hard-coded to 1200x800
    if 'viewBox="0 0 800 500"' not in svg: issues.append("SHAPE cover must be 800x500 (16:10, .build_cover aspect-ratio 16/10)")
    small = [s for s in map(float, re.findall(r'font-size="([\d.]+)"', svg)) if s * 360 / 800 < 11]
    if small: issues.append(f"LEGIBILITY {len(small)} text(s) under 11px at the ~360px card (need >=26 design px)")
    return issues
def render(svg_path, width, out):
    import raster; raster.to_png(svg_path, out, width)
def sheet(pngs, cols, tile, out, gap=20):
    from PIL import Image
    ims = [Image.open(p).convert('RGB').resize(tile, Image.LANCZOS) for p in pngs]
    rows = (len(ims) + cols - 1) // cols
    s = Image.new('RGB', (cols * tile[0] + (cols - 1) * gap, rows * tile[1] + (rows - 1) * gap), 'white')
    for i, im in enumerate(ims): s.paste(im, ((i % cols) * (tile[0] + gap), (i // cols) * (tile[1] + gap)))
    s.save(out); return out

def build_usecase(key, write=True):
    import outline
    p = page(key); d = os.path.join(REPO, 'images', key); os.makedirs(d, exist_ok=True); outs = []
    for i, ref in enumerate(p['scenes'], 1):
        src = fn(ref)(); iss = gates_usecase(src)
        if iss: sys.exit(f"GATE FAIL {key} uc-{i} ({ref}): {iss}")
        v = outline.convert(src); assert '<text' not in v and 'font-family' not in v
        outs.append((os.path.join(d, f'uc-{i}.svg'), v))
    if write:
        os.makedirs(REVIEW, exist_ok=True); pngs = []
        for path, v in outs:
            open(path, 'w').write(v); png = os.path.join(REVIEW, key.replace('/', '_') + '_' + os.path.basename(path) + '.png')
            render(path, 830, png); pngs.append(png)
        print("wrote 4 use-case SVGs; review sheet (true desktop size):", sheet(pngs, 2, (830, 553), os.path.join(REVIEW, key.replace('/', '_') + '_usecase.png')))
    return outs
def build_cover(key, write=True):
    import outline
    p = page(key); src = fn(p['cover'])(); iss = gates_cover(src)
    if iss: sys.exit(f"GATE FAIL {key} cover: {iss}")
    v = outline.convert(src); path = os.path.join(REPO, 'images', key, 'cover.svg')
    if write:
        os.makedirs(os.path.dirname(path), exist_ok=True); open(path, 'w').write(v); os.makedirs(REVIEW, exist_ok=True)
        from PIL import Image
        png = os.path.join(REVIEW, key.replace('/', '_') + '_cover.png'); render(path, 720, png)
        card = Image.new('RGB', (392, 300), '#F7F7F9'); card.paste(Image.new('RGB', (376, 290), 'white'), (8, 5))
        card.paste(Image.open(png).convert('RGB').resize((360, 225), Image.LANCZOS), (16, 13))
        out = os.path.join(REVIEW, key.replace('/', '_') + '_cover_in_card.png'); card.save(out); print("wrote cover.svg; review at card size:", out)
    return [(path, v)]
def build_og(key, write=True):
    import ds5 as L, hubs5 as H, outline
    from qa import width as tw
    from PIL import Image
    p = page(key); hub = p['hub']
    src = fn(p['cover'])()
    for pat in [r'<rect width="800" height="500" fill="url\(#bg\)"/>', r'<rect width="800" height="500" fill="url\(#glowA\)"/>',
                r'<rect width="800" height="500" fill="url\(#glowB\)"/>', r'<rect width="800" height="500" fill="url\(#grid\)" mask="url\(#gridMask\)"/>']:
        src = re.sub(pat, '', src)                                   # the card sits on the share image's own background
    cov = base64.b64encode(outline.convert(src).encode()).decode()
    H.set_hub(hub); size = 50
    lines = p.get('og_lines')
    if not lines:
        lines = [""]
        for w in p['og_headline'].split():
            cand = (lines[-1] + " " + w).strip()
            if tw(cand, size, 800, -1.2) <= 480: lines[-1] = cand
            else: lines.append(w)
    for l in lines:
        if tw(l, size, 800, -1.2) > 480: sys.exit(f"GATE FAIL og headline line too wide (>480px column): {l!r}")
    if len(lines) > 3: sys.exit("GATE FAIL og headline needs more than 3 lines; shorten it or set og_lines")
    if len(lines) > 1 and len(lines[-1].split()) == 1: print(f"WARNING orphan last line {lines[-1]!r}: set og_lines in pages.json to balance")
    y0 = 315 - (len(lines) * 62 + 70) / 2 + 40
    b = L.T(72, y0 - 18, "emergent", 30, 800, L.ACC_D, ls=-0.5)
    for i, l in enumerate(lines): b += L.T(72, y0 + 44 + i * 62, l, size, 800, L.INK, ls=-1.2)
    b += L.T(72, y0 + 44 + len(lines) * 62 + 10, "From a prompt to a working app. Free to start.", 22, 500, L.SUB)
    b += f'<image x="590" y="130" width="590" height="369" href="data:image/svg+xml;base64,{cov}"/>'
    L.W, L.H = 1200, 630; s = L.canvas(b, title="", desc=""); L.W, L.H = 1200, 800
    v = outline.convert(s); path = os.path.join(REPO, 'images', key, 'og.png')
    import tempfile; tmp_svg = os.path.join(tempfile.gettempdir(), '_og.svg'); open(tmp_svg, 'w').write(v); tmp_png = os.path.join(tempfile.gettempdir(), '_og.png')
    import raster; raster.to_png(tmp_svg, tmp_png, 1200, 630)
    buf = io.BytesIO(); Image.open(tmp_png).convert('RGB').save(buf, 'PNG', optimize=True); data = buf.getvalue()
    if write:
        open(path, 'wb').write(data); os.makedirs(REVIEW, exist_ok=True)
        out = os.path.join(REVIEW, key.replace('/', '_') + '_og.png'); open(out, 'wb').write(data); print("wrote og.png (1200x630); review:", out)
    return [(path, data)]

def check():
    bad = 0; n = 0
    for key in [k for k in PAGES if not k.startswith('_')]:
        for builder in (build_usecase, build_cover, build_og):
            for path, content in builder(key, write=False):
                n += 1; cur = open(path, 'rb').read(); new = content if isinstance(content, bytes) else content.encode()
                same = cur == new; bad += not same
                print(("IDENTICAL " if same else "DIFFERS   ") + os.path.relpath(path, REPO))
    print(f"{n - bad}/{n} identical"); sys.exit(1 if bad else 0)
def files_for(key, kinds):
    d = os.path.join('images', key); out = []
    if 'usecase' in kinds: out += [os.path.join(d, f'uc-{i}.svg') for i in range(1, 5)]
    if 'cover' in kinds: out.append(os.path.join(d, 'cover.svg'))
    if 'og' in kinds: out.append(os.path.join(d, 'og.png'))
    return out
def verify(sha, key, kinds=('usecase', 'cover', 'og')):
    ok = 0; fs = files_for(key, kinds)
    for f in fs:
        remote = urllib.request.urlopen(RAW.format(sha=sha, path=f), timeout=30).read()
        same = hashlib.sha256(remote).digest() == hashlib.sha256(open(os.path.join(REPO, f), 'rb').read()).digest()
        ok += same; print(("OK   " if same else "DIFF ") + f)
    print(f"{ok}/{len(fs)} served byte-identical at {sha[:7]}"); sys.exit(0 if ok == len(fs) else 1)
def payload(sha, key, kinds):
    p = page(key); fd = {}
    if 'usecase' in kinds:
        for i in range(1, 5):
            f = os.path.join('images', key, f'uc-{i}.svg'); desc = re.search(r'<desc>(.*?)</desc>', open(os.path.join(REPO, f)).read(), re.S)
            alt = (desc.group(1) if desc else '').replace('&amp;', '&').strip()
            if not alt: sys.exit(f"{f} has no <desc>; alt text comes from it")
            fd[UC_FIELDS[i - 1]] = {"url": RAW.format(sha=sha, path=f), "alt": alt}
    if 'cover' in kinds: fd[p['cover_field']] = {"url": RAW.format(sha=sha, path=os.path.join('images', key, 'cover.svg')), "alt": p['cover_alt']}
    if 'og' in kinds: fd["thumbnail-image"] = {"url": RAW.format(sha=sha, path=os.path.join('images', key, 'og.png')), "alt": p['og_alt']}
    print(json.dumps({"label": key.replace('/', '_'), "update_collection_items": {"collection_id": p['collection_id'],
          "request": {"items": [{"id": p['item_id'], "isDraft": True, "fieldData": fd}]}}}, indent=1))
    print("\n# NOTE: isDraft true keeps the item a draft. Set false only when Divit approves going live.", file=sys.stderr)
def record(key, kind, ids):
    p = page(key)
    if kind == 'usecase':
        assert len(ids) == 4, "give the 4 fileIds in uc-1..uc-4 order"
        man = json.load(open(os.path.join(REPO, 'manifest.json'))); n = 0
        for m in man:
            if m.get('item_id') == p['item_id'] and m['path'].endswith('.svg') and '/uc-' in m['path']:
                k = int(m['path'].split('uc-')[1][0]) - 1; m['webflow_file_id'] = ids[k]; m['status'] = 'live'; n += 1
        if n == 0:   # new page: create the 4 entries
            for i in range(1, 5):
                f = os.path.join('images', key, f'uc-{i}.svg')
                man.append({"image": f"uc-{p['hub']}-{i}", "hub": p['hub'], "path": f, "item_id": p['item_id'], "collection_id": p['collection_id'],
                            "field": UC_FIELDS[i - 1], "webflow_file_id": ids[i - 1], "status": "live", "design_system": "v5"}); n += 1
        json.dump(man, open(os.path.join(REPO, 'manifest.json'), 'w'), indent=1); print(f"manifest: {n} entries updated")
    else:
        a = os.path.join(REPO, 'assets.json'); data = json.load(open(a)) if os.path.exists(a) else {}
        data.setdefault(key, {})[kind] = ids[0]; json.dump(data, open(a, 'w'), indent=1); print(f"assets.json: {key} {kind} = {ids[0]}")

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    cmd = a[0]
    if cmd == 'usecase': build_usecase(a[1])
    elif cmd == 'cover': build_cover(a[1])
    elif cmd == 'og': build_og(a[1])
    elif cmd == 'all': build_usecase(a[1]); build_cover(a[1]); build_og(a[1])
    elif cmd == 'check': check()
    elif cmd == 'verify': verify(a[1], a[2])
    elif cmd == 'payload': payload(a[1], a[2], a[3].split(',') if len(a) > 3 else ['usecase', 'cover', 'og'])
    elif cmd == 'record': record(a[1], a[2], a[3:])
    else: sys.exit(__doc__)
