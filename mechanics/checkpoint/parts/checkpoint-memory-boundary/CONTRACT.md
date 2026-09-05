# Checkpoint memory boundary Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/checkpoint/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and historical placement is recorded in `../../PROVENANCE.md`.

## Source Surfaces

- [CHECKPOINT_MEMORY_BOUNDARY](../../docs/CHECKPOINT_MEMORY_BOUNDARY.md)

## Contract

names what memo may preserve and what routes away

## Artifact Contract

This part owns the package boundary regression that proves checkpoint artifacts
stay part-local and stronger owner claims stay outside memo.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
