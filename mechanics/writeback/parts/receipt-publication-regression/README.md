# Receipt publication regression

This active part belongs to `mechanics/writeback/` and materializes the matching row in `../../PARTS.md`.

## Start Here

- [CONTRACT](CONTRACT.md)
- [VALIDATION](VALIDATION.md)

## Source Surfaces

- `mechanics/writeback/parts/receipt-publication-regression/tests/fixtures/memo_writeback_receipts.example.jsonl`
- `mechanics/writeback/parts/receipt-publication-regression/tests/test_publish_live_receipts_core.py`
- `mechanics/writeback/parts/receipt-publication-regression/tests/test_publish_live_receipts_boundaries.py`
- `mechanics/writeback/parts/receipt-publication-regression/tests/test_publish_live_receipts_growth.py`

## Function

keeps tracked writeback receipts part-local and recall-surface backed

## Local Artifacts

- `scripts/publish_live_receipts.py`
- `tests/fixtures/memo_writeback_receipts.example.jsonl`
- `tests/publish_live_receipts_support.py`
- `tests/test_publish_live_receipts_core.py`
- `tests/test_publish_live_receipts_boundaries.py`
- `tests/test_publish_live_receipts_growth.py`

## Next Route

Use `../../OWNER_MAP.md` for stronger owner routing and `../../PROVENANCE.md` for placement history.
