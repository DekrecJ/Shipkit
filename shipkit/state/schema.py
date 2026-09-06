from __future__ import annotations
from datetime import datetime, timezone
from shipkit.constants import PHASES, STATE_SCHEMA, PROJECT_SCHEMA


def now(): return datetime.now(timezone.utc).isoformat()

def new_state(name: str) -> dict:
    ts=now(); return {"$schema":STATE_SCHEMA,"schema_version":1,"shipkit_version":"0.2.0","project":name,"current_phase":"discovery","phases":{p:("in_progress" if p=="discovery" else "pending") for p in PHASES},"current_task":None,"completed_tasks":[],"blockers":[],"created_at":ts,"updated_at":ts}

def new_project(name: str, project_type: str="unknown", level: str="intermediate") -> dict:
    return {"$schema":PROJECT_SCHEMA,"schema_version":1,"shipkit_version":"0.2.0","name":name,"type":project_type,"level":level,"summary":"","platforms":[],"roles":[],"features":[],"capabilities":{"auth":False,"database":False,"rbac":False,"multi_tenant":False,"storage":False,"notifications":False,"payments":False,"realtime":False,"ai":False},"stack":{},"constraints":[],"acceptance":[]}
