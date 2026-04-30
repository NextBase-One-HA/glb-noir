# NEXTBASE DYNAMIC CANONICAL

This file records the current moving state toward `canonical/NEXTBASE_IMMUTABLE_CANONICAL.md`.
It can change as implementation changes.
It cannot override the immutable canonical.

## Current status

```text
STATE: HOLD
GOAL: Make GLB work as the first revenue product inside NextBase OS with a dedicated AI Router.
BLOCKER: Current live `nextbase-gateway-v1` still runs the old mixed gateway shape (`uvicorn smile_friend:app`).
NEXT_ACTION: Deploy dedicated `ai_router/` as the real AI Router, prove `/health` and `/translate`, then switch Smile Friend Engine to it.
OUTPUT: HOLD until real endpoint evidence passes.
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
  Role: human-side entrance/exit, quota, entitlement, STELLA checks

AI Router dedicated implementation:
  Repo path: ai_router/
  Intended Cloud Run service: ai-router
  Region: asia-northeast1
  Role: AI-side routing, key resolution, model resolution, provider call
  Status: CREATED IN REPO / NOT LIVE-PROVEN

nextbase-gateway-v1:
  Current Cloud Run service exists.
  Current build still appears to use old mixed entrypoint: uvicorn smile_friend:app.
  Role after redesign: legacy compatibility until replaced by dedicated ai-router.

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

- Path mismatch between translate and AI Router was fixed.
- translate `/health` returns gateway_v1_configured true.
- translate POST reaches AI Router `/translate`.
- Current old gateway returns provider-level API key expired.
- Dedicated `ai_router/` implementation was added to repo, but is not yet proven live.
- Current live `nextbase-gateway-v1` still builds with old `CMD [uvicorn, smile_friend:app]`.
- NextBase API exists by user report, but is not yet proven usable.

## Model rule

Use current stable provider model strings, verified against provider documentation before deploy.
For Gemini API text route, current production default is `gemini-2.5-flash` unless real provider docs or listModels proves otherwise.
Do not use dead model names such as `gemini-2.0-flash`.
Do not use `latest` aliases for production unless explicitly approved.

## Current release gate

HOLD until all pass:

1. Dedicated AI Router `/health` returns HTTP 200.
2. Dedicated AI Router `/translate` returns HTTP 200 with `key_source=NB_GATE_PROD` or equivalent evidence.
3. Smile Friend Engine is pointed to dedicated AI Router.
4. Smile Friend Engine requests 1 to 5 return HTTP 200.
5. Smile Friend Engine request 6 returns HTTP 429 with `FREE_LIMIT_REACHED`.
6. GLB UI uses Smile Friend Engine route correctly.
7. Payment flow still routes through modal.
8. Cancellation flow explains before external portal.
9. NextBase API role and usable endpoint evidence are verified if it is part of the release route.

## Immediate technical priority

```text
1. Add Dockerfile / requirements for ai_router/ if missing.
2. Deploy ai_router/ to separate Cloud Run service `ai-router`.
3. Set NB_GATE_PROD, NB_GATE_DEV, NB_GATE_ADMIN, NB_GATE_NOIR, GEMINI_MODEL.
4. Test /health and /translate.
5. Only after live proof, migrate Smile Friend Engine route.
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
Current old gateway is legacy compatibility.
Dedicated `ai_router/` is the new optimal design.
translate is adapter only.
Primary path is Smile Friend Engine -> dedicated AI Router.
NextBase API exists but is HOLD until endpoint evidence proves usability and role.
Current state is HOLD until endpoint proof passes.
