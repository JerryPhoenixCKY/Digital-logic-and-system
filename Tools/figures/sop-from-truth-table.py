"""Figure: truth table -> rows with output 1 -> one minterm each -> OR = SOP.

Uses the lecture example of p.43:  Y = A'B'C + AB'C' + ABC, i.e. the rows
001, 100 and 111 of the 3-variable truth table.  The flow drawn here is the
recipe itself: read the output column, keep the rows where it is 1, write the
minterm of each kept row (unbarred where the input is 1, barred where it is 0),
then OR the minterms together.

A table + boxes + arrows, so matplotlib.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

# the lecture function of p.43: Y = A'B'C + AB'C' + ABC
KEEP = {1: r'$\bar{A}\bar{B}C$', 4: r'$A\bar{B}\bar{C}$', 7: r'$ABC$'}
ROWS = ['000', '001', '010', '011', '100', '101', '110', '111']


def build_figure():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(13.8, 6.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.0, 0.972, "(4-09) Truth table  ->  rows with output 1  ->  one minterm "
                        "each  ->  OR",
            ha='left', va='center', fontsize=15, weight='bold', color=INK)
    ax.text(0.0, 0.928, "lecture example (p.43): the same three minterms make "
                        "$Y = \\bar{A}\\bar{B}C + A\\bar{B}\\bar{C} + ABC = \\sum m(1,4,7)$",
            ha='left', va='center', fontsize=11.5, color=MUTED)

    # ---------------- step 1: the truth table ------------------------------
    xa, xb, xc, xy = 0.055, 0.115, 0.175, 0.258
    ytop, dy = 0.790, 0.068
    ax.text(0.02, 0.885, "step 1  write the truth table", ha='left', va='center',
            fontsize=11.5, color=ACCENT, weight='bold')
    ax.text(xa, 0.840, '$A$', ha='center', va='center', fontsize=12.5, color=INK)
    ax.text(xb, 0.840, '$B$', ha='center', va='center', fontsize=12.5, color=INK)
    ax.text(xc, 0.840, '$C$', ha='center', va='center', fontsize=12.5, color=INK)
    ax.text(xy, 0.840, '$Y$', ha='center', va='center', fontsize=12.5, color=INK)
    ax.plot([0.025, 0.285], [0.822, 0.822], color=INK, lw=1.2)

    for i, row in enumerate(ROWS):
        y = ytop - i * dy
        keep = i in KEEP
        if keep:
            ax.add_patch(Rectangle((0.025, y - 0.030), 0.262, 0.060, facecolor=FILL,
                                   edgecolor='none', zorder=1))
        for x, ch in zip((xa, xb, xc), row):
            ax.text(x, y, ch, ha='center', va='center', fontsize=13, color=INK,
                    family='DejaVu Sans Mono', zorder=3)
        ax.text(xy, y, '1' if keep else '0', ha='center', va='center', fontsize=13,
                color=HILITE if keep else MUTED, weight='bold', zorder=3)
        ax.text(0.300, y, ('row %d' % i) if keep else 'skip', ha='left', va='center',
                fontsize=10.5, color=HILITE if keep else MUTED, zorder=3)

    # ---------------- step 2: one minterm per kept row ---------------------
    ax.text(0.475, 0.885, "step 2  minterm of each 1-row", ha='left', va='center',
            fontsize=11.5, color=ACCENT, weight='bold')
    ax.text(0.475, 0.855, "$0 \\rightarrow$ bar the variable,  $1 \\rightarrow$ "
                          "write it plain", ha='left', va='center', fontsize=10.5,
            color=MUTED)

    ys = []
    for i in sorted(KEEP):
        y = ytop - i * dy
        ys.append(y)
        ax.add_patch(FancyArrowPatch((0.360, y), (0.462, y),
                                     arrowstyle='-|>', mutation_scale=13,
                                     color=HILITE, lw=1.4, zorder=2))
        ax.add_patch(Rectangle((0.470, y - 0.030), 0.180, 0.060, facecolor='white',
                               edgecolor=HILITE, lw=1.3, zorder=2))
        ax.text(0.560, y, KEEP[i], ha='center', va='center', fontsize=13.5,
                color=INK, zorder=3)
        ax.text(0.660, y, '$m_{%d}$' % i, ha='left', va='center', fontsize=12,
                color=ACCENT, zorder=3)

    # plus signs between the boxes: the OR
    for y1, y2 in zip(ys, ys[1:]):
        ax.text(0.560, (y1 + y2) / 2, '+', ha='center', va='center', fontsize=16,
                color=HILITE)

    # ---------------- step 3: OR them into the SOP -------------------------
    ax.text(0.755, 0.885, "step 3  OR the minterms", ha='left', va='center',
            fontsize=11.5, color=ACCENT, weight='bold')
    ax.add_patch(Rectangle((0.745, 0.470), 0.252, 0.200, facecolor=FILL,
                           edgecolor=MUTED, lw=1.2, zorder=2))
    ax.text(0.871, 0.615, '$Y = \\bar{A}\\bar{B}C + A\\bar{B}\\bar{C} + ABC$',
            ha='center', va='center', fontsize=13.5, color=INK, zorder=3)
    ax.text(0.871, 0.545, '$= \\sum m(1,\\,4,\\,7)$', ha='center', va='center',
            fontsize=13.5, color=GOOD, zorder=3)
    ax.text(0.745, 0.425, "$\\sum$ just means \"OR of the listed minterms\";",
            ha='left', va='center', fontsize=10.5, color=MUTED)
    ax.text(0.745, 0.385, "any Boolean function can be written this way.",
            ha='left', va='center', fontsize=10.5, color=MUTED)

    ax.add_patch(FancyArrowPatch((0.680, ys[1]), (0.735, 0.570),
                                 arrowstyle='-|>', mutation_scale=13, color=ACCENT,
                                 lw=1.4, zorder=2,
                                 connectionstyle='arc3,rad=-0.25'))

    ax.plot([0.0, 1.0], [0.255, 0.255], color=MUTED, lw=1.0)
    ax.text(0.0, 0.205, "check: all 8 rows of $(A,B,C)$ enumerated -- this SOP gives "
                        "exactly the $Y$ column above, so $\\sum m(1,4,7)$ is correct (OK).",
            ha='left', va='center', fontsize=11.5, color=INK)
    ax.text(0.0, 0.150, "the rows with $Y = 0$ are simply left out: the missing minterms "
                        "are the ones that would make $Y$ 1 in those rows.",
            ha='left', va='center', fontsize=11, color=MUTED)
    ax.text(0.0, 0.095, "the other direction (standard POS from the 0-rows) is figure "
                        "pos-from-truth-table.", ha='left', va='center', fontsize=11,
            color=MUTED)
    return fig


def main():
    fig = build_figure()
    save_fig(fig, 'sop-from-truth-table')

    # ---- numbers the note quotes -------------------------------------------
    import itertools
    def mterm(i, row):
        return int(all(b == ((i >> (2 - k)) & 1) for k, b in enumerate(row)))

    rows = list(itertools.product([0, 1], repeat=3))
    y = [int(any(mterm(i, r) for i in KEEP)) for r in rows]
    print('check  Y column            :', y)
    print('check  Y = 1 exactly in rows:', [i for i, v in enumerate(y) if v])
    print('check  sum m(1,4,7) enumerated over 8 rows matches the table: %s'
          % (y == [1 if i in KEEP else 0 for i in range(8)]))
    excl = [i for i in range(8) if i not in KEEP]
    print('check  rows with Y = 0 (left out):', excl)


if __name__ == '__main__':
    main()
