# -*- coding: utf-8 -*-
"""ECE2050 Chapter 2 — verify every number that the notes will quote.

Run:  D:\\anaconda\\python.exe .scratch\\verify_ch2.py > .scratch\\verify_ch2.txt
Slide page numbers refer to `.scratch/extract/ECE2050-Chap2.txt`.
"""
from __future__ import annotations

import struct

DIGITS = "0123456789ABCDEF"


def to_base(value: int, base: int, width: int | None = None) -> str:
    if value == 0:
        s = "0"
    else:
        neg = value < 0
        v = abs(value)
        out = []
        while v:
            out.append(DIGITS[v % base])
            v //= base
        s = "".join(reversed(out))
        if neg:
            s = "-" + s
    if width:
        s = s.zfill(width)
    return s


def from_base(text: str, base: int) -> int:
    return int(text, base)


def frac_to_base(value: float, base: int, nbits: int) -> str:
    out = []
    v = value
    for _ in range(nbits):
        v *= base
        d = int(v)
        out.append(DIGITS[d])
        v -= d
    return "".join(out)


def twos(value: int, width: int) -> str:
    return to_base(value & ((1 << width) - 1), 2, width)


def from_twos(bits: str) -> int:
    n = len(bits)
    v = int(bits, 2)
    return v - (1 << n) if bits[0] == "1" else v


def crc_divide(dividend: str, gen: str) -> tuple[str, str]:
    """Modulo-2 (XOR) long division. Returns (quotient, remainder)."""
    g = len(gen)
    work = list(dividend)
    for i in range(len(dividend) - g + 1):
        if work[i] == "1":
            for j in range(g):
                work[i + j] = "1" if work[i + j] != gen[j] else "0"
    return "".join(work[: len(dividend) - g + 1]), "".join(work[-(g - 1):])


def fix16(value: float) -> int:
    return int(round(value * (1 << 16)))


