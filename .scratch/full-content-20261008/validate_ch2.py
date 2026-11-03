from pathlib import Path
import re, json, struct, itertools, yaml

ROOT=Path.cwd()
BASE=ROOT/'.scratch/full-content-20261008'
names=[g['target'] for g in json.loads((ROOT/'.scratch/consolidation-20261008/mapping.json').read_text(encoding='utf-8-sig'))['groups'] if g['chapter']=='Ch2']
report={'notes':{},'math_checks':{},'errors':[]}
note_paths={p.stem:p for p in (ROOT/'Notes').glob('*.md')}
note_paths.update({p.stem:p for p in (BASE/'draft/Notes').glob('*.md')})
assets={p.name for p in ROOT.rglob('*') if p.is_file() and '.scratch' not in p.parts}
for name in names:
    before=(ROOT/'Notes'/(name+'.md')).read_text(encoding='utf-8-sig')
    after=(BASE/'draft/Notes'/(name+'.md')).read_text(encoding='utf-8-sig')
    before_heads=re.findall(r'^## (.+)',before,re.M)
    after_heads=re.findall(r'^## (.+)',after,re.M)
    assert before_heads==after_heads,(name,'main section structure changed')
    metadata=yaml.safe_load(after.split('---',2)[1])
    assert metadata.get('aliases') and name in metadata['aliases']
    blocks=lambda t:re.findall(r'(?:^|\n)(?:> )?```[^\n]*\n.*?\n(?:> )?```',t,re.S)
    assert blocks(before)==blocks(after),(name,'existing code/mermaid block changed')
    assert after.count('$$')%2==0,(name,'unbalanced display math')
    link_count=0
    for embed,body in re.findall(r'(!?)\[\[([^\]]+)\]\]',after):
        destination=body.split('|',1)[0]
        if embed:
            if destination not in assets:report['errors'].append([name,'missing asset',destination])
            continue
        note,_,anchor=destination.partition('#')
        note=note.removesuffix('.md')
        if note not in note_paths:report['errors'].append([name,'missing note',note]);continue
        if anchor:
            target=note_paths[note].read_text(encoding='utf-8-sig')
            hs=re.findall(r'^#{1,6} (.+)',target,re.M)
            if anchor not in hs:report['errors'].append([name,'missing heading',destination])
        link_count+=1
    report['notes'][name]={'preserved_main_headings':len(before_heads),'preserved_code_blocks':len(blocks(before)),'wikilinks':link_count,'before_bytes':len(before.encode('utf-8')),'after_bytes':len(after.encode('utf-8'))}

def signed(u,n):return u if u<1<<(n-1) else u-(1<<n)
checked=0
for n in range(1,7):
    mod=1<<n
    for ua,ub in itertools.product(range(mod),repeat=2):
        a,b=signed(ua,n),signed(ub,n)
        # A is sign-extended before each shift; multiplier MSB is negative.
        accum=sum(((ub>>i)&1)*(a<<i) for i in range(n-1))-((ub>>(n-1))&1)*(a<<(n-1))
        assert signed(accum% (1<<(2*n)),2*n)==a*b
        add=signed((ua+ub)%mod,n); sub=signed((ua-ub)%mod,n)
        sa,sb,ss=(ua>>(n-1)),(ub>>(n-1)),((ua+ub)%mod>>(n-1))
        sf=((ua-ub)%mod)>>(n-1)
        assert ((sa==sb) and (ss!=sa)) == (not -(1<<(n-1))<=a+b<(1<<(n-1)))
        assert ((sa!=sb) and (sf!=sa)) == (not -(1<<(n-1))<=a-b<(1<<(n-1)))
        checked+=1
report['math_checks']['signed_multiply_and_add_sub_overflow_pairs']=checked

for a,b,c in itertools.product(range(10),range(10),range(2)):
    t=a+b+c; low=t&15; c4=t>>4
    k=bool(c4 or ((low>>3)&1 and ((low>>2)&1 or (low>>1)&1)))
    digit=(low+(6 if k else 0))&15
    assert digit==t%10 and int(k)==t//10
report['math_checks']['BCD_digit_additions']=200

def gray_decode(g,n):
    b=g
    shift=1
    while shift<n:
        b^=b>>shift;shift*=2
    return b
for n in range(1,9):
    seq=[k^(k>>1) for k in range(1<<n)]
    assert len(set(seq))==1<<n
    assert all(gray_decode(g,n)==k for k,g in enumerate(seq))
    assert all((seq[i]^seq[(i+1)%len(seq)]).bit_count()==1 for i in range(len(seq)))
report['math_checks']['Gray_roundtrip_and_cyclic_adjacency']='all codes for widths 1–8'

def rem(word,g):
    while word.bit_length()>=g.bit_length():word^=g<<(word.bit_length()-g.bit_length())
    return word
examples=[('11010011','1010',3,'010'),('11010011','1010',4,'0100'),('1101','1011',3,'001'),('10110010','1010',3,'110')]
for d,g,k,r in examples:
    assert rem(int(d,2)<<k,int(g,2))==int(r,2)
    assert rem((int(d,2)<<k)|int(r,2),int(g,2))==0
counts={}
for e in range(1,1<<12):
    weight=e.bit_count()
    burst=e.bit_length()-((e&-e).bit_length()-1)
    for key,test in [('single',weight==1),('double',weight==2),('odd',weight%2==1),('even',weight%2==0),('short_burst',burst<=3),('long_burst',burst>=4)]:
        if test:
            counts.setdefault(key,[0,0]);counts[key][0]+=1;counts[key][1]+=bool(rem(e,0b1010))
assert counts=={'single':[12,12],'double':[66,41],'odd':[2048,2048],'even':[2047,1536],'short_burst':[43,34],'long_burst':[4052,3550]},counts
report['math_checks']['CRC_examples_and_12_bit_exhaustion']=counts
for x,h in [(228,'43640000'),(-58.25,'c2690000'),(10.5,'41280000'),(0.1,'3dcccccd')]:
    assert struct.pack('>f',x).hex()==h
report['math_checks']['binary32_encodings']=4
report['math_checks']['ASCII_partition']={'printable':0x7e-0x20+1,'controls':0x20+1}
assert report['math_checks']['ASCII_partition']=={'printable':95,'controls':33}
(BASE/'validation-ch2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
assert not report['errors'], report['errors']
