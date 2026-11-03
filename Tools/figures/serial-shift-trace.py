"""Explicit pre/post-edge values for a four-bit right shift register."""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import INK, HILITE, ACCENT, MUTED, FILL, GOOD, MPL_LW, apply_mpl_style, save_fig
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def sampled_trace(initial=(0, 0, 0, 0), inputs=(1, 0, 1, 1)):
    state = tuple(initial)
    rows = []
    for edge, bit in enumerate(inputs, 1):
        old = state
        state = (bit,) + old[:3]
        rows.append((edge, bit, old, old[3], state))
    return rows


def main():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(11.7, 6.7))
    ax.set(xlim=(-0.2, 13.5), ylim=(-0.7, 8.8))
    ax.axis('off')
    ax.text(6.6, 8.35, 'Serial input enters Q3; each rising edge shifts old values toward Q0',
            ha='center', weight='bold')
    positions = [4.1, 5.6, 7.1, 8.6]
    for x, label in zip(positions, ('Q3', 'Q2', 'Q1', 'Q0')):
        ax.add_patch(Rectangle((x-0.55, 6.6), 1.1, 0.85, edgecolor=INK, facecolor=FILL, lw=MPL_LW))
        ax.text(x, 7.02, label, ha='center', va='center')
    for left, right in [(2.4, 3.55), (4.65, 5.05), (6.15, 6.55), (7.65, 8.05), (9.15, 10.5)]:
        ax.annotate('', xy=(right, 7.02), xytext=(left, 7.02),
                    arrowprops=dict(arrowstyle='->', color=ACCENT, lw=MPL_LW))
    ax.text(1.3, 7.02, 'sampled Din', ha='center', va='center', color=HILITE)
    ax.text(11.7, 7.02, 'shifted out', ha='center', va='center', color=ACCENT)
    ax.text(6.6, 6.15, r'$[Q_3Q_2Q_1Q_0]_{new}=[D_{in},Q_{3,old},Q_{2,old},Q_{1,old}]$',
            ha='center', fontsize=14)
    headers = [('Rising edge', 0.9), ('Din sampled', 2.8), ('Old Q3 Q2 Q1 Q0', 5.4),
               ('Out = old Q0', 8.4), ('New Q3 Q2 Q1 Q0', 11.55)]
    for label, x in headers:
        ax.text(x, 5.32, label, ha='center', weight='bold', fontsize=11)
    ax.plot([0, 13.3], [4.93, 4.93], color=INK, lw=MPL_LW/1.5)
    for index, (edge, bit, old, out, new) in enumerate(sampled_trace()):
        y = 4.3-index*0.95
        if index % 2 == 0:
            ax.add_patch(Rectangle((0, y-0.37), 13.3, 0.74, facecolor=FILL, edgecolor='none'))
        old_text = ' '.join(map(str, old))
        new_text = ' '.join(map(str, new))
        for value, x, color in [(edge, 0.9, INK), (bit, 2.8, HILITE), (old_text, 5.4, INK),
                                 (out, 8.4, ACCENT), (new_text, 11.55, GOOD)]:
            ax.text(x, y, str(value), ha='center', va='center', color=color)
    ax.text(6.6, -0.08, 'Initial Q3 Q2 Q1 Q0 = 0000. Sampled input sequence: 1, 0, 1, 1.',
            ha='center', fontsize=12)
    ax.text(6.6, -0.57, 'All four stages update together after the edge; no stage uses another stage\'s new value.',
            ha='center', fontsize=11)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.04)
    save_fig(fig, 'serial-shift-trace')


if __name__ == '__main__':
    main()
