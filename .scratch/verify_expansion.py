"""Independent arithmetic/state checks for the 2026-09-30 note expansion.

Reference expectations use integer arithmetic or the stated word/string
specification, rather than a second copy of the gate equations.
"""
from itertools import product
from pathlib import Path
import json

checks = 0

def check(actual, expected, label):
    global checks
    assert actual == expected, (label, actual, expected)
    checks += 1

def bits(n, width):
    return tuple((n >> i) & 1 for i in range(width - 1, -1, -1))

def nand(a, b):
    return 1 - (a & b)

def nor(a, b):
    return 1 - (a | b)

def full_adder(a, b, c):
    return a ^ b ^ c, (a & b) | (a & c) | (b & c)

for a, b, c in product(range(2), repeat=3):
    s, carry = full_adder(a, b, c)
    check(s + 2 * carry, a + b + c, 'full-adder conservation')
    d = a ^ b ^ c
    borrow = ((1-a) & b) | ((1-a) & c) | (b & c)
    check(d - 2 * borrow, a - b - c, 'full-subtractor conservation')

for a, b, c, d in product(range(2), repeat=4):
    check(nand(nand(a,b), nand(c,d)), (a & b) | (c & d), 'NAND SOP')
    check(nor(nor(a,b), nor(c,d)), (a | b) & (c | d), 'NOR POS')
    detect = (a & b & (1-c)) | (b & c & (1-d))
    factored = b & (a | c) & ((1-c) | (1-d))
    check(detect, int('110' in ''.join(map(str,(a,b,c,d)))), 'parallel 110 detector')
    check(factored, detect, '110 POS equivalence')

for a, b, c in product(range(2), repeat=3):
    majority = (a & b) | (a & c) | (b & c)
    check(majority, int(a+b+c >= 2), 'majority specification')
    check((0,c,c,1)[2*a+b], majority, 'MUX majority cofactors')
    check((c,1-c,1-c,c)[2*a+b], (a+b+c) % 2, 'MUX parity cofactors')

for a, b, cin in product(range(16), range(16), range(2)):
    p = [((a>>i)&1) ^ ((b>>i)&1) for i in range(4)]
    g = [((a>>i)&1) & ((b>>i)&1) for i in range(4)]
    carry = [cin]
    sums = []
    for i in range(4):
        sums.append(p[i] ^ carry[i])
        carry.append(g[i] | (p[i] & carry[i]))
    c4 = g[3] | (p[3]&g[2]) | (p[3]&p[2]&g[1]) | (p[3]&p[2]&p[1]&g[0]) | (p[3]&p[2]&p[1]&p[0]&cin)
    check(sum(s << i for i,s in enumerate(sums)) + 16*carry[4], a+b+cin, 'four-bit RCA')
    check(c4, int(a+b+cin >= 16), 'CLA expanded carry')

# Adder-subtractor result and carry/borrow semantics.
for a, b in product(range(16), repeat=2):
    total = a + ((~b)&15) + 1
    check(total&15, (a-b)%16, 'adder-subtractor difference')
    check(int(total >= 16), int(a >= b), 'carry means no unsigned borrow')

# Multi-bit comparator: lexicographic gate expression versus integer order.
for a, b in product(range(16), repeat=2):
    equal_above = 1
    gt = 0
    for ai,bi in zip(bits(a,4),bits(b,4)):
        gt |= equal_above & ai & (1-bi)
        equal_above &= int(ai == bi)
    check(gt, int(a>b), 'unsigned comparator')
    check(equal_above, int(a==b), 'word equality')

# Three-bit multiplier: add partial products using bit columns and HA/FA cells.
for a,b in product(range(8), repeat=2):
    pp = [[((a>>i)&1)&((b>>j)&1) for j in range(3)] for i in range(3)]
    # The published network names each addition by its bit-column weight.
    p0 = pp[0][0]
    p1,c1 = full_adder(pp[1][0],pp[0][1],0)
    s2,c2 = full_adder(pp[2][0],pp[1][1],pp[0][2])
    p2,c3 = full_adder(s2,c1,0)
    s3,c4 = full_adder(pp[2][1],pp[1][2],c2)
    p3,c5 = full_adder(s3,c3,0)
    p4,p5 = full_adder(pp[2][2],c4,c5)
    actual = sum(x<<i for i,x in enumerate((p0,p1,p2,p3,p4,p5)))
    check(actual,a*b,'3x3 unsigned multiplier')

