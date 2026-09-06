from __future__ import annotations

from pathlib import Path
import importlib.resources as resources
import os
import shutil

from shipkit.utils.filesystem import append_managed_block, remove_managed_block

MARKER = "SHIPKIT-GLOBAL"


def _assets():
    return resources.files("shipkit").joinpath("assets")


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser()


def skills_home() -> Path:
    override = os.environ.get("SHIPKIT_SKILLS_HOME")
    return Path(override).expanduser() if override else Path.home() / ".agents" / "skills"


def library_home() -> Path:
    return Path.home() / ".shipkit" / "library"


def install() -> dict:
    skill_target = skills_home()
    skill_target.mkdir(parents=True, exist_ok=True)
    source_skills = _assets().joinpath("skills")
    installed = []
    for item in source_skills.iterdir():
        if not item.is_dir():
            continue
        dst = skill_target / item.name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(str(item), dst)
        installed.append(item.name)

    lib = library_home()
    lib.mkdir(parents=True, exist_ok=True)
    for folder in ["blueprints", "capabilities", "templates"]:
        src = _assets().joinpath(folder)
        dst = lib / folder
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(str(src), dst)

    global_agents = codex_home() / "AGENTS.md"
    bootstrap = _assets().joinpath("templates", "AGENTS.global.md").read_text(encoding="utf-8")
    append_managed_block(global_agents, MARKER, bootstrap)
    return {"skills_home": str(skill_target), "codex_home": str(codex_home()), "skills": installed, "library": str(lib)}


def uninstall() -> dict:
    removed = []
    target = skills_home()
    if target.exists():
        for path in target.glob("shipkit-*"):
            if path.is_dir():
                shutil.rmtree(path)
                removed.append(str(path))
    remove_managed_block(codex_home() / "AGENTS.md", MARKER)
    lib = library_home()
    if lib.exists():
        shutil.rmtree(lib)
    return {"removed": removed}
