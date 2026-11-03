"""Figure: the Karnaugh-map rules (ECE2050 Ch4, slides p.48-p.49).

Panel (a)  numbering: the 3-variable map is 2 rows x 4 columns, the
           4-variable map is 4 x 4.  Both axes are labelled with the Gray
           code 00 01 11 10 (never 00 01 10 11), so two adjacent cells differ
           in exactly one variable -- that is the whole reason a pair of
           neighbours can drop one literal.  Every cell carries its minterm
           number m_i and the ABCD pattern it stands for.
Panel (b)  the five circle rules as pictures: a 1x2 pair, a 2x2 quad and a
           wrap-around group are legal; a diagonal pair, a 3-cell run and an
           L-shape are not.  Cell contents are left blank on purpose -- this
           panel is about the *geometry* of a circle, not about a function.

Everything is a table of cells, so matplotlib is the right tool.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

GRAY2 = ['00', '01', '11', '10']      # the only allowed row/column order
CELL_LW = 1.4
BOX_LW = 2.0


# ---------------------------------------------------------------- geometry ---
def gray_value(label: str) -> int:
    """'11' -> 3, '10' -> 2: the *binary* value the Gray label stands for."""
    return int(label, 2)


def minterm(nvar: int, r: int, c: int) -> int:
    """Minterm number of the cell in row r, column c (rows = left axis pair)."""
    ab = gray_value(GRAY2[c])                     # columns are always A B
    a, b = (ab >> 1) & 1, ab & 1
    if nvar == 3:
        return 4 * a + 2 * b + int(GRAY2[r], 2)
    cd = gray_value(GRAY2[r])
    return 8 * a + 4 * b + 2 * ((cd >> 1) & 1) + (cd & 1)


def pattern(nvar: int, r: int, c: int) -> str:
    """The ABCD pattern the cell stands for, e.g. '0110'."""
    m = minterm(nvar, r, c)
    return format(m, '0%db' % nvar)


def draw_map(ax, x0, y0, nvar, col_var, row_var, show_numbers=True):
    """Draw one empty K-map frame; returns (ncols, nrows)."""
    ncols, nrows = 4, (2 if nvar == 3 else 4)
    for r in range(nrows):
        for c in range(ncols):
            yb = y0 + (nrows - 1 - r)
            ax.add_patch(Rectangle((x0 + c, yb), 1, 1, facecolor='white',
                                   edgecolor=INK, lw=CELL_LW, zorder=2))
            if show_numbers:
                ax.text(x0 + c + 0.5, yb + 0.62, 'm%d' % minterm(nvar, r, c),
                        ha='center', va='center', fontsize=10.5, color=INK,
                        zorder=3)
                ax.text(x0 + c + 0.5, yb + 0.27, pattern(nvar, r, c),
                        ha='center', va='center', fontsize=7.5, color=MUTED,
                        zorder=3)
    for c, lab in enumerate(GRAY2):
        ax.text(x0 + c + 0.5, y0 + nrows + 0.16, lab, ha='center',
                va='bottom', fontsize=10, color=ACCENT, zorder=3)
    for r, lab in enumerate(GRAY2[:nrows]):
        ax.text(x0 - 0.24, y0 + (nrows - 1 - r) + 0.5, lab, ha='right',
                va='center', fontsize=10, color=ACCENT, zorder=3)
    ax.text(x0 + ncols / 2.0, y0 + nrows + 0.58, col_var, ha='center',
            va='bottom', fontsize=12, color=HILITE, zorder=3)
    ax.text(x0 - 1.15, y0 + nrows / 2.0, row_var, ha='center', va='center',
            fontsize=12, color=HILITE, zorder=3)
    return ncols, nrows


def cell_box(ax, x0, y0, nrows, r, c, color, pad=0.07, lw=BOX_LW, ls='-'):
    """Rounded outline around one cell."""
    ax.add_patch(FancyBboxPatch(
        (x0 + c + pad, y0 + (nrows - 1 - r) + pad),
        1 - 2 * pad, 1 - 2 * pad,
        boxstyle='round,pad=0,rounding_size=0.16', facecolor='none',
        edgecolor=color, lw=lw, ls=ls, zorder=5))


def group_box(ax, x0, y0, nrows, r0, r1, c0, c1, color=HILITE, pad=0.10,
              lw=BOX_LW, ls='-', shade=True):
    """Rounded outline around the rectangle of cells rows r0..r1, cols c0..c1."""
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            if shade:
                ax.add_patch(Rectangle((x0 + c, y0 + (nrows - 1 - r)), 1, 1,
                                       facecolor=FILL, edgecolor='none',
                                       zorder=1))
    xa, ya = x0 + c0 + pad, y0 + (nrows - 1 - r1) + pad
    ax.add_patch(FancyBboxPatch(
        (xa, ya), (c1 - c0 + 1) - 2 * pad, (r1 - r0 + 1) - 2 * pad,
        boxstyle='round,pad=0,rounding_size=0.18', facecolor='none',
        edgecolor=color, lw=lw, ls=ls, zorder=5))


def wrap_frame(ax, x0, y0, ncols, nrows, color=HILITE):
    """Dashed frame just outside the map: the two opposite edges are joined."""
    pad = 0.30
    ax.add_patch(FancyBboxPatch(
        (x0 - pad, y0 - pad), ncols + 2 * pad, nrows + 2 * pad,
        boxstyle='round,pad=0,rounding_size=0.30', facecolor='none',
        edgecolor=color, lw=BOX_LW - 0.4, ls=(0, (4, 3)), zorder=4))


def marker(ax, x0, y0, nrows, r, c, text, color):
    ax.text(x0 + c + 0.22, y0 + (nrows - 1 - r) + 0.80, text, ha='center',
            va='center', fontsize=11, color=color, zorder=7)


def legend(ax, x, y, lines):
    for i, (tag, text, color) in enumerate(lines):
        ax.text(x, y - i * 0.40, tag, ha='right', va='center', fontsize=10.5,
                color=color)
        ax.text(x + 0.16, y - i * 0.40, text, ha='left', va='center',
                fontsize=10.5, color=INK)


# ------------------------------------------------------------------ panels ---
def panel_a(ax):
    ax.set_xlim(-2.0, 11.9)
    ax.set_ylim(-0.6, 5.5)
    ax.axis('off')

    draw_map(ax, 0.0, 0.0, 3, 'AB', 'C')
    ax.text(2.0, 4.30, '(a) 3-variable map: 2 x 4 = 8 cells', ha='center',
            va='center', fontsize=12, color=INK)
    ax.text(2.0, -0.42, 'rows differ in C only', ha='center', va='center',
            fontsize=9.5, color=MUTED)

    draw_map(ax, 6.7, 0.0, 4, 'AB', 'CD')
    ax.text(8.7, 4.30, '(a) 4-variable map: 4 x 4 = 16 cells', ha='center',
            va='center', fontsize=12, color=INK)
    ax.text(8.7, -0.42, 'neighbours differ in exactly 1 variable',
            ha='center', va='center', fontsize=9.5, color=MUTED)


def panel_b(ax, legal: bool):
    x0, y0, nrows = 0.0, 0.0, 4
    ax.set_xlim(-2.0, 5.6)
    ax.set_ylim(-2.2, 5.6)
    ax.axis('off')
    draw_map(ax, x0, y0, 4, 'AB', 'CD', show_numbers=False)

    if legal:
        ax.set_title('(b) legal circles', color=GOOD)
        group_box(ax, x0, y0, nrows, 1, 2, 1, 2, color=HILITE)      # 2x2
        marker(ax, x0, y0, nrows, 1, 1, '2', HILITE)
        group_box(ax, x0, y0, nrows, 3, 3, 1, 2, color=ACCENT)      # 1x2
        marker(ax, x0, y0, nrows, 3, 1, '1', ACCENT)
        wrap_frame(ax, x0, y0, 4, 4)
        for (r, c) in ((0, 0), (0, 3), (3, 0), (3, 3)):             # corners
            cell_box(ax, x0, y0, nrows, r, c, HILITE)
        marker(ax, x0, y0, nrows, 0, 0, '3', HILITE)
        legend(ax, 0.30, -0.85, [
            ('1', '1 x 2 pair (one literal drops)', ACCENT),
            ('2', '2 x 2 quad (two literals drop)', HILITE),
            ('3', '4 corners: the edges wrap around', HILITE),
        ])
    else:
        ax.set_title('(b) illegal circles', color=BAD)
        for r, c in ((0, 0), (1, 1)):                               # diagonal
            cell_box(ax, x0, y0, nrows, r, c, BAD, ls=(0, (3, 2)))
        marker(ax, x0, y0, nrows, 0, 0, '1', BAD)
        group_box(ax, x0, y0, nrows, 3, 3, 0, 2, color=BAD, shade=False,
                  ls=(0, (3, 2)))                                   # 3 cells
        marker(ax, x0, y0, nrows, 3, 0, '2', BAD)
        for r, c in ((1, 3), (2, 3), (2, 2)):                       # L-shape
            cell_box(ax, x0, y0, nrows, r, c, BAD, ls=(0, (3, 2)))
        marker(ax, x0, y0, nrows, 1, 3, '3', BAD)
        legend(ax, 0.30, -0.85, [
            ('1', 'diagonal: not allowed', BAD),
            ('2', '3 cells: not a power of 2', BAD),
            ('3', 'L-shape: must be a rectangle', BAD),
        ])


def build_figure():
    fig = plt.figure(figsize=(13.0, 9.4))
    gs = fig.add_gridspec(2, 2, height_ratios=[0.80, 1.0], hspace=0.30,
                          wspace=0.10)
    panel_a(fig.add_subplot(gs[0, :]))
    panel_b(fig.add_subplot(gs[1, 0]), legal=True)
    panel_b(fig.add_subplot(gs[1, 1]), legal=False)
    return fig


def main():
    apply_mpl_style()
    save_fig(build_figure(), 'kmap-rules')

    # ---- numbers the note quotes -------------------------------------------
    print('check  3-variable map, rows C, columns AB 00 01 11 10:')
    for r in range(2):
        print('        C=%s | ' % GRAY2[r][1]
              + '  '.join('m%-2d %s' % (minterm(3, r, c), pattern(3, r, c))
                          for c in range(4)))
    print('check  4-variable map, rows CD, columns AB 00 01 11 10:')
    for r in range(4):
        print('        CD=%s | ' % GRAY2[r]
              + '  '.join('m%-2d %s' % (minterm(4, r, c), pattern(4, r, c))
                          for c in range(4)))
    # adjacency proof: every step in the Gray order flips exactly one bit
    bad = []
    for order in (GRAY2, GRAY2):                       # columns and rows
        for i in range(len(order)):
            j = (i + 1) % len(order)
            d = bin(gray_value(order[i]) ^ gray_value(order[j])).count('1')
            if d != 1:
                bad.append((order[i], order[j], d))
    print('check  Gray order 00 01 11 10 (wrap included): %s'
          % ('all steps flip exactly 1 bit' if not bad else bad))
    print('check  minterm numbers are the binary value of the cell pattern: %s'
          % all(minterm(4, r, c) == int(pattern(4, r, c), 2)
                for r in range(4) for c in range(4)))


if __name__ == '__main__':
    main()
