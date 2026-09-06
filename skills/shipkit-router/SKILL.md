---
name: shipkit-router
description: Use when the user wants to create, start, plan, architect, scaffold, or substantially restructure a software project (web app, SaaS, API, automation, AI app, mobile app, or CLI). It activates or resumes the ShipKit lifecycle, selects the next ShipKit skill, and preserves project state. Do not use for tiny isolated fixes or simple coding questions unless ShipKit is explicitly requested.
---

# ShipKit Router

ShipKit is a software-delivery process layered on the current coding agent. You are still the coding agent; ShipKit supplies the workflow, project state, and verification gates.

## Activation

When this skill is relevant:

1. Look for `.shipkit/state.json` in the current repository.
2. If it exists, print `◆ ShipKit resumed`, read `.shipkit/project.json`, `.shipkit/state.json`, and relevant `.shipkit/*.md`, then continue the current phase.
3. If it does not exist, print `◆ ShipKit active`, run `shipkit init --name <reasonable-project-name>` in the intended project root, then use `$shipkit-project-analyzer`.
4. Resolve the CLI in this order: `shipkit`, then `python -m shipkit`, then on Windows `py -3 -m shipkit`. If all fail, explain that ShipKit is not installed correctly and point to the installer/doctor; do not fake ShipKit state.

## Phase routing

- discovery → `$shipkit-project-analyzer`
- requirements or architecture → `$shipkit-project-planner`
- implementation → `$shipkit-implementation`
- testing → `$shipkit-testing-review`
- security → `$shipkit-security-review`
- release → `$shipkit-release-review`

## Rules

- Prefer the simplest architecture that satisfies explicit requirements.
- Separate required, recommended, optional, and rejected complexity.
- Do not call a project production-ready based only on model judgment.
- Persist important decisions to `.shipkit/`; do not depend on chat memory.
- Keep questions minimal. Ask only when a missing answer materially changes architecture, security, or project scope.
