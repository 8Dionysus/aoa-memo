# AGENTS.md

Route card for `schemas/recall-posture/`.

## Purpose

This district owns recall, lifecycle, trust, operation-mode, and decay-posture
schemas used by memo recall contracts.

## Source

`recall_contract.schema.json` is the shared recall contract.
`memory_operation_mode.schema.json` binds task-level memory access posture.
Schemas here bind recall posture. Doctrine lives in `docs/posture/` and
`docs/memory/MEMORY_MODEL.md`.

## Route

- Up: `schemas/AGENTS.md`, then `AGENTS.md`.
- Across: `examples/recall/` and `docs/posture/`.
- Downstream: validators in `scripts/memory/`.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
