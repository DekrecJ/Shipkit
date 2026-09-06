<h1 align="center">ShipKit</h1>

<p align="center">
  <strong>Software delivery orchestration for AI coding agents.</strong><br/>
  Give Codex and Claude Code a lifecycle, persistent state and quality gates instead of an unstructured chat loop.
</p>

<p align="center">
  <a href="https://github.com/DekrecJ/Shipkit/actions/workflows/ci.yml"><img src="https://github.com/DekrecJ/Shipkit/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-111111?logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/version-0.2.0-111111" alt="v0.2.0" />
  <img src="https://img.shields.io/badge/license-MIT-111111" alt="MIT" />
</p>

---

## Why ShipKit exists

AI coding agents are good at producing code, but a long software project needs more than code generation: requirements, state, checkpoints, tests, security checks and an explicit definition of "ready".

**ShipKit does not replace the coding agent.** It gives the agent a delivery system around the work.

```text
DISCOVERY → REQUIREMENTS → ARCHITECTURE → IMPLEMENTATION → TESTING → SECURITY → RELEASE
```

At each stage ShipKit can persist state, validate the current phase and prevent accidental advancement when required evidence is missing.

## Core capabilities

- **Persistent project state** with atomic writes and backups.
- **Explicit lifecycle phases** instead of relying on chat history.
- **Guarded advancement** through phase validation.
- **Quality scoring** with `READY`, `REVIEW` and `NOT_READY` outcomes.
- **Versioned state/project schemas** with migration support.
- **Versioned skill manifests** for agent integrations.
- **Repair and doctor commands** for recovering or inspecting an installation.
- **Codex and Claude Code installers** from the same CLI.
- **CI verification** across Python 3.10, 3.11 and 3.12.

## Quick start

### 1. Install

```bash
git clone https://github.com/DekrecJ/Shipkit.git
cd Shipkit
python -m pip install .
```

### 2. Install ShipKit for your coding agent

```bash
shipkit install codex
```

or:

```bash
shipkit install claude
```

### 3. Initialize a project

```bash
cd /path/to/your/project
shipkit init --type web --level intermediate
shipkit status
```

### 4. Work through the lifecycle

```bash
shipkit validate-phase
shipkit advance
shipkit check
```

Typical maintenance commands:

```bash
shipkit doctor --project
shipkit repair
shipkit migrate
```

Run `shipkit --help` for the complete CLI.

## How it fits around an AI coding agent

```text
┌─────────────────────┐
│  Codex / Claude     │
│  coding agent       │
└──────────┬──────────┘
           │ reads / writes
           ▼
┌─────────────────────┐
│       ShipKit       │
│                     │
│ lifecycle           │
│ persistent state    │
│ validation gates    │
│ quality checks      │
│ recovery tooling    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Your repository     │
│ code · tests · docs │
└─────────────────────┘
```

## Repository map

| Area | Purpose |
| --- | --- |
| `shipkit/` | Python package and CLI |
| `shipkit/state/` | state lifecycle, migrations and persistence |
| `shipkit/checks/` | repository quality checks and scoring |
| `shipkit/installer/` | Codex / Claude installation logic |
| `blueprints/` | reusable project blueprints |
| `capabilities/` | capability definitions |
| `examples/` | example usage and project material |
| `docs/` | deeper integration, execution and recovery documentation |
| `tests/` | automated test suite |

## Documentation

- [Architecture](./ARCHITECTURE.md)
- [Installation](./INSTALL.md)
- [Changelog](./CHANGELOG.md)
- [Test report](./TEST_REPORT.md)
- [Contributing](./CONTRIBUTING.md)
- [Full docs](./docs/)

## Verification

The GitHub Actions workflow installs ShipKit and runs the unit test suite on **Python 3.10, 3.11 and 3.12**, then verifies the CLI version command.

Local verification:

```bash
python -m unittest discover -s tests -v
python -m shipkit --version
```

## Design principle

> The agent can write the code. ShipKit makes the delivery process explicit, inspectable and repeatable.

## License

MIT — see [LICENSE](./LICENSE).
