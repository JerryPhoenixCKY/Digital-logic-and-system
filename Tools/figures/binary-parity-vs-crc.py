"""Parity bit vs CRC: which error types are detected on the same 12-bit frame.

Both codes are measured by brute force on the lecture frame 1101 0011 0100
(12 bits, 4095 non-zero error patterns):

  parity : detected  <=>  an odd number of bits was flipped
  CRC    : detected  <=>  the error pattern is NOT a multiple of G = 1010

Cells are coloured GOOD (every such error caught), MUTED (only some) or BAD
(none), so the reason CRC exists is visible at a glance.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

apply_mpl_style()

FRAME = "110100110100"          # D = 11010011 plus the 4-bit checksum 0100
GEN = "1010"
N = len(FRAME)


def mod2_remainder(dividend, gen=GEN):
    cur = list(dividend)
    for i in range(len(cur) - len(gen) + 1):
        if cur[i] == "1":
            for j, g in enumerate(gen):
                cur[i + j] = "1" if cur[i + j] != g else "0"
    return "".join(cur)[len(cur) - len(gen) + 1:]


def error_pattern(recv):
    return "".join("1" if a != b else "0" for a, b in zip(FRAME, recv))


ALL = [e for e in (error_pattern(format(m, "0%db" % N))
                   for m in range(1 << N)) if "1" in e]


def parity_detects(e):
    """Even parity on the whole word: caught iff an odd number of flips."""
    return (FRAME.count("1") + e.count("1")) % 2 == 1


def crc_detects(e):
    return mod2_remainder(e) != "000"


def span(e):
    ones = [i for i, b in enumerate(e) if b == "1"]
    return ones[-1] - ones[0] + 1


def weight(e):
    return e.count("1")


GROUPS = [
    ("single-bit\nerror\n(1 flip)", lambda e: weight(e) == 1),
    ("two-bit\nerror\n(2 flips)", lambda e: weight(e) == 2),
    ("odd count\nof flips\n(1,3,...,11)", lambda e: weight(e) % 2 == 1),
    ("even count\nof flips\n(2,4,...,12)", lambda e: weight(e) % 2 == 0),
    ("burst\nspanning\n<= 3 bits", lambda e: span(e) <= 3),
    ("burst\nspanning\n>= 4 bits", lambda e: span(e) >= 4),
]

rows = []
for label, test in GROUPS:
    sel = [e for e in ALL if test(e)]
    assert sel, label
    rows.append((label, len(sel),
                 sum(parity_detects(e) for e in sel),
                 sum(crc_detects(e) for e in sel)))

# the numbers quoted in the notes come out of this brute force
assert rows[0][1:] == (12, 12, 12)
assert rows[1][1:] == (66, 0, 41)
assert rows[2][1:] == (2048, 2048, 2048)
assert rows[3][1:] == (2047, 0, 1536)
assert rows[4][1:] == (43, 22, 34)
assert rows[5][1:] == (4052, 2026, 3550)

CODES = ["Parity bit\n(even parity)", "CRC\n($G$ = 1010)"]


def style_for(hit, total):
    if hit == total:
        return GOOD, "white", "DETECTED"
    if hit == 0:
        return BAD, "white", "BLIND"
    return MUTED, "white", "PARTLY"


fig, ax = plt.subplots(figsize=(12.6, 6.6))
W, H = 1.62, 1.05
X0, Y0 = 0.0, 0.0

for c, (label, total, p_hit, c_hit) in enumerate(rows):
    ax.text(X0 + c * W + W / 2, Y0 + 2 * H + 0.22, label, ha="center",
            va="bottom", fontsize=10.5, color=INK, linespacing=1.35)
    for r, hit in enumerate((p_hit, c_hit)):
        face, tcol, verdict = style_for(hit, total)
        y = Y0 + (1 - r) * H
        ax.add_patch(Rectangle((X0 + c * W, y), W, H, facecolor=face,
                               edgecolor="white", linewidth=2.4, zorder=2))
        ax.text(X0 + c * W + W / 2, y + H * 0.74, verdict, ha="center",
                va="center", fontsize=11.5, color=tcol, fontweight="bold",
                zorder=3)
        ax.text(X0 + c * W + W / 2, y + H * 0.44, f"{hit}/{total}", ha="center",
                va="center", fontsize=10.5, color=tcol, zorder=3)
        ax.text(X0 + c * W + W / 2, y + H * 0.17,
                f"{100 * hit / total:.0f}%", ha="center",
                va="center", fontsize=10, color=tcol, zorder=3)

for r, name in enumerate(CODES):
    ax.text(X0 - 0.22, Y0 + (1 - r) * H + H / 2, name, ha="right",
            va="center", fontsize=12, color=INK, fontweight="bold")

ax.text(X0 + 3 * W, Y0 + 2 * H + 1.62,
        "error patterns detected on the lecture frame 1101 0011 0100 "
        "(12 bits, 4095 non-zero error patterns)",
        ha="center", va="center", fontsize=12, color=INK, fontweight="bold")
ax.text(X0 + 3 * W, Y0 + 2 * H + 1.22,
        "DETECTED = every error of that type is caught   |   "
        "PARTLY = only some   |   BLIND = none",
        ha="center", va="center", fontsize=10.5, color=MUTED)

CAPTION = [
    (0.42, INK, "Parity sees only HOW MANY bits flipped: an even number of "
                "flips cancels out."),
    (0.00, INK, "CRC sees WHERE they flipped: it fails only for error "
                "patterns that are exact multiples of $G(x)$"),
    (-0.42, INK, "(any error pattern equal to a shifted copy of 1010 slips "
                 "through)."),
    (-0.95, MUTED, "The lecture generator 1010 = $x^3+x$ is a toy: it ends "
                   "in 0, so it still misses 511 of the 4095 patterns (12.5 %)."),
    (-1.37, MUTED, "A real CRC generator ends in 1, which removes those "
                   "blind spots."),
]
for dy, col, line in CAPTION:
    ax.text(X0, Y0 - 0.32 + dy, line, ha="left", va="top", fontsize=11,
            color=col)

ax.set_xlim(X0 - 2.75, X0 + 6 * W + 0.15)
ax.set_ylim(Y0 - 2.35, Y0 + 4.05)
ax.axis("off")

save_fig(fig, "binary-parity-vs-crc")
