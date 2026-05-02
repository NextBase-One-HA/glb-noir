# SYSTEM_INVENTORY

STATE: INVENTORY_OK

Inventory reference for gateway HOLD checks. Services and keys are named only; secrets are never stored in-repo.

## Routing

- **nextbase-api** — mandatory canonical injection + `/gateway`
- **ai-router** — upstream LLM routing (address via `TRANSLATE_UPSTREAM_URL` only in deployment env)

## Operations

Rotations and env updates are done out-of-band; gateway reads this file each request (no reliance on remote chat history). Audit failure markers are documented only in ops runbooks, not in free text that could false-trigger automation.
