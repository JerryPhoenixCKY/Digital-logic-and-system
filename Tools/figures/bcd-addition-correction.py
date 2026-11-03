"""Figure: BCD addition and the +6 (0110) correction.

Panel (a): 8 + 5.  Binary addition gives 1101, which is *not* a legal BCD
nibble (only 0000..1001 are), so the result is corrected by adding 0110:
1101 + 0110 = 1 0011, i.e. tens digit 1 and ones digit 3 -> BCD 0001 0011.

Panel (b): 9 + 9.  Here the nibble addition carries out of the group, the
second condition that triggers the correction: 1 0010 + 0110 = 1 1000 ->
BCD 0001 1000 = 18.

Why 0110?  BCD skips six of the sixteen four-bit codes (1010 ... 1111), so
binary counting runs six steps ahead of BCD counting; adding 6 realigns them.

Column arithmetic with bit fields, so matplotlib.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

MONO = 'DejaVu Sans Mono'


def cells(ax, x0, y, bits, cellw=0.72, cellh=0.78, face=FILL, edge=INK,
          color=INK, lw=1.4, fs=12.5):
    """Draw one bit string as a row of cells; returns the right edge."""
    x = x0
    for b in bits:
        ax.add_patch(Rectangle((x, y - cellh / 2), cellw, cellh,
                               facecolor=face, edgecolor=edge, lw=lw,
                               zorder=2))
        ax.text(x + cellw / 2, y, b, ha='center', va='center', color=color,
                fontsize=fs, family=MONO, zorder=3)
        x += cellw
    return x


def draw_column(ax, a, b, title, sum_tag, judge_lines, tail):
    """One BCD addition worked out as a vertical column."""
    ax.set_xlim(0.0, 10.0)
    ax.set_ylim(0.25, 10.6)
    ax.axis('off')

    xb = 2.6                      # left edge of the 4-bit nibble
    xc = xb - 0.80                # left edge of the carry cell

    # ---- the two addends -------------------------------------------------
    ax.text(0.25, 8.75, r'$%d_{10}$' % a, ha='left', va='center',
            fontsize=14, color=INK)
    ax.text(0.25, 7.75, r'$%d_{10}$' % b, ha='left', va='center',
            fontsize=14, color=INK)
    ax.text(2.25, 7.75, '+', ha='center', va='center', fontsize=15,
            color=HILITE)
    cells(ax, xb, 8.75, format(a, '04b'))
    cells(ax, xb, 7.75, format(b, '04b'))
    ax.plot([xb, xb + 4 * 0.72], [7.18, 7.18], color=INK, lw=1.6)

    # ---- raw binary sum (5 bits: carry + nibble) -------------------------
    s = a + b
    carry, low = s >> 4, s & 0xF
    tag_col = BAD if low > 9 else HILITE
    cells(ax, xc, 6.40, str(carry), face='white',
          edge=HILITE if carry else MUTED,
          color=HILITE if carry else MUTED, lw=1.8)
    cells(ax, xb, 6.40, format(low, '04b'), face='white',
          edge=BAD if low > 9 else INK,
          color=BAD if low > 9 else INK, lw=1.8 if low > 9 else 1.4)
    ax.text(5.78, 6.40, sum_tag, ha='left', va='center', fontsize=12,
            color=tag_col)
    ax.annotate('', xy=(2.32, 5.30), xytext=(5.72, 5.72),
                arrowprops=dict(arrowstyle='->', color=HILITE, lw=1.4,
                                connectionstyle='arc3,rad=0.22'))

    # ---- correction row --------------------------------------------------
    ax.text(2.25, 4.85, '+', ha='center', va='center', fontsize=15,
            color=HILITE)
    cells(ax, xb, 4.85, '0110', face='white', edge=HILITE, color=HILITE,
          lw=1.8)
    ax.text(5.78, 4.85, 'add 6', ha='left', va='center', fontsize=12,
            color=HILITE)
    ax.plot([xb, xb + 4 * 0.72], [4.28, 4.28], color=INK, lw=1.6)

    # ---- corrected result ------------------------------------------------
    f = s + 6
    fc, fl = f >> 4, f & 0xF
    cells(ax, xc, 3.50, str(fc), face='white', edge=HILITE, color=HILITE,
          lw=1.8)
    cells(ax, xb, 3.50, format(fl, '04b'), face='white', edge=GOOD,
          color=GOOD, lw=1.8)
    ax.text(5.78, 3.50, 'ok', ha='left', va='center', fontsize=12,
            color=GOOD)

    ax.text(xb, 2.45, 'BCD  %s %s  = %d'
            % (format(fc, '04b'), format(fl, '04b'), 10 * fc + fl),
            ha='left', va='center', fontsize=13, family=MONO, color=GOOD)
    ax.text(xb, 1.72, tail, ha='left', va='center', fontsize=11, color=MUTED)
    ax.text(xb, 0.98, judge_lines[0], ha='left', va='center', fontsize=11,
            color=tag_col)
    ax.text(xb, 0.55, judge_lines[1], ha='left', va='center', fontsize=11,
            color=tag_col)

    ax.set_title(title)


def build_figure():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 6.8))
    draw_column(
        ax1, 8, 5,
        r'(a) $8 + 5$: nibble sum $1101 > 1001$',
        '= 13  >  9',
        ['judging point: the 4-bit sum 1101',
         'is above 1001, so 0110 is added'],
        'the adding itself was a plain binary add')
    draw_column(
        ax2, 9, 9,
        r'(b) $9 + 9$: carry out of the nibble',
        'carry out',
        ['judging point: the addition carries',
         'out of the group, so 0110 is added'],
        'nibble 0010 alone looks legal; the carry gives it away')
    fig.text(0.5, 0.012,
             'the correction is 6 because BCD skips exactly 6 of the 16 '
             'four-bit codes (1010 ... 1111)',
             ha='center', va='center', fontsize=11.5, color=HILITE)
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    return fig


def main():
    apply_mpl_style()
    fig = build_figure()
    save_fig(fig, 'bcd-addition-correction')

    # ---- numbers the note quotes -------------------------------------------
    for a, b in ((8, 5), (9, 9)):
        s = a + b
        f = s + 6
        print('check  %d + %d : %s + %s = %s (carry %d, nibble %s)'
              % (a, b, format(a, '04b'), format(b, '04b'), format(s, '05b'),
                 s >> 4, format(s & 0xF, '04b')))
        print('       +0110 -> %s -> carry %d, nibble %s -> BCD %s %s = %d'
              % (format(f, '05b'), f >> 4, format(f & 0xF, '04b'),
                 format(f >> 4, '04b'), format(f & 0xF, '04b'),
                 10 * (f >> 4) + (f & 0xF)))
    print('check  illegal BCD codes skipped: %s'
          % ' '.join(format(v, '04b') for v in range(10, 16)))


if __name__ == '__main__':
    main()
