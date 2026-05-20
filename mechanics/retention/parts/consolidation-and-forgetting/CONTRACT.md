# Consolidation and forgetting Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/retention/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and `../../legacy/`.

## Source Surfaces

- [CONSOLIDATION_FORGETTING_OPERATION](../../docs/CONSOLIDATION_FORGETTING_OPERATION.md)
- `schemas/memory_consolidation_forgetting_operation_v1.json`
- `examples/memory_consolidation_forgetting.supersede.example.json`
- `examples/memory_consolidation_forgetting.archive.example.json`

## Contract

keeps demotion, deduplication, supersession, retraction, archive, and freeze as explicit reviewed memory operations

## Artifact Contract

This part owns the schema and examples for lifecycle-changing memory
operations. Every operation keeps target memory ids, trigger, lifecycle
transition, retention fields, review route, output refs, and audit refs
inspectable.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
