# NEXTBASE_SYSTEM_CANONICAL

STATE: CANONICAL_OK

This file is the system canonical law for NextBase API gateway enforcement.

- All AI-bound traffic must be prefixed with the merged canonical context at the gateway.
- No client may bypass the gateway for production traffic.

## Internal note

Operational blocks must use explicit NORI approval in inventory only; do not insert audit failure markers into this file except via controlled release process.
