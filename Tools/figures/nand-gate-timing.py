"""3-05 NAND Gate -- timing diagram of Y = NOT(A AND B).

Four lanes on one time base: A, B, the AND output A*B, and the NAND output
Y = (AB)'.  The two outputs are complements in every slot -- that is exactly the
lecture's "How to verify/prove?" question on p.8: a NAND gate is an AND gate
followed by an inverter (the bubble).

A has period 4 and B has period 2, so all four input combinations occur twice
and the waveforms can be read against the four-row truth table:

    A B | A*B | Y = (AB)'
    0 0 |  0  |  1
    0 1 |  0  |  1
    1 0 |  0  |  1
    1 1 |  1  |  0        (checked in Python, all 4 rows)

The shaded slots are the ones where A*B = 1, i.e. where the bubble flips the
AND output to 0.

Run:  D:\\anaconda\\python.exe Tools\\figures\\nand-gate-timing.py
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt

A = [0, 0, 1, 1, 0, 0, 1, 1]
B = [0, 1, 0, 1, 0, 1, 0, 1]
AND = [a & b for a, b in zip(A, B)]
Y = [1 - v for v in AND]                       # NAND = AND + bubble
assert Y == [1, 1, 1, 0, 1, 1, 1, 0]           # matches the truth table above

SLOTS = len(A)
PITCH, HI = 1.0, 0.62                          # lane pitch, high level
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

    names = ["$A$", "$B$", "$A\\cdot B$", "$Y=\\overline{A\\cdot B}$"]
    colors = [INK, INK, ACCENT, HILITE]
    lanes = [A, B, AND, Y]
    n = len(lanes)
    top = (n - 1) + HI
    y_lo, y_hi = -1.55, top + 0.85
    SH_HI = top + 0.18                         # top of the shaded band

    def shade(ax, i):
        """Light band over one slot, covering the waveform area only."""
        ax.axvspan(i, i + 1, color=FILL, zorder=0,
                   ymin=(SH_LO - y_lo) / (y_hi - y_lo),
                   ymax=(SH_HI - y_lo) / (y_hi - y_lo))

    # slot separators + the 0/1 guide levels of every lane
    for i in range(SLOTS + 1):
        ax.plot([i, i], [-0.30, top], color=MUTED, lw=0.8, ls=(0, (2, 3)),
                zorder=0)
    for k in range(n):
        base = (n - 1 - k) * PITCH
        for lvl in (0.0, HI):
            ax.plot([0.0, SLOTS], [base + lvl] * 2, color=MUTED, lw=0.9,
                    ls=(0, (2, 3)), zorder=1)
        ax.text(-0.30, base + HI / 2.0, names[k], ha="right", va="center",
                color=colors[k], zorder=5)

    # every slot in which the AND output is 1 (the bubble turns it into 0)
    for i, v in enumerate(AND):
        if v:
            shade(ax, i)
            ax.text(i + 0.5, top + 0.42, "$A\\cdot B=1$", ha="center",
                    va="center", color=HILITE, fontsize=FS_NOTE, zorder=5)

    for k, bits in enumerate(lanes):
        lane(ax, (n - 1 - k) * PITCH, bits, colors[k], names[k])

    ax.text(0.5 * SLOTS, -1.20,
            "NAND = AND + inverter: in every slot $Y$ is the complement of "
            "$A\\cdot B$ (bubble flips 1 -> 0)", ha="center", va="center",
            color=HILITE, fontsize=FS_NOTE, zorder=5)
    for i in range(SLOTS):
        ax.text(i + 0.5, -0.62, str(i + 1), ha="center", va="center",
                color=MUTED, fontsize=FS_NOTE, zorder=5)

    ax.set_title("NAND timing: $Y=\\overline{A\\cdot B}$ against the AND output",
                 loc="left")
    ax.set_xlim(-1.95, 8.25)
    ax.set_ylim(y_lo, y_hi)
    ax.set_axis_off()
    save_fig(fig, "nand-gate-timing")


if __name__ == "__main__":
    main()
