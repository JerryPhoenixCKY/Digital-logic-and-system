"""Figure: signed binary division by repeated subtraction ("restoring" division).

Panel (a): the magnitude division 100 / 25 walked through step by step.  Each
subtraction that leaves a non-negative remainder adds one to the quotient; the
loop stops when the remainder reaches zero (or would go negative, in which case
the last subtraction is undone by adding the divisor back).

Panel (b): how the sign of the quotient is fixed up *after* the magnitude
division, and why the same magnitude path gives +4 or -4 depending only on the
operand signs.

Division, so this figure is drawn with matplotlib.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import matplotlib.pyplot as plt

DIVIDEND, DIVISOR = 100, 25          # 01100100 / 00011001
W = 8


def bits(v: int, w: int = W) -> str:
    return format(v & ((1 << w) - 1), '0%db' % w)


def grp(s: str) -> str:
    return ' '.join(s[i:i + 4] for i in range(0, len(s), 4))


def main():
    apply_mpl_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 6.8),
                                   gridspec_kw={'width_ratios': [1.15, 1.0]})
    for ax in (ax1, ax2):
        ax.axis('off')
        ax.grid(False)
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)

    # ------------------------------------------------------------ panel (a)
    ax1.set_title('(a) repeated subtraction:  $100 \\div 25$', fontsize=13)

    ladder = []
    q, r = 0, DIVIDEND
    ladder.append(('start', r, q, False))
    while q < 12:
        r_next = r - DIVISOR
        if r_next < 0:                       # would overshoot -> restore
            ladder.append(('restore $+25$', r, q, True))
            break
        r = r_next
        q += 1
        ladder.append((f'subtract {q}', r, q, r == 0))
        if r == 0:
            break

    xs = {'step': 0.03, 'bin': 0.50, 'dec': 0.80, 'quo': 0.94}
    y, dy = 0.855, 0.096
    for key, head in (('step', 'step'), ('bin', 'remainder'),
                      ('dec', 'decimal'), ('quo', 'quotient')):
        ax1.text(xs[key], y + 0.055, head, fontsize=10.5, color=MUTED,
                 ha='left' if key == 'step' else 'center')

    for i, (label, rem, quo, done) in enumerate(ladder):
        yy = y - i * dy
        col = GOOD if done else INK
        ax1.text(xs['step'], yy, label, fontsize=11, color=col, va='center')
        ax1.text(xs['bin'], yy, grp(bits(rem)), fontsize=11.5, color=col,
                 family='monospace', va='center', ha='center',
                 bbox=dict(boxstyle='square,pad=0.18', fc=FILL, ec=col, lw=1.2))
        ax1.text(xs['dec'], yy, str(rem), fontsize=11.5, color=col,
                 va='center', ha='center')
        ax1.text(xs['quo'], yy, str(quo), fontsize=11.5, color=ACCENT,
                 va='center', ha='center')
        if i < len(ladder) - 1:
            ax1.text(xs['step'] + 0.015, yy - dy / 2, r'$- 0001\ 1001$',
                     fontsize=10, color=HILITE, va='center')

    ax1.text(0.03, 0.075,
             r'stop when the remainder is $0$ (or would go negative)',
             fontsize=11, color=INK, va='center')
    ax1.text(0.03, 0.030,
             r'$100 = 4 \times 25 + 0$   $\Rightarrow$   quotient $= 4 = 0100_2$',
             fontsize=11, color=INK, va='center')

    # ------------------------------------------------------------ panel (b)
    ax2.set_title('(b) fix the sign afterwards', fontsize=13)

    rows = [
        (r'$(+100)\div(+25)$', 'same', '+4', bits(4), GOOD),
        (r'$(-100)\div(-25)$', 'same', '+4', bits(4), GOOD),
        (r'$(+100)\div(-25)$', 'different', '-4', bits(-4), HILITE),
        (r'$(-100)\div(+25)$', 'different', '-4', bits(-4), HILITE),
    ]
    xr = {'op': 0.02, 'rule': 0.42, 'q': 0.72, 'bits': 0.90}
    y2, dy2 = 0.775, 0.150
    ax2.text(xr['op'], y2 + 0.105, 'operands', fontsize=10.5, color=MUTED)
    ax2.text(xr['rule'], y2 + 0.105, 'signs', fontsize=10.5, color=MUTED)
    ax2.text(xr['q'], y2 + 0.105, 'quotient', fontsize=10.5, color=MUTED)
    ax2.text(xr['bits'], y2 + 0.105, '8-bit', fontsize=10.5, color=MUTED,
             ha='center')
    for i, (op, rule, qtxt, qbits, col) in enumerate(rows):
        yy = y2 - i * dy2
        ax2.text(xr['op'], yy, op, fontsize=11.5, color=INK, va='center')
        ax2.text(xr['rule'], yy, rule, fontsize=10, color=MUTED, va='center')
        ax2.text(xr['q'], yy, qtxt, fontsize=11.5, color=col, va='center')
        ax2.text(xr['bits'], yy, grp(qbits), fontsize=10.5, color=col,
                 family='monospace', va='center', ha='center',
                 bbox=dict(boxstyle='square,pad=0.16', fc=FILL, ec=col, lw=1.2))

    ax2.text(0.02, 0.190, r'magnitude first:  $0100_2$',
             fontsize=11, color=ACCENT, va='center')
    ax2.text(0.02, 0.120, r'negative quotient: invert $+$ add $1$',
             fontsize=11, color=HILITE, va='center')
    ax2.text(0.02, 0.050, r'$1111\,1100_2 = -128+64+32+16+8+4 = -4$',
             fontsize=10.5, color=INK, va='center')

    fig.tight_layout()
    save_fig(fig, 'signed-division-restoring')

    # ---- numbers the note quotes ------------------------------------------
    q, r, steps = 0, DIVIDEND, 0
    while r >= DIVISOR:
        r -= DIVISOR
        q += 1
        steps += 1
    print('check  100 / 25  -> quotient %d = %s, remainder %d after %d subtractions'
          % (q, format(q, '04b'), r, steps))
    print('check  %d = %d x %d + %d' % (DIVIDEND, q, DIVISOR, r))
    print('check  -4 in 8-bit two\'s complement = %s (read back %d)'
          % (grp(bits(-4)), -4))


if __name__ == '__main__':
    main()
