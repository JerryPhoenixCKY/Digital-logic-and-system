"""3-08 Exclusive-NOR Gate -- timing diagram of Y = NOT(A xor B).

Four lanes on one time base: A, B, the XOR output A xor B (dashed, drawn as the
reference), and the XNOR output Y = (A xor B)'.  The two outputs are complements
in every slot -- XNOR is XOR plus a bubble.

    A B | A xor B | Y = (A xor B)'
    0 0 |    0    |   1
    0 1 |    1    |   0
    1 0 |    1    |   0
    1 1 |    0    |   1        (checked in Python, all 4 rows)

Every slot above the A lane carries "=" (inputs equal, Y = 1) or "!=" (inputs
differ, Y = 0); the shaded slots are the "=" ones -- the equality detector.

Run:  D:\\anaconda\\python.exe Tools\\figures\\xnor-gate-timing.py
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt

A = [0, 0, 1, 1, 0, 0, 1, 1]
B = [0, 1, 0, 1, 0, 1, 0, 1]
XOR = [a ^ b for a, b in zip(A, B)]
Y = [1 - v for v in XOR]                       # XNOR = XOR + bubble
assert Y == [1, 0, 0, 1, 1, 0, 0, 1]           # matches the truth table above

SLOTS = len(A)
PITCH, HI = 1.0, 0.62
FS_NOTE = 10.5
SH_LO = -0.25                                  # bottom of the shaded band


def lane(ax, base, bits, color, name, dashed=False):
    """One digital waveform: low level at `base`, high level at `base + HI`."""
    xs, ys = [0.0], [base + (HI if bits[0] else 0.0)]
    for i in range(1, len(bits)):
        xs += [float(i), float(i)]
        ys += [base + (HI if bits[i - 1] else 0.0), base + (HI if bits[i] else 0.0)]
    xs.append(float(len(bits)))
    ys.append(base + (HI if bits[-1] else 0.0))
    ax.plot(xs, ys, color=color, ls=(0, (4, 2.4)) if dashed else "-",
            solid_joinstyle="miter", solid_capstyle="butt", zorder=4)
    ax.text(-0.30, base + HI / 2.0, name, ha="right", va="center", color=color,
            zorder=5)


def main():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(11.0, 5.6))

    names = ["$A$", "$B$", "$A\\oplus B$", "$Y=\\overline{A\\oplus B}$"]
    colors = [INK, INK, MUTED, HILITE]
    lanes = [A, B, XOR, Y]
    n = len(lanes)
    top = (n - 1) + HI
    y_lo, y_hi = -1.55, top + 0.95
    SH_HI = top + 0.18                         # top of the shaded band

    def shade(ax, i):
        """Light band over one slot, covering the waveform area only."""
        ax.axvspan(i, i + 1, color=FILL, zorder=0,
                   ymin=(SH_LO - y_lo) / (y_hi - y_lo),
                   ymax=(SH_HI - y_lo) / (y_hi - y_lo))

    for i in range(SLOTS + 1):
        ax.plot([i, i], [-0.30, top], color=MUTED, lw=0.8, ls=(0, (2, 3)),
                zorder=0)
    for k in range(n):
        base = (n - 1 - k) * PITCH
        for lvl in (0.0, HI):
            ax.plot([0.0, SLOTS], [base + lvl] * 2, color=MUTED, lw=0.9,
                    ls=(0, (2, 3)), zorder=1)

    # equality detector: shade every slot where the two inputs are equal
    for i, (a, b) in enumerate(zip(A, B)):
        equal = a == b
        if equal:
            shade(ax, i)
        ax.text(i + 0.5, top + 0.46, "$=$" if equal else "$\\neq$",
                ha="center", va="center", fontsize=FS_NOTE, zorder=5,
                color=HILITE if equal else MUTED)

    for k, bits in enumerate(lanes):
        lane(ax, (n - 1 - k) * PITCH, bits, colors[k], names[k],
             dashed=(k == 2))

    ax.text(0.5 * SLOTS, -1.20,
            "inputs equal ($A=B$) -> $Y=1$   |   XNOR is XOR plus a bubble: "
            "$Y$ is the complement of $A\\oplus B$", ha="center", va="center",
            color=HILITE, fontsize=FS_NOTE, zorder=5)
    for i in range(SLOTS):
        ax.text(i + 0.5, -0.62, str(i + 1), ha="center", va="center",
                color=MUTED, fontsize=FS_NOTE, zorder=5)

    ax.set_title("XNOR timing: $Y=\\overline{A\\oplus B}$ is 1 exactly where the "
                 "inputs are equal", loc="left")
    ax.set_xlim(-1.95, 8.25)
    ax.set_ylim(y_lo, y_hi)
    ax.set_axis_off()
    save_fig(fig, "xnor-gate-timing")


if __name__ == "__main__":
    main()
