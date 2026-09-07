# Install ShipKit v0.2.0

ShipKit is designed to be installed once and then used from Codex or Claude Code across your projects.

## Requirements

Before installing ShipKit, install:

- Python 3.10+
- Git
- Codex for the primary workflow

ShipKit does not require an additional API key or its own LLM.

## Windows — recommended

Open PowerShell:

```powershell
git clone https://github.com/DekrecJ/Shipkit.git
cd Shipkit
.\install-codex.ps1
```

If PowerShell blocks scripts:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install-codex.ps1
```

The script installs ShipKit, installs the Codex skills, configures persistent instructions and runs `shipkit doctor`.

Restart Codex after installation.

## Linux / macOS — recommended

```bash
git clone https://github.com/DekrecJ/Shipkit.git
cd Shipkit
chmod +x install-codex.sh
./install-codex.sh
```

Restart Codex after installation.

## Verify

```bash
shipkit --version
shipkit doctor
```

Expected:

```text
ShipKit 0.2.0
```

## First project

Move to your project folder:

```bash
cd /path/to/your/project
shipkit init --type web_app --level intermediate
shipkit status
```

Then open the folder with Codex and describe what you want to build.

## Manual installation

Use this only if you do not want to use the provided installer scripts:

```bash
git clone https://github.com/DekrecJ/Shipkit.git
cd Shipkit
python -m pip install .
shipkit install codex
shipkit doctor
```

For Claude Code:

```bash
shipkit install claude
```

## What the Codex installer changes

The Codex installer:

1. Copies `shipkit-*` skills to `~/.agents/skills`.
2. Adds a managed ShipKit block to `~/.codex/AGENTS.md`.
3. Copies reusable blueprints, capabilities, specs, schemas and templates to `~/.shipkit/library`.
4. Leaves project-specific state inside each project's `.shipkit/` directory.

It does not install another AI model and does not require a second API account.

## Useful commands

```bash
shipkit --help
shipkit status
shipkit validate-phase
shipkit advance
shipkit check
shipkit doctor --project
shipkit repair
shipkit migrate
```
