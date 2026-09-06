# ShipKit project: {{PROJECT_NAME}}

This repository uses ShipKit. Before substantial implementation work:

1. Read `.shipkit/project.json` and `.shipkit/state.json`.
2. Read the relevant `.shipkit/*.md` planning documents.
3. Resume the current phase/task rather than recreating the project plan.
4. Implement in small vertical slices tied to acceptance criteria.
5. Run project tests/build/lint after meaningful changes.
6. Update ShipKit state and task documentation when work advances.
7. Before declaring the project ready, run `shipkit check` and address blocking failures.

Do not add infrastructure, frameworks, databases, authentication, AI, queues, caching, or other complexity unless the project requirements justify them.
