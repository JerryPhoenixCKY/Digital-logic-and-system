from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
for title in ['Binary Number System','Decimal Number System','Hexadecimal Number System','Number Systems']:
    p=root/'Notes'/(title+'.md')
    lines=p.read_text(encoding='utf-8').splitlines()
    fixed=[]
    i=0
    changes=0
    while i<len(lines):
        line=lines[i]
        clean=re.sub(r'`[^`]*`','',line)
        count=len(re.findall(r'(?<!\\)\$',clean))
        if count%2 and i+1<len(lines) and lines[i+1].strip().startswith('='):
            following=lines[i+1]
            assert len(re.findall(r'(?<!\\)\$',following))%2
            fixed.append(line+' '+following.strip())
            i+=2
            changes+=1
        else:
            fixed.append(line)
            i+=1
    p.write_text('\n'.join(fixed)+'\n',encoding='utf-8')
    print(title,changes,'inline math spans joined')
