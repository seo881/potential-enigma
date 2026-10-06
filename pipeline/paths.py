"""Where the image pipeline finds fonts, icons and its review folder, on any machine.
Linux sandbox (Claude.ai): the original /root/.fonts and /home/claude paths.
Anywhere else (Claude Code on macOS): <repo>/.cache/, filled by `python3 pipeline/assets.py`.
Override any of them with PE_FONTS, PE_ICONS, PE_REVIEW."""
import os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(REPO, ".cache")
def _pick(env, *cands):
    if os.environ.get(env): return os.environ[env].rstrip("/") + "/"
    for c in cands:
        if os.path.isdir(c): return c.rstrip("/") + "/"
    return cands[-1].rstrip("/") + "/"
FONT_DIR = _pick("PE_FONTS", "/root/.fonts", os.path.join(CACHE, "fonts"))
ICON_DIR = _pick("PE_ICONS", "/home/claude/lucide/package/icons", os.path.join(CACHE, "lucide", "package", "icons"))
REVIEW = _pick("PE_REVIEW", *(["/home/claude/review"] if os.path.isdir("/home/claude") else []), os.path.join(CACHE, "review"))
