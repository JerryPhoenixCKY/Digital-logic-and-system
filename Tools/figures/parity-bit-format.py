"""Parity bit: (a) even/odd parity on a 7-bit data word, (b) the two-bit blind spot.

(a) data word 110 1001 -> even parity appends P = 0, odd parity appends P = 1.
(b) a two-bit error (one 1->0 and one 0->1) keeps the number of 1s unchanged,
    so the even-parity check still passes and the error is invisible.

Data-space layout: one data unit is ~1 % of the figure width, so long English
labels live in wide side columns (LEFT / RIGHT) that the bit cells never enter.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

apply_mpl_style()

DATA = "1101001"            # 7 data bits, 4 ones
EVEN_WORD = DATA + "0"      # 1101 0010 -> 4 ones (even)
ODD_WORD = DATA + "1"       # 1101 0011 -> 5 ones (odd)
SENT = EVEN_WORD            # 1101 0010
RECV = "01010110"           # bit 1 (1->0) and bit 6 (0->1): still 4 ones
FLIPPED = (0, 5)

assert DATA.count("1") == 4
assert EVEN_WORD.count("1") == 4 and ODD_WORD.count("1") == 5
assert len(RECV) == 8 and RECV.count("1") == 4
assert [i for i in range(8) if RECV[i] != SENT[i]] == list(FLIPPED)

CELL, GAP, PITCH = 0.86, 0.34, 1.0
LEFT, RIGHT = -3.05, 9.9         # x of the short left labels / right verdicts
XMIN, XMAX = -3.2, 16.9


def cell_x(i):
    """x of the left edge of bit i (the two 4-bit groups are separated)."""
    return i * PITCH + GAP * (i // 4)


def draw_row(ax, y, bits, *, edge=None, face=None, mark=(), parity=False,
             text_color=None, size=14):
    edge = edge or {}
    face = face or {}
    text_color = text_color or {}
    for i, b in enumerate(bits):
        is_p = parity and i == len(bits) - 1
        ec = edge.get(i, HILITE if is_p else INK)
        fc = face.get(i, FILL if b == "1" else "white")
        lw = 2.6 if (i in mark or is_p) else 1.1
        ax.add_patch(Rectangle((cell_x(i), y), CELL, CELL, facecolor=fc,
                               edgecolor=ec, linewidth=lw, zorder=2))
        ax.text(cell_x(i) + CELL / 2, y + CELL / 2, b, ha="center",
                va="center", fontsize=size, color=text_color.get(i, INK),
                fontweight="bold" if (i in mark or is_p) else "normal",
                zorder=3)


fig, (axa, axb) = plt.subplots(2, 1, figsize=(11.4, 7.6))

# ------------------------------------------------------------------ panel (a)
axa.set_title("(a) one attached bit forces the total number of 1s to be "
              "always even or always odd")
axa.text(LEFT, 5.15, "data word  $d_1\\!\\cdots d_7$ = 110 1001    ->    "
         "4 ones inside the data word", fontsize=12, color=INK, va="center")

# --- even parity row
draw_row(axa, 2.75, EVEN_WORD, parity=True)
for i in range(8):
    axa.text(cell_x(i) + CELL / 2, 3.95, "$d_%d$" % (i + 1) if i < 7 else "$P$",
             ha="center", va="center", fontsize=11.5,
             color=HILITE if i == 7 else INK)
axa.text(LEFT, 3.20, "EVEN parity", fontsize=12.5, color=GOOD,
         fontweight="bold", va="center")
axa.text(LEFT, 2.45, "P = 1^1^0^1^0^0^1 = 0", fontsize=11, color=INK,
         va="center")
axa.text(RIGHT, 3.70, "total 1s = 4 + 0 = 4  (even)", fontsize=11.5, color=GOOD,
         fontweight="bold", va="center")
axa.text(RIGHT, 3.25, "parity check passes", fontsize=11.5, color=GOOD,
         va="center")
axa.text(RIGHT, 2.75, "word sent:  1101 0010", fontsize=11.5, color=INK,
         va="center")

# --- odd parity row
draw_row(axa, 0.60, ODD_WORD, parity=True)
axa.text(LEFT, 1.05, "ODD parity", fontsize=12.5, color=ACCENT,
         fontweight="bold", va="center")
axa.text(LEFT, 0.30, "P = NOT(0) = 1", fontsize=11, color=INK, va="center")
axa.text(RIGHT, 1.55, "total 1s = 4 + 1 = 5  (odd)", fontsize=11.5,
         color=ACCENT, fontweight="bold", va="center")
axa.text(RIGHT, 1.10, "parity check passes", fontsize=11.5, color=ACCENT,
         va="center")
axa.text(RIGHT, 0.60, "word sent:  1101 0011", fontsize=11.5, color=INK,
         va="center")

axa.text(LEFT, -0.55, "shaded cell = bit is 1     red frame = parity bit P "
         "(appended after the data bits)", fontsize=11, color=MUTED,
         va="center")
axa.set_xlim(XMIN, XMAX)
axa.set_ylim(-0.95, 5.55)
axa.axis("off")

# ------------------------------------------------------------------ panel (b)
axb.set_title("(b) blind spot: two flipped bits cancel each other")
axb.text(LEFT, 3.05, "transmitted", fontsize=12, color=INK, va="center")
draw_row(axb, 2.00, SENT, parity=True)
axb.text(RIGHT, 3.05, "even parity word  1101 0010", fontsize=11.5, color=INK,
         va="center")
axb.text(RIGHT, 2.45, "4 ones  ->  parity check passes", fontsize=11.5,
         color=GOOD, va="center")

axb.text(LEFT, 1.05, "received", fontsize=12, color=INK, va="center")
draw_row(axb, 0.00, RECV, mark=FLIPPED, edge={i: BAD for i in FLIPPED},
         text_color={i: BAD for i in FLIPPED})
axb.text(RIGHT, 1.05, "bit 1:  1 -> 0   (removes a 1)", fontsize=11.5,
         color=BAD, va="center")
axb.text(RIGHT, 0.45, "bit 6:  0 -> 1   (adds a 1)", fontsize=11.5,
         color=BAD, va="center")

for i, lab in zip(FLIPPED, ("1 -> 0", "0 -> 1")):
    x = cell_x(i) + CELL / 2
    axb.annotate("", xy=(x, 1.95), xytext=(x, 0.93),
                 arrowprops=dict(arrowstyle="-|>", color=BAD, linewidth=2.0,
                                 shrinkA=1, shrinkB=1))
    axb.text(x, 1.44, lab, fontsize=10.5, color=BAD, ha="center", va="center",
             bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                       edgecolor="none"))

axb.text(LEFT, -0.85,
         "1-count is still 4  ->  the even-parity check passes\n"
         "one flip adds a 1, the other removes a 1: a parity bit counts only\n"
         "the PARITY of the error count, never the bit positions",
         fontsize=12, color=BAD, va="center", fontweight="bold")

axb.set_xlim(XMIN, XMAX)
axb.set_ylim(-1.55, 3.60)
axb.axis("off")

fig.subplots_adjust(hspace=0.22)
save_fig(fig, "parity-bit-format")
