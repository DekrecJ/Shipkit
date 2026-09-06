from __future__ import annotations
from pathlib import Path
import json, os, shutil, tempfile


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True); return path


def read_json(path: Path, default=None):
    if not path.exists(): return default
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError): return default


def read_json_strict(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, value, backup: bool=True) -> None:
    ensure_dir(path.parent)
    data=json.dumps(value, indent=2, ensure_ascii=False)+"\n"
    if backup and path.exists():
        shutil.copy2(path, path.with_suffix(path.suffix+".bak"))
    fd,tmp=tempfile.mkstemp(prefix=path.name+".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd,'w',encoding='utf-8',newline='\n') as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def write_json(path: Path, value) -> None:
    write_json_atomic(path, value)


def recover_json(path: Path):
    try: return read_json_strict(path), False
    except Exception:
        bak=path.with_suffix(path.suffix+".bak")
        if bak.exists():
            data=read_json_strict(bak); write_json_atomic(path,data,backup=False); return data, True
        raise


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src,dst)


def append_managed_block(path: Path, marker: str, content: str) -> None:
    start=f"<!-- {marker}:START -->"; end=f"<!-- {marker}:END -->"
    current=path.read_text(encoding='utf-8') if path.exists() else ''
    block=f"{start}\n{content.rstrip()}\n{end}"
    if start in current and end in current:
        before=current.split(start,1)[0].rstrip(); after=current.split(end,1)[1].lstrip()
        new="\n\n".join(x for x in [before,block,after] if x).rstrip()+"\n"
    else: new=current.rstrip()+("\n\n" if current.strip() else '')+block+"\n"
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(new,encoding='utf-8')


def remove_managed_block(path: Path, marker: str) -> None:
    if not path.exists(): return
    start=f"<!-- {marker}:START -->"; end=f"<!-- {marker}:END -->"; current=path.read_text(encoding='utf-8')
    if start not in current or end not in current: return
    before=current.split(start,1)[0].rstrip(); after=current.split(end,1)[1].lstrip(); new="\n\n".join(x for x in [before,after] if x).rstrip()
    path.write_text((new+'\n') if new else '',encoding='utf-8')
