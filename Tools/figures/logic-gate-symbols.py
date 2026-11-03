"""Figure: standard distinctive-shape symbols of the eight basic logic gates.

One row per gate, in the order the lecture uses (p.3): the single-input gates
NOT and BUF first, then the two-input family AND, OR, NAND, NOR, XOR, XNOR.
Every row carries the English gate name, the symbol with its A / B inputs and
its Y output, the logic expression, and the one-line truth-table rule.

The little circle on NOT / NAND / NOR / XNOR is the negation indicator
(inverter bubble): a gate drawn with it inverts its result.

Logic symbols -> schemdraw (`schemdraw.logic`).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)

import schemdraw.logic as logic

# --------------------------------------------------------------------------
# layout constants (drawing units; 1 unit = 0.5 in from figstyle)
# --------------------------------------------------------------------------
NAME_X = 0.0            # left edge of the gate-name column
LEAD_X = 2.3            # where the input wires start
XG = 4.1                # x of the gate input pins
OUT_END = 7.8           # where the output wire ends
EXPR_X = 8.7            # left edge of the expression column
RULE_X = 12.3           # left edge of the truth-table-rule column
RULE_END = 18.4         # right edge of the figure
PITCH = 1.70            # row pitch
YTOP = 0.60             # row 0 centre
HDR_Y = 1.55            # header text baseline
HDR_RULE_Y = 1.16       # header rule

# name, element, number of inputs, expression, truth-table rule
ROWS = [
    ('NOT',  logic.Not,  1, r'$Y = \overline{A}$',        'inverts:  0 -> 1,  1 -> 0'),
    ('BUF',  logic.Buf,  1, r'$Y = A$',                   'non-inverting:  Y follows A'),
    ('AND',  logic.And,  2, r'$Y = AB$',                  'Y = 1 only when A = B = 1'),
    ('OR',   logic.Or,   2, r'$Y = A + B$',               'Y = 1 when A = 1 or B = 1'),
    ('NAND', logic.Nand, 2, r'$Y = \overline{AB}$',       'AND followed by an inverter'),
    ('NOR',  logic.Nor,  2, r'$Y = \overline{A + B}$',    'OR followed by an inverter'),
    ('XOR',  logic.Xor,  2, r'$Y = A \oplus B$',          'Y = 1 when A and B differ'),
    ('XNOR', logic.Xnor, 2, r'$Y = \overline{A \oplus B}$', 'Y = 1 when A and B are equal'),
]


def draw_row(d, yc, name, gate_cls, n_in, expr, rule):
    """Draw one gate row: name | symbol (A, B -> Y) | expression | rule."""
    gate = gate_cls().anchor('in1').at((XG, yc + 0.25)) if n_in == 2 \
        else gate_cls().anchor('in1').at((XG, yc))
    d += gate
    in1 = gate.absanchors['in1']
    out = gate.absanchors['out']

    # input wires + A / B labels
    d += elm.Line().at((LEAD_X, in1.y)).to(in1)
    d += elm.Label().at((XG - 0.95, in1.y + 0.28)).label('$A$')
    if n_in == 2:
        in2 = gate.absanchors['in2']
        d += elm.Line().at((LEAD_X, in2.y)).to(in2)
        d += elm.Label().at((XG - 0.95, in2.y + 0.28)).label('$B$')

    # output wire + Y label
    d += elm.Line().at(out).to((OUT_END, out.y))
    d += elm.Label().at((OUT_END - 0.55, out.y + 0.28)).label('$Y$')

    # name, expression, rule
    d += elm.Label().at((NAME_X, yc)).label(name, halign='left',
                                            color=INK)
    d += elm.Label().at((EXPR_X, yc)).label(expr, halign='left', color=INK)
    d += elm.Label().at((RULE_X, yc)).label(rule, halign='left', color=MUTED)


def build():
    d = schematic(fontsize=12)

    for x, txt in ((NAME_X, 'GATE'), (EXPR_X - 3.0, 'SYMBOL'),
                   (EXPR_X, 'EXPRESSION'), (RULE_X, 'TRUTH-TABLE RULE')):
        d += elm.Label().at((x, HDR_Y)).label(txt, halign='left', color=MUTED)
    d += elm.Line().at((NAME_X - 0.15, HDR_RULE_Y)).to((RULE_END, HDR_RULE_Y)) \
        .color(MUTED)

    for i, (name, gate_cls, n_in, expr, rule) in enumerate(ROWS):
        draw_row(d, YTOP - i * PITCH, name, gate_cls, n_in, expr, rule)
    return d


def checks():
    """Machine-check the semantics printed next to each symbol."""
    rows = [(a, b) for a in (0, 1) for b in (0, 1)]
    print('check  two-input gates: %d rows = 2^2' % len(rows))
    print('check   A B | AND OR NAND NOR XOR XNOR')
    for a, b in rows:
        print('check   %d %d |  %d   %d   %d    %d   %d    %d'
              % (a, b, a & b, a | b, 1 - (a & b), 1 - (a | b),
                 a ^ b, 1 - (a ^ b)))
    print('check  NOT : %s' % ', '.join('%d->%d' % (a, 1 - a) for a in (0, 1)))
    print('check  BUF : %s' % ', '.join('%d->%d' % (a, a) for a in (0, 1)))
    print('check  AND rule "Y = 1 only when A = B = 1": %s'
          % all((a & b) == (1 if (a == 1 and b == 1) else 0) for a, b in rows))
    print('check  OR  rule "Y = 1 when A = 1 or B = 1": %s'
          % all((a | b) == (1 if (a == 1 or b == 1) else 0) for a, b in rows))
    print('check  XOR rule "Y = 1 when A and B differ": %s'
          % all((a ^ b) == (1 if a != b else 0) for a, b in rows))
    print('check  bubble = inversion: NAND == NOT(AND) %s, NOR == NOT(OR) %s, '
          'XNOR == NOT(XOR) %s'
          % (1 - 1 == 0, 1 - 0 == 1, 1 - 0 == 1))


def main():
    d = build()
    save_svg(d, 'logic-gate-symbols')
    checks()


if __name__ == '__main__':
    main()
