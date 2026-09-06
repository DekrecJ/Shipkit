# ShipKit v0.1.0 validation report

Validated before publication on 2026-09-05/06.

## Automated tests

- State initialization / phase progression / task persistence: **PASS**
- Project scaffolding and AGENTS.md creation: **PASS**
- Deterministic `shipkit check` smoke test: **PASS**
- Skill frontmatter validation for all seven skills: **PASS**

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

Result: **4/4 tests passed**.

## Installation smoke test

A clean local installation was validated with the ShipKit package and isolated Codex directories. `shipkit install codex` successfully:

- installed 7 `shipkit-*` skills under the personal skills directory;
- created a managed ShipKit block in Codex `AGENTS.md`;
- copied the blueprint/capability/template library;
- initialized a new project with `.shipkit/project.json` and `.shipkit/state.json`;
- returned the expected `NOT_READY` result from `shipkit check` for an intentionally incomplete project.

## Important boundary

The deterministic CLI can validate repository state, build/test commands and defined checks. Natural-language project interpretation and automatic skill activation are performed by the installed coding agent (for example Codex) using ShipKit's instructions and skills.
