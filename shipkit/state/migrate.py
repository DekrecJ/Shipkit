from __future__ import annotations
from shipkit.constants import STATE_SCHEMA, PROJECT_SCHEMA, PHASES
from shipkit.state.schema import now

def migrate_state(data: dict) -> tuple[dict,bool]:
    if data.get("$schema")==STATE_SCHEMA: return data,False
    out=dict(data); out["$schema"]=STATE_SCHEMA; out["schema_version"]=1; out["shipkit_version"]="0.2.0"; out.setdefault("blockers",[]); phases=out.setdefault("phases",{}); current=out.get("current_phase","discovery"); [phases.setdefault(p, "in_progress" if p==current else "pending") for p in PHASES]; out["updated_at"]=now(); return out,True

def migrate_project(data: dict) -> tuple[dict,bool]:
    if data.get("$schema")==PROJECT_SCHEMA: return data,False
    out=dict(data); out["$schema"]=PROJECT_SCHEMA; out["schema_version"]=1; out["shipkit_version"]="0.2.0"; return out,True
