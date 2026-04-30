# GLB PRODUCT UI DIRECTION

This document converts visual reference images into product UI direction.
Images are not code.
The existing HTML/JS logic must remain the source of runtime behavior.

## Core rule

```text
Image = mood reference
HTML/CSS = implementation shell
Existing JS = runtime logic
```

Do not rebuild business logic from visual references.
Do not change API endpoints, caller_id mapping, quota, billing, entitlements, or travel-pass rules from a design pass.

## Product split

```text
2.99 = fun entry product
14.99 = travel protection product
```

## 2.99 direction

Role:
- Entry product
- First paid step
- Light, fun, approachable
- Makes the user want to try GLB

Emotion:
- Fun
- Curiosity
- Travel excitement
- Friendly voice

Visual direction:
- Brighter than 14.99
- Smile / travel / movement
- Voice UI can feel playful
- Image-led hero is allowed
- Phone mockup / microphone motif is acceptable

Copy direction:

```text
Travel is easier when you can speak.
Say it anywhere.
Talk freely while you travel.
```

CTA direction:

```text
Start translating
Try voice
Keep talking
```

Avoid:
- Fear-heavy language
- Emergency-first framing
- Overly dark / severe UI

## 14.99 direction

Role:
- Higher-value travel pass
- Safety and no-stuck product
- Strong reason to pay before/during travel

Emotion:
- Relief
- Security
- Control
- Preparedness

Visual direction:
- More serious than 2.99
- Still premium, not frightening
- Focus on real travel friction:
  - airport
  - taxi
  - hotel
  - restaurant
  - hospital / emergency
  - lost / misunderstood situations
- The stage should feel like a tool the user can show to someone immediately.

Copy direction:

```text
When words fail, this speaks for you.
Stuck in another language? Show this.
Say it. I’ll make it understood.
Don’t get stuck without words.
```

CTA direction:

```text
Speak now
Type message
Show phrase
```

Upgrade / quota copy:

```text
3 chances left today.
Don’t get stuck without words.
```

At limit:

```text
Limit reached. Don’t let language stop you.
```

Avoid:
- Cute-only visuals
- Generic AI assistant feeling
- Abstract world peace / child imagery as primary sales frame
- Copy that does not explain the travel use case immediately

## Implementation rule

For both 2.99 and 14.99:

Keep these runtime IDs stable:

```text
t-from
t-to
t-swap
glb-result
flip-btn
btn-speak
btn-show
btn-essentials
panel-speak
panel-show
panel-essentials
mic-btn
show-input
t-btn
glb-cards
glb-quota
```

Never remove or rename these without updating the existing JS.

## HTML strategy

```text
1. Preserve current script logic.
2. Replace / refine CSS and visible shell only.
3. Keep existing endpoint and payload behavior.
4. Keep caller_id semantics.
5. Verify on real mobile screen before GO.
```

## Product hierarchy

```text
2.99 sells curiosity.
14.99 sells confidence.
```

## Short form

The reference image is good for 2.99: bright, fun, approachable.
14.99 must be more protective: travel safety, no-stuck, show-this-to-someone.
Do not convert image directly into code.
Convert image into mood, copy, layout pressure, then implement around stable IDs and existing logic.
