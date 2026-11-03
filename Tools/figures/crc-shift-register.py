"""CRC encoder hardware: 4-stage serial shift register with one XOR feedback tap.

This four-stage register divides by H = x G = 10100 = x^4 + x^2,
where the lecture generator is G = 1010. Its next state is

    D0 <- D_in      D1 <- Q0      D2 <- Q1 ^ Q3      D3 <- Q2

so the leading (most significant) stage Q3 is fed back through one XOR gate
into the x^2 tap of H. Feeding 1101 0011 0000 (data + four zeros) leaves 0100
in the register - exactly the remainder of the long division drawn in
crc-modulo2-division.svg.  The register is simulated below, so the drawing and
the numbers cannot drift apart.

Geometry note: one drawing unit is about 22 px at fontsize 15, i.e. a text line
is roughly one unit tall - the annotation labels therefore use fontsize 10.5
and the free bands between the element rows.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig,
                      dot)
import schemdraw.logic as logic


def simulate(stream):
    """Run the register described above; q = [Q0, Q1, Q2, Q3]."""
    q = [0, 0, 0, 0]
    for b in stream:
        q = [int(b), q[0], q[1] ^ q[3], q[2]]
    return "".join(str(x) for x in reversed(q))           # Q3..Q0


assert simulate("110100110000") == "0100"      # data + four zeros -> checksum
assert simulate("110100110100") == "0000"      # clean frame -> no error
assert simulate("110100110101") == "0001"      # one flipped bit -> error

D = schematic()
FF_X = [0.0, 4.6, 12.5, 17.0]                  # D-input x of the four stages
BUS_Y = -2.7                                   # clock bus
FB_Y = 6.2                                     # feedback rail
XOR_C = (9.6, 2.75)                            # XOR gate centre
NOTE_FS = 10.5                                 # annotation font size

# ---- four D flip-flops ----------------------------------------------------
ffs = []
for i, x in enumerate(FF_X):
    ff = elm.DFlipFlop().at((x, 0.0))
    ff.label(f"$D_{i}$", loc="top")
    ffs.append(ff)
    D += ff
ff0, ff1, ff2, ff3 = ffs

# ---- data path ------------------------------------------------------------
D += elm.Line().at((ff0.D.x - 2.1, ff0.D.y)).to(ff0.D)
D += elm.Label().at((ff0.D.x - 3.35, ff0.D.y + 0.1)).label("$D_{in}$",
                                                           loc="center")
D += elm.Line().at(ff0.Q).to(ff1.D)
D += elm.Line().at(ff1.Q).to((XOR_C[0], ff1.Q.y))          # Q1 into the gate

xor = logic.Xor(inputs=2).at(XOR_C).label("XOR", loc="top")
D += xor
D += elm.Line().at(xor.out).to((ff2.D.x - 0.5, xor.out.y))
D += elm.Line().at((ff2.D.x - 0.5, xor.out.y)).to((ff2.D.x - 0.5, ff2.D.y))
D += elm.Line().at((ff2.D.x - 0.5, ff2.D.y)).to(ff2.D)
D += elm.Line().at(ff2.Q).to(ff3.D)
D += elm.Line().at(ff3.Q).to((ff3.Q.x + 2.6, ff3.Q.y))
D += elm.Label().at((ff3.Q.x + 3.55, ff3.Q.y + 0.1)).label("out", loc="center")

# ---- XOR feedback: the bit shifted out of D3 returns to the x^2 tap -------
D += elm.Line().at(ff3.Q).to((ff3.Q.x, FB_Y))
D += elm.Line().at((ff3.Q.x, FB_Y)).to((XOR_C[0], FB_Y))
D += elm.Line().at((XOR_C[0], FB_Y)).to(xor.in1)
D += elm.Label().at(((ff3.Q.x + XOR_C[0]) / 2, FB_Y + 0.75)).label(
    "$Q_3$ fed back (leading bit)", loc="center", fontsize=NOTE_FS)

# ---- clock bus ------------------------------------------------------------
D += elm.Line().at((ff0.CLK.x - 1.0, BUS_Y)).to((ff3.CLK.x + 1.0, BUS_Y))
D += elm.Label().at((ff0.CLK.x - 1.4, BUS_Y)).label("CLK", loc="left")
for ff in ffs:
    D += elm.Line().at((ff.CLK.x, ff.CLK.y)).to((ff.CLK.x, BUS_Y))
    dot(D, (ff.CLK.x, BUS_Y))

# ---- annotations (kept in the free bands, smaller than the element text) --
D += elm.Label().at((1.5, 5.85)).label(
    "$H$ = 10100 = $x^4+x^2$", loc="center", fontsize=NOTE_FS)
D += elm.Label().at((1.5, 4.75)).label(
    "4 x D flip-flop shift register + XOR", loc="center", fontsize=NOTE_FS)
D += elm.Label().at((7.5, -3.45)).label(
    "modulo-2 addition (XOR): 0$\\oplus$0=0, 0$\\oplus$1=1, "
    "1$\\oplus$0=1, 1$\\oplus$1=0", loc="center", fontsize=NOTE_FS)
D += elm.Label().at((7.5, -4.45)).label(
    "each box is one rising-edge D flip-flop, outputs $Q_0$..$Q_3$",
    loc="center", fontsize=NOTE_FS)
D += elm.Label().at((7.5, -5.45)).label(
    "12 clocks with $D_{in}$ = 1101 0011 0000  ->  register = 0100",
    loc="center", fontsize=NOTE_FS)

save_svg(D, "crc-shift-register")
