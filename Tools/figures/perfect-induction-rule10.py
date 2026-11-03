"""Figure: two proofs of Rule 10, A + AB = A, side by side.

Panel (a) Method 1 -- perfect induction: the truth table lists every possible
input combination (4 rows for two variables) and the columns for A + AB and
for A are compared row by row.  They agree in all 4 rows, so the two
expressions are the same function: the proof is finished, and no algebra is
needed.

Panel (b) Method 2 -- algebra: use the other axioms/theorems to turn one side
into the other, annotating every step with the rule it uses:
    A + AB = A*1 + AB      (Rule 2 backwards: A = A*1)
           = A(1 + B)      (distributive law, factored)
           = A*1           (Rule 3: 1 + B = 1)
           = A             (Rule 2: A*1 = A)

Panel (a) is mechanical and always works but blows up as 2^n; panel (b) is
short but needs the rules.  Numbers in the table are computed, not typed.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

MONO = 'DejaVu Sans Mono'


def cell(ax, x, y, w, h, s, face='white', edge=INK, color=INK, lw=1.3, fs=13):
    """One table cell: rectangle + centred text."""
    ax.add_patch(Rectangle((x, y), w, h, facecolor=face, edgecolor=edge,
                           lw=lw, zorder=2))
    ax.text(x + w / 2, y + h / 2, s, ha='center', va='center', color=color,
            fontsize=fs, zorder=3)


def panel_truth_table(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(2.4, 10.4)
    ax.axis('off')

    cols = [('A', 1.5), ('B', 1.5), ('AB', 1.5), ('A + AB', 2.0), ('A', 1.5)]
    x0, ytop, h = 1.0, 9.2, 0.9
    xs, x = [], x0
    for _, w in cols:
        xs.append(x)
        x += w
    HL = (3, 4)                       # the two columns being compared

    # header row
    for i, ((name, w), cx) in enumerate(zip(cols, xs)):
        hot = i in HL
        cell(ax, cx, ytop, w, h, name, face=FILL, edge=INK,
             color=(GOOD if hot else INK), fs=14)

    # data rows, computed from the definition of the two expressions
    rows = [(a, b) for a in (0, 1) for b in (0, 1)]
    for i, (a, b) in enumerate(rows):
        y = ytop - (i + 1) * h
        prod = a and b
        lhs = a or prod
        vals = ['%d' % a, '%d' % b, '%d' % prod, '%d' % lhs, '%d' % a]
        for j, ((name, w), cx, v) in enumerate(zip(cols, xs, vals)):
            if j in HL:
                cell(ax, cx, y, w, h, v, face=FILL, edge=GOOD, color=GOOD,
                     lw=1.6, fs=14)
            else:
                cell(ax, cx, y, w, h, v, fs=14)

    ax.text(5.0, 10.05,
            '(a) Method 1: perfect induction -- check every input row',
            ha='center', va='center', fontsize=14, color=INK, weight='bold')
    ax.text(1.0, 4.05,
            'columns 4 and 5 agree in 4 of 4 rows  ->  A + AB = A',
            ha='left', va='center', fontsize=13, color=GOOD)
    ax.text(1.0, 3.35,
            'every input combination is covered, so the identity is proven',
            ha='left', va='center', fontsize=12, color=MUTED)
    ax.text(1.0, 2.75,
            'cost: 2^n rows (4 here, 8 for 3 variables, 1024 for 10)',
            ha='left', va='center', fontsize=12, color=ACCENT)


def panel_algebra(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(2.4, 10.4)
    ax.axis('off')

    ax.text(5.0, 10.05,
            '(b) Method 2: algebra -- make one side look like the other',
            ha='center', va='center', fontsize=14, color=INK, weight='bold')

    steps = [
        (r'$A + AB$', '', INK),
        (r'$= A\cdot 1 + AB$', r'Rule 2 backwards:  $A = A\cdot 1$', INK),
        (r'$= A\,(1 + B)$', 'distributive law, factor out $A$', INK),
        (r'$= A\cdot 1$', r'Rule 3:  $1 + B = 1$', INK),
        (r'$= A$', r'Rule 2:  $A\cdot 1 = A$', GOOD),
    ]
    y = 8.75
    for expr, why, col in steps:
        ax.text(0.45, y, expr, ha='left', va='center', fontsize=16, color=col)
        if why:
            ax.text(9.55, y, why, ha='right', va='center', fontsize=12,
                    color=(GOOD if col is GOOD else ACCENT))
        y -= 1.15

    ax.plot([5.95, 5.95], [3.85, 9.20], color=MUTED, lw=1.2, ls='--',
            zorder=1)
    ax.text(0.45, 2.95,
            'same result as (a), but no 2^n table is needed',
            ha='left', va='center', fontsize=12, color=GOOD)
    ax.text(0.45, 2.55,
            'each line names the axiom/rule/theorem that justifies it',
            ha='left', va='center', fontsize=12, color=MUTED)


def build_figure():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.6))
    panel_truth_table(ax1)
    panel_algebra(ax2)
    fig.text(0.5, 0.015,
             'Rule 10:  A + AB = A   --   exhaustively true (a), or derived '
             'from the rules (b)',
             ha='center', va='center', fontsize=12.5, color=HILITE)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    return fig


def main():
    apply_mpl_style()
    fig = build_figure()
    save_fig(fig, 'perfect-induction-rule10')

    # ---- perfect induction: A + AB == A in every row ----------------------
    print('check  Rule 10 by perfect induction')
    for a in (0, 1):
        for b in (0, 1):
            print('       A=%d B=%d -> AB=%d  A+AB=%d  A=%d  %s'
                  % (a, b, a & b, a | (a & b), a,
                     'equal' if (a | (a & b)) == a else 'DIFFERENT'))

    # ---- the dual of Rule 10, same table ---------------------------------
    print("check  dual of Rule 10, A(A+B) = A")
    for a in (0, 1):
        for b in (0, 1):
            print('       A=%d B=%d -> A+B=%d  A(A+B)=%d  A=%d  %s'
                  % (a, b, a | b, a & (a | b), a,
                     'equal' if (a & (a | b)) == a else 'DIFFERENT'))

    # ---- the algebra of panel (b), evaluated symbolically per row --------
    print('check  step 2 of panel (b): A*1 + AB equals A + AB')
    for a in (0, 1):
        for b in (0, 1):
            print('       A=%d B=%d -> A*1+AB=%d  A+AB=%d'
                  % (a, b, (a & 1) | (a & b), a | (a & b)))


if __name__ == '__main__':
    main()
