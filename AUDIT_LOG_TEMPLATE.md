# AUDIT LOG TEMPLATE

## Purpose
- Keep 2.99 mode billing lock behavior verifiable at every entry point.
- Reject completion claims without concrete evidence.

## Run Information
- Date:
- Operator:
- Branch:
- Commit hash under test:
- Environment URL:

## Entry Audit Matrix

### 1) `index.next.html` (paid entry)
- [ ] `session_id` present -> `glb_subscribed` set paid and `LS_BILLING_LOCK=1` (PASS/FAIL)
- [ ] Paid pre-hide active before visible render (`#t-free-quota`, subscribe area hidden) (PASS/FAIL)
- [ ] Guard blocks unpaid direct access and redirects to `index.html` (PASS/FAIL)
- [ ] Stripe cancel/manage routes visible and clickable (PASS/FAIL)
- Evidence (console/storage/DOM):

### 2) `index.html` (free entry)
- [ ] `session_id` landing primes paid lock (`LS_BILLING_LOCK=1`) (PASS/FAIL)
- [ ] Paid pre-hide suppresses free-tier UI flash (PASS/FAIL)
- [ ] Unpaid state still shows free entry as designed (PASS/FAIL)
- Evidence:

### 3) `index.premium.html` (premium/travel layer)
- [ ] `isGlbUnlimited()` honors `glb_subscribed` OR `LS_BILLING_LOCK` (PASS/FAIL)
- [ ] `syncEntitlements` keeps paid UX when lock exists and API temporarily returns false (PASS/FAIL)
- [ ] Cancel route remains present and not hidden/removed (PASS/FAIL)
- Evidence:

### 4) Operations Guardrail Files
- [ ] `OPERATIONS_SNAPSHOT.md` exists and includes evidence-first completion rule (PASS/FAIL)
- [ ] `.cursorrules` includes snapshot-first session rule and Stripe route protection (PASS/FAIL)
- Evidence:

## Deployment/Runtime Checks
- [ ] Render static deploy completed without runtime mismatch regression (PASS/FAIL)
- [ ] GitHub Pages live URL behavior matches expected billing guards (PASS/FAIL)
- Evidence (build log excerpt / live behavior):

## Result
- Overall: PASS / HOLD
- Blocking findings:
- Required fixes:
- Re-test scope:
