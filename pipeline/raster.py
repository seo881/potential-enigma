"""SVG -> PNG. Uses rsvg-convert when installed (the Linux sandbox; keeps live share images byte-identical),
otherwise resvg-py (pip wheel, no system libraries; works on macOS)."""
import shutil, subprocess, os
def to_png(svg_path, out, width, height=None):
    if os.environ.get("PE_RASTER") != "resvg" and shutil.which("rsvg-convert"):
        cmd = ["rsvg-convert", "-w", str(width)] + (["-h", str(height)] if height else []) + ["-o", out, svg_path]
        subprocess.run(cmd, check=True); return out
    import resvg_py
    data = resvg_py.svg_to_bytes(svg_path=svg_path, width=width, height=height)
    open(out, "wb").write(bytes(data)); return out

# Share image (og:image) as WebP (Divit, 2026-10-09; LESSONS.md section 4): exactly 1200x630, at most 300 KB.
# Encoded twice with method 6, lossless and quality 90; the smaller wins, and the lossy one only if the text stays crisp at 100%
# (PSNR against the rendered raster >= OG_MIN_PSNR dB). The gates run on the encoded WebP itself.
OG_W, OG_H, OG_MAX_BYTES, OG_MIN_PSNR = 1200, 630, 300 * 1024, 38.0

def _psnr(a, b):
    from PIL import ImageChops, ImageStat
    import math
    mse = sum(v ** 2 for v in ImageStat.Stat(ImageChops.difference(a, b)).rms) / 3
    return 99.0 if mse == 0 else 20 * math.log10(255 / math.sqrt(mse))

def og_webp(src):
    """src: a path or PIL image of the rendered share image. Returns (webp bytes, info). Raises ValueError on a failed gate."""
    import io
    from PIL import Image
    im = (Image.open(src) if isinstance(src, str) else src).convert("RGB")
    if im.size != (OG_W, OG_H): raise ValueError(f"share image is {im.size[0]}x{im.size[1]}, must be {OG_W}x{OG_H}")
    cands = []
    for mode, kw in (("lossless", {"lossless": True}), ("q90", {"quality": 90})):
        buf = io.BytesIO(); im.save(buf, "WEBP", method=6, **kw); data = buf.getvalue()
        back = Image.open(io.BytesIO(data)); back.load()
        psnr = _psnr(im, back.convert("RGB"))
        cands.append((len(data), mode, data, psnr, back))
    ok = [c for c in cands if c[1] == "lossless" or c[3] >= OG_MIN_PSNR]
    size, mode, data, psnr, back = min(ok)
    # gates on the WebP as written
    if back.format != "WEBP": raise ValueError("encoded share image is not WebP")
    if back.size != (OG_W, OG_H): raise ValueError(f"WebP is {back.size[0]}x{back.size[1]}, must be {OG_W}x{OG_H}")
    if size > OG_MAX_BYTES: raise ValueError(f"WebP is {size // 1024} KB, limit {OG_MAX_BYTES // 1024} KB")
    return data, {"mode": mode, "bytes": size, "psnr": round(psnr, 1)}
