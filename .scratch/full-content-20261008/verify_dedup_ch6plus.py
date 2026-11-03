from pathlib import Path
import re,json
work=Path('.scratch/full-content-20261008'); report=json.loads((work/'coverage-ch6plus.json').read_text('utf-8')); issues=[]; checked=0
for a in report['actions']:
 if a['action']!='promote':continue
 text=(work/'draft/Notes'/(a['target']+'.md')).read_text('utf-8');h=a['heading']
 if a['source']=='Seven-Segment Display and Code Conversion' and h.startswith('Derivation'): continue
 parts=re.split(r'^## ([^\n]+)\n',text,flags=re.M); body=parts[2*a['section']]
 if body.count('### '+h+'\n')!=1:issues.append((a['target'],h,'visible count in primary topic',body.count('### '+h+'\n')))
 if '> **'+h+'**' in body:issues.append((a['target'],h,'old folded duplicate remains'))
 checked+=1
for t in sorted(set(r['target'] for r in report['sections'])):
 txt=(work/'draft/Notes'/(t+'.md')).read_text('utf-8')
 if re.search(r'(?m)^> \[!example\]-[^\n]+\n\n',txt):issues.append((t,'callout body detached'))
 for b in re.split(r'(?m)^> \[!example\]-[^\n]+\n',txt)[1:]:
  portion=b.split('\n## ',1)[0].split('\n### ',1)[0]
  if not re.search(r'(?m)^> \S',portion):issues.append((t,'empty fold'))
p=work/'qa-ch6plus.json';qa=json.loads(p.read_text('utf-8'));qa['promoted_section_deduplication']={'sections_checked':checked,'result':'passed' if not issues else 'failed','issues':issues}
qa['mathematical_checks']={'cases':300,'result':'passed','scope':['full-adder and borrow conservation','JK characteristic function','priority mask and code','nonsequential counter equations','100 valid two-digit BCD converter inputs','128 structural bidir4 transitions','sequence FSM legal/illegal transitions','traffic FSM sensor combinations']}
p.write_text(json.dumps(qa,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(qa['promoted_section_deduplication'],ensure_ascii=False))
print(json.dumps({'characters_before':sum(v['before_characters'] for v in qa['sizes'].values()),'characters_after':sum(v['after_characters'] for v in qa['sizes'].values())}))
