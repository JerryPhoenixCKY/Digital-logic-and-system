"""Figure: truth table -> rows with output 0 -> one maxterm each -> AND = POS.

Same 3-variable function as figure ``sop-from-truth-table`` (the lecture example
of p.44): the rows whose output is 0 are 000, 010, 011, 101 and 110, so the POS
form is

    Y = (A+B+C)(A+B'+C)(A+B'+C')(A'+B+C')(A'+B'+C) = PRODUCT M(0,2,3,5,6)

The drawing stresses the difference from a minterm: inside a maxterm a 0 in the
row makes the variable appear PLAIN and a 1 makes it BARRED -- the opposite of
the minterm rule -- and the maxterms are ANDed.

A table + boxes + arrows, so matplotlib.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

# rows with Y = 0 for the p.44 function -> their maxterms
KEEP = {0: r'$A+B+C$', 2: r'$A+\bar{B}+C$', 3: r'$A+\bar{B}+\bar{C}$',
        5: r'$\bar{A}+B+\bar{C}$', 6: r'$\bar{A}+\bar{B}+C$'}
ROWS = ['000', '001', '010', '011', '100', '101', '110', '111']


def build_figure():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(13.8, 7.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.0, 0.972, "(4-10) Truth table  ->  rows with output 0  ->  one maxterm "
                        "each  ->  AND",
            ha='left', va='center', fontsize=15, weight='bold', color=INK)
    ax.text(0.0, 0.930, "lecture example (p.44): the SAME function as the SOP figure, "
                        "read the other way -- $Y = \\prod M(0,2,3,5,6)$",
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
            ax.add_patch(Rectangle((0.025, y - 0.026), 0.262, 0.052, facecolor=FILL,
                                   edgecolor='none', zorder=1))
        for x, ch in zip((xa, xb, xc), row):
            ax.text(x, y, ch, ha='center', va='center', fontsize=12.5, color=INK,
                    family='DejaVu Sans Mono', zorder=3)
        ax.text(xy, y, '0' if keep else '1', ha='center', va='center', fontsize=12.5,
                color=HILITE if keep else MUTED, weight='bold', zorder=3)
        ax.text(0.300, y, ('row %d' % i) if keep else 'skip', ha='left', va='center',
                fontsize=10.5, color=HILITE if keep else MUTED, zorder=3)

    # ---------------- step 2: one maxterm per 0-row ------------------------
    ax.text(0.430, 0.885, "step 2  one maxterm per 0-row", ha='left', va='center',
            fontsize=11.5, color=ACCENT, weight='bold')
    ax.text(0.430, 0.850, "$0 \\rightarrow$ plain,  $1 \\rightarrow$ barred",
            ha='left', va='center', fontsize=10.5, color=MUTED)

    ys = []
    for i in sorted(KEEP):
        y = ytop - i * dy
        ys.append(y)
        ax.add_patch(FancyArrowPatch((0.355, y), (0.428, y),
                                     arrowstyle='-|>', mutation_scale=12,
                                     color=HILITE, lw=1.3, zorder=2))
        ax.add_patch(Rectangle((0.435, y - 0.026), 0.180, 0.052, facecolor='white',
                               edgecolor=HILITE, lw=1.2, zorder=2))
        ax.text(0.525, y, KEEP[i], ha='center', va='center', fontsize=12, color=INK,
                zorder=3)
        ax.text(0.620, y, '$M_{%d}$' % i, ha='left', va='center', fontsize=11,
                color=ACCENT, zorder=3)

    # ---------------- step 3: AND them into the POS ------------------------
    ax.text(0.720, 0.850, "step 3  AND the maxterms", ha='left', va='center',
            fontsize=11.5, color=ACCENT, weight='bold')
    ax.add_patch(Rectangle((0.700, 0.430), 0.295, 0.365, facecolor=FILL,
                           edgecolor=MUTED, lw=1.2, zorder=2))
    ax.text(0.847, 0.730, '$Y = (A+B+C)(A+\\bar{B}+C)$', ha='center', va='center',
            fontsize=11.5, color=INK, zorder=3)
    ax.text(0.847, 0.660, '$\\cdot\\,(A+\\bar{B}+\\bar{C})(\\bar{A}+B+\\bar{C})'
                          '(\\bar{A}+\\bar{B}+C)$',
            ha='center', va='center', fontsize=11.5, color=INK, zorder=3)
    ax.text(0.847, 0.565, '$= \\prod M(0,2,3,5,6)$', ha='center', va='center',
            fontsize=13, color=GOOD, zorder=3)
    ax.text(0.847, 0.485, "$\\prod$ means \"AND of the listed maxterms\"",
            ha='center', va='center', fontsize=10.5, color=MUTED, zorder=3)

    ax.add_patch(FancyArrowPatch((0.660, ys[2]), (0.694, 0.610),
                                 arrowstyle='-|>', mutation_scale=13, color=ACCENT,
                                 lw=1.4, zorder=2,
                                 connectionstyle='arc3,rad=-0.25'))

    ax.plot([0.0, 1.0], [0.245, 0.245], color=MUTED, lw=1.0)
    ax.text(0.0, 0.195, "check: all 8 rows of $(A,B,C)$ enumerated -- this POS gives "
                        "exactly the $Y$ column above, so $\\prod M(0,2,3,5,6)$ is correct (OK).",
            ha='left', va='center', fontsize=11.5, color=INK)
    ax.text(0.0, 0.135, "row $010$: $A{=}0 \\rightarrow A$,  $B{=}1 \\rightarrow \\bar{B}$,  "
                        "$C{=}0 \\rightarrow C$  gives the maxterm $A + \\bar{B} + C$.",
            ha='left', va='center', fontsize=11, color=ACCENT)
    ax.text(0.0, 0.075, "the 1-rows are left out again: POS and SOP of the same function "
                        "list complementary index sets.", ha='left', va='center',
            fontsize=11, color=MUTED)
    return fig


def main():
    fig = build_figure()
    save_fig(fig, 'pos-from-truth-table')

    # ---- numbers the note quotes -------------------------------------------
    import itertools
    def maxterm(i, row):
        return int(any(b != ((i >> (2 - k)) & 1) for k, b in enumerate(row)))

    rows = list(itertools.product([0, 1], repeat=3))
    y = [int(all(maxterm(i, r) for i in KEEP)) for r in rows]
    print('check  Y column            :', y)
    print('check  Y = 0 exactly in rows:', [i for i, v in enumerate(y) if not v])
    print('check  prod M(0,2,3,5,6) enumerated over 8 rows matches the table: %s'
          % (y == [0 if i in KEEP else 1 for i in range(8)]))
    print('check  complementary to the SOP index set {1,4,7}: %s'
          % (sorted(set(range(8)) - set(KEEP)) == [1, 4, 7]))


if __name__ == '__main__':
    main()
