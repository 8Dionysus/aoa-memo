# Prebinding and candidate intake

This active part belongs to `mechanics/agon/` and materializes the matching row in `../../PARTS.md`.

## Start Here

- [CONTRACT](CONTRACT.md)
- [VALIDATION](VALIDATION.md)

## Source Surfaces

- [AGON_MEMORY_PREBINDING](../../docs/AGON_MEMORY_PREBINDING.md)
- [AGON_DELTA_CHRONICLE_PREBINDING_MODEL](../../docs/AGON_DELTA_CHRONICLE_PREBINDING_MODEL.md)
- [AGON_SCAR_CANDIDATE_INTAKE_MODEL](../../docs/AGON_SCAR_CANDIDATE_INTAKE_MODEL.md)
- [AGON_SCAR_REQUEST_INTAKE_ALIGNMENT](../../docs/AGON_SCAR_REQUEST_INTAKE_ALIGNMENT.md)
- [AGON_RETENTION_CANDIDATE_BOUNDARY](../../docs/AGON_RETENTION_CANDIDATE_BOUNDARY.md)
- [AGON_RETENTION_CANDIDATE_INTAKE](../../docs/AGON_RETENTION_CANDIDATE_INTAKE.md)
- [AGON_MEMO_RECURRENCE_REVIEW_BOUNDARY](../../docs/AGON_MEMO_RECURRENCE_REVIEW_BOUNDARY.md)
- [AGON_RANK_MEMORY_BOUNDARY](../../docs/AGON_RANK_MEMORY_BOUNDARY.md)

## Function

keeps candidate memory explicit before any stronger Agon write

## Technical Homes

- `config/`, `generated/`, `schemas/`, `scripts/`, and `tests/` own memo
  prebinding and retention-rank candidate intake companions.
- `manifests/` owns recurrence components and hook bindings for this part.

## Next Route

Use `../../OWNER_MAP.md` for stronger owner routing and `../../PROVENANCE.md` for placement history.
