from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out = Path('output/hw3')
out.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12})
times = [-1, 0, 2, 3, 4, 5, 7, 9]
signals = [
    ('A', [1, 0, 0, 0, 0, 0, 0, 0], 0, '1 to 0 at 0 ns'),
    ('P', [0, 0, 0, 0, 0, 1, 1, 1], 5, '0 to 1 at 5 ns'),
    ('Q', [1, 1, 0, 0, 0, 0, 0, 0], 2, '1 to 0 at 2 ns'),
    ('F', [1, 1, 1, 1, 0, 0, 1, 1], None, ''),
]
fig, axes = plt.subplots(4, 1, figsize=(11.5, 6.2), sharex=True,
                         gridspec_kw={'hspace': .33})
for ax, (name, values, transition, label) in zip(axes, signals):
    color = '#c23a3a' if name == 'F' else '#175c94'
    ax.step(times, values, where='post', color=color, linewidth=2.7)
    for t in [0, 2, 3, 4, 5, 7]:
        ax.axvline(t, color='#dce2e8', linewidth=.8, linestyle='--', zorder=0)
    ax.set_yticks([0, 1])
    ax.set_ylim(-.25, 1.5)
    ax.set_ylabel(name, rotation=0, labelpad=22, fontsize=16, fontweight='bold')
    for side in ['top', 'right']:
        ax.spines[side].set_visible(False)
    ax.spines['left'].set_color('#b5bec8')
    ax.spines['bottom'].set_color('#b5bec8')
    if label:
        ax.text(8.8, 1.21, label, ha='right', fontsize=10, color='#364553')
axes[-1].axvspan(4, 7, color='#c23a3a', alpha=.09)
axes[-1].annotate('', xy=(4, .52), xytext=(7, .52),
                  arrowprops={'arrowstyle': '<->', 'color': '#c23a3a', 'lw': 1.5})
axes[-1].text(5.5, .69, 'Low glitch: 3 ns', ha='center', fontsize=11, color='#a02c2c')
axes[-1].set_xticks([0, 2, 3, 4, 5, 7, 9])
axes[-1].set_xlim(-1, 9)
axes[-1].set_xlabel('Time t (ns)', labelpad=10)
fig.suptitle('Q5: propagation delays and the static-1 hazard', fontsize=17, y=.98)
fig.subplots_adjust(top=.89, bottom=.12, left=.1, right=.97)
fig.savefig(out / 'HW3_Q5_timing.png', dpi=180)
print(out / 'HW3_Q5_timing.png')
