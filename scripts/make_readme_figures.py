#!/usr/bin/env python3
"""Build the README figures from the committed plates and review data.

Writes:
  docs/atlas.jpg    - contact sheet of all 38 columns in reading order
  docs/styles.jpg   - one column (w047) in the three plate styles
  docs/windows.jpg  - w047 ink map with the confirmed-legible windows boxed

docs/viewer.jpg (the viewer screenshot) is captured by hand, not by this
script. Run after make_plates.py / make_photo_plates.py / make_thumbs.py.

Usage:
    python scripts/make_readme_figures.py
"""
import json
import os
import re

from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
BG, AMBER, MUTED = "#100d09", "#e8a33d", "#a4937a"
FIG = "13_w047"          # the widest-read body column: 12 confirmed windows


def font(size):
    for path in ("/System/Library/Fonts/Menlo.ttc",
                 "/System/Library/Fonts/SFNSMono.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()   # ponytail: ugly but never fails


def contact_sheet():
    """All 38 columns, 6 per row, in reading order."""
    names = sorted(n for n in os.listdir(os.path.join(ROOT, "thumbs")) if n.endswith(".jpg"))
    cols, cw, ch, pad = 6, 208, 176, 10
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw + pad, rows * ch + pad), BG)
    draw = ImageDraw.Draw(sheet)
    f = font(15)
    for i, name in enumerate(names):
        with Image.open(os.path.join(ROOT, "thumbs", name)) as im:
            im = im.copy()
        im.thumbnail((cw - 2 * pad, ch - 40))
        x = (i % cols) * cw + pad + (cw - 2 * pad - im.width) // 2
        y = (i // cols) * ch + pad
        sheet.paste(im, (x, y))
        pos, wrap = name[:-4].split("_")
        draw.text(((i % cols) * cw + pad, y + ch - 34), pos, font=f, fill=AMBER)
        draw.text(((i % cols) * cw + pad + 28, y + ch - 34), wrap, font=f, fill=MUTED)
    return sheet


def style_strip():
    """The same column rendered three ways."""
    srcs = [("ink map", f"plates/{FIG}.png"),
            ("papyrus (ours)", f"plates_photo/{FIG}_photo.png"),
            ("papyrus (villa recipe)", f"plates_villa/{FIG}_villa.png")]
    w, f = 430, font(15)
    tiles = []
    for label, rel in srcs:
        with Image.open(os.path.join(ROOT, rel)) as im:
            im = im.convert("RGB")
            im.thumbnail((w, w))
        tiles.append((label, im))
    h = max(im.height for _, im in tiles)
    strip = Image.new("RGB", (len(tiles) * (w + 8) + 8, h + 40), BG)
    draw = ImageDraw.Draw(strip)
    for i, (label, im) in enumerate(tiles):
        x = 8 + i * (w + 8)
        strip.paste(im, (x + (w - im.width) // 2, 8))
        draw.text((x, h + 18), label, font=f, fill=MUTED)
    return strip


def windows():
    """w047's ink map with the human-confirmed windows boxed, as the viewer draws them."""
    decisions = json.load(open(os.path.join(ROOT, "data/review_0139_human.json")))["decisions"]
    decisions += json.load(open(os.path.join(ROOT, "data/review_band_0139.json")))["decisions"]
    wrap = FIG.split("_")[1]
    with Image.open(os.path.join(ROOT, "plates", FIG + ".png")) as im:
        full_w, im = im.width, im.convert("RGB")
    im.thumbnail((1200, 1200))
    k = im.width / full_w
    draw = ImageDraw.Draw(im)
    for d in decisions:
        if d["rating"] == 1 and re.search(rf"-{wrap}_", d["segment"]):
            x, y, s = d["x"] * k, d["y"] * k, d["win"] * k
            draw.rectangle([x, y, x + s, y + s], outline=AMBER, width=2)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fig in (("atlas", contact_sheet()), ("styles", style_strip()),
                      ("windows", windows())):
        path = os.path.join(OUT, name + ".jpg")
        fig.save(path, quality=82, optimize=True)
        print(f"{path}  {fig.width}x{fig.height}  {os.path.getsize(path)//1024} KB")


if __name__ == "__main__":
    main()
