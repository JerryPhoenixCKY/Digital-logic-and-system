"""Transport-delay example for Chapter 6 p.52-53; values are assumed, not IC limits."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import INK, HILITE, ACCENT, MUTED, FILL, GOOD, MPL_LW, apply_mpl_style, save_fig
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def wave(ax, base, initial, events, color):
    """Draw ideal 0/1 transitions on a shared time axis in ns."""
    times, values = [-0.3], [base + 0.8 * initial]
    old = initial
    for time, value in events:
        times.extend([time, time])
        values.extend([base + 0.8 * old, base + 0.8 * value])
        old = value
    times.append(7.0)
    values.append(base + 0.8 * old)
    ax.plot(times, values, color=color, lw=MPL_LW)


def main():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(11.6, 7.4))
    ax.set(xlim=(-2.1, 8.2), ylim=(-0.85, 14.0))
    ax.axis("off")
    ax.text(3.1, 13.3, "Static-1 hazard: A = 0, C = 1, B falls at t = 0",
            ha="center", weight="bold")
    ax.text(3.1, 12.45, "Assumed transport delays: INV = 1 ns, AND = 2 ns, OR = 1 ns",
            ha="center", fontsize=11)

    rows = [
        (10.6, r"$B$", 1, [(0, 0)], INK),
        (8.2, r"$n_2=BC$", 1, [(2, 0)], MUTED),
        (5.8, r"$n_1=\overline{A}\,\overline{B}$", 0, [(3, 1)], ACCENT),
        (3.4, r"$Y$", 1, [(3, 0), (4, 1)], HILITE),
        (1.0, r"$Y_{safe}$", 1, [], GOOD),
    ]
    ax.add_patch(Rectangle((3, 3.2), 1, 1.2, facecolor=FILL, edgecolor="none"))
    for time in (0, 2, 3, 4):
        ax.plot([time, time], [0.75, 11.8], color=MUTED, ls="--", lw=MPL_LW / 2)
    for base, label, initial, events, color in rows:
        ax.text(-0.65, base + 0.4, label, ha="right", va="center", color=color)
        wave(ax, base, initial, events, color)

    ax.text(5.6, 9.35, "direct path falls at 2 ns", ha="center", fontsize=11)
    ax.text(5.6, 6.95, "inverted path rises at 3 ns", ha="center", fontsize=11)
    ax.text(5.7, 4.6, "original: HIGH - LOW - HIGH", ha="center", fontsize=11, color=HILITE)
    ax.text(5.5, 2.15, r"with consensus $\overline{A}C=1$", ha="center", fontsize=11, color=GOOD)
    ax.annotate("", xy=(4, 2.8), xytext=(3, 2.8),
                arrowprops=dict(arrowstyle="<->", color=HILITE, lw=MPL_LW / 1.5,
                                shrinkA=0, shrinkB=0))
    ax.text(3.5, 2.45, "1 ns LOW pulse", ha="center", va="top", fontsize=11, color=HILITE)

    ax.annotate("", xy=(7.2, 0), xytext=(-0.3, 0),
                arrowprops=dict(arrowstyle="->", color=INK, lw=MPL_LW / 1.5))
    for time in range(7):
        ax.plot([time, time], [-0.12, 0.08], color=INK, lw=MPL_LW / 2)
        ax.text(time, -0.32, str(time), ha="center", va="top", fontsize=11)
    ax.text(7.35, 0, "time (ns)", va="center", fontsize=11)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.985, bottom=0.075)
    save_fig(fig, "ch6-static-hazard-timing")


if __name__ == "__main__":
    main()
