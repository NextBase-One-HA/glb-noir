# NEXTBASE DYNAMIC CANONICAL

This file records the current moving state toward `canonical/NEXTBASE_IMMUTABLE_CANONICAL.md`.
It can change as implementation changes.
It cannot override the immutable canonical.

## Current status

```text
STATE: HOLD
GOAL: Make GLB work as the first revenue product inside NextBase OS through the dedicated AI Router.
BLOCKER: GLB UI route, payment modal path, and cancellation flow still need live verification.
NEXT_ACTION: Verify GLB UI uses Smile Friend Engine route, then verify payment and cancellation flows.
OUTPUT: HOLD until GLB UI and revenue/user-facing flows pass live evidence.
```

## Correct production target

```text
User
  -> GLB
  -> Smile Friend Engine
  -> AI Router dedicated service
  -> AI provider
  -> GLB
```

## Adapter path (non-primary)

```text
Smile Friend Engine
  -> translate
  -> AI Router
```

## Current service map

```text
GLB UI:
  GitHub Pages / static HTML files

Smile Friend Engine:
  Cloud Run service: smile-friend-engine
  Region: us-central1
  URL: https://smile-friend-engine-125142687526.us-central1.run.app
  Role: human-side entrance/exit, quota, entitlement, STELLA checks
  Status: LIVE_PASS for upstream to dedicated AI Router and free quota gate

AI Router dedicated service:
  Repo path: ai_router/
  Cloud Run service: ai-router
  Region: asia-northeast1
  URL: https://ai-router-125142687526.asia-northeast1.run.app
  Role: AI-side routing, key resolution, model resolution, provider call
  Status: LIVE_PASS

nextbase-gateway-v1:
  Current Cloud Run service exists.
  Legacy mixed gateway shape (`uvicorn smile_friend:app`).
  Role after redesign: legacy compatibility / rollback only.

translate:
  Cloud Run service: translate
  Region: us-central1
  Role: fallback / test / compatibility adapter only

nextbase-app:
  Cloud Run service exists.
  Role not fully finalized in current GLB route.

NextBase API:
  API has been created in NextBase context.
  Usability, endpoint shape, deployment target, and production role are not yet verified.
  Treat as HOLD until real endpoint evidence exists.
```

## Confirmed facts

- Dedicated `ai_router/` implementation was added to repo.
- `ai-router` Cloud Run service deployed successfully.
- `ai-router /translate` returned HTTP 200.
- `ai-router /translate` used `model=gemini-2.5-flash`.
- `ai-router /translate` returned `key_source=NB_GATE_PROD`.
- Provider returned `provider_status=200`.
- Therefore dedicated AI Router is LIVE_PASS.
- Smile Friend Engine was pointed to dedicated `ai-router` via `TRANSLATE_UPSTREAM_URL`.
- Smile Friend Engine `/translate` returned HTTP 200 through dedicated AI Router.
- Smile Friend Engine quota test passed: requests 1-5 returned HTTP 200, request 6 returned HTTP 429 with `FREE_LIMIT_REACHED`.
- nextbase-gateway-v1 remains legacy compatibility, not primary production route.
- NextBase API exists by user report, but is not yet proven usable.

## Model rule

Use current stable provider model strings, verified against provider documentation before deploy.
For Gemini API text route, current production default is `gemini-2.5-flash` unless real provider docs or listModels proves otherwise.
Do not use dead model names such as `gemini-2.0-flash`.
Do not use `latest` aliases for production unless explicitly approved.

## Current release gate

HOLD until all pass:

1. Dedicated AI Router `/health` returns HTTP 200.
2. Dedicated AI Router `/translate` returns HTTP 200 with `key_source=NB_GATE_PROD` or equivalent evidence. PASS.
3. Smile Friend Engine is pointed to dedicated AI Router. PASS.
4. Smile Friend Engine requests 1 to 5 return HTTP 200. PASS.
5. Smile Friend Engine request 6 returns HTTP 429 with `FREE_LIMIT_REACHED`. PASS.
6. GLB UI uses Smile Friend Engine route correctly.
7. Payment flow still routes through modal.
8. Cancellation flow explains before external portal.
9. NextBase API role and usable endpoint evidence are verified if it is part of the release route.

## Immediate technical priority

```text
1. Verify GLB UI route points to Smile Friend Engine.
2. Verify GLB UI translation live behavior.
3. Verify payment flow still routes through modal.
4. Verify cancellation flow explains before external portal.
5. Record evidence in execution ledger.
```

## Naming rule

Use:

- GLB
- Smile Friend Engine
- STELLA
- translate
- AI Router
- Self Optimization Layer
- Proof Mode
- NextBase API

## Evidence rule

No GO from:

- local code only
- branch only
- merge only
- deploy only
- API creation alone

GO candidate requires real endpoint evidence.

## Short form
Immutable canonical points.
Dynamic canonical moves.
Dedicated AI Router is LIVE_PASS.
Smile Friend Engine upstream and quota are LIVE_PASS.
nextbase-gateway-v1 is legacy compatibility.
translate is adapter only.
Primary path is GLB -> Smile Friend Engine -> dedicated AI Router.
NextBase API exists but is HOLD until endpoint evidence proves usability and role.
Current state is HOLD until GLB UI and revenue/user-facing flows pass endpoint proof.
