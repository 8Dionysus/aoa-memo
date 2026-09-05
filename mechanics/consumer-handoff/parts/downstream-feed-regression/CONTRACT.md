# Downstream feed regression Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/consumer-handoff/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and historical placement is recorded in `../../PROVENANCE.md`.

## Source Surfaces

- `mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_downstream_feed_generated_contracts.py`
- `mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_downstream_feed_runtime_writeback_contracts.py`
- `mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_downstream_feed_docs_routes.py`
- `mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_consumer_handoff_mechanic.py`

## Contract

keeps consumer-facing recall, KAG export, checkpoint, and writeback read surfaces aligned without becoming runtime authority

## Artifact Contract

The part owns consumer-handoff regression tests that cross generated memory
families, KAG donor export, checkpoint return, writeback intake, root docs, and
quest references. It can assert read-surface alignment; it must not become
runtime authority, proof, route dispatch, or owner acceptance.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
