# Downstream Feed Test Localization

- Decision ID: AOA-MEM-D-0008

## Status

Accepted on 2026-05-18.

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-downstream-feed-test-localization.md
- Surface classes: consumer handoff, validation guard
- Mechanic parents: none
- Guard families: docs route
- Memory object classes: none
- Posture: active rationale

## Context

`config/root_technical_districts.json` grouped three root test artifacts under
one `downstream_memory_feed_contracts` family:

- `tests/test_downstream_feed_contracts.py`
- `tests/fixtures/memo_writeback_receipts.example.jsonl`
- `tests/test_cross_mechanic_candidate_contracts.py`

That grouping was mechanically convenient but semantically wrong. The
downstream feed regression is the consumer-handoff package's read-surface
contract. The tracked receipt fixture is writeback-owned test evidence. The
cross-mechanic candidate-contract regression is the only item in that group that remains a true
cross-mechanic root test.

Leaving all three in root would keep root `tests/` as an artifact parking lot
after the mechanics tree already had package-local test lanes.

## Decision

Move the downstream feed regression to
`mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_downstream_feed_contracts.py`.

Move the tracked writeback receipt fixture to
`mechanics/writeback/parts/receipt-publication-regression/tests/fixtures/memo_writeback_receipts.example.jsonl`.

Keep `tests/test_cross_mechanic_candidate_contracts.py` in root as the
cross-mechanic candidate-contract regression, and rename its root technical family
to `cross_mechanic_candidate_contracts`.

## Consequences

- Consumer-facing recall, KAG export, checkpoint, and writeback read-surface
  alignment now routes through the consumer-handoff mechanic.
- Writeback receipt publication keeps its durable fixture beside the
  writeback tests that consume it.
- Root `tests/` keeps only the cross-mechanic contract regression from this group.
- `scripts/validate_mechanic_artifact_topology.py` now accepts an explicit
  `cross-mechanic-contract-regression` root test-family role.

## Verification

Expected verification:

- `python scripts/validate_mechanic_artifact_topology.py`
- `python scripts/build_mechanic_artifact_inventory.py --check`
- `python scripts/validate_mechanic_artifact_inventory.py`
- `python -m pytest -q mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_downstream_feed_contracts.py mechanics/writeback/parts/receipt-publication-regression/tests/test_publish_live_receipts.py tests/test_cross_mechanic_candidate_contracts.py tests/test_mechanic_artifact_topology.py tests/test_mechanic_artifact_inventory.py`
- `python scripts/release_check.py`
