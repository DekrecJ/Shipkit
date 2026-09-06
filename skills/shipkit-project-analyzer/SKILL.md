---
name: shipkit-project-analyzer
description: Analyze a user's software idea during ShipKit Discovery. Classify the project, users, roles, capabilities, constraints, complexity, and MVP; write the structured result to .shipkit/project.json and PROJECT.md without starting implementation.
---

# ShipKit Project Analyzer

Turn the user's natural-language idea into explicit project intent.

## Read first

- `.shipkit/project.json`
- `.shipkit/state.json`
- `~/.shipkit/library/blueprints/` when available
- `~/.shipkit/library/capabilities/` when available

## Required analysis

Determine:

- project name and one of: `web_app`, `saas`, `api`, `automation`, `ai_app`, `mobile_app`, `cli_tool`
- user level: beginner, intermediate, advanced (use existing value unless user says otherwise)
- problem and desired outcome
- primary users and roles
- core MVP features
- platforms
- whether data persistence is required
- capabilities: auth, database, rbac, multi_tenant, storage, notifications, payments, realtime, ai
- constraints and explicit non-goals
- complexity: low, medium, high

## Deterministic implications

Use these rules unless the requirements justify an exception:

- accounts/users → authentication is required
- multiple permission levels → RBAC/authorization is required
- multi-tenant SaaS → tenant isolation is required
- persistent relational business data → database is required
- user uploads → storage + upload validation are required
- payments → server-side secrets + signature verification + idempotency tests are required
- AI/RAG → AI evaluation + prompt/data boundary review are required

Do not add capabilities merely because they are common.

## Outputs

Update `.shipkit/project.json` with valid JSON. Preserve the schema keys created by `shipkit init`.

Rewrite `.shipkit/PROJECT.md` with:

1. Problem
2. Users
3. MVP Scope
4. Non-goals
5. Constraints
6. Success criteria
7. Detected capabilities
8. Open decisions (only material unresolved items)

Then run:

`shipkit phase requirements --status in_progress`

and hand off to `$shipkit-project-planner`.
