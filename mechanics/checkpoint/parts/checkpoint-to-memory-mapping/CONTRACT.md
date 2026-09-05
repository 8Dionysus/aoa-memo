# Checkpoint-to-memory mapping Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/checkpoint/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and historical placement is recorded in `../../PROVENANCE.md`.

## Source Surfaces

- [CHECKPOINT_TO_MEMORY_MAPPING](../../docs/CHECKPOINT_TO_MEMORY_MAPPING.md)

## Contract

maps checkpoint artifacts into existing object kinds without creating checkpoint-only memory

## Artifact Contract

This part owns the checkpoint-to-memory schema and example consumed by
`mechanics/writeback/`. Consumers may read this contract, but they do not own
the checkpoint artifact or its promotion into memory.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
