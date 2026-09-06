---
name: shipkit-project-planner
description: Convert a ShipKit project analysis into testable requirements, an appropriately simple architecture, data model when needed, security plan, test strategy, and ordered implementation tasks. Use after Discovery or when project architecture materially changes.
---

# ShipKit Project Planner

## Inputs
Read every relevant file in `.shipkit/`, especially `project.json` and `PROJECT.md`. Consult ShipKit blueprints/capabilities under `~/.shipkit/library/` if present.

## 1. Requirements
Rewrite `REQUIREMENTS.md` using stable IDs. Every requirement must include acceptance criteria. Distinguish MVP from later work.

## 2. Architecture
Rewrite `ARCHITECTURE.md` with:

- component/data-flow diagram (Mermaid or ASCII)
- chosen stack and why
- deployment shape
- external integrations
- explicit rejected complexity (technologies not justified)
- failure boundaries and important tradeoffs

Do not choose a technology solely because it is popular. Prefer boring, maintainable defaults appropriate to the developer's level.

## 3. Database
If `capabilities.database=true`, rewrite `DATABASE.md` with entities, ownership, relationships, indexes, migration approach, and authorization boundaries. If false, explain briefly why a DB is intentionally absent.

## 4. Security
Rewrite `SECURITY.md`. Make controls proportional to capabilities. Multi-role and multi-tenant systems require concrete authorization/isolation design, not just authentication.

## 5. Testing
Rewrite `TESTING.md`. Use the smallest set that provides confidence. Require authorization/isolation tests when relevant; require AI evaluation when AI is relevant.

## 6. Tasks
Rewrite `TASKS.md` as ordered vertical slices. Each task needs:

- ID
- goal
- dependencies
- acceptance criteria
- verification evidence/command

Avoid one enormous “build frontend/backend” task.

## Finish planning
Run:

`shipkit phase architecture --status completed`
`shipkit phase implementation --status in_progress`

Then hand off to `$shipkit-implementation`.
