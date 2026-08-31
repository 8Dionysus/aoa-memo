# AGENTS.md

Route card for `docs/boundaries/`.

## Purpose

This district owns repository, operational, and write-path boundary language
for memo: what memory may claim, what must route to stronger owners, and where
live operation or untrusted source pressure remains outside memo.

## Source

`BOUNDARIES.md` is the primary owner-boundary surface.
`OPERATIONAL_BOUNDARY.md` narrows operational claims and runtime-facing limits.
`MEMORY_WRITE_PATH_GUARDRAILS.md` names the untrusted-input and write-path
boundary before mechanic-level admission.

## Route

- Up: `docs/AGENTS.md`, then `AGENTS.md`.
- Across: `docs/memory/` for object doctrine and `docs/posture/` for temporal
  and provenance posture.
- Downstream: mechanic `OWNER_MAP.md` files when a boundary is package-local.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
