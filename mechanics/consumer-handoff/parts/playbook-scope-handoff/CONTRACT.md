# Playbook scope handoff Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/consumer-handoff/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and historical placement is recorded in `../../PROVENANCE.md`.

## Source Surfaces

- [PLAYBOOK_MEMORY_SCOPES](../../docs/PLAYBOOK_MEMORY_SCOPES.md)
- `tests/test_playbook_memory_scopes.py`

## Contract

tells playbooks how to request bounded recall modes and scopes

## Artifact Contract

The part owns the local regression that keeps playbook-facing recall scopes,
return-ready checkpoint continuity, and discoverability aligned. It does not
define playbook choreography or active quest execution.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
