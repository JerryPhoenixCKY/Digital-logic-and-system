from pathlib import Path
import contextlib
import hashlib
import importlib.util
import io
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
MODE = 'live' if '--live' in sys.argv else 'staged'
VAULT = ROOT if MODE == 'live' else WORK/'draft'

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

audit_mod = load_module('audit_final', Path('C:/Users/lucky/.codex/plugins/cache/personal/cky-obsidian-assistant/1.0.0+codex.20260928005737/skills/hardware-vault-maintenance/scripts/audit_vault.py'))
report = audit_mod.audit(VAULT, ['.scratch', 'Tools'], True)
(WORK/('audit-'+MODE+'.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2), 'utf-8')
print('Strict audit:', json.dumps(report['summary'], ensure_ascii=False))
if report['issues']:
    print(json.dumps(report['issues'], ensure_ascii=False, indent=2))

qa = load_module('vault_qa_final', ROOT/'Tools/check_vault.py')
qa.NOTES = VAULT/'Notes'
qa.FIGS = ROOT/'Figures'
with contextlib.redirect_stdout(io.StringIO()) as output:
    result = qa.main()
qa_report = {'mode': MODE, 'problems': qa.problems, 'warnings': qa.warnings, 'output': output.getvalue()}
(WORK/('native-qa-'+MODE+'.json')).write_text(json.dumps(qa_report, ensure_ascii=False, indent=2), 'utf-8')
print('Original validator:', json.dumps({'problems':len(qa.problems),'warnings':len(qa.warnings)},ensure_ascii=False))
if qa.problems:
    print(json.dumps(qa.problems, ensure_ascii=False, indent=2))

hashes = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Figures').iterdir() if p.is_file()}
manifest = WORK/'figure-hashes.json'
if not manifest.exists():
    manifest.write_text(json.dumps(hashes, ensure_ascii=False, indent=2), 'utf-8')
else:
    assert hashes == json.loads(manifest.read_text('utf-8')), 'A figure changed during enrichment'
print('Figure files preserved:', len(hashes))
raise SystemExit(1 if result or report['summary']['errors'] else 0)
