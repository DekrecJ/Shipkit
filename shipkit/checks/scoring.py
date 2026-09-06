from __future__ import annotations
from pathlib import Path
import importlib.resources as resources, json

def load_scoring(root:Path,project:dict|None):
    local=root/'.shipkit'/'scoring.json'
    if local.exists(): return json.loads(local.read_text(encoding='utf-8'))
    base=json.loads(resources.files('shipkit').joinpath('assets','specs','scoring-v1.json').read_text(encoding='utf-8'))
    ptype=(project or {}).get('type','unknown'); override=base.get('profiles',{}).get(ptype,{})
    out=json.loads(json.dumps(base)); out['weights'].update(override.get('weights',{})); out['thresholds'].update(override.get('thresholds',{})); return out
