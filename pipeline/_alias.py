"""Let the pipeline import its modules by the short names the scene code uses (ds5, hubs5, covers5, scenes32)
straight from the repo, so no working copy under /home/claude/pipe is needed."""
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
for short, real in [("ds5", "scenes_v5"), ("hubs5", "hubs_v5"), ("covers5", "covers_v5")]:
    if short not in sys.modules: sys.modules[short] = importlib.import_module(real)
