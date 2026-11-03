"""Independent numerical and exhaustive checks for the midterm learning materials."""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import re
import struct
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
counts: dict[str, int] = {}


def check(group, condition):
    if not condition:
        raise AssertionError(group)
    counts[group] = counts.get(group, 0) + 1


def signed(v, n):
    return v - (1 << n) if v & (1 << (n - 1)) else v


def remainder_int(v, g):
    while v.bit_length() >= g.bit_length():
        v ^= g << (v.bit_length() - g.bit_length())
    return v


def remainder_bits(data, generator):
    work = [int(c) for c in data]
    g = [int(c) for c in generator]
    for i in range(len(work) - len(g) + 1):
        if work[i]:
            for j, bit in enumerate(g):
                work[i + j] ^= bit
    return ''.join(str(x) for x in work[-(len(g) - 1):])


def minimum_cover(n, on, dc=frozenset()):
    """Exact set-cover minimum (term count, literal count) from all implicants."""
    on = set(on)
    allowed = on | set(dc)
    indices = {row: i for i, row in enumerate(sorted(on))}
    terms = []
    for pattern in product((-1, 0, 1), repeat=n):
        rows = {v for v in range(1 << n)
                if all(bit == -1 or bit == (v >> (n - 1 - i) & 1)
                       for i, bit in enumerate(pattern))}
        if rows <= allowed and rows & on:
            mask = sum(1 << indices[row] for row in rows & on)
            terms.append((mask, sum(bit != -1 for bit in pattern)))
    full = (1 << len(on)) - 1
    dp = {0: (0, 0)}
    for mask in range(full + 1):
        if mask not in dp:
            continue
        for term_mask, literals in terms:
            new_mask = mask | term_mask
            cost = (dp[mask][0] + 1, dp[mask][1] + literals)
            if cost < dp.get(new_mask, (10**9, 10**9)):
                dp[new_mask] = cost
    return dp[full]


# Numeric examples checked against exact arithmetic, not copied bit procedures.
check('numeric examples', Q(45) + Q(5, 8) == Q(int('101101101', 2), 8))
check('numeric examples', Q(45) + Q(5, 8) == Q(int('2DA', 16), 16))
check('numeric examples', round(3 + 2 / 3, 2) == 3.67)
check('numeric examples', (1 << 9) < 1001 <= (1 << 10))
check('numeric examples', signed(0xD6, 8) == -42 and -(0xD6 & 0x7F) == -86)
check('numeric examples', signed(0xFD6, 12) == -42 and 0xD6 - 63 == 151)
check('numeric examples', (84 - 109) & 255 == 0xE7)
check('numeric examples', signed((100 + 60) & 255, 8) == -96)
check('numeric examples', 12 - signed(0xF6, 8) == 0x16)
check('numeric examples', ((-13 * 7) & 255) == 0xA5)
check('numeric examples', signed(0xAA, 8) * Q(1, 16) == -Q(43, 8))
check('numeric examples', ((12 * 16 + Q(15, 2) * 16) % 256) / 16 == Q(7, 2))
for value, bits in [(-45.375, 0xC2358000), (-58.25, 0xC2690000),
                    (228.0, 0x43640000), (-10.0, 0xC1200000)]:
    packed = struct.unpack('>I', struct.pack('>f', value))[0]
    s, e, f = packed >> 31, packed >> 23 & 255, packed & ((1 << 23) - 1)
    decoded = (-1)**s * (1 + Q(f, 1 << 23)) * Q(2)**(e - 127)
    check('binary32 examples', packed == bits and decoded == Q(value))

for a, b in product(range(256), repeat=2):
    sa, sb = signed(a, 8), signed(b, 8)
    add, sub = (a + b) & 255, (a - b) & 255
    x, y, zadd, zsub = a >> 7, b >> 7, add >> 7, sub >> 7
    vadd = (not (x ^ y)) and (x ^ zadd)
    vsub = (x ^ y) and (x ^ zsub)
    carry_add = (((a & 127) + (b & 127)) >> 7) ^ ((a + b) >> 8)
    bcomp = b ^ 255
    carry_sub = (((a & 127) + (bcomp & 127) + 1) >> 7) ^ ((a + bcomp + 1) >> 8)
    check('8-bit overflow equations', bool(vadd) == (not -128 <= sa + sb <= 127)
          and bool(vsub) == (not -128 <= sa - sb <= 127)
          and vadd == carry_add and vsub == carry_sub)

for a, b, cin in product(range(10), range(10), range(2)):
    t = a + b + cin
    nibble, carry = t & 15, t >> 4
    k = bool(carry or ((nibble >> 3 & 1) and ((nibble >> 2 & 1) or (nibble >> 1 & 1))))
    digit = (nibble + (6 if k else 0)) & 15
    check('BCD correction', 10 * k + digit == t and digit < 10)

