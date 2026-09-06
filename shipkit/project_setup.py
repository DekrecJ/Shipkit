from __future__ import annotations

from pathlib import Path
import importlib.resources as resources
from shipkit.utils.filesystem import append_managed_block

DOCS = ["PROJECT.md", "REQUIREMENTS.md", "ARCHITECTURE.md", "DATABASE.md", "SECURITY.md", "TESTING.md", "TASKS.md"]


def _asset_text(relative: str) -> str:
    return resources.files("shipkit").joinpath("assets", relative).read_text(encoding="utf-8")


def scaffold_project(root: Path, name: str) -> None:
    base = root / ".shipkit"
    base.mkdir(parents=True, exist_ok=True)
    for doc in DOCS:
        path = base / doc
        if not path.exists():
            path.write_text(_asset_text(f"templates/{doc}").replace("{{PROJECT_NAME}}", name), encoding="utf-8")
    agents = _asset_text("templates/AGENTS.project.md").replace("{{PROJECT_NAME}}", name)
    append_managed_block(root / "AGENTS.md", "SHIPKIT-PROJECT", agents)
