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
Former name: NE Gateway / nextbase-gateway-v1.

Responsible for:
- AI provider routing
- role-based key selection
- separating prod / dev / admin / noir roles
- keeping provider keys behind server-side gates

Do not call it NE Gateway in normal work.
Use AI Router.

## Role mapping
```text
caller_id = noir  -> NB_GATE_NOIR
caller_id = admin -> NB_GATE_ADMIN
caller_id = dev   -> NB_GATE_DEV
caller_id = prod  -> NB_GATE_PROD
```

## Current release gate
HOLD until all pass:

1. translate /health returns gateway mode.
2. translate POST /translate returns HTTP 200.
3. smile-friend-engine requests 1 to 5 return HTTP 200.
4. smile-friend-engine request 6 returns 429 FREE_LIMIT_REACHED.
5. payment flow still routes through modal.
6. cancellation flow has explanation before Stripe.

## Current known blocker
If AI Router returns provider error such as expired prod key, do not change structure.
Fix or rotate the prod key in AI Router first.

## Forbidden
- Do not rename GLB into Smile Friend.
- Do not treat Smile Friend Engine as the product.
- Do not bypass AI Router with direct provider calls.
- Do not use admin role as prod fallback.
- Do not request key re-entry before checking service env and route.
- Do not claim GO from local tests only.
- Do not claim GO from deploy success only.

## Short form
GLB is the product.
Smile Friend Engine controls people-side access.
AI Router controls AI-side access.
translate connects them.
