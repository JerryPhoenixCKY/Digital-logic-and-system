"""Figure: why Gray labelling matters for a 4-PSK constellation.

Four transmitted symbols sit on a circle.  Noise can push the received point
into a neighbouring decision region, so the receiver picks a neighbour.

Panel (a): natural binary labelling, 00 01 10 11.  The arcs are labelled with
the Hamming distance of the two labels; one of the four neighbour pairs is
2 bits apart, so that symbol error costs 2 bit errors.

Panel (b): Gray labelling, 00 01 11 10.  Every neighbour pair is exactly 1 bit
apart, so any adjacent-symbol error costs a single bit error (slide p.68:
the symbol error probability is inversely proportional to the symbol
distance, and the Gray order minimises the bit damage of a near miss).

Constellation geometry, so matplotlib.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle

MONO = 'DejaVu Sans Mono'


def hamming(a, b):
    return bin(int(a, 2) ^ int(b, 2)).count('1')


def constellation(ax, labels, title, note, note_color):
    """One 4-PSK constellation; labels = the codes in 45,135,225,315 order."""
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.78, 1.62)
    ax.set_aspect('equal')
    ax.axis('off')

    # I / Q axes
    for xy, txt, tpos in (((1.45, 0), 'I', (1.52, 0.09)),
                          ((0, 1.45), 'Q', (0.09, 1.50))):
        ax.annotate('', xy=xy, xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.2))
        ax.text(tpos[0], tpos[1], txt, ha='center', va='center',
                fontsize=12, color=MUTED)

    ax.add_patch(Circle((0, 0), 1.0, fill=False, edgecolor=MUTED, lw=1.2,
                        ls='--', zorder=1))

    ang = [45.0, 135.0, 225.0, 315.0]
    pts = [(np.cos(np.radians(a)), np.sin(np.radians(a))) for a in ang]

    # arcs between neighbouring symbols, labelled with the Hamming distance
    for i in range(4):
        j = (i + 1) % 4
        d = hamming(labels[i], labels[j])
        col = GOOD if d == 1 else BAD
        t1, t2 = ang[i], ang[j]
        if t2 < t1:                  # the 315 -> 45 pair wraps through 0
            t2 += 360.0
        ax.add_patch(Arc((0, 0), 2.0, 2.0, theta1=t1, theta2=t2,
                         edgecolor=col, lw=3.2, zorder=2))
        mid = np.radians((t1 + t2) / 2.0)
        ax.text(1.20 * np.cos(mid), 1.20 * np.sin(mid), r'$d=%d$' % d,
                ha='center', va='center', fontsize=11.5, color=col, zorder=4)

    # symbols and their code labels
    for (x, y), lab in zip(pts, labels):
        ax.plot([x], [y], 'o', ms=11, color=INK, markerfacecolor=FILL,
                zorder=5)
        ax.text(1.42 * x, 1.42 * y, lab, ha='left' if x > 0 else 'right',
                va='bottom' if y > 0 else 'top', fontsize=13.5, family=MONO,
                color=INK, zorder=5)

    ax.text(0.0, -1.45, note, ha='center', va='center', fontsize=11,
            color=note_color)
    ax.set_title(title)


def build_figure():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 6.9))
    constellation(
        ax1, ['00', '01', '10', '11'],
        '(a) natural binary labelling 00 01 10 11',
        'a neighbouring symbol can be 2 bits away', BAD)
    constellation(
        ax2, ['00', '01', '11', '10'],
        '(b) Gray labelling 00 01 11 10',
        'every neighbouring symbol is 1 bit away', GOOD)
    fig.text(0.5, 0.018,
             'a noise hit that lands on a neighbouring point is decoded as one '
             'symbol error;\n'
             'the arcs give the Hamming distance of the two labels',
             ha='center', va='center', fontsize=10.5, color=INK)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    return fig


def main():
    apply_mpl_style()
    fig = build_figure()
    save_fig(fig, 'gray-code-symbol-mapping')

    # ---- numbers the note quotes -------------------------------------------
    nat = ['00', '01', '10', '11']
    gray = ['00', '01', '11', '10']
    print('check  natural binary neighbour distances: %s (worst %d bits)'
          % ([hamming(nat[i], nat[(i + 1) % 4]) for i in range(4)],
             max(hamming(nat[i], nat[(i + 1) % 4]) for i in range(4))))
    print('check  Gray neighbour distances: %s (worst %d bit)'
          % ([hamming(gray[i], gray[(i + 1) % 4]) for i in range(4)],
             max(hamming(gray[i], gray[(i + 1) % 4]) for i in range(4))))


if __name__ == '__main__':
    main()
