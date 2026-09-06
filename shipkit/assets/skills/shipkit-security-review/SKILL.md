---
name: shipkit-security-review
description: Perform the ShipKit security phase for projects that handle users, authorization, secrets, uploads, payments, multi-tenancy, or AI data boundaries. Review design and implementation, run deterministic checks, and create/fix actionable security issues.
---

# ShipKit Security Review

Use the project capabilities to scope the review. Do not produce generic security theater.

Review actual code/config for applicable areas:

- secret handling and `.gitignore`
- server/client trust boundary
- authentication lifecycle
- authorization/RBAC
- multi-tenant isolation
- input validation
- file upload validation/access
- payment signatures/idempotency
- dependency/runtime exposure
- AI prompt/data/tool boundaries
- unsafe error leakage

Run `shipkit check` and inspect its security/test findings. Deterministic failures outrank a model's opinion.

Do not declare security complete merely because `SECURITY.md` exists.

When required security controls and security tests are evidenced, run:

`shipkit phase security --status completed`
`shipkit phase release --status in_progress`

Then use `$shipkit-release-review`.
