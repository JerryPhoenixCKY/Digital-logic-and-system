from pathlib import Path
from itertools import product, combinations
import re,json

ROOT=Path.cwd(); BASE=ROOT/'.scratch/full-content-20261008'; OUT=BASE/'draft/Notes'
mapping=json.loads((ROOT/'.scratch/consolidation-20261008/mapping.json').read_text(encoding='utf-8-sig'))
targets=[g for g in mapping['groups'] if g['chapter'] in ['Ch3','Ch4']]
checks=[]
def record(name,passed,detail=None):
    assert passed,(name,detail)
    checks.append({'check':name,'passed':True,'detail':detail})

for g in targets:
    n=g['target']; now=(OUT/(n+'.md')).read_text(encoding='utf-8'); before=(ROOT/'Notes'/(n+'.md')).read_text(encoding='utf-8-sig')
    record(n+' H2 preserved', re.findall(r'^## .+$',now,re.M)==re.findall(r'^## .+$',before,re.M))
    record(n+' current image embeds preserved',re.findall(r'!\[\[[^\]]+\]\]',now)==re.findall(r'!\[\[[^\]]+\]\]',before))
    record(n+' current detailed callouts preserved',re.findall(r'^> \[!example\]- .+$',now,re.M)==re.findall(r'^> \[!example\]- .+$',before,re.M))
    record(n+' canonical duplicate references removed','Boolean Forms and Algebraic Simplification 1' not in now)
    record(n+' control characters absent',not any(ord(c)<32 and c not in '\n\t' for c in now))
    record(n+' alias list retained', bool(re.search(r'^aliases:\n(?:  - .+\n)+',now,re.M)))
    headings=set(re.findall(r'^#{1,6} (.+)$',now,re.M))
    selflinks=[h for dst,h in re.findall(r'\[\[([^#|\]]+)#([^|\]]+)',now) if dst==n]
    record(n+' self heading links resolve',all(h in headings for h in selflinks),[h for h in selflinks if h not in headings])

identity_checks=0
for a,b,c in product([False,True],repeat=3):
    identities=[
        (not(a and b),not a or not b),(not(a or b),not a and not b),
        (a or False,a),(a and True,a),(a or True,True),(a and False,False),
        (a or a,a),(a and a,a),(a or not a,True),(a and not a,False),(not(not a),a),
        (a or(a and b),a),(a and(a or b),a),
        (a or(not a and b),a or b),(a and(not a or b),a and b),
        ((a or b)and(a or c),a or(b and c)),((a and b)or(a and c),a and(b or c)),
        (a^b,(a and not b)or(not a and b)),(not(a^b),(a and b)or(not a and not b)),
        (a^b,(a or b)and not(a and b)),
        (not(a or(not b and c)),not a and(b or not c)),
        (not((a or b)and c),(not a and not b)or not c),
        (not((a and not b)or c),(not a or b)and not c),
        ((a and not b and c)or(a and b and c)or(not a and b and c),(a and c)or(b and c)),
        ((not a and b)or(a and b),b),
        ((a and b)or(a and(b or c))or(b and(b or c)),(a and c)or b),
        ((a and b)or(not a and c)or(b and c),(a and b)or(not a and c)),
    ]
    record('Boolean identities row '+str((a,b,c)),all(x==y for x,y in identities));identity_checks+=len(identities)

for n in range(1,7):
    for bits in product([0,1],repeat=n):
        xor=sum(bits)%2
        xnor_chain=bits[0]
        for bit in bits[1:]: xnor_chain=int(not(xnor_chain^bit))
        record('XNOR cascade n='+str(n)+' '+''.join(map(str,bits)),xnor_chain==(xor^((n-1)%2)))

for n in [2,3,4]:
    rows=list(product([0,1],repeat=n))
    for i,row in enumerate(rows):
        mi=[all(bit==p for bit,p in zip(x,row)) for x in rows]
        Mi=[any(bit!=p for bit,p in zip(x,row)) for x in rows]
        record('minterm/maxterm n='+str(n)+' i='+str(i),sum(mi)==1 and sum(Mi)==len(rows)-1 and all(x!=y for x,y in zip(mi,Mi)))

def cost_min(n,on,dc=()):
    on=set(on); allowed=on|set(dc); rows=list(product([0,1],repeat=n)); cubes=[]
    if not on:return (0,0)
    for pat in product([-1,0,1],repeat=n):
        covered={i for i,bits in enumerate(rows) if all(p==-1 or b==p for b,p in zip(bits,pat))}
        if covered&on and covered<=allowed:cubes.append((covered,sum(p!=-1 for p in pat)))
    primes=[cube for cube in cubes if not any(cube[0]<other[0] for other in cubes)]
    for k in range(1,len(primes)+1):
        valid=[sum(c[1] for c in cs) for cs in combinations(primes,k) if on<=set().union(*(c[0] for c in cs))]
        if valid:return k,min(valid)

