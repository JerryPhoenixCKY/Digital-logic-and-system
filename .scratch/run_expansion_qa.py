from pathlib import Path
import json,subprocess,sys,re,hashlib
root=Path(__file__).resolve().parents[1]
out=root/'.scratch/qa-20260930'
out.mkdir(exist_ok=True)
plugin=Path('C:/Users/lucky/.codex/plugins/cache/personal/cky-obsidian-assistant/1.0.0+codex.20260928005737/skills/hardware-vault-maintenance/scripts/audit_vault.py')
commands={
    'vault':[sys.executable,'Tools/check_vault.py'],
    'concept-graph':[sys.executable,'.scratch/audit_expansion.py'],
    'new-models':[sys.executable,'.scratch/verify_expansion.py'],
    'applications':[sys.executable,'.scratch/application-checks.py'],
    'original-ch2':[sys.executable,'.scratch/verify_ch2.py'],
    'original-ch34':[sys.executable,'.scratch/verify_ch34.py'],
    'new-figure-models':['D:/anaconda/python.exe','.scratch/expansion-figure-checks.py'],
    'new-figure-layout':['D:/anaconda/python.exe','Tools/figcheck.py','setup-hold-window','register-short-long-paths','serial-shift-trace'],
    'plugin-vault-audit':[sys.executable,str(plugin),str(root),'--exclude','.scratch','--exclude','Tools','--exclude','LGU_HUB_ECE2050','--strict-links','--format','json'],
}
results={}
for name,cmd in commands.items():
    r=subprocess.run(cmd,cwd=root,capture_output=True,encoding='utf-8',errors='replace')
    (out/(name+'.txt')).write_text(r.stdout+('\nSTDERR:\n'+r.stderr if r.stderr else ''),encoding='utf-8')
    results[name]={'exit_code':r.returncode,'status':'PASS' if r.returncode==0 else 'FAIL'}

# Check Markdown delimiters and metadata without imposing a paragraph-length rule.
issues=[]
for p in (root/'Notes').glob('*.md'):
    t=p.read_text(encoding='utf-8')
    if len(re.findall(r'^```',t,re.M))%2:
        issues.append((p.name,'unclosed code/Mermaid fence'))
    t=re.sub(r'```.*?```','',t,flags=re.S)
    t=re.sub(r'`[^`\n]*`',' ',t)
    if len(re.findall(r'(?<!\\)\$\$',t))%2:
        issues.append((p.name,'unclosed display math'))
    t=re.sub(r'\$\$.*?\$\$','',t,flags=re.S)
    for n,line in enumerate(t.splitlines(),1):
        if len(re.findall(r'(?<!\\)\$',line))%2:
            issues.append((p.name,f'unpaired inline math at stripped line {n}'))
(out/'markdown-boundaries.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2),encoding='utf-8')
results['markdown-boundaries']={'status':'PASS' if not issues else 'FAIL','findings':len(issues)}
manifest=json.loads((root/'.scratch/sources-20260930/manifest.json').read_text(encoding='utf-8'))
changed_sources=[]
for row in manifest:
    p=root/'LGU_HUB_ECE2050'/row['file']
    if hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
        changed_sources.append(row['file'])
results['source-integrity']={'status':'FAIL' if changed_sources else 'PASS','checked_files':len(manifest),'changed_files':changed_sources}
(out/'summary.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
if issues:
    print(json.dumps(issues,ensure_ascii=False,indent=2))
if any(v['status']=='FAIL' for v in results.values()):
    raise SystemExit(1)