for b in range(256):
    g = b ^ (b >> 1)
    recovered = 0
    for i in range(8):
        recovered ^= g >> i
    next_gray = ((b + 1) % 256) ^ (((b + 1) % 256) >> 1)
    check('Gray and parity', recovered == b and (g ^ next_gray).bit_count() == 1)
    p_even = b.bit_count() % 2
    check('Gray and parity', (b.bit_count() + p_even) % 2 == 0
          and (b.bit_count() + (1 - p_even)) % 2 == 1)
check('Gray and parity', (0b101101 ^ (0b101101 >> 1)) == 0b111011)
check('Gray and parity', (0b100110 ^ (0b100110 >> 1)) == 0b110101)

crc_examples = [('1101', '101', '10', '110110'),
                ('10110110', '1101', '010', '10110110010'),
                ('11010011', '1010', '010', '11010011010'),
                ('10110010', '1010', '110', '10110010110')]
for d, g, expected_r, expected_code in crc_examples:
    r = len(g) - 1
    rb = remainder_bits(d + '0' * r, g)
    ri = remainder_int(int(d, 2) << r, int(g, 2))
    check('CRC independent divisions', rb == expected_r and int(rb, 2) == ri
          and d + rb == expected_code and remainder_bits(expected_code, g) == '0' * r
          and remainder_int(int(expected_code, 2), int(g, 2)) == 0)
check('CRC printed steps', int('10110110000', 2) ^ int('11010000000', 2) == int('01100110000', 2))
check('CRC printed steps', int('01100110000', 2) ^ int('01101000000', 2) == int('00001110000', 2))
check('CRC printed steps', int('00001110000', 2) ^ int('00001101000', 2) == int('00000011000', 2))
check('CRC printed steps', int('00000011000', 2) ^ int('00000011010', 2) == 2)

for a, b, c in product(range(2), repeat=3):
    check('Boolean identities', (a or (not a and b)) == (a or b)
          and ((a and b) or (not a and b) or (a and not b)) == (a or b)
          and ((a or b) and (a or c)) == (a or (b and c)))
    before = (not a and not b) or (b and c)
    check('Consensus', before == (before or (not a and c)))
    check('HA/FA weights', a + b == (a ^ b) + 2 * (a & b)
          and a + b + c == (a ^ b ^ c) + 2 * ((a & b) | (a & c) | (b & c)))
    index = (a << 2) | (b << 1) | c
    check('canonical and MUX', bool((a and b) or (a and c)) == (index in {5, 6, 7}))
    selected = [c, 1 - c, 0, 1][(a << 1) | b]
    check('canonical and MUX', bool(selected) == (index in {1, 2, 6, 7}))

for v in range(16):
    a, b, c, d = (v >> i & 1 for i in (3, 2, 1, 0))
    check('K-map XNOR', bool((not b and not d) or (b and d))
          == bool((b or not d) and (not b or d)) == (v in {0, 2, 5, 7, 8, 10, 13, 15}))
    prime_dc = (not b and c) or (b and d)
    prime_strict = not a and prime_dc
    if v < 10:
        check('BCD prime functions', bool(prime_dc) == (v in {2, 3, 5, 7})
              and prime_dc == ((b or c) and (not b or d)))
    check('BCD prime functions', bool(prime_strict) == (v in {2, 3, 5, 7}))
    exact = ((not a and b and c and d) or (a and not b and c and d)
             or (a and b and not c and d) or (a and b and c and not d))
    at_least = (a and b and c) or (a and b and d) or (a and c and d) or (b and c and d)
    parallel = (a and b and not c) or (b and c and not d)
    check('specification truth tables', bool(exact) == (v.bit_count() == 3)
          and bool(at_least) == (v.bit_count() >= 3)
          and bool(parallel) == ('110' in f'{v:04b}')
          and bool(parallel) == bool(b and (not c or not d) and (a or c)))
    nand = lambda x, y: not (x and y)
    nor = lambda x, y: not (x or y)
    check('universal gates', nand(nand(a, b), nand(c, d)) == ((a and b) or (c and d))
          and nor(nor(a, b), nor(c, d)) == ((a or b) and (c or d)))
    e1, e0, valid = a or b, a or (not b and c), bool(v)
    check('priority encoder', not valid or (int(e1) * 2 + int(e0)) == v.bit_length() - 1)

