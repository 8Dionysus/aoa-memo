# VALIDATION.md

On-demand human procedure for `scripts/memory/validators/AGENTS.md`.

## On-demand procedure

### Preserved route from `scripts/memory/validators/AGENTS.md`

Shared executable routes remain owned by [`docs/validation/VALIDATION.md`](../../../docs/validation/VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python scripts/memory/validate_memo.py --profile all
python -m pytest -q tests/memory/test_memo_schema_contracts.py tests/memory/test_memo_runtime_writeback_boundaries.py tests/memory/test_memo_live_receipt_boundaries.py tests/root-topology/test_validator_topology.py
```
