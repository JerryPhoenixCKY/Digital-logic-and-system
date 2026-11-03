"""AND-OR and AOI: the same products, complementary outputs."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)
from schemdraw import logic as lg


def wire(d, a, b):
    d += elm.Line().at(a).to(b)


def label(d, xy, text, fs=13, color=INK):
    d += elm.Label().at(xy).label(text, loc='center', fontsize=fs).color(color)


def build():
    d = schematic(fontsize=13)
    for y, inverted in [(0, False), (-5.3, True)]:
        upper = lg.And(inputs=2).at((0, y+1.1))
        lower = lg.And(inputs=2).at((0, y-1.1))
        final = (lg.Nor(inputs=2) if inverted else lg.Or(inputs=2)).at((5, y))
        d += upper
        d += lower
        d += final
        for gate, names in [(upper, ('A', 'B')), (lower, ('C', 'D'))]:
            for pin, name in zip([gate.in1, gate.in2], names):
                wire(d, (-1.3, pin[1]), pin)
                label(d, (-1.7, pin[1]), name)
        for gate, target, x in [(upper, final.in1, 3.7), (lower, final.in2, 4.1)]:
            wire(d, gate.out, (x, gate.out[1]))
            wire(d, (x, gate.out[1]), (x, target[1]))
            wire(d, (x, target[1]), target)
        label(d, (2.5, y+1.55), '$AB$', color=ACCENT)
        label(d, (2.5, y-1.55), '$CD$', color=ACCENT)
        wire(d, final.out, (8.2, y))
        label(d, (8.7, y), '$Y$')
        heading = '(b) AND-OR-Invert (AOI)' if inverted else '(a) AND-OR'
        equation = r'$Y=\overline{AB+CD}$' if inverted else r'$Y=AB+CD$'
        label(d, (3.7, y+2.5), heading, fs=15, color=ACCENT)
        label(d, (3.7, y-2.2), equation, fs=15, color=HILITE)
    return d


def main():
    save_svg(build(), 'and-or-aoi-logic')


if __name__ == '__main__':
    main()
