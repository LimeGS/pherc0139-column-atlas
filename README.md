# PHerc 0139: the columns, in reading order

**The columns of PHerc 0139 (Philodemus, On Gods, book 8) as plates in
physical reading order: 10 with no published readings at all, 4 with
isolated phrase-level readings published in the paper's supplement, and
the already-read title column as a control. Built entirely from public
data: the official ds8 ink maps and the public segment meshes.**

What is formally published on PHerc 0139 (arXiv 2606.29085, 2026-06-25):
the end title ("Φιλοδήμου περὶ θεῶν Η") and, in Supplementary Fig. 1
("Readings from PHerc. 139"), five isolated phrase readings located by
wrap: w49 χωρὶϲ προνο[ί]α̣ϲ̣, w25 ἀόρατα, w34 καὶ τὸ κατ̣ὰ̣ φύϲιν,
w47 καὶ πάν̣τ̣α̣ χωρὶϲ πόνων, w49(int) νοερόν. No continuous transcription
of any column has been published. Everything in these plates beyond the
title and those five phrases is, as of 2026-07-13, unpublished territory —
and the five located phrases double as anchor points to align this series
against the official reading.

Open `viewer/index.html` (or serve this repo and open `/viewer/`) for the
annotated reading view; `plates/` holds the clean full-resolution PNGs.

## How the reading order was obtained

### 1. Wrap order = mesh geometry, not file names

Every segment's TIFXYZ mesh (x/y/z.tif point map, public bucket) references
the same CT volume (20260102150214, 2.399 µm), so all coordinates are
directly comparable. We fit the scroll axis (first principal component of
the union of all segment point clouds, ~760k subsampled points) and
computed, per segment, the **mean radial distance of its point cloud to
that axis** — the wrap radius.

Result: **Spearman rho = 0.9993 (p = 2e-51)** between the wNNN number in
the segment names and the measured radius. The numbering IS the physical
radial order: w023 innermost (r = 7.02 mm) to w059 outermost (13.26 mm),
all 37 wraps consecutive with no gaps, and the mean radial step between
consecutive wraps is **~0.17 mm — the thickness of rolled papyrus**, an
independent physical sanity check.

> **Method pitfall, documented so you don't repeat it:** the radius of a
> segment's *centroid* is useless here. Each segment is a full turn, so
> its centroid collapses onto the axis regardless of the wrap's radius
> (centroids gave Spearman 0.28 = noise). Use the mean radial distance of
> the *cloud*.

Herculaneum scrolls are read unrolling outer → inner (the end of the work,
with the subscriptio, is rolled innermost). So reading order is
w059 → w024. The title lands at r = 5.50 mm — **inside** the innermost
body wrap — exactly where a subscriptio should be. (Caveat: the title
mesh sits ~4-5 cm away along the axis from the body wraps — a physically
separate chunk in the same scanned volume — so its radius is indicative,
not as rigorous as the body monotonicity.)

### 2. One wrap ≈ one column

At these radii the circumference of one turn is 2πr = 46-83 mm — roughly
the width of one Herculaneum column. Measured plate widths track 2πr wrap
by wrap (e.g. w059: 87.7 mm map vs 83.3 mm circumference; w024: 58.0 vs
45.7, constant margin). **Each segment map is already an unrolled
column** — no stitching across segments needed.

### 3. Reading direction within a plate

Two independent checks (evidence in `data/direction_check/`):

- **Line continuity**: strips cut across contiguous review windows show
  text lines running horizontally and continuously across the full plate
  width (w047 band y=546, 1911 px through 6 windows without a seam;
  w043 band y=1904, 1610 px).
- **No mirroring**: asymmetric letterforms (lunate epsilon/sigma opening
  RIGHT) in the top-scoring windows, plus the decisive convention anchor:
  the title was officially read from this same render family — a mirrored
  family would not read.

