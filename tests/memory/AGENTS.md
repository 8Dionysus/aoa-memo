# AGENTS.md

Route card for `tests/memory/`.

## Purpose

This district owns regression tests for memory schemas, recall contracts,
operation-cycle contracts, generated memory surfaces, and Phase Alpha object
examples.

## Source

Tests here protect source contracts in `docs/memory/`, `docs/posture/`,
`schemas/`, and `examples/`.

## Route

- Up: `tests/AGENTS.md`, then `AGENTS.md`.
- Across: `scripts/memory/`.
- Downstream: generated memory parity.

## Validate

```bash
python -m pytest -q tests/memory
python scripts/memory/validate_memory_operations.py
```