check('minimum cover', minimum_cover(4, {0, 2, 5, 7, 8, 10, 13, 15}) == (2, 4))
check('minimum cover', minimum_cover(4, {2, 3, 5, 7}, set(range(10, 16))) == (2, 4))
check('minimum cover', minimum_cover(4, {0, 1, 4, 6, 8, 9}, set(range(10, 16))) == (2, 4))
check('minimum cover', minimum_cover(4, {2, 3, 5, 7}) == (2, 6))

for a, b, cin in product(range(16), range(16), range(2)):
    aa, bb = [(a >> i) & 1 for i in range(4)], [(b >> i) & 1 for i in range(4)]
    for xor_propagate in (False, True):
        g = [x & y for x, y in zip(aa, bb)]
        p = [x ^ y if xor_propagate else x | y for x, y in zip(aa, bb)]
        carries = [cin]
        for i in range(4):
            expanded = all(p[:i+1]) and cin
            for j in range(i+1):
                expanded |= g[j] and all(p[j+1:i+1])
            carries.append(int(expanded))
        out = sum((aa[i] ^ bb[i] ^ carries[i]) << i for i in range(4)) + (carries[4] << 4)
        check('4-bit CLA both conventions', out == a + b + cin)
    eq_bits = [int(x == y) for x, y in zip(aa, bb)]
    gt = any(aa[i] and not bb[i] and all(eq_bits[i+1:]) for i in range(4))
    lt = any(not aa[i] and bb[i] and all(eq_bits[i+1:]) for i in range(4))
    eq = all(eq_bits)
    check('comparator equations', gt == (a > b) and lt == (a < b) and eq == (a == b))

for a, b in product(range(4), repeat=2):
    a0, a1, b0, b1 = a & 1, a >> 1, b & 1, b >> 1
    p00, p10, p01, p11 = a0 & b0, a1 & b0, a0 & b1, a1 & b1
    k = p10 & p01
    z = p00 + ((p10 ^ p01) << 1) + ((p11 ^ k) << 2) + ((p11 & k) << 3)
    check('2-bit multiplier', z == a * b)

for a in range(8):
    low_outputs = [int(a != j) for j in range(8)]
    f = not all(low_outputs[j] for j in (1, 3, 6))
    check('decoder polarity', f == (a in {1, 3, 6}))
for v in range(10):
    a, b, c, d = (v >> i & 1 for i in (3, 2, 1, 0))
    check('display segment a', bool(a or c or (b and d) or (not b and not d))
          == (v in {0, 2, 3, 5, 6, 7, 8, 9}))
check('voltage and delay examples', Q(3) - Q(21, 10) == Q(9, 10)
      and Q(8, 10) - Q(1, 4) == Q(55, 100)
      and Q(3) - Q(55, 100) == Q(245, 100)
      and Q(1, 4) + Q(4, 10) == Q(65, 100)
      and max(2 + 2 + 3, 2) == 7 and min(Q(1, 2)*2+Q(8, 10), Q(1, 2)) == Q(1, 2))
check('ASCII examples', ord('5') == 0x35 == 0x30 + 5 and ord('a') - ord('A') == 0x20)

# Deliverable-specific links, source page numbers, aliases and equation delimiters.
from pypdf import PdfReader
import logging
logging.getLogger('pypdf').setLevel(logging.ERROR)
pages = {}
names = ['Midterm Review Guide', 'Midterm Formula Sheet', 'Midterm Practice and Answers']
notes = {p.stem for p in (ROOT / 'Notes').glob('*.md')}
for name in names:
    path = ROOT / 'Notes' / (name + '.md')
    body = path.read_text(encoding='utf-8')
    check('document integrity', body.count('$$') % 2 == 0 and '\ufffd' not in body)
    check('document integrity', body.rstrip().endswith('索引：[[ECE2050.1]] · [[Glossary]]'))
    check('document integrity', len(re.findall(r'^# ', body, re.M)) == 1)
    for target in re.findall(r'(?<!!)\[\[([^\]|#]+)', body):
        check('internal links', target in notes)
    for url, page in re.findall(r'\]\((\.\./.*?\.(?:pdf|md))(?:#page=(\d+))?\)', body):
        source = (path.parent / unquote(url)).resolve()
        check('source links', source.exists())
        if page:
            if source not in pages:
                pages[source] = len(PdfReader(source).pages)
            check('source page links', 1 <= int(page) <= pages[source])

practice = (ROOT / 'Notes' / (names[2] + '.md')).read_text(encoding='utf-8')
numbers = [int(x) for x in re.findall(r'^### (\d+) ·', practice, re.M)]
check('question sequence', numbers == list(range(1, 34)))
report = {'status': 'PASS', 'total_checks': sum(counts.values()), 'groups': counts,
          'source_pdf_page_counts': {p.name: n for p, n in pages.items()},
          'crc_examples': crc_examples}
(Path(__file__).parent / 'verification-report.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
