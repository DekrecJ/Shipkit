# ShipKit installation

## Windows

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install-codex.ps1
```

The script installs the local Python package, installs ShipKit Codex skills/instructions, and runs `shipkit doctor`.

Restart Codex after installation so a new session discovers the skills.

## Linux/macOS

```bash
chmod +x install-codex.sh
./install-codex.sh
```

## Verify inside Codex

Start a new task and type:

```text
Use $shipkit-router and report the current ShipKit status.
```

For an automatic activation test, start in an empty project directory and say:

```text
Create a SaaS where mechanics update repairs and customers track their vehicles.
```

A correct ShipKit flow begins with `◆ ShipKit active` (or `resumed` when `.shipkit/` already exists).

## Remove

```bash
shipkit uninstall codex
python -m pip uninstall shipkit-ai
```
