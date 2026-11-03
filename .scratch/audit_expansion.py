from pathlib import Path
import json, re
from collections import defaultdict

root = Path(__file__).resolve().parents[1]
paths = list((root/'Notes').glob('*.md'))
name_map = defaultdict(set)
for p in paths:
    name_map[p.stem].add(p.stem)
    t=p.read_text(encoding='utf-8')
    fm=t.split('---',2)[1] if t.startswith('---') else ''
    aliases=fm.split('aliases:',1)[-1]
    for a in re.findall(r'^  - (.+)$',aliases,re.M):
        name_map[a.strip()].add(p.stem)
link_re=re.compile(r'(?<!!)\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]')
edges={p.stem:set() for p in paths}
unresolved=[]
en=cjk=0
note_stats=[]
for p in paths:
    t=p.read_text(encoding='utf-8')
    for target in link_re.findall(t):
        if target not in name_map:
            unresolved.append((p.stem,target))
        else:
            edges[p.stem].update(name_map[target])
    prose=re.sub(r'\A---.*?\n---','',t,flags=re.S)
    prose=re.sub(r'```.*?```','',prose,flags=re.S)
    prose=re.sub(r'\$\$.*?\$\$|\$[^$\n]*\$','',prose,flags=re.S)
    prose=re.sub(r'!\[\[.*?\]\]','',prose)
    prose=re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]',r'\2',prose)
    prose=re.sub(r'\[\[([^\]]+)\]\]',r'\1',prose)
    prose=re.sub(r'`[^`]+`','',prose)
    e=len(re.findall(r'\b[A-Za-z]+(?:[\x27’-][A-Za-z]+)*\b',prose))
    c=len(re.findall(r'[\u4e00-\u9fff]',prose))
    en+=e;cjk+=c
    note_stats.append({'title':p.stem,'lines':len(t.splitlines()),'english_words':e,'cjk_characters':c,'estimated_english_reading_share':round(e/(e+c/2)*100,1) if e+c else 0})
topic=set(edges)-{'ECE2050 Knowledge Tree','Glossary'}
incoming={name:set() for name in edges}
for name,targets in edges.items():
    for target in targets:
        incoming[target].add(name)
semantic_orphans=[n for n in topic if not (incoming[n]&topic)]
glossary_missing=sorted(topic-edges['Glossary'])
tree_missing=sorted(topic-edges['ECE2050 Knowledge Tree'])
report={'notes':len(topic),'hubs':len(paths)-len(topic),'wikilink_edges':sum(len(v) for v in edges.values()),'unresolved':unresolved,'ambiguous_aliases':{k:sorted(v) for k,v in name_map.items() if len(v)>1},'semantic_orphans':sorted(semantic_orphans),'tree_missing':tree_missing,'glossary_missing':glossary_missing,'english_words':en,'cjk_characters':cjk,'estimated_english_reading_share':round(en/(en+cjk/2)*100,1),'language_estimator':'English words / (English words + Chinese characters / 2), excluding YAML, code and math; a readability estimate rather than a strict token ratio.','note_stats':note_stats}
(root/'.scratch/expansion-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
summary={k:v for k,v in report.items() if k!='note_stats'}
print(json.dumps(summary,ensure_ascii=False,indent=2))
if unresolved or report['ambiguous_aliases'] or semantic_orphans or tree_missing or glossary_missing:
    raise SystemExit(1)
