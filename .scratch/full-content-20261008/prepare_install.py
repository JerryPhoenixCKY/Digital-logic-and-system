from pathlib import Path
import hashlib
import json
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
NOTES = ROOT/'Notes'
with zipfile.ZipFile(WORK/'before-enrichment.zip') as z:
    before = {Path(n).name:z.read(n).decode('utf-8-sig') for n in z.namelist() if n.endswith('.md')}
current = {p.name:p.read_text('utf-8-sig') for p in NOTES.iterdir() if p.is_file() and p.suffix == '.md'}
assert {p.name for p in NOTES.iterdir()} == set(before), 'Notes changed in structure during editing; inspect before installation'
def normalize(t):
    return t.replace('\r\n','\n').replace('[[Boolean Forms and Algebraic Simplification 1', '[[Boolean Forms and Algebraic Simplification')
changes = [n for n in before if normalize(before[n]) != normalize(current[n])]
assert not changes, 'New edits need merging before installation: '+repr(changes)
preflight = {'current_notes':len(current), 'new_content_edits':changes,
             'current_hashes':{n:hashlib.sha256((NOTES/n).read_bytes()).hexdigest() for n in current}}
(WORK/'pre-install-check.json').write_text(json.dumps(preflight,ensure_ascii=False,indent=2),'utf-8')

with zipfile.ZipFile(WORK/'pre-install-current-notes.zip','w',zipfile.ZIP_DEFLATED) as z:
    for n in sorted(current):z.write(NOTES/n,'Notes/'+n)

for p in (WORK/'draft/Notes').glob('*.md'):
    t=p.read_text('utf-8')
    t=re.sub(r'^updated: \d{4}-\d{2}-\d{2}$','updated: 2026-10-09',t,count=1,flags=re.M)
    p.write_text(t,'utf-8')
install=WORK/'install-Notes'
assert not install.exists(), 'Installation preparation already exists; inspect it before retrying'
shutil.copytree(WORK/'draft/Notes',install)
print(json.dumps({'current_notes_preserved':len(current),'new_content_edits':changes,'prepared_formal_notes':len(list(install.glob('*.md')))},ensure_ascii=False,indent=2))
