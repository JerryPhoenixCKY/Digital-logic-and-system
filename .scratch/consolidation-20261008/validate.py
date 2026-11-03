from __future__ import annotations

import importlib.util
import json
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
NOTES = ROOT / 'Notes' if '--live' in sys.argv else WORK / 'draft' / 'Notes'
errors = []
checks = 0

def check(ok, message):
    global checks
    checks += 1
    if not ok:
        errors.append(message)

groups = json.loads((WORK / 'mapping.json').read_text('utf-8'))['groups']
mapping = json.loads((WORK / 'link-mapping.json').read_text('utf-8'))
texts = {p.stem: p.read_text('utf-8') for p in NOTES.glob('*.md')}
expected = {g['target'] for g in groups} | {'ECE2050 Knowledge Tree', 'Glossary'}
check(set(texts) == expected, 'Topic file set does not match the 31-topic mapping')

name_index = defaultdict(set)
headers = {}
for name, t in texts.items():
    try:
        fm = yaml.safe_load(t.split('---', 2)[1])
    except Exception as e:
        errors.append(name + ': malformed YAML: ' + str(e)); continue
    check(all(k in fm for k in ['tags', 'date', 'aliases']), name + ': metadata fields missing')
    for alias in [name] + fm['aliases']:
        name_index[alias.casefold()].add(name)
    headers[name] = set(re.findall(r'^#{1,6} ([^\n]+)', t, re.M))
    check(t.rstrip().endswith('索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]'), name + ': hub footer missing')
    check(t.count('\ufffd') == 0, name + ': encoding replacement character')
    # Quote markers surrounding expandable blocks do not belong to their code.
    flat = re.sub(r'^> ?', '', t, flags=re.M)
    check(len(re.findall(r'^```', flat, re.M)) % 2 == 0, name + ': unclosed code fence')
    check(len(re.findall(r'\$\$', flat)) % 2 == 0, name + ': unclosed display math')
    for local in re.findall(r'(?<!\!)\[[^\]]+\]\(([^\s)]+)\)', t):
        if '://' in local or local.startswith('#'):
            continue
        dest = (ROOT / 'Notes' / unquote(local.split('#')[0])).resolve()
        check(dest.exists(), name + ': missing Markdown attachment ' + local)
for alias, dests in name_index.items():
    check(len(dests) == 1, 'Ambiguous alias ' + alias + ': ' + repr(dests))
for alias, dest in mapping.items():
    check(name_index[alias.casefold()] == {dest['target']}, 'Lost legacy name: ' + alias)
    check(dest['heading'] in headers[dest['target']], 'Missing mapped heading: ' + alias)

used_assets = set(); link_count = 0; anchor_count = 0
for name, t in texts.items():
    for embed, full in re.findall(r'(!?)\[\[([^\]]+)\]\]', t):
        link_count += 1
        spec = full.split('|', 1)[0]
        target, _, heading = spec.partition('#')
        if embed:
            used_assets.add(target)
            check((ROOT / 'Figures' / target).exists(), name + ': missing embedded ' + target)
            continue
        dests = name_index.get(target.casefold(), set()) if target else {name}
        check(len(dests) == 1, name + ': unresolved/ambiguous ' + full)
        if heading and len(dests) == 1:
            anchor_count += 1
            check(heading in headers[next(iter(dests))], name + ': invalid heading ' + full)

with zipfile.ZipFile(WORK / 'original-notes.zip') as z:
    original = {Path(p).stem: z.read(p).decode('utf-8-sig') for p in z.namelist() if p.endswith('.md')}
    all_old_assets = set(re.findall(r'!\[\[([^\]|]+)', '\n'.join(original.values())))
    check(used_assets == all_old_assets, 'Embedded asset coverage changed: ' + repr(all_old_assets - used_assets))
    # Full executable examples must survive the prose rewrite, including port order.
    for source in ['VHDL Language and Modeling', 'Testbench and Functional Verification', 'Structural Shift Register Project']:
        codeblocks = re.findall(r'```vhdl\n(.*?)\n```', original[source], re.S)
        target = mapping[source]['target']
        flat = re.sub(r'^> ?', '', texts[target], flags=re.M)
        newblocks = re.findall(r'```vhdl\n(.*?)\n```', flat, re.S)
        for code in codeblocks:
            check(code in newblocks, source + ': VHDL code example changed or lost')

