# KAG source export Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/consumer-handoff/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and historical placement is recorded in `../../PROVENANCE.md`.

## Source Surfaces

- [KAG_SOURCE_EXPORT](../../docs/KAG_SOURCE_EXPORT.md)
- `schemas/memo_to_kag_bridge_record_v1.json`
- `examples/memo_to_kag_bridge_record.example.json`
- `generated/kag_export.min.json`
- `scripts/generate_kag_export.py`

## Contract

describes the source-owned tiny donor export for KAG readiness

## Artifact Contract

The part keeps the memo-owned KAG donor export, its generator, and the
`memo_to_kag_bridge_record` bridge contract together. The generated export may
point toward KAG consumers, but it remains a source-owned memo donor capsule
and not graph substrate truth or federation activation.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
