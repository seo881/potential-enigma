"""og_webp.py: one-off conversion of every existing share image images/<dir>/<slug>/og.png to og.webp (Divit, 2026-10-09).

    .venv/bin/python3 ops/og_webp.py            convert (skips pages whose og.webp is already rendered) and point spec.images.share_image at og.webp

Uses the renderer's encoder and gates (pipeline/raster.og_webp: 1200x630, <= 300 KB, crisp text). The PNGs stay in the repo
until the launch pages are verified live, then go in one commit. Pixels are identical to the PNG render, so nothing is re-rendered.
"""
import glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import raster

def main():
    conv = skip = 0; bad = []; sizes = []; specs = 0
    for png in sorted(glob.glob(os.path.join(ROOT, "images", "*", "*", "og.png"))):
        webp = png[:-4] + ".webp"
        if os.path.exists(webp) and os.path.getmtime(webp) > os.path.getmtime(png): skip += 1; continue
        try: data, info = raster.og_webp(png)
        except ValueError as e: bad.append(f"{os.path.relpath(png, ROOT)}: {e}"); continue
        open(webp, "wb").write(data); conv += 1; sizes.append(info["bytes"])
    for sp in sorted(glob.glob(os.path.join(ROOT, "specs", "*", "*.json"))):
        raw = open(sp).read(); s = json.loads(raw); im = (s.get("images") or {}).get("share_image") or {}
        if (im.get("path") or "").endswith("/og.png") and os.path.exists(os.path.join(ROOT, im["path"][:-4] + ".webp")):
            im["path"] = im["path"][:-4] + ".webp"; specs += 1
            open(sp, "w").write(json.dumps(s, indent=1, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""))
    print(f"converted {conv}; already WebP {skip}; failed {len(bad)}; specs repointed {specs}"
          + (f"; WebP {min(sizes) // 1024}-{max(sizes) // 1024} KB" if sizes else ""))
    for b in bad: print("  FAIL", b)
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
