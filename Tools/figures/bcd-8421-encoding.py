"""Figure: the 8421 BCD code (Binary Coded Decimal).

Panel (a): all sixteen four-bit codes.  Ten of them carry a decimal digit
(0-9); the six codes 1010..1111 have no digit and are therefore illegal.
Those six codes are exactly what the +6 correction in BCD addition skips.

Panel (b): decimal -> BCD is a per-digit translation, not a base conversion:
every decimal digit becomes its own four-bit group, so 170 needs three groups
and 2469 needs four.  Reading BCD back starts from the right, four bits at a
time (slide p.65).

Everything is a bit field / table, so matplotlib is the right tool.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

MONO = 'DejaVu Sans Mono'


def bit_row(ax, x0, y, bits, cellw, cellh, face=FILL, edge=INK, color=INK,
            lw=1.4, fs=12.5):
    """Draw one bit string as a row of filled cells.  Returns the right edge."""
    x = x0
    for b in bits:
        ax.add_patch(Rectangle((x, y - cellh / 2), cellw, cellh,
                               facecolor=face, edgecolor=edge, lw=lw,
                               zorder=2))
        ax.text(x + cellw / 2, y, b, ha='center', va='center', color=color,
                fontsize=fs, family=MONO, zorder=3)
        x += cellw
    return x


def panel_a(ax):
    """The 16 four-bit codes; legal BCD digits vs the 6 illegal codes."""
    ax.set_xlim(-0.15, 7.6)
    ax.set_ylim(-0.4, 18.6)
    ax.axis('off')

    ax.text(0.55, 17.75, 'Decimal', ha='center', va='center', fontsize=11.5)
    for i, w in enumerate('8421'):
        ax.text(1.76 + i * 0.72, 17.75, w, ha='center', va='center',
                fontsize=12.5, color=ACCENT, family=MONO)
    ax.text(4.62, 17.75, 'legal BCD?', ha='left', va='center', fontsize=11.5,
            color=INK)
    ax.plot([0.0, 7.5], [17.3, 17.3], color=INK, lw=1.2)

    for v in range(16):
        y = 16.6 - v * 0.98
        legal = v < 10
        bit_row(ax, 1.4, y, format(v, '04b'), cellw=0.72, cellh=0.80,
                face=FILL if legal else 'white',
                edge=INK if legal else BAD,
                color=INK if legal else BAD, lw=1.4 if legal else 1.8)
        ax.text(0.55, y, str(v), ha='center', va='center', fontsize=12.5,
                family=MONO, color=INK)
        if legal:
            ax.text(4.62, y, 'yes  (digit %d)' % v, ha='left', va='center',
                    fontsize=11, color=GOOD)
        else:
            ax.text(4.62, y, 'no   (illegal code)', ha='left', va='center',
                    fontsize=11, color=BAD)

    ax.text(0.1, 1.05, '10 codes used, 6 codes skipped (1010 ... 1111)',
            ha='left', va='center', fontsize=11.5, color=HILITE)
    ax.text(0.1, 0.25, 'these 6 unused codes are why BCD addition adds 0110',
            ha='left', va='center', fontsize=11.5, color=HILITE)

    ax.set_title('(a) 16 four-bit codes: 10 digits, 6 illegal')


def panel_b(ax):
    """170 and 2469: one 4-bit group per decimal digit."""
    ax.set_xlim(0.0, 13.4)
    ax.set_ylim(0.4, 10.9)
    ax.axis('off')

    cellw, cellh, x0, pitch = 0.60, 0.72, 2.2, 2.8

    def band(top, number, note):
        digits = str(number)
        # decimal digit boxes
        for i, d in enumerate(digits):
            gx = x0 + i * pitch
            ax.add_patch(Rectangle((gx, top - 0.85), 4 * cellw, 0.85,
                                   facecolor=FILL, edgecolor=INK, lw=1.4,
                                   zorder=2))
            ax.text(gx + 2 * cellw, top - 0.425, d, ha='center', va='center',
                    fontsize=13.5, family=MONO, color=INK, zorder=3)
            ax.plot([gx + 2 * cellw, gx + 2 * cellw],
                    [top - 0.85, top - 1.05], color=MUTED, ls=':', lw=1.2)
            bit_row(ax, gx, top - 1.45, format(int(d), '04b'),
                    cellw=cellw, cellh=cellh)
        ax.text(0.15, top - 0.42, r'$%d_{10}$' % number, ha='left',
                va='center', fontsize=14, color=HILITE)
        bcd = ' '.join(format(int(d), '04b') for d in digits)
        ax.text(x0, top - 2.12, 'BCD:  ' + bcd, ha='left', va='center',
                fontsize=12.5, family=MONO, color=INK)
        ax.text(x0, top - 2.62, note, ha='left', va='center', fontsize=11,
                color=MUTED)

    band(10.4, 170, '3 decimal digits -> 3 four-bit groups')
    band(5.6, 2469, '4 decimal digits -> 4 four-bit groups')

    ax.text(0.15, 1.85, 'each decimal digit is translated on its own;',
            ha='left', va='center', fontsize=11.5, color=INK)
    ax.text(0.15, 1.20, 'BCD is NOT binary:  $13_{10}$ = BCD 0001 0011,'
                        ' but binary 13 = 1101',
            ha='left', va='center', fontsize=11.5, color=BAD)

    ax.set_title('(b) decimal -> BCD: one 4-bit group per decimal digit')


def build_figure():
    """Assemble the two panels (kept apart from main() so it can be re-checked)."""
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(13.2, 7.0), gridspec_kw={'width_ratios': [0.82, 1.18]})
    panel_a(ax1)
    panel_b(ax2)
    fig.tight_layout()
    return fig


def main():
    apply_mpl_style()
    fig = build_figure()
    save_fig(fig, 'bcd-8421-encoding')

    # ---- numbers the note quotes -------------------------------------------
    for n in (170, 2469):
        s = ' '.join(format(int(d), '04b') for d in str(n))
        print('check  BCD %d = %s' % (n, s))
    print('check  16 codes - 10 digits = %d illegal codes: %s'
          % (16 - 10, ' '.join(format(v, '04b') for v in range(10, 16))))
    print('check  13 -> BCD 0001 0011 (= %d read as plain binary) vs binary 1101 (= 13)'
          % int('00010011', 2))


if __name__ == '__main__':
    main()
