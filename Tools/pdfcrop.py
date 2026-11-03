r"""Crop lecture figures out of the ECE2050 chapter PDFs into ``Figures/<name>.png``.

Why PNG here: these are verbatim lecture graphics (gate symbol blocks, worked
K-map examples).  Anything that has to be *argued* (timing diagrams, VTC,
noise margins, K-map circle groups) is still redrawn as SVG by a script in
``Tools/figures/`` under the vault's normal visual language.

Every crop is registered below, so the whole figure set is reproducible with one
command and each image keeps a machine-readable link to its source page:

    D:\anaconda\python.exe Tools\pdfcrop.py                # render everything
    D:\anaconda\python.exe Tools\pdfcrop.py ch3-two-input  # render one crop

Crop modes
    "graphics"  union of the page's non-background graphics (images / curves /
                rects / lines) -- the normal choice for a figure slide
    "page"      the whole slide (when the slide IS the figure)
    "below"     everything below a given y (points from the top), e.g. under a title

Each rendered PNG is checked for ink coverage so a blank or all-white crop is
reported instead of silently embedded in a note.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pdfplumber
from PIL import Image

VAULT = Path(__file__).resolve().parent.parent
FIG_DIR = VAULT / "Figures"
DPI = 300

# name -> (pdf, page number as printed on the slide, mode, optional y for "below")
CROPS: dict[str, dict] = {
    # ---------------------------------------------------------------- Chapter 3
    "ch3-inverter-symbol": dict(pdf="ECE2050-Chap3.pdf", page=4, mode="graphics"),
    "ch3-single-input-gates": dict(pdf="ECE2050-Chap3.pdf", page=5, mode="graphics"),
    "ch3-xor-xnor": dict(pdf="ECE2050-Chap3.pdf", page=10, mode="graphics"),
    "ch3-xor-adder": dict(pdf="ECE2050-Chap3.pdf", page=11, mode="graphics"),
    "ch3-two-input-gates": dict(pdf="ECE2050-Chap3.pdf", page=12, mode="graphics"),
    "ch3-multiple-input-gates": dict(pdf="ECE2050-Chap3.pdf", page=13, mode="graphics"),
    # NOTE: slide p.16 (logic-level voltage ranges) is deliberately NOT cropped:
    # it is a measurement diagram with axis values, so it is redrawn as
    # Figures/logic-level-ranges.svg under the vault's mixed figure policy.
    # ---------------------------------------------------------------- Chapter 4
    "ch4-combinational-nodes": dict(pdf="ECE2050-Chap4.pdf", page=5, mode="graphics"),
    "ch4-kmap-3var-basic": dict(pdf="ECE2050-Chap4.pdf", page=50, mode="graphics"),
    "ch4-kmap-3var-example": dict(pdf="ECE2050-Chap4.pdf", page=51, mode="graphics"),
    "ch4-kmap-4var": dict(pdf="ECE2050-Chap4.pdf", page=52, mode="graphics"),
    "ch4-kmap-pos-example": dict(pdf="ECE2050-Chap4.pdf", page=55, mode="graphics"),
    "ch4-kmap-pos-to-sop": dict(pdf="ECE2050-Chap4.pdf", page=56, mode="graphics"),
    "ch4-kmap-dont-care": dict(pdf="ECE2050-Chap4.pdf", page=59, mode="graphics"),
    "ch4-seven-segment-kmap": dict(pdf="ECE2050-Chap4.pdf", page=61, mode="graphics"),
    # ---------------------------------------------------------------- Chapter 6
    # Full pages preserve power/ground labels and complements near slide edges.
    "ch6-adder-cascade": dict(pdf="ECE2050-Chap6.pdf", page=10, mode="page"),
    "ch6-voting-system": dict(pdf="ECE2050-Chap6.pdf", page=11, mode="page"),
    "ch6-comparator-cascade": dict(pdf="ECE2050-Chap6.pdf", page=23, mode="page"),
    "ch6-priority-encoder147": dict(pdf="ECE2050-Chap6.pdf", page=27, mode="page"),
    "ch6-decoder-expansion": dict(pdf="ECE2050-Chap6.pdf", page=34, mode="page"),
    "ch6-zero-suppression": dict(pdf="ECE2050-Chap6.pdf", page=37, mode="page"),
    "ch6-mux-implementations": dict(pdf="ECE2050-Chap6.pdf", page=40, mode="page"),
    "ch6-mux-function-generator": dict(pdf="ECE2050-Chap6.pdf", page=44, mode="page"),
    "ch6-hazard-consensus": dict(pdf="ECE2050-Chap6.pdf", page=53, mode="page"),
}


def _page_index(pdf, slide_no: int) -> int:
    """Slide number as printed == PDF page order for these decks (verified)."""
    return slide_no - 1


def graphics_bbox(page, pad: float = 6.0):
    """Union box of the figure graphics, ignoring slide furniture.

    Every slide in these decks carries a full-page background rect, a title
    banner in the top band and a footer band with a logo.  Those would drag any
    naive union out to the whole slide, so they are dropped first: full-page
    backgrounds, and anything living entirely inside the title band (top 13%)
    or the footer band (bottom 12%).

    Note: a *wide* graphic is NOT dropped -- several figures (the logic-level
    bands on Ch3 p.16, the four-gate summary on p.12) legitimately span ~90% of
    the slide width.  The band test above is what removes the banners.
    """
    W, H = page.width, page.height
    boxes = []
    for im in page.images:
        boxes.append((im["x0"], im["top"], im["x1"], im["bottom"]))
    for obj in list(page.curves) + list(page.rects) + list(page.lines):
        w = obj["x1"] - obj["x0"]
        h = obj["bottom"] - obj["top"]
        if w > 0.95 * W and h > 0.95 * H:
            continue                                   # slide background
        if obj["top"] > 0.88 * H or obj["bottom"] < 0.13 * H:
            continue                                   # footer logo / title band
        boxes.append((obj["x0"], obj["top"], obj["x1"], obj["bottom"]))
    if not boxes:
        return None
    x0 = min(b[0] for b in boxes) - pad
    top = min(b[1] for b in boxes) - pad
    x1 = max(b[2] for b in boxes) + pad
    bottom = max(b[3] for b in boxes) + pad
    return (max(0.0, x0), max(0.0, top),
            min(page.width, x1), min(page.height, bottom))


def ink_report(path: Path) -> str:
    import numpy as np

    im = Image.open(path).convert("L")
    small = im.resize((min(im.width, 400), min(im.height, 400)))
    arr = np.asarray(small)
    ink = float((arr < 240).mean())
    return f"{im.width}x{im.height}px, ink {ink:.1%}"


def content_bbox(page, left: float = 0.02, top: float = 0.13,
                 right: float = 0.02, bottom: float = 0.12):
    """Everything between the title band and the footer band (whole-width).

    Used when a slide's artwork is not in the vector layer (it can be baked into
    a background picture), where :func:`graphics_bbox` would return a fragment.
    """
    return (left * page.width, top * page.height,
            (1.0 - right) * page.width, (1.0 - bottom) * page.height)


def render_one(name: str, spec: dict, quiet: bool = False) -> int:
    pdf = VAULT / spec["pdf"]
    if not pdf.exists():
        print(f"  X {name}: missing {pdf.name}")
        return 1
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    note = ""
    with pdfplumber.open(pdf) as doc:
        page = doc.pages[_page_index(pdf, spec["page"])]
        if spec["mode"] == "page":
            box = (0.0, 0.0, page.width, page.height)
        elif spec["mode"] == "below":
            box = (0.0, float(spec["y"]), page.width, page.height)
        elif spec["mode"] == "content":
            box = content_bbox(page)
        else:
            box = graphics_bbox(page)
            area = 0.0 if box is None else (box[2] - box[0]) * (box[3] - box[1])
            if box is None or area < 0.15 * page.width * page.height:
                box = content_bbox(page)       # fell back: artwork is baked in
                note = "  (graphics box was a fragment -> content box)"
        img = page.crop(box).to_image(resolution=DPI)
        out = FIG_DIR / f"{name}.png"
        img.save(str(out))
    if not quiet:
        print(f"  wrote Figures/{name}.png  <- {spec['pdf']} p.{spec['page']} "
              f"[{spec['mode']}]  {ink_report(out)}{note}")
    return 0


def main() -> int:
    args = sys.argv[1:]
    names = args if args else list(CROPS)
    bad = 0
    for name in names:
        if name not in CROPS:
            print(f"  X {name}: not in the crop registry")
            bad += 1
            continue
        bad += render_one(name, CROPS[name])
    print(f"\ncrops rendered: {len(names) - bad}, problems: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
