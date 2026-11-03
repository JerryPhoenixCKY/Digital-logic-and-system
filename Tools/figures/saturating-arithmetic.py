"""U4.4 adder output vs. the true (exact) sum: wrap-around vs. saturation.

An 8-bit U4.4 register holds only [0, 15.9375] with a step of 2^-4.  Adding
12 + 7.5 = 19.5 needs 9 bits: keeping the low 8 bits (0011 1000 = 3.5) is
badly wrong, saturating arithmetic clamps to 1111 1111 = 15.9375.  The wrap
produces the classic artifacts -- a dark pixel inside a bright video area, a
loud click in audio.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import numpy as np
import matplotlib.pyplot as plt

MAXV = 15.9375          # U4.4 full scale = 255 / 2^4
X = 19.5                # 12 + 7.5
WRAPV = 3.5             # 19.5 - 16 = 3.5  (low 8 bits of 1 0011 1000)

apply_mpl_style()
fig, ax = plt.subplots(figsize=(10.2, 5.9))

xa = np.linspace(0.0, 16.0, 2001)
xb = np.linspace(16.0, 20.0, 501)
ax.plot(xa, xa, color=BAD)                       # wrap
ax.plot(xb, xb - 16.0, color=BAD)
ax.plot(xa, np.minimum(xa, MAXV), color=GOOD)    # saturate
ax.plot(xb, np.full_like(xb, MAXV), color=GOOD)

ax.plot([0.0, 20.0], [MAXV, MAXV], color=MUTED, linestyle=(0, (5, 3)))
ax.plot([X, X], [0.0, MAXV], color=MUTED, linestyle=(0, (2, 2)))

ax.plot([X], [WRAPV], marker="o", markersize=9, color=BAD, zorder=5)
ax.plot([X], [MAXV], marker="o", markersize=9, color=GOOD, zorder=5)

ax.annotate("wrap = keep the low 8 bits\n$12 + 7.5 = 19.5$  ->  3.5 = 0011 1000",
            xy=(X - 0.3, WRAPV), xytext=(10.6, 2.2), ha="left", va="center",
            fontsize=11, color=BAD,
            arrowprops=dict(arrowstyle="->", color=BAD))
ax.annotate("saturate = clamp at the maximum\n->  15.9375  =  1111 1111",
            xy=(X - 0.3, MAXV), xytext=(8.6, 13.4), ha="left", va="center",
            fontsize=11, color=GOOD,
            arrowprops=dict(arrowstyle="->", color=GOOD))

ax.text(20.4, MAXV + 0.7, "U4.4 max = 15.9375", ha="right", va="center",
        fontsize=10.5, color=MUTED)

ax.text(0.4, 22.6,
        "while the sum still fits, both curves agree: output = input\n"
        "wrap artifact: a dark pixel among bright video pixels, or a loud\n"
        "click (pop) in audio -- the peak flips to a tiny value\n"
        "saturation artifact: the peak is flattened, never inverted",
        ha="left", va="top", fontsize=10, color=INK,
        bbox=dict(facecolor=FILL, edgecolor=MUTED, pad=0.45))

ax.set_xlim(0.0, 20.6)
ax.set_ylim(0.0, 23.0)
ax.set_xlabel("true sum $a + b$  (exact real value)")
ax.set_ylabel("8-bit U4.4 output\n(value stored / read back)")
ax.set_title("U4.4 adder: wrap-around vs. saturating arithmetic")

save_fig(fig, "saturating-arithmetic")
