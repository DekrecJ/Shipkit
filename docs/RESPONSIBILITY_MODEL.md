# Responsibility Model

## Codex / Claude
Interpret intent, reason about architecture, generate code and documentation.

## ShipKit skills
Provide workflow instructions only. They do not independently prove correctness.

## ShipKit CLI
Owns persistent state, guarded phase transitions, migrations, repository checks and release status.

## Repository
Contains the code, tests, docs and evidence being evaluated.
