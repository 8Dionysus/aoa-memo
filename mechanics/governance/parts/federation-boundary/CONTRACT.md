# Federation boundary Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/governance/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and `../../legacy/`.

## Source Surfaces

- [FEDERATION_MEMORY_BOUNDARIES](../../docs/FEDERATION_MEMORY_BOUNDARIES.md)
- [FEDERATION_FORGETTING_LAW](../../docs/FEDERATION_FORGETTING_LAW.md)
- `schemas/federation_forgetting_decision_v1.json`
- `schemas/federation_memory_gate_decision_v1.json`
- `examples/federation_forgetting_decision.example.json`
- `examples/federation_memory_gate_decision.example.json`

## Contract

cross-repo pattern memory, forgetting, and harvest gates without promotion authority

## Artifact Contract

The part keeps federation gate and forgetting contracts beside the federation
boundary docs. These examples may be consumed by lineage-harvest tests, but
they remain governance-owned memory gates, not pattern-lineage adoption or KAG
promotion.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
