"""hex-memory-address.svg -- a byte-addressed memory view in hexadecimal.

Eight bytes ("ECE2050!") stored from address 0x0000; every byte is shown as two
hex digits and expanded into its two nibbles (bits 7-4 on the left = MSB nibble,
bits 3-0 on the right = LSB nibble), so that "2 hex digits = 1 byte" and
"1 hex digit = 4 bits = 1 nibble" are visible at a glance.

Used by Notes/Hexadecimal Number System.md.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

apply_mpl_style()

DATA = b"ECE2050!"                    # 8 bytes -> addresses 0x0000 .. 0x0007
START = 0x0000

XLIM, YLIM = (0.0, 13.0), (0.1, 12.7)
BYTE_X, BYTE_W = 1.95, 0.63
HN_X, LN_X, BPITCH, BWID = 4.20, 8.05, 0.72, 0.62
ROW0, RPITCH = 10.40, 1.00
NIB_SEP = 7.50

fig, ax = plt.subplots(figsize=(13.0, 7.6))
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_title("Memory is addressed byte by byte: 2 hex digits = 1 byte", pad=14)

# ---------------------------------------------------------------- header -----
ax.text(1.30, 12.10, "address", ha="center", va="center", fontsize=11,
        color=INK)
ax.text(2.60, 12.10, "byte", ha="center", va="center", fontsize=11, color=INK)
ax.text(5.60, 12.10, "high nibble", ha="center", va="center", fontsize=11,
        color=INK)
ax.text(9.45, 12.10, "low nibble", ha="center", va="center", fontsize=11,
        color=INK)
ax.text(11.30, 12.10, "ASCII", ha="center", va="center", fontsize=11,
        color=INK)
ax.text(2.60, 11.55, "2 hex digits", ha="center", va="center", fontsize=9,
        color=MUTED)
ax.text(5.60, 11.55, "bits 7-4  =  MSB nibble", ha="center", va="center",
        fontsize=9, color=HILITE)
ax.text(9.45, 11.55, "bits 3-0  =  LSB nibble", ha="center", va="center",
        fontsize=9, color=HILITE)
ax.text(11.30, 11.55, "character", ha="center", va="center", fontsize=9,
        color=MUTED)

ax.plot([NIB_SEP, NIB_SEP], [2.95, 10.85], color=MUTED, linestyle="--",
        zorder=2)
ax.text(NIB_SEP, 10.95, "nibble boundary", ha="center", va="bottom", fontsize=9,
        color=MUTED)

# ------------------------------------------------------------------ rows -----
for i, byte in enumerate(DATA):
    y = ROW0 - i * RPITCH
    last = i == len(DATA) - 1
    ax.text(1.72, y, f"0x{START + i:04X}", ha="right", va="center",
            fontsize=10.5, color=HILITE if last else INK, family="DejaVu Sans Mono")
    if last:
        ax.text(1.05, y, "last byte", ha="right", va="center", fontsize=9,
                color=HILITE)
    for j, ch in enumerate(f"{byte:02X}"):
        ax.add_patch(Rectangle((BYTE_X + j * (BYTE_W + 0.04), y - 0.30),
                               BYTE_W, 0.60, zorder=3, facecolor=FILL,
                               edgecolor=INK))
        ax.text(BYTE_X + j * (BYTE_W + 0.04) + BYTE_W / 2, y, ch, ha="center",
                va="center", fontsize=11, color=INK, zorder=4,
                family="DejaVu Sans Mono")
    ax.annotate("", xy=(HN_X - 0.18, y), xytext=(BYTE_X + 2 * BYTE_W + 0.12, y),
                arrowprops=dict(arrowstyle="->", color=MUTED, shrinkA=0,
                                shrinkB=0))
    for j, bit in enumerate(f"{byte:08b}"):
        x0 = HN_X if j < 4 else LN_X
        x = x0 + (j % 4) * BPITCH
        ax.add_patch(Rectangle((x, y - 0.30), BWID, 0.60, zorder=3,
                               facecolor=FILL if bit == "1" else "white",
                               edgecolor=INK))
        ax.text(x + BWID / 2, y, bit, ha="center", va="center", fontsize=10.5,
                color=INK, zorder=4, family="DejaVu Sans Mono")
    ax.text(11.30, y, chr(byte), ha="center", va="center", fontsize=12,
            color=ACCENT, family="DejaVu Sans Mono")

ax.annotate("", xy=(1.78, ROW0 - 7 * RPITCH),
            xytext=(1.05, ROW0 - 7 * RPITCH),
            arrowprops=dict(arrowstyle="->", color=HILITE, shrinkA=3,
                            shrinkB=0))

# ----------------------------------------------------------------- footer ----
ax.text(0.20, 2.35, "1 byte = 8 bits = 2 hex digits = 2 nibbles;  "
                    "1 hex digit = 4 bits = 1 nibble",
        ha="left", va="center", fontsize=9.5, color=INK)
ax.text(0.20, 1.70, "8 bytes stored from $0x0000$: last byte address = "
                    "$0x0000 + 8 - 1 = 0x0007$",
        ha="left", va="center", fontsize=9.5, color=INK)
ax.text(0.20, 1.05, "one byte covers $0x00$-$0xFF$, i.e. 256 values "
                    "$[0, 255]$; MSB is written on the left, LSB on the right",
        ha="left", va="center", fontsize=9.5, color=INK)

fig.tight_layout()
save_fig(fig, "hex-memory-address")