# Custom counter: equations against an independently stored required sequence.
sequence = [0,5,1,2,7,6,3,4]
expected_next = dict(zip(sequence,sequence[1:]+sequence[:1]))
for q in range(8):
    q2,q1,q0 = bits(q,3)
    d2 = ((1-q2)&(1-q0)) | (q1&q0)
    d1 = ((1-q2)&(1-q1)&q0) | (q1&(1-q0)) | (q2&q1)
    d0 = (q2&(1-q1)&q0) | ((1-q2)&(1-q0)) | (q1&(1-q0))
    check(4*d2+2*d1+d0,expected_next[q],'custom eight-state counter')

for q in range(4):
    q1,q0=bits(q,2)
    nextq=2*((1-q1)&q0)+((1-q1)&(1-q0))
    check(nextq,{0:1,1:2,2:0,3:0}[q],'mod3 including recovery')

for q in range(16):
    qvec=[(q>>i)&1 for i in range(4)]
    for direction in (1,-1):
        nxt=[]
        for i in range(4):
            toggle=all(qvec[j] == (1 if direction==1 else 0) for j in range(i))
            nxt.append(qvec[i] ^ int(toggle))
        check(sum(x<<i for i,x in enumerate(nxt)),(q+direction)%16,'T-FF up/down equations')

# Serial 110 Mealy detector: state equations versus the longest-suffix behavior.
for word_length in range(1,9):
    for stream in product(range(2),repeat=word_length):
        q=0
        seen=''
        for x in stream:
            q1,q0=bits(q,2)
            z=q1&(1-q0)&(1-x)
            seen+=str(x)
            check(z,int(seen.endswith('110')),'110 detector output')
            q=2*(x&(q1^q0))+(x&(1-q1)&(1-q0))
            suffix=2 if seen.endswith('11') else 1 if seen.endswith('1') else 0
            check(q,suffix,'110 detector longest suffix state')
for x in (0,1):
    check(2*(x*(1^1))+x*(1-1)*(1-1),0,'FSM unused 11 recovers')

# Traffic controller equations versus the requirement table, including both sensors.
for q,ta,tb in product(range(4),range(2),range(2)):
    q1,q0=bits(q,2)
    nxt=2*(q1^q0)+(((1-q1)&(1-q0)&(1-ta)) | (q1&(1-q0)&(1-tb)))
    target={0:0 if ta else 1,1:2,2:2 if tb else 3,3:0}[q]
    check(nxt,target,'traffic transition')
    la=2*q1+((1-q1)&q0)
    lb=2*(1-q1)+(q1&q0)
    check((la,lb),[(0,2),(1,2),(2,0),(2,1)][q],'traffic Moore outputs')

# Bidirectional structural equations against a word-string shift specification.
for q,r,sr,sl in product(range(16),range(2),range(2),range(2)):
    q3,q2,q1,q0=bits(q,4)
    d=(r&sr)|((1-r)&q2),(r&q3)|((1-r)&q1),(r&q2)|((1-r)&q0),(r&q1)|((1-r)&sl)
    expected = str(sr)+format(q,'04b')[:3] if r else format(q,'04b')[1:]+str(sl)
    check(''.join(map(str,d)),expected,'structural bidirectional register')
q=0
trace=[]
for sr in [1,0,1,1]:
    q=(sr<<3)|(q>>1)
    trace.append(format(q,'04b'))
check(trace,['1000','0100','1010','1101'],'project directed trace')

def cycle(step,start):
    result=[]
    q=start
    while q not in result:
        result.append(q)
        q=step(q)
    return result,q

