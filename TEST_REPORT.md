# ShipKit v0.1.0 validation report

Validated before packaging on 2026-09-05/06.

## Automated tests

- State initialization / phase progression / task persistence: PASS
- Project scaffolding and AGENTS.md creation: PASS
- Deterministic `shipkit check` smoke test: PASS
- Skill frontmatter validation for all seven skills: PASS

`python -m unittest discover -s tests -v` → **4/4 passed**.

## Clean-install smoke test

A fresh Python virtual environment installed the bundled wheel without source build dependencies. In an isolated HOME/CODEX_HOME, `shipkit install codex` successfully:

- installed 7 `shipkit-*` skills under the personal skills directory;
- created a managed ShipKit block in Codex `AGENTS.md`;
- copied the blueprint/capability/template library;
- initialized a new project with `.shipkit/project.json` and `.shipkit/state.json`;
- returned expected `NOT_READY` from `shipkit check` for an intentionally empty project.

The final end-to-end natural-language behavior still depends on the Codex version/model discovering and applying installed skills, as expected for an agent-skill package.
