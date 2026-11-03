from pathlib import Path
import re,json
root=Path('.'); work=root/'.scratch/full-content-20261008'; source=root/'.scratch/consolidation-20261008/original-Notes'
report=json.loads((work/'coverage-ch6plus.json').read_text('utf-8'))
def norm(s):
 s=re.sub(r'^> ?', '', s, flags=re.M)
 s=re.sub(r'!?\[\[([^\]]+)\]\]',lambda m:m[1].split('|')[-1].split('#')[0],s)
 s=re.sub(r'^#{1,6} ', '', s, flags=re.M)
 return re.sub(r'\s+','',s.replace('**',''))
issues=[]; all_lines=0; relationship_rows=0
for sname in sorted(set(r['source'] for r in report['sections'])):
 rows=[r for r in report['sections'] if r['source']==sname and ' > ' not in r['source_section']]; target=rows[0]['target']; text=(work/'draft/Notes'/(target+'.md')).read_text('utf-8')
 raw=(source/(sname+'.md')).read_text('utf-8')
 parts=re.split(r'^## ([^\n]+)\n',raw,flags=re.M)
 for i in range(1,len(parts),2):
  h,b=parts[i:i+2]
  b=re.sub(r'^索引：.*$', '',b,flags=re.M); b=re.sub(r'\n---\s*$','',b)
  for line in b.splitlines():
   if not line.strip() or line.startswith('### '):continue
   n=norm(line)
   if not n:continue
   all_lines+=1
   if n not in norm(text):
    # Pure link lists were deliberately converted into semantic prose. All
    # original destinations/display concepts must still be present.
    rest=re.sub(r'!?\[\[([^\]]+)\]\]','',line)
    if re.fullmatch(r'[\s,.，。]*',rest):
     relationship_rows+=1
     for link in re.findall(r'\[\[([^\]]+)\]\]',line):
      display=link.split('|')[-1].split('#')[0]
      if display not in text:issues.append((sname,h,'lost relationship',display))
    else:issues.append((sname,h,line))
print(json.dumps({'original_content_lines_checked':all_lines,'semantic_relationship_rows':relationship_rows,'issues':issues},ensure_ascii=False))
qa=json.loads((work/'qa-ch6plus.json').read_text('utf-8')); qa['original_content_lines_checked']=all_lines;qa['semantic_relationship_rows']=relationship_rows;qa['original_content_issues']=issues
(work/'qa-ch6plus.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),'utf-8')