johnson=lambda q: ((1-(q&1))<<3)|(q>>1)
check(cycle(johnson,0),([0,8,12,14,15,7,3,1],0),'Johnson intended cycle')
check(cycle(johnson,5),([5,2,9,4,10,13,6,11],5),'Johnson alternate cycle')
ring=lambda q: ((q&1)<<3)|(q>>1)
check(len(cycle(ring,1)[0]),4,'one-hot ring modulus')
check(cycle(ring,0),([0],0),'all-zero ring trap')

def polynomial_remainder(value,g):
    while value and value.bit_length()>=g.bit_length():
        value^=g << (value.bit_length()-g.bit_length())
    return value

for data,g,r,frame in [('10110010','1010','110','10110010110'),('1101','101','10','110110')]:
    degree=len(g)-1
    rem=polynomial_remainder(int(data,2)<<degree,int(g,2))
    check(format(rem,f'0{degree}b'),r,'CRC remainder')
    check(data+format(rem,f'0{degree}b'),frame,'degree-r frame length')
    check(polynomial_remainder(int(frame,2),int(g,2)),0,'CRC transmitted frame residue')
    # Multiples of the generator produce undetectable changes.
    check(polynomial_remainder(int(frame,2)^int(g,2),int(g,2)),0,'CRC nonzero undetectable error')

check(12-(-10),22,'2025 subtraction correction')
check(format((12-(-10))&255,'08b'),'00010110','subtraction retained bits')
check(1-(int('00010100',2).bit_count()%2),1,'odd parity correction')
check((1+int('011',2)/8)*2**(130-127),11.0,'binary32 normalized example')
check(8192*16//8,16384,'8Kx16 bytes')
check((16384//8192)*(16//8),4,'mixed memory expansion chip count')
check(65536-40000,25536,'counter preset')
check(hex(25536),'0x63c0','counter preset hex')
check(50+3*35+60,215,'setup maximum path ps')
check(30+25-70,-15,'hold slack ps')
check(30+25+25-70,10,'hold repair slack ps')
check(round(1e3/215,3),4.651,'setup-only frequency GHz')
check(round(30e-15*0.1/1e-15,9),3.0,'illustrative DRAM retention seconds')

# Follow-up refinements: storage excitation, keyboard address and CRC hardware.
for old,e,d in product(range(2),repeat=3):
    j=e&d
    k=e&(1-d)
    actual=(j&(1-old))|((1-k)&old)
    check(actual,d if e else old,'JK key-register load/hold')
for row,col in product(range(8),repeat=2):
    check(int(format(row,'03b')+format(col,'03b'),2),8*row+col,'keyboard six-bit address')
check(65536-20000,45536,'keyboard divider preset')
check(format(45536,'016b'),'1011000111100000','keyboard preset binary')
check(100_000_000//20000,5000,'scan event repetition rate')
check(5000/8,625.0,'eight-row frame rate')
for width in range(1,10):
    for value in range(1<<width):
        r0=r1=r2=0
        for bit in format(value,f'0{width}b'):
            r2,r1,r0=r1,r0^r2,int(bit)
        check(4*r2+2*r1+r0,polynomial_remainder(value,0b1010),'true three-stage G divider')

for a,b,c,d in product(range(2),repeat=4):
    check(((1-a)&(1-b))|(1-c),1-(((a|b)&c)),'nested DeMorgan practice')
    check((a&b)|(a&(1-b))|((1-a)&c),a|c,'Ch4 absorption practice')
    check((1-b)&(1-d),int((8*a+4*b+2*c+d) in {0,2,8,10}),'K-map corner practice')
check(-(1+512/2048)*2**(9-7),-5.0,'custom16 normal value')
check(-(1+512/2048)*2**(9-15),-0.01953125,'wrong-bias counterexample')

import struct
f32=lambda x:struct.unpack('>f',struct.pack('>f',x))[0]
check(f32(f32(0.1)+f32(0.2))==f32(0.3),True,'binary32 step-rounded equality boundary')
check((0.1+0.2)==0.3,False,'binary64 decimal-fraction example')

report={'status':'PASS','independent_assertions':checks,'scope':'gate/arithmetic, multiplier, counter/FSM state equations, bidirectional shift, initialization, CRC conventions, timing and capacity examples','hdl_simulation':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
