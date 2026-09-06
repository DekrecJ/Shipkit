# ShipKit example scenarios

Use these to validate that the router/planner adapts rather than applying one fixed template.

## Beginner — Expense tracker
Prompt: `Build a personal expense tracker that works in my browser.`
Expected bias: local-first web app; no auth/database/backend unless requested.

## Intermediate — Workshop SaaS
Prompt: `Build a SaaS for repair shops where mechanics update jobs and customers track vehicles.`
Expected capabilities: auth, database, roles/RBAC, likely notifications; if multiple shops share one deployment, multi-tenancy and isolation tests.

## AI — Document Q&A
Prompt: `Companies upload PDFs and ask questions about their own documents.`
Expected capabilities: auth, storage, database, tenant isolation, AI/RAG boundary, retrieval/evaluation and file-access controls.
