# AGENTS.md

Route card for `config/root-topology/`.

## Purpose

This district owns the root technical district source map: which root files are
allowed to remain repo-wide, which family they belong to, and which validator
protects them.

## Source

`root_technical_districts.json` is source-authored and drives
`generated/root-topology/root_technical_districts.min.json`.

## Route

- Up: `config/AGENTS.md`, then `AGENTS.md`.
- Across: `docs/root/ROOT_SURFACE_LAW.md` and `mechanics/ARTIFACT_TOPOLOGY.md`.
- Downstream: `scripts/root-topology/` and district-local `AGENTS.md` cards.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
