# Write path guardrails Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/operational-gate/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and historical placement is recorded in `../../PROVENANCE.md`.

## Source Surfaces

- [MEMORY_WRITE_PATH_GUARDRAILS](../../docs/MEMORY_WRITE_PATH_GUARDRAILS.md)
- `schemas/memory_write_path_guard_v1.json`
- `examples/memory_write_path_guard.untrusted_prompt_injection.example.json`
- `examples/memory_write_path_guard.reviewed_owner_candidate.example.json`

## Contract

keeps untrusted or derived memory writes candidate-bound until provenance, review route, derivation lineage, and action-safety separation are explicit

## Artifact Contract

This part owns the write-path guard schema and examples. The schema keeps
source trust, ingestion risks, derivation lineage, review route, proposed
lifecycle, action-safety separation, and allowed write result in one auditable
record.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
