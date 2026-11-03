from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
src=root/'.scratch/sources-20260930'
for p in sorted(src.glob('*.txt')):
    if 'Chap' in p.name or 'VHDL' in p.name or 'Vivado' in p.name: continue
    print('\nDOCUMENT',p.name)
    for part in re.split(r'========== PAGE (\d+) ==========\n',p.read_text(encoding='utf-8'))[1::2]:
        pass
    chunks=re.split(r'========== PAGE (\d+) ==========\n',p.read_text(encoding='utf-8'))
    for i in range(1,len(chunks),2):
        t=re.sub(r'\s+',' ',chunks[i+1])
        t=re.sub(r'<latexit.*?</latexit>','',t)
        print('p'+chunks[i]+': '+t[:650])
