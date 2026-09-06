from __future__ import annotations
import argparse,json,shutil,sys
from pathlib import Path
from shipkit import __version__
from shipkit.constants import LEVELS,PROJECT_TYPES,PHASES
from shipkit.state.manager import initialize,load,update_phase,update_task,advance,repair
from shipkit.state.phases import validate_phase
from shipkit.project_setup import scaffold_project
from shipkit.checks.runner import run_all
from shipkit.installer import codex as codex_installer, claude as claude_installer

def _root(v): return Path(v or '.').resolve()
def cmd_install(a):
    r=codex_installer.install() if a.target=='codex' else claude_installer.install(); print(f'ShipKit {__version__} installed for {a.target}'); print(f"  Skills: {r['skills_home']}")
def cmd_init(a):
    root=_root(a.path); name=a.name or root.name
    try: initialize(root,name,a.type,a.level,a.force)
    except FileExistsError as e: print(str(e),file=sys.stderr); return 2
    scaffold_project(root,name); print(f'◆ ShipKit initialized: {name}')
def cmd_status(a):
    project,state=load(_root(a.path))
    if not project or not state: print('No ShipKit project found.',file=sys.stderr); return 2
    completed=sum(v=='completed' for v in state['phases'].values()); progress=round(completed/len(PHASES)*100)
    print("SHIPKIT STATUS")
    print(f"Project: {project['name']}")
    print(f"Type: {project['type']}")
    print(f"Progress: {progress}%")
    print(f"Current phase: {state['current_phase']}")
    if state.get('blockers'): print('Blockers: '+ '; '.join(state['blockers']))
def cmd_validate(a):
    _,state=load(_root(a.path)); phase=a.phase or (state or {}).get('current_phase')
    if not phase: return 2
    r=validate_phase(_root(a.path),phase); print(json.dumps(r,indent=2)); return 0 if r['ok'] else 1
def cmd_advance(a):
    try:r=advance(_root(a.path),force=a.force); print(f"Advanced to: {r['current_phase']}")
    except (ValueError,FileNotFoundError) as e: print(str(e),file=sys.stderr); return 2
def cmd_phase(a):
    try:r=update_phase(_root(a.path),a.phase,a.status,a.force); print(f"ShipKit phase updated: {a.phase} -> {a.status}")
    except (ValueError,FileNotFoundError) as e: print(str(e),file=sys.stderr); return 2
def cmd_task(a):
    try:r=update_task(_root(a.path),a.task_id,a.status); print(f"ShipKit task updated: {a.task_id} -> {a.status}")
    except FileNotFoundError as e: print(str(e),file=sys.stderr); return 2
def cmd_check(a):
    r=run_all(_root(a.path))
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print("SHIPKIT CHECK")
        print(f"Score: {r['score']}/100")
        print(f"Status: {r['status']}")
        if r['blockers']:
            for b in r['blockers']:
                print("- "+b)
        else:
            print("No blocking failures.")
    return 0 if r['status']=='READY' else 1
def cmd_repair(a): print(json.dumps(repair(_root(a.path)),indent=2))
def cmd_migrate(a):
    project,state=load(_root(a.path),auto_migrate=True); print(json.dumps({'project_schema':project.get('$schema') if project else None,'state_schema':state.get('$schema') if state else None},indent=2))
def cmd_doctor(a):
    print(f'SHIPKIT DOCTOR {__version__}')
    for tool in ['git','codex','node','npm','docker']:
        path=shutil.which(tool); print(('✓' if path else '○')+f' {tool}: {path or "not found"}')
    if a.project:
        project,state=load(_root(a.path)); print('Project metadata: '+('ok' if project else 'missing')); print('Project state: '+('ok' if state else 'missing'))
def build_parser():
    p=argparse.ArgumentParser(prog='shipkit'); p.add_argument('--version',action='version',version=f'ShipKit {__version__}'); sub=p.add_subparsers(dest='command',required=True)
    sp=sub.add_parser('install'); sp.add_argument('target',choices=['codex','claude']); sp.set_defaults(func=cmd_install)
    sp=sub.add_parser('init'); sp.add_argument('--path',default='.'); sp.add_argument('--name'); sp.add_argument('--type',choices=PROJECT_TYPES,default='unknown'); sp.add_argument('--level',choices=LEVELS,default='intermediate'); sp.add_argument('--force',action='store_true'); sp.set_defaults(func=cmd_init)
    sp=sub.add_parser('status'); sp.add_argument('--path',default='.'); sp.set_defaults(func=cmd_status)
    sp=sub.add_parser('validate-phase'); sp.add_argument('--phase',choices=PHASES); sp.add_argument('--path',default='.'); sp.set_defaults(func=cmd_validate)
    sp=sub.add_parser('advance'); sp.add_argument('--path',default='.'); sp.add_argument('--force',action='store_true'); sp.set_defaults(func=cmd_advance)
    sp=sub.add_parser('phase'); sp.add_argument('phase',choices=PHASES); sp.add_argument('--status',choices=['pending','in_progress','completed','blocked'],default='in_progress'); sp.add_argument('--path',default='.'); sp.add_argument('--force',action='store_true'); sp.set_defaults(func=cmd_phase)
    sp=sub.add_parser('task'); sp.add_argument('task_id'); sp.add_argument('--status',choices=['in_progress','completed','blocked'],default='in_progress'); sp.add_argument('--path',default='.'); sp.set_defaults(func=cmd_task)
    sp=sub.add_parser('check'); sp.add_argument('--path',default='.'); sp.add_argument('--json',action='store_true'); sp.set_defaults(func=cmd_check)
    sp=sub.add_parser('repair'); sp.add_argument('--path',default='.'); sp.set_defaults(func=cmd_repair)
    sp=sub.add_parser('migrate'); sp.add_argument('--path',default='.'); sp.set_defaults(func=cmd_migrate)
    sp=sub.add_parser('doctor'); sp.add_argument('--project',action='store_true'); sp.add_argument('--path',default='.'); sp.set_defaults(func=cmd_doctor)
    return p
def main(argv=None):
    a=build_parser().parse_args(argv); return int(a.func(a) or 0)
