"""Shared-axis positive-edge setup/hold aperture, with clock-to-Q delay."""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import INK, ACCENT, HILITE, MUTED, FILL, GOOD, MPL_LW, apply_mpl_style, save_fig
import matplotlib.pyplot as plt


def main():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(10.6, 6.3))
    ax.set(xlim=(-8.6, 8.6), ylim=(-0.9, 9.3))
    ax.axis('off')
    ax.axvspan(-3, 2, ymin=0.14, ymax=0.83, facecolor=FILL, edgecolor='none')
    ax.text(0, 8.75, 'Positive-edge capture: data must remain stable across the aperture',
            ha='center', weight='bold')
    ax.text(-8.4, 7, 'CLK', va='center', weight='bold')
    ax.text(-8.4, 4.5, 'D', va='center', weight='bold')
    ax.text(-8.4, 1.6, 'Q', va='center', weight='bold')
    ax.plot([-7.2, 0, 0, 6, 6, 8], [6.5, 6.5, 7.5, 7.5, 6.5, 6.5], color=INK)
    ax.plot([-7.2, -6, -6, 5, 5, 8], [4, 4, 5, 5, 4, 4], color=ACCENT)
    ax.plot([-7.2, 1.5, 1.5, 8], [1.1, 1.1, 2.1, 2.1], color=GOOD)
    for t in (-3, 2):
        ax.plot([t, t], [2.8, 7.8], color=MUTED, ls='--', lw=MPL_LW/2)
    ax.plot([0, 0], [0.0, 8.05], color=HILITE, ls='--', lw=MPL_LW/2)
    ax.text(0, 7.9, 'capture edge', ha='center', va='bottom', color=HILITE)
    ax.text(-0.5, 5.45, 'stable sampled value = 1', ha='center', color=ACCENT)
    arrow = dict(arrowstyle='<->', color=INK, lw=MPL_LW/1.6, shrinkA=0, shrinkB=0)
    ax.annotate('', xy=(0, 3.15), xytext=(-3, 3.15), arrowprops=arrow)
    ax.annotate('', xy=(2, 3.15), xytext=(0, 3.15), arrowprops=arrow)
    ax.text(-1.5, 2.85, r'$t_{SU}$ (setup)', ha='center', va='top')
    ax.text(1, 2.85, r'$t_H$ (hold)', ha='center', va='top')
    ax.annotate('', xy=(1.5, 0.5), xytext=(0, 0.5), arrowprops=arrow)
    ax.text(0.75, 0.23, r'$t_{CQ}$', ha='center', va='top', color=GOOD)
    ax.text(4.8, 1.45, 'captured value appears after CLK-to-Q delay', ha='center', fontsize=11)
    ax.annotate('', xy=(8, -0.6), xytext=(-7.2, -0.6),
                arrowprops=dict(arrowstyle='->', color=INK, lw=MPL_LW/1.6))
    for t, label in [(-3, r'$-t_{SU}$'), (0, '0'), (2, r'$+t_H$')]:
        ax.plot([t, t], [-0.68, -0.51], color=INK, lw=MPL_LW/2)
        ax.text(t, -0.77, label, ha='center', va='top', fontsize=11)
    ax.text(8.2, -0.6, 'time', ha='left', va='center', fontsize=11)
    ax.text(-6.1, 5.45, 'allowed change', ha='center', fontsize=11)
    ax.text(5.3, 5.45, 'allowed change', ha='center', fontsize=11)
    fig.subplots_adjust(left=0.03, right=0.98, top=0.97, bottom=0.08)
    save_fig(fig, 'setup-hold-window')


if __name__ == '__main__':
    main()
