# Governance boundary Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/governance/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and `../../legacy/`.

## Source Surfaces

- [GOVERNANCE_MEMORY_BOUNDARIES](../../docs/GOVERNANCE_MEMORY_BOUNDARIES.md)
- [GOVERNANCE_RUNTIME_MEMORY_BOUNDARIES](../../docs/GOVERNANCE_RUNTIME_MEMORY_BOUNDARIES.md)
- `schemas/governance_decision_memory_v1.json`
- `schemas/governance_memory_writeback_v1.json`
- `examples/governance_decision_memory_v1.example.json`
- `examples/governance_memory_writeback.example.json`
- `tests/test_governance_mechanic.py`
- `tests/test_experience_wave4_seed_contracts.py`

## Contract

memo-side governance and runtime-governance memory stop-lines

## Artifact Contract

The part keeps governance decision/writeback seed contracts and the local
governance regression together. The Wave 4 seed regression stays here because
governance-boundary is the anchor that checks the governance decision/writeback
bundle while still routing retention and writeback contracts to their stronger
or neighboring mechanic homes.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
