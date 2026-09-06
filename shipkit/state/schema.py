from __future__ import annotations

from datetime import datetime, timezone
from shipkit.constants import PHASES


def new_state(name: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "shipkit_version": "0.1.0",
        "project": name,
        "current_phase": "discovery",
        "phases": {phase: ("in_progress" if phase == "discovery" else "pending") for phase in PHASES},
        "current_task": None,
        "completed_tasks": [],
        "created_at": now,
        "updated_at": now,
    }


def new_project(name: str, project_type: str = "unknown", level: str = "intermediate") -> dict:
    return {
        "name": name,
        "type": project_type,
        "level": level,
        "summary": "",
        "platforms": [],
        "roles": [],
        "features": [],
        "capabilities": {
            "auth": False,
            "database": False,
            "rbac": False,
            "multi_tenant": False,
            "storage": False,
            "notifications": False,
            "payments": False,
            "realtime": False,
            "ai": False,
        },
        "stack": {},
        "constraints": [],
        "acceptance": [],
    }