for g in groups:
    check('✅' in next((line for line in texts['ECE2050 Knowledge Tree'].splitlines() if '[[' + g['target'] + ']]' in line), ''), 'Tree misses ' + g['target'])

# Independently evaluate the newly stated small examples against definitions.
import itertools
math_cases = 0
for a, b, c, d in itertools.product([0, 1], repeat=4):
    i = 8*a + 4*b + 2*c + d
    original_p19 = (a and not b and not c) or (a and b and not c and not d) or (not a and not b and not c and d) or (not a and not b and not c and not d)
    reduced = (not b and not c) or (a and not c and not d)
    check(bool(original_p19) == bool(reduced) == (i in {0,1,8,9,12}), 'P19 / K-map mismatch ' + str(i))
    exactly3 = ((not a and b and c and d) or (a and not b and c and d) or (a and b and not c and d) or (a and b and c and not d))
    check(bool(exactly3) == (a+b+c+d == 3), 'Exactly-three mismatch ' + str(i))
    w = [bool(d), bool(not d and c), bool(not d and not c and b), bool(not d and not c and not b and a)]
    y = 2*bool(d or c) + bool(d or (not c and b))
    expect_w = [False]*4
    if i:
        high = max(j for j, v in enumerate([a,b,c,d]) if v)
        expect_w[3-high] = True
        check(y == high, 'Priority code mismatch ' + str(i))
    check(w == expect_w, 'Priority mask mismatch ' + str(i))
    math_cases += 1
for a, b, cin in itertools.product([0,1], repeat=3):
    check(a+b+cin == 2*bool(a*b or a*cin or b*cin) + (a^b^cin), 'Full adder failed')
    diff = a^b^cin; borrow = bool((not a and b) or ((not (a^b)) and cin))
    check(a-b-cin == diff-2*borrow, 'Full subtractor failed')
    check(bool(a*b or a*cin or b*cin) == (a+b+cin>=2), 'Majority mismatch')
    check(bool((not a and not b) or (not a and not cin) or (not b and not cin)) == (a+b+cin<=1), 'Low-active majority mismatch')
    math_cases += 1

def remainder(x, g):
    while x and x.bit_length() >= g.bit_length():
        x ^= g << (x.bit_length()-g.bit_length())
    return x
check(remainder(0b1101 << 3, 0b1011) == 1, 'New CRC example remainder incorrect')
check(remainder(0b1101001, 0b1011) == 0, 'New CRC codeword not divisible')
for q1,q0 in itertools.product([0,1],repeat=2):
    state=2*q1+q0; nxt=2*bool(not q1 and q0)+bool(not q1 and not q0)
    check(nxt == {0:1,1:2,2:0,3:0}[state], 'Modulo-3 equation incorrect')
    math_cases += 1
import struct
check(struct.pack('>f', 10.5).hex().upper() == '41280000', 'New IEEE-754 example incorrect')
check((0b1011 ^ (0b1011 >> 1)) == 0b1110, 'New Gray example incorrect')
math_cases += 4

report = {'mode': 'live' if '--live' in sys.argv else 'staged', 'topic_notes': 31, 'hubs': 2,
          'legacy_names_preserved': len(mapping), 'wikilinks_checked': link_count,
          'heading_links_checked': anchor_count, 'embedded_assets': len(used_assets),
          'checks': checks, 'mathematical_cases': math_cases, 'errors': errors}
(WORK / ('validation-live.json' if '--live' in sys.argv else 'validation-staged.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2), 'utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors else 0)
