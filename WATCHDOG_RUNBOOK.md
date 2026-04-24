# GLB Watchdog Runbook

## Purpose
- Keep `index.next.html` and routing canonicals under continuous guard.
- Fail closed on risky drift and keep a machine-readable report.

## Commands
- Single check (immediate autofix default): `npm run watchdog:check`
- Single check with safe autofix (explicit): `npm run watchdog:autofix`
- Continuous watch (immediate autofix): `npm run watchdog:watch`
- Strict check without autofix: `npm run watchdog:check:strict`

## Outputs
- Latest report: `logs/watchdog.latest.json`
- Append-only event stream: `logs/watchdog.events.jsonl`

## Current guard rules
- Required snippets in `index.next.html`:
  - `id="tr-run"`
  - `id="glb-mic-btn"`
  - `id="glb-quick-speak"`
  - `GLBFunnel.summary`
- Forbidden snippet:
  - `micBtn.style.display = 'none'` (and double-quote variant)
- Canonical JSON shape checks:
  - `canonical/language_pair_table.json` must be object
  - `canonical/travel_categories.json` must be array

## Operation model
- On PASS: continue running
- On HOLD: fix and re-run; do not release while HOLD

