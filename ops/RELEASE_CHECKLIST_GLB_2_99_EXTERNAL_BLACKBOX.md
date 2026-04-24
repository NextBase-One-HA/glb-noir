# GLB 2.99 Release Checklist (External Black Box)

## Scope lock
- Keep translation core flow unchanged: dictionary -> cache -> direct/pivot -> API fallback.
- Keep self-optimization as an external gate only (no in-core mutation).

## Release checks (must PASS)
- `npm run launch:ready`
- `npm run security:test`
- `python3 tools/glb_startup_integrity_gate.py --mode check`

## Pricing and CTA
- `$2.99` appears consistently on release surfaces (`index.html`, `index.next.html`, `travel.html`, `index.premium.html`).
- `id="t-btn-monthly"` exists and points to Stripe Payment Link.
- `payment_cta_click` and `purchase_success` events are emitted.
- Primary CTA copy is short and clear (`Start GLB 2.99` / local equivalent).

## Startup integrity gate
- Gate order enforced before release: immutable -> dynamic -> manifest -> approval -> revoke -> permit.
- Failures are fail-closed with `reason_code` in `logs/startup_integrity_audit.jsonl`.
- `monitoring/glb_startup_manifest.latest.json` is generated with:
  - `build_id`, `app_version`, `immutable_json_sha256`, `dynamic_json_sha256`
  - `manifest_sha256`, `approval_mode`, `signer_id`, `token_id`
  - `revocation_status`, `release_channel`

## Travel mode minimal
- Feature flag: `NEXTBASE_TRAVEL_MODE_FULL`.
- OFF: no travel minimal section shown.
- ON: minimal travel categories shown and events emitted:
  - `travel_mode_entry`
  - `travel_phrase_used`

## Quality gate event coverage
- `translation_success`
- `translation_failure`
- `api_failure`
- `travel_mode_entry`
- `travel_phrase_used`
- `payment_cta_click`
- `purchase_success`
- `user_drop_point`

## Audit safety
- Startup audit contains only operational metadata.
- No translation body, no personal info in startup audit log.

## Commands for release decision
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `npm run security:startup-gate`
- `npm run launch:ready`

## Latest pre-release run (2026-04-24)
- `npm run dynamic:refresh` (`nextbase_self_opt_layer`): PASS
- `python3 -m unittest discover -s tests -p 'test_*.py'`: PASS (9 tests)
- `npm run security:startup-gate`: PASS (`reason_code=STARTUP_OK`, `revocation_status=ACTIVE`)
- `npm run launch:ready`: PASS (watchdog + startup gate + readiness)
- Decision: **GO** (dynamic drift occurs => HOLD/fail-closed by design)
