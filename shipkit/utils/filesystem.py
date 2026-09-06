from __future__ import annotations

from pathlib import Path
import json
import shutil


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path, default=None):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def write_json(path: Path, value) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def append_managed_block(path: Path, marker: str, content: str) -> None:
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    block = f"{start}\n{content.rstrip()}\n{end}"
    if start in current and end in current:
        before = current.split(start, 1)[0].rstrip()
        after = current.split(end, 1)[1].lstrip()
        new = "\n\n".join(x for x in [before, block, after] if x).rstrip() + "\n"
    else:
        new = current.rstrip() + ("\n\n" if current.strip() else "") + block + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new, encoding="utf-8")


def remove_managed_block(path: Path, marker: str) -> None:
    if not path.exists():
        return
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    current = path.read_text(encoding="utf-8")
    if start not in current or end not in current:
        return
    before = current.split(start, 1)[0].rstrip()
    after = current.split(end, 1)[1].lstrip()
    new = "\n\n".join(x for x in [before, after] if x).rstrip()
    path.write_text((new + "\n") if new else "", encoding="utf-8")
