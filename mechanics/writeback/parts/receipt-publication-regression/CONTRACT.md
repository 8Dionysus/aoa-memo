# Receipt publication regression Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/writeback/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and historical placement is recorded in `../../PROVENANCE.md`.

## Source Surfaces

- `mechanics/writeback/parts/receipt-publication-regression/tests/fixtures/memo_writeback_receipts.example.jsonl`
- `mechanics/writeback/parts/receipt-publication-regression/tests/test_publish_live_receipts_core.py`
- `mechanics/writeback/parts/receipt-publication-regression/tests/test_publish_live_receipts_boundaries.py`
- `mechanics/writeback/parts/receipt-publication-regression/tests/test_publish_live_receipts_growth.py`

## Contract

keeps tracked writeback receipts part-local and recall-surface backed

The publication helper and receipt fixture are part-local regression surfaces.
They may validate and append owner-local memo receipts, but they must not become
runtime receipt authority or cross-repo stats truth.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
