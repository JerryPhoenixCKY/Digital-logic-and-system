from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
notes=root/'Notes'
records=[]
for draft in sorted((root/'.scratch/expansion-drafts').glob('*.md')):
    for block in draft.read_text(encoding='utf-8').split('@@NOTE\n')[1:]:
        meta,body=block.split('\n',1)
        title,zh,alt,tag,chapter=meta.split('|')
        path=notes/(title+'.md')
        body=body.replace('索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]','').strip().removesuffix('---').strip()
        text=f'---\ntags:\n  - ECE2050\n  - {tag}\ndate: 2026-09-30\naliases:\n  - {zh}\n  - {title}\n  - {alt}\n---\n\n# {title} · {zh}\n\n'+body+'\n\n---\n索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]\n'
        path.write_text(text,encoding='utf-8')
        records.append(dict(title=title,zh=zh,alt=alt,tag=tag,chapter=chapter))
(root/'.scratch/expansion-manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('Created/refined',len(records),'expansion notes')
