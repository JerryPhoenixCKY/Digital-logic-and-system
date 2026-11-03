"""Figure: inverter timing diagram -- ideal (zero delay) vs real (t_pd).

Panel (a): the ideal inverter.  Y = NOT A, and every edge of Y lines up exactly
with the opposite edge of A: the dashed guides at 20 / 40 / 60 ns cross both
lanes at the same instant, which is what "zero delay" buys you.

Panel (b): a real inverter.  Y is the very same waveform, shifted right by the
propagation delay t_pd = 4 ns.  The double arrow marks that lag on the first
edge; the shaded dots sit on the two edges the arrow connects.

A is a 50 % duty-cycle 25 MHz square wave (20 ns high, 20 ns low), so the
inverter must reproduce the same 50 % duty cycle -- only delayed.

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
Y_Y = 0.0                       # lane baselines (level 0 of each lane)
Y_A = 2.0
TPD = 4.0                       # propagation delay, ns

# A: 20 ns high, 20 ns low -> 50 % duty cycle, edges at 0 / 20 / 40 / 60 / 80 ns
A_SEGS = [(0.0, 20.0, 1), (20.0, 40.0, 0), (40.0, 60.0, 1), (60.0, 80.0, 0)]
# ideal Y = NOT A, edges at the very same instants
Y_IDEAL = [(0.0, 20.0, 0), (20.0, 40.0, 1), (40.0, 60.0, 0), (60.0, 80.0, 1)]
# real Y: Y(t) = NOT A(t - t_pd); A is assumed low before t = 0
Y_REAL = [(0.0, 4.0, 1), (4.0, 24.0, 0), (24.0, 44.0, 1),
          (44.0, 64.0, 0), (64.0, 80.0, 1)]


def wave(ax, segs, y0, color=INK):
    """Draw one digital waveform: segs = [(t_start, t_end, level), ...]."""
    xs, ys = [], []
    for t0, t1, lv in segs:
        xs += [t0, t1]
        ys += [y0 + lv, y0 + lv]
    ax.plot(xs, ys, color=color, zorder=4)


def panel(ax, title, y_segs, guides, guide_y, note, note_color=MUTED):
    ax.set_xlim(XLO, XHI)
    ax.set_ylim(-0.7, 3.9)
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(['0', '1', '0', '1'])
    ax.set_xticks(range(0, 81, 10))
    ax.set_title(title, loc='left')
    ax.set_xlabel('time (ns)')

    wave(ax, A_SEGS, Y_A)
    wave(ax, y_segs, Y_Y)

    for g in guides:
        ax.plot([g, g], [guide_y[0], guide_y[1]], color=MUTED, ls='--',
                lw=1.2, zorder=2)

    ax.text(NAMEX, Y_A + 0.5, '$A$', ha='left', va='center', color=INK)
    ax.text(NAMEX, Y_Y + 0.5, '$Y$', ha='left', va='center', color=INK)
    ax.text(XLO + 1.0, 3.55, note, ha='left', va='center', fontsize=11,
            color=note_color)


def build():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.0, 7.6))
    fig.subplots_adjust(left=0.075, right=0.985, top=0.925, bottom=0.085,
                        hspace=0.52)

    # (a) ideal: Y edges sit exactly on the A edges
    panel(ax1, '(a) ideal inverter -- zero delay, Y edges line up with A edges',
          Y_IDEAL, [20.0, 40.0, 60.0], (-0.5, 3.35),
          'dashed guides: one vertical line crosses the A edge and the Y edge '
          'at the same instant')

    # (b) real: the same waveform, late by t_pd
    panel(ax2, '(b) real inverter -- Y is the same waveform, delayed by t_pd',
          Y_REAL, [20.0, 40.0, 60.0], (-0.5, 3.35),
          'A changes at 20 / 40 / 60 ns; Y follows t_pd later')

    ax2.annotate('', xy=(20.0 + TPD, 1.5), xytext=(20.0, 1.5),
                 arrowprops=dict(arrowstyle='<->', color=HILITE, lw=1.4))
    ax2.plot([20.0, 20.0 + TPD], [2.0, 1.0], color=HILITE, ls=':', lw=1.2,
             zorder=5)
    ax2.plot([20.0], [2.0], marker='o', color=HILITE, ms=5, zorder=6)
    ax2.plot([20.0 + TPD], [1.0], marker='o', color=HILITE, ms=5, zorder=6)
    ax2.text(24.6, 1.5, r'$t_{pd} = 4$ ns', ha='left', va='center',
             color=HILITE, fontsize=12)

    return fig


def checks():
    def duty(segs, t_end=80.0):
        hi = sum(t1 - t0 for t0, t1, lv in segs if lv == 1)
        return hi, 100.0 * hi / t_end

    print('check  A          : %s' % A_SEGS)
    print('check  ideal Y    : %s' % Y_IDEAL)
    print('check  real  Y    : %s' % Y_REAL)
    for name, segs in (('A', A_SEGS), ('ideal Y', Y_IDEAL),
                       ('real Y', Y_REAL)):
        hi, pct = duty(segs)
        print('check  %-8s high time = %g ns of 80 ns -> duty = %.1f %%'
              % (name, hi, pct))
    ok = all(1 - a == y for a, y in zip((1, 0, 1, 0), (0, 1, 0, 1)))
    print('check  ideal Y = NOT A on the four 20 ns slots: %s' % ok)
    # Y(t) = NOT A(t - t_pd), sampled on a 1 ns grid
    def level(segs, t):
        for t0, t1, lv in segs:
            if t0 <= t < t1:
                return lv
        return segs[-1][2]

    grid = [t + 0.5 for t in range(80)]
    lag_ok = all(level(Y_REAL, t) == 1 - (level(A_SEGS, t - TPD)
                                          if t - TPD >= 0 else 0)
                 for t in grid)
    print('check  real Y(t) == NOT A(t - 4 ns) on an 80-point 1 ns grid: %s'
          % lag_ok)


def main():
    fig = build()
    save_fig(fig, 'inverter-timing')
    checks()


if __name__ == '__main__':
    main()
