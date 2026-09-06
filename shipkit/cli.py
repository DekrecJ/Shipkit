from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from shipkit import __version__
from shipkit.constants import LEVELS, PROJECT_TYPES, PHASES
from shipkit.state.manager import initialize, load, update_phase, update_task
from shipkit.project_setup import scaffold_project
from shipkit.checks.runner import run_all
from shipkit.installer import codex as codex_installer
from shipkit.installer import claude as claude_installer


def _root(value: str | None) -> Path:
    return Path(value or ".").resolve()


def cmd_install(args):
    if args.target == "codex":
        result = codex_installer.install()
        print(f"ShipKit {__version__} installed for Codex")
        print(f"  Skills: {result['skills_home']}")
        print(f"  Codex instructions: {result['codex_home']}/AGENTS.md")
        print(f"  Library: {result['library']}")
        print("\nRestart Codex, then describe a new software project. You can also invoke $shipkit-router explicitly.")
    elif args.target == "claude":
        result = claude_installer.install()
        print(f"ShipKit {__version__} skills installed for Claude Code")
        print(f"  Skills: {result['skills_home']}")


def cmd_uninstall(args):
    if args.target != "codex":
        print("Uninstall is currently implemented for Codex only.", file=sys.stderr)
        return 2
    result = codex_installer.uninstall()
    print("ShipKit Codex integration removed.")
    print(f"Removed skill directories: {len(result['removed'])}")


def cmd_init(args):
    root = _root(args.path)
    name = args.name or root.name
    try:
        initialize(root, name, args.type, args.level, force=args.force)
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    scaffold_project(root, name)
    print(f"◆ ShipKit initialized: {name}")
    print(f"  Project metadata: {root / '.shipkit' / 'project.json'}")
    print(f"  State: {root / '.shipkit' / 'state.json'}")
    print("  Next: ask Codex to analyze the project with $shipkit-project-analyzer, or simply describe what you want to build.")


def _bar(percent: int, width: int = 20) -> str:
    filled = max(0, min(width, round(percent / 100 * width)))
    return "█" * filled + "░" * (width - filled)


def cmd_status(args):
    root = _root(args.path)
    project, state = load(root)
    if not project or not state:
        print("No ShipKit project found. Run: shipkit init", file=sys.stderr)
        return 2
    phase_values = list(state.get("phases", {}).values())
    completed = sum(v == "completed" for v in phase_values)
    progress = round(completed / len(PHASES) * 100) if PHASES else 0
    print("SHIPKIT STATUS")
    print(f"Project: {project.get('name')}")
    print(f"Type: {project.get('type')}")
    print(f"Level: {project.get('level')}")
    print(f"Progress: {_bar(progress)} {progress}%")
    print(f"Current phase: {state.get('current_phase')}")
    if state.get("current_task"):
        print(f"Current task: {state['current_task']}")
    print("")
    symbols = {"completed": "✓", "in_progress": "◐", "pending": "○", "blocked": "✗"}
    for phase in PHASES:
        status = state.get("phases", {}).get(phase, "pending")
        print(f"{symbols.get(status, '?')} {phase:<15} {status}")


def cmd_phase(args):
    root = _root(args.path)
    try:
        state = update_phase(root, args.phase, args.status)
    except (ValueError, FileNotFoundError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"ShipKit phase updated: {args.phase} -> {args.status}")
    print(f"Current phase: {state['current_phase']}")


def cmd_task(args):
    root = _root(args.path)
    try:
        state = update_task(root, args.task_id, args.status)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"ShipKit task updated: {args.task_id} -> {args.status}")
    print(f"Current task: {state.get('current_task') or '-'}")


def _print_check(result: dict):
    icons = {"pass": "✓", "fail": "✗", "warn": "!", "skip": "○"}
    print("SHIPKIT CHECK")
    print("=" * 54)
    for section in result["sections"]:
        print(f"\n{section['name']} [{section['score']}/{section['weight']}]")
        for item in section["items"]:
            icon = icons.get(item["status"], "?")
            detail = f" — {item['detail']}" if item.get("detail") else ""
            print(f"  {icon} {item['name']}{detail}")
    print("\n" + "=" * 54)
    print(f"Score: {result['score']}/100")
    print(f"Status: {result['status']}")
    if result["blockers"]:
        print("\nBlockers:")
        for b in result["blockers"]:
            print(f"  - {b}")


def cmd_check(args):
    root = _root(args.path)
    result = run_all(root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        _print_check(result)
    return 0 if result["status"] == "READY" else 1


def cmd_doctor(args):
    tools = ["git", "codex", "node", "npm", "docker"]
    print(f"SHIPKIT DOCTOR {__version__}")
    print(f"Python: {sys.version.split()[0]} ✓")
    for tool in tools:
        path = shutil.which(tool)
        required = tool in {"git", "codex"}
        icon = "✓" if path else ("✗" if required else "○")
        note = path or ("required for primary Codex workflow" if required else "optional / project-dependent")
        print(f"{icon} {tool:<8} {note}")
    print(f"Codex home: {codex_installer.codex_home()}")
    print(f"Skill home: {codex_installer.skills_home()}")


def build_parser():
    p = argparse.ArgumentParser(prog="shipkit", description="Software delivery orchestrator for AI coding agents")
    p.add_argument("--version", action="version", version=f"ShipKit {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("install", help="Install ShipKit integration for an agent")
    sp.add_argument("target", choices=["codex", "claude"])
    sp.set_defaults(func=cmd_install)

    sp = sub.add_parser("uninstall", help="Remove ShipKit integration")
    sp.add_argument("target", choices=["codex"])
    sp.set_defaults(func=cmd_uninstall)

    sp = sub.add_parser("init", help="Initialize ShipKit metadata in a project")
    sp.add_argument("--path", default=".")
    sp.add_argument("--name")
    sp.add_argument("--type", choices=PROJECT_TYPES, default="unknown")
    sp.add_argument("--level", choices=LEVELS, default="intermediate")
    sp.add_argument("--force", action="store_true")
    sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("status", help="Show ShipKit project state")
    sp.add_argument("--path", default=".")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("phase", help="Update current project phase")
    sp.add_argument("phase", choices=PHASES)
    sp.add_argument("--status", choices=["pending", "in_progress", "completed", "blocked"], default="in_progress")
    sp.add_argument("--path", default=".")
    sp.set_defaults(func=cmd_phase)

    sp = sub.add_parser("task", help="Update current task state")
    sp.add_argument("task_id")
    sp.add_argument("--status", choices=["in_progress", "completed", "blocked"], default="in_progress")
    sp.add_argument("--path", default=".")
    sp.set_defaults(func=cmd_task)

    sp = sub.add_parser("check", help="Run deterministic release checks")
    sp.add_argument("--path", default=".")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_check)

    sp = sub.add_parser("doctor", help="Check local prerequisites")
    sp.set_defaults(func=cmd_doctor)
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    result = args.func(args)
    return int(result or 0)
