"""positional-weights.svg -- positional weights in base 10 and base 2.

(a) (568.23)_10 : one bar per position, bar top = the weight 10^i of that position.
(b) (10.101)_2  : the same picture in base 2; the fractional weights 2^-1..2^-3
                  (0.5 / 0.25 / 0.125) are highlighted.

An "on" position (non-zero digit) is painted, an "off" position (digit 0) is an
empty dashed slot: the digit x weight product is written above every bar.
Used by Notes/Number Systems.md and Notes/Decimal Number System.md.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt

apply_mpl_style()

BOT = 0.001          # bottom of every bar (a log axis needs a positive base)
YLIM = (0.0008, 3000)
YTICKS = [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000]   # fixed decade ticks: every label
                                                # stays inside the canvas


def panel(ax, digits, weights, split, radix_name, box, title, base):
    """One weight ladder.  split = index of the first fractional position."""
    xs = list(range(len(digits)))
    for x, w, dg in zip(xs, weights, digits):
        if dg == "0":
            ax.bar([x], [w - BOT], width=0.62, bottom=BOT, color="white",
                   edgecolor=MUTED, linestyle="--", zorder=3)
        else:
            face = ACCENT if x < split else HILITE
            ax.bar([x], [w - BOT], width=0.62, bottom=BOT, color=face,
                   edgecolor=INK, zorder=3)
        ax.text(x, BOT * 1.75, dg, ha="center", va="bottom", fontsize=13,
                fontweight="bold", zorder=4,
                color=MUTED if dg == "0" else "white")
        val = int(dg) * w
        txt = f"${dg}\\times{base}^{{{x - split}}}$"
        txt += f" $= {('%g' % val)}$"
        ax.text(x, w * 1.45, txt, ha="center", va="bottom", fontsize=9,
                color=MUTED if dg == "0" else INK, zorder=4)

    ax.axvline(split - 0.5, color=MUTED, linestyle="--", zorder=2)
    ax.text(split - 0.5, 1.012, radix_name, transform=ax.get_xaxis_transform(),
            ha="center", va="bottom", fontsize=9, color=MUTED)

    ax.set_xticks(xs)
    ax.set_xticklabels([f"${base}^{{{x - split}}}$" for x in xs], fontsize=11)
    ax.set_xlim(-0.7, len(digits) - 0.3)
    ax.set_yscale("log")
    ax.set_ylim(*YLIM)
    ax.set_yticks(YTICKS)          # fixed locator: no out-of-range tick labels
    ax.set_ylabel("positional weight (log scale)", fontsize=11)
    ax.set_title(title, pad=20)
    ax.text(0.98, 0.965, box, transform=ax.transAxes, ha="right", va="top",
            fontsize=10, linespacing=1.6,
            bbox=dict(boxstyle="round,pad=0.45", facecolor=FILL,
                      edgecolor=MUTED))


fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.4))

panel(
    axes[0],
    digits=["5", "6", "8", "2", "3"],
    weights=[100.0, 10.0, 1.0, 0.1, 0.01],
    split=3,
    radix_name="decimal point",
    base=10,
    title="(a) $(568.23)_{10}$: every position carries a weight",
    box=("$5\\times10^{2}+6\\times10^{1}+8\\times10^{0}+2\\times10^{-1}+3\\times10^{-2}$\n"
         "$=500+60+8+0.2+0.03=(568.23)_{10}$"),
)

panel(
    axes[1],
    digits=["1", "0", "1", "0", "1"],
    weights=[2.0, 1.0, 0.5, 0.25, 0.125],
    split=2,
    radix_name="binary point",
    base=2,
    title="(b) $(10.101)_{2}$: the same ladder, halved per step",
    box=("$1\\times2^{1}+0\\times2^{0}+1\\times2^{-1}+0\\times2^{-2}+1\\times2^{-3}$\n"
         "$=2+0+0.5+0+0.125=(2.625)_{10}$"),
)

fig.tight_layout()
save_fig(fig, "positional-weights")
