"""Flatten transparent PNGs onto a solid background and write the numbered dataset folder.
usage: python3 prep_dataset.py <src_dir> <dst_dir> [white|black|#rrggbb]
dst_dir name is kohya-style `<repeats>_<name>` (e.g. dataset/10_mychar)."""
import os, sys, glob
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
bg_arg = sys.argv[3] if len(sys.argv) > 3 else "white"
bg = {"white": (255, 255, 255), "black": (0, 0, 0)}.get(bg_arg) or Image.new("RGB", (1, 1), bg_arg).getpixel((0, 0))
os.makedirs(dst, exist_ok=True)
files = sorted(f for ext in ("png", "jpg", "jpeg", "webp") for f in glob.glob(f"{src}/*.{ext}"))
for i, f in enumerate(files):
    im = Image.open(f).convert("RGBA")
    canvas = Image.new("RGBA", im.size, bg + (255,))
    canvas.alpha_composite(im)
    canvas.convert("RGB").save(f"{dst}/{i:03d}.png")
print(f"{len(files)} images -> {dst}")
