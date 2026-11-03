"""Figure: DeMorgan's theorems at gate level.

(a)  NAND  ==  OR with inverted inputs:   (A*B)' = A' + B'
(b)  NOR   ==  AND with inverted inputs:  (A+B)' = A' * B'

Each row is one theorem: the same two inputs A, B feed a single gate on the
left and a gate with inverted inputs on the right; the "=" in the middle says
the two gates compute the same function for every input combination.

The gate-level picture is the practical reading of DeMorgan: push the bubble
from the output to the inputs (and swap AND <-> OR) and the function does not
change.  That is how a NAND/NOR-only circuit is rewritten as an AND/OR one.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)
from schemdraw import logic as lg


def place(d, e, xy):
    d += e.at(xy)
    return e


def pin(e, name):
    return tuple(e.absanchors[name])


def wire(d, p1, p2, color=INK):
    d += elm.Line().at(p1).to(p2).color(color)


def text(d, xy, s, color=INK, fs=None):
    lab = elm.Label().at(xy)
    d += (lab.label(s, fontsize=fs) if fs else lab.label(s)).color(color)


def one_row(d, y, gate_left, gate_right, eq_left, eq_right, title):
    """One equivalence: left gate == right gate, both fed by A and B."""
    g1 = place(d, gate_left, (1.60, y))
    g2 = place(d, gate_right, (6.30, y))

    a1, b1 = pin(g1, 'in1'), pin(g1, 'in2')
    o1 = pin(g1, 'out')
    a2, b2 = pin(g2, 'in1'), pin(g2, 'in2')
    o2 = pin(g2, 'out')

    wire(d, (0.85, a1[1]), a1)                      # A -> left gate
    wire(d, (0.85, b1[1]), b1)                      # B -> left gate
    wire(d, o1, (o1[0] + 0.70, o1[1]))              # left output stub
    wire(d, (5.55, a2[1]), a2)                      # A -> right gate
    wire(d, (5.55, b2[1]), b2)                      # B -> right gate
    wire(d, o2, (o2[0] + 0.70, o2[1]))              # right output stub

    text(d, (0.58, a1[1]), 'A')
    text(d, (0.58, b1[1]), 'B')
    text(d, (5.28, a2[1]), 'A')
    text(d, (5.28, b2[1]), 'B')
    text(d, (4.72, y), '=', color=HILITE, fs=22)
    text(d, (2.60, y + 0.95), eq_left, fs=15)
    text(d, (7.35, y + 0.95), eq_right, fs=15)
    text(d, (4.72, y + 1.80), title, color=ACCENT, fs=13)


def build():
    d = schematic()

    one_row(d, 0.0,
            lg.Nand(inputs=2),
            lg.Or(inputs=2, inputnots=[1, 2]),
            r'$\overline{AB}$', r'$\bar{A}+\bar{B}$',
            '(a)  NAND  =  OR with inverted inputs')

    one_row(d, -2.70,
            lg.Nor(inputs=2),
            lg.And(inputs=2, inputnots=[1, 2]),
            r'$\overline{A+B}$', r'$\bar{A}\,\bar{B}$',
            '(b)  NOR  =  AND with inverted inputs')

    return d


def main():
    d = build()
    save_svg(d, 'demorgan-gate-equivalence')

    # ---- perfect induction: the two sides agree in every row ---------------
    print('check  (A*B)\' vs A\'+B\'   and   (A+B)\' vs A\'*B\'')
    for a in (0, 1):
        for b in (0, 1):
            nand_side = 1 - (a & b)
            or_side = (1 - a) | (1 - b)
            nor_side = 1 - (a | b)
            and_side = (1 - a) & (1 - b)
            print('       A=%d B=%d -> NAND=%d  bubbled-OR=%d  %s   |   '
                  'NOR=%d  bubbled-AND=%d  %s'
                  % (a, b, nand_side, or_side,
                     'equal' if nand_side == or_side else 'DIFFERENT',
                     nor_side, and_side,
                     'equal' if nor_side == and_side else 'DIFFERENT'))

    print('check  3-variable generalisation, all 8 combinations:')
    for x in (0, 1):
        for y in (0, 1):
            for z in (0, 1):
                lhs = 1 - (x & y & z)
                rhs = (1 - x) | (1 - y) | (1 - z)
                if lhs != rhs:
                    print('       MISMATCH at', x, y, z)
    print('       (X*Y*Z)\' = X\'+Y\'+Z\' holds in all 8 rows')


if __name__ == '__main__':
    main()
