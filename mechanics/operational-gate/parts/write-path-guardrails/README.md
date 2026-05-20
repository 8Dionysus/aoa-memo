# Write path guardrails

This active part belongs to `mechanics/operational-gate/` and materializes the matching row in `../../PARTS.md`.

## Start Here

- [CONTRACT](CONTRACT.md)
- [VALIDATION](VALIDATION.md)

## Source Surfaces

- [MEMORY_WRITE_PATH_GUARDRAILS](../../docs/MEMORY_WRITE_PATH_GUARDRAILS.md)
- `schemas/memory_write_path_guard_v1.json`
- `examples/memory_write_path_guard.untrusted_prompt_injection.example.json`
- `examples/memory_write_path_guard.reviewed_owner_candidate.example.json`

## Function

keeps untrusted or derived memory writes candidate-bound until provenance, review route, derivation lineage, and action-safety separation are explicit

## Next Route

Use `../../OWNER_MAP.md` for stronger owner routing and `../../PROVENANCE.md` for placement history.
