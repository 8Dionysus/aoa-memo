# Move Agon Memo Docs Into `docs/agon/`

- Decision ID: AOA-MEM-D-0003

Date: 2026-05-18

## Index Metadata

- Original date: 2026-05-18
- Surface classes: root/topology, mechanic package
- Mechanic parents: agon
- Guard families: docs route
- Memory object classes: none
- Posture: active rationale

## Context

`aoa-memo` had 27 flat Agon docs-root surfaces. The root topology spine
explicitly warned that Agon docs should not be moved as cosmetic cleanup. After
the AGENTS mesh landed, the repository had enough route-card and generated
coverage to move one owner family with a local map and validator.

## Decision

Move all current Agon docs-root files into `docs/agon/`.

Add `docs/agon/AGENTS.md` as the local route card, `docs/agon/README.md` as the
district map, and `scripts/validate_docs_districts.py` as the validator that
prevents old flat Agon docs-root paths from returning.

Update recurrence manifests and hook manifests from their old flat Agon refs to
`docs/agon/AGON_*.md`.

## Alternatives Considered

1. Leave Agon docs flat and only document the future move.
   This would keep the first topology spine honest but leave the largest
   clearly named owner family in the flat docs root.
2. Move Agon, Titan, adoption, retention, rollback, and writeback together.
   That would be faster but harder to review and easier to break links.
3. Move only Agon now, with a route card, map, validator, decision record, and
   release gate.
   This keeps the migration bounded and gives later districts a repeatable
   pattern.

## Consequences

- `docs/agon/` is now the source home for Agon memo docs.
- Old flat Agon docs-root references are validator failures.
- Agon-specific config, schemas, examples, generated registries, manifests,
  quests, scripts, and tests remain in their current technical homes; this
  change only moves the authored docs district.
- The move does not grant `aoa-memo` authority over Agon verdicts, rank,
  durable scars, KAG promotion, Tree-of-Sophia canon, or runtime retention.

## Affected Surfaces

- `docs/agon/AGENTS.md`
- `docs/agon/README.md`
- `docs/agon/AGON_*.md`
- `manifests/recurrence/component.agon.*`
- `manifests/recurrence/hooks/component.agon.*`
- `scripts/validate_docs_districts.py`
- `tests/test_docs_districts.py`
- `config/agents_mesh.json`
- `generated/agents_mesh.min.json`

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
