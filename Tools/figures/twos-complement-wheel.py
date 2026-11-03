"""twos-complement-wheel — the 16 code words of a 4-bit two's complement number
arranged on a 16-sector wheel.

Walking one sector clockwise adds 1, so "add k" is "turn k sectors".  The wheel
makes three things visible at once: zero has a single spelling, the numbers run
-8 ... +7 (not symmetric), and the step from 0111 (+7) to 1000 (-8) crosses the
sign boundary.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

apply_mpl_style()

import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, FancyArrowPatch

N = 16
STEP = 360.0 / N          # 22.5 deg per sector
R = 1.0
R_CODE = 0.84
R_VAL = 0.54


def value_of(i: int) -> int:
    return i if i < 8 else i - 16


def pol(r: float, deg: float):
    a = math.radians(deg)
    return r * math.cos(a), r * math.sin(a)


fig, ax = plt.subplots(figsize=(9.6, 9.6))
ax.set_aspect('equal')
ax.set_xlim(-2.15, 2.15)
ax.set_ylim(-2.15, 2.15)
ax.axis('off')
ax.set_title("The 4-bit two's complement wheel:  clockwise = +1", pad=14)

for i in range(N):
    mid = 90.0 - i * STEP
    fc = 'white' if i < 8 else FILL
    ax.add_patch(Wedge((0, 0), R, mid - STEP / 2, mid + STEP / 2,
                       fc=fc, ec=MUTED, zorder=2))
    x, y = pol(R_CODE, mid)
    col = HILITE if i == 8 else INK
    ax.text(x, y, format(i, '04b'), ha='center', va='center', rotation=0,
            family='monospace', fontsize=9.5, color=col, zorder=5)
    x, y = pol(R_VAL, mid)
    col = HILITE if i == 8 else (ACCENT if i == 0 else INK)
    ax.text(x, y, str(value_of(i)), ha='center', va='center', fontsize=11.5,
            color=col, zorder=5)

# sign boundary / wrap point: between 0111 (+7) and 1000 (-8)
bx, by = pol(R, 90.0 - 7.5 * STEP)
ax.plot([0, bx], [0, by], color=HILITE, zorder=4)
ax.text(*pol(1.02, 90.0 - 7.5 * STEP), 'sign boundary', ha='center',
        va='center', fontsize=9, color=HILITE, zorder=5)

# the single zero
ax.annotate('0000 = 0 :  the one and only zero', xy=(0.03, 1.02),
            xytext=(0.0, 1.62), ha='center', va='center', fontsize=11.5,
            color=ACCENT, arrowprops=dict(arrowstyle='->', color=ACCENT))

# clockwise rotation cue
ax.add_patch(FancyArrowPatch((-0.24, 0.20), (0.24, 0.20),
                             connectionstyle='arc3,rad=0.62',
                             arrowstyle='-|>', color=INK, mutation_scale=18,
                             zorder=6))

# half labels
ax.text(1.16, 0.66, 'sign bit = 0\n0000 ... 0111\nvalues  0 ... +7',
        ha='left', va='center', fontsize=11, color=INK)
ax.text(-1.16, 0.66, 'sign bit = 1\n1000 ... 1111\nvalues  -8 ... -1',
        ha='right', va='center', fontsize=11, color=INK)

ax.text(0.0, -0.06, 'add k  =  turn k steps', ha='center', va='center',
        fontsize=10.5, color=INK, zorder=6)

# wrap annotation
ax.text(0.46, -1.42, 'wrap point\n0111 (+7) + 1   ->   1000 (-8)',
        ha='left', va='top', fontsize=12, color=HILITE, zorder=6)
ax.annotate('', xy=(0.24, -1.00), xytext=(0.52, -1.40),
            arrowprops=dict(arrowstyle='->', color=HILITE, ls='--'))

ax.text(0.0, -1.98, '16 code words, 16 values:  no code word is wasted, '
                    'and zero is spelled only once',
        ha='center', va='center', fontsize=11, color=GOOD)

save_fig(fig, 'twos-complement-wheel')
