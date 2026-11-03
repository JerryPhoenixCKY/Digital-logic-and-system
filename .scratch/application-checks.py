"""Independent finite-input and numeric checks for application/review examples."""
from itertools import product
from fractions import Fraction
from pathlib import Path
import re

checks = 0

def check(condition, context):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(context)

labels = 'abcdefg'
digit_segments = ['abcdef', 'bc', 'abdeg', 'abcdg', 'bcfg',
                  'acdfg', 'acdefg', 'abc', 'abcdefg', 'abcdfg']
printed_codes = ['1111110', '0110000', '1101101', '1111001', '0110011',
                 '1011011', '1011111', '1110000', '1111111', '1111011']
for digit, segments in enumerate(digit_segments):
    code = ''.join(str(int(label in segments)) for label in labels)
    check(code == printed_codes[digit], f'display code for {digit}')
    inverted = ''.join(str(1-int(bit)) for bit in code)
    check(all(int(p) + int(q) == 1 for p,q in zip(code,inverted)),
          f'active-low polarity for {digit}')
check(''.join(str(1-int(c)) for c in printed_codes[1]) == '1001111', 'CA digit 1')
check(''.join(str(1-int(c)) for c in printed_codes[4]) == '1001100', 'CA digit 4')
check(''.join(str(1-int(c)) for c in printed_codes[2]) == '0010010', 'CA digit 2')

for code in range(16):
    q3,q2,q1,q0 = [(code >> b) & 1 for b in (3,2,1,0)]
    invalid = bool(q3 and (q2 or q1))
    check(invalid == (code >= 10), f'BCD validity detector at {code}')
    a_logic = bool(q3 or q1 or (q2 and q0) or ((not q2) and (not q0)))
    if code < 10:
        check(a_logic == ('a' in digit_segments[code]), f'a segment at digit {code}')
    else:
        check(not ((not invalid) and a_logic), f'invalid code blanking at {code}')

def convert_two_adders(tens, units):
    r = tens + (units >> 1)
    s = tens + (r >> 2)
    result = (s << 3) | ((r & 3) << 1) | (units & 1)
    return r,s,result

for tens,units in product(range(10),repeat=2):
    r,s,result = convert_two_adders(tens,units)
    check(r < 16 and s < 16, f'adder carry bounds {tens}{units}')
    check(result == 10*tens+units, f'two-adder conversion {tens}{units}')
    check(result < 128, f'7-bit output bound {tens}{units}')
check(convert_two_adders(3,7) == (6,4,37), 'BCD 37 intermediate outputs')
check(convert_two_adders(9,9) == (13,12,99), 'BCD 99 intermediate outputs')
check((37 == 0b0100101) and (99 == 0b1100011), 'binary printed results')
check(int('00110111',2) == 55, 'BCD concatenation counterexample')

def suppress_leading(digits, keep_units=True):
    result = []
    propagating = True
    for pos,digit in enumerate(digits):
        can_blank = propagating and digit == 0
        if keep_units and pos == len(digits)-1:
            can_blank = False
        result.append(None if can_blank else digit)
        propagating = can_blank
    return result

check(suppress_leading([0,0,3,0]) == [None,None,3,0], '0030 zero suppression')
check(suppress_leading([0,0,0,0]) == [None,None,None,0], 'retain visible zero')
check(suppress_leading([1,0,0,2]) == [1,0,0,2], 'preserve internal zeros')
check(Fraction(980,4000) == Fraction(245,1000), 'scan duty with blanking')
check(Fraction(8)*Fraction(980,4000) == Fraction(196,100), 'average current mA')
check((3.3-2.0-0.1)/.005 > 239.999, 'LED resistance lower numeric bound')
check((3.3-2.0-0.1)/.005 < 240.001, 'LED resistance upper numeric bound')

detect_n0,detect_n1 = set(),set()
for a,b,c in product((0,1),repeat=3):
    good = bool((a and b) or c)
    fault0 = bool(c)
    fault1 = True
    vector = ''.join(map(str,(a,b,c)))
    if good != fault0:
        detect_n0.add(vector)
    if good != fault1:
        detect_n1.add(vector)
    check((good != fault0) == bool(a and b and not c), f'n/0 detecting algebra {vector}')
    check((good != fault1) == bool((not c) and ((not a) or (not b))),
          f'n/1 detecting algebra {vector}')
    b_stuck0 = bool((a and 0) or c)
    check(b_stuck0 == fault0, f'fault indistinguishability at {vector}')
check(detect_n0 == {'110'}, 'complete n/0 detection set')
check(detect_n1 == {'000','010','100'}, 'complete n/1 detection set')

for s,d0,d1 in product((0,1),repeat=3):
    good = d1 if s else d0
    fault = d0
    check((good != fault) == bool(s and (d0 != d1)), f'MUX select fault {s}{d0}{d1}')
