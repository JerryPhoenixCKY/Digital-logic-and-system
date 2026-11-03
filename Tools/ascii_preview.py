r"""Crude ASCII preview of a rendered figure — lets a text-only agent eyeball
figure geometry without an image viewer.

Usage:
    D:\anaconda\python.exe Tools\ascii_preview.py wheatstone-bridge [width]

Reads the PNG backup written by figstyle (``.scratch/png/<name>.png``).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

VAULT = Path(__file__).resolve().parent.parent
PNG_DIR = VAULT / ".scratch" / "png"
RAMP = " .:-=+*#%@"


def preview(path: Path, width: int = 110) -> str:
    """Min-pooled (darkest-pixel-wins) ASCII render, cropped to the ink box.

    Min pooling keeps 2 px schematic strokes visible after downsampling;
    a plain resize would wash them out to near-white.
    """
    im = Image.open(path).convert("L")
    a = np.asarray(im, dtype=float)
    ink = a < 205
    if not ink.any():
        return "(blank figure: no ink)"
    ys, xs = np.nonzero(ink)
    pad = 4
    y0, y1 = max(0, ys.min() - pad), min(a.shape[0], ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(a.shape[1], xs.max() + pad + 1)
    a = a[y0:y1, x0:x1]

    h, w = a.shape
    bw = max(1, w // width)
    bh = max(1, int(round(bw * 2.1)))  # terminal cells are ~2x taller than wide
    H, W = max(1, h // bh), max(1, w // bw)
    block = a[: H * bh, : W * bw].reshape(H, bh, W, bw).min(axis=(1, 3))

    def ch(v: float) -> str:
        if v < 120:
            return "#"
        if v < 200:
            return "+"
        if v < 243:
            return "."
        return " "

    return "\n".join("".join(ch(v) for v in row).rstrip() for row in block)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    name = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 110
    path = PNG_DIR / (Path(name).stem + ".png")
    if not path.exists():
        print(f"missing PNG backup: {path}")
        return 1
    print(f"=== {path.name} ===")
    print(preview(path, width))
    return 0


if __name__ == "__main__":
    sys.exit(main())
