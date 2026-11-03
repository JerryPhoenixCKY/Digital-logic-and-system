"""IEEE 754 single precision: 32-bit field layout + the two worked examples.

Bit 31 = sign, bits 30..23 = biased exponent (stored = E + 127), bits 22..0 =
fraction field.  The leading '1.' of the normalised mantissa is implicit and is
never stored, so 23 stored bits give 24 significant bits.

    228.0    ->  0 10000110 11001000000000000000000  = 0x43640000
    -58.25   ->  1 10000100 11010010000000000000000  = 0xC2690000
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

W = 1.0        # one bit column
H = 0.80       # row height
GAP = 0.12


def cell_style(i):
    """Colour key used by every row: sign / exponent / fraction."""
    if i == 0:
        return HILITE, "white"
    if 1 <= i <= 8:
        return ACCENT, "white"
    return FILL, INK


def bit_row(ax, bits, y):
    for i, b in enumerate(bits):
        face, txt = cell_style(i)
        ax.add_patch(Rectangle((i * W, y), W - GAP, H, facecolor=face,
                               edgecolor=INK, zorder=2))
        ax.text(i * W + (W - GAP) / 2, y + H / 2, b, ha="center", va="center",
                fontsize=9, color=txt, zorder=3)


apply_mpl_style()
fig, ax = plt.subplots(figsize=(15.5, 7.4))
ax.set_xlim(-5.6, 33.6)
ax.set_ylim(-1.7, 7.1)
ax.set_axis_off()
ax.set_title("IEEE 754 single precision (binary32): 1 + 8 + 23 bits")

# ---------------------------------------------------------- field layout row
ax.add_patch(Rectangle((0.0, 5.20), 1.0 - GAP, H, facecolor=HILITE,
                       edgecolor=INK, zorder=2))
ax.text(0.44, 5.60, "S", ha="center", va="center", fontsize=11, color="white",
        zorder=3)
ax.add_patch(Rectangle((1.0, 5.20), 8.0 - GAP, H, facecolor=ACCENT,
                       edgecolor=INK, zorder=2))
ax.text(4.44, 5.60, "E  (8 bits)", ha="center", va="center", fontsize=11,
        color="white", zorder=3)
ax.add_patch(Rectangle((9.0, 5.20), 23.0 - GAP, H, facecolor=FILL,
                       edgecolor=INK, zorder=2))
ax.text(20.44, 5.60, "F  (23 stored bits)", ha="center", va="center",
        fontsize=11, color=INK, zorder=3)

# the hidden leading 1 sits immediately left of the stored fraction
ax.add_patch(Rectangle((8.55, 6.05), 0.90, 0.45, facecolor="white",
                       edgecolor=HILITE, linestyle=(0, (3, 2)), zorder=2))
ax.text(9.00, 6.28, "1.", ha="center", va="center", fontsize=11, color=HILITE,
        zorder=3)
ax.text(9.75, 6.28, "implicit leading 1 - never stored (23 + 1 = 24 bits)",
        ha="left", va="center", fontsize=10.5, color=HILITE)

# ------------------------------------------------------------- bit numbering
for i in range(32):
    ax.text(i * W + (W - GAP) / 2, 5.05, str(31 - i), ha="center", va="top",
            fontsize=8, color=MUTED)
ax.text(-0.35, 5.05, "bit", ha="right", va="top", fontsize=9, color=MUTED)

# --------------------------------------------------------- field captions
ax.text(0.50, 4.55, "sign", ha="center", va="center", fontsize=10.5)
ax.text(5.00, 4.55, "exponent = E + 127", ha="center", va="center",
        fontsize=10.5)
ax.text(20.50, 4.55, "fraction bits (23)", ha="center", va="center",
        fontsize=10.5)

# ------------------------------------------------------------- 228 example
E228 = "0" + "10000110" + "11001" + "0" * 18
bit_row(ax, E228, 3.30)
ax.text(-0.45, 3.70, "228 =", ha="right", va="center", fontsize=11.5)
ax.text(-5.45, 2.80,
        "228 = 1110 0100 = 1.11001 x 2^7   ->   exponent stored as 127 + 7 = 134 "
        "= 1000 0110   ->   0x43640000",
        ha="left", va="center", fontsize=10.5, color=INK)
ax.plot([-5.5, 32.5], [2.35, 2.35], color=MUTED, linestyle=(0, (4, 4)))

# ----------------------------------------------------------- -58.25 example
E58 = "1" + "10000100" + "1101001" + "0" * 16
bit_row(ax, E58, 1.55)
ax.text(-0.45, 1.95, "-58.25 =", ha="right", va="center", fontsize=11.5)
ax.text(-5.45, 1.05,
        "58.25 = 111010.01 = 1.1101001 x 2^5   ->   exponent stored as 127 + 5 = 132 "
        "= 1000 0100   ->   0xC2690000",
        ha="left", va="center", fontsize=10.5, color=INK)

# ------------------------------------------------------------------- notes
ax.text(-5.45, 0.15,
        "value $= (-1)^{S}\\times 1.F\\times 2^{E}$      with      "
        "$E$ = exponent field - 127  (bias 127 = 0111 1111)",
        ha="left", va="center", fontsize=10.5, color=INK)
ax.text(-5.45, -0.60,
        "exponent field runs 0 ... 255, so E runs -127 ... +128; field 0 and field 255 "
        "are reserved for 0 / denormals / infinities / NaN",
        ha="left", va="center", fontsize=10.5, color=MUTED)
ax.text(-5.45, -1.30,
        "the 23 stored bits plus the implicit 1 give 24 significant bits  "
        "~  7 significant decimal digits",
        ha="left", va="center", fontsize=10.5, color=ACCENT)

save_fig(fig, "ieee754-single-format")
