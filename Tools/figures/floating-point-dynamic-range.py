"""Dynamic range of IEEE 754 single precision vs. a fixed-point format.

Both formats spend their bits very differently: Q4.4 spans only
[0.0625, 15.9375] (2.4 decades of magnitude), while binary32 covers the normal
numbers 2^-126 ... (2 - 2^-23) x 2^127, i.e. about 76.5 decades.  The ends of
the exponent field are reserved: all-zero encodes 0 (and denormals), all-one
encodes +/-infinity and NaN.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

SMALL = 2.0 ** -126                  # 1.1754943508222875e-38  smallest normal
LARGE = (2 - 2 ** -23) * 2 ** 127    # 3.4028234663852886e+38  largest normal
QMIN, QMAX = 0.0625, 15.9375         # Q4.4 magnitude span

apply_mpl_style()
fig, ax = plt.subplots(figsize=(13.0, 6.2))

ax.set_xscale("log")
ax.set_xlim(1e-40, 1e41)
ax.set_ylim(-4.0, 2.4)
# pin the decade ticks to the visible window: LogLocator would otherwise also
# emit 10^50 / 10^60 ticks whose labels fall outside the canvas
ax.set_xticks([1e-40, 1e-30, 1e-20, 1e-10, 1e0, 1e10, 1e20, 1e30, 1e40])

# ------------------------------------------------------------- magnitude axis
ax.axhline(0.0, color=INK, zorder=3)

# ------------------------------------------------------------ float32 normals
ax.add_patch(Rectangle((SMALL, 0.22), LARGE - SMALL, 0.30, facecolor=FILL,
                       edgecolor=ACCENT, zorder=2))
ax.plot([SMALL, SMALL], [-0.45, 0.95], color=ACCENT, linestyle=(0, (2, 2)))
ax.plot([LARGE, LARGE], [-0.45, 0.95], color=ACCENT, linestyle=(0, (2, 2)))
ax.text(1.6e-38, 1.05, "smallest normal\n$2^{-126}$ = 1.18e-38", ha="left",
        va="center", fontsize=10.5, color=ACCENT)
ax.text(1.1e38, 1.05, "largest normal\n$(2-2^{-23})\\times 2^{127}$ = 3.40e38",
        ha="right", va="center", fontsize=10.5, color=ACCENT)
ax.text(1.2e-38, 0.60,
        "IEEE 754 single precision: normal numbers, ~76.5 decades",
        ha="left", va="center", fontsize=11, color=ACCENT)

# --------------------------------------------------------------- the examples
ax.plot([58.25, 58.25], [0.0, 1.45], color=MUTED, linestyle=(0, (2, 2)))
ax.plot([228.0, 228.0], [0.0, 1.45], color=MUTED, linestyle=(0, (2, 2)))
ax.text(70.0, 1.62, "58.25", ha="right", va="center", fontsize=11, color=INK)
ax.text(190.0, 1.62, "228", ha="left", va="center", fontsize=11, color=INK)

# ------------------------------------------------------------------- zero end
ax.plot([3.0e-40], [0.0], marker="o", markersize=8, color=HILITE, zorder=5)
ax.text(3.5e-40, -0.45, "0", ha="left", va="center", fontsize=11, color=HILITE)

# ------------------------------------------------------- Q4.4 comparison bar
ax.add_patch(Rectangle((QMIN, -0.98), QMAX - QMIN, 0.30, facecolor=FILL,
                       edgecolor=HILITE, zorder=2))
ax.plot([QMIN, QMIN], [-1.30, -0.60], color=HILITE, linestyle=(0, (2, 2)))
ax.plot([QMAX, QMAX], [-1.30, -0.60], color=HILITE, linestyle=(0, (2, 2)))
ax.annotate("Q4.4 fixed point: $|x|$ in [0.0625, 15.9375]\n"
            "= only 2.4 decades of magnitude",
            xy=(QMIN, -0.86), xytext=(1.05e-40, -1.80), ha="left", va="center",
            fontsize=11, color=HILITE,
            arrowprops=dict(arrowstyle="->", color=HILITE))

# ------------------------------------------------------------- special values
ax.text(1.05e-40, -2.35,
        "0 :  exponent = 0000 0000, fraction = 0 (sign bit ignored)",
        ha="left", va="center", fontsize=10.5, color=HILITE)
ax.text(1e41, -2.35,
        "$\\pm\\infty$ :  exponent = 1111 1111, fraction = 0",
        ha="right", va="center", fontsize=10.5, color=BAD)
ax.text(1e41, -2.95,
        "NaN :  exponent = 1111 1111, fraction $\\neq$ 0",
        ha="right", va="center", fontsize=10.5, color=BAD)
ax.text(1.0, -3.55,
        "same bits, opposite trade-off:  binary32 keeps ~76.5 decades at a 2^-24 relative "
        "step;  Q4.4 has an exact 2^-4 step",
        ha="center", va="center", fontsize=10.5, color=INK)

ax.set_xlabel("magnitude $|x|$   (logarithmic scale, one tick = 10 decades)")
ax.set_title("Where the representable numbers live: binary32 vs. Q4.4 fixed point")

save_fig(fig, "floating-point-dynamic-range")