check(digit_segments[8].replace('g','') == digit_segments[0], '8 missing g resembles 0')
failures = [n for n in range(100) if (n & ~(1 << 5)) != n]
check(failures[0] == 32, 'first output-bit-5 stuck-at-0 detection')
check((32 & ~(1 << 5)) == 0, 'faulty output at 32')

check((-5)*(-3) == int('00001111',2), 'signed multiply')
signed4 = lambda x: x-16 if x & 8 else x
check(signed4(0b1011) == -5 and signed4(0b1101) == -3, 'signed operands')
check(signed4(0b1111) == -1, 'incorrect narrowed signed result')
binary_fraction = 2+Fraction(int('101101',2),2**6)
octal_fraction = 2+Fraction(5,8)+Fraction(5,64)
hex_fraction = 2+Fraction(11,16)+Fraction(4,256)
check(binary_fraction == octal_fraction == hex_fraction == Fraction(173,64),
      'binary fractional octal/hex grouping')

on_set = set()
off_set = set()
for a,b,c in product((0,1),repeat=3):
    index = (a<<2)|(b<<1)|c
    truth = bool((a and b) or c)
    (on_set if truth else off_set).add(index)
    canonical_pos = (a or b or c) and (a or not b or c) and (not a or b or c)
    minimum_pos = (a or c) and (b or c)
    n1 = not (a and b)
    n2 = not (c and c)
    nand_implementation = not (n1 and n2)
    mux = [c,c,c,1][(a<<1)|b]
    check(truth == bool(canonical_pos), f'canonical POS row {index}')
    check(truth == bool(minimum_pos), f'minimum POS row {index}')
    check(truth == bool(nand_implementation), f'NAND network row {index}')
    check(truth == bool(mux), f'MUX cofactors row {index}')
check(on_set == {1,3,5,6,7}, 'canonical minterms')
check(off_set == {0,2,4}, 'canonical maxterms')

word_set = set()
for a,b,c,d in product((0,1),repeat=4):
    word = ''.join(map(str,(a,b,c,d)))
    oracle = '110' in word
    sop = (a and b and not c) or (b and c and not d)
    pos = b and (a or c) and ((not c) or (not d))
    check(oracle == bool(sop), f'word 110 SOP {word}')
    check(oracle == bool(pos), f'word 110 POS {word}')
    if oracle:
        word_set.add(int(word,2))
check(word_set == {6,12,13,14}, 'word 110 complete detection set')

check(2+7+1 == 10, 'setup period ns')
check(Fraction(1,10)*1000 == 100, 'maximum frequency MHz')
check(Fraction(5,10)+Fraction(2,10) < 1, 'hold violation')
state = 0
trace = []
for bit in [1,0,1,1]:
    state = ((state<<1)|bit)&7
    trace.append(format(state,'03b'))
check(trace == ['001','010','101','011'], 'simultaneous shift state trace')

def next_mod3(q):
    q1,q0 = (q>>1)&1,q&1
    d1 = (not q1) and q0
    d0 = (not q1) and (not q0)
    return (int(d1)<<1)|int(d0)

check([next_mod3(q) for q in range(4)] == [1,2,0,0], 'mod3 all encoded states')
q=0
cycle=[]
for _ in range(6):
    cycle.append(q)
    q=next_mod3(q)
check(cycle == [0,1,2,0,1,2], 'mod3 cycle period')
check(0b1000-1 == 0b0111, 'down counter source-pitfall check')
check([format(i.bit_count(),'02b') for i in range(8)] ==
      ['00','01','01','10','01','10','10','11'], 'ROM complete word contents')
check((1<<3)*2 == 16, 'ROM capacity')

def remainder(value, generator):
    while value.bit_length() >= generator.bit_length():
        value ^= generator << (value.bit_length()-generator.bit_length())
    return value

data,generator = 0b10110010,0b1010
degree = generator.bit_length()-1
rem = remainder(data<<degree,generator)
transmitted = (data<<degree)|rem
check(degree == 3 and rem == 0b110, 'CRC generator degree/remainder')
check(format(transmitted,'011b') == '10110010110', 'correct systematic CRC code')
check(remainder(transmitted,generator) == 0, 'correct code is divisible')
printed_source_code = int('101100100110',2)
check(printed_source_code.bit_length() != 8+degree, 'printed code has wrong length')
check((printed_source_code >> degree) != data, 'printed code changes original data prefix')

draft = Path(__file__).with_name('expansion-drafts')/'04-applications.md'
text = draft.read_text(encoding='utf-8')
new_titles = {chunk.strip().splitlines()[0].split('|')[0]
              for chunk in text.split('@@NOTE')[1:]}
existing_titles = {p.stem for p in Path('Notes').glob('*.md')}
for target in set(re.findall(r'\[\[([^\]|#]+)',text)):
    check(target in existing_titles|new_titles, f'canonical link exists: {target}')
print(f'APPLICATION/REVIEW CHECKS PASSED: {checks} assertions')
print('Coverage: all 100 BCD pairs; segment/invalid rows; complete fault vectors;')
print('canonical/K-map equivalence; word matching; state cycles; timing; ROM; CRC; links.')
