---
name: shipkit-release-review
description: Final ShipKit release gate. Use when implementation, testing, and security are complete. Runs shipkit check, validates remaining tasks/docs/deployment assumptions, and refuses to label the project ready while deterministic blockers remain.
---

# ShipKit Release Review

1. Read `.shipkit/state.json`, `TASKS.md`, and deployment-relevant documentation.
2. Run `shipkit check` from the project root.
3. Treat deterministic blockers as blockers. Do not override them with prose.
4. Confirm there are no required implementation tasks still open.
5. Report READY only if `shipkit check` returns READY and no known requirement remains unimplemented.
6. If not ready, fix actionable blockers when in scope and rerun the check.
7. If ready, run `shipkit phase release --status completed` and summarize evidence (build, tests, security, docs) concisely.

Never equate “demo works” with “release ready” when the planned quality gates are not satisfied.
