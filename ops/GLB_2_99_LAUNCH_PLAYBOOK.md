# GLB $2.99 Launch Playbook

## Objective
- Maximize paid conversion while protecting user trust.
- Keep launch operations reversible until irreversible release gate.

## North Star
- User anxiety near zero.
- Every user is treated as the hero.
- Conversion is optimized without degrading trust.

## Phase 1: Pre-Launch (T-7 to T-1)
- Confirm paid flow behavior in `index.next.html` with evidence.
- Keep `GLBFunnel` events active:
  - `index_reach`
  - `translate_click`
  - `stripe_click`
  - `checkout_success`
- Run watchdog and security cycle before each launch candidate:
  - `npm run watchdog:check`
  - `cd /Users/user/nextbase_self_opt_layer && npm run security:cycle`
- Freeze non-essential UI changes 24h before launch.

## Phase 2: Launch Day (T0)
- Publish build after final pass checks only.
- Monitor first hour in 15-minute windows:
  - paid entry success rate
  - checkout start rate
  - checkout success rate
  - fail reasons from client logs
- Apply reversible fixes immediately if user-impact issue is detected.

## Phase 3: First Week (T+1 to T+7)
- Ship one conversion improvement per day.
- Do not ship more than one primary CTA experiment at once.
- Keep a daily summary with:
  - conversion deltas
  - churn risk signals
  - unresolved blockers

## Required Evidence Before "PASS"
- Behavioral proof for:
  - successful paid entry (`session_id` path)
  - paid lock persistence
  - unpaid guard behavior
  - manage/cancel route visibility
- Updated run log in `logs/` and summary note in daily scorecard.
