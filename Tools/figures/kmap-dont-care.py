"""Figure: K-map with don't cares (ECE2050 Ch4, slide p.59).

Panel (a)  the map exactly as the slide gives it: 1, 0 and the seven X cells
           (m5 and the illegal-BCD block m10 ... m15).  With rows CD and
           columns AB, each cell also carries its minterm number.
Panel (b)  the same map with the three circles that produce the minimum
           expression.  Two of them swallow X cells (that is the whole point
           of a don't care); the third (bar B bar D, the four corners) needs
           the wrap-around rule.  The final expression is written out.

Everything is a table of cells, so matplotlib is the right tool.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

GRAY2 = ['00', '01', '11', '10']          # rows CD and columns AB, Gray order
CELL_LW = 1.4
BOX_LW = 2.0

# the function of slide p.59: ones, zeros and don't cares
ONES = {0, 2, 3, 6, 7, 8, 9}
ZEROS = {1, 4}
DCS = {5, 10, 11, 12, 13, 14, 15}
# the minimum expression the slide circles out
FINAL = [[(0, 1)], [(2, 1)], [(1, 0), (3, 0)]]        # A + C + Bbar Dbar
NO_DC = [[(0, 0), (2, 1)], [(0, 1), (1, 0), (2, 0)],
         [(0, 0), (1, 0), (3, 0)]]                    # X forced to 0
NAMES = 'ABCD'


def minterm(r, c):
    ab, cd = int(GRAY2[c], 2), int(GRAY2[r], 2)
    return 8 * ((ab >> 1) & 1) + 4 * (ab & 1) + 2 * ((cd >> 1) & 1) + (cd & 1)


def value(m):
    return '1' if m in ONES else ('0' if m in ZEROS else 'X')


def draw_map(ax, x0, y0, title):
    n = 4
    ax.set_xlim(x0 - 1.9, x0 + 5.9)
    ax.set_ylim(y0 - 3.6, y0 + 5.4)
    ax.axis('off')
    for r in range(n):
        for c in range(n):
            m = minterm(r, c)
            yb = y0 + (n - 1 - r)
            ax.add_patch(Rectangle((x0 + c, yb), 1, 1, facecolor='white',
                                   edgecolor=INK, lw=CELL_LW, zorder=2))
            v = value(m)
            ax.text(x0 + c + 0.5, yb + 0.52, v, ha='center', va='center',
                    fontsize=15, zorder=4,
                    color=ACCENT if v == 'X' else INK)
            ax.text(x0 + c + 0.86, yb + 0.16, 'm%d' % m, ha='right',
                    va='center', fontsize=7.5, color=MUTED, zorder=4)
    for c, lab in enumerate(GRAY2):
        ax.text(x0 + c + 0.5, y0 + n + 0.16, lab, ha='center', va='bottom',
                fontsize=10, color=ACCENT, zorder=3)
    for r, lab in enumerate(GRAY2):
        ax.text(x0 - 0.24, y0 + (n - 1 - r) + 0.5, lab, ha='right',
                va='center', fontsize=10, color=ACCENT, zorder=3)
    ax.text(x0 + 2.0, y0 + n + 0.60, 'AB', ha='center', va='bottom',
            fontsize=12, color=HILITE, zorder=3)
    ax.text(x0 - 1.25, y0 + 2.0, 'CD', ha='center', va='center', fontsize=12,
            color=HILITE, zorder=3)
    ax.text(x0 + 2.0, y0 + n + 1.05, title, ha='center', va='bottom',
            fontsize=12, color=INK, zorder=3)


def group_box(ax, x0, y0, r0, r1, c0, c1, color=HILITE, pad=0.11,
              ls='-', shade=True):
    if shade:
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                ax.add_patch(Rectangle((x0 + c, y0 + 3 - r), 1, 1,
                                       facecolor=FILL, edgecolor='none',
                                       zorder=1))
    ax.add_patch(FancyBboxPatch(
        (x0 + c0 + pad, y0 + (3 - r1) + pad),
        (c1 - c0 + 1) - 2 * pad, (r1 - r0 + 1) - 2 * pad,
        boxstyle='round,pad=0,rounding_size=0.18', facecolor='none',
        edgecolor=color, lw=BOX_LW, ls=ls, zorder=6))


def cell_box(ax, x0, y0, r, c, color, pad=0.08):
    ax.add_patch(FancyBboxPatch(
        (x0 + c + pad, y0 + (3 - r) + pad), 1 - 2 * pad, 1 - 2 * pad,
        boxstyle='round,pad=0,rounding_size=0.16', facecolor=FILL,
        edgecolor=color, lw=BOX_LW, zorder=6))


def wrap_frame(ax, x0, y0, color=HILITE):
    pad = 0.32
    ax.add_patch(FancyBboxPatch(
        (x0 - pad, y0 - pad), 4 + 2 * pad, 4 + 2 * pad,
        boxstyle='round,pad=0,rounding_size=0.30', facecolor='none',
        edgecolor=color, lw=BOX_LW - 0.4, ls=(0, (4, 3)), zorder=5))


def marker(ax, x0, y0, r, c, text, color):
    ax.text(x0 + c + 0.20, y0 + (3 - r) + 0.80, text, ha='center',
            va='center', fontsize=11, color=color, zorder=8)


def term_text(term):
    """[(var, value), ...] -> mathtext for the product term."""
    out = ''
    for var, val in term:
        out += ('\\bar{%s}' % NAMES[var]) if val == 0 else NAMES[var]
    return '$%s$' % out


def panel_a(ax):
    draw_map(ax, 0.0, 0.0, '(a) the map: 1, 0 and X (unused BCD codes)')
    ax.text(-1.05, -0.95, 'X = the input combination cannot occur,',
            ha='left', va='center', fontsize=10.5, color=ACCENT)
    ax.text(-1.05, -1.35, 'so the output may be defined either way',
            ha='left', va='center', fontsize=10.5, color=ACCENT)
    expr = ' + '.join(term_text(t) for t in NO_DC)
    ax.text(-1.05, -2.05, 'if every X were forced to 0:  ' + expr,
            ha='left', va='center', fontsize=10.5, color=BAD)
    ax.text(-1.05, -2.45, '= 3 terms, 8 literals', ha='left', va='center',
            fontsize=10.5, color=BAD)


def panel_b(ax):
    draw_map(ax, 0.0, 0.0, '(b) circle the X only where it helps')
    group_box(ax, 0.0, 0.0, 2, 3, 0, 3, color=ACCENT)          # C
    marker(ax, 0.0, 0.0, 2, 0, '1', ACCENT)
    group_box(ax, 0.0, 0.0, 0, 3, 2, 3, color=HILITE)          # A
    marker(ax, 0.0, 0.0, 0, 2, '2', HILITE)
    wrap_frame(ax, 0.0, 0.0)
    for r, c in ((0, 0), (0, 3), (3, 0), (3, 3)):              # bar B bar D
        cell_box(ax, 0.0, 0.0, r, c, HILITE)
    marker(ax, 0.0, 0.0, 0, 0, '3', HILITE)
    legend = [('1', r'$C$  rows CD = 11, 10  (uses X at m10, m11, m14, m15)',
               ACCENT),
              ('2', r'$A$  columns AB = 11, 10  (uses X at m10 ... m15)',
               HILITE),
              ('3', r'$\bar{B}\bar{D}$  four corners, wrap-around  (uses X at m10)',
               HILITE)]
    for i, (tag, text, color) in enumerate(legend):
        y = -0.95 - i * 0.44
        ax.text(-1.05, y, tag, ha='right', va='center', fontsize=10.5,
                color=color)
        ax.text(-0.75, y, text, ha='left', va='center', fontsize=10.5,
                color=INK)
    box = FancyBboxPatch((-1.05, -2.95), 6.4, 0.62,
                         boxstyle='round,pad=0.10,rounding_size=0.12',
                         facecolor=FILL, edgecolor=HILITE, lw=BOX_LW,
                         zorder=2)
    ax.add_patch(box)
    ax.text(2.15, -2.64, r'$Y = A + C + \bar{B}\bar{D}$   (3 terms, 4 literals)',
            ha='center', va='center', fontsize=13, color=HILITE, zorder=3)


def build_figure():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.6, 7.6))
    panel_a(ax1)
    panel_b(ax2)
    fig.tight_layout()
    return fig


# ------------------------------------------------------------- verification --
def evaluate(terms, dont_cares=()):
    """Evaluate a sum-of-products over all 16 input combinations."""
    out = {}
    for m in range(16):
        bits = [(m >> (3 - k)) & 1 for k in range(4)]
        out[m] = 1 if any(all(bits[v] == val for v, val in t) for t in terms) else 0
    return out


def main():
    apply_mpl_style()
    save_fig(build_figure(), 'kmap-dont-care')

    # ---- the check the note quotes -----------------------------------------
    got = evaluate(FINAL)
    ok_ones = all(got[m] == 1 for m in ONES)
    ok_zeros = all(got[m] == 0 for m in ZEROS)
    print('check  map 1s %s | 0s %s | X %s'
          % (sorted(ONES), sorted(ZEROS), sorted(DCS)))
    print('check  Y = A + C + barB barD  ->  %s'
          % ''.join(str(got[m]) for m in range(16)))
    print('check  every 1 covered: %s | every 0 respected: %s | X values chosen: %s'
          % (ok_ones, ok_zeros,
             ''.join(str(got[m]) for m in sorted(DCS))))
    old = evaluate(NO_DC)
    print('check  X forced to 0: %s  -> terms/literals 3/8 vs 3/4 with X'
          % ''.join(str(old[m]) for m in range(16)))


if __name__ == '__main__':
    main()
