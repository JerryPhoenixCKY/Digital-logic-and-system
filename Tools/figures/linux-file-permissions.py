"""linux-file-permissions.svg -- one octal digit = three bits (rwx).

Top   : chmod 644 / 755 / 754 expanded into three groups of three bits, with the
        octal digit above each group, the rwx string below it and its 4/2/1
        decode underneath.
Bottom: the complete octal digit <-> rwx table for 0-7.

Used by Notes/Octal Number System.md.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

apply_mpl_style()

XLIM, YLIM = (0.0, 12.6), (0.0, 11.2)
BOX_W, BOX_GAP = 0.55, 0.09
GROUP_W = 3 * BOX_W + 2 * BOX_GAP            # 1.83
GROUP_X = [2.35, 5.15, 7.95]
GROUP_C = [gx + GROUP_W / 2 for gx in GROUP_X]

EXAMPLES = [
    ("644", "110100100", "rw-r--r--", ["4+2", "4", "4"],
     ["owner: read + write", "group: read", "others: read"]),
    ("755", "111101101", "rwxr-xr-x", ["4+2+1", "4+1", "4+1"],
     ["owner: read + write + execute", "group: read + execute",
      "others: read + execute"]),
    ("754", "111101100", "rwxr-xr--", ["4+2+1", "4+1", "4"],
     ["owner: read + write + execute", "group: read + execute",
      "others: read"]),
]

fig, ax = plt.subplots(figsize=(13.0, 8.0))
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_title("Linux file permissions are octal: each octal digit packs one rwx group",
             pad=14)

for (octal, bits, rwx, decode, meaning), y in zip(EXAMPLES, [9.6, 7.0, 4.4]):
    ax.text(0.15, y + 1.02, f"chmod {octal}", ha="left", va="center",
            fontsize=13, color=INK, family="DejaVu Sans Mono")
    for g in range(3):
        ax.text(GROUP_C[g], y + 1.02, octal[g], ha="center", va="center",
                fontsize=16, fontweight="bold", color=HILITE)
        ax.text(GROUP_C[g], y - 0.72, rwx[g * 3:g * 3 + 3], ha="center",
                va="center", fontsize=12, color=INK,
                family="DejaVu Sans Mono")
        ax.text(GROUP_C[g], y - 1.20, decode[g], ha="center", va="center",
                fontsize=9, color=MUTED)
        ax.plot([GROUP_X[g], GROUP_X[g] + GROUP_W], [y - 0.30, y - 0.30],
                color=MUTED, zorder=2)
        for xb in (GROUP_X[g], GROUP_X[g] + GROUP_W):
            ax.plot([xb, xb], [y - 0.30, y - 0.18], color=MUTED, zorder=2)
        for j in range(3):
            x = GROUP_X[g] + j * (BOX_W + BOX_GAP)
            bit = bits[g * 3 + j]
            ax.add_patch(Rectangle((x, y - 0.13), BOX_W, 0.62, zorder=3,
                                   facecolor=FILL if bit == "1" else "white",
                                   edgecolor=INK))
            ax.text(x + BOX_W / 2, y + 0.18, bit, ha="center", va="center",
                    fontsize=11, color=INK, zorder=4)
    for k, line in enumerate(meaning):
        ax.text(10.15, y + 0.42 - 0.30 * k, line, ha="left", va="center",
                fontsize=9.5, color=INK)

# ------------------------------------------------ the 0-7 table (bottom) ----
ax.text(0.20, 2.80,
        "one octal digit = exactly three bits = one rwx group "
        "(weights $4/2/1$: $6=4+2$, $5=4+1$, $4=4$)",
        ha="left", va="center", fontsize=10.5, fontweight="bold", color=INK)

RWX = {0: "---", 1: "--x", 2: "-w-", 3: "-wx", 4: "r--", 5: "r-x", 6: "rw-",
       7: "rwx"}
for d in range(8):
    cx = 0.20 + d * 1.55
    ax.add_patch(Rectangle((cx, 0.20), 1.43, 2.30, zorder=2,
                           facecolor=FILL, edgecolor=MUTED))
    ax.text(cx + 0.715, 2.22, f"{d}", ha="center", va="center", fontsize=14,
            fontweight="bold", color=HILITE, zorder=4)
    for j, bit in enumerate(f"{d:03b}"):
        x = cx + 0.115 + j * 0.42
        ax.add_patch(Rectangle((x, 1.10), 0.36, 0.60, zorder=3,
                               facecolor="white", edgecolor=INK))
        ax.text(x + 0.18, 1.40, bit, ha="center", va="center", fontsize=8.5,
                color=INK, zorder=4)
    ax.text(cx + 0.715, 0.62, RWX[d], ha="center", va="center", fontsize=11,
            color=INK, family="DejaVu Sans Mono", zorder=4)

fig.tight_layout()
save_fig(fig, "linux-file-permissions")
