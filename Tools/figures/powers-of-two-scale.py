"""N07 Bits and Bytes -- the powers-of-two scale.

A log10 ruler carrying 2^10 .. 2^60 with their prefix names, their exact decimal
values and the IEC prefix of each step, plus the two estimates the lecture asks
for (p.26): 2^24 ~ 16 M and 2^32 ~ 4 G.

Verified numbers (verify_ch2.txt):
    2^10 = 1,024            2^20 = 1,048,576         2^30 = 1,073,741,824
    2^40 = 1,099,511,627,776   2^50 = 1,125,899,906,842,624
    2^60 = 1,152,921,504,606,846,976
    2^24 = 16,777,216      2^32 = 4,294,967,296     2^32-1 = 4,294,967,295

Run:  D:\\anaconda\\python.exe Tools\\figures\\powers-of-two-scale.py
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt

LOG2 = math.log10(2.0)

# (exponent, prefix name, IEC prefix)
STEPS = [(10, "kilo", "KiB"), (20, "mega", "MiB"), (30, "giga", "GiB"),
         (40, "tera", "TiB"), (50, "peta", "PiB"), (60, "exa", "EiB")]


def main():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(13.0, 5.8))

    ax.set_title("Powers of two on a log scale: 2$^{10}$ .. 2$^{60}$, "
                 "and the two estimates worth memorising",
                 loc="left", fontsize=13.5, pad=12)

    # ---- the ruler ------------------------------------------------------
    ax.plot([2.60, 19.40], [0, 0], color=INK, lw=2.4, solid_capstyle="round",
            zorder=3)
    for k, name, iec in STEPS:
        x = k * LOG2
        ax.plot([x, x], [-0.13, 0.13], color=INK, lw=2.0, zorder=4)
        ax.plot([x], [0], marker="o", ms=6.5, color=INK, zorder=5)
        ax.text(x, 0.34, "$2^{%d}$" % k, ha="center", va="center",
                fontsize=12.5, color=INK, fontweight="bold", zorder=5)
        ax.text(x, 0.74, "%s  $\\approx 10^{%d}$" % (name, k // 10 * 3),
                ha="center", va="center", fontsize=10.5, color=ACCENT,
                zorder=5)
        ax.text(x, -0.45, "{:,}".format(2 ** k), ha="center", va="center",
                fontsize=8.6, color=INK, zorder=5)
        ax.text(x, -0.95, "= 1 %s" % iec, ha="center", va="center",
                fontsize=10.0, color=ACCENT, zorder=5)

    # ---- the two estimates (p.26) ---------------------------------------
    for k, ytxt, txt in (
        (24, -1.85,
         "$2^{24} = 16\\times 2^{20}\\approx 16$ M $= 16,777,216$ (16 MiB)"),
        (32, -2.80,
         "$2^{32} = 4\\times 2^{30}\\approx 4$ G $= 4,294,967,296$ (4 GiB)"),
    ):
        x = k * LOG2
        ax.plot([x], [0], marker="v", ms=9.0, color=HILITE, zorder=6)
        ax.plot([x, x], [-0.05, ytxt + 0.20], color=HILITE, lw=1.4,
                ls=(0, (4, 3)), zorder=2)
        ax.text(x, ytxt, txt, ha="center", va="center", fontsize=10.5,
                color=HILITE, zorder=6)

    ax.text(19.40, -1.80,
            "32-bit unsigned integer: max $= 2^{32}-1 = 4,294,967,295$",
            ha="right", va="center", fontsize=10.0, color=INK, zorder=6)
    ax.text(19.40, -2.25,
            "32-bit address space: $4$ GiB $= 4\\times 2^{30}$ bytes",
            ha="right", va="center", fontsize=10.0, color=INK, zorder=6)

    # ---- the 1024 vs 1000 caveat ----------------------------------------
    ax.text(2.62, 1.16,
            "IEC prefixes step by 1024 ($2^{10}$), SI prefixes step by 1000 "
            "($10^{3}$) -- so a '1 TB' drive holds only 0.909 TiB",
            ha="left", va="center", fontsize=10.0, color=INK, zorder=6)

    # ---- decade ruler ---------------------------------------------------
    ax.set_xlim(2.50, 19.70)
    ax.set_ylim(-3.30, 1.45)
    ax.set_xticks([3, 6, 9, 12, 15, 18])
    ax.set_xticklabels(["$10^{3}$", "$10^{6}$", "$10^{9}$", "$10^{12}$",
                        "$10^{15}$", "$10^{18}$"])
    ax.set_yticks([])
    ax.set_xlabel("magnitude on a log scale (every 10x step has the same "
                  "width)")
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", color=MUTED, alpha=0.35, lw=0.9)

    save_fig(fig, "powers-of-two-scale")


if __name__ == "__main__":
    main()
