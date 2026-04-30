# NEXTBASE DYNAMIC CANONICAL

This file records the current moving state toward `canonical/NEXTBASE_IMMUTABLE_CANONICAL.md`.
It can change as implementation changes.
It cannot override the immutable canonical.

## Current status

```text
STATE: HOLD
GOAL: Make GLB work as the first revenue product inside NextBase OS.
BLOCKER: AI Router endpoint compatibility is not fully verified after rebuild.
NEXT_ACTION: Restore/verify AI Router gateway behavior, then verify translate and Smile Friend Engine.
OUTPUT: HOLD until real endpoint evidence passes.
```

## Current runtime target

```text
User
  -> GLB
  -> Smile Friend Engine
  -> translate
  -> AI Router
  -> AI provider
  -> GLB
```

## Current service map

```text
GLB UI:
  GitHub Pages / static HTML files

Smile Friend Engine:
  Cloud Run service: smile-friend-engine
  Region: us-central1
  Role: human-side entrance/exit, quota, entitlement, STELLA checks

translate:
  Cloud Run service: translate
  Region: us-central1
  Role: bridge from Smile Friend Engine to AI Router

AI Router:
  Cloud Run service: nextbase-gateway-v1
  Region: asia-northeast1
  Role: AI-side routing and provider control

nextbase-app:
  Cloud Run service exists
  Role not fully finalized in current GLB route
```

## Confirmed facts

- NextBase immutable canonical exists.
- Self Optimization Layer V2 exists.
- Proof Mode 120 context exists.
- Tomori preflight exists.
- Tomori response gate exists.
- Smile Friend Engine `/docs` exposes `/health` and `/translate`.
- AI Router-related services expose gateway-style API structures in screenshots.
- AI Router was rebuilt and redeployed, but `/gateway` behavior must be verified.
- `GEMINI_MODEL` has been set to `gemini-2.5-flash` on AI Router, but runtime behavior must be checked by real endpoint response.

## Current release gate

HOLD until all pass:

1. AI Router expected gateway endpoint returns valid response.
2. translate `/health` shows gateway mode.
3. translate POST `/translate` returns HTTP 200.
4. Smile Friend Engine requests 1 to 5 return HTTP 200.
5. Smile Friend Engine request 6 returns HTTP 429 with `FREE_LIMIT_REACHED`.
6. GLB UI uses Smile Friend Engine route correctly.
7. Payment flow still routes through modal.
8. Cancellation flow explains before external portal.

## Immediate technical priority

```text
1. Identify the correct AI Router endpoint path.
2. If `/gateway` was lost, restore it from the original gateway structure.
3. Keep existing API shape.
4. Change only model selection and current compatibility.
5. Do not rebuild AI Router as a different service.
```

## Current naming rule

Use:

- GLB
- Smile Friend Engine
- STELLA
- translate
- AI Router
- Self Optimization Layer
- Proof Mode

Old names may appear only as historical notes.

## Evidence rule

No GO from:

- local code only
- branch only
- merge only
- deploy only

GO candidate requires real endpoint evidence.

## Short form
Immutable canonical points.
Dynamic canonical moves.
Current state is HOLD until endpoint proof passes.
