"""binary-powers-and-counting.svg -- powers of two and counting in 4 bits.

(a) 2^0 .. 2^10 : weight label, decimal value (log axis, values labelled).
(b) 0000 .. 1111 : the 16 four-bit code words with their decimal value; the bit
    that changed with respect to the previous step carries a triangle marker,
    which makes the rhythm visible (bit0 every step ... bit3 every 8 steps).

Used by Notes/Binary Number System.md.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

apply_mpl_style()

BOT = 0.1
POW_BOT, POW_TOP = 0.09, 6000

fig = plt.figure(figsize=(13.2, 6.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.5], wspace=0.18)
ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])

# ---------------------------------------------------------------- (a) 2^k ----
ks = list(range(11))
vals = [2 ** k for k in ks]
for k, v in zip(ks, vals):
    face = HILITE if k == 10 else ACCENT
    ax_a.bar([k], [v - POW_BOT], width=0.6, bottom=POW_BOT, color=face,
             edgecolor=INK, zorder=3)
    ax_a.text(k, v * 1.5, f"{v}", ha="center", va="bottom", fontsize=9,
              color=INK, zorder=4)

ax_a.set_yscale("log")
ax_a.set_ylim(POW_BOT, POW_TOP)
ax_a.set_yticks([0.1, 1, 10, 100, 1000])   # fixed decade ticks: every label is
                                           # inside the view, none off-canvas
ax_a.set_xlim(-0.8, 10.8)
ax_a.set_xticks(ks)
ax_a.set_xticklabels([f"$2^{{{k}}}$" for k in ks], fontsize=10)
ax_a.set_ylabel("weight (log scale)", fontsize=11)
ax_a.set_title("(a) powers of two $2^{0}$-$2^{10}$", pad=14)
ax_a.text(0.03, 0.96,
          "handy to memorize:\n$2^{0}$-$2^{7}$ (p.8);\n"
          "$2^{10}=1024=$ 1 K (p.25)",
          transform=ax_a.transAxes, ha="left", va="top", fontsize=9,
          linespacing=1.6,
          bbox=dict(boxstyle="round,pad=0.4", facecolor=FILL, edgecolor=MUTED))

# ------------------------------------------------------- (b) counting 0-15 ---
WORDS = [f"{i:04b}" for i in range(16)]
COL_X = [1.75, 7.95]           # left edge of the bit boxes of each column
LAB_X = [1.35, 7.55]           # right edge of the decimal column
ROW_Y = [8.0 - i for i in range(8)]
BW, BH, PITCH = 0.82, 0.66, 1.0

ax_b.set_xlim(0.0, 14.0)
ax_b.set_ylim(-1.05, 10.1)
ax_b.set_xticks([])
ax_b.set_yticks([])
ax_b.grid(False)
for spine in ax_b.spines.values():
    spine.set_visible(False)
ax_b.set_title("(b) counting 0-15 in four bits: the changed bit is marked",
               pad=14)

for col in (0, 1):
    for j in range(4):
        ax_b.text(COL_X[col] + j * PITCH + BW / 2, 9.15, f"bit {3 - j}",
                  ha="center", va="center", fontsize=9, color=MUTED)

for i, word in enumerate(WORDS):
    col, row = divmod(i, 8)
    y = ROW_Y[row]
    ax_b.text(LAB_X[col], y, f"{i}", ha="right", va="center", fontsize=11,
              color=INK)
    for j, bit in enumerate(word):
        x = COL_X[col] + j * PITCH
        ax_b.add_patch(Rectangle((x, y - BH / 2), BW, BH, zorder=3,
                                 facecolor=FILL if bit == "1" else "white",
                                 edgecolor=INK))
        ax_b.text(x + BW / 2, y, bit, ha="center", va="center", fontsize=11,
                  color=INK, zorder=4)
        if i > 0 and bit != WORDS[i - 1][j]:
            ax_b.scatter([x + BW / 2], [y - BH / 2 - 0.16], marker="v", s=34,
                         color=HILITE, zorder=5)

ax_b.scatter([5.60], [9.15], marker="v", s=34, color=HILITE, zorder=5)
ax_b.text(5.78, 9.15, "= flipped", ha="left", va="center",
          fontsize=9, color=HILITE)
ax_b.text(7.0, 0.05,
          "bit 0 flips every step  |  bit 1 every 2 steps\n"
          "bit 2 every 4 steps  |  bit 3 every 8 steps",
          ha="center", va="center", fontsize=9.5, color=INK, linespacing=1.6,
          bbox=dict(boxstyle="round,pad=0.4", facecolor=FILL, edgecolor=MUTED))
ax_b.text(7.0, -0.75,
          "0111 -> 1000 flips all four bits at once: the carry ripples through",
          ha="center", va="center", fontsize=9.5, color=BAD)

fig.subplots_adjust(left=0.055, right=0.995, top=0.90, bottom=0.085, wspace=0.20)
save_fig(fig, "binary-powers-and-counting")
