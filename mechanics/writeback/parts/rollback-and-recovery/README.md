# Rollback and recovery

This active part belongs to `mechanics/writeback/` and materializes the matching row in `../../PARTS.md`.

## Start Here

- [CONTRACT](CONTRACT.md)
- [VALIDATION](VALIDATION.md)

## Source Surfaces

- [ROLLBACK_MEMORY_WRITEBACK](../../docs/ROLLBACK_MEMORY_WRITEBACK.md)
- [ROLLBACK_REVISION_LEDGER_WRITEBACK](../../docs/ROLLBACK_REVISION_LEDGER_WRITEBACK.md)
- [TRAIN_ROLLBACK_MEMORY_WRITEBACK](../../docs/TRAIN_ROLLBACK_MEMORY_WRITEBACK.md)

## Function

keeps rollback memory bounded

## Local Artifacts

- `schemas/rollback_memory_entry_v1.json`
- `schemas/rollback_revision_ledger_entry_v1.json`
- `examples/rollback_memory_entry_v1.example.json`
- `examples/rollback_revision_ledger_entry.example.json`
- `tests/test_rollback_recovery_contracts.py`

## Next Route

Use `../../OWNER_MAP.md` for stronger owner routing and `../../PROVENANCE.md` for placement history.
