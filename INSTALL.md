# Install ShipKit v0.2.0

Requirements: Python 3.10+, Git, and Codex for the primary workflow.

```bash
python -m pip install .
shipkit install codex
shipkit doctor
```

The Codex installer copies `shipkit-*` skills to `~/.agents/skills`, writes a managed ShipKit block to `~/.codex/AGENTS.md`, and stores reusable blueprints/capabilities/specs/schemas in `~/.shipkit/library`.
