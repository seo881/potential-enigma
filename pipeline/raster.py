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
