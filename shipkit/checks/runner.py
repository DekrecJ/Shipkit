from __future__ import annotations
from pathlib import Path
import json,re,sys
from shipkit.checks.model import CheckItem,CheckSection
from shipkit.checks.scoring import load_scoring
from shipkit.state.manager import load
from shipkit.utils.subprocess import run
SKIP_DIRS={'.git','node_modules','.venv','venv','dist','build','.next','coverage','__pycache__'}
TEXT_EXTS={'.py','.js','.jsx','.ts','.tsx','.json','.toml','.yaml','.yml','.env','.md','.txt'}
SECRET_PATTERNS=[('OpenAI-style key',re.compile(r'\bsk-[A-Za-z0-9_-]{20,}\b')),('GitHub token',re.compile(r'\bgh[pousr]_[A-Za-z0-9]{20,}\b')),('AWS access key',re.compile(r'\bAKIA[0-9A-Z]{16}\b')),('Private key',re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'))]
def _scripts(root):
    p=root/'package.json'
    if not p.exists(): return {}
    try: return json.loads(p.read_text(encoding='utf-8')).get('scripts',{})
    except Exception: return {}
def _run_script(root,name): return run(['npm','run',name],root) if name in _scripts(root) else None
def structure(root,w):
    s=CheckSection('Structure',w)
    for name in ['README.md','.shipkit','AGENTS.md']:
        ok=(root/name).exists(); s.items.append(CheckItem(name,'pass' if ok else 'fail','present' if ok else 'missing',blocker=name=='.shipkit'))
    return s
def build(root,w):
    s=CheckSection('Build',w); r=_run_script(root,'build')
    if r is not None: s.items.append(CheckItem('npm run build','pass' if r.ok else 'fail','build passed' if r.ok else (r.stderr or r.stdout or r.reason)[-800:],blocker=not r.ok)); return s
    if (root/'pyproject.toml').exists():
        r=run([sys.executable,'-m','compileall','-q','.'],root); s.items.append(CheckItem('python compile','pass' if r.ok else 'fail','compileall passed' if r.ok else (r.stderr or r.stdout)[-800:],blocker=not r.ok))
    else: s.items.append(CheckItem('build command','skip','no build script detected'))
    return s
def lint(root,w):
    s=CheckSection('Lint',w); scripts=_scripts(root); cand=next((x for x in ['lint','check','typecheck'] if x in scripts),None)
    if cand:
        r=_run_script(root,cand); s.items.append(CheckItem(f'npm run {cand}','pass' if r and r.ok else 'fail','passed' if r and r.ok else ((r.stderr or r.stdout)[-800:] if r else 'not available')))
    else:s.items.append(CheckItem('lint/typecheck','skip','no lint, check, or typecheck script detected'))
    return s
def tests(root,project,w):
    s=CheckSection('Tests',w); scripts=_scripts(root); r=None; label=''
    if 'test' in scripts: r=_run_script(root,'test');label='npm test'
    elif (root/'pyproject.toml').exists() and (root/'tests').exists() and any((root/'tests').rglob('test_*.py')): r=run([sys.executable,'-m','unittest','discover','-s','tests'],root);label='python unittest'
    if r: s.items.append(CheckItem(label,'pass' if r.ok else 'fail','test command passed' if r.ok else (r.stderr or r.stdout)[-1000:],blocker=not r.ok))
    else:s.items.append(CheckItem('test command','fail','no runnable test command detected',blocker=True))
    return s
def _iter(root):
    c=0
    for p in root.rglob('*'):
        if c>=2500: break
        if not p.is_file() or any(x in SKIP_DIRS for x in p.parts): continue
        if p.suffix.lower() not in TEXT_EXTS and p.name not in {'.env','.env.local','.env.production'}: continue
        try:
            if p.stat().st_size>1_000_000: continue
        except OSError: continue
        c+=1; yield p
def security(root,project,w):
    s=CheckSection('Security',w); gitignore=(root/'.gitignore').read_text(encoding='utf-8',errors='ignore') if (root/'.gitignore').exists() else ''
    envs=[root/x for x in ['.env','.env.local','.env.production'] if (root/x).exists()]
    if envs:
        ignored='.env' in gitignore or '.env*' in gitignore;s.items.append(CheckItem('environment files ignored','pass' if ignored else 'fail','.env ignore rule present' if ignored else 'environment file exists without ignore rule',blocker=not ignored))
    else:s.items.append(CheckItem('environment files','pass','no root environment file detected'))
    findings=[]
    for p in _iter(root):
        if p.name.endswith('.example') or p.name=='.env.example': continue
        try:text=p.read_text(encoding='utf-8',errors='ignore')
        except OSError:continue
        for label,pat in SECRET_PATTERNS:
            if pat.search(text): findings.append(f'{label} in {p.relative_to(root)}')
    s.items.append(CheckItem('baseline secret scan','fail' if findings else 'pass','; '.join(findings[:10]) if findings else 'no high-confidence secret patterns found',blocker=bool(findings)))
    return s
def documentation(root,project,w):
    s=CheckSection('Documentation',w); expected=['PROJECT.md','REQUIREMENTS.md','ARCHITECTURE.md','SECURITY.md','TESTING.md','TASKS.md']
    if (project or {}).get('capabilities',{}).get('database'): expected.append('DATABASE.md')
    for name in expected:
        p=root/'.shipkit'/name
        if not p.exists():s.items.append(CheckItem(name,'fail','missing'));continue
        text=p.read_text(encoding='utf-8',errors='ignore').strip(); placeholder='shipkit will' in text.lower() or len(text)<80
        s.items.append(CheckItem(name,'fail' if placeholder else 'pass','exists but still looks like a placeholder' if placeholder else 'documented'))
    return s
def state_check(root,state,w):
    s=CheckSection('ShipKit State',w)
    if not state:s.items.append(CheckItem('state.json','fail','missing or invalid',blocker=True));return s
    s.items.append(CheckItem('schema','pass' if state.get('$schema')=='shipkit:state-v1' else 'fail',str(state.get('$schema')),blocker=state.get('$schema')!='shipkit:state-v1'))
    blockers=state.get('blockers',[]); s.items.append(CheckItem('lifecycle debt','fail' if blockers else 'pass','; '.join(blockers) if blockers else 'none',blocker=bool(blockers))); return s
def run_all(root:Path):
    project,state=load(root); scoring=load_scoring(root,project); w=scoring['weights']
    sections=[structure(root,w['structure']),build(root,w['build']),lint(root,w['lint']),tests(root,project,w['tests']),security(root,project,w['security']),documentation(root,project,w['documentation']),state_check(root,state,w['state'])]
    raw=sum(s.score() for s in sections); max_score=sum(s.weight for s in sections); score=round(raw*100/max_score) if max_score else 0
    blockers=[f'{s.name}: {i.name} — {i.detail}' for s in sections for i in s.items if i.blocker and i.status=='fail']
    th=scoring['thresholds']; status='READY' if score>=th['ready'] and not blockers else ('REVIEW' if score>=th['review'] and not blockers else 'NOT_READY')
    return {'scoring_schema':scoring['$schema'],'score':score,'status':status,'blockers':blockers,'sections':[s.to_dict() for s in sections]}
