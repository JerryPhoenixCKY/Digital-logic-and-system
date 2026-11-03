"""Fixed-point formats: U4.4 / U3.5 / U6.2 for +6.75 and Q4.4 for -6.75.

Panel (a): the eight positional weights of a U4.4 register with the implied
binary point, plus the same value 6.75 re-encoded as U3.5 and U6.2 (moving the
point one place left shifts the stored pattern one place left).

Panel (b): Q4.4 -- the MSB carries the weight -2^3, so the same 8-bit register
becomes signed; -6.75 is built from 6.75 by "invert the bits, add 1".
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

CW = 1.0          # cell width  (one bit)
CH = 0.62         # cell height
GAP = 0.10        # gap between neighbouring bit cells


def bit_cells(ax, bits, y, point_after=None, emphasise=(), x0=0.0):
    """One row of bit cells; `point_after` = number of integer bits."""
    for i, b in enumerate(bits):
        x = x0 + i * CW
        if i in emphasise:
            face, txt = HILITE, "white"
        else:
            face, txt = FILL, INK
        ax.add_patch(Rectangle((x, y), CW - GAP, CH, facecolor=face,
                               edgecolor=INK, zorder=2))
        ax.text(x + (CW - GAP) / 2, y + CH / 2, b, ha="center", va="center",
                fontsize=12, color=txt, zorder=3)
    if point_after is not None:
        xp = x0 + point_after * CW - GAP / 2
        ax.plot([xp, xp], [y - 0.22, y + CH + 0.22], color=HILITE,
                linestyle=(0, (2, 2)), zorder=1)
        ax.plot([xp], [y - 0.30], marker="o", markersize=5, color=HILITE,
                zorder=4)


def weights(ax, labels, values, y_sym, y_val, x0=0.0, emphasise=()):
    """Two text rows above a bit row: symbolic weights, then their values."""
    for i, (lab, val) in enumerate(zip(labels, values)):
        x = x0 + i * CW + (CW - GAP) / 2
        col = HILITE if i in emphasise else INK
        ax.text(x, y_sym, lab, ha="center", va="center", fontsize=11, color=col)
        ax.text(x, y_val, val, ha="center", va="center", fontsize=10, color=col)


apply_mpl_style()
fig, (axa, axb) = plt.subplots(1, 2, figsize=(14.4, 6.0))

# ----------------------------------------------------------------- panel (a)
axa.set_xlim(-2.4, 15.6)
axa.set_ylim(-0.75, 5.35)
axa.set_axis_off()
axa.set_title("(a) U4.4 : the implied binary point")

sym = ["$2^{3}$", "$2^{2}$", "$2^{1}$", "$2^{0}$",
       "$2^{-1}$", "$2^{-2}$", "$2^{-3}$", "$2^{-4}$"]
val = ["8", "4", "2", "1", "1/2", "1/4", "1/8", "1/16"]

weights(axa, sym, val, 4.92, 4.50)
bit_cells(axa, "01101100", 3.55, point_after=4)
axa.text(-0.35, 3.86, "U4.4", ha="right", va="center", fontsize=12)
axa.text(8.35, 3.86, "0110.1100", ha="left", va="center", fontsize=12,
         color=HILITE)
axa.text(8.35, 3.40, "= 108 / $2^{4}$ = 108/16 = 6.75", ha="left", va="center",
         fontsize=11)
axa.text(-0.35, 3.15, "point", ha="right", va="center", fontsize=9, color=MUTED)
axa.text(3.95, 2.90, "binary point (implied, never stored)", ha="center",
         va="center", fontsize=10, color=MUTED)

axa.text(-2.30, 2.15, "same value, other agreed point positions:", ha="left",
         va="center", fontsize=11, color=ACCENT)
bit_cells(axa, "11011000", 1.35, point_after=3)
axa.text(-0.35, 1.66, "U3.5", ha="right", va="center", fontsize=12)
axa.text(8.35, 1.66, "110.11000 = 216 / $2^{5}$ = 6.75", ha="left",
         va="center", fontsize=11)
axa.text(-0.35, 1.20, "step $2^{-5}$ = 0.03125", ha="right", va="center",
         fontsize=9, color=MUTED)

bit_cells(axa, "00011011", 0.25, point_after=6)
axa.text(-0.35, 0.56, "U6.2", ha="right", va="center", fontsize=12)
axa.text(8.35, 0.56, "000110.11 = 27 / $2^{2}$ = 6.75", ha="left", va="center",
         fontsize=11)
axa.text(-0.35, 0.10, "step $2^{-2}$ = 0.25", ha="right", va="center",
         fontsize=9, color=MUTED)

axa.text(-2.30, -0.45,
         "point left by k  ->  stored pattern left by k (same value, new step)",
         ha="left", va="center", fontsize=10, color=ACCENT)

# ----------------------------------------------------------------- panel (b)
axb.set_xlim(-3.4, 15.4)
axb.set_ylim(-0.95, 5.35)
axb.set_axis_off()
axb.set_title("(b) Q4.4 : MSB weight $-2^{3}$")

qsym = ["$-2^{3}$", "$2^{2}$", "$2^{1}$", "$2^{0}$",
        "$2^{-1}$", "$2^{-2}$", "$2^{-3}$", "$2^{-4}$"]
qval = ["-8", "4", "2", "1", "1/2", "1/4", "1/8", "1/16"]

weights(axb, qsym, qval, 4.92, 4.50, emphasise=(0,))
bit_cells(axb, "10010100", 3.55, point_after=4, emphasise=(0,))
axb.text(-0.35, 3.86, "Q4.4", ha="right", va="center", fontsize=12)
axb.text(8.35, 3.86, "1001.0100", ha="left", va="center", fontsize=12,
         color=HILITE)
axb.text(8.35, 3.40, "sign bit = 1 (negative)", ha="left", va="center",
         fontsize=11, color=BAD)
axb.text(3.95, 2.90, "the same implied point as U4.4", ha="center", va="center",
         fontsize=10, color=MUTED)

axb.text(-3.30, 2.15, "6.75  =  0110 1100", ha="left", va="center",
         fontsize=12)
axb.text(-3.30, 1.62, "invert  ->  1001 0011", ha="left", va="center",
         fontsize=12)
axb.text(-3.30, 1.09, "add 1   ->  1001 0100", ha="left", va="center",
         fontsize=12, color=HILITE)
axb.text(8.90, 1.62, "= -6.75", ha="left", va="center", fontsize=12,
         color=HILITE)
axb.text(8.90, 1.09, "LSB +1: 0011 + 1 = 0100", ha="left", va="center",
         fontsize=10, color=MUTED)

axb.text(-3.30, 0.42, "value check:  $-8 + 1 + 0.25 = -6.75$", ha="left",
         va="center", fontsize=11)
axb.text(-3.30, 0.00, "Q4.4 range $[-8,\\ +7.9375]$, step $2^{-4}$ = 0.0625",
         ha="left", va="center", fontsize=11)
axb.text(-3.30, -0.48,
         "MSB is weight, not just a flag: 1000 0000 = -8, 1111 1111 = -0.0625",
         ha="left", va="center", fontsize=10, color=ACCENT)

save_fig(fig, "fixed-point-format")
