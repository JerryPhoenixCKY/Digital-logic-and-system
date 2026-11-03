"""Independent exhaustive checks for the Chapter 5 note revision."""
from itertools import product
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
RESULTS = []


def check(name, inputs, predicate):
    cases = list(inputs)
    for case in cases:
        assert predicate(*case), (name, case)
    RESULTS.append({'check': name, 'cases': len(cases), 'status': 'PASS'})


def bits(n):
    return product((0, 1), repeat=n)


def N(a, b):
    return 1-(a & b)


def R(a, b):
    return 1-(a | b)


def prime_cubes(n, on):
    assignments = list(bits(n))
    valid = {}
    for cube in product((None, 0, 1), repeat=n):
        covered = {sum(v << (n-1-i) for i, v in enumerate(row))
                   for row in assignments
                   if all(c is None or c == v for c, v in zip(cube, row))}
        if covered and covered <= on:
            valid[cube] = covered
    return {cube: covered for cube, covered in valid.items()
            if not any(covered < larger for larger in valid.values())}


check('p4 SOP and factored form: ON={0,4,5}', bits(3),
      lambda a,b,c: (((1-a)&(1-b)&(1-c)) | (a&(1-b)&(1-c)) | (a&(1-b)&c))
      == ((1-b)&((1-c)|a)) == int((4*a+2*b+c) in {0,4,5}))
check('p6 AOI versus DeMorgan POS', bits(4),
      lambda a,b,c,d: (1-((a&b)|(c&d)))
      == (((1-a)|(1-b)) & ((1-c)|(1-d))))
check('p5 high-active tank alarm', bits(3),
      lambda a,b,c: ((a&b)|(a&c)|(b&c)) == int(a+b+c >= 2))
check('p7 low-active tank alarm / AOI', bits(3),
      lambda a,b,c: (1-((a&b)|(a&c)|(b&c)))
      == (((1-a)&(1-b))|((1-a)&(1-c))|((1-b)&(1-c)))
      == int(3-a-b-c >= 2))
check('p8-p9 XOR and XNOR SOP/POS', bits(2),
      lambda a,b: (a ^ b) == ((a&(1-b))|((1-a)&b))
      and (1-(a^b)) == ((a&b)|((1-a)&(1-b)))
      == (((1-a)|b)&(a|(1-b))))
check('Binary XNOR cascade over three inputs is XOR', bits(3),
      lambda a,b,c: 1-((1-(a^b))^c) == (a^b^c))
check('p16 truth table: ON={3,4}', bits(3),
      lambda a,b,c: (((1-a)&b&c)|(a&(1-b)&(1-c)))
      == int(4*a+2*b+c in {3,4}))
check('p16 five-input AB+CDE implementation', bits(5),
      lambda a,b,c,d,e: ((a&b)|(c&d&e))
      == int((a == b == 1) or (c == d == e == 1)))
check('p17 exactly three of four inputs', bits(4),
      lambda a,b,c,d: (((1-a)&b&c&d)|(a&(1-b)&c&d)
                     |(a&b&(1-c)&d)|(a&b&c&(1-d)))
      == int(a+b+c+d == 3) == int(8*a+4*b+2*c+d in {7,11,13,14}))
assert len(prime_cubes(4, {7,11,13,14})) == 4
assert all(len(c) == 1 for c in prime_cubes(4, {7,11,13,14}).values())
RESULTS.append({'check': 'p17 minimum SOP has four isolated minterms', 'cases': 81, 'status': 'PASS'})


def example18(a,b,c,d):
    n = 1-((1-a)&(1-b)&(1-c))
    return (n&c)|n|d


def example19(a,b,c,d):
    return ((a&(1-b)&(1-c)) | (a&b&(1-c)&(1-d))
            |((1-a)&(1-b)&(1-c)&d) | ((1-a)&(1-b)&(1-c)&(1-d)))


check('p18 original node model versus 4-input OR', bits(4),
      lambda a,b,c,d: example18(a,b,c,d) == int(a+b+c+d > 0))
check('p19 original four products versus minimum SOP', bits(4),
      lambda a,b,c,d: example19(a,b,c,d)
      == (((1-b)&(1-c))|(a&(1-c)&(1-d)))
      == int(8*a+4*b+2*c+d in {0,1,8,9,12}))
primes = prime_cubes(4, {0,1,8,9,12})
assert primes == {(None,0,0,None): {0,1,8,9}, (1,None,0,0): {8,12}}
assert sum(0 in c for c in primes.values()) == 1
assert sum(12 in c for c in primes.values()) == 1
RESULTS.append({'check': 'p19 exactly two essential prime implicants', 'cases': 81, 'status': 'PASS'})


