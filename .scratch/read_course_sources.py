from pathlib import Path
import hashlib, json, zipfile
from xml.etree import ElementTree as ET
from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
out = root / '.scratch' / 'sources-20260930'
out.mkdir(exist_ok=True)
records = []
for p in sorted((root / 'LGU_HUB_ECE2050').iterdir()):
    if p.suffix.lower() not in {'.pdf', '.pptx', '.md'}:
        continue
    record = {'file': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    chunks = []
    if p.suffix.lower() == '.pdf':
        reader = PdfReader(p)
        for i, page in enumerate(reader.pages, 1):
            s = page.extract_text() or ''
            chunks.append(f'========== PAGE {i} ==========\n{s}')
        record['pages'] = len(reader.pages)
        record['short_pages'] = [i+1 for i,pag in enumerate(reader.pages) if len((pag.extract_text() or '').strip()) < 70]
    elif p.suffix.lower() == '.pptx':
        with zipfile.ZipFile(p) as z:
            names = sorted([n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')], key=lambda n:int(n.rsplit('slide',1)[1].split('.')[0]))
            for i, name in enumerate(names, 1):
                elem = ET.fromstring(z.read(name))
                s = '\n'.join(n.text or '' for n in elem.iter() if n.tag.endswith('}t'))
                chunks.append(f'========== SLIDE {i} ==========\n{s}')
            record['slides'] = len(names)
    else:
        chunks = [p.read_text(encoding='utf-8')]
    text = '\n\n'.join(chunks)
    record['chars'] = len(text)
    (out / (p.name+'.txt')).write_text(text, encoding='utf-8')
    records.append(record)
(out/'manifest.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
for r in records:
    print(f"{r['file']}: {r.get('pages',r.get('slides',1))} pages/slides, {r['chars']} chars, sparse={r.get('short_pages',[])}")
groups = {}
for r in records: groups.setdefault(r['sha256'],[]).append(r['file'])
print('EXACT DUPLICATES:', [v for v in groups.values() if len(v)>1])
