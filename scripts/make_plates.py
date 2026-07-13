#!/usr/bin/env python3
"""Regenerate the column plates from the OFFICIAL ds8 ink maps.

For each wrap in reading order (outer to inner, w059 -> w023, then the
title as control), downloads the segment's official ds8 ink-detection map
from the open-data bucket and writes a full-resolution plate:
contrast stretch to the 2-98 percentile band, NOTHING else (no denoising,
no content edits, no resampling).

Reading order comes from wrap_radial.json (see wrap_order.py): the wNNN
sequence is strongly geometry-consistent with radial order (Spearman 0.9993),
though it is not a strict sort of the per-wrap radius estimates. Scrolls are read
unrolling outer -> inner, and within a plate the greek runs left to right
(verified: continuous text lines across the full plate width + non-mirrored
letterforms + the officially-read title belongs to this same render family).

Usage:
    python scripts/make_plates.py [--out plates] [--work work_maps]
"""
import argparse
import glob
import os
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vesuvius_data import ls, download  # noqa: E402

# Every segmented wrap in physical reading order (outer -> inner, w059 -> w023;
# rho=0.9993 vs radius), with the title (subscriptio, innermost) last as control.
READING = ["w059", "w058", "w057", "w056", "w055", "w054", "w053", "w052",
           "w051", "w050", "w049", "w048", "w047", "w046", "w045", "w044",
           "w043", "w042", "w041", "w040", "w039", "w038", "w037", "w036",
           "w035", "w034", "w033", "w032", "w031", "w030", "w029", "w028",
           "w027", "w026", "w025", "w024", "w023", "title"]


def stretch(a):
    lo, hi = np.percentile(a, [2, 98])
    return np.clip((a.astype(np.float32) - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="plates")
    ap.add_argument("--work", default="work_maps")
    ap.add_argument("--scroll", default="PHerc0139")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    subs, _ = ls(f"{args.scroll}/segments/", delimiter="/")
    segs = sorted(s.split("/")[-2] for s in subs)
    by_wrap = {}
    for seg in segs:
        for w in READING:
            if f"-{w}_" in seg:
                by_wrap[w] = seg

    for i, w in enumerate(READING):
        seg = by_wrap[w]
        _, keys = ls(f"{args.scroll}/segments/{seg}/ink-detection/downsampled/", delimiter="/")
        ds8 = [k for k, _ in keys if k.endswith("-ds8.jpg")]
        if not ds8:
            print(f"{w}: sin mapa ds8, salteado")
            continue
        local = os.path.join(args.work, os.path.basename(ds8[0]))
        download(ds8[0], local)
        M = np.array(Image.open(local).convert("L"))
        Image.fromarray(stretch(M)).save(f"{args.out}/{i+1:02d}_{w}.png", optimize=True)
        print(f"{i+1:02d} {w} <- {seg} ({M.shape[1]}x{M.shape[0]}px)")


if __name__ == "__main__":
    main()
