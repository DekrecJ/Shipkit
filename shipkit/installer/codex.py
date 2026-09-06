from __future__ import annotations
from pathlib import Path
import importlib.resources as resources,os,shutil
from shipkit.utils.filesystem import append_managed_block,remove_managed_block
MARKER='SHIPKIT-GLOBAL'
def _assets(): return resources.files('shipkit').joinpath('assets')
def codex_home(): return Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex'))).expanduser()
def skills_home():
    o=os.environ.get('SHIPKIT_SKILLS_HOME'); return Path(o).expanduser() if o else Path.home()/'.agents'/'skills'
def library_home(): return Path.home()/'.shipkit'/'library'
def install():
    target=skills_home(); target.mkdir(parents=True,exist_ok=True); installed=[]
    for item in _assets().joinpath('skills').iterdir():
        if not item.is_dir(): continue
        dst=target/item.name
        if dst.exists(): shutil.rmtree(dst)
        shutil.copytree(str(item),dst); installed.append(item.name)
    lib=library_home(); lib.mkdir(parents=True,exist_ok=True)
    for folder in ['blueprints','capabilities','templates','specs','schemas']:
        src=_assets().joinpath(folder); dst=lib/folder
        if dst.exists(): shutil.rmtree(dst)
        shutil.copytree(str(src),dst)
    bootstrap=_assets().joinpath('templates','AGENTS.global.md').read_text(encoding='utf-8'); append_managed_block(codex_home()/'AGENTS.md',MARKER,bootstrap)
    return {'skills_home':str(target),'codex_home':str(codex_home()),'skills':installed,'library':str(lib)}
def uninstall():
    removed=[]; target=skills_home()
    if target.exists():
        for p in target.glob('shipkit-*'):
            if p.is_dir(): shutil.rmtree(p); removed.append(str(p))
    remove_managed_block(codex_home()/'AGENTS.md',MARKER); lib=library_home()
    if lib.exists(): shutil.rmtree(lib)
    return {'removed':removed}
