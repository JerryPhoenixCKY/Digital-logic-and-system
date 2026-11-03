"""sign-magnitude-zero — the 16 code words of a 4-bit sign/magnitude number on
the number line, plus the failed addition (-6) + (+6) = 1 0100.

(a) every code word placed at the decimal value it denotes: the two zeros
    (0000 / 1000) collapse onto one point, 0111 = +7 and 1111 = -7 are the
    range endpoints;
(b) the vertical working of 1110 + 0110, which yields 20 instead of 0.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

apply_mpl_style()

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig = plt.figure(figsize=(11.5, 7.8))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.92], hspace=0.26)
ax = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

BIT_DX = 0.222


def chip(a, x, y, bits, fs=9.0, color=INK, sign_edge=INK):
    """One 4-bit code word drawn as four boxed characters centred at (x, y)."""
    for j, ch in enumerate(bits):
        a.text(x + (j - 1.5) * BIT_DX, y, ch, ha='center', va='center',
               family='monospace', fontsize=fs, color=color,
               bbox=dict(boxstyle='square,pad=0.10', fc=FILL,
                         ec=(sign_edge if j == 0 else MUTED)))


# --------------------------------------------------------------------------
# (a) the 16 code words on the number line
# --------------------------------------------------------------------------
ax.set_title('(a) All 16 code words of a 4-bit sign/magnitude number, '
             'placed at the value they denote')
ax.set_xlim(-8.9, 9.5)
ax.set_ylim(-1.55, 2.15)
ax.axis('off')

# decimal number line
ax.annotate('', xy=(9.0, 0.0), xytext=(-8.9, 0.0),
            arrowprops=dict(arrowstyle='-|>', color=INK))
for v in range(-7, 8):
    ax.plot([v, v], [-0.10, 0.10], color=INK)
    ax.text(v, -0.34, str(v), ha='center', va='top', fontsize=11, color=INK)

# code words: MSB = 0 -> non-negative half, MSB = 1 -> negative half
special = {'0111': HILITE, '1111': HILITE, '0000': ACCENT, '1000': ACCENT}
for i in range(16):
    bits = format(i, '04b')
    if bits[0] == '0':
        val, y = int(bits, 2), 0.34
    else:
        val, y = -int(bits[1:], 2), 0.34
    if bits == '1000':                       # -0 sits above +0
        y = 1.00
    chip(ax, val, y, bits, color=special.get(bits, INK))

# the two code words that both mean "zero"
ax.add_patch(Rectangle((-0.52, 0.12), 1.04, 1.10, fc='none', ec=ACCENT,
                       ls='--'))
ax.text(0.55, 1.62, 'two code words, one value:  0000 (+0)  and  1000 (-0)',
        ha='center', va='center', fontsize=11, color=ACCENT)

# range endpoints
ax.annotate('most negative: 1111 = -7', xy=(-7.0, 0.58), xytext=(-8.85, 1.90),
            ha='left', va='center', fontsize=11, color=HILITE,
            arrowprops=dict(arrowstyle='->', color=HILITE, ls='--'))
ax.annotate('most positive: 0111 = +7', xy=(7.0, 0.58), xytext=(9.45, 1.90),
            ha='right', va='center', fontsize=11, color=HILITE,
            arrowprops=dict(arrowstyle='->', color=HILITE, ls='--'))
ax.text(0.0, -1.34,
        'range of an N-bit sign/magnitude number:  '
        r'$[-(2^{N-1}-1),\ 2^{N-1}-1]$   ->   $[-7,\ +7]$ for $N=4$',
        ha='center', va='center', fontsize=11.5, color=INK)

# --------------------------------------------------------------------------
# (b) the vertical addition that fails
# --------------------------------------------------------------------------
ax2.set_title('(b) Why addition breaks:  $(-6) + (+6)$  in 4-bit sign/magnitude')
ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(-0.16, 1.04)
ax2.axis('off')

XR, XL, XA = 0.29, 0.02, 0.34          # numeric right edge, label, annotation
ROWS = [
    (0.94, 'carry', '1 1 1 1 0', MUTED, 13.0, 'carry-out of the MSB column, discarded'),
    (0.75, '',      '  1 1 1 0', INK, 15.0, '-6  =  1110   (sign bit 1, magnitude 110)'),
    (0.56, '',      '+ 0 1 1 0', INK, 15.0, '+6  =  0110   (sign bit 0, magnitude 110)'),
    (0.37, '',      '---------', INK, 15.0, None),
    (0.18, '',      '1 0 1 0 0', BAD, 15.0, '= 20 decimal, and it is not 0'),
]
for y, lab, num, col, fs, ann in ROWS:
    if lab:
        ax2.text(XL, y, lab, ha='left', va='center', fontsize=12, color=MUTED)
    ax2.text(XR, y, num, ha='right', va='center', family='monospace',
             fontsize=fs, color=col)
    if ann:
        ax2.text(XA, y, ann, ha='left', va='center', fontsize=11.5, color=col)

ax2.text(XL, -0.02,
         'neither the 5-bit value 20 nor its low 4 bits (0100 = +4) is 0   ->   '
         'sign/magnitude addition FAILS',
         ha='left', va='center', fontsize=12, color=BAD)

save_fig(fig, 'sign-magnitude-zero')
