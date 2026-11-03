from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=(root/'.scratch/ch4-expansion.md').read_text(encoding='utf-8')
changed=[]
for block in source.split('@@TARGET\n')[1:]:
    title,addition=block.split('\n',1)
    p=root/'Notes'/(title+'.md')
    text=p.read_text(encoding='utf-8')
    heading=addition.splitlines()[0]
    if heading not in text:
        marker='## Connections · 相关笔记'
        text=text.replace(marker,addition.strip()+'\n\n'+marker)
        p.write_text(text,encoding='utf-8')
        changed.append(title)
print('Refined original Ch4 notes:',len(changed))
