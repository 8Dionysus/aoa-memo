# AGENTS.md

Route card for `generated/quests/`.

## Purpose

This district holds generated Questbook read-model projections.

## Source

Quest source truth routes to `quests/`, `QUESTBOOK.md`, and
`mechanics/questbook/`.

## Route

- Up: `generated/AGENTS.md`, then `AGENTS.md`.
- Across: `mechanics/questbook/parts/quest-read-model-projections/`.
- Downstream: consumers may inspect generated quest catalog and dispatch only
  as read models.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
