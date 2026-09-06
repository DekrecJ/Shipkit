---
name: shipkit-testing-review
description: Review and execute the ShipKit test strategy after implementation or after meaningful behavioral changes. Checks whether tests map to requirements and required authorization, tenant-isolation, payment, or AI-evaluation risks.
---

# ShipKit Testing Review

Read `TESTING.md`, `REQUIREMENTS.md`, `project.json`, and the actual test suite.

1. Map critical acceptance criteria to concrete tests.
2. Run available tests; do not infer pass status from source inspection alone.
3. For RBAC, require tests demonstrating denied access as well as allowed access.
4. For multi-tenancy, require cross-tenant isolation tests.
5. For payment flows, require failure, signature, and idempotency behavior when applicable.
6. For AI features, verify retrieval/tool/prompt fallback or evaluation cases appropriate to the feature.
7. Fix missing high-value tests without creating redundant test bloat.

When meaningful test requirements pass, run `shipkit phase testing --status completed` and `shipkit phase security --status in_progress`, then use `$shipkit-security-review`.
