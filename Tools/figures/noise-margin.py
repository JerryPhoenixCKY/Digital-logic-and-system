"""noise-margin -- how much the signal may degrade before the logic value flips.

Both panels put the four guaranteed numbers of one logic family on the same
vertical voltage axis: V_OH / V_OL (what a driver promises) and V_IH / V_IL
(what a receiver demands).  The shaded bands are the noise margins

    NM_H = V_OH - V_IH,        NM_L = V_IL - V_OL

i.e. the allowed loss of a HIGH and of a LOW.  Panel (a) is TTL at 5 V
(NM_H = NM_L = 0.4 V, lecture p.23), panel (b) is LVCMOS at 3.3 V
(NM_H = 0.9 V, NM_L = 0.54 V).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

apply_mpl_style()

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

TTL = dict(name='TTL', vdd=5.0, vil=0.8, vih=2.0, vol=0.4, voh=2.4)
LVCMOS = dict(name='LVCMOS', vdd=3.3, vil=0.9, vih=1.8, vol=0.36, voh=2.7)

X0, X1 = 0.35, 9.65          # the four lines span this range
LX = 9.60                    # right-aligned line labels
AX_X = 1.00                  # x of the two double arrows


def panel(ax, spec, title):
    ax.set_title(title, loc='left', fontsize=13)
    ax.set_xlim(0.0, 10.0)
    ax.set_ylim(-0.95, 5.95)
    ax.set_xticks([])
    ax.set_yticks(range(0, 6))
    ax.set_ylabel('Voltage (V)')
    ax.grid(False)
    for side in ('bottom', 'top', 'right'):
        ax.spines[side].set_visible(False)

    voh, vih, vil, vol = spec['voh'], spec['vih'], spec['vil'], spec['vol']

    # the two noise-margin bands and the forbidden band in between
    ax.add_patch(Rectangle((X0, vih), X1 - X0, voh - vih, facecolor=FILL,
                           edgecolor=GOOD, lw=1.4, zorder=1))
    ax.add_patch(Rectangle((X0, vol), X1 - X0, vil - vol, facecolor=FILL,
                           edgecolor=GOOD, lw=1.4, zorder=1))
    ax.add_patch(Rectangle((X0, vil), X1 - X0, vih - vil, facecolor='white',
                           edgecolor=MUTED, hatch='///', lw=1.2, zorder=1))

    # output limits (solid) and input thresholds (dashed)
    for y, col, ls in ((voh, ACCENT, '-'), (vih, HILITE, (0, (5, 3))),
                       (vil, HILITE, (0, (5, 3))), (vol, ACCENT, '-')):
        ax.plot([X0, X1], [y, y], color=col, ls=ls, zorder=4)

    for y, txt, col in ((voh, '$V_{OH}$ = %.2f' % voh, ACCENT),
                        (vih, '$V_{IH}$ = %.2f' % vih, HILITE),
                        (vil, '$V_{IL}$ = %.2f' % vil, HILITE),
                        (vol, '$V_{OL}$ = %.2f' % vol, ACCENT)):
        ax.text(LX, y + 0.13, txt, ha='right', va='center', fontsize=11,
                color=col, zorder=6,
                bbox=dict(boxstyle='square,pad=0.16', fc='white', ec='none'))

    # NM_H and NM_L with double arrows and the worked-out numbers
    ax.add_patch(FancyArrowPatch((AX_X, vih), (AX_X, voh), arrowstyle='<|-|>',
                                 color=GOOD, mutation_scale=14, zorder=5))
    ax.text(AX_X + 0.22, (vih + voh) / 2,
            '$NM_H = V_{OH} - V_{IH} = %.2f - %.2f = %.2f$ V'
            % (voh, vih, voh - vih), ha='left', va='center', fontsize=11,
            color=GOOD, zorder=6,
            bbox=dict(boxstyle='square,pad=0.18', fc='white', ec='none'))
    ax.add_patch(FancyArrowPatch((AX_X, vol), (AX_X, vil), arrowstyle='<|-|>',
                                 color=GOOD, mutation_scale=14, zorder=5))
    ax.text(AX_X + 0.22, (vol + vil) / 2,
            '$NM_L = V_{IL} - V_{OL} = %.2f - %.2f = %.2f$ V'
            % (vil, vol, vil - vol), ha='left', va='center', fontsize=11,
            color=GOOD, zorder=6,
            bbox=dict(boxstyle='square,pad=0.18', fc='white', ec='none'))

    ax.text(4.0, (vil + vih) / 2,
            'forbidden band  %.2f - %.2f V:  the logic value is undefined'
            % (vil, vih), ha='center', va='center', fontsize=10.5, color=BAD,
            zorder=6, bbox=dict(boxstyle='square,pad=0.18', fc='white',
                                ec='none'))

    ax.text(X0, 5.42, 'driver promises  $V_{out} \\geq V_{OH}$  for a 1',
            ha='left', va='center', fontsize=10.5, color=ACCENT)
    ax.text(X0, 4.86, 'receiver demands  $V_{in} \\geq V_{IH}$  for a 1',
            ha='left', va='center', fontsize=10.5, color=HILITE)
    ax.text(X0, -0.44, 'worst case only: $V_{OH}$(min), $V_{IH}$(min),',
            ha='left', va='center', fontsize=10.5, color=MUTED)
    ax.text(X0, -0.80, '$V_{IL}$(max), $V_{OL}$(max) - datasheet limits',
            ha='left', va='center', fontsize=10.5, color=MUTED)


fig, (axa, axb) = plt.subplots(1, 2, figsize=(13.0, 6.4))
panel(axa, TTL, '(a) TTL at 5 V:  $NM_H$ = $NM_L$ = 0.4 V')
panel(axb, LVCMOS, '(b) LVCMOS at 3.3 V:  $NM_H$ = 0.9 V, $NM_L$ = 0.54 V')

save_fig(fig, 'noise-margin')
