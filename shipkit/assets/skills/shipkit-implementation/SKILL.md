---
name: shipkit-implementation
description: Implement an already-planned ShipKit software project task by task. Use when .shipkit/state.json is in implementation, preserving architecture, acceptance criteria, tests, and project state instead of free-form coding.
---

# ShipKit Implementation

Read `.shipkit/TASKS.md`, requirements, architecture, security, testing, project JSON, and state before editing code.

## Work loop

1. Select the next uncompleted task whose dependencies are satisfied.
2. State the task ID briefly and run `shipkit task <TASK-ID> --status in_progress`.
3. Implement the smallest complete vertical slice.
4. Add/update tests required by that task.
5. Run the narrowest useful verification, then broader build/test/lint when the slice is complete.
6. Mark the task complete in `TASKS.md` only when acceptance evidence exists, then run `shipkit task <TASK-ID> --status completed`.
7. Keep `.shipkit/state.json` current; do not rewrite completed planning unless implementation exposes a real architectural contradiction.
8. If architecture must change, record the reason in `ARCHITECTURE.md` before broad refactoring.

## Guardrails

- Never commit secrets or hard-code production credentials.
- Do not add dependencies without justification.
- Do not silently weaken tests or security controls to make checks pass.
- Do not claim completion while required tasks remain.

When implementation tasks are complete, run `shipkit phase testing --status in_progress` and use `$shipkit-testing-review`.
