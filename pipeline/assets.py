"""Fetch the pinned design assets into <repo>/.cache (any OS, Python only):
Inter 4.1 (5 weights) and Lucide icons from lucide-static 1.52.0, the version the approved images were drawn with."""
import os, io, zipfile, tarfile, urllib.request, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import CACHE
INTER = "https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip"
LUCIDE = "https://registry.npmjs.org/lucide-static/-/lucide-static-1.52.0.tgz"
def main():
    fd = os.path.join(CACHE, "fonts"); os.makedirs(fd, exist_ok=True)
    if not os.path.exists(os.path.join(fd, "Inter-ExtraBold.ttf")):
        z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(INTER, timeout=120).read()))
        for w in ["Regular", "Medium", "SemiBold", "Bold", "ExtraBold"]:
            name = next(n for n in z.namelist() if n.endswith(f"/Inter-{w}.ttf") or n == f"Inter-{w}.ttf")
            open(os.path.join(fd, f"Inter-{w}.ttf"), "wb").write(z.read(name))
    ld = os.path.join(CACHE, "lucide")
    if not os.path.isdir(os.path.join(ld, "package", "icons")):
        os.makedirs(ld, exist_ok=True)
        tarfile.open(fileobj=io.BytesIO(urllib.request.urlopen(LUCIDE, timeout=120).read())).extractall(ld)
    print("assets OK:", fd, os.path.join(ld, "package", "icons"))
if __name__ == "__main__": main()
