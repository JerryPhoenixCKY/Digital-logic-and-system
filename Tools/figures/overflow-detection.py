"""overflow-detection — where an 8-bit two's complement addition overflows.

(a) the 8-bit number line [-128, +127]: a legal addition ((-5) + (-9) = -14)
    stays inside the range, while (-125) + (-58) = -183 leaves it and wraps
    back to an apparent 0100 1001 = +73;
(b) the lecture p.43 example worked column by column: 1000 0011 + 1100 0110
    = 1 0100 1001, where both addends are negative but the result's sign bit
    is 0 -- the criterion "same sign in, opposite sign out".
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

apply_mpl_style()

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

N = 8
LO, HI = -(1 << (N - 1)), (1 << (N - 1)) - 1        # -128 .. +127

fig = plt.figure(figsize=(11.5, 8.6))
gs = fig.add_gridspec(2, 1, height_ratios=[1.05, 1.0], hspace=0.30)
ax = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# --------------------------------------------------------------------------
# (a) the 8-bit number line
# --------------------------------------------------------------------------
ax.set_title('(a) 8-bit two\'s complement number line  '
             r'$[-2^{N-1},\ 2^{N-1}-1] = [-128,\ +127]$')
ax.set_xlim(-218, 172)
ax.set_ylim(-2.25, 1.55)
ax.axis('off')

X0, X1 = -212, 164
ax.annotate('', xy=(X1, 0.0), xytext=(X0, 0.0),
            arrowprops=dict(arrowstyle='-|>', color=INK))
ax.add_patch(Rectangle((LO, -0.15), HI - LO, 0.30, fc=FILL, ec=INK, zorder=3))
for v in (-128, -64, 0, 64, 127):
    ax.plot([v, v], [-0.24, -0.32], color=INK, zorder=4)
    ax.text(v, -0.36, str(v), ha='center', va='top', fontsize=10, color=INK)
ax.text(0.0, 0.0, r'$[-2^{N-1},\ 2^{N-1}-1]$', ha='center', va='center',
        fontsize=12, color=INK, zorder=6)
ax.text(LO, 0.30, r'$-2^{N-1} = -128$   (range limit)', ha='center',
        va='bottom', fontsize=10.5, color=INK)
ax.text(HI, 0.30, r'$+127$   (max)', ha='center', va='bottom', fontsize=10.5,
        color=INK)

# legal addition: (-5) + (-9) = -14
ax.add_patch(FancyArrowPatch((-5, 0.72), (-14, 0.72), arrowstyle='<|-|>',
                             color=GOOD, mutation_scale=16))
ax.text(-15.5, 1.00, r'$(-5)+(-9)=-14$   stays inside the range',
        ha='left', va='center', fontsize=11.5, color=GOOD)

# overflowing addition: (-125) + (-58) = -183
ax.add_patch(FancyArrowPatch((-125, -0.72), (-183, -0.72), arrowstyle='<|-|>',
                             color=BAD, mutation_scale=16))
ax.text(-184, -1.00, r'$(-125)+(-58)=-183$   left of -128  ->  out of range',
        ha='left', va='center', fontsize=11.5, color=BAD)
ax.plot([LO, LO], [-1.35, 0.26], color=MUTED, ls='--')

# the apparent (wrapped) result
ax.plot([73, 73], [-1.35, -0.30], color=BAD, ls='--')
ax.text(73, -1.00, 'apparent result\n' + r'$0100\ 1001_2 = +73$',
        ha='center', va='center', fontsize=11, color=BAD)
ax.add_patch(FancyArrowPatch((-183, -1.58), (73, -1.58), arrowstyle='-|>',
                             color=HILITE, ls='--',
                             connectionstyle='arc3,rad=-0.10'))
ax.text(-55, -2.00, r'mod $2^{8}$ wrap:  $-183+256=+73$', ha='center',
        va='center', fontsize=11, color=HILITE)

# --------------------------------------------------------------------------
# (b) the lecture p.43 example, column by column
# --------------------------------------------------------------------------
ax2.set_title('(b) Lecture p.43:  1000 0011 + 1100 0110 = 1 0100 1001  '
              '(both addends negative)')
ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(0.0, 1.06)
ax2.axis('off')

DX, X0C, Y0, DY = 0.0525, 0.150, 0.92, 0.190
COLLAB = ['cout', '7', '6', '5', '4', '3', '2', '1', '0']
ROWS = [
    ('carry',   '100001110', {0: ACCENT}, MUTED,
     'carry-out of bit 7, simply discarded'),
    (r'$-125$', ' 10000011', {1: HILITE}, INK,
     r'$1000\ 0011$   sign bit = 1'),
    (r'$-58$',  ' 11000110', {1: HILITE}, INK,
     r'$1100\ 0110$   sign bit = 1'),
    ('sum',     '101001001', {0: BAD, 1: BAD}, BAD,
     r'$0100\ 1001$   sign bit = 0  ->  reads as $+73$'),
]


def cells(y, bits, marks, txtcol):
    for j, ch in enumerate(bits):
        if ch == ' ':
            continue
        fc, ec, tc = (FILL, INK, txtcol) if ch == '1' else ('white', MUTED, MUTED)
        if j in marks:
            ec, tc = marks[j], marks[j]
        ax2.text(X0C + j * DX, y, ch, ha='center', va='center',
                 family='monospace', fontsize=11, color=tc, zorder=5,
                 bbox=dict(boxstyle='square,pad=0.12', fc=fc, ec=ec))


for j, lab in enumerate(COLLAB):
    ax2.text(X0C + j * DX, Y0 + 0.09, lab, ha='center', va='bottom',
             fontsize=9, color=MUTED)

for i, (lab, bits, marks, col, ann) in enumerate(ROWS):
    y = Y0 - i * DY
    ax2.text(X0C - 0.055, y, lab, ha='right', va='center', fontsize=11.5,
             color=INK)
    cells(y, bits, marks, col)
    ax2.text(X0C + 9 * DX + 0.015, y, ann, ha='left', va='center',
             fontsize=10.5, color=col)

ax2.annotate('the sign bit of the sum flipped to 0',
             xy=(X0C + 1 * DX, Y0 - 3 * DY - 0.085),
             xytext=(X0C + 1.3 * DX, Y0 - 3.95 * DY), ha='left', va='center',
             fontsize=11, color=BAD,
             arrowprops=dict(arrowstyle='->', color=BAD, ls='--'))
ax2.text(0.0, 0.04,
         'criterion:  the two addends have the SAME sign but the sum has the '
         'opposite sign  ->  overflow',
         ha='left', va='center', fontsize=12, color=BAD)

save_fig(fig, 'overflow-detection')
