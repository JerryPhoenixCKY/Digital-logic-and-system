from pathlib import Path
import re, json, hashlib
base=Path('.scratch/full-content-20261008'); original=Path('.scratch/consolidation-20261008/original-Notes')
report=json.loads((base/'coverage-ch6plus.json').read_text('utf-8'))
selected=sorted(set(r['target'] for r in report['sections']))
def norm(s):
 s=re.sub(r'^> ?', '', s, flags=re.M)
 s=re.sub(r'!?\[\[([^\]]+)\]\]',lambda m:m[1].split('|')[-1].split('#')[0],s)
 s=re.sub(r'^#{1,6} ', '', s, flags=re.M)
 return re.sub(r'\s+','',s.replace('**',''))
def code(s):
 return re.findall(r'```(?:vhdl|mermaid)[^\n]*\n(.*?)```',re.sub(r'^> ?', '',s,flags=re.M),re.S)
issues=[]; totals={}; asset_count=0; block_count=0
for t in selected:
 before=Path('Notes',t+'.md').read_text('utf-8'); after=(base/'draft/Notes'/(t+'.md')).read_text('utf-8')
 if re.findall(r'^## (.*)',before,re.M)!=re.findall(r'^## (.*)',after,re.M):issues.append((t,'primary headings changed'))
 before_codes=code(before); after_codes=code(after)
 for c in before_codes:
  if c not in after_codes:issues.append((t,'lost code block',c[:40]))
 block_count+=len(before_codes)
 before_assets=re.findall(r'!\[\[([^\]]+)\]\]',before)
 for a in before_assets:
  if '![[%s]]'%a not in after:issues.append((t,'lost embed',a))
 asset_count+=len(before_assets)
 # Exact content-line evidence prevents a concise rephrasing from deleting
 # existing derivations, traces, code, diagrams, or textbook qualifications.
 body=before.split('---',2)[2]
 for l in body.splitlines():
  if not l.strip() or re.match(r'^(?:> \[!|#{1,6} |>|---|索引：)',l.strip()) and not l.startswith('> '):continue
  if l.startswith('> [!') or re.match(r'^> \*\*[^*]+\*\*$',l):continue
  n=norm(l)
  if n and n not in norm(after):issues.append((t,'current content line absent',l[:120]))
 totals[t]={'before_characters':len(before),'after_characters':len(after),'before_lines':len(before.splitlines()),'after_lines':len(after.splitlines())}
 # Fences are checked after unquoting because many examples stay foldable.
 if len(re.findall(r'^```',re.sub(r'^> ?','',after,flags=re.M),re.M))%2:issues.append((t,'unbalanced fences'))
 # Every old concept link is rewritten to canonical target+existing H2.
 canonical=set(json.loads(Path('.scratch/consolidation-20261008/mapping.json').read_text('utf-8'))['old_to_new'].values())|{'ECE2050 Knowledge Tree','Glossary'}
 for _,spec in re.findall(r'(!?)\[\[([^\]]+)\]\]',after):
  dest=spec.split('|')[0]; name,sep,h=dest.partition('#')
  if name not in canonical and not Path('assets',name).exists() and not any(x.endswith(name) for x in before_assets):issues.append((t,'noncanonical target',name))
  if sep and name in canonical and Path('Notes',name+'.md').exists():
   targettxt=(base/'draft/Notes'/(name+'.md')).read_text('utf-8') if (base/'draft/Notes'/(name+'.md')).exists() else Path('Notes',name+'.md').read_text('utf-8')
   if h not in re.findall(r'^#{1,6} (.*)',targettxt,re.M):issues.append((t,'missing anchor',name,h))
result={'targets':len(selected),'retained_existing_code_blocks':block_count,'retained_existing_embeds':asset_count,'issues':issues,'sizes':totals}
(base/'qa-ch6plus.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='sizes'},ensure_ascii=False))
