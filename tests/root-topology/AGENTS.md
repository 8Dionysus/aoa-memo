# AGENTS.md

Route card for `tests/root-topology/`.

## Purpose

This district owns regression tests for root topology, docs placement, roadmap
parity, validator topology, validation lanes, test topology, and current
direction routes.

## Source

Tests here protect `docs/root/`, `docs/validation/`, `docs/testing/`,
`config/root-topology/`, `config/validation_lanes.json`,
`scripts/root-topology/`, `scripts/validation_lanes.py`, `scripts/ci_gate.py`,
release orchestration, and `generated/root-topology/`.

## Route

- Up: `tests/AGENTS.md`, then `AGENTS.md`.
- Across: `scripts/root-topology/`.
- Downstream: root district placement and release gate readiness.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
