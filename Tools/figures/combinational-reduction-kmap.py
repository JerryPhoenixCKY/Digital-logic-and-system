"""Chapter 5 p.19: two essential groups, including wrap-around and overlap."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch


def build():
    apply_mpl_style()
    fig, ax = plt.subplots(figsize=(8.3, 5.5))
    ax.set_xlim(-.2, 7.6)
    ax.set_ylim(-.6, 5.3)
    ax.axis('off')
    gray = [(0, 0), (0, 1), (1, 1), (1, 0)]
    on = {0, 1, 8, 9, 12}
    for row, (a, b) in enumerate(gray):
        for col, (c, d) in enumerate(gray):
            i = 8*a+4*b+2*c+d
            x, y = 1+1.5*col, 3.6-.9*row
            ax.add_patch(Rectangle((x, y), 1.5, .9,
                         facecolor=FILL if i in on else 'white',
                         edgecolor=INK, linewidth=2.0))
            ax.text(x+.75, y+.48, str(int(i in on)), ha='center', va='center', fontsize=16)
            ax.text(x+1.12, y+.22, f'm{i}', ha='right', va='center', color=MUTED, fontsize=9)
    for k, bits in enumerate(gray):
        s = ''.join(map(str, bits))
        ax.text(1.75+1.5*k, 4.74, s, ha='center', va='center')
        ax.text(.3, 4.05-.9*k, s, ha='center', va='center')
    ax.text(.25, 4.72, 'AB / CD', ha='center', va='center', fontsize=11)
    ax.text(4, 5.15, 'Two essential implicants: wrap-around and overlap',
            ha='center', va='center', color=ACCENT, fontsize=14)
    for y in [3.66, .96]:
        ax.add_patch(FancyBboxPatch((1.06, y), 2.88, .78,
                     boxstyle='round,pad=0.01,rounding_size=0.16',
                     fill=False, edgecolor=ACCENT, linewidth=2.2))
    ax.plot([1.05, .85, .85, 1.05], [4.05, 4.05, 1.35, 1.35],
             color=ACCENT, linestyle='--', linewidth=2.0)
    ax.add_patch(FancyBboxPatch((1.18, 1.04), 1.14, 1.50,
                  boxstyle='round,pad=0.01,rounding_size=0.14',
                  fill=False, edgecolor=HILITE, linewidth=2.2))
    ax.text(2.5, .42, r'$\{0,1,8,9\}\ \to\ \bar B\bar C$',
            color=ACCENT, ha='center', va='center', fontsize=13)
    ax.text(5.6, .42, r'$\{8,12\}\ \to\ A\bar C\bar D$',
            color=HILITE, ha='center', va='center', fontsize=13)
    ax.text(4, -.23, r'$X=\bar B\bar C+A\bar C\bar D\quad$ (cell 8 is shared)',
            ha='center', va='center', fontsize=14)
    return fig


def main():
    save_fig(build(), 'combinational-reduction-kmap')


if __name__ == '__main__':
    main()
