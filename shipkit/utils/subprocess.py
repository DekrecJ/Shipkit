from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CommandResult:
    command: list[str]
    returncode: int | None
    stdout: str
    stderr: str
    skipped: bool = False
    reason: str = ""

    @property
    def ok(self) -> bool:
        return not self.skipped and self.returncode == 0


def executable(name: str) -> str | None:
    return shutil.which(name)


def run(command: list[str], cwd: Path, timeout: int = 180) -> CommandResult:
    if not command:
        return CommandResult([], None, "", "", True, "empty command")
    if not executable(command[0]):
        return CommandResult(command, None, "", "", True, f"{command[0]} not found")
    try:
        proc = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            errors="replace",
        )
        return CommandResult(command, proc.returncode, proc.stdout[-8000:], proc.stderr[-8000:])
    except subprocess.TimeoutExpired as exc:
        return CommandResult(command, None, (exc.stdout or "")[-8000:], (exc.stderr or "")[-8000:], False, f"timeout after {timeout}s")
