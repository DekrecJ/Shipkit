from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from shipkit.constants import PHASES, SHIPKIT_DIR
from shipkit.utils.filesystem import read_json, write_json_atomic, recover_json
from shipkit.state.schema import new_state,new_project
from shipkit.state.migrate import migrate_state,migrate_project
from shipkit.state.phases import validate_phase

def paths(root:Path):
    base=root/SHIPKIT_DIR; return base,base/'project.json',base/'state.json'

def initialize(root:Path,name:str,project_type='unknown',level='intermediate',force=False):
    base,pp,sp=paths(root); base.mkdir(parents=True,exist_ok=True)
    if (pp.exists() or sp.exists()) and not force: raise FileExistsError('ShipKit project already exists. Use --force to reinitialize metadata.')
    project=new_project(name,project_type,level); state=new_state(name)
    write_json_atomic(pp,project); write_json_atomic(sp,state); return {'project':project,'state':state}

def load(root:Path,auto_migrate=True):
    _,pp,sp=paths(root)
    project=read_json(pp); state=read_json(sp)
    if auto_migrate:
        if project:
            project,changed=migrate_project(project)
            if changed: write_json_atomic(pp,project)
        if state:
            state,changed=migrate_state(state)
            if changed: write_json_atomic(sp,state)
    return project,state

def _save_state(sp:Path,state:dict):
    state['updated_at']=datetime.now(timezone.utc).isoformat(); write_json_atomic(sp,state); return state

def update_phase(root:Path,phase:str,status='in_progress',force=False):
    if phase not in PHASES: raise ValueError(f'Unknown phase: {phase}')
    _,_,sp=paths(root); _,state=load(root)
    if not state: raise FileNotFoundError('No .shipkit/state.json found')
    current=state.get('current_phase','discovery'); ci=PHASES.index(current); ti=PHASES.index(phase)
    if ti>ci+1 and not force: raise ValueError(f'Cannot jump from {current} to {phase}. Use shipkit advance or --force.')
    if ti>ci and current in PHASES:
        validation=validate_phase(root,current)
        if not validation['ok'] and not force: raise ValueError(f'Cannot leave {current}; phase validation failed.')
        state['phases'][current]='completed' if validation['ok'] else 'blocked'
        if not validation['ok']:
            debt=f'Forced transition from incomplete phase: {current}'
            if debt not in state.setdefault('blockers',[]): state['blockers'].append(debt)
    state['current_phase']=phase; state['phases'][phase]=status
    return _save_state(sp,state)

def advance(root:Path,force=False):
    _,state=load(root)
    if not state: raise FileNotFoundError('No .shipkit/state.json found')
    current=state['current_phase']; idx=PHASES.index(current)
    if idx==len(PHASES)-1: return state
    return update_phase(root,PHASES[idx+1],'in_progress',force=force)

def update_task(root:Path,task_id:str,status:str):
    _,_,sp=paths(root); _,state=load(root)
    if not state: raise FileNotFoundError('No .shipkit/state.json found')
    completed=state.setdefault('completed_tasks',[])
    if status=='in_progress': state['current_task']=task_id
    elif status=='completed':
        if task_id not in completed: completed.append(task_id)
        if state.get('current_task')==task_id: state['current_task']=None
    elif status=='blocked': state['current_task']=task_id; state['task_blocked']=task_id
    return _save_state(sp,state)

def repair(root:Path):
    _,pp,sp=paths(root); repaired=[]
    for p in [pp,sp]:
        if not p.exists(): continue
        try:
            _,did=recover_json(p)
            if did: repaired.append(p.name)
        except Exception:
            continue
    project,state=load(root,auto_migrate=True)
    return {'project':bool(project),'state':bool(state),'repaired':repaired}
