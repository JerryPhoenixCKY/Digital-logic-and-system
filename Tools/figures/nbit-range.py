"""nbit-range - the three 4-bit number representations, one number line each:
unsigned [0, 15], sign/magnitude [-7, +7] (with its two zeros) and two's
complement [-8, +7] (with its one extra negative code word).

All three panels share one horizontal scale so the ranges, the tick counts and
the code-word counts can be compared directly.  Only the code words that carry
the story are drawn as bit chips: the two ends of each range, the duplicate
zero of sign/magnitude, and the spare code word 1000 of two's complement.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

apply_mpl_style()

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, axes = plt.subplots(3, 1, figsize=(11.0, 8.4))
fig.subplots_adjust(hspace=0.62)

XLO, XHI = -10.5, 17.5
BAR_H = 0.30
BIT_DX = 0.32               # wide enough that the four bit boxes stay separate


def panel(ax, title):
    ax.set_title(title, loc='left')
    ax.set_xlim(XLO, XHI)
    ax.set_ylim(-1.30, 1.30)
    ax.axis('off')
    ax.annotate('', xy=(XHI - 0.4, 0.0), xytext=(XLO + 0.2, 0.0),
                arrowprops=dict(arrowstyle='-|>', color=INK))


def bar(ax, lo, hi, fc=FILL, ec=INK):
    ax.add_patch(Rectangle((lo, -BAR_H / 2), hi - lo, BAR_H,
                           fc=fc, ec=ec, zorder=3))


def ticks(ax, lo, hi):
    for v in range(lo, hi + 1):
        ax.plot([v, v], [-BAR_H / 2 - 0.03, -BAR_H / 2 - 0.13], color=INK,
                zorder=4)
        ax.text(v, -BAR_H / 2 - 0.17, str(v), ha='center', va='top',
                fontsize=9.5, color=INK)


def codeword(ax, x, y, bits, color=INK, fs=8.5):
    for j, ch in enumerate(bits):
        ax.text(x + (j - 1.5) * BIT_DX, y, ch, ha='center', va='center',
                family='monospace', fontsize=fs, color=color, zorder=6,
                bbox=dict(boxstyle='square,pad=0.09', fc=FILL, ec=MUTED))


# --------------------------------------------------------------------------
# (a) unsigned
# --------------------------------------------------------------------------
ax = axes[0]
panel(ax, '(a) unsigned  -  every one of the 16 code words is used')
bar(ax, 0, 15)
ticks(ax, 0, 15)
codeword(ax, 0.0, 0.62, '0000')
codeword(ax, 15.0, 0.62, '1111')
ax.text(7.5, 0.0, r'$[0,\ 2^{N}-1] = [0,\ 15]$', ha='center', va='center',
        fontsize=11.5, color=INK, zorder=6)
ax.text(XLO + 0.4, -0.82,
        '16 code words  ->  16 distinct values:  no code word is wasted, '
        'and zero has exactly one spelling',
        ha='left', va='center', fontsize=11, color=GOOD)

# --------------------------------------------------------------------------
# (b) sign/magnitude
# --------------------------------------------------------------------------
ax = axes[1]
panel(ax, '(b) sign/magnitude  -  16 code words but only 15 values')
bar(ax, -7, 7)
ticks(ax, -7, 7)
codeword(ax, 0.0, 0.62, '0000', color=ACCENT)
codeword(ax, 0.0, 1.00, '1000', color=ACCENT)
ax.add_patch(Rectangle((-0.62, 0.40), 1.24, 0.82, fc='none', ec=ACCENT,
                       ls='--', zorder=5))
ax.text(0.95, 1.00, 'two spellings of zero:  0000 (+0)  and  1000 (-0)',
        ha='left', va='center', fontsize=10.5, color=ACCENT)
codeword(ax, -7.0, 0.62, '1111', color=HILITE)
codeword(ax, 7.0, 0.62, '0111', color=HILITE)
ax.text(0.0, 0.0, r'$[-(2^{N-1}-1),\ 2^{N-1}-1] = [-7,\ +7]$',
        ha='center', va='center', fontsize=11.5, color=INK, zorder=6)
ax.text(XLO + 0.4, -0.82,
        '16 code words  ->  15 values:  one is spent on the duplicate zero, '
        'and the negative half stops at -7',
        ha='left', va='center', fontsize=11, color=BAD)

# --------------------------------------------------------------------------
# (c) two's complement
# --------------------------------------------------------------------------
ax = axes[2]
panel(ax, "(c) two's complement  -  16 code words, 16 values, but asymmetric")
bar(ax, -8, 7)
ax.add_patch(Rectangle((-8, -BAR_H / 2), 1.0, BAR_H, fc=HILITE, ec=HILITE,
                       zorder=4))
ticks(ax, -8, 7)
codeword(ax, -8.0, 0.62, '1000', color=HILITE)
codeword(ax, 7.0, 0.62, '0111', color=HILITE)
ax.text(7.9, 0.62, 'no +8 to pair with -8', ha='left', va='center',
        fontsize=10.5, color=HILITE)
ax.text(-2.5, 0.0, r'$[-2^{N-1},\ 2^{N-1}-1] = [-8,\ +7]$', ha='center',
        va='center', fontsize=11.5, color=INK, zorder=6)
ax.annotate('the spare code word is -8',
            xy=(-7.10, 0.28), xytext=(-6.4, 1.02), ha='center', va='center',
            fontsize=10.5, color=HILITE, zorder=6,
            arrowprops=dict(arrowstyle='->', color=HILITE, ls='--'))
ax.text(XLO + 0.4, -0.82,
        '16 code words  ->  16 values:  zero is spelled once, so the spare '
        'code word becomes -8',
        ha='left', va='center', fontsize=11, color=GOOD)

save_fig(fig, 'nbit-range')
