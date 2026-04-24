# GLB maintenance switch (Core / index.next.html)

## Goals
- Ship full release, but be able to **flip to maintenance immediately** when a serious issue is confirmed.
- Avoid “silent recovery”: if `/system-status` fails, maintenance must not auto-clear when a hard lock is active.

## Mechanisms (priority)
1. **URL (fastest / emergency)**
   - Enable: add `?glb_maint=1&glb_maint_msg=...` (message optional)
   - Disable: add `?glb_maint_off=1` (clears local forced flag)
2. **localStorage force (ops / bookmarklet)**
   - Key: `GLB_MAINTENANCE_FORCE_V1`
   - Value example:
     - `{"enabled":true,"message":"Maintenance: billing safety fix in progress","until":0}`
     - Optional `until` epoch ms to auto-expire
3. **Static JSON (deploy-time switch, same origin)**
   - File: `glb_maintenance.json` (served next to `index.next.html`)
   - Schema:
     - `maintenance_mode` boolean
     - `maintenance_message` string
4. **Remote `/system-status` (existing)**
   - Still polled every 30s

## Operator playbook
- Confirm severity → choose fastest mechanism:
  - **0–60s**: URL param or localStorage force
  - **1–5 min**: set `glb_maintenance.json` `maintenance_mode=true` and deploy static hosting
- Verify:
  - overlay visible
  - translate action does not run (`GLB_MAINTENANCE_ON`)
- Clear:
  - restore JSON to false OR use `glb_maint_off=1` OR remove localStorage force

## Notes
- Hard lock prevents background status fetch from clearing maintenance accidentally.
- Keep cancel/manage trust routes reachable via support pages as already designed.
