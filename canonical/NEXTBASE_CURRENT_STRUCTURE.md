# NEXTBASE CURRENT STRUCTURE

This is the current canonical structure for GLB work.
Do not continue with old names or mixed roles.

## Final human authority
NORI-san keeps final GO / HOLD authority.
AI only supports structure, checks, implementation assistance, and reporting.

## Product
```text
GLB = the user-facing translation product
```

Users see GLB.
Users do not need to see internal service names.

## Runtime structure
```text
User
  -> GLB UI
  -> Smile Friend Engine
  -> translate
  -> AI Router
  -> AI provider
  -> GLB UI
```

## Roles

### GLB
User-facing translation app.

Responsible for:
- input
- translation result display
- payment entry
- cancellation explanation entry
- clear user experience

### Smile Friend Engine
Human-side control layer.

Responsible for:
- free quota
- paid entitlement check
- subscription state handling
- customer-friendly entry and exit behavior
- stopping free overuse before provider cost is spent

### translate
Internal bridge.

Responsible for:
- accepting translation requests after Smile Friend Engine
- forwarding to AI Router
- normalizing translation response shape for GLB

Not responsible for:
- direct provider key ownership
- business entitlement decisions
- user-facing product identity

### AI Router
Former name: nextbase-gateway-v1.

Responsible for:
- AI provider routing
- role-based access selection
- separating prod / dev / admin / noir roles
- keeping provider credentials behind server-side gates

Use AI Router as the working name.

## Role mapping
```text
caller_id = noir  -> noir role credential
caller_id = admin -> admin role credential
caller_id = dev   -> dev role credential
caller_id = prod  -> prod role credential
```

## AI Router runtime configuration note
Cloud Run has been configured with:

- current model setting: gemini-2.5-flash
- general provider credential variable
- noir role credential
- admin role credential
- dev role credential
- prod role credential
- master public/private control variables

Secret values must never be stored in this repository.

Important: if runtime still calls an old model while the current model setting is configured, the deployed AI Router image may still contain hardcoded model logic. In that case, do not ask for credential re-entry first. Rebuild or redeploy the corrected AI Router image.

## Current release gate
HOLD until all pass:

1. translate /health returns gateway mode.
2. translate POST /translate returns HTTP 200.
3. Smile Friend Engine requests 1 to 5 return HTTP 200.
4. Smile Friend Engine request 6 returns 429 FREE_LIMIT_REACHED.
5. payment flow still routes through modal.
6. cancellation flow explains before external portal.

## Current known blocker
If AI Router returns provider error such as expired prod credential, do not change structure.
Fix or rotate the prod credential in AI Router first.
If AI Router returns a model not found error for an old model while the current model setting is configured, rebuild the AI Router image so code reads the model setting.

## Forbidden
- Do not rename GLB into Smile Friend.
- Do not treat Smile Friend Engine as the product.
- Do not bypass AI Router with direct provider calls.
- Do not use admin role as prod fallback.
- Do not request credential re-entry before checking service env and route.
- Do not claim GO from local tests only.
- Do not claim GO from deploy success only.

## Short form
GLB is the product.
Smile Friend Engine controls people-side access.
AI Router controls AI-side access.
translate connects them.
