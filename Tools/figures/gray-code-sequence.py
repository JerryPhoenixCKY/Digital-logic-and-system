"""Figure: the 4-bit Gray code sequence and the bit-flip cost of counting.

Panel (a): the 16 Gray code words in sequence.  Every gap is labelled with the
Hamming distance of the two neighbouring words -- all of them are 1, including
the wrap-around from the last word back to the first (that is the "cyclic"
property of the code).

Panel (b): how many bits actually change at each counting step, natural binary
versus Gray.  Natural binary spikes whenever a carry ripples (0111 -> 1000
flips 4 bits at once); Gray stays at exactly 1 for every step.  The inset shows
the reflection rule that builds the code.

Bit strings and a bar chart, so matplotlib.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

MONO = 'DejaVu Sans Mono'

SEQ = [format(i ^ (i >> 1), '04b') for i in range(16)]


def panel_a(ax):
    """The 16 code words, snaking left->right then right->left."""
    ax.set_xlim(-0.1, 18.4)
    ax.set_ylim(3.30, 9.30)
    ax.axis('off')

    bw, bh, pitch, x0 = 1.5, 0.90, 2.1, 1.6
    ytop, ybot = 7.65, 5.25

    for k in range(16):
        if k < 8:                      # row 1: left -> right
            i, y = k, ytop
        else:                          # row 2: right -> left
            i, y = 15 - k, ybot
        x = x0 + i * pitch
        ax.add_patch(Rectangle((x, y - bh / 2), bw, bh, facecolor=FILL,
                               edgecolor=INK, lw=1.4, zorder=2))
        ax.text(x + bw / 2, y, SEQ[k], ha='center', va='center', fontsize=12.5,
                family=MONO, color=INK, zorder=3)
        ax.text(x + bw / 2, y - 0.78, 'k=%d' % k, ha='center', va='center',
                fontsize=9.5, color=MUTED)

    # Hamming distance 1 between neighbours inside each row
    for i in range(7):
        xg = x0 + i * pitch + bw + 0.30
        ax.text(xg, ytop, '1', ha='center', va='center', fontsize=12.5,
                color=GOOD)
        ax.text(xg, ybot, '1', ha='center', va='center', fontsize=12.5,
                color=GOOD)

    # the turn: word k=7 down to word k=8
    xr = x0 + 7 * pitch + bw / 2
    ax.annotate('', xy=(xr, ybot + bh / 2 + 0.05), xytext=(xr, ytop - bh / 2 - 0.05),
                arrowprops=dict(arrowstyle='->', color=GOOD, lw=1.4))
    ax.text(xr + 0.28, (ytop + ybot) / 2, '1', ha='left', va='center',
            fontsize=12.5, color=GOOD)

    # the wrap-around: word k=15 back to word k=0 (cyclic code)
    xl = x0 - 1.05
    ax.annotate('', xy=(xl, ytop), xytext=(xl, ybot),
                arrowprops=dict(arrowstyle='<->', color=GOOD, lw=1.4))
    ax.text(xl + 0.35, 6.45, 'd = 1 as well: the code is cyclic',
            ha='left', va='center', fontsize=10.5, color=GOOD)

    ax.text(0.0, 3.75, 'every gap carries the Hamming distance of its two '
                       'code words -- always 1',
            ha='left', va='center', fontsize=10.5, color=MUTED)

    ax.set_title('(a) 4-bit Gray code: 16 code words, 1 bit per step')


def panel_b(ax):
    """Bits flipped per counting step: natural binary vs Gray."""
    steps = np.arange(15)
    nat = np.array([1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1])
    gray = np.ones(15, dtype=int)

    ax.bar(steps - 0.19, nat, width=0.38, color=ACCENT, label='natural binary')
    ax.bar(steps + 0.19, gray, width=0.38, color=GOOD, label='Gray code')
    ax.set_ylim(0, 9.2)
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.set_xticks(steps)
    ax.set_xlabel(r'counting step  $k \rightarrow k+1$')
    ax.set_ylabel('bits flipped')
    ax.set_title('(b) bits flipped per counting step')

    ax.annotate('binary 0111 -> 1000 flips 4 bits at once',
                xy=(6.81, 4.05), xytext=(0.0, 4.80),
                color=BAD, fontsize=10.5, ha='left', va='center',
                arrowprops=dict(arrowstyle='->', color=BAD, lw=1.4))
    ax.legend(loc='upper right', ncol=1)

    ins = ax.inset_axes([0.02, 0.56, 0.50, 0.41])
    ins.set_facecolor(FILL)
    ins.axis('off')
    ins.text(0.03, 0.96, 'reflection construction', fontsize=10.5, color=INK,
             ha='left', va='top', weight='bold')
    for y, s in ((0.78, 'G1 = 0 1'),
                 (0.61, 'G2 = 00 01 11 10'),
                 (0.44, 'G3 = 000 001 011 010'),
                 (0.29, '     110 111 101 100'),
                 (0.15, 'Gn = 0 + Gn-1'),
                 (0.075, '     1 + reverse(Gn-1)')):
        ins.text(0.03, y, s, fontsize=10, family=MONO, color=INK, ha='left',
                 va='top')
    for s in ins.spines.values():
        s.set_visible(True)
        s.set_color(MUTED)


def build_figure():
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(14.4, 7.0), gridspec_kw={'width_ratios': [1.06, 1.0]})
    panel_a(ax1)
    panel_b(ax2)
    fig.tight_layout()
    return fig


def main():
    apply_mpl_style()
    fig = build_figure()
    save_fig(fig, 'gray-code-sequence')

    # ---- numbers the note quotes -------------------------------------------
    print('check  4-bit Gray sequence: %s' % ' '.join(SEQ))
    d = [bin(int(SEQ[i], 2) ^ int(SEQ[i + 1], 2)).count('1') for i in range(15)]
    print('check  consecutive Hamming distances: %s -> all 1: %s'
          % (d, set(d) == {1}))
    print('check  wrap-around %s -> %s distance: %d'
          % (SEQ[15], SEQ[0], bin(int(SEQ[15], 2) ^ int(SEQ[0], 2)).count('1')))
    nb = [bin(i ^ (i + 1)).count('1') for i in range(15)]
    print('check  natural binary flips per step: %s' % nb)
    print('check  worst step 7->8: %s -> %s flips %d bits'
          % (format(7, '04b'), format(8, '04b'), nb[7]))


if __name__ == '__main__':
    main()
