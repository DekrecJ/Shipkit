from __future__ import annotations

from pathlib import Path
import json
import os
import re
import sys
from shipkit.checks.model import CheckItem, CheckSection
from shipkit.state.manager import load
from shipkit.utils.subprocess import run

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", ".next", "coverage", "__pycache__"}
TEXT_EXTS = {".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".toml", ".yaml", ".yml", ".env", ".md", ".txt"}
SECRET_PATTERNS = [
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
]


def _package_scripts(root: Path) -> dict:
    path = root / "package.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("scripts", {})
    except Exception:
        return {}


def _run_script(root: Path, name: str):
    scripts = _package_scripts(root)
    if name not in scripts:
        return None
    return run(["npm", "run", name], root)


def structure(root: Path) -> CheckSection:
    s = CheckSection("Structure", 10)
    expected = ["README.md", ".shipkit", "AGENTS.md"]
    for name in expected:
        ok = (root / name).exists()
        s.items.append(CheckItem(name, "pass" if ok else "fail", "present" if ok else "missing", blocker=name == ".shipkit"))
    has_manifest = any((root / f).exists() for f in ["package.json", "pyproject.toml", "Cargo.toml", "go.mod"])
    s.items.append(CheckItem("project manifest", "pass" if has_manifest else "warn", "detected" if has_manifest else "no standard manifest detected"))
    return s


def build(root: Path) -> CheckSection:
    s = CheckSection("Build", 20)
    result = _run_script(root, "build")
    if result is not None:
        if result.skipped:
            s.items.append(CheckItem("npm build", "skip", result.reason))
        else:
            detail = "build passed" if result.ok else (result.stderr or result.stdout or result.reason)[-800:]
            s.items.append(CheckItem("npm run build", "pass" if result.ok else "fail", detail, blocker=not result.ok))
        return s
    if (root / "pyproject.toml").exists():
        result = run([sys.executable, "-m", "compileall", "-q", "."], root)
        s.items.append(CheckItem("python compile", "pass" if result.ok else "fail", "compileall passed" if result.ok else (result.stderr or result.stdout)[-800:], blocker=not result.ok))
    else:
        s.items.append(CheckItem("build command", "skip", "no build script detected"))
    return s


def lint(root: Path) -> CheckSection:
    s = CheckSection("Lint", 10)
    scripts = _package_scripts(root)
    candidate = next((x for x in ["lint", "check", "typecheck"] if x in scripts), None)
    if candidate:
        result = _run_script(root, candidate)
        if result and not result.skipped:
            s.items.append(CheckItem(f"npm run {candidate}", "pass" if result.ok else "fail", "passed" if result.ok else (result.stderr or result.stdout)[-800:]))
        else:
            s.items.append(CheckItem(candidate, "skip", result.reason if result else "not available"))
    else:
        s.items.append(CheckItem("lint/typecheck", "skip", "no lint, check, or typecheck script detected"))
    return s


def tests(root: Path, project: dict | None) -> CheckSection:
    s = CheckSection("Tests", 25)
    scripts = _package_scripts(root)
    result = None
    label = ""
    if "test" in scripts:
        result = _run_script(root, "test")
        label = "npm test"
    elif (root / "pyproject.toml").exists() and any(root.rglob("test_*.py")):
        result = run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], root)
        label = "python unittest"
    if result:
        if result.skipped:
            s.items.append(CheckItem(label, "skip", result.reason))
        else:
            s.items.append(CheckItem(label, "pass" if result.ok else "fail", "test command passed" if result.ok else (result.stderr or result.stdout)[-1000:], blocker=not result.ok))
    else:
        s.items.append(CheckItem("test command", "fail", "no runnable test command detected", blocker=True))

    caps = (project or {}).get("capabilities", {})
    test_text = ""
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".js", ".jsx", ".ts", ".tsx"} and any(part.lower() in {"test", "tests", "__tests__"} or "test" in part.lower() for part in p.parts):
            try:
                if p.stat().st_size <= 500_000:
                    test_text += p.read_text(encoding="utf-8", errors="ignore").lower() + "\n"
            except OSError:
                pass
    if caps.get("multi_tenant"):
        present = any(k in test_text for k in ["tenant", "organization", "workspace", "isolation"])
        s.items.append(CheckItem("tenant isolation coverage", "pass" if present else "fail", "tenant-related test evidence found" if present else "multi-tenant project requires isolation test evidence", blocker=not present))
    if caps.get("rbac"):
        present = any(k in test_text for k in ["role", "permission", "unauthorized", "forbidden", "rbac"])
        s.items.append(CheckItem("authorization coverage", "pass" if present else "fail", "authorization test evidence found" if present else "RBAC project requires authorization test evidence", blocker=not present))
    return s


