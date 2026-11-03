"""ASCII code map: 7-bit code split into high nibble (row) x low nibble (column).

Row = bits 6..4 (high nibble 0x0-0xF), column = bits 3..0 (low nibble 0x0-0xF).
Cell colour encodes the block structure of the standard: control characters,
symbols / space, digits, upper case and lower case letters.  The three anchor
codes '0' = 0x30, 'A' = 0x41 and 'a' = 0x61 are ringed.  Rows 0x8-0xF are the
8-bit extension (Latin-1, code pages) and are NOT part of 7-bit ASCII.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

apply_mpl_style()

CONTROL, SYMBOL, DIGIT, UPPER, LOWER, EXT = BAD, FILL, GOOD, ACCENT, HILITE, "#ffffff"
WHITE = "#ffffff"


def category(code: int) -> str:
    if code > 0x7F:
        return "ext"
    if code < 0x20 or code == 0x7F:
        return "control"
    if 0x30 <= code <= 0x39:
        return "digit"
    if 0x41 <= code <= 0x5A:
        return "upper"
    if 0x61 <= code <= 0x7A:
        return "lower"
    return "symbol"


FACE = {"control": CONTROL, "symbol": SYMBOL, "digit": DIGIT,
        "upper": UPPER, "lower": LOWER, "ext": EXT}
TEXT = {"control": WHITE, "symbol": INK, "digit": WHITE,
        "upper": WHITE, "lower": WHITE, "ext": MUTED}
ANCHORS = (0x30, 0x41, 0x61)


def cell_text(code: int) -> str:
    if code == 0x20:
        return "SP"
    if code == 0x7F:
        return "DEL"
    if code < 0x20 or code > 0x7E:
        return ""
    return chr(code)


fig, ax = plt.subplots(figsize=(11.0, 7.8))

for hi in range(16):            # row = high nibble
    for lo in range(16):        # column = low nibble
        code = (hi << 4) | lo
        cat = category(code)
        ax.add_patch(Rectangle((lo + 0.04, hi + 0.04), 0.92, 0.92,
                               facecolor=FACE[cat], edgecolor=INK,
                               linewidth=0.8, zorder=2,
                               hatch="////" if cat == "ext" else None))
        label = cell_text(code)
        if label:
            size = 9.0 if len(label) > 1 else 10.5
            ax.text(lo + 0.5, hi + 0.5, label, ha="center", va="center",
                    color=TEXT[cat], fontsize=size, zorder=3,
                    fontweight="bold" if code in ANCHORS else "normal")
        if code in ANCHORS:
            ax.add_patch(FancyBboxPatch((lo + 0.14, hi + 0.14), 0.72, 0.72,
                                        boxstyle="round,pad=0.02,rounding_size=0.12",
                                        facecolor="none", edgecolor=WHITE,
                                        linewidth=2.6, zorder=4))

# boundary between 7-bit ASCII and the 8-bit extension
ax.plot([-0.02, 16.02], [8.0, 8.0], color=INK, linewidth=2.4, zorder=5)
ax.text(16.25, 7.9, "ASCII ends here:\n0x00-0x7F = 128 codes (7 bits)",
        ha="left", va="bottom", fontsize=10.5, color=INK)
ax.text(16.25, 8.1, "8-bit extension 0x80-0xFF\n(Latin-1, code pages;\nnot ASCII)",
        ha="left", va="top", fontsize=10.5, color=MUTED)

ax.set_xlim(-0.75, 21.9)
ax.set_ylim(16.45, -2.05)
ax.set_xticks([c + 0.5 for c in range(16)])
ax.set_xticklabels([f"0x{c:X}" for c in range(16)], fontsize=11)
ax.set_yticks([r + 0.5 for r in range(16)])
ax.set_yticklabels([f"0x{r:X}" for r in range(16)], fontsize=11)
ax.xaxis.set_ticks_position("top")
ax.xaxis.set_label_position("top")
ax.set_xlabel("low nibble  (bits 3..0)   ->   column index", fontsize=12)
ax.set_ylabel("high nibble  (bits 6..4)   ->   row index", fontsize=12)
ax.set_axisbelow(True)
ax.grid(False)
for side in ("top", "right", "bottom", "left"):
    ax.spines[side].set_visible(False)
ax.tick_params(length=0)

ax.text(-0.75, -1.72, "code = high nibble x 16 + low nibble          "
        "0x00-0x7F = 128 code words, 0x20-0x7E = 95 printable",
        ha="left", va="center", fontsize=12, color=INK, fontweight="bold")

handles = [
    Rectangle((0, 0), 1, 1, facecolor=CONTROL, edgecolor=INK,
              label="control chars  0x00-0x1F, 0x7F"),
    Rectangle((0, 0), 1, 1, facecolor=SYMBOL, edgecolor=INK,
              label="symbols + SP  0x20-0x2F, 0x3A-0x40, 0x5B-0x60, 0x7B-0x7E"),
    Rectangle((0, 0), 1, 1, facecolor=DIGIT, edgecolor=INK,
              label="digits '0'-'9'  0x30-0x39"),
    Rectangle((0, 0), 1, 1, facecolor=UPPER, edgecolor=INK,
              label="upper case 'A'-'Z'  0x41-0x5A"),
    Rectangle((0, 0), 1, 1, facecolor=LOWER, edgecolor=INK,
              label="lower case 'a'-'z'  0x61-0x7A"),
]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.42, -0.012),
          ncol=2, frameon=False, fontsize=11, handlelength=1.6,
          handleheight=1.0, labelspacing=0.5)

fig.text(0.5, -0.055,
         "Ringed anchors:  '0' = 0x30,  'A' = 0x41,  'a' = 0x61    |    "
         "digit code = 0x30 + digit    |    'a' - 'A' = 0x20 (bit 5 only)",
         ha="center", va="center", fontsize=11.5, color=INK)

save_fig(fig, "ascii-code-structure")
