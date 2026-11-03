"""Four-data-bit even parity generator and five-bit received-word checker."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)
from schemdraw import logic as lg


def wire(d, a, b):
    d += elm.Line().at(a).to(b)


def label(d, xy, text, fs=13, color=INK):
    d += elm.Label().at(xy).label(text, loc='center', fontsize=fs).color(color)


def tree(d, y, prefix):
    g0 = lg.Xor(inputs=2).at((1.7, y+1.1))
    g1 = lg.Xor(inputs=2).at((1.7, y-1.1))
    g2 = lg.Xor(inputs=2).at((5.1, y))
    for gate in [g0, g1, g2]:
        d += gate
    for index, pin in enumerate([g0.in1, g0.in2, g1.in1, g1.in2]):
        wire(d, (0, pin[1]), pin)
        label(d, (-.6, pin[1]), f'${prefix}_{index}$')
    for source, target, x in [(g0.out, g2.in1, 4.0), (g1.out, g2.in2, 4.4)]:
        wire(d, source, (x, source[1]))
        wire(d, (x, source[1]), (x, target[1]))
        wire(d, (x, target[1]), target)
    return g2


def build():
    d = schematic(fontsize=13)
    generator = tree(d, 0, 'A')
    wire(d, generator.out, (10.1, generator.out[1]))
    label(d, (10.6, 0), '$P$', color=HILITE)
    label(d, (5.2, 2.8), '(a) Transmit: four data bits, even-parity bit P', fs=14, color=ACCENT)
    label(d, (5.2, -2.3), r'$P=(A_0\oplus A_1)\oplus(A_2\oplus A_3)$', fs=14, color=HILITE)
    recomputed = tree(d, -6.1, 'r')
    final = lg.Xor(inputs=2).at((9.1, -6.9))
    d += final
    wire(d, recomputed.out, (8.1, recomputed.out[1]))
    wire(d, (8.1, recomputed.out[1]), (8.1, final.in1[1]))
    wire(d, (8.1, final.in1[1]), final.in1)
    label(d, (7.7, -5.7), '$Q$', color=ACCENT)
    wire(d, (6.6, final.in2[1]), final.in2)
    label(d, (6.0, final.in2[1]), '$p_r$')
    wire(d, final.out, (12.1, final.out[1]))
    label(d, (12.6, final.out[1]), '$E$', color=HILITE)
    label(d, (5.2, -3.4), '(b) Receive: four received data bits and received parity', fs=14, color=ACCENT)
    label(d, (5.2, -9.0), r'$E=Q\oplus p_r\quad (1:\ error\ detected;\ 0:\ no\ error\ detected)$', fs=13, color=HILITE)
    return d


def main():
    save_svg(build(), 'parity-generator-checker')


if __name__ == '__main__':
    main()
