# Deployment incident gate Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/operational-gate/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and `../../legacy/`.

## Source Surfaces

- [DEPLOYMENT_INCIDENT_MEMORY_GATE](../../docs/DEPLOYMENT_INCIDENT_MEMORY_GATE.md)
- `schemas/deployment_incident_memory_gate_v1.json`
- `schemas/deployment_lesson_candidate_v1.json`
- `examples/deployment_incident_memory_gate.example.json`
- `examples/deployment_lesson_candidate.example.json`
- `tests/test_operational_gate_mechanic.py`

## Contract

admits deployment incident memory only with evidence, owner route, review posture, and future effect

## Artifact Contract

The part keeps deployment incident gate decisions, deployment lesson
candidates, and the package boundary regression together because both contract
objects answer whether deployment evidence deserves durable memo recall.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
