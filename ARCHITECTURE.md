# ShipKit architecture

ShipKit deliberately separates model reasoning from deterministic verification.

```text
User intent
   ↓
Codex / Claude (the model + coding agent)
   ↓ loads
ShipKit skills
   ↓ writes
.shipkit project record
   ↓ drives
Implementation by coding agent
   ↓
ShipKit CLI checks actual repository
   ↓
READY / NOT_READY
```

The skills perform natural-language interpretation because they run inside Codex/Claude. The CLI never pretends to understand free-form intent; it manages state, installation, and mechanical checks.
