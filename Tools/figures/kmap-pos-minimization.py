"""Figure: POS and SOP minimisation on one and the same K-map (slide p.56).

The standard POS expression of slide p.56 is prod M(1,2,3,4,9,12): exactly six
cells of the 4-variable map are 0 and the other ten are 1.

Panel (a)  circle the 0s.  Every circle is read as one maxterm: a variable that
           is 0 all over the circle is written as itself, a variable that is 1
           all over it is written complemented, and the maxterms are ANDed.
           -> min POS = (A+B+bar C)(B+C+bar D)(bar B+C+D)
Panel (b)  circle the 1s on the same map, read every circle as a product term
           (1 -> the variable, 0 -> its complement) and OR them.
           -> min SOP = bar B bar C bar D + BD + BC + AC

Both answers describe the same function; the point of the figure is that the
SOP answer and the POS answer come out of the same picture.

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

# standard POS of slide p.56:  prod M(1,2,3,4,9,12)
ZEROS = {1, 2, 3, 4, 9, 12}
ONES = {m for m in range(16) if m not in ZEROS}

# every circle is an explicit list of cells; `wrap` marks an edge-to-edge group
POS_GROUPS = [
    dict(cells=[(2, 0), (3, 0)], text=r'$(A+B+\bar{C})$', mk=(2, 0), tag='1'),
    dict(cells=[(1, 0), (1, 3)], text=r'$(B+C+\bar{D})$', mk=(1, 3), tag='2',
         wrap=True),
    dict(cells=[(0, 1), (0, 2)], text=r'$(\bar{B}+C+D)$', mk=(0, 1), tag='3'),
]
SOP_GROUPS = [
    dict(cells=[(1, 1), (1, 2), (2, 1), (2, 2)], text=r'$BD$', mk=(1, 1),
         tag='1'),
    dict(cells=[(2, 1), (2, 2), (3, 1), (3, 2)], text=r'$BC$', mk=(3, 1),
         tag='2'),
    dict(cells=[(2, 2), (2, 3), (3, 2), (3, 3)], text=r'$AC$', mk=(3, 3),
         tag='3'),
    dict(cells=[(0, 0), (0, 3)], text=r'$\bar{B}\bar{C}\bar{D}$', mk=(0, 0),
         tag='4', wrap=True),
]


def minterm(r, c):
    ab, cd = int(GRAY2[c], 2), int(GRAY2[r], 2)
    return 8 * ((ab >> 1) & 1) + 4 * (ab & 1) + 2 * ((cd >> 1) & 1) + (cd & 1)


def draw_map(ax, x0, y0, title, keep):
    n = 4
    ax.set_xlim(x0 - 2.0, x0 + 6.0)
    ax.set_ylim(y0 - 5.0, y0 + 5.4)
    ax.axis('off')
    for r in range(n):
        for c in range(n):
            m = minterm(r, c)
            yb = y0 + (n - 1 - r)
            ax.add_patch(Rectangle((x0 + c, yb), 1, 1, facecolor='white',
                                   edgecolor=INK, lw=CELL_LW, zorder=2))
            v = '1' if m in ONES else '0'
            ax.text(x0 + c + 0.5, yb + 0.52, v, ha='center', va='center',
                    fontsize=15, zorder=4, color=INK if v == keep else MUTED)
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
    ax.text(x0 - 1.30, y0 + 2.0, 'CD', ha='center', va='center', fontsize=12,
            color=HILITE, zorder=3)
    ax.text(x0 + 2.0, y0 + n + 1.05, title, ha='center', va='bottom',
            fontsize=12.5, color=INK, zorder=3)


def shade(ax, x0, y0, r, c):
    ax.add_patch(Rectangle((x0 + c, y0 + 3 - r), 1, 1, facecolor=FILL,
                           edgecolor='none', zorder=1))


def group_box(ax, x0, y0, cells, pad=0.09):
    """Rounded outline around the bounding rectangle of a rectangular group."""
    rows = [r for r, _ in cells]
    cols = [c for _, c in cells]
    r0, r1, c0, c1 = min(rows), max(rows), min(cols), max(cols)
    ax.add_patch(FancyBboxPatch(
        (x0 + c0 + pad, y0 + (3 - r1) + pad),
        (c1 - c0 + 1) - 2 * pad, (r1 - r0 + 1) - 2 * pad,
        boxstyle='round,pad=0,rounding_size=0.18', facecolor='none',
        edgecolor=HILITE, lw=BOX_LW, zorder=6))


def cell_box(ax, x0, y0, r, c, pad=0.08):
    ax.add_patch(FancyBboxPatch(
        (x0 + c + pad, y0 + (3 - r) + pad), 1 - 2 * pad, 1 - 2 * pad,
        boxstyle='round,pad=0,rounding_size=0.16', facecolor=FILL,
        edgecolor=HILITE, lw=BOX_LW, zorder=6))


def wrap_frame(ax, x0, y0):
    """Dashed frame around the map: opposite edges of the map are joined."""
    pad = 0.32
    ax.add_patch(FancyBboxPatch(
        (x0 - pad, y0 - pad), 4 + 2 * pad, 4 + 2 * pad,
        boxstyle='round,pad=0,rounding_size=0.30', facecolor='none',
        edgecolor=HILITE, lw=BOX_LW - 0.4, ls=(0, (4, 3)), zorder=5))


def marker(ax, x0, y0, r, c, text):
    ax.text(x0 + c + 0.20, y0 + (3 - r) + 0.80, text, ha='center',
            va='center', fontsize=11, color=HILITE, zorder=8)


def panel(ax, groups, title, keep, head, expr, note):
    """keep='0' -> POS (circle the 0s); keep='1' -> SOP (circle the 1s)."""
    x0, y0 = 0.0, 0.0
    draw_map(ax, x0, y0, title, keep)
    any_wrap = False
    for i, g in enumerate(groups):
        for r, c in g['cells']:
            if ('1' if minterm(r, c) in ONES else '0') == keep:
                shade(ax, x0, y0, r, c)
        if g.get('wrap'):
            any_wrap = True
            for r, c in g['cells']:
                cell_box(ax, x0, y0, r, c)
        else:
            group_box(ax, x0, y0, g['cells'], pad=0.09 + 0.11 * (i % 3))
        marker(ax, x0, y0, g['mk'][0], g['mk'][1], g['tag'])
    if any_wrap:
        wrap_frame(ax, x0, y0)
    for i, g in enumerate(groups):
        ax.text(4.40, 3.40 - i * 0.52, g['tag'] + ' = ' + g['text'], ha='left',
                va='center', fontsize=11, color=INK)
    ax.text(4.40, 3.40 - len(groups) * 0.52 - 0.18, head, ha='left',
            va='center', fontsize=11, color=HILITE)
    ax.add_patch(FancyBboxPatch((-1.10, -2.10), 7.0, 0.62,
                                boxstyle='round,pad=0.10,rounding_size=0.12',
                                facecolor=FILL, edgecolor=HILITE, lw=BOX_LW,
                                zorder=2))
    ax.text(2.40, -1.79, expr, ha='center', va='center', fontsize=13,
            color=HILITE, zorder=3)
    ax.text(-1.05, -2.80, note, ha='left', va='center', fontsize=10.5,
            color=MUTED)
    if any_wrap:
        ax.text(1.95, -3.55, 'dashed frame: the left and right map edges are joined',
                ha='center', va='center', fontsize=9.5, color=HILITE)


def build_figure():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.6, 8.2))
    panel(ax1, POS_GROUPS,
          '(a) POS: circle the 0s  (same map)', '0',
          'min POS = product of the three sums',
          r'$(A+B+\bar{C})(B+C+\bar{D})(\bar{B}+C+D)$',
          '3 sums, 9 literals')
    panel(ax2, SOP_GROUPS,
          '(b) SOP: circle the 1s  (same map)', '1',
          'min SOP = sum of the four products',
          r'$\bar{B}\bar{C}\bar{D} + BD + BC + AC$',
          '4 products, 9 literals')
    fig.tight_layout()
    return fig


# ------------------------------------------------------------- verification --
def evaluate(terms):
    """Evaluate a sum-of-products over all 16 input combinations."""
    out = {}
    for m in range(16):
        bits = [(m >> (3 - k)) & 1 for k in range(4)]
        out[m] = 1 if any(all(bits[v] == val for v, val in t) for t in terms) else 0
    return out


def evaluate_pos(sums):
    """Evaluate a product-of-sums; (var, comp) -> comp=1 means complemented."""
    out = {}
    for m in range(16):
        bits = [(m >> (3 - k)) & 1 for k in range(4)]
        val = 1
        for s in sums:
            v = 0
            for var, comp in s:
                v |= (1 - bits[var]) if comp else bits[var]
            val &= v
        out[m] = val
    return out


def main():
    apply_mpl_style()
    save_fig(build_figure(), 'kmap-pos-minimization')

    # ---- the check the note quotes -----------------------------------------
    truth = {m: (0 if m in ZEROS else 1) for m in range(16)}
    truth_s = ''.join(str(truth[m]) for m in range(16))
    pos_s = evaluate_pos([[(0, 0), (1, 0), (2, 1)], [(1, 0), (2, 0), (3, 1)],
                          [(1, 1), (2, 0), (3, 0)]])
    sop_terms = [[(1, 0), (2, 0), (3, 0)], [(1, 1), (3, 1)],
                 [(1, 1), (2, 1)], [(0, 1), (2, 1)]]
    sop_s = evaluate(sop_terms)
    print('check  standard POS prod M(1,2,3,4,9,12) -> %s' % truth_s)
    print('check  min POS (A+B+Cbar)(B+C+Dbar)(Bbar+C+D) -> %s  %s'
          % (''.join(str(pos_s[m]) for m in range(16)),
             'MATCH' if all(pos_s[m] == truth[m] for m in range(16))
             else 'MISMATCH'))
    print('check  min SOP BbarCbarDbar + BD + BC + AC     -> %s  %s'
          % (''.join(str(sop_s[m]) for m in range(16)),
             'MATCH' if all(sop_s[m] == truth[m] for m in range(16))
             else 'MISMATCH'))
    print('check  zeros %s   ones %s' % (sorted(ZEROS), sorted(ONES)))
    print('check  standard SOP = sum m%s' % sorted(ONES))
    # every circle must hold cells of one value only, and cover everything
    for name, groups, keep in (('POS', POS_GROUPS, '0'), ('SOP', SOP_GROUPS, '1')):
        covered = set()
        for g in groups:
            vals = ''.join('1' if minterm(r, c) in ONES else '0'
                           for r, c in g['cells'])
            covered |= {minterm(r, c) for r, c in g['cells']}
            print('check  %s circle %s = %-16s cells m%s -> values %s'
                  % (name, g['tag'], g['text'], [minterm(r, c) for r, c in g['cells']],
                     vals))
        need = {m for m in range(16) if ('1' if m in ONES else '0') == keep}
        print('check  %s: every %s covered: %s'
              % (name, keep, need <= covered))


if __name__ == '__main__':
    main()
