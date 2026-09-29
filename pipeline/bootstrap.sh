#!/usr/bin/env bash
# Rebuilds the image-pipeline environment in a fresh Claude sandbox. Run from the repo root:  bash pipeline/bootstrap.sh
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
pip install cairosvg uharfbuzz fonttools pillow --break-system-packages -q
which rsvg-convert >/dev/null 2>&1 || (apt-get install -y -q librsvg2-bin >/dev/null 2>&1 || (apt-get update -q >/dev/null 2>&1 && apt-get install -y -q librsvg2-bin >/dev/null 2>&1))
# Inter 4.1 static TTFs (the pipeline expects /root/.fonts/Inter-<Weight>.ttf)
mkdir -p /root/.fonts
if [ ! -f /root/.fonts/Inter-ExtraBold.ttf ]; then
  cd /tmp && curl -sSL -o inter.zip https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip && rm -rf inter && unzip -o -q inter.zip -d inter
  for w in Regular Medium SemiBold Bold ExtraBold; do cp "$(find /tmp/inter -name "Inter-$w.ttf" | head -1)" /root/.fonts/; done
fi
# Lucide icons (ISC) at the path the scene library expects
if [ ! -d /home/claude/lucide/package/icons ]; then
  mkdir -p /home/claude/lucide && cd /home/claude/lucide && npm pack lucide-static@latest -q >/dev/null && tar xzf lucide-static-*.tgz
fi
# Working copy with the module names the code imports
mkdir -p /home/claude/pipe /home/claude/cards
cp "$REPO"/pipeline/*.py /home/claude/pipe/
cp /home/claude/pipe/scenes_v5.py /home/claude/pipe/ds5.py
cp /home/claude/pipe/hubs_v5.py  /home/claude/pipe/hubs5.py
cp /home/claude/pipe/covers_v5.py /home/claude/pipe/covers5.py
cp /home/claude/pipe/scenes.py   /home/claude/pipe/scenes32.py
cp /home/claude/pipe/helpers.py  /home/claude/cards/helpers.py
# Smoke test: build every approved scene and cover, run all gates, convert to vector
cd /home/claude/pipe && python3 - << 'PY'
import sys; sys.path.insert(0,'/home/claude/pipe')
import ds5, hubs5, covers5, qa3, outline
n=0
for name,f in ds5.SCENES.items():
    s=f(); assert not qa3.run(s), (name, qa3.run(s)); assert '<text' not in outline.convert(s); n+=1
for hub,fs in hubs5.SCENES.items():
    for f in fs:
        s=f(); assert not qa3.run(s); assert '<text' not in outline.convert(s); n+=1
for k,f in covers5.COVERS.items():
    s=f(); assert not [i for i in qa3.run(s) if not i.startswith('off-canvas')]; n+=1
print(f"BOOTSTRAP OK: {n} scenes/covers built, all gates clean, vector conversion OK")
PY
