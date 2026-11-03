"""Figure: the three rules of combinational composition -- legal vs illegal.

Panel (a) legal.  E1 (AND) drives the internal node n1; n1 fans out to E2
(OR, whose other input is C) and to E3 (NOT).  Fan-out is fine: every node
still has exactly one driver, and the circuit has no loop.

Panel (b) illegal.  The output of E4 (NOT) and the output of E5 (AND) are tied
to the same node.  That node then has two drivers, and they can disagree
(E4 may want to pull it to 1 while E5 wants to pull it to 0), so the node
voltage -- and therefore Y -- is undefined.

Every element here is combinational, so the only rule panel (b) breaks is
"every node is either an input or connects to exactly one output".
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)
from schemdraw import logic as lg


def place(d, e, xy):
    """Add a gate to the drawing and return it (pins live in .absanchors)."""
    d += e.at(xy)
    return e


def pin(e, name):
    return tuple(e.absanchors[name])


def wire(d, p1, p2, color=INK):
    d += elm.Line().at(p1).to(p2).color(color)


def text(d, xy, s, color=INK, fs=None):
    lab = elm.Label().at(xy)
    d += (lab.label(s, fontsize=fs) if fs else lab.label(s)).color(color)


def build():
    d = schematic()

    # ------------------------------------------------------------------ (a)
    text(d, (4.70, 3.85), '(a) legal: every node is one driver or an input',
         color=GOOD)

    e1 = place(d, lg.And(inputs=2), (2.40, 1.60))       # E1
    e2 = place(d, lg.Or(inputs=2), (5.60, 0.40))        # E2
    e3 = place(d, lg.Not(), (5.40, 2.55))               # E3

    a1, a2 = pin(e1, 'in1'), pin(e1, 'in2')
    o1 = pin(e1, 'out')
    b1 = pin(e2, 'in1')
    c2 = pin(e2, 'in2')
    o2 = pin(e2, 'out')
    i3 = pin(e3, 'in1')
    o3 = pin(e3, 'out')

    node = (o1[0] + 0.65, o1[1])                        # internal node n1

    wire(d, (1.10, a1[1]), a1)                          # A -> E1.in1
    wire(d, (1.10, a2[1]), a2)                          # B -> E1.in2
    wire(d, o1, node)                                   # E1.out -> n1
    wire(d, node, (node[0], i3[1]))                     # n1 up ...
    wire(d, (node[0], i3[1]), i3)                       # ... into E3
    wire(d, node, (node[0], b1[1]))                     # n1 down ...
    wire(d, (node[0], b1[1]), b1)                       # ... into E2.in1
    wire(d, (3.30, c2[1]), c2)                          # C -> E2.in2
    wire(d, o2, (o2[0] + 0.80, o2[1]))                  # E2.out -> Y
    wire(d, o3, (o3[0] + 0.80, o3[1]))                  # E3.out -> Z
    d += elm.Dot().at(node).color(INK)

    text(d, (0.80, a1[1]), 'A')
    text(d, (0.80, a2[1]), 'B')
    text(d, (3.02, c2[1]), 'C')
    text(d, (3.35, 2.48), 'E1')
    text(d, (6.40, 1.15), 'E2')
    text(d, (o3[0] - 0.45, 3.28), 'E3')
    text(d, (node[0] - 0.42, node[1] + 0.42), 'n1')
    text(d, (o2[0] + 1.05, o2[1]), 'Y', color=HILITE)
    text(d, (o3[0] + 1.35, o3[1]), 'Z', color=HILITE)

    # ------------------------------------------------------------------ (b)
    text(d, (4.70, -0.62),
         '(b) illegal: two gate outputs tied to one node', color=BAD)

    e4 = place(d, lg.Not(leadin=0.30, leadout=0.30), (2.40, -1.30))  # E4
    e5 = place(d, lg.And(inputs=2), (2.40, -2.70))                   # E5

    p4 = pin(e4, 'in1')
    q4 = pin(e4, 'out')
    p5a, p5b = pin(e5, 'in1'), pin(e5, 'in2')
    q5 = pin(e5, 'out')

    bad_node = (q5[0] + 0.85, q5[1])                    # two drivers meet here

    wire(d, (1.10, p4[1]), p4)                          # A -> E4.in1
    wire(d, (1.10, p5a[1]), p5a)                        # B -> E5.in1
    wire(d, (1.10, p5b[1]), p5b)                        # C -> E5.in2
    wire(d, q4, (bad_node[0], q4[1]), color=BAD)        # E4.out ...
    wire(d, (bad_node[0], q4[1]), bad_node, color=BAD)  # ... down to the node
    wire(d, q5, bad_node, color=BAD)                    # E5.out -> same node
    wire(d, bad_node, (bad_node[0] + 0.90, bad_node[1]), color=BAD)
    d += elm.Dot().at(bad_node).color(BAD)
    d += elm.Dot(radius=0.24, open=True).at(bad_node).color(BAD)

    text(d, (0.80, p4[1]), 'A')
    text(d, (0.80, p5a[1]), 'B')
    text(d, (0.80, p5b[1]), 'C')
    text(d, (4.30, -0.95), 'E4')
    text(d, (4.67, -2.35), 'E5')
    text(d, (bad_node[0] + 1.16, bad_node[1]), 'Y', color=BAD)
    text(d, (5.60, -3.90),
         'the two drivers disagree -> node level undefined', color=BAD,
         fs=12)

    return d


def main():
    d = build()
    save_svg(d, 'combinational-rules')

    # ---- perfect induction on the two circuits ---------------------------
    print('check  the legal circuit of panel (a), all 8 input combinations:')
    for a, b, c in [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
                    (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]:
        n1 = a & b                      # E1: AND
        y = n1 | c                      # E2: OR
        z = 1 - n1                      # E3: NOT
        print('       A=%d B=%d C=%d -> n1=E1=%d  Y=E2=%d  Z=E3=%d'
              % (a, b, c, n1, y, z))

    print('check  the illegal node of panel (b): E4=NOT A drives it, '
          'E5=AND(B,C) also drives it')
    bad = 0
    for a, b, c in [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
                    (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]:
        d4, d5 = 1 - a, b & c
        clash = 'CONFLICT' if d4 != d5 else 'agree'
        bad += d4 != d5
        print('       A=%d B=%d C=%d -> E4=%d, E5=%d  -> %s'
              % (a, b, c, d4, d5, clash))
    print('check  %d of 8 input combinations make the two drivers disagree '
          '-> the node level is undefined' % bad)


if __name__ == '__main__':
    main()
