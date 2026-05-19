# Witness trace contract Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/recurrence-support/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and `../../legacy/`.

## Source Surfaces

- [WITNESS_TRACE_CONTRACT](../../docs/WITNESS_TRACE_CONTRACT.md)

## Contract

keeps witness trace exports reviewable and maps later writeback into existing memo object kinds

## Part-Local Artifacts

- `schemas/witness-trace.schema.json`
- `examples/witness_trace.example.json`
- `tests/test_recurrence_support_mechanic.py`

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
