"""signed-multiplication-partial-products — the staircase of partial products
for 59 x 83.

59 = 11 1011 (6 bits), 83 = 101 0011 (7 bits), 59 x 83 = 4897 = 1 0011 0010 0001.
Every 1 in the multiplier contributes one shifted copy of 83; the shift is the
weight of that bit.  The last block turns +4897 into its 14-bit two's complement
form 10 1100 1101 1111, i.e. -4897.

The grid is 14 bits wide so that both the 13-bit product and its 14-bit
two's complement form fit in the same columns.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

apply_mpl_style()

import matplotlib.pyplot as plt

W = 14                      # bits per row: bit 13 (left) ... bit 0 (right)


def b14(v: int) -> str:
    return format(v & 0x3FFF, '0%db' % W)


fig, ax = plt.subplots(figsize=(12.0, 8.8))
fig.subplots_adjust(left=0.012, right=0.988, top=0.925, bottom=0.015)
ax.set_xlim(0.0, 1.0)
ax.set_ylim(0.0, 1.0)
ax.axis('off')
ax.set_title('Partial products for  $59 \\times 83$  '
             r'($59 = 11\,1011_2$,  $83 = 101\,0011_2$)', pad=12)

X0, DX, GAP = 0.225, 0.0300, 0.022
BOUND = {4, 8, 12}          # extra space between 4-bit groups
XL, XR = 0.215, 0.705       # left label column / right annotation column
Y0, DY = 0.945, 0.0705


def xcol(j: int) -> float:
    return X0 + j * DX + GAP * len([b for b in BOUND if b <= j])


def row(i: float) -> float:
    return Y0 - i * DY


def bitrow(y, bits, ec1=INK, tc1=INK, fc1=FILL, ec0=MUTED, tc0=MUTED):
    for j, ch in enumerate(bits):
        if ch == ' ':
            continue
        if ch == '1':
            fc, ec, tc = fc1, ec1, tc1
        else:
            fc, ec, tc = 'white', ec0, tc0
        ax.text(xcol(j), y, ch, ha='center', va='center', family='monospace',
                fontsize=11, color=tc, zorder=5,
                bbox=dict(boxstyle='square,pad=0.12', fc=fc, ec=ec))


def label(y, txt, color=INK, fs=11.5):
    ax.text(XL, y, txt, ha='right', va='center', fontsize=fs, color=color)


def note(y, txt, color=INK, fs=10.5):
    ax.text(XR, y, txt, ha='left', va='center', fontsize=fs, color=color)


# column weights -----------------------------------------------------------
for j in range(W):
    ax.text(xcol(j), row(0) + 0.030, str(W - 1 - j), ha='center', va='bottom',
            fontsize=8.5, color=MUTED)
label(row(0) + 0.030, 'bit', color=MUTED, fs=8.5)

# multiplier ---------------------------------------------------------------
label(row(1), r'multiplier $59$')
bitrow(row(1), b14(59), ec1=ACCENT, tc1=ACCENT)
note(row(1), r'$59 = 11\,1011_2$')

# partial products, heaviest weight first ----------------------------------
PPS = [(5, 2656), (4, 1328), (3, 664), (2, None), (1, 166), (0, 83)]
for k, (shift, val) in enumerate(PPS):
    y = row(2 + k)
    label(y, r'$83 \times 2^{%d}$' % shift)
    if val is None:
        ax.text(X0 + 0.030, y, 'multiplier bit = 0  ->  no partial product',
                ha='left', va='center', fontsize=10.5, color=MUTED,
                style='italic')
        continue
    bitrow(y, b14(83 << shift))
    note(y, r'$= %d$' % val)

# the sum ------------------------------------------------------------------
YS = row(2 + len(PPS))
ax.plot([X0 - 0.010, xcol(W - 1) + 0.012], [YS + 0.030, YS + 0.030],
        color=INK)
label(YS, 'sum', color=GOOD)
bitrow(YS, b14(4897), ec1=GOOD, tc1=GOOD)
note(YS, r'$= 4897_{10} = 1\,0011\,0010\,0001_2$', color=GOOD)

# sign handling: put the product into 14-bit two's complement --------------
label(row(9), "two's complement", color=HILITE)
steps = [
    (row(10), r'$+4897$', b14(4897), 'the product, padded to 14 bits'),
    (row(11), 'invert', b14(~4897), 'invert all 14 bits'),
    (row(12), r'$+1$', b14(-4897), r'add 1  ->  $-4897$'),
]
for i, (y, lab, bits, ann) in enumerate(steps):
    last = (i == len(steps) - 1)
    label(y, lab)
    bitrow(y, bits, ec1=HILITE if last else INK,
           tc1=HILITE if last else INK)
    note(y, ann, color=HILITE if last else INK)

ax.text(0.0, 0.030,
        r'check:  $-4897$ needs 14 bits:  $10\,1100\,1101\,1111_2$,  and the '
        r'14-bit two\'s complement range $[-8192,\ +8191]$ holds it',
        ha='left', va='center', fontsize=11, color=HILITE)

save_fig(fig, 'signed-multiplication-partial-products')
