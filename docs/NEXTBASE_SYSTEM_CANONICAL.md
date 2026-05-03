# NEXTBASE_SYSTEM_CANONICAL

STATE: CANONICAL_OK

This file is the system canonical law for NextBase API gateway enforcement.

- All AI-bound traffic must be prefixed with the merged canonical context at the gateway.
- No client may bypass the gateway for production traffic.
- AI memory is not trusted as system state. External canonical, inventory, session, room, and evidence state must be injected by the gateway.

## Agent evidence rule

AI, Gemini, Cursor, and any agent must not declare DONE from language alone.

DONE is valid only when the NextBase OS evidence gate has verified all required physical evidence:

- git_commit
- deploy_revision
- test_command
- test_response

If any required evidence is missing, incomplete, unverifiable, or inconsistent, the task status must remain HOLD with securityLevel = 1.

The physical source of truth for agent completion is the agent_tasks ledger exposed by nextbase-api:

- POST /agent/task/start
- POST /agent/task/finish
- GET /agent/task/{task_id}
- GET /agent/tasks/open

Canonical DONE formula:

DONE = git_commit + deploy_revision + test_command + test_response

Missing evidence = HOLD.

## Internal note

Operational blocks must use explicit NORI approval in inventory only; do not insert audit failure markers into this file except via controlled release process.
