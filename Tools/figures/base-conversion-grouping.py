"""N06 Number Base Conversion -- "grouping IS conversion".

(a) one 16-bit string (1100 1010 0101 0111) read twice: in 4-bit groups -> hex
    and in 3-bit groups -> octal, both taken from the RIGHT (LSB) leftwards;
(b) a short leftmost group must be padded with leading zeros.

Numbers are the verified ones (verify_ch2.txt):
    1100 1010 0101 0111 (base 2) = CA57 (base 16) = 145127 (base 8) = 51799

Run:  D:\\anaconda\\python.exe Tools\\figures\\base-conversion-grouping.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BITS = "1100101001010111"          # 16 bits, index 0 = MSB (bit 15)


def cell(ax, x, y, text="", w=1.0, h=1.0, fc=FILL, ec=INK, tc=INK,
         fs=15.0, ls="-", lw=1.6, z=3):
    """One bit cell: FILL box + INK border, digit centred inside."""
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                           linewidth=lw, linestyle=ls, zorder=z))
    if text:
        ax.text(x + w / 2.0, y + h / 2.0, text, ha="center", va="center",
                color=tc, fontsize=fs, zorder=z + 1)


def group(ax, xa, xb, y, h, digit, color, fs=17.0):
    """A grouping box spanning [xa, xb] with the digit of that group inside."""
    ax.add_patch(Rectangle((xa + 0.06, y), xb - xa - 0.12, h,
                           facecolor="none", edgecolor=color,
                           linewidth=2.0, zorder=4))
    ax.text((xa + xb) / 2.0, y + h / 2.0, digit, ha="center", va="center",
            color=color, fontsize=fs, zorder=5)


def tick(ax, x, y0, y1):
    ax.plot([x, x], [y0, y1], color=MUTED, lw=1.0, ls=(0, (3, 2)), zorder=1)


def panel_a(ax):
    """Same string, two groupings."""
    ax.set_title("(a) Grouping is conversion: one 16-bit string, two readings",
                 loc="left", fontsize=12.5, pad=10)
    ax.text(8.0, 10.55, "group first, then convert -- always starting at the "
                        "right (LSB) and moving left",
            ha="center", va="center", fontsize=10.0, color=MUTED,
            style="italic")
    ax.annotate("", xy=(0.15, 9.95), xytext=(15.85, 9.95),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3,
                                shrinkA=0.0, shrinkB=0.0))

    # ---------------- hex block: 4-bit groups ----------------
    for i, ch in enumerate(BITS):
        cell(ax, i, 8.1, ch, fs=15.0)
        ax.text(i + 0.5, 9.35, str(15 - i), ha="center", va="center",
                fontsize=8.0, color=MUTED)
    for g in range(4):
        seg = BITS[4 * g:4 * g + 4]
        group(ax, 4 * g, 4 * g + 4, 6.66, 0.88, format(int(seg, 2), "X"),
              ACCENT)
    for x in (4, 8, 12):
        tick(ax, x, 7.60, 8.10)
    ax.text(-0.35, 7.10, "4-bit groups", ha="right", va="center",
            fontsize=10.5, color=ACCENT)
    ax.text(8.0, 5.95, "(1100)(1010)(0101)(0111)  ->  C A 5 7  ->  (CA57)$_{16}$",
            ha="center", va="center", fontsize=10.5, color=ACCENT)

    # ---------------- octal block: 3-bit groups ----------------
    for k in (-2, -1):                       # two invented leading zeros
        cell(ax, k, 4.3, "0", fc="white", ec=HILITE, tc=HILITE, fs=15.0,
             ls=(0, (3, 2)), lw=1.4)
    for i, ch in enumerate(BITS):
        cell(ax, i, 4.3, ch, fs=15.0)
        ax.text(i + 0.5, 5.55, str(15 - i), ha="center", va="center",
                fontsize=8.0, color=MUTED)
    spans = [(-2, 1), (1, 4), (4, 7), (7, 10), (10, 13), (13, 16)]
    for (xa, xb), d in zip(spans, "145127"):
        group(ax, xa, xb, 2.86, 0.88, d, HILITE)
    for x in (1, 4, 7, 10, 13):
        tick(ax, x, 3.80, 4.30)
    ax.text(-2.35, 3.30, "3-bit groups", ha="right", va="center",
            fontsize=10.5, color=HILITE)
    ax.text(-0.08, 3.98, "pad 0", ha="right", va="center", fontsize=9.0,
            color=HILITE)
    ax.text(8.0, 2.15, "(001)(100)(101)(001)(010)(111)  ->  1 4 5 1 2 7  "
                       "->  (145127)$_8$",
            ha="center", va="center", fontsize=10.5, color=HILITE)

    ax.set_xlim(-4.8, 16.6)
    ax.set_ylim(1.40, 10.95)
    ax.set_axis_off()


def panel_b(ax):
    """A short leftmost group gets leading zeros."""
    bits = "11010110"                        # 8 bits
    ax.set_title("(b) Leftover group: pad it with leading 0s",
                 loc="left", fontsize=12.5, pad=10)

    cell(ax, -1, 5.30, "0", fc="white", ec=HILITE, tc=HILITE, fs=15.0,
         ls=(0, (3, 2)), lw=1.4)
    for i, ch in enumerate(bits):
        cell(ax, i, 5.30, ch, fs=15.0)
        ax.text(i + 0.5, 6.62, str(7 - i), ha="center", va="center",
                fontsize=8.0, color=MUTED)

    for g in range(2):                       # 4-bit groups: no padding needed
        group(ax, 4 * g, 4 * g + 4, 3.90, 0.88,
              format(int(bits[4 * g:4 * g + 4], 2), "X"), ACCENT)
    ax.text(-1.20, 4.34, "hex", ha="right", va="center", fontsize=10.5,
            color=ACCENT)
    ax.text(3.5, 3.15, "1101 0110  ->  D 6  ->  (D6)$_{16}$",
            ha="center", va="center", fontsize=10.0, color=ACCENT)

    for g in range(3):                       # 3-bit groups: left one padded
        xa = -1 + 3 * g
        group(ax, xa, xa + 3, 1.50, 0.88, format(int(
            ("0" + bits)[g * 3:g * 3 + 3], 2), "o"), HILITE)
    ax.text(-1.20, 1.94, "octal", ha="right", va="center", fontsize=10.5,
            color=HILITE)
    ax.text(3.5, 0.78, "011 010 110  ->  3 2 6  ->  (326)$_8$",
            ha="center", va="center", fontsize=10.0, color=HILITE)
    ax.text(-0.08, 4.95, "pad 0", ha="right", va="center", fontsize=9.0,
            color=HILITE)

    ax.set_xlim(-1.75, 8.75)
    ax.set_ylim(0.35, 7.10)
    ax.set_aspect("equal")
    ax.set_anchor("W")
    ax.set_axis_off()


def main():
    apply_mpl_style()
    fig = plt.figure(figsize=(12.0, 7.8))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.9, 1.0], hspace=0.10)
    panel_a(fig.add_subplot(gs[0]))
    panel_b(fig.add_subplot(gs[1]))
    save_fig(fig, "base-conversion-grouping")


if __name__ == "__main__":
    main()
