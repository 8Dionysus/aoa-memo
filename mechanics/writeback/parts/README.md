# Writeback Parts Index

Functioning Writeback memo parts live here. Each part mirrors one active row in `../PARTS.md` and keeps its own contract and validation route.

## Parts

- [Runtime and temperature](runtime-and-temperature/README.md) - keeps runtime writeback mapped without runtime ownership
- [Quest and chronicle](quest-and-chronicle/README.md) - keeps quest writeback source-linked and manual-first
- [Revision ledgers](revision-ledgers/README.md) - keeps revision and revocation writeback reviewable
- [Rollback and recovery](rollback-and-recovery/README.md) - keeps rollback memory bounded
- [Growth and continuity](growth-and-continuity/README.md) - keeps growth and continuity writeback owner-routed
- [Receipt publication regression](receipt-publication-regression/README.md) - keeps tracked writeback receipts package-local and recall-surface backed

## Validation

Use the package validation lane in [AGENTS](../AGENTS.md#validation).

For part topology changes, also run:

```bash
python scripts/validate_memo_mechanic_parts.py
```
