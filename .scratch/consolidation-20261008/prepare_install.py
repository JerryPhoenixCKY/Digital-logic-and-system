import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
live = (ROOT / 'Notes').resolve()
archive = (WORK / 'original-Notes').resolve()
stage = (WORK / 'draft' / 'Notes').resolve()
install = (WORK / 'install-Notes').resolve()
for path in [live, archive, stage, install]:
    assert ROOT == path or ROOT in path.parents, 'Path outside vault: ' + str(path)
assert not archive.exists(), 'Archive exists; installation must not replace it'
assert not install.exists(), 'Install folder already exists'
validation = json.loads((WORK / 'validation-staged.json').read_text('utf-8'))
audit = json.loads((WORK / 'audit-staged.json').read_text('utf-8'))
assert validation['errors'] == []
assert audit['summary']['errors'] == audit['summary']['warnings'] == 0
with zipfile.ZipFile(WORK / 'original-notes.zip') as z:
    archived = {Path(p).name: z.read(p) for p in z.namelist() if p.endswith('.md')}
    current = {p.name: p.read_bytes() for p in live.glob('*.md')}
    assert set(archived) == set(current), 'Original file set changed after backup'
    for name in current:
        old = archived[name].decode('utf-8-sig').replace('\r\n', '\n')
        new = current[name].decode('utf-8-sig').replace('\r\n', '\n')
        assert old == new, 'Original content changed after backup; preserve edits: ' + name
assert len(current) == 90 and len(list(stage.glob('*.md'))) == 33
for path in [ROOT / 'Tools' / 'README.md', ROOT / '.obsidian' / 'workspace.json']:
    if path.exists():
        shutil.copy2(path, WORK / ('before-' + path.parent.name + '-' + path.name))
shutil.copytree(stage, install)
assert {p.name: p.read_bytes() for p in install.glob('*.md')} == {p.name: p.read_bytes() for p in stage.glob('*.md')}
print('Original 90 files match the backup. Reviewed 33-file replacement is ready.')
