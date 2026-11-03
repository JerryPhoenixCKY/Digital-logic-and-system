"""Figure: AND gate timing diagram -- any 0 input gates the output to 0.

Three lanes: A, B and Y = AB, sharing one time axis.  A is high for 30 ns
(10-40 ns), B is high for 40 ns (20-60 ns); Y is high only while *both* are
high, i.e. from 20 to 40 ns.

The shaded bands mark every instant at which at least one input is 0, and the
short tag between the B and Y lanes names the input that is doing the gating.
The green band is the only interval in which Y can be 1: the AND gate is a
"gate" in the literal sense -- a single 0 input closes it and holds the output
at 0, no matter what the other input does.

Timing waveforms -> matplotlib.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

apply_mpl_style()

import matplotlib.pyplot as plt

XLO, XHI = -15.0, 84.0          # time axis, ns
NAMEX = XLO + 1.4               # signal names live in the empty left margin
Y_Y, Y_B, Y_A = 0.0, 2.0, 4.0   # lane baselines (level 0 of each lane)

A_SEGS = [(0.0, 10.0, 0), (10.0, 40.0, 1), (40.0, 80.0, 0)]
B_SEGS = [(0.0, 20.0, 0), (20.0, 60.0, 1), (60.0, 80.0, 0)]
Y_SEGS = [(0.0, 20.0, 0), (20.0, 40.0, 1), (40.0, 80.0, 0)]


def wave(ax, segs, y0, color=INK):
    """Draw one digital waveform: segs = [(t_start, t_end, level), ...]."""
    xs, ys = [], []
    for t0, t1, lv in segs:
        xs += [t0, t1]
        ys += [y0 + lv, y0 + lv]
    ax.plot(xs, ys, color=color, zorder=4)


def build():
    fig, ax = plt.subplots(figsize=(11.0, 6.6))

    ax.set_xlim(XLO, XHI)
    ax.set_ylim(-0.8, 8.0)
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.set_yticklabels(['0', '1', '0', '1', '0', '1'])
    ax.set_xticks(range(0, 81, 10))
    ax.set_xlabel('time (ns)')

    # bands: where Y is forced to 0 (bad) and where both inputs allow Y = 1 (good)
    ax.axvspan(0.0, 20.0, color=BAD, alpha=0.07, zorder=0)
    ax.axvspan(40.0, 80.0, color=BAD, alpha=0.07, zorder=0)
    ax.axvspan(20.0, 40.0, color=GOOD, alpha=0.12, zorder=0)

    for t in (20.0, 40.0):
        ax.plot([t, t], [-0.6, 5.2], color=MUTED, ls='--', lw=1.2, zorder=2)

    wave(ax, A_SEGS, Y_A)
    wave(ax, B_SEGS, Y_B)
    wave(ax, Y_SEGS, Y_Y)

    ax.text(NAMEX, Y_A + 0.5, '$A$', ha='left', va='center', color=INK)
    ax.text(NAMEX, Y_B + 0.5, '$B$', ha='left', va='center', color=INK)
    ax.text(NAMEX, Y_Y + 0.5, '$Y = AB$', ha='left', va='center', color=INK)

    # which input is holding Y down, written in the gap under the B lane
    for x, tag in ((5.0, 'A = B = 0'), (15.0, 'B = 0'),
                   (50.0, 'A = 0'), (70.0, 'A = B = 0')):
        ax.text(x, 1.45, tag, ha='center', va='center', fontsize=10.5,
                color=BAD)

    ax.text(XLO + 1.0, 5.65, 'any input at 0 gates Y to 0 and holds it there',
            ha='left', va='center', fontsize=12, color=BAD)
    ax.text(30.0, 6.85, 'A = B = 1  ->  Y = 1  (only in this interval)',
            ha='center', va='center', fontsize=12, color=GOOD)

    fig.tight_layout()
    return fig


def checks():
    def level(segs, t):
        for t0, t1, lv in segs:
            if t0 <= t < t1:
                return lv
        return segs[-1][2]

    def edges(segs):
        out = []
        for t in range(1, 80):
            if level(segs, t - 0.5) != level(segs, t + 0.5):
                out.append(t)
        return out

    print('check  A : %s  edges at %s ns' % (A_SEGS, edges(A_SEGS)))
    print('check  B : %s  edges at %s ns' % (B_SEGS, edges(B_SEGS)))
    print('check  Y : %s  edges at %s ns' % (Y_SEGS, edges(Y_SEGS)))
    grid = [t + 0.25 for t in range(80)]
    ok = all(level(Y_SEGS, t) == (level(A_SEGS, t) & level(B_SEGS, t))
             for t in grid)
    print('check  Y(t) == A(t) AND B(t) on an 80-point grid: %s' % ok)
    print('check  4-row truth table, A B -> Y : %s'
          % ' '.join('%d%d->%d' % (a, b, a & b)
                     for a in (0, 1) for b in (0, 1)))
    print('check  rows with Y = 1: %d of 4 (only A = B = 1)'
          % sum(1 for a in (0, 1) for b in (0, 1) if a & b))
    print('check  n-input AND needs 2^n truth-table rows: 2^2 = 4, 2^3 = 8')


def main():
    fig = build()
    save_fig(fig, 'and-gate-timing')
    checks()


if __name__ == '__main__':
    main()
