# AGENTS.md

Route card for `generated/agents/`.

## Purpose

This district holds the compact AGENTS mesh generated companion.
The current output is `agents_mesh.min.json`.

## Source

`config/agents/agents_mesh.json` and the referenced `AGENTS.md` cards are the
source surfaces. The JSON here is a generated inspection surface.

## Route

- Up: `generated/AGENTS.md`, then `AGENTS.md`.
- Across: `config/agents/`.
- Downstream: agent route-card audits.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
