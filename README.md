# ShipKit

**Software Delivery Orchestrator for AI Coding Agents**

ShipKit v0.2.0 gives Codex and Claude Code a structured software-delivery lifecycle with persistent state and repository-based quality gates.

> ShipKit does not replace the coding agent. It supplies process, state, contracts and verification.

## v0.2.0 highlights
- atomic state writes with backups;
- explicit state/project schemas and migration;
- phase validation and guarded advancement;
- versioned scoring with READY / REVIEW / NOT_READY;
- versioned skill manifests;
- repair and project doctor commands.

## Install
```bash
git clone https://github.com/DekrecJ/Shipkit.git
cd Shipkit
python -m pip install .
shipkit install codex
```

## Lifecycle
Discovery → Requirements → Architecture → Implementation → Testing → Security → Release

Use `shipkit validate-phase`, `shipkit advance`, `shipkit check`, `shipkit repair`, and `shipkit migrate`.

See `docs/` for integration, execution, scoring, schemas, skills and recovery.
