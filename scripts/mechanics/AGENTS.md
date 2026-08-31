# AGENTS.md

Route card for `scripts/mechanics/`.

## Purpose

This district owns mechanic index, readiness, owner route, landing log, card,
parts, and artifact validators.

## Source

Source truth routes to `config/mechanics/memo_mechanics.json`,
`mechanics/README.md`, and package-local mechanic files.

## Route

- Up: `scripts/AGENTS.md`, then `AGENTS.md`.
- Across: `tests/mechanics/` and `generated/mechanics/`.
- Downstream: mechanic package readiness and artifact inventory.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
