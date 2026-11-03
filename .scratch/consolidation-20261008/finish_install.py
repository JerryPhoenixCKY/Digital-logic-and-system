import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
mapping = json.loads((WORK / 'link-mapping.json').read_text('utf-8'))
live = ROOT / 'Notes'; stage = WORK / 'draft' / 'Notes'
assert {p.name: p.read_bytes() for p in live.glob('*.md')} == {p.name: p.read_bytes() for p in stage.glob('*.md')}

readme = ROOT / 'Tools' / 'README.md'
t = readme.read_text('utf-8').replace('88 篇专题笔记', '31 篇主线笔记')
needle = '- 枢纽双链统一写**文件名形式**'
t = t.replace(needle, '- **合并笔记 / Consolidated notes**：每章 1–5 篇，正文按概念与因果顺序推进；详细推导、例题与原图使用对应小节中的可展开块。旧标题与别名保留用于检索，正式双链指向新文件和相应小节。总行数含折叠内容，原有微型笔记的长度提示仅供参考。\n' + needle)
readme.write_text(t, 'utf-8')

workspace = ROOT / '.obsidian' / 'workspace.json'
def rewrite(value):
    if isinstance(value, str):
        if value.startswith('Notes/') and value.endswith('.md'):
            old = value[6:-3]
            if old in mapping:
                return 'Notes/' + mapping[old]['target'] + '.md'
        return value
    if isinstance(value, list):
        return [rewrite(v) for v in value]
    if isinstance(value, dict):
        out = {k: rewrite(v) for k, v in value.items()}
        if out.get('type') == 'leaf':
            file = out.get('state', {}).get('state', {}).get('file')
            if file and 'title' in out.get('state', {}):
                out['state']['title'] = Path(file).stem
        if 'lastOpenFiles' in out:
            out['lastOpenFiles'] = list(dict.fromkeys(out['lastOpenFiles']))
        return out
    return value
if workspace.exists():
    current = json.loads(workspace.read_text('utf-8'))
    updated = rewrite(current)
    if updated != current:
        workspace.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + '\n', 'utf-8')
print('Installed files match the reviewed draft; course documentation and open-note paths updated.')
