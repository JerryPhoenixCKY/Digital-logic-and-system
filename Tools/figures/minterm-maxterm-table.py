"""Figure: the minterm / maxterm tables for 2 and 3 variables.

Panel (a) lists the eight 3-variable minterms m0..m7 next to their maxterms
M0..M7; panel (b) does the same for the four 2-variable terms.  In both tables
row i is shaded: that is the ONE row in which m_i is 1 and the ONE row in which
M_i is 0 -- the two right-hand columns spell that out.  The footnotes give the
complement relation M_i = NOT m_i and the two ways the terms are used
(OR the m_i where the output is 1 -> SOP, AND the M_i where the output is 0 -> POS).

A table-like drawing, so matplotlib.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def terms(n, i):
    """minterm / maxterm (mathtext) of index i for n variables A, B[, C]."""
    names = 'ABC'[:n]
    bits = [(i >> (n - 1 - k)) & 1 for k in range(n)]
    mt = ''.join(('\\bar{%s}' if b == 0 else '%s') % nm for nm, b in zip(names, bits))
    Mt = '+'.join(('%s' % nm) if b == 0 else ('\\bar{%s}' % nm)
                  for nm, b in zip(names, bits))
    return r'$%s$' % mt, r'$%s$' % Mt


COLS = [0.055, 0.215, 0.500, 0.755, 0.885, 0.975]      # i, bits, m_i, M_i, m_i, M_i
HEAD = ['index $i$', 'row values', 'minterm $m_i$', 'maxterm $M_i$',
        '$m_i$', '$M_i$']


def draw_table(ax, n, title):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title(title, loc='left')

    rows = 2 ** n
    ytop, ybot = 0.845, 0.175
    dy = (ytop - ybot) / (rows - 1)
    band = dy * 0.44

    ax.text(COLS[0], ytop + dy * 0.78, HEAD[0], ha='center', va='center',
            fontsize=10.5, color=MUTED)
    ax.text(COLS[1], ytop + dy * 0.78, HEAD[1], ha='center', va='center',
            fontsize=10.5, color=MUTED)
    ax.text(COLS[2], ytop + dy * 0.78, HEAD[2], ha='center', va='center',
            fontsize=10.5, color=MUTED)
    ax.text(COLS[3], ytop + dy * 0.78, HEAD[3], ha='center', va='center',
            fontsize=10.5, color=MUTED)
    ax.text(COLS[4], ytop + dy * 0.78, HEAD[4], ha='center', va='center',
            fontsize=10.5, color=GOOD)
    ax.text(COLS[5], ytop + dy * 0.78, HEAD[5], ha='center', va='center',
            fontsize=10.5, color=BAD)
    ax.plot([0.0, 1.0], [ytop + dy * 0.42, ytop + dy * 0.42], color=MUTED, lw=1.0)

    for i in range(rows):
        y = ytop - i * dy
        bits = format(i, '0%db' % n)
        ax.add_patch(Rectangle((0.0, y - band), 1.0, 2 * band, facecolor=FILL,
                               edgecolor='none', zorder=1))
        mt, Mt = terms(n, i)
        ax.text(COLS[0], y, '%d' % i, ha='center', va='center', fontsize=13,
                color=INK, zorder=3)
        ax.text(COLS[1], y, ' '.join(bits), ha='center', va='center', fontsize=13,
                family='DejaVu Sans Mono', color=INK, zorder=3)
        ax.text(COLS[2], y, mt, ha='center', va='center', fontsize=13, color=INK,
                zorder=3)
        ax.text(COLS[3], y, Mt, ha='center', va='center', fontsize=13, color=INK,
                zorder=3)
        ax.text(COLS[4], y, '1', ha='center', va='center', fontsize=13, color=GOOD,
                weight='bold', zorder=3)
        ax.text(COLS[5], y, '0', ha='center', va='center', fontsize=13, color=BAD,
                weight='bold', zorder=3)

    ax.plot([0.0, 1.0], [ybot - dy * 0.55, ybot - dy * 0.55], color=MUTED, lw=1.0)


def build_figure():
    apply_mpl_style()
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(14.2, 7.4), gridspec_kw={'width_ratios': [1.30, 1.0]})

    draw_table(ax1, 3, '(a) 3 variables: 8 minterms, 8 maxterms')
    draw_table(ax2, 2, '(b) 2 variables: 4 minterms, 4 maxterms')

    for ax, lines in (
        (ax1, [
            (INK, r"shaded band = row $i$: the only row where $m_i = 1$ and $M_i = 0$."),
            (ACCENT, r"$M_i = \overline{m_i}$ ($\overline{m_2} = \overline{\bar{A}B\bar{C}} "
                     r"= A + \bar{B} + C = M_2$)"),
            (MUTED, r"numbering: read the row as a binary number, $A$ is the MSB."),
        ]),
        (ax2, [
            (INK, r"$m_1 = \bar{A}B$,  $M_1 = A + \bar{B}$,  "
                  r"$\overline{m_1} = A + \bar{B} = M_1$"),
            (MUTED, r"OR the $m_i$ of the 1-rows  ->  SOP"),
            (MUTED, r"AND the $M_i$ of the 0-rows  ->  POS"),
        ])):
        y = 0.105
        for colour, txt in lines:
            ax.text(0.0, y, txt, ha='left', va='top', fontsize=11, color=colour)
            y -= 0.062
    return fig


def evalm(n, i, row):
    """value of minterm i in the given row (row[0] is the MSB)."""
    return int(all(b == ((i >> (n - 1 - k)) & 1) for k, b in enumerate(row)))


def evalM(n, i, row):
    """value of maxterm i in the given row."""
    return int(any(b != ((i >> (n - 1 - k)) & 1) for k, b in enumerate(row)))


def main():
    fig = build_figure()
    save_fig(fig, 'minterm-maxterm-table')

    # ---- numbers the note quotes -------------------------------------------
    import itertools
    for n in (2, 3):
        print('--- %d variables ---' % n)
        rows = list(itertools.product([0, 1], repeat=n))
        for i in range(2 ** n):
            mt, Mt = terms(n, i)
            vm = [evalm(n, i, r) for r in rows]
            vM = [evalM(n, i, r) for r in rows]
            print('  m%d = %-26s %s   M%d = %-26s %s   m_i=1 only in row %s, '
                  'M_i=0 only in row %s'
                  % (i, mt, vm, i, Mt, vM, vm.index(1), vM.index(0)))
        print('  every m_i is 1 in exactly one row: %s'
              % all(sum(evalm(n, i, r) for r in rows) == 1 for i in range(2 ** n)))
        print('  every M_i is 0 in exactly one row: %s'
              % all(sum(1 - evalM(n, i, r) for r in rows) == 1 for i in range(2 ** n)))
        print('  M_i == NOT m_i in every row: %s'
              % all(evalM(n, i, r) == 1 - evalm(n, i, r)
                    for i in range(2 ** n) for r in rows))


if __name__ == '__main__':
    main()
