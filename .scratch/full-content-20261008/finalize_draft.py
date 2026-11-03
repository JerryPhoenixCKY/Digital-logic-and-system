from pathlib import Path
from collections import Counter
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
OLD = ROOT / '.scratch/consolidation-20261008'
NOTES = WORK / 'draft/Notes'
groups = json.loads((OLD / 'mapping.json').read_text('utf-8'))['groups']
expected = {g['target'] for g in groups} | {'ECE2050 Knowledge Tree', 'Glossary'}
assert {p.stem for p in NOTES.glob('*.md')} == expected

records = []
for c in json.loads((WORK / 'coverage-root.json').read_text('utf-8')):
    records.append({'source': c['source'], 'source_heading': c['source_heading'], 'level':2,
                    'target': c['target'], 'target_section':c['target_heading'], 'status':c['status'], 'detail':c['detail']})
for s in json.loads((WORK / 'coverage-ch2.json').read_text('utf-8'))['sources']:
    for c in s['sections']:
        records.append({'source':s['original_note'], 'source_heading':c['original_heading'], 'level':c['original_level'],
                        'target':s['target_note'], 'target_section':c['target_section'].split('#',1)[-1], 'status':c['status'], 'detail':c['coverage']})
for c in json.loads((WORK / 'coverage-ch34.json').read_text('utf-8'))['records']:
    records.append({'source':Path(c['source']).stem,'source_heading':c['source_heading'],'level':c['source_level'],
                    'target':Path(c['target']).stem,'target_section':c['target_section'],'status':c['status'],'detail':c['note']})
for c in json.loads((WORK / 'coverage-ch6plus.json').read_text('utf-8'))['sections']:
    records.append({'source':c['source'],'source_heading':c['source_section'],'level':c.get('source_level',2),
                    'target':c['target'],'target_section':c['target_section'],'status':c['status'],'detail':c['coverage_note']})
inventory = json.loads((WORK / 'section-inventory.json').read_text('utf-8'))
index = {(c['source'],c['source_heading']):c for c in records}
missing = [c for c in inventory if (c['source'],c['heading']) not in index]
assert not missing, missing
source_coverage = [index[(c['source'],c['heading'])] for c in inventory]
for c in source_coverage:
    target_text=(NOTES/(c['target']+'.md')).read_text('utf-8')
    target_sections = c['target_section'] if isinstance(c['target_section'], list) else [c['target_section']]
    assert all(s in re.findall(r'^## ([^\n]+)',target_text,re.M) for s in target_sections),c

# Table cell separators in display-text wikilinks must be escaped for Obsidian.
# Within inline math use an explicit TeX vertical-bar command instead.
changed_rows = 0
for p in NOTES.glob('*.md'):
    rows=[]
    for line in p.read_text('utf-8').splitlines():
        before=line
        if line.lstrip('> ').startswith('|'):
            line=re.sub(r'\[\[([^\]]+)\]\]',lambda m:'[['+re.sub(r'(?<!\\)\|',r'\\|',m[1])+']]',line)
            line=re.sub(r'(?<!\$)\$([^$\n]+)\$(?!\$)',lambda m:'$'+re.sub(r'(?<!\\)\|',lambda _:r'\vert ',m[1])+'$',line)
            line=re.sub(r'`([^`]+)`',lambda m:'`'+re.sub(r'(?<!\\)\|',r'\\|',m[1])+'`',line)
        line=line.replace('[[Boolean Forms and Algebraic Simplification 1', '[[Boolean Forms and Algebraic Simplification')
        if line!=before:changed_rows+=1
        rows.append(line)
    p.write_text('\n'.join(rows)+'\n','utf-8')

coverage_report={'original_topics':88,'original_H2_sections':len(inventory), 'H2_sections_covered':len(source_coverage),
    'missing_sections':missing,'status_counts':dict(Counter(c['status'] for c in source_coverage)),
    'extra_subsection_records':len(records)-len(inventory),'table_rows_repaired':changed_rows,'records':source_coverage}
(WORK/'coverage-all.json').write_text(json.dumps(coverage_report,ensure_ascii=False,indent=2),'utf-8')

text=(OLD/'validate.py').read_text('utf-8')
text=text.replace('WORK = Path(__file__).resolve().parent\n','WORK = Path(__file__).resolve().parent\nOLD = ROOT / ".scratch/consolidation-20261008"\n')
for name in ['mapping.json','link-mapping.json','original-notes.zip']:
    text=text.replace("WORK / '"+name+"'", "OLD / '"+name+"'")
text=text.replace("spec = full.split('|', 1)[0]", "spec = full.replace(r'\\|', '|').split('|', 1)[0]")
text=text.replace("check(t.count('\\ufffd') == 0, name + ': encoding replacement character')", "check(t.count('\\ufffd') == 0, name + ': encoding replacement character')\n    check(not re.search(r'[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]', t), name + ': invalid control character')")
(WORK/'validate.py').write_text(text,'utf-8')
print(json.dumps({k:v for k,v in coverage_report.items() if k!='records'},ensure_ascii=False,indent=2))
