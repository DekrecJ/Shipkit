from __future__ import annotations

from pathlib import Path
import importlib.resources as resources
import shutil


def install() -> dict:
    target = Path.home() / ".claude" / "skills"
    target.mkdir(parents=True, exist_ok=True)
    src = resources.files("shipkit").joinpath("assets", "skills")
    installed = []
    for item in src.iterdir():
        if item.is_dir():
            dst = target / item.name
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(str(item), dst)
            installed.append(item.name)
    return {"skills_home": str(target), "skills": installed}
