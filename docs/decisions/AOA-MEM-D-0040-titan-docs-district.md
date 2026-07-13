# Move Titan Memo Docs Into `docs/titan/`

- Decision ID: AOA-MEM-D-0040

Date: 2026-05-18

## Index Metadata

- Original date: 2026-05-18
- Surface classes: root/topology, mechanic package
- Mechanic parents: titan
- Guard families: docs route
- Memory object classes: none
- Posture: active rationale

## Context

After the Agon district landed, the next flat owner family was Titan. The root
docs map still exposed Titan memory posture, remembrance, and audit-memory
surfaces from the flat docs root, and examples/tests held explicit source refs
to those flat paths.

## Decision

Move all current Titan docs-root files into `docs/titan/`.

Add `docs/titan/AGENTS.md` as the local route card, `docs/titan/README.md` as
the district map, and extend `scripts/validate_docs_districts.py` so Titan docs
cannot drift back into the flat docs root.

Update README, examples, and tests to use `docs/titan/` source refs.

## Alternatives Considered

1. Leave Titan docs flat until every remaining docs family is ready.
   This would keep compatibility but leave an already coherent owner family
   mixed into the flat docs root.
2. Move Titan together with adoption, writeback, and retention.
   That would create a larger review surface and mix different stop-lines.
3. Move only Titan now, with a local route card, map, validator extension,
   decision record, and release gate.
   This keeps the sequence bounded after Agon.

## Consequences

- `docs/titan/` is now the source home for Titan memo posture docs.
- Old flat Titan docs-root refs are validator failures.
- Titan schemas, examples, and tests stay in their current technical homes,
  but their source refs now point at `docs/titan/`.
- The move does not grant memory write authority, role rights, proof status,
  private retention, or owner-repo source authority to `aoa-memo`.

## Affected Surfaces

- `docs/titan/AGENTS.md`
- `docs/titan/README.md`
- `docs/titan/TITAN_*.md`
- `README.md`
- `examples/titan_*.json`
- `tests/test_titan_*.py`
- `scripts/validate_docs_districts.py`
- `tests/test_docs_districts.py`
- `config/agents_mesh.json`
- `generated/agents_mesh.min.json`

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
