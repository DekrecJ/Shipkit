# Execution Model

1. `shipkit install codex` installs skills and persistent Codex bootstrap instructions.
2. `$shipkit-router` activates/resumes when a project is created or substantially restructured.
3. `shipkit init` creates `.shipkit/project.json`, `.shipkit/state.json` and lifecycle docs.
4. The agent works within the current phase.
5. `shipkit validate-phase` checks explicit exit criteria.
6. `shipkit advance` refuses invalid transitions unless `--force` is used; forced transitions record lifecycle debt.
7. `shipkit check` evaluates the actual repository before release.
