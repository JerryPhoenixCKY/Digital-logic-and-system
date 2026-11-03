"""Chapter 5 pp.30-31: NOR/NAND/NAND and the equivalent bubble form."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)
from schemdraw import logic as lg


def wire(d, a, b):
    d += elm.Line().at(a).to(b)


def label(d, xy, text, fs=13, color=INK):
    d += elm.Label().at(xy).label(text, loc='center', fontsize=fs).color(color)


def chain(d, y, equivalent):
    if equivalent:
        g1 = lg.And(inputs=2, inputnots=[1, 2]).at((0, y))
        g2 = lg.And(inputs=2).at((4, y-.8))
        g3 = lg.Or(inputs=2, inputnots=[2]).at((8, y-1.6))
    else:
        g1 = lg.Nor(inputs=2).at((0, y))
        g2 = lg.Nand(inputs=2).at((4, y-.8))
        g3 = lg.Nand(inputs=2).at((8, y-1.6))
    for gate in [g1, g2, g3]:
        d += gate
    for pin, name in [(g1.in1, 'A'), (g1.in2, 'B')]:
        wire(d, (-1.3, pin[1]), pin)
        label(d, (-1.7, pin[1]), name)
    for gate, target, x in [(g1, g2.in1, 3.1), (g2, g3.in1, 7.1)]:
        wire(d, gate.out, (x, gate.out[1]))
        wire(d, (x, gate.out[1]), (x, target[1]))
        wire(d, (x, target[1]), target)
    for pin, name, x in [(g2.in2, 'C', 2.0), (g3.in2, 'D', 6.0)]:
        wire(d, (x, pin[1]), pin)
        label(d, (x-.4, pin[1]), name)
    label(d, (2.4, y+.45), '$t$' if equivalent else '$n_1$', color=ACCENT)
    label(d, (6.4, y-.35), '$u$' if equivalent else '$n_2$', color=ACCENT)
    wire(d, g3.out, (11.1, g3.out[1]))
    label(d, (11.5, g3.out[1]), '$Y$')
    if equivalent:
        equation = r'$t=\bar A\bar B,\quad u=tC,\quad Y=u+\bar D$'
        heading = '(b) Equivalent: the D input bubble remains'
    else:
        equation = r'$n_1=\overline{A+B},\quad n_2=\overline{n_1C},\quad Y=\overline{n_2D}$'
        heading = '(a) Original NOR - NAND - NAND'
    label(d, (4.8, y+1.6), heading, fs=14, color=ACCENT)
    label(d, (4.8, y-2.8), equation, fs=14, color=HILITE)


def build():
    d = schematic(fontsize=13)
    chain(d, 0, False)
    chain(d, -5.1, True)
    return d


def main():
    save_svg(build(), 'bubble-pushing-cascade')


if __name__ == '__main__':
    main()
