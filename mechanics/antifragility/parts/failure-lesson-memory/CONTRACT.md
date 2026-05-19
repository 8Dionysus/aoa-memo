# Failure lesson memory Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/antifragility/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and `../../legacy/`.

## Source Surfaces

- [FAILURE_LESSON_MEMORY](../../docs/FAILURE_LESSON_MEMORY.md)
- [FAILURE_LESSON_RECALL](../../docs/FAILURE_LESSON_RECALL.md)
- [DRIFT_REVIEW_LESSON_MEMORY](../../docs/DRIFT_REVIEW_LESSON_MEMORY.md)
- `schemas/failure_lesson_memory_v1.json`
- `schemas/shared_lesson_memory_v1.json`
- `examples/failure_lesson_memory.example.json`
- `examples/failure_lesson_memory.lineage.example.json`
- `examples/failure_lesson_memory.rollout.example.json`
- `examples/failure_lesson_memory.drift_review.example.json`
- `examples/shared_lesson_memory.example.json`
- `tests/test_antifragility_failure_lessons.py`

## Contract

keeps repeated failure lessons recallable without becoming proof

## Artifact Contract

The part keeps the failure lesson contract, shared lesson seed contract,
failure lesson examples, drift-review example, and local regression together.
`shared_lesson_memory` stays here because it is a lesson-memory support object
used by antifragility recall, not a standalone operation or proof family.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
