"""3-07 Exclusive-OR Gate -- timing diagram of Y = A xor B.

Three lanes on one time base: A, B and Y = A*B' + A'B = A xor B.  A has period
4 and B has period 2, so all four input combinations occur twice:

    A B | Y = A xor B
    0 0 |  0
    0 1 |  1
    1 0 |  1
    1 1 |  0        (checked in Python, all 4 rows)

Above the A lane every slot carries the comparison mark: "!=" (inputs differ,
Y = 1) or "=" (inputs equal, Y = 0).  The shaded slots are exactly the "!="
slots -- the picture of "an XOR gate is a difference detector / the sum bit of
two bits".

Run:  D:\\anaconda\\python.exe Tools\\figures\\xor-gate-timing.py
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt

A = [0, 0, 1, 1, 0, 0, 1, 1]
B = [0, 1, 0, 1, 0, 1, 0, 1]
Y = [a ^ b for a, b in zip(A, B)]
assert Y == [0, 1, 1, 0, 0, 1, 1, 0]           # matches the truth table above

SLOTS = len(A)
PITCH, HI = 1.0, 0.62
FS_NOTE = 10.5
SH_LO = -0.25                                  # bottom of the shaded band


def lane(ax, base, bits, color, name):
    """One digital waveform: low level at `base`, high level at `base + HI`."""
    xs, ys = [0.0], [base + (HI if bits[0] else 0.0)]
    for i in range(1, len(bits)):
        xs += [float(i), float(i)]
        ys += [base + (HI if bits[i - 1] else 0.0), base + (HI if bits[i] else 0.0)]
    xs.append(float(len(bits)))
    ys.append(base + (HI if bits[-1] else 0.0))
    ax.plot(xs, ys, color=color, solid_joinstyle="miter", solid_capstyle="butt",
            zorder=4)
    ax.text(-0.30, base + HI / 2.0, name, ha="right", va="center", color=color,
            zorder=5)


def main():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(11.0, 4.6))

    names = ["$A$", "$B$", "$Y=A\\oplus B$"]
    colors = [INK, INK, HILITE]
    lanes = [A, B, Y]
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

    # the difference detector: shade every slot where the two inputs differ
    for i, (a, b) in enumerate(zip(A, B)):
        differ = a != b
        if differ:
            shade(ax, i)
        ax.text(i + 0.5, top + 0.46, "$\\neq$" if differ else "$=$",
                ha="center", va="center", fontsize=FS_NOTE, zorder=5,
                color=HILITE if differ else MUTED)

    for k, bits in enumerate(lanes):
        lane(ax, (n - 1 - k) * PITCH, bits, colors[k], names[k])

    ax.text(0.5 * SLOTS, -1.20,
            "inputs differ ($A\\neq B$) -> $Y=1$   |   inputs equal -> $Y=0$; "
            "$Y$ is the sum bit of $A+B$", ha="center", va="center",
            color=HILITE, fontsize=FS_NOTE, zorder=5)
    for i in range(SLOTS):
        ax.text(i + 0.5, -0.62, str(i + 1), ha="center", va="center",
                color=MUTED, fontsize=FS_NOTE, zorder=5)

    ax.set_title("XOR timing: $Y=A\\oplus B$ is 1 exactly where the inputs differ",
                 loc="left")
    ax.set_xlim(-1.95, 8.25)
    ax.set_ylim(y_lo, y_hi)
    ax.set_axis_off()
    save_fig(fig, "xor-gate-timing")


if __name__ == "__main__":
    main()
