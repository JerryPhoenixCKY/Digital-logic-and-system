"""3-07 Exclusive-OR Gate -- the half adder: XOR gives Sum, AND gives Carry.

One XOR gate and one AND gate share the same two inputs A and B (node dots mark
the fan-out).  The XOR output is the sum bit and the AND output is the carry bit,
which is the lecture's p.11 statement "an XOR gate can be used to add two bits":

    A B | Sum = A xor B | Carry = A and B | 2*Carry + Sum
    0 0 |       0       |        0        |       0
    0 1 |       1       |        0        |       1
    1 0 |       1       |        0        |       1
    1 1 |       0       |        1        |       2 = 10 (base 2)

The two branch wires are routed so that no two wires cross (a crossing without a
dot would be ambiguous); the only dots are the two fan-out nodes on the A and B
input lines.

Run:  D:\\anaconda\\python.exe Tools\\figures\\xor-half-adder.py
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig,
                      dot)
import schemdraw.logic as logic

# the circuit below is the half adder: Sum = A xor B, Carry = A and B
HALF_ADDER = {(a, b): (a ^ b, a & b) for a in (0, 1) for b in (0, 1)}
assert HALF_ADDER == {(0, 0): (0, 0), (0, 1): (1, 0),
                      (1, 0): (1, 0), (1, 1): (0, 1)}
assert all(2 * carry + s == a + b for (a, b), (s, carry) in HALF_ADDER.items())

D = schematic()
FS_NOTE = 10.5                                   # annotation font size

# ---- the two gates (stacked; both are symmetric, so the input order of the
# ---- AND gate is free and is chosen to keep the wiring crossing-free) -------
xor = logic.Xor(inputs=2).at((0.0, 5.0)).label("XOR", loc="top")
andg = logic.And(inputs=2).at((0.0, 0.0)).label("AND", loc="top")
D += xor
D += andg

# ---- input A: straight into XOR in1, with a branch down to AND in2 ---------
D += elm.Line().at((-10.0, xor.in1[1])).to(xor.in1)
D += elm.Label().at((-10.55, xor.in1[1])).label("$A$", loc="center")
dot(D, (-8.0, xor.in1[1]))
D += elm.Line().at((-8.0, xor.in1[1])).to((-8.0, andg.in2[1]))
D += elm.Line().at((-8.0, andg.in2[1])).to(andg.in2)

# ---- input B: into XOR in2, with a branch down to AND in1 ------------------
D += elm.Line().at((-5.0, xor.in2[1])).to(xor.in2)
D += elm.Label().at((-5.55, xor.in2[1])).label("$B$", loc="center")
dot(D, (-3.0, xor.in2[1]))
D += elm.Line().at((-3.0, xor.in2[1])).to((-3.0, andg.in1[1]))
D += elm.Line().at((-3.0, andg.in1[1])).to(andg.in1)

# ---- outputs --------------------------------------------------------------
D += elm.Line().at(xor.out).to((5.6, xor.out[1]))
D += elm.Label().at((7.4, xor.out[1])).label("Sum $= A\\oplus B$", loc="center")
D += elm.Line().at(andg.out).to((5.6, andg.out[1]))
D += elm.Label().at((7.4, andg.out[1])).label("Carry $= A\\cdot B$", loc="center")

# ---- annotations ----------------------------------------------------------
D += elm.Label().at((-2.0, 7.35)).label(
    "Half adder: A and B in, Sum and Carry out", loc="center", fontsize=12.0)
D += elm.Label().at((-2.0, 6.55)).label(
    "XOR adds the two bits (Sum), AND reports the overflow (Carry)",
    loc="center", fontsize=FS_NOTE)
D += elm.Label().at((3.2, -1.75)).label(
    "$1+1=10$ (base 2):  Sum $=0$, Carry $=1$", loc="center", fontsize=FS_NOTE,
    color=HILITE)
D += elm.Label().at((1.0, -2.75)).label(
    "filled dots = the two input nodes fan out to both gates",
    loc="center", fontsize=FS_NOTE, color=MUTED)

save_svg(D, "xor-half-adder")
