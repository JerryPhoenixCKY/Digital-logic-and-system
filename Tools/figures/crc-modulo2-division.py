"""CRC: modulo-2 long division of the lecture example (D = 11010011, G = 1010).

(a) sender side: append 0000 -> D' = 1101 0011 0000, divide by G = 1010 with
    XOR at every step (the ladder clears one leading 1 per step), remainder 100,
    which the lecture carries as the 4-bit checksum 0100 -> frame 1101 0011 0100.
(b) receiver side: dividing the whole received frame by G gives 000 (no error);
    flipping the last bit gives 001 != 000 (error detected).

Every number is recomputed here, so the drawing cannot drift from the text.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

apply_mpl_style()

DATA = "11010011"
GEN = "1010"
AUG = DATA + "0000"                 # 12-bit dividend D'
DEG0 = DATA + "000"                 # textbook convention: 3 zeros (deg G = 3)


def mod2_divide(dividend, gen):
    """Return (remainder, steps); step = (shift, row_before, row_after)."""
    cur = list(dividend)
    steps = []
    for i in range(len(cur) - len(gen) + 1):
        if cur[i] == "1":
            before = "".join(cur)
            for j, g in enumerate(gen):
                cur[i + j] = "1" if cur[i + j] != g else "0"
            steps.append((i, before, "".join(cur)))
    return "".join(cur)[len(cur) - len(gen) + 1:], steps


rem, steps = mod2_divide(AUG, GEN)
checksum = rem.rjust(4, "0")
FRAME = DATA + checksum
recv_rem, _ = mod2_divide(FRAME, GEN)
ERR_FRAME = FRAME[:-1] + ("1" if FRAME[-1] == "0" else "0")
err_rem, _ = mod2_divide(ERR_FRAME, GEN)
text_rem, _ = mod2_divide(DEG0, GEN)

assert rem == "100", rem
assert [s[0] for s in steps] == [0, 1, 2, 4, 7], [s[0] for s in steps]
assert checksum == "0100" and FRAME == "110100110100", (checksum, FRAME)
assert recv_rem == "000" and err_rem == "001", (recv_rem, err_rem)
assert ERR_FRAME == "110100110101"
assert text_rem == "010"            # textbook convention, 3 appended zeros

CELL, GAP, PITCH = 0.86, 0.34, 1.0


def col_x(i):
    """x of the left edge of bit column i (12 columns in three 4-bit groups)."""
    return i * PITCH + GAP * (i // 4)


def draw_bits(ax, y, s, x_of, *, mark=None, size=13, text_color=None):
    mark = mark or {}
    text_color = text_color or {}
    for i, b in enumerate(s):
        x = x_of(i)
        is_marked = i in mark
        ax.add_patch(Rectangle((x, y), CELL, CELL,
                               facecolor=FILL if b == "1" else "white",
                               edgecolor=mark.get(i, INK),
                               linewidth=2.6 if is_marked else 1.0, zorder=2))
        ax.text(x + CELL / 2, y + CELL / 2, b, ha="center", va="center",
                fontsize=size, color=text_color.get(i, INK), zorder=3,
                fontweight="bold" if is_marked else "normal")


fig, (axa, axb) = plt.subplots(2, 1, figsize=(11.6, 11.2),
                               gridspec_kw=dict(height_ratios=[3.4, 1.0]))

# ------------------------------------------------------------------ panel (a)
axa.set_title("(a) sender: modulo-2 long division of $D'$ = 1101 0011 0000 "
              "by the generator $G$ = 1010")
axa.text(-3.55, 12.95, "$D'$ = $D$ followed by 0000  (one zero per checksum bit)",
         fontsize=12, color=INK, va="center")
axa.text(-3.55, 12.30, "leftmost bit = $x^{11}$",
         fontsize=11, color=MUTED, va="center")

y = 11.35
draw_bits(axa, y, AUG, col_x, size=13)
y_after_first = None

for k, (shift, before, after) in enumerate(steps):
    y_gen = y - 0.72
    for j, g in enumerate(GEN):
        axa.text(col_x(shift + j) + CELL / 2, y_gen + 0.30, g, ha="center",
                 va="center", fontsize=13, color=ACCENT, fontweight="bold")
    axa.text(col_x(shift) - 0.55, y_gen + 0.30, "$\\oplus$", ha="center",
             va="center", fontsize=14, color=HILITE)
    axa.plot([col_x(shift), col_x(shift + 3) + CELL], [y_gen - 0.02, y_gen - 0.02],
             color=INK, linewidth=1.4, zorder=2)
    axa.text(-3.55, y_gen + 0.30, f"step {k + 1}", fontsize=11.5, color=INK,
             va="center")
    axa.text(14.15, y_gen + 0.30, f"clear the 1 at $x^{{{11 - shift}}}$",
             fontsize=11, color=HILITE, va="center")

    y_res = y_gen - 1.18
    draw_bits(axa, y_res, after, col_x, mark={shift: HILITE},
              text_color={shift: HILITE}, size=13)
    y = y_res

# final remainder: columns 9..11 of the last row
axa.plot([col_x(9) - 0.10, col_x(11) + CELL + 0.10], [y - 0.14, y - 0.14],
         color=GOOD, linewidth=2.4, zorder=2)
axa.text(col_x(9) - 0.10, y - 0.42,
         "remainder = 100  ($x^2$), taken as the 4-bit checksum 0100",
         fontsize=12, color=GOOD, va="center", fontweight="bold")
axa.text(col_x(9) - 0.10, y - 0.95,
         "frame sent = $D$ + checksum = 1101 0011 0100",
         fontsize=12, color=INK, va="center")
axa.text(-3.55, y - 0.95,
         "textbook form:\n$D$ + 000 gives\nremainder 010",
         fontsize=10.5, color=MUTED, va="center")

axa.set_xlim(-3.65, 22.0)
axa.set_ylim(y - 1.45, 13.45)
axa.axis("off")

# ------------------------------------------------------------------ panel (b)
axb.set_title("(b) receiver: divide the whole received frame by $G$ = 1010")
RX_X = lambda j: col_x(11) + 2.55 + j * PITCH      # noqa: E731

axb.text(-3.55, 2.72, "frame received", fontsize=12, color=INK, va="center")
draw_bits(axb, 2.05, FRAME, col_x, size=12)
axb.text(17.55, 2.72, "remainder 000", fontsize=12, color=GOOD,
         fontweight="bold", va="center")
axb.text(17.55, 2.05, "all bits divide evenly", fontsize=11, color=GOOD,
         va="center")

axb.text(-3.55, 0.72, "one bit flipped", fontsize=12, color=INK, va="center")
draw_bits(axb, 0.05, ERR_FRAME, col_x, mark={11: BAD}, text_color={11: BAD},
          size=12)
axb.text(17.55, 0.72, "remainder 001", fontsize=12, color=BAD,
         fontweight="bold", va="center")
axb.text(17.55, 0.05, "non-zero -> error detected", fontsize=11, color=BAD,
         va="center")

# remaining bits of the two receiver divisions, shown as the FCS field
draw_bits(axb, 2.05, recv_rem, RX_X, mark={0: GOOD, 1: GOOD, 2: GOOD},
          text_color={i: GOOD for i in range(3)}, size=12)
draw_bits(axb, 0.05, err_rem, RX_X, mark={0: BAD, 1: BAD, 2: BAD},
          text_color={i: BAD for i in range(3)}, size=12)
axb.text(RX_X(0) - 0.75, 2.48, "$\\div$", fontsize=15, color=MUTED,
         ha="center", va="center")
axb.text(RX_X(0) - 0.75, 0.48, "$\\div$", fontsize=15, color=MUTED,
         ha="center", va="center")

axb.set_xlim(-3.65, 22.0)
axb.set_ylim(-0.75, 3.45)
axb.axis("off")

fig.subplots_adjust(hspace=0.10)
save_fig(fig, "crc-modulo2-division")
