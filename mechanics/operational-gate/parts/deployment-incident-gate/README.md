# Deployment incident gate

This active part belongs to `mechanics/operational-gate/` and materializes the matching row in `../../PARTS.md`.

## Start Here

- [CONTRACT](CONTRACT.md)
- [VALIDATION](VALIDATION.md)

## Source Surfaces

- [DEPLOYMENT_INCIDENT_MEMORY_GATE](../../docs/DEPLOYMENT_INCIDENT_MEMORY_GATE.md)
- `schemas/deployment_incident_memory_gate_v1.json`
- `schemas/deployment_lesson_candidate_v1.json`
- `examples/deployment_incident_memory_gate.example.json`
- `examples/deployment_lesson_candidate.example.json`
- `tests/test_operational_gate_mechanic.py`

## Function

admits deployment incident memory only with evidence, owner route, review posture, and future effect

## Next Route

Use `../../OWNER_MAP.md` for stronger owner routing and `../../PROVENANCE.md` for placement history.
