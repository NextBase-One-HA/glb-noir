# TOMORI ZERO TRUST GATE

## Purpose
Stop unchecked assumptions before NextBase work continues.
This file is a physical gate, not a conversation promise.

## Rule
Trust nothing until checked.

## Mandatory order
1. STATE
2. GOAL
3. BLOCKER
4. NEXT_ACTION
5. EVIDENCE
6. IRREVERSIBLE
7. OUTPUT

## Hard stop triggers
Stop and verify before speaking or acting when any of these appear:

- payment flow
- cancellation flow
- API usage
- user data
- Cloud Run deploy
- GitHub branch or merge state
- file path or working directory
- screenshot mismatch
- user says: zureru, zure, chigau, dame, HOLD, rollback

## Physical preflight
Before any command instruction, require:

```bash
pwd
ls -la
```

Before any file-specific command, require:

```bash
test -f PATH || { echo "STOP: missing PATH"; exit 1; }
```

Before any directory-specific command, require:

```bash
test -d PATH || { echo "STOP: missing PATH"; exit 1; }
```

## Forbidden
- Do not guess paths.
- Do not say done without evidence.
- Do not explain before checking.
- Do not treat local success as production success.
- Do not treat branch success as main success.
- Do not treat deploy success as behavior success.

## Completion evidence
A task is complete only when the final real target passes.

Examples:
- Branch code exists is not enough. Main must contain it.
- Main contains it is not enough. Cloud Run must deploy it.
- Cloud Run deploy is not enough. Real endpoint must return expected result.
- Quota code exists is not enough. 6th request must return 429.

## Current NextBase release gate
HOLD until all pass:

- translate direct request returns HTTP 200
- smile-friend-engine requests 1 to 5 return HTTP 200
- smile-friend-engine request 6 returns 429 FREE_LIMIT_REACHED
- payment flow still routes through modal
- cancel flow has explanation before Stripe

## Short form
Check first.
Show evidence.
Stop on mismatch.
Fix before reporting.
