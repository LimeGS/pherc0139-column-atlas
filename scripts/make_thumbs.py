#!/usr/bin/env python3
"""Downscale the villa plates into viewer index thumbnails (thumbs/*.jpg).

The viewer's column rail needs 38 small images, not 285 MB of full-resolution
PNGs. Run after make_photo_plates.py, before build_viewer.py.

Usage:
    python scripts/make_thumbs.py
"""
import os
import re

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIDTH = 200  # rail is 88 px wide; 200 covers 2x displays


def main():
    src_dir = os.path.join(ROOT, "plates_villa")
    out_dir = os.path.join(ROOT, "thumbs")
    os.makedirs(out_dir, exist_ok=True)
    for name in sorted(os.listdir(src_dir)):
        m = re.match(r"(\d+_[^.]+)_villa\.png$", name)
        if not m:
            continue
        with Image.open(os.path.join(src_dir, name)) as im:
            im.thumbnail((WIDTH, WIDTH * 4), Image.LANCZOS)
            out = os.path.join(out_dir, m.group(1) + ".jpg")
            im.convert("RGB").save(out, quality=80, optimize=True)
        print(f"{m.group(1)}.jpg {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
