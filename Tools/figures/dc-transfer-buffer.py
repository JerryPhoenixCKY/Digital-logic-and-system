"""dc-transfer-buffer -- the DC transfer characteristic (V_out vs V_in) of a buffer.

Panel (a): the ideal buffer.  The VTC is a single step at V_in = V_M = V_DD/2,
so V_IL = V_IH = V_DD/2, V_OL = 0, V_OH = V_DD and

    NM_H = V_OH - V_IH = V_DD/2,   NM_L = V_IL - V_OL = V_DD/2,
    NM_H + NM_L = V_DD.

Panel (b): a real buffer (V_DD = 5 V, V_IL = 2.0 V, V_IH = 3.0 V).  The
transition region has a finite width W = V_IH - V_IL, so the V_DD budget splits
into NM_L + W + NM_H and

    NM_H + NM_L = V_DD - (V_IH - V_IL) = 5.0 - 1.0 = 4.0 V < V_DD,

with NM_H = NM_L = 2.0 V, i.e. each is still below V_DD/2 = 2.5 V.  The stacked
bar under both curves shows that budget split; V_M is the point where the curve
crosses V_out = V_in.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

apply_mpl_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

VDD = 5.0
VIL, VIH = 2.0, 3.0          # real buffer transition band (panel b)
VM = 0.5 * (VIL + VIH)

XLIM = (-1.0, 6.0)
YLIM = (-2.70, 5.85)
BAR_Y0, BAR_Y1 = -1.95, -1.30


def frame(ax, title):
    ax.set_title(title, loc='left', fontsize=13)
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_xticks(range(0, 6))
    ax.set_yticks(range(0, 6))
    ax.set_xlabel('$V_{in}$ (V)')
    ax.set_ylabel('$V_{out}$ (V)')
    ax.grid(False)


def budget_bar(ax, splits, labels):
    """Stacked V_DD budget under the VTC: [NM_L][W][NM_H] from 0 to V_DD."""
    edges = [0.0] + list(splits) + [VDD]
    for i in range(len(edges) - 1):
        x0, x1 = edges[i], edges[i + 1]
        ax.add_patch(Rectangle((x0, BAR_Y0), x1 - x0, BAR_Y1 - BAR_Y0,
                               facecolor=FILL, edgecolor=GOOD, lw=1.4,
                               zorder=2))
    for x in splits:
        ax.plot([x, x], [BAR_Y0, BAR_Y1], color=INK, lw=1.4, zorder=3)
    for x0, x1, txt in labels:
        ax.text((x0 + x1) / 2, (BAR_Y0 + BAR_Y1) / 2, txt, ha='center',
                va='center', fontsize=10, color=INK, zorder=4)


fig, (axa, axb) = plt.subplots(1, 2, figsize=(13.0, 6.6))

# =========================================================== (a) ideal buffer
frame(axa, '(a) Ideal buffer: step VTC, transition width W = 0')
axa.plot([0.0, VDD / 2], [0.0, 0.0], color=INK)
axa.plot([VDD / 2, VDD], [VDD, VDD], color=INK)
axa.plot([VDD / 2, VDD / 2], [0.0, VDD], color=HILITE, ls=(0, (4, 3)))
axa.plot([VDD / 2, VDD / 2], [0.0, VDD], ls='none', marker='o', ms=6,
         color=HILITE)

axa.text(0.12, 4.35, '$V_{OH} = V_{DD} = 5$ V', ha='left', va='center',
         fontsize=10.5, color=ACCENT)
axa.text(0.12, 0.30, '$V_{OL} = 0$', ha='left', va='center', fontsize=10.5,
         color=ACCENT)
axa.add_patch(FancyArrowPatch((0.05, 0.95), (VDD / 2, 0.95),
                              arrowstyle='<|-|>', color=GOOD,
                              mutation_scale=14, zorder=5))
axa.text(VDD / 4, 1.35, '$NM_L = 2.5$ V', ha='center', va='center',
         fontsize=11, color=GOOD,
         bbox=dict(boxstyle='square,pad=0.16', fc='white', ec='none'))
axa.add_patch(FancyArrowPatch((VDD / 2, 4.85), (VDD, 4.85),
                              arrowstyle='<|-|>', color=GOOD,
                              mutation_scale=14, zorder=5))
axa.text(0.75 * VDD, 5.22, '$NM_H = 2.5$ V', ha='center', va='center',
         fontsize=11, color=GOOD)
axa.text(VDD / 2, -0.45, '$V_{IL} = V_{IH} = V_M = 2.5$ V', ha='center',
         va='center', fontsize=10.5, color=HILITE)
budget_bar(axa, [VDD / 2], [(0.0, VDD / 2, 'NM_L 2.5'),
                            (VDD / 2, VDD, 'NM_H 2.5')])
axa.text(VDD / 2, -2.32,
         '$NM_H + NM_L = 2.5 + 2.5 = 5.0$ V $= V_{DD}$', ha='center',
         va='center', fontsize=11.5, color=HILITE)

# =========================================================== (b) real buffer
frame(axb, '(b) Real buffer: transition band W = 1.0 V')
t = np.linspace(0.0, 1.0, 240)
vout = VDD * (3 * t ** 2 - 2 * t ** 3)
vin = VIL + t * (VIH - VIL)
axb.plot([0.0, VIL], [0.0, 0.0], color=INK)
axb.plot(vin, vout, color=HILITE, ls=(0, (5, 2)))
axb.plot([VIH, VDD], [VDD, VDD], color=INK)
for x in (VIL, VIH):
    axb.plot([x, x], [0.0, VDD], color=MUTED, ls=(0, (4, 3)), lw=1.3)
axb.plot([0.0, VDD], [0.0, VDD], color=MUTED, ls=':', lw=1.3, zorder=1)
axb.plot([VM], [VM], ls='none', marker='o', ms=6, color=HILITE, zorder=5)

axb.text(0.12, 4.35, '$V_{OH} = V_{DD} = 5$ V', ha='left', va='center',
         fontsize=10.5, color=ACCENT)
axb.text(0.12, 0.30, '$V_{OL} = 0$', ha='left', va='center', fontsize=10.5,
         color=ACCENT)
axb.text(4.35, 4.05, '$V_{out} = V_{in}$', ha='right', va='bottom',
         fontsize=10, color=MUTED,
         bbox=dict(boxstyle='square,pad=0.14', fc='white', ec='none'))
axb.text(VM + 0.12, 2.12, '$V_M = 2.5$ V', ha='left', va='center',
         fontsize=11, color=HILITE,
         bbox=dict(boxstyle='square,pad=0.16', fc='white', ec='none'))
axb.add_patch(FancyArrowPatch((0.05, 0.95), (VIL, 0.95),
                              arrowstyle='<|-|>', color=GOOD,
                              mutation_scale=14, zorder=5))
axb.text(VIL / 2, 1.35, '$NM_L = 2.0$ V', ha='center', va='center',
         fontsize=11, color=GOOD,
         bbox=dict(boxstyle='square,pad=0.16', fc='white', ec='none'))
axb.add_patch(FancyArrowPatch((VIH, 4.85), (VDD, 4.85),
                              arrowstyle='<|-|>', color=GOOD,
                              mutation_scale=14, zorder=5))
axb.text(0.5 * (VIH + VDD), 5.22, '$NM_H = 2.0$ V', ha='center', va='center',
         fontsize=11, color=GOOD)
axb.text(VIL, -0.45, '$V_{IL} = 2.0$ V', ha='center', va='center',
         fontsize=10.5, color=HILITE)
axb.text(VIH, -0.88, '$V_{IH} = 3.0$ V', ha='center', va='center',
         fontsize=10.5, color=HILITE)
budget_bar(axb, [VIL, VIH], [(0.0, VIL, 'NM_L 2.0'),
                             (VIL, VIH, 'W 1.0'),
                             (VIH, VDD, 'NM_H 2.0')])
axb.text(VDD / 2, -2.32,
         '$NM_L + W + NM_H = 2.0 + 1.0 + 2.0 = 5.0$ V $= V_{DD}$',
         ha='center', va='center', fontsize=11.5, color=HILITE)

save_fig(fig, 'dc-transfer-buffer')
