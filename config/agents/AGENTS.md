# AGENTS.md

Route card for `config/agents/`.

## Purpose

This district owns the source map for agent-facing route-card coverage.

## Source

`agents_mesh.json` is source-authored and drives
`generated/agents/agents_mesh.min.json`.

## Route

- Up: `config/AGENTS.md`, then `AGENTS.md`.
- Across: every `AGENTS.md` named in `canonical_cards`.
- Downstream: `scripts/agents/` builders and validators.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
