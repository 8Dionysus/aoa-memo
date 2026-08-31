# AGENTS.md

Route card for `generated/mechanics/`.

## Purpose

This district holds generated mechanic indexes, cards, owner routes, landing
logs, readiness, and artifact inventory.

## Source

Source truth routes to `config/mechanics/memo_mechanics.json`,
`mechanics/README.md`, and package-local mechanic surfaces.

## Route

- Up: `generated/AGENTS.md`, then `AGENTS.md`.
- Across: `mechanics/` and `scripts/mechanics/`.
- Downstream: OS Abyss readiness inspection and package route selection.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
