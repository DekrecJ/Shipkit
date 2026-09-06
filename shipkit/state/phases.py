from __future__ import annotations
from pathlib import Path
from shipkit.constants import PHASES

CRITERIA={
"discovery":[("PROJECT.md",["overview","goals","users","constraints"],120)],
"requirements":[("REQUIREMENTS.md",["functional","non-functional","acceptance"],180)],
"architecture":[("ARCHITECTURE.md",["architecture","components","data"],180)],
"implementation":[],
"testing":[("TESTING.md",["unit","integration"],120)],
"security":[("SECURITY.md",["authentication","authorization","secrets"],120)],
"release":[]}

def validate_phase(root: Path, phase: str) -> dict:
    if phase not in PHASES: raise ValueError(f"Unknown phase: {phase}")
    base=root/'.shipkit'; checks=[]
    for name,sections,minlen in CRITERIA[phase]:
        p=base/name
        if not p.exists(): checks.append({"name":name,"ok":False,"detail":"missing"}); continue
        text=p.read_text(encoding='utf-8',errors='ignore').lower(); missing=[s for s in sections if s not in text]
        ok=len(text.strip())>=minlen and not missing and 'shipkit will' not in text
        detail='ok' if ok else ('missing sections: '+', '.join(missing) if missing else f'content too short (<{minlen})')
        checks.append({"name":name,"ok":ok,"detail":detail})
    ok=all(c['ok'] for c in checks) if checks else True
    return {"phase":phase,"ok":ok,"checks":checks}
