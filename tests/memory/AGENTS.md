# AGENTS.md

Route card for `tests/memory/`.

## Purpose

This district owns regression tests for memory schemas, recall contracts,
operation-cycle contracts, generated memory surfaces, runtime degradation
fixtures, handoff boundaries, eval guardrails, and Phase Alpha object examples.
It also protects the reviewed `memo/` corpus shape and reviewed intake landing
route.

## Source

Tests here protect source contracts in `docs/memory/`, `docs/posture/`,
`docs/validation/`, `schemas/`, `examples/`, `memo/`, and mechanic-local
owner surfaces. Large memory validator regressions should stay split by
boundary instead of returning to one broad `test_memo_validators.py` file.

## Route

- Up: `tests/AGENTS.md`, then `AGENTS.md`.
- Across: `scripts/memory/`.
- Downstream: generated memory parity.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
