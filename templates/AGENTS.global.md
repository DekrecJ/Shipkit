# ShipKit bootstrap for Codex

ShipKit is an installed software-delivery workflow. Its skills are discoverable as `shipkit-*` skills.

Use `$shipkit-router` automatically when the user asks to create, start, architect, plan, or substantially restructure a software project such as a web app, SaaS, API, automation, AI application, mobile application, or CLI tool. Do not invoke ShipKit for isolated syntax questions, tiny bug fixes, explanations, or one-off snippets unless the user explicitly asks for ShipKit.

When a repository contains `.shipkit/`, treat `.shipkit/project.json`, `.shipkit/state.json`, and the Markdown documents inside `.shipkit/` as the persistent ShipKit project record. Resume from those files in new sessions instead of relying on chat history.

When ShipKit is active, show a compact `◆ ShipKit active` or `◆ ShipKit resumed` indicator near the start of the response. Use the ShipKit skills and deterministic `shipkit` CLI checks rather than claiming a phase is complete without evidence.
CLI resolution: prefer `shipkit ...`. If that command is not on PATH, use `python -m shipkit ...` (or `py -3 -m shipkit ...` on Windows). Do not treat a missing console-script PATH entry as a missing ShipKit installation until these fallbacks are checked.
