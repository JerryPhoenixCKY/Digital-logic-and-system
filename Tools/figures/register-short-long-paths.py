"""Conceptual register-to-register maximum and minimum timing paths."""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import INK, HILITE, ACCENT, MUTED, FILL, MPL_LW, apply_mpl_style, save_fig
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def main():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(11.5, 6.4))
    ax.set(xlim=(0, 13), ylim=(-0.3, 8.5))
    ax.axis('off')
    ax.text(6.5, 8.1, 'Two timing bounds for the same launch and capture registers',
            weight='bold', ha='center')
    for x, name in [(0.5, 'Launch'), (10.5, 'Capture')]:
        ax.add_patch(Rectangle((x, 3.7), 2, 3.4, edgecolor=INK, facecolor=FILL, lw=MPL_LW))
        ax.text(x+1, 6.35, name+'\nregister', ha='center', va='center')
        ax.text(x+1, 4.0, 'CLK', ha='center', va='center', fontsize=11)
    ax.text(2.23, 5.3, 'Q', ha='center', va='center')
    ax.text(10.76, 5.3, 'D', ha='center', va='center')
    for y, label, color in [(6.1, r'Longest sensitizable path: $t_{PD,max}$', HILITE),
                            (4.5, r'Shortest sensitizable path: $t_{CD,min}$', ACCENT)]:
        ax.plot([2.5, 3.2, 3.2, 4.1], [5.3, 5.3, y, y], color=color, lw=MPL_LW)
        ax.add_patch(Rectangle((4.1, y-0.45), 4.6, 0.9, edgecolor=color, facecolor='white', lw=MPL_LW))
        ax.text(6.4, y, label, ha='center', va='center', fontsize=12)
        ax.plot([8.7, 9.8, 9.8, 10.25], [y, y, 5.3, 5.3], color=color, lw=MPL_LW)
    ax.annotate('', xy=(10.5, 5.3), xytext=(10.15, 5.3),
                arrowprops=dict(arrowstyle='->', color=INK, lw=MPL_LW))
    ax.text(6.5, 7.35, 'Conceptual alternatives through one combinational network',
            ha='center', fontsize=11, color=MUTED)
    ax.plot([1.5, 11.5], [2.95, 2.95], color=INK, lw=MPL_LW)
    for x in (1.5, 11.5):
        ax.annotate('', xy=(x, 3.7), xytext=(x, 2.95),
                    arrowprops=dict(arrowstyle='->', color=INK, lw=MPL_LW))
    ax.text(6.5, 2.62, 'Shared clock; zero skew; one-cycle capture; uncertainty omitted',
            ha='center', va='top', fontsize=11)
    ax.text(6.5, 1.7, r'Setup: $T_{CLK}\geq t_{CQ,max}+t_{PD,max}+t_{SU}$',
            ha='center', color=HILITE, fontsize=15)
    ax.text(6.5, 0.85, r'Hold: $t_{CQ,min}+t_{CD,min}\geq t_H$',
            ha='center', color=ACCENT, fontsize=15)
    ax.text(6.5, 0.0, 'Maximum delay limits clock speed. Minimum delay protects the captured old value.',
            ha='center', fontsize=12)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.06)
    save_fig(fig, 'register-short-long-paths')


if __name__ == '__main__':
    main()
