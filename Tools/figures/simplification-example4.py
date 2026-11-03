"""Figure: the step-by-step simplification of lecture Example 4 (p.33).

The lecture simplifies

    Y = B*C + B'*D + C*D          (three product terms, one of them redundant)

by ADDING the redundant term C*D(B + B') -- which is just C*D multiplied by 1 --
expanding it, regrouping the four products into two pairs and then absorbing
each pair with Rule 10 (X + XY = X):

    BC + B'D + CD  ->  BC + B'D + CD(B + B')  ->  BC + B'D + BCD + B'CD
                   ->  BC + BCD + B'D + B'CD  ->  BC(1+D) + B'D(1+C)
                   ->  BC + B'D

Every step carries the axiom / theorem / rule it uses on the right, which is the
writing convention the lecture asks for (p.32).

Text-only content (a derivation on a ruled grid), so matplotlib.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# (left, right, colour of the left-hand expression, colour of the rule)
STEPS = [
    (r"$Y = BC + \bar{B}D + CD$", "given expression", INK, MUTED),
    (r"$= BC + \bar{B}D + CD(B + \bar{B})$",
     r"Rule 7: $B + \bar{B} = 1$, so $CD\cdot 1 = CD$", HILITE, INK),
    (r"$= BC + \bar{B}D + BCD + \bar{B}CD$",
     r"distributive law: $CD(B+\bar{B}) = BCD + \bar{B}CD$", INK, INK),
    (r"$= BC + BCD + \bar{B}D + \bar{B}CD$",
     "commutative + associative: regroup into two pairs", INK, INK),
    (r"$= BC(1 + D) + \bar{B}D(1 + C)$",
     "distributive law (factor out)", INK, INK),
    (r"$= BC + \bar{B}D$",
     r"Rule 10: $X + XY = X$, applied twice", GOOD, INK),
]

NOTES = [
    (HILITE, r"the only new idea: multiply $CD$ by $(B+\bar{B}) = 1$ -- nothing changes, "
             r"but $BCD$ and $\bar{B}CD$ now exist to be absorbed."),
    (GOOD, r"absorbed: $BC + BCD = BC(1+D) = BC$ and $\bar{B}D + \bar{B}CD = \bar{B}D(1+C) = \bar{B}D$."),
    (MUTED, r"check: all 8 rows of $(B,C,D)$ enumerated -- $BC+\bar{B}D+CD$ and $BC+\bar{B}D$ "
            r"agree in every row (OK)."),
    (BAD, r"the bar on $B$ is essential: $BC+\bar{B}D+CD = BC+\bar{B}D$, but $BC+BD+CD \neq BC+BD$ "
          r"(row $B{=}0,C{=}1,D{=}1$ gives 1 vs 0)."),
]


def build_figure():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(12.6, 8.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.0, 0.968, "(4-07) Example 4 (lecture p.33): add a redundant term, then absorb",
            ha='left', va='center', fontsize=15.5, weight='bold', color=INK)
    ax.text(0.0, 0.918, "every step is tagged on the right with the law / rule it uses "
                        "-- the writing convention of the lecture (p.32)",
            ha='left', va='center', fontsize=11, color=MUTED)
    ax.plot([0.0, 1.0], [0.888, 0.888], color=MUTED, lw=1.0)

    y = 0.822
    dy = 0.095
    for left, right, lc, rc in STEPS:
        ax.add_patch(Rectangle((0.0, y - 0.037), 0.588, 0.074, facecolor=FILL,
                               edgecolor='none', zorder=1))
        ax.text(0.012, y, left, ha='left', va='center', fontsize=15.5, color=lc,
                zorder=3, math_fontfamily='dejavusans')
        ax.text(0.995, y, right, ha='right', va='center', fontsize=11.5, color=rc,
                zorder=3)
        y -= dy

    ax.plot([0.0, 1.0], [0.330, 0.330], color=MUTED, lw=1.0)

    yy = 0.296
    for colour, txt in NOTES:
        ax.text(0.012, yy, txt, ha='left', va='top', fontsize=11, color=colour)
        yy -= 0.066

    ax.text(0.012, 0.036, "result: one product term fewer than $BC + \\bar{B}D + CD$, "
                          "same truth table, fewer gates", ha='left', va='center',
            fontsize=11.5, color=INK)
    return fig


def main():
    fig = build_figure()
    save_fig(fig, 'simplification-example4')

    # ---- numbers the note quotes -------------------------------------------
    import itertools
    f = lambda B, C, D: (B and C) or ((not B) and D) or (C and D)
    g = lambda B, C, D: (B and C) or ((not B) and D)
    rows = list(itertools.product([0, 1], repeat=3))
    print('check  BC+B\'D+CD  :', [int(f(*v)) for v in rows])
    print('check  BC+B\'D      :', [int(g(*v)) for v in rows])
    print('check  all 8 rows identical: %s' % ([int(f(*v)) for v in rows]
                                               == [int(g(*v)) for v in rows]))
    print('check  without the bar (BC+BD+CD vs BC+BD) row B=0,C=1,D=1: %d vs %d'
          % (int((0 and 1) or (0 and 1) or (1 and 1)), int((0 and 1) or (0 and 1))))


if __name__ == '__main__':
    main()
