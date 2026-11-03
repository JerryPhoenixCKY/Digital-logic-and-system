"""Figure: OR gate timing diagram -- any 1 input makes the output 1.

Three lanes: A, B and Y = A + B, sharing one time axis.  The same A and B
waveforms as the AND figure are reused on purpose, so the two figures can be
compared lane by lane.

Here Y is 1 from 10 to 60 ns: it turns 1 the moment A rises (B is still 0) and
stays 1 until B falls at 60 ns, because a single 1 input is already enough.
The only intervals with Y = 0 are the two in which *both* inputs are 0 --
"some input is 0" is never a reason for the output of an OR gate to be 0.

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
Y_SEGS = [(0.0, 10.0, 0), (10.0, 60.0, 1), (60.0, 80.0, 0)]


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

    # bands: where Y = 0 (both inputs low) and where at least one input is high
    ax.axvspan(0.0, 10.0, color=BAD, alpha=0.07, zorder=0)
    ax.axvspan(60.0, 80.0, color=BAD, alpha=0.07, zorder=0)
    ax.axvspan(10.0, 60.0, color=GOOD, alpha=0.12, zorder=0)

    for t in (10.0, 60.0):
        ax.plot([t, t], [-0.6, 5.2], color=MUTED, ls='--', lw=1.2, zorder=2)

    wave(ax, A_SEGS, Y_A)
    wave(ax, B_SEGS, Y_B)
    wave(ax, Y_SEGS, Y_Y)

    ax.text(NAMEX, Y_A + 0.5, '$A$', ha='left', va='center', color=INK)
    ax.text(NAMEX, Y_B + 0.5, '$B$', ha='left', va='center', color=INK)
    ax.text(NAMEX, Y_Y + 0.5, '$Y = A + B$', ha='left', va='center',
            color=INK)

    # the only way to get Y = 0: both inputs low
    for x in (5.0, 70.0):
        ax.text(x, 1.45, 'A = B = 0', ha='center', va='center', fontsize=10.5,
                color=BAD)

    ax.text(XLO + 1.0, 5.65, 'either input at 1 makes Y = 1',
            ha='left', va='center', fontsize=12, color=GOOD)
    ax.text(35.0, 6.85, 'Y = 0 only while A = B = 0  ->  "some input is 0" '
                        'is not enough', ha='center', va='center',
            fontsize=12, color=BAD)

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
    ok = all(level(Y_SEGS, t) == (level(A_SEGS, t) | level(B_SEGS, t))
             for t in grid)
    print('check  Y(t) == A(t) OR B(t) on an 80-point grid: %s' % ok)
    print('check  4-row truth table, A B -> Y : %s'
          % ' '.join('%d%d->%d' % (a, b, a | b)
                     for a in (0, 1) for b in (0, 1)))
    print('check  T/F "if any input is 0 the output is 0": False '
          '(counterexample A = 0, B = 1 -> Y = 1)')
    print('check  3-input OR3, 8 rows = 2^3, Y = 0 only on the 000 row: %s'
          % ' '.join('%d%d%d->%d' % (a, b, c, a | b | c)
                     for a in (0, 1) for b in (0, 1) for c in (0, 1)))


def main():
    fig = build()
    save_fig(fig, 'or-gate-timing')
    checks()


if __name__ == '__main__':
    main()
