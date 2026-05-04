# NEXTBASE_CURRENT_STRUCTURE

Last updated: 2026-04-30

## Core Names (authoritative)

- Product/UI name: `GLB`
- Server quota + translate gate: `Smile Friend Engine`
- Provider routing layer name: `AI Router`

## Naming Prohibition

- `NE Gateway` is a deprecated historical name.
- Do not use `NE Gateway` in active implementation reports, code comments, runbooks, or deploy instructions.
- Allowed exception: explicit historical note like "formerly called NE Gateway".

## Operational Evidence Rule

- No completion claim is valid without real endpoint evidence.
- Evidence must be concrete (HTTP status + response body excerpts).

## Reporting Rule

- Every status report must explicitly include one of:
  - `GO`
  - `HOLD`

## Immediate Stop Keywords

If user input contains any of these terms, stop current execution and wait for confirmation:

- `ズレ`
- `違う`
- `ダメ`
- `HOLD`
- `rollback`