Non-mirrored + lines along x ⇒ the greek runs left → right ⇒ within-plate
reading order is x ascending. The exact wrap-to-wrap seam position (where
one turn's text ends and the next begins) is not modeled; it does not
affect the relative order of anything shown.

### 4. The plates (two styles)

Two renderings of each column, toggled in the viewer:

- **`plates/` — pure ink maps.** The official ds8 ink-detection maps
  (~18 µm/px), contrast-stretched to the 2-98 percentile band, ink white
  on black. Nothing else: no denoising, no content edits, no resampling.
  The viewer overlays amber boxes on the reviewed windows; the PNGs are
  clean.
- **`plates_photo/` — publication-style composites.** Papyrus texture from
  the CT surface volume (the segment's `surface-volumes` zarr, level-3
  multiscale, mid-depth layer) as a light background, with the ink
  prediction composited in BLACK on top
  (`out = paper_texture * (1 - 0.88 * ink)`). This is the same recipe as
  the paper's Fig. 4 panel b ("ink-enhanced signal shown in black against
  the papyrus texture"): letters read as lines of text rather than white
  blobs. The texture is fetched with HTTP Range requests over the raw
  (uncompressed, `compressor: null`) zarr chunks so only the three mid
  layers of each chunk are downloaded, not the whole volume. Regenerate
  with `scripts/make_photo_plates.py`, which fetches both the official ds8
  maps and the textures from the public bucket.

## Human review behind the amber boxes

The windows come from a legibility index over the official maps
(proxy classifier → human review of every flagged window, one by one):
63 flagged, **54 rated "clear text"** (52 outside the title). In a second
pass, the 52 body windows were re-reviewed *in physical reading order*
with 6 visual filters each: **52/52 confirmed legible**
(`data/atlas_readthrough.json`; raw first-pass review in
`data/review_0139_human.json`). Single reviewer, no inter-rater check;
"legible" means letterforms a reader could attempt — **it is not a
transcription**.

## Reading order and content summary

| # | wrap | radius (mm) | clear windows |
|---|------|------------|---------------|
| 01 | w059 | 13.26 | 3 |
| 02 | w058 | 13.05 | 1 |
| 03 | w056 | 12.79 | 2 |
| 04 | w049 | 11.62 | 4 |
| 05 | w047 | 11.37 | 8 |
| 06 | w046 | 10.95 | 4 |
| 07 | w045 | 10.92 | 3 |
| 08 | w044 | 10.62 | 7 |
| 09 | w043 | 10.43 | 10 |
| 10 | w042 | 10.25 | 1 |
| 11 | w041 | 10.15 | 1 |
| 12 | w034 | 9.04 | 3 |
| 13 | w025 | 7.52 | 1 |
| 14 | w024 | 7.28 | 4 |
| 15 | title | 5.50 | 2 (control — officially read) |

The densest text sits mid-band (w043-w047: 29 of the 52 windows).

## How much of the scroll is this?

Measured against what is publicly segmented (38 segments, 1,529 cm2 of
mesh, ~2.4 m of papyrus by sum of 2*pi*r): these 15 plates are 584 cm2 /
0.97 m, i.e. **about 40% of everything segmented so far**.

Against the whole scroll (estimate, assumptions explicit): the scanned
volume is 184.6 mm along the axis and 63.6 mm across. With an outer radius
of 25-30 mm, a core of 3-5 mm and the measured 0.17 mm/wrap step, the
scroll holds roughly 118-159 wraps and 11-16 m of papyrus. These plates
are then **~6-9% of the papyrus length within the covered band, and ~2-3%
of the total surface**.

One more honest number: the segments only span a **52 mm axial band of the
184.6 mm volume (~28% of the axis)**. If papyrus occupies the full axis,
these plates show a horizontal band of taller columns, with text above and
below what is segmented today. In other words: most of this scroll,
including more of these same wraps, is still waiting for segmentation.

## Two open asks (for papyrologist eyes)

1. Is any of this actually readable at ds8 resolution?
2. The paper's Supplementary Fig. 1 publishes five phrase readings WITH
   wrap locations (w25, w34, w47, w49) and images at 5 mm scale. All four
   wraps are plates in this atlas (13, 12, 05, 04). Matching those five
   published snippets to exact coordinates in our plates would anchor the
   whole series, pixel-level, against the official reading.

## Honest limits

- We flag and order; we do not read greek. No transcription is claimed.
- Four of the fourteen body plates (w025, w034, w047, w049) contain the
  five isolated phrases read in the paper's supplement; they are labeled
  in the viewer. The other ten body plates have no published readings we
  could locate (checked against the paper incl. supplement,
  scrollprize.org and community repos, 2026-07-13).
- Single reviewer for the window labels.
- ds8 resolution (~18 µm/px): letters are 80-220 px tall — visible, but a
  serious reading attempt may want the full-resolution renders.
- **The amber boxes undercount the text — by design.** They mark only the
  windows that scored >=0.9 AND were human-confirmed (62 of 1,860 one-cm
  windows on these segments, ~3%). The index is precision-oriented triage;
  the plates visibly contain far more text than the flagged spots (faint or
  partial text dilutes inside a 1 cm window and scores low). Boxes mean
  "guaranteed", not "all there is".
- This is triage/presentation of official model output, not a new ink
  detector. Whatever the official maps miss, these plates miss.
- Perishable: the official team is actively scaling transcription
  (PHerc 1667 fully read, 2026-06). This ordering is useful today.

## Reproduce (all from public data)

```bash
pip install numpy pillow boto3 scipy
python scripts/wrap_order.py            # meshes -> wrap_radial.json + table (~1 GB download)
python scripts/make_plates.py           # official ds8 maps -> plates/*.png
python scripts/make_photo_plates.py     # + surface textures -> plates_photo/*.png
```

`scripts/vesuvius_data.py` is the anonymous open-data-bucket helper.
`data/wrap_radial.json` is the committed result of wrap_order.py so the
numbers above are checkable without re-downloading anything.

## License

Text and scripts MIT. The plates are derived from the Vesuvius Challenge's
official ink maps (CC BY-NC 4.0) and are therefore CC BY-NC 4.0.