def _iter_text_files(root: Path):
    count = 0
    for p in root.rglob("*"):
        if count >= 2500:
            break
        if not p.is_file() or any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in TEXT_EXTS and p.name not in {".env", ".env.local", ".env.production"}:
            continue
        try:
            if p.stat().st_size > 1_000_000:
                continue
        except OSError:
            continue
        count += 1
        yield p


def security(root: Path, project: dict | None) -> CheckSection:
    s = CheckSection("Security", 25)
    gitignore = (root / ".gitignore").read_text(encoding="utf-8", errors="ignore") if (root / ".gitignore").exists() else ""
    env_files = [root / x for x in [".env", ".env.local", ".env.production"] if (root / x).exists()]
    if env_files:
        ignored = ".env" in gitignore or ".env*" in gitignore
        s.items.append(CheckItem("environment files ignored", "pass" if ignored else "fail", ".env ignore rule present" if ignored else "environment file exists without an obvious .gitignore rule", blocker=not ignored))
    else:
        s.items.append(CheckItem("environment files", "pass", "no root environment file detected"))

    findings = []
    for p in _iter_text_files(root):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if p.name.endswith(".example") or p.name == ".env.example":
            continue
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(f"{label} in {p.relative_to(root)}")
                if len(findings) >= 10:
                    break
        if len(findings) >= 10:
            break
    s.items.append(CheckItem("obvious secret scan", "fail" if findings else "pass", "; ".join(findings) if findings else "no high-confidence secret patterns found", blocker=bool(findings)))

    caps = (project or {}).get("capabilities", {})
    security_doc = root / ".shipkit" / "SECURITY.md"
    text = security_doc.read_text(encoding="utf-8", errors="ignore").lower() if security_doc.exists() else ""
    if caps.get("auth"):
        present = any(k in text for k in ["authentication", "auth", "session"])
        s.items.append(CheckItem("auth security plan", "pass" if present else "fail", "documented" if present else "authentication is required but not documented"))
    if caps.get("rbac"):
        present = any(k in text for k in ["authorization", "rbac", "role", "permission"])
        s.items.append(CheckItem("authorization plan", "pass" if present else "fail", "documented" if present else "RBAC is required but authorization is not documented"))
    return s


def documentation(root: Path, project: dict | None) -> CheckSection:
    s = CheckSection("Documentation", 10)
    expected = ["PROJECT.md", "REQUIREMENTS.md", "ARCHITECTURE.md", "SECURITY.md", "TESTING.md", "TASKS.md"]
    caps = (project or {}).get("capabilities", {})
    if caps.get("database"):
        expected.append("DATABASE.md")
    for name in expected:
        p = root / ".shipkit" / name
        if not p.exists():
            s.items.append(CheckItem(name, "fail", "missing"))
            continue
        text = p.read_text(encoding="utf-8", errors="ignore").strip()
        placeholder = "shipkit will" in text.lower() or len(text) < 80
        s.items.append(CheckItem(name, "fail" if placeholder else "pass", "exists but still looks like a placeholder" if placeholder else "documented"))
    return s


def state_check(root: Path, state: dict | None) -> CheckSection:
    s = CheckSection("ShipKit State", 10)
    if not state:
        s.items.append(CheckItem("state.json", "fail", "missing or invalid", blocker=True))
        return s
    s.items.append(CheckItem("state.json", "pass", f"phase={state.get('current_phase', 'unknown')}"))
    phases = state.get("phases", {})
    pending_before = []
    current = state.get("current_phase")
    order = ["discovery", "requirements", "architecture", "implementation", "testing", "security", "release"]
    if current in order:
        for phase in order[:order.index(current)]:
            if phases.get(phase) != "completed":
                pending_before.append(phase)
    s.items.append(CheckItem("phase consistency", "fail" if pending_before else "pass", f"incomplete prior phases: {', '.join(pending_before)}" if pending_before else "phase order consistent"))
    return s


def run_all(root: Path) -> dict:
    project, state = load(root)
    sections = [
        structure(root),
        build(root),
        lint(root),
        tests(root, project),
        security(root, project),
        documentation(root, project),
        state_check(root, state),
    ]
    raw = sum(s.score() for s in sections)
    max_score = sum(s.weight for s in sections)
    score = round(raw * 100 / max_score) if max_score else 0
    blockers = [f"{s.name}: {i.name} — {i.detail}" for s in sections for i in s.items if i.blocker and i.status == "fail"]
    return {
        "score": score,
        "status": "READY" if score >= 85 and not blockers else "NOT_READY",
        "blockers": blockers,
        "sections": [s.to_dict() for s in sections],
    }
