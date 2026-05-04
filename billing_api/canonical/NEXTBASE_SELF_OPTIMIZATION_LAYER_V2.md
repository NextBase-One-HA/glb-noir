# NEXTBASE_SELF_OPTIMIZATION_LAYER_V2

Last updated: 2026-04-30
Status: ACTIVE

## Purpose

Define strict execution and reporting controls for all AI work in the NextBase stack.

## Mandatory Sequence

1. Read `canonical/NEXTBASE_CURRENT_STRUCTURE.md` first.
2. Use canonical names only: `GLB`, `Smile Friend Engine`, `AI Router`.
3. Execute tasks with endpoint-backed verification.
4. Report outcome with explicit `GO` or `HOLD`.

## Name Policy

- Forbidden active term: `NE Gateway`
- Exception: historical note only, explicitly marked.

## Completion Gate

A task cannot be marked complete unless endpoint evidence is present.

Minimum evidence set:

- endpoint URL or route
- request method
- response status code
- response body excerpt

## Stop Policy

On user correction keywords, stop immediately:

- `ズレ`
- `違う`
- `ダメ`
- `HOLD`
- `rollback`

Immediate stop means:

- no further edits
- no deploy/push/commit
- wait for user direction

## Report Contract

Every report must include:

- `STATE: GO` or `STATE: HOLD`
- concise evidence block
- next action (if HOLD)
