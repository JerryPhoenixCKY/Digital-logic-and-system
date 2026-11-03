"""Figure: standard SOP  <->  truth table  <->  standard POS, on one example.

The complete lecture example of p.45-p.46: the standard SOP expression

    X = A'BC + AB'C' + ABC' + ABC      (minterms 3, 4, 6, 7)

and the standard POS expression

    X = (A+B+C)(A+B'+C')(A+B'+C)(A'+B+C')      (maxterms 0, 1, 2, 5)

describe the SAME function: the two index sets are complementary, and filling a
truth table from either side gives the same X column.

The four arrows are the four conversion moves: a minterm marks its own row with
1, a maxterm marks its own row with 0, and the table is read back by collecting
the 1-rows (SOP) or the 0-rows (POS).

Boxes + a table + arrows, so matplotlib.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

SOP_MIN = [3, 4, 6, 7]
POS_MAX = [0, 1, 2, 5]
ROWS = ['000', '001', '010', '011', '100', '101', '110', '111']


def box(ax, x0, x1, y0, y1):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=FILL,
                           edgecolor=MUTED, lw=1.2, zorder=2))


def build_figure():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(14.4, 8.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.0, 0.972, "(4-11) Standard SOP  <->  truth table  <->  standard POS",
            ha='left', va='center', fontsize=15.5, weight='bold', color=INK)
    ax.text(0.0, 0.928, "one complete example (lecture p.45-p.46): "
                        "$X = \\sum m(3,4,6,7)$ and $X = \\prod M(0,1,2,5)$ are the "
                        "same function",
            ha='left', va='center', fontsize=11.5, color=MUTED)

    # ---------------- the truth table in the middle ------------------------
    xa, xb, xc, xx = 0.425, 0.465, 0.505, 0.575
    ytop, dy = 0.800, 0.062
    ax.text(xa, 0.848, '$A$', ha='center', va='center', fontsize=12.5, color=INK)
    ax.text(xb, 0.848, '$B$', ha='center', va='center', fontsize=12.5, color=INK)
    ax.text(xc, 0.848, '$C$', ha='center', va='center', fontsize=12.5, color=INK)
    ax.text(xx, 0.848, '$X$', ha='center', va='center', fontsize=12.5, color=INK)
    ax.plot([0.400, 0.620], [0.828, 0.828], color=INK, lw=1.2)

    for i, row in enumerate(ROWS):
        y = ytop - i * dy
        onerow = i in SOP_MIN
        if onerow:
            ax.add_patch(Rectangle((0.400, y - 0.024), 0.220, 0.048, facecolor=FILL,
                                   edgecolor='none', zorder=1))
        for x, ch in zip((xa, xb, xc), row):
            ax.text(x, y, ch, ha='center', va='center', fontsize=12.5, color=INK,
                    family='DejaVu Sans Mono', zorder=3)
        ax.text(xx, y, '1' if onerow else '0', ha='center', va='center', fontsize=12.5,
                color=HILITE if onerow else ACCENT, weight='bold', zorder=3)

    ax.text(0.510, 0.318, "shaded = rows with $X = 1$  ($\\sum m$)", ha='center',
            va='center', fontsize=10.5, color=HILITE)
    ax.text(0.510, 0.272, "unshaded = rows with $X = 0$  ($\\prod M$)", ha='center',
            va='center', fontsize=10.5, color=ACCENT)

    # ---------------- standard SOP box -------------------------------------
    box(ax, 0.010, 0.220, 0.330, 0.660)
    ax.text(0.115, 0.618, "Standard SOP form", ha='center', va='center',
            fontsize=12, weight='bold', color=INK, zorder=3)
    ax.text(0.115, 0.568, "(sum of minterms)", ha='center', va='center', fontsize=10.5,
            color=MUTED, zorder=3)
    ax.text(0.115, 0.508, '$X = \\bar{A}BC + A\\bar{B}\\bar{C}$', ha='center',
            va='center', fontsize=12, color=INK, zorder=3)
    ax.text(0.115, 0.455, '$+\\; AB\\bar{C} + ABC$', ha='center', va='center',
            fontsize=12, color=INK, zorder=3)
    ax.text(0.115, 0.390, '$= \\sum m(3,4,6,7)$', ha='center', va='center',
            fontsize=13, color=GOOD, zorder=3)

    # ---------------- standard POS box -------------------------------------
    box(ax, 0.780, 0.990, 0.330, 0.660)
    ax.text(0.885, 0.618, "Standard POS form", ha='center', va='center',
            fontsize=12, weight='bold', color=INK, zorder=3)
    ax.text(0.885, 0.568, "(product of maxterms)", ha='center', va='center',
            fontsize=10.5, color=MUTED, zorder=3)
    ax.text(0.885, 0.508, '$X = (A+B+C)(A+B+\\bar{C})$', ha='center', va='center',
            fontsize=11, color=INK, zorder=3)
    ax.text(0.885, 0.455, '$\\cdot\\,(A+\\bar{B}+C)(\\bar{A}+B+\\bar{C})$', ha='center',
            va='center', fontsize=11, color=INK, zorder=3)
    ax.text(0.885, 0.390, '$= \\prod M(0,1,2,5)$', ha='center', va='center',
            fontsize=13, color=GOOD, zorder=3)

    # ---------------- the four conversion arrows ---------------------------
    ax.add_patch(FancyArrowPatch((0.232, 0.640), (0.392, 0.640), arrowstyle='-|>',
                                 mutation_scale=14, color=HILITE, lw=1.5, zorder=2))
    ax.text(0.312, 0.684, "minterm $m_i$  ->  a 1 in row $i$", ha='center',
            va='center', fontsize=10.5, color=HILITE)
    ax.add_patch(FancyArrowPatch((0.392, 0.520), (0.232, 0.520), arrowstyle='-|>',
                                 mutation_scale=14, color=HILITE, lw=1.5, zorder=2))
    ax.text(0.312, 0.470, "rows with $X = 1$  ->  minterms", ha='center', va='center',
            fontsize=10.5, color=HILITE)

    ax.add_patch(FancyArrowPatch((0.778, 0.640), (0.628, 0.640), arrowstyle='-|>',
                                 mutation_scale=14, color=ACCENT, lw=1.5, zorder=2))
    ax.text(0.703, 0.684, "maxterm $M_i$  ->  a 0 in row $i$", ha='center',
            va='center', fontsize=10.5, color=ACCENT)
    ax.add_patch(FancyArrowPatch((0.628, 0.520), (0.778, 0.520), arrowstyle='-|>',
                                 mutation_scale=14, color=ACCENT, lw=1.5, zorder=2))
    ax.text(0.703, 0.470, "rows with $X = 0$  ->  maxterms", ha='center', va='center',
            fontsize=10.5, color=ACCENT)

    # ---------------- footer ----------------------------------------------
    ax.plot([0.0, 1.0], [0.215, 0.215], color=MUTED, lw=1.0)
    ax.text(0.0, 0.165, "check: all 8 rows enumerated -- $\\sum m(3,4,6,7)$ and "
                        "$\\prod M(0,1,2,5)$ give the same $X$ in every row (OK).",
            ha='left', va='center', fontsize=11.5, color=INK)
    ax.text(0.0, 0.112, "the two index sets are complementary: "
                        "$\\{3,4,6,7\\} \\cup \\{0,1,2,5\\} = \\{0,\\dots,7\\}$ -- "
                        "that is why both forms describe one function.",
            ha='left', va='center', fontsize=11, color=ACCENT)
    ax.text(0.0, 0.058, "filling the table from a term: a term that is not satisfied in "
                        "a row is simply 0 there -- the lecture marks such cells "
                        "\"Don't Care\" (p.43-44).",
            ha='left', va='center', fontsize=11, color=MUTED)
    return fig


def main():
    fig = build_figure()
    save_fig(fig, 'truth-table-conversion')

    # ---- numbers the note quotes -------------------------------------------
    import itertools
    def minterm(i, row, n=3):
        return int(all(b == ((i >> (n - 1 - k)) & 1) for k, b in enumerate(row)))

    def maxterm(i, row, n=3):
        return int(any(b != ((i >> (n - 1 - k)) & 1) for k, b in enumerate(row)))

    rows = list(itertools.product([0, 1], repeat=3))
    sop = [int(any(minterm(i, r) for i in SOP_MIN)) for r in rows]
    pos = [int(all(maxterm(i, r) for i in POS_MAX)) for r in rows]
    print('check  X from SOP sum m(3,4,6,7) :', sop)
    print('check  X from POS prod M(0,1,2,5):', pos)
    print('check  identical in all 8 rows: %s' % (sop == pos))
    print('check  index sets complementary: %s'
          % (sorted(set(SOP_MIN) | set(POS_MAX)) == list(range(8))
             and not (set(SOP_MIN) & set(POS_MAX))))
    print('check  SOP 1-rows: %s   POS 0-rows: %s'
          % ([i for i, v in enumerate(sop) if v], [i for i, v in enumerate(pos) if not v]))


if __name__ == '__main__':
    main()