def priority(d3,d2,d1,d0):
    w = [d3, (1-d3)&d2, (1-d3)&(1-d2)&d1, (1-d3)&(1-d2)&(1-d1)&d0]
    requests = [i for i,b in enumerate([d0,d1,d2,d3]) if b]
    winner = max(requests) if requests else None
    ref = [int(winner == i) for i in [3,2,1,0]]
    y = 2*(d3|d2)+(d3|((1-d2)&d1))
    v = d3|d2|d1|d0
    return w == ref and sum(w) == v and y == (winner or 0)


check('p20-p22 winner mask, code, and valid for all overlapping requests', bits(4), priority)
compact = [('0000','0000'),('0001','0001'),('001X','0010'),('01XX','0100'),('1XXX','1000')]
expanded = {}
for pattern, output in compact:
    for row in bits(4):
        if all(p == 'X' or int(p) == v for p,v in zip(pattern,row)):
            assert row not in expanded
            value = sum(v << (3-i) for i,v in enumerate(row))
            expected = 1 << (value.bit_length()-1) if value else 0
            assert int(output,2) == expected
            expanded[row] = output
assert len(expanded) == 16
RESULTS.append({'check': 'p22 input X compresses exactly sixteen specified rows', 'cases': 16, 'status': 'PASS'})

check('p24-p25 eight NAND/NOR constructions', bits(2),
      lambda a,b: N(a,a) == R(a,a) == 1-a
      and N(N(a,b),N(a,b)) == a&b
      and N(N(a,a),N(b,b)) == a|b
      and N(N(N(a,a),N(b,b)),N(N(a,a),N(b,b))) == 1-(a|b)
      and R(R(a,b),R(a,b)) == a|b
      and R(R(a,a),R(b,b)) == a&b
      and R(R(R(a,a),R(b,b)),R(R(a,a),R(b,b))) == 1-(a&b))
check('p29 NAND-NAND SOP and NOR-NOR POS', bits(4),
      lambda a,b,c,d: N(N(a,b),N(c,d)) == ((a&b)|(c&d))
      and R(R(a,b),R(c,d)) == ((a|b)&(c|d)))
check('p30-p31 original NOR-NAND-NAND and bubble form', bits(4),
      lambda a,b,c,d: N(N(R(a,b),c),d)
      == (((1-a)&(1-b)&c)|(1-d))
      == int(d == 0 or (a == b == 0 and c == 1)))
check('p12 three-input even-parity SOP and XOR', bits(3),
      lambda a,b,c: (((1-a)&(1-b)&c)|((1-a)&b&(1-c))
                    |(a&(1-b)&(1-c))|(a&b&c))
      == a^b^c == (a+b+c)%2)


def parity(data, mask):
    a = [(data >> i)&1 for i in range(4)]
    p = (a[0]^a[1])^(a[2]^a[3])
    clean = (data << 1)|p
    received = clean^mask
    r = [(received >> (i+1))&1 for i in range(4)]
    pr = received&1
    e = ((r[0]^r[1])^(r[2]^r[3]))^pr
    return clean.bit_count()%2 == 0 and e == mask.bit_count()%2


check('p13-p14 every 4-bit data word with every 5-bit error mask',
      product(range(16),range(32)), parity)
assert 0b10100.bit_count()%2 == 0
assert 0b00100.bit_count()%2 == 1
assert 0b01100.bit_count()%2 == 0

# Verify that the published full truth tables match the independent references.
design = (ROOT/'Notes'/'Combinational Logic Design.md').read_text(encoding='utf-8')
table = re.findall(r'^\| (\d+) \| ([01]{4}) \| (\d+) \| ([01]) \|$', design, re.M)
assert len(table) == 16
for i, pattern, count, x in table:
    assert int(pattern,2) == int(i)
    assert pattern.count('1') == int(count)
    assert int(x) == int(int(count) == 3)
encoder = (ROOT/'Notes'/'Encoder and Priority Encoder.md').read_text(encoding='utf-8')
table = re.findall(r'^\| ([01]{4}) \| ([01]{4}) \| ([01]{2}) \| ([01]) \|$', encoder, re.M)
assert len(table) == 16
for pattern, mask, code, v in table:
    value = int(pattern,2)
    winner = value.bit_length()-1 if value else None
    assert int(mask,2) == (1 << winner if value else 0)
    assert int(code,2) == (winner or 0)
    assert int(v) == int(value > 0)
RESULTS.append({'check':'Published exactly-three and priority truth tables', 'cases':32, 'status':'PASS'})

target = Path(__file__).with_suffix('.json')
target.write_text(json.dumps({'checks':RESULTS, 'all_passed':True}, ensure_ascii=False, indent=2), encoding='utf-8')
for result in RESULTS:
    print(f"PASS: {result['check']} ({result['cases']} cases)")
print('ALL PASSED', len(RESULTS), 'checks')
