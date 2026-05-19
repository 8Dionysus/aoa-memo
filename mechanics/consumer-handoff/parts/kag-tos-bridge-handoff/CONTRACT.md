# KAG/ToS bridge handoff Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/consumer-handoff/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and `../../legacy/`.

## Source Surfaces

- [KAG_TOS_BRIDGE_CONTRACT](../../docs/KAG_TOS_BRIDGE_CONTRACT.md)
- `schemas/memory_chunk_face.schema.json`
- `schemas/memory_graph_face.schema.json`
- `examples/episode.tos-interpretation.example.json`
- `examples/claim.tos-bridge-ready.example.json`
- `examples/bridge.kag-lift.example.json`
- `examples/provenance_thread.kag-lift.example.json`
- `examples/memory_chunk_face.bridge.example.json`
- `examples/memory_graph_face.bridge.example.json`

## Contract

defines chunk-face, graph-face, and ToS bridge posture without graph ownership

## Artifact Contract

The part keeps the bridge-bearing memo object chain and its chunk/graph export
faces together. These examples may be consumed by object-surface generators,
writeback regression tests, and KAG export checks, but they remain memo-owned
handoff faces rather than ToS source meaning or KAG graph truth.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