cases=[
    ('p45 SOP',3,{3,4,6,7},set(),lambda a,b,c:(b and c)or(a and not c),(2,4)),
    ('p50',3,{2,3,7},set(),lambda a,b,c:(not a and b)or(b and c),(2,4)),
    ('p51',3,{0,1,2,4,5,7},set(),lambda a,b,c:not b or(not a and not c)or(a and c),(3,5)),
    ('p52',4,{0,2,3,5,6,7,8,9,10},set(),lambda a,b,c,d:(not a and c)or(not a and b and d)or(a and not b and not c)or(not b and not d),(4,10)),
    ('p56 SOP',4,{0,5,6,7,8,10,11,13,14,15},set(),lambda a,b,c,d:(not b and not c and not d)or(b and d)or(b and c)or(a and c),(4,9)),
    ('p59 X fixed 0',4,{0,2,3,6,7,8,9},set(),lambda a,b,c,d:(not a and c)or(a and not b and not c)or(not a and not b and not d),(3,8)),
    ('p59 X free',4,{0,2,3,6,7,8,9},{5,10,11,12,13,14,15},lambda a,b,c,d:a or c or(not b and not d),(3,4)),
    ('seven-segment a',4,{0,2,3,5,6,7,8,9},{10,11,12,13,14,15},lambda a,b,c,d:a or c or(b and d)or(not b and not d),(4,6)),
    ('boundary wrap',4,{0,1,8,9,12},set(),lambda a,b,c,d:(not b and not c)or(a and not c and not d),(2,5)),
]
for name,n,on,dc,fn,cost in cases:
    actual={i for i,bits in enumerate(product([0,1],repeat=n)) if fn(*bits)}
    record(name+' assigned rows',on<=actual and actual<=on|dc,{'on':sorted(on),'actual':sorted(actual),'dc':sorted(dc)})
    result=cost_min(n,on,dc);record(name+' exact cover minimum', result==cost,{'terms':result[0],'literals':result[1]})

pos=lambda a,b,c,d:(a or b or not c)and(b or c or not d)and(not b or c or d)
on={0,5,6,7,8,10,11,13,14,15};actual={i for i,bits in enumerate(product([0,1],repeat=4)) if pos(*bits)}
record('p56 POS assigned rows',actual==on)
record('p56 POS exact cover minimum',cost_min(4,set(range(16))-on)==(3,9))
record('exactly three ones singleton minimum',cost_min(4,{7,11,13,14})==(4,16))
record('p45 POS exact cover minimum',cost_min(3,{0,1,2,5})==(2,4))

algebra=(OUT/'Boolean Algebra and Circuit Models.md').read_text(encoding='utf-8')
block=algebra.split('> **Example 2 — 讲义 p.29')[1].split('> **Example 3 — 把 NAND-only')[0]
table=[list(map(int,re.findall(r'(?<=\|)\s*([01])\s*(?=✓?\s*\|)',line))) for line in block.splitlines() if re.match(r'^> \| [01] \| [01] \| [01] \|',line)]
expected=[]
for a,b,c in product([0,1],repeat=3):
    t=int(not b and c);before=int(a or t);y=int(not before);expected.append([a,b,c,t,before,y,y,y])
record('retained DeMorgan worked-example table cells',table==expected,table)

coverage=json.loads((BASE/'coverage-ch34.json').read_text(encoding='utf-8'))
record('coverage every original subsection and orientation', len(coverage['records'])==sum(1+len(re.findall(r'^#{2,6} ',(ROOT/'.scratch/consolidation-20261008/original-Notes'/(s+'.md')).read_text(encoding='utf-8-sig'),re.M)) for g in targets for s in g['sources']))
record('coverage destinations exist',all(entry['target_heading'] in set(re.findall(r'^#{1,6} (.+)$',(OUT/entry['target']).read_text(encoding='utf-8'),re.M)) for entry in coverage['records']))
coverage['validation']={'passed':True,'checks':len(checks),'boolean_identity_row_comparisons':identity_checks,'exact_minimum_cases':12,'details_file':'verification-ch34.json'}
(BASE/'coverage-ch34.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'verification-ch34.json').write_text(json.dumps({'passed':True,'checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':True,'checks':len(checks),'identity_row_comparisons':identity_checks,'minimum_cases':12},ensure_ascii=False))