def main() -> None:
    P = print
    P("=" * 78)
    P("ECE2050 Chapter 2 — numeric verification report")
    P("=" * 78)

    # ---------------------------------------------------------------- slide 5-7
    P("\n--- positional / base-R (slide 4-7) ---")
    P("(568.23)10 expansion =", 5 * 100 + 6 * 10 + 8 + 2 * 0.1 + 3 * 0.01)
    P("(10.101)2 = ", 1 * 2 + 0 * 1 + 1 * 0.5 + 0 * 0.25 + 1 * 0.125)
    P("(10.101)2 in hex fraction =", frac_to_base(0.625, 2, 3))

    # ---------------------------------------------------------------- slide 10-13
    P("\n--- conversion (slide 10-13, 15-20) ---")
    P("(10011)2      =", from_base("10011", 2))
    P("(53)10        =", to_base(53, 2), "(expect 110101)")
    P("method-1 powers of 2 for 53: 32+16+4+1 =", 32 + 16 + 4 + 1)
    rem, q = [], 53
    while q:
        q, r = divmod(q, 2)
        rem.append(r)
    P("method-2 remainders (LSB first):", rem, "-> MSB-first", "".join(map(str, reversed(rem))))
    P("4-bit values 2^4 =", 2 ** 4, "range [0,", 2 ** 4 - 1, "]")
    P("(2374)8       =", from_base("2374", 8), "(expect 1276)")
    P("(E5)16        =", from_base("E5", 16), "(expect 229)")
    P("(359)10 -> octal  =", to_base(359, 8), "(expect 547)")
    P("(650)10 -> hex    =", to_base(650, 16), "(expect 28A)")
    P("(7526)8  -> binary =", to_base(from_base("7526", 8), 2), "(expect 111101010110)")
    P("(CF8E)16 -> binary =", to_base(from_base("CF8E", 16), 2), "(expect 1100111110001110)")
    P("(100110011010)2 -> octal =", to_base(from_base("100110011010", 2), 8), "(expect 4632)")
    P("(1100101001010111)2 -> hex =", to_base(from_base("1100101001010111", 2), 16), "(expect CA57)")

    # ---------------------------------------------------------------- slide 24-26
    P("\n--- bits, bytes, powers of two (slide 24-26) ---")
    P("byte  = 8 bits -> values", 2 ** 8, "range [0,", 2 ** 8 - 1, "]")
    P("nibble= 4 bits -> values", 2 ** 4, "range [0,", 2 ** 4 - 1, "]")
    for e in (10, 20, 30, 40, 50, 60):
        P(f"  2^{e} = {2 ** e:,}")
    P("2^24 =", 2 ** 24, "≈", round(2 ** 24 / 1e6, 2), "million")
    P("2^32 =", 2 ** 32, "≈", round(2 ** 32 / 1e9, 2), "billion")
    P("2^32 - 1 =", 2 ** 32 - 1)

    # ---------------------------------------------------------------- slide 28-33
    P("\n--- binary arithmetic (slide 28-33) ---")
    P("1011 + 0110 =", to_base(from_base("1011", 2) + from_base("0110", 2), 2),
      "=", from_base("1011", 2) + from_base("0110", 2), "(needs 5 bits -> 4-bit overflow)")
    P("111 + 1011 =", from_base("111", 2) + from_base("1011", 2))
    q, r = divmod(from_base("1001", 2), from_base("11", 2))
    P("(1001)2 / (11)2 =", to_base(q, 2), "rem", to_base(r, 2), "-> 9/3 =", q)
    P("100 / 25 =", 100 // 25, " quotient in binary", to_base(4, 2, 4))

    # ---------------------------------------------------------------- slide 35-41
    P("\n--- sign/magnitude and two's complement (slide 35-41) ---")
    P("4-bit sign/magnitude: +6 = 0110, -6 = 1110 ; range [-7, 7]")
    P("1110 + 0110 =", to_base(from_base("1110", 2) + from_base("0110", 2), 2),
      "-> 4-bit result", to_base((from_base("1110", 2) + from_base("0110", 2)) & 0xF, 2, 4),
      "= ", from_twos(to_base((from_base("1110", 2) + from_base("0110", 2)) & 0xF, 2, 4)),
      "(sign/magnitude reading, wrong)")
    P("two's complement of 3 (0011) ->", twos(-3, 4), "(expect 1101)")
    P("1001 in two's complement =", from_twos("1001"), "(expect -7)")
    P("1111 two's complement ->", to_base((-1) & 0xF, 2, 4), "= -1")
    P("reversing 1111 (invert+1) =", twos(-(-1), 4), "= +1  -> mirror of the T/F quiz item")
    P("Most negative 4-bit =", twos(-8, 4), "most positive =", twos(7, 4))
    for n in (4, 8, 16, 32):
        P(f"  N={n:2d}: unsigned [0, {2 ** n - 1}], sign/mag [-(2^{n - 1}-1), {2 ** (n - 1) - 1}], "
          f"two's comp [-{2 ** (n - 1)}, {2 ** (n - 1) - 1}]")

    # ---------------------------------------------------------------- slide 42-45
    P("\n--- two's complement addition / subtraction (slide 42-45) ---")
    def add8(a: int, b: int):
        s = a + b
        bits = (s & 0xFF)
        return bits, s, (1 if (a & 0xFF) + (b & 0xFF) > 0xFF else 0)
    for a, b in ((5, 9), (-5, -9), (16, -24), (15, -6), (8, -3), (3, -5), (-125, -58)):
        bits, s, carry = add8(a, b)
        P(f"  {a:>4} + {b:>4} = {s:>5} | 8-bit {to_base(bits, 2, 8)} (={from_twos(to_base(bits, 2, 8))})"
          f" carry_out={carry} {'OVERFLOW (out of [-128,127])' if not -128 <= s <= 127 else 'ok'}")

    # ---------------------------------------------------------------- slide 46-47
    P("\n--- signed multiplication / division (slide 46-47) ---")
    P("  59 x 83 =", 59 * 83, "; 4897 in binary =", to_base(4897, 2))
    P("  -4897 in 14-bit two's complement =", twos(-4897, 14), "(slide shows 10110011011111)")
    P("  14-bit range =", [-(2 ** 13), 2 ** 13 - 1], "-> 4897 fits" if 4897 <= 2 ** 13 - 1 else "!")
    P("  100 / 25 = 4 -> quotient", to_base(4, 2, 4), "and 100/-25 = -4 ->", twos(-4, 8))
    P("  01100100 =", from_base("01100100", 2), "; 00011001 =", from_base("00011001", 2))

    # ---------------------------------------------------------------- slide 51-55
    P("\n--- fixed point (slide 51-55) ---")
    P("  6.75 = 0110.1100 (U4.4) -> bits", to_base(6 * 16 + 12, 2, 8))
    P("  6.75 U3.5 ->", to_base(int(6.75 * 32), 2, 8), "=", to_base(216, 2, 8),
      "(expect 11011000,= 216/32 =", 216 / 32, ")")
    P("  6.75 U6.2 ->", to_base(int(6.75 * 4), 2, 8), "(expect 00011011, = 27/4 =", 27 / 4, ")")
    P("  -6.75 Q4.4  ->", twos(int(-6.75 * 16), 8), "(expect 10010100)")
    P("  U4.4 resolution 2^-4 =", 2 ** -4, "; max =", 15 + 15 / 16, "; min = 0")
    P("  Q4.4 range = [", -8, ",", 7 + 15 / 16, "]")
    P("  Q1.15 range = [", -1.0, ",", 1 - 2 ** -15, "] -> so slide's '(1,-1]' is loose")
    P("  saturation: 12 + 7.5 =", 12 + 7.5, "-> U4.4 raw sum", to_base((12 * 16 + int(7.5 * 16)) & 0xFF, 2, 8),
      "raw =", ((12 * 16 + int(7.5 * 16)) & 0xFF) / 16, "-> clamp 11111111 =", 255 / 16)

    # ---------------------------------------------------------------- slide 57-62
    P("\n--- floating point / IEEE 754 (slide 57-62) ---")
    P("  228 =", to_base(228, 2), "= 1.11001 x 2^7")
    P("  biased exponent = 127 + 7 =", 127 + 7, "=", to_base(134, 2, 8))
    bits228 = to_base(228, 2, 32)
    P("  228 in binary32 =", bits228, "-> 0x%08X" % struct.unpack(">I", struct.pack(">f", 228.0))[0])
    P("  -58.25 = 111010.01 = 1.1101001 x 2^5 ; biased exp = 127+5 =", 127 + 5,
      "=", to_base(132, 2, 8))
    P("  -58.25 binary32 = 0x%08X" % struct.unpack(">I", struct.pack(">f", -58.25))[0])
    P("  exponent field range [0,255] -> unbiased [-127, +128] ; bias = 127")
    P("  smallest normal 2^-126 =", 2.0 ** -126, "; largest  (2-2^-23)x2^127 =", (2 - 2 ** -23) * 2 ** 127)
    P("  spacing at 1.0 = 2^-23 =", 2.0 ** -23, "; float32 eps = 2^-23")
    for v in (0.0, float("inf"), float("-inf"), float("nan")):
        P("   %-6s -> 0x%08X" % (v, struct.unpack(">I", struct.pack(">f", v))[0]))
    P("  round-trip check 228 ->", struct.unpack(">f", struct.pack(">I", 0x43640000))[0],
      "; -58.25 ->", struct.unpack(">f", struct.pack(">I", 0xC2690000))[0])

    # ---------------------------------------------------------------- slide 64-70
    P("\n--- BCD / Gray / ASCII (slide 64-70) ---")
    for n in (170, 2469):
        enc = " ".join(to_base(int(d), 2, 4) for d in str(n))
        P(f"  BCD {n} =", enc)
    P("  BCD 8+5: binary 1000+0101 =", to_base(8 + 5, 2, 4), ">9 -> +0110 ->",
      to_base(8 + 5 + 6, 2, 4), "= 1 0011 -> BCD 0001 0011 = 13")
    P("  BCD 9+9: 1001+1001 =", to_base(9 + 9, 2, 5), "-> +0110 =", to_base(9 + 9 + 6, 2, 5),
      "-> 1 1000 -> 0001 1000 = 18")
    P("  BCD unused codes per digit: 16 - 10 =", 16 - 10, "-> correction +6")
    seq = [i ^ (i >> 1) for i in range(16)]
    P("  4-bit Gray sequence:", " ".join(to_base(g, 2, 4) for g in seq))
    ham = [bin(seq[i] ^ seq[i + 1]).count("1") for i in range(15)]
    P("  consecutive Hamming distances:", ham, "-> all 1:", all(h == 1 for h in ham))
    P("  wrap-around 1000 -> 0000 distance:", bin(seq[15] ^ seq[0]).count("1"))
    def gray_encode(v: int) -> int:
        return v ^ (v >> 1)

    def gray_decode(bits: str) -> int:
        """Gray -> binary: cascade of prefix XORs (NOT the one-line encode form)."""
        v = from_base(bits, 2)
        v ^= v >> 1
        v ^= v >> 2
        v ^= v >> 4
        v ^= v >> 8
        return v

    P("  encode: 3 -> gray", to_base(gray_encode(3), 2, 3), "(expect 010)")
    P("  decode gray 011 ->", gray_decode("011"), "=", to_base(gray_decode("011"), 2, 3),
      "(expect 2 = 010: b2=g2, b1=b2^g1, b0=b1^g0)")
    P("  decode gray 100 ->", gray_decode("100"), "=", to_base(gray_decode("100"), 2, 3),
      "(expect 7 = 111, NOT 6 -- the old one-line form was the ENCODE formula)")
    P("  round trip gray(1011)=1110 ->", to_base(gray_encode(11), 2, 4), "-> decode ->",
      gray_decode("1110"), "(expect 11 = 1011)")
    P("  slide's 011->100 transition: binary flips", bin(3 ^ 4).count("1"),
      "bits at once; Gray path 011->010->110->111->101->100 flips 1 bit per step")
    P("  ASCII: '0'=0x%02X(%d), '9'=0x%02X, 'A'=0x%02X, 'Z'=0x%02X, 'a'=0x%02X, 'z'=0x%02X, SP=0x%02X, DEL=0x%02X"
      % (ord('0'), ord('0'), ord('9'), ord('A'), ord('Z'), ord('a'), ord('z'), ord(' '), 127))
    P("  printable range 0x20-0x7E = %d chars; total ASCII codes = 128" % (0x7E - 0x20 + 1))

    # ---------------------------------------------------------------- slide 70-71
    P("\n--- parity and CRC (slide 70-71) ---")
    for g in ("10110", "11010", "110011", "110101110100", "1100010101010"):
        P(f"  odd parity group {g}: ones = {g.count('1')} -> {'OK' if g.count('1') % 2 else 'ERROR'}")
    data, gen = "11010011", "1010"
    for zeros in (3, 4):
        d = data + "0" * zeros
        q, r = crc_divide(d, gen)
        P(f"  CRC: D' = {d} (append {zeros} zeros) / G = {gen} -> remainder {r} (len {len(r)})")
    d4 = data + "0000"
    q4, r4 = crc_divide(d4, gen)
    tx = data + r4[-3:].rjust(4, "0")[-4:] if False else data + ("0" * (len(gen) - 1))
    # slide convention: 4-bit checksum appended
    tx_slide = data + r4.zfill(4)[-4:]
    P("  slide convention -> checksum", r4.zfill(4)[-4:], "; transmitted", tx_slide)
    q_rx, r_rx = crc_divide(tx_slide, gen)
    P("  receiver divides", tx_slide, "by", gen, "-> remainder", r_rx,
      "-> no error" if set(r_rx) <= {"0"} else "-> NON-ZERO (slide's own numbers are not self-consistent)")
    # one-bit error
    bad = tx_slide[:-1] + ("0" if tx_slide[-1] == "1" else "1")
    _, r_bad = crc_divide(bad, gen)
    P("  one-bit error at the end:", bad, "-> remainder", r_bad,
      "-> detected" if set(r_bad) - {"0"} else "-> MISSED")
    q3, r3 = crc_divide(data + "000", gen)
    P("  textbook convention (append degree=3 zeros) -> remainder", r3, "; transmitted", data + r3)
    _, r3_rx = crc_divide(data + r3, gen)
    P("  receiver check -> remainder", r3_rx, "-> clean" if set(r3_rx) <= {"0"} else "-> not clean")

    P("\n" + "=" * 78)
    P("report end")
    P("=" * 78)


if __name__ == "__main__":
    main()
