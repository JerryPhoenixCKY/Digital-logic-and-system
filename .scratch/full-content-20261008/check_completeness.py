from pathlib import Path
import json
import re
import zipfile
import sys
from collections import Counter

ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
OLD=ROOT/'.scratch/consolidation-20261008'
MODE='live' if '--live' in sys.argv else 'staged'
NOTES=ROOT/'Notes' if MODE=='live' else WORK/'draft/Notes'
issues=[]
with zipfile.ZipFile(WORK/'before-enrichment.zip') as z:
    prior={Path(p).stem:z.read(p).decode('utf-8-sig').replace('\r\n','\n') for p in z.namelist() if p.endswith('.md')}
mapping=json.loads((OLD/'mapping.json').read_text('utf-8'))['groups']
code_count=0
asset_count=0
for g in mapping:
    name=g['target'];old=prior[name];new=(NOTES/(name+'.md')).read_text('utf-8')
    for h in re.findall(r'^## ([^\n]+)',old,re.M):
        if h not in re.findall(r'^## ([^\n]+)',new,re.M):issues.append(name+': lost original H2 '+h)
    old_assets=Counter(re.findall(r'!\[\[([^\]|]+)',old));new_assets=Counter(re.findall(r'!\[\[([^\]|]+)',new))
    for a in old_assets:
        if new_assets[a]==0:issues.append(name+': lost asset '+a)
        asset_count+=1
    def blocks(t):
        t=re.sub(r'^> ?', '',t,flags=re.M)
        return re.findall(r'^```([^\n]*)\n(.*?)\n```',t,re.M|re.S)
    newblocks=blocks(new)
    for lang,body in blocks(old):
        code_count+=1
        if (lang,body) not in newblocks:
            # One conceptual flow may change only to correct a documented source error.
            if lang=='vhdl':issues.append(name+': changed/lost executable VHDL block')
            else:issues.append(name+': review changed '+lang+' block')
    if re.search(r'^> \[!example\]-[^\n]*\n(?=\n(?:##|###))',new,re.M):
        issues.append(name+': empty example block')
    for line in new.splitlines():
        if line.lstrip('> ').startswith('|') and re.search(r'\[\[[^\]]*[^\\]\|[^\]]*\]\]',line):
            issues.append(name+': table link delimiter not escaped')
coverage=json.loads((WORK/'coverage-all.json').read_text('utf-8'))
if coverage['missing_sections']:issues.append('Missing original content coverage')
report={'mode':MODE,'original_topics':88,'canonical_topics':31,'original_H2_sections':coverage['original_H2_sections'],
        'source_H2_sections_covered':coverage['H2_sections_covered'],
        'existing_code_blocks_checked':code_count,'existing_embed_locations_checked':asset_count,
        'topic_characters_before':sum(len(prior[g['target']]) for g in mapping),
        'topic_characters_after':sum(len((NOTES/(g['target']+'.md')).read_text('utf-8')) for g in mapping),
        'issues':issues}
(WORK/('completeness-'+MODE+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(1 if issues else 0)
