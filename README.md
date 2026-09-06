# ShipKit

**Software Delivery Orchestrator for AI Coding Agents**

[![CI](https://github.com/DekrecJ/Shipkit/actions/workflows/ci.yml/badge.svg)](https://github.com/DekrecJ/Shipkit/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-informational)
![Status](https://img.shields.io/badge/status-alpha-orange)
![License](https://img.shields.io/badge/license-MIT-green)

ShipKit adds a repeatable software-delivery workflow to AI coding agents such as **Codex** and, experimentally, **Claude Code**.

> **ShipKit does not replace your coding agent. It gives your coding agent a software-delivery process.**

Instead of letting an agent jump directly from an idea to code, ShipKit guides the project through a structured lifecycle and verifies the real repository before calling it ready.

```text
Idea
  ↓
Discovery
  ↓
Requirements
  ↓
Architecture
  ↓
Implementation
  ↓
Testing
  ↓
Security Review
  ↓
Release
```

## Why ShipKit?

AI coding agents can generate code quickly, but projects still fail when engineering steps are skipped. ShipKit is designed to reduce problems such as:

- unclear requirements;
- unnecessary architecture;
- missing authorization;
- secrets committed to the repository;
- weak or missing tests;
- no persistent project state;
- incomplete documentation;
- agents declaring a project finished without actually building or testing it.

ShipKit separates model reasoning from deterministic verification:

```text
Codex / Claude
      │
      │ reasoning + implementation
      ▼
ShipKit Skills
      │
      │ workflow + rules + persistent state
      ▼
Repository
      │
      │ actual code + tests + documentation
      ▼
ShipKit CLI
      │
      │ deterministic verification
      ▼
READY / NOT_READY
```

## Features

ShipKit v0.1.0 includes:

- Codex integration through persistent instructions and agent skills;
- **7 ShipKit skills** covering routing, analysis, planning, implementation, testing, security, and release;
- persistent project state stored in `.shipkit/`;
- reusable project blueprints and capability rules;
- support for beginner, intermediate, and advanced workflows;
- deterministic build, test, security, structure, and documentation checks;
- project status tracking;
- release score from `0–100`;
- JSON output through `shipkit check --json`;
- Windows, Linux, and macOS installers;
- no ShipKit cloud account;
- no separate OpenAI or Anthropic API key required by ShipKit itself.

## Supported Project Types

| Type | Identifier | Example |
|---|---|---|
| Web application | `web_app` | Dashboard, expense tracker, internal tool |
| SaaS | `saas` | CRM, inventory system, business platform |
| API | `api` | REST API, backend service |
| Automation | `automation` | Processing workflow, webhook automation |
| AI application | `ai_app` | RAG app, document assistant, AI workflow |
| Mobile application | `mobile_app` | Flutter or React Native app |
| CLI tool | `cli_tool` | Developer utility, data-processing command |

## Installation

### Requirements

- Python **3.10+**
- Git
- Codex for the primary workflow

### Windows

```powershell
git clone https://github.com/DekrecJ/Shipkit.git
cd Shipkit
Set-ExecutionPolicy -Scope Process Bypass
.\install-codex.ps1
```

Restart Codex after installation.

### Linux / macOS

```bash
git clone https://github.com/DekrecJ/Shipkit.git
cd Shipkit
chmod +x install-codex.sh
./install-codex.sh
```

Restart Codex after installation.

### Manual installation

```bash
python -m pip install .
shipkit install codex
shipkit doctor
```

For more detail, see **[INSTALL.md](INSTALL.md)**.

## First Test

Create an empty project folder and open Codex:

```bash
mkdir workshop-flow
cd workshop-flow
codex
```

Then simply describe the project:

```text
Build a SaaS for automotive repair shops where mechanics update repair jobs
and customers can track the status of their vehicles.
```

When ShipKit activates, the workflow should begin with:

```text
◆ ShipKit active
```

If automatic activation does not happen, invoke the router explicitly:

```text
$shipkit-router Build a SaaS for automotive repair shops...
```

## Persistent Project State

A ShipKit-managed project receives:

```text
.shipkit/
├── project.json
├── state.json
├── PROJECT.md
├── REQUIREMENTS.md
├── ARCHITECTURE.md
├── DATABASE.md
├── SECURITY.md
├── TESTING.md
└── TASKS.md
```

This allows a new Codex session to resume work from repository state instead of depending on chat history.

## CLI

```bash
shipkit --version
shipkit install codex
shipkit install claude
shipkit init
shipkit status
shipkit check
shipkit check --json
shipkit doctor
```

Example:

```bash
shipkit status
```

```text
SHIPKIT STATUS
Project: WorkshopFlow
Type: saas
Progress: ███████████░░░░░░░░░ 57%
Current phase: implementation
```

Before release:

```bash
shipkit check
```

ShipKit checks the actual repository and returns a deterministic result such as:

```text
SHIPKIT CHECK

Build          ✓
Tests          ✓
Security       ✗
Documentation ✓

Score: 82/100
Status: NOT_READY
```

## Included Skills

```text
skills/
├── shipkit-router/
├── shipkit-project-analyzer/
├── shipkit-project-planner/
├── shipkit-implementation/
├── shipkit-testing-review/
├── shipkit-security-review/
└── shipkit-release-review/
```

The coding agent remains the reasoning engine. ShipKit supplies the workflow and controls.

## Repository Structure

```text
Shipkit/
├── .github/workflows/      # CI
├── blueprints/             # Project-type rules
├── capabilities/           # Auth, DB, RBAC, AI, storage, etc.
├── examples/               # Example project scenarios
├── shipkit/                # Python CLI and packaged assets
│   ├── checks/
│   ├── installer/
│   ├── state/
│   ├── utils/
│   └── assets/
├── skills/                 # Human-readable ShipKit skills
├── templates/              # Generated project documents
├── tests/                  # Automated test suite
├── ARCHITECTURE.md
├── INSTALL.md
├── CONTRIBUTING.md
├── TEST_REPORT.md
├── install-codex.ps1
├── install-codex.sh
└── pyproject.toml
```

## Design Principle

ShipKit follows one central rule:

> **The model may reason about the project, but readiness must be verified against the actual repository.**

That means Codex/Claude can interpret requirements and write software, while ShipKit maintains project state and runs deterministic checks against the files, tests, build commands, security evidence, and documentation.

## Development

Install locally in editable mode:

```bash
python -m pip install -e .
```

Run tests:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

The included test suite currently validates project scaffolding, persistent state, skill metadata, and release-check behavior.

## Current Status

**v0.1.0 — Alpha**

ShipKit currently focuses on Codex. Claude Code support is experimental. It does not contain its own LLM, does not guarantee production readiness, and does not replace professional security review or penetration testing.

See **[ARCHITECTURE.md](ARCHITECTURE.md)** for the internal design and **[TEST_REPORT.md](TEST_REPORT.md)** for validation notes.

## Roadmap

Planned directions include:

- deeper Codex integration;
- additional agent adapters;
- richer deterministic security checks;
- GitHub pull-request and CI awareness;
- additional project blueprints;
- architecture-change records;
- optional visual project status tooling.

## Contributing

Contributions are welcome. See **[CONTRIBUTING.md](CONTRIBUTING.md)**.

## License

MIT — see **[LICENSE](LICENSE)**.
