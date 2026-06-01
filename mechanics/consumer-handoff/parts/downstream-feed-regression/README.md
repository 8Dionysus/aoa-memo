# Downstream feed regression

This active part belongs to `mechanics/consumer-handoff/` and materializes the matching row in `../../PARTS.md`.

## Start Here

- [CONTRACT](CONTRACT.md)
- [VALIDATION](VALIDATION.md)

## Source Surfaces

- `mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_downstream_feed_generated_contracts.py`
- `mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_downstream_feed_runtime_writeback_contracts.py`
- `mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_downstream_feed_docs_routes.py`
- `mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_consumer_handoff_mechanic.py`

## Function

keeps consumer-facing recall, KAG export, checkpoint, and writeback read surfaces aligned without becoming runtime authority

## Next Route

Use `../../OWNER_MAP.md` for stronger owner routing and `../../PROVENANCE.md` for placement history.
