# Rollback and recovery Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/writeback/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and `../../legacy/`.

## Source Surfaces

- [ROLLBACK_MEMORY_WRITEBACK](../../docs/ROLLBACK_MEMORY_WRITEBACK.md)
- [ROLLBACK_REVISION_LEDGER_WRITEBACK](../../docs/ROLLBACK_REVISION_LEDGER_WRITEBACK.md)
- [TRAIN_ROLLBACK_MEMORY_WRITEBACK](../../docs/TRAIN_ROLLBACK_MEMORY_WRITEBACK.md)

## Contract

keeps rollback memory bounded

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
