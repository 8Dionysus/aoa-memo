# VALIDATION.md

On-demand human procedure for `tests/memory/AGENTS.md`.

## On-demand procedure

### Preserved route from `tests/memory/AGENTS.md`

Shared executable routes remain owned by [`docs/memory/VALIDATION.md`](../../docs/memory/VALIDATION.md), [`memo/VALIDATION.md`](../../memo/VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python -m pytest -q tests/memory
python -m pytest -q tests/memory/test_memo_schema_contracts.py tests/memory/test_memo_memory_context_boundaries.py
python -m pytest -q tests/memory/test_memo_runtime_writeback_boundaries.py tests/memory/test_memo_live_receipt_boundaries.py tests/memory/test_memo_handoff_boundaries.py tests/memory/test_memo_eval_guardrails.py
python -m pytest -q tests/memory/test_reviewed_intake_landing.py
```
