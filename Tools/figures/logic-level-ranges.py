"""logic-level-ranges -- voltage ranges (not single points) carry the logic value.

Panel (a): the four parameters on one vertical voltage axis.  A driver only
guarantees V_out <= V_OL for a 0 and V_out >= V_OH for a 1; a receiver only
promises to read V_in <= V_IL as 0 and V_in >= V_IH as 1.  Everything between
V_IL and V_IH is the transition band, where the logic value is undefined.
(TTL 5 V numbers are used as the worked example.)

Panel (b): the same voltage axis with the two families of lecture p.23 --
TTL at 5 V and LVCMOS at 3.3 V -- so each family's four numbers and the width
of its forbidden band can be read off directly.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

apply_mpl_style()

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

TTL = dict(vdd=5.0, vil=0.8, vih=2.0, vol=0.4, voh=2.4)
LVCMOS = dict(vdd=3.3, vil=0.9, vih=1.8, vol=0.36, voh=2.7)

YLIM = (-1.30, 5.90)


def region(ax, x0, x1, y0, y1, fc=FILL, ec=INK, hatch=None, lw=1.2):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=fc,
                           edgecolor=ec, hatch=hatch, lw=lw, zorder=1))


def level_line(ax, x0, x1, y, color, label=None, lx=None, fs=11.0):
    ax.plot([x0, x1], [y, y], color=color, ls=(0, (5, 3)), zorder=4)
    if label:
        ax.text(lx, y, label, ha='left', va='center', fontsize=fs, color=color,
                zorder=6, bbox=dict(boxstyle='square,pad=0.18', fc='white',
                                    ec='none'))


fig, (axa, axb) = plt.subplots(1, 2, figsize=(14.0, 6.4))

# =========================================================== panel (a)
axa.set_title('(a) Four parameters, one vertical voltage axis', loc='left',
              fontsize=13)
axa.set_xlim(0.0, 10.0)
axa.set_ylim(*YLIM)
axa.set_xticks([])
axa.set_yticks(range(0, 6))
axa.set_ylabel('Voltage (V)')
axa.grid(False)
for side in ('bottom', 'top', 'right'):
    axa.spines[side].set_visible(False)

CX0, CX1 = 0.70, 3.30
region(axa, CX0, CX1, 0.0, TTL['vil'], fc=FILL, ec=INK)
region(axa, CX0, CX1, TTL['vil'], TTL['vih'], fc='white', ec=MUTED, hatch='///')
region(axa, CX0, CX1, TTL['vih'], TTL['vdd'], fc=FILL, ec=INK)
region(axa, CX0, CX1, 0.0, TTL['vdd'], fc='none', ec=INK, lw=1.8)

axa.text((CX0 + CX1) / 2, 0.40, 'logic 0', ha='center', va='center',
         fontsize=11, color=INK, zorder=6)
axa.text((CX0 + CX1) / 2, 3.50, 'logic 1', ha='center', va='center',
         fontsize=11, color=INK, zorder=6)
axa.text((CX0 + CX1) / 2, 1.40, 'transition\nband', ha='center', va='center',
         fontsize=10, color=INK, zorder=6,
         bbox=dict(boxstyle='square,pad=0.16', fc='white', ec='none'))

level_line(axa, CX0, 9.60, TTL['vdd'], MUTED, '$V_{DD}$ = 5 V   (supply)', 3.45)
level_line(axa, CX0, 9.60, TTL['voh'], ACCENT,
           '$V_{OH}$ = 2.4 V   min output HIGH', 3.45)
level_line(axa, CX0, 9.60, TTL['vih'], HILITE,
           '$V_{IH}$ = 2.0 V   min input HIGH', 3.45)
level_line(axa, CX0, 9.60, TTL['vil'], HILITE,
           '$V_{IL}$ = 0.8 V   max input LOW', 3.45)
level_line(axa, CX0, 9.60, TTL['vol'], ACCENT,
           '$V_{OL}$ = 0.4 V   max output LOW', 3.45)
level_line(axa, CX0, 3.20, 0.0, MUTED, 'GND = 0 V', 3.45)

axa.text(0.70, -0.62,
         'receiver rule:   $V_{in} \\geq V_{IH}$ -> logic 1 ,   '
         '$V_{in} \\leq V_{IL}$ -> logic 0',
         ha='left', va='center', fontsize=11, color=INK)
axa.text(0.70, -1.05,
         'in between (the transition band): the logic value is undefined',
         ha='left', va='center', fontsize=11, color=BAD)

# =========================================================== panel (b)
axb.set_title('(b) TTL 5 V and LVCMOS 3.3 V (lecture p.23)', loc='left',
              fontsize=13)
axb.set_xlim(0.0, 10.0)
axb.set_ylim(*YLIM)
axb.set_xticks([])
axb.set_yticks(range(0, 6))
axb.set_ylabel('Voltage (V)')
axb.grid(False)
for side in ('bottom', 'top', 'right'):
    axb.spines[side].set_visible(False)


def family(ax, xc, w, spec, title, w_pct):
    x0, x1 = xc - w / 2, xc + w / 2
    region(ax, x0, x1, 0.0, spec['vil'], fc=FILL, ec=INK)
    region(ax, x0, x1, spec['vil'], spec['vih'], fc='white', ec=MUTED,
           hatch='///')
    region(ax, x0, x1, spec['vih'], spec['vdd'], fc=FILL, ec=INK)
    region(ax, x0, x1, 0.0, spec['vdd'], fc='none', ec=INK, lw=1.8)
    ax.text(xc, spec['vdd'] + 0.22, title, ha='center', va='bottom',
            fontsize=11.5, color=INK)
    for key, sym, col in (('voh', 'V_{OH}', ACCENT), ('vih', 'V_{IH}', HILITE),
                          ('vil', 'V_{IL}', HILITE), ('vol', 'V_{OL}', ACCENT)):
        y = spec[key]
        ax.plot([x0, x1], [y, y], color=col, ls=(0, (5, 3)), zorder=4)
        ax.text(xc, y, '$%s$ %.2f' % (sym, y), ha='center', va='center',
                fontsize=10.5, color=col, zorder=6,
                bbox=dict(boxstyle='square,pad=0.16', fc='white', ec='none'))
    band = spec['vih'] - spec['vil']
    ax.text(xc, -0.62, 'transition band %.1f V' % band, ha='center',
            va='center', fontsize=10.5, color=BAD)
    ax.text(xc, -1.05, '= %.0f%% of $V_{DD}$' % w_pct, ha='center',
            va='center', fontsize=10.5, color=MUTED)


family(axb, 2.50, 2.60, TTL, 'TTL @ 5 V', 24.0)
family(axb, 7.50, 2.60, LVCMOS, 'LVCMOS @ 3.3 V', 27.3)

save_fig(fig, 'logic-level-ranges')
