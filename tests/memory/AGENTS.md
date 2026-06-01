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

## Validate

```bash
python -m pytest -q tests/memory
python -m pytest -q tests/memory/test_memo_schema_contracts.py tests/memory/test_memo_memory_context_boundaries.py
python -m pytest -q tests/memory/test_memo_runtime_writeback_boundaries.py tests/memory/test_memo_live_receipt_boundaries.py tests/memory/test_memo_handoff_boundaries.py tests/memory/test_memo_eval_guardrails.py
python -m pytest -q tests/memory/test_reviewed_intake_landing.py
python scripts/memory/validate_memo_corpus.py
python scripts/memory/validate_memory_operations.py
```
