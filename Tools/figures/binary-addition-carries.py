"""N08 Binary Arithmetic -- the carry chain of 1011 + 0110.

(a) the four columns of the long addition with carry-in / carry-out of every
    column, giving the 5-bit sum 1 0001 (base 2) = 17;
(b) the same sum in a 4-bit register: the carry-out of the MSB column is
    dropped, so the register reads 0001 = 1 -- an error of 16 = 2^4.

Verified numbers (verify_ch2.txt): 1011 + 0110 = 10001 = 17 (needs 5 bits).

Run:  D:\\anaconda\\python.exe Tools\\figures\\binary-addition-carries.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# bit index -> bit value, for every row of the addition table (bit 4 is the
# extra 5th bit that only the carry reaches)
C_IN = {4: 1, 3: 1, 2: 1, 1: 0, 0: 0}
C_OUT = {4: 1, 3: 1, 2: 1, 1: 1, 0: 0}
ROWA = {4: 0, 3: 1, 2: 0, 1: 1, 0: 1}
ROWB = {4: 0, 3: 0, 2: 1, 1: 1, 0: 0}
SUMS = {4: 1, 3: 0, 2: 0, 1: 0, 0: 1}
COL_EQ = {4: "0+0+1=1", 3: "1+0+1=10", 2: "0+1+1=10",
          1: "1+1+0=10", 0: "1+0+0=1"}


def cell(ax, x, y, text, fc=FILL, ec=INK, tc=INK, fs=15.0, ls="-", lw=1.6,
         w=1.0, h=1.0, z=3):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                           linewidth=lw, linestyle=ls, zorder=z))
    ax.text(x + w / 2.0, y + h / 2.0, text, ha="center", va="center",
            color=tc, fontsize=fs, zorder=z + 1)


def row(ax, values, y, h, tc=INK, fc=FILL, ec=INK, fs=15.0, muted=None,
        hl=None, ls="-", lw=1.6):
    """Draw one 5-bit row; bits are placed at x = 4 - bit."""
    for b in range(4, -1, -1):
        x = 4 - b
        v = str(values[b])
        if muted is not None and b in muted:
            cell(ax, x, y, v, fc="white", ec=MUTED, tc=MUTED, fs=fs,
                 ls=(0, (3, 2)), lw=1.3, h=h)
        elif hl is not None and b in hl:
            cell(ax, x, y, v, fc=FILL, ec=HILITE, tc=HILITE, fs=fs,
                 lw=2.4, h=h)
        else:
            cell(ax, x, y, v, fc=fc, ec=ec, tc=tc, fs=fs, ls=ls, lw=lw, h=h)


def panel_a(ax):
    ax.set_title("(a) Carry chain of 1011 + 0110", loc="left", fontsize=12.5,
                 pad=10)

    row(ax, C_IN, 6.60, 1.00, tc=ACCENT)
    row(ax, C_OUT, 5.10, 1.00, tc=ACCENT)
    row(ax, ROWA, 3.60, 1.00, muted={4})
    row(ax, ROWB, 2.30, 1.00, muted={4})

    ax.plot([0, 5], [2.05, 2.05], color=INK, lw=2.2, solid_capstyle="round",
            zorder=4)
    row(ax, SUMS, 0.80, 1.00, tc=INK, hl={4})

    # every carry-out is the carry-in of the column on its left
    for b in range(4):
        ax.annotate("", xy=(4.5 - (b + 1), 6.58), xytext=(4.5 - b, 6.12),
                    arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.4,
                                    shrinkA=0.0, shrinkB=0.0), zorder=4)

    labels = [(7.10, "carry in $c_{in}$", ACCENT),
              (5.60, "carry out $c_{out}$", ACCENT),
              (4.10, "A = 1011", INK),
              (2.80, "B = 0110", INK),
              (1.30, "sum", INK)]
    for y, txt, col in labels:
        ax.text(-0.35, y, txt, ha="right", va="center", fontsize=10.5,
                color=col, zorder=5)

    for b in range(5):
        # staggered on two levels: neighbouring column equations would touch
        ax.text(4.5 - b, 0.45 if b % 2 == 0 else 0.05, COL_EQ[b],
                ha="center", va="center", fontsize=9.0, color=MUTED, zorder=5)
    ax.text(2.5, -0.45,
            "1011 + 0110 = 1 0001 (base 2) = 17 (base 10): the sum needs 5 bits",
            ha="center", va="center", fontsize=10.5, color=HILITE, zorder=5)

    ax.set_xlim(-2.95, 5.70)
    ax.set_ylim(-0.95, 8.15)
    ax.set_axis_off()


def panel_b(ax):
    ax.set_title("(b) 4-bit output: the carry-out is lost, so 17 reads as 1",
                 loc="left", fontsize=12.5, pad=10)

    ax.plot([0.10, 17.90], [4.40, 4.40], color=INK, lw=2.4,
            solid_capstyle="round", zorder=3)
    for v in range(18):
        ax.plot([v, v], [4.40, 4.28], color=MUTED, lw=1.1, zorder=2)
    for v in (0, 5, 10, 15, 16, 17):
        ax.text(v, 4.16, str(v), ha="center", va="top", fontsize=9.5,
                color=MUTED, zorder=5)

    ax.add_patch(Rectangle((0, 3.58), 15, 0.24, facecolor=FILL,
                           edgecolor=MUTED, linewidth=1.2, zorder=1))
    ax.text(5.5, 3.20, "4-bit range: [0, 15]", ha="center", va="center",
            fontsize=10.5, color=INK, zorder=5)

    ax.plot([17], [4.40], marker="o", ms=9.5, color=HILITE, zorder=6)
    ax.plot([1], [4.40], marker="o", ms=9.5, color=BAD, zorder=6)

    ax.plot([17, 17], [3.95, 2.60], color=BAD, lw=1.4, ls=(0, (4, 3)),
            zorder=2)
    ax.plot([1, 1], [3.50, 2.35], color=BAD, lw=1.4, ls=(0, (4, 3)),
            zorder=2)
    ax.annotate("", xy=(1.45, 2.55), xytext=(17.0, 2.55),
                arrowprops=dict(arrowstyle="-|>", color=BAD, lw=1.7,
                                shrinkA=0.0, shrinkB=0.0), zorder=4)
    ax.text(9.2, 2.95, "drop the carry: 17 - 16 = 1", ha="center",
            va="center", fontsize=10.5, color=BAD, zorder=5)

    ax.text(17.90, 4.72, "true sum: 1 0001 = 17", ha="right", va="center",
            fontsize=10.5, color=HILITE, zorder=5)
    ax.text(1.00, 2.05, "4-bit result: 0001 = 1\nerror: 17 - 1 = 16 = $2^{4}$",
            ha="left", va="top", fontsize=10.5, color=BAD, zorder=5)

    ax.set_xlim(-0.40, 18.40)
    ax.set_ylim(1.30, 4.90)
    ax.set_axis_off()


def main():
    apply_mpl_style()
    fig = plt.figure(figsize=(12.4, 5.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.32, 1.0], wspace=0.10)
    panel_a(fig.add_subplot(gs[0]))
    panel_b(fig.add_subplot(gs[1]))
    save_fig(fig, "binary-addition-carries")


if __name__ == "__main__":
    main()
