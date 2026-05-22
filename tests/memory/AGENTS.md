# AGENTS.md

Route card for `tests/memory/`.

## Purpose

This district owns regression tests for memory schemas, recall contracts,
operation-cycle contracts, generated memory surfaces, and Phase Alpha object
examples. It also protects the reviewed `memo/` corpus shape and reviewed
intake landing route.

## Source

Tests here protect source contracts in `docs/memory/`, `docs/posture/`,
`schemas/`, `examples/`, and `memo/`.

## Route

- Up: `tests/AGENTS.md`, then `AGENTS.md`.
- Across: `scripts/memory/`.
- Downstream: generated memory parity.

## Validate

```bash
python -m pytest -q tests/memory
python -m pytest -q tests/memory/test_reviewed_intake_landing.py
python scripts/memory/validate_memo_corpus.py
python scripts/memory/validate_memory_operations.py
```
