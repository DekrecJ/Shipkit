from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from shipkit.constants import PHASES, SHIPKIT_DIR
from shipkit.utils.filesystem import read_json, write_json
from .schema import new_state, new_project


def paths(root: Path) -> tuple[Path, Path, Path]:
    base = root / SHIPKIT_DIR
    return base, base / "project.json", base / "state.json"


def initialize(root: Path, name: str, project_type: str = "unknown", level: str = "intermediate", force: bool = False) -> dict:
    base, project_path, state_path = paths(root)
    base.mkdir(parents=True, exist_ok=True)
    if (project_path.exists() or state_path.exists()) and not force:
        raise FileExistsError("ShipKit project already exists. Use --force to reinitialize metadata.")
    project = new_project(name, project_type, level)
    state = new_state(name)
    write_json(project_path, project)
    write_json(state_path, state)
    return {"project": project, "state": state}


def load(root: Path) -> tuple[dict | None, dict | None]:
    _, project_path, state_path = paths(root)
    return read_json(project_path), read_json(state_path)


def update_phase(root: Path, phase: str, status: str = "in_progress") -> dict:
    if phase not in PHASES:
        raise ValueError(f"Unknown phase: {phase}")
    _, _, state_path = paths(root)
    state = read_json(state_path)
    if not state:
        raise FileNotFoundError("No .shipkit/state.json found")
    idx = PHASES.index(phase)
    for i, p in enumerate(PHASES):
        if i < idx and state["phases"].get(p) != "completed":
            state["phases"][p] = "completed"
    state["current_phase"] = phase
    state["phases"][phase] = status
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(state_path, state)
    return state


def update_task(root: Path, task_id: str, status: str) -> dict:
    _, _, state_path = paths(root)
    state = read_json(state_path)
    if not state:
        raise FileNotFoundError("No .shipkit/state.json found")
    completed = state.setdefault("completed_tasks", [])
    if status == "in_progress":
        state["current_task"] = task_id
    elif status == "completed":
        if task_id not in completed:
            completed.append(task_id)
        if state.get("current_task") == task_id:
            state["current_task"] = None
    elif status == "blocked":
        state["current_task"] = task_id
        state["task_blocked"] = task_id
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(state_path, state)
    return state
