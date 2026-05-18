# Adoption, Writeback, and Retention Move to Memo Mechanics

## Status

Accepted.

## Context

`aoa-memo` already moved Agon and Titan into docs districts because those
families are primarily source documents with local route cards.

Adoption, writeback, and retention are different. They describe repeatable
memory-layer moves: a candidate becomes reviewable for adoption, a writeback
target or intake crosses owner boundaries, and retention evidence remains
visible without runtime execution. Treating these as ordinary docs
subdirectories would hide the owner split, legacy route, and validation shape.

`Agents-of-Abyss` provides the stronger topology pattern: mechanics packages
with route cards, package cards, owner maps, provenance bridges, landing logs,
roadmaps, active docs, and legacy routes.

## Decision

Move the former flat adoption, writeback, and retention docs-root surfaces into
memo mechanic packages:

- `mechanics/adoption/docs/`
- `mechanics/writeback/docs/`
- `mechanics/retention/docs/`

Each package has:

- `AGENTS.md`
- `README.md`
- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/README.md`
- `legacy/INDEX.md`

Add `config/memo_mechanics.json`,
`generated/memo_mechanics.min.json`, and mechanics validators so the mechanic
shape is machine-checkable.

## Consequences

- `docs/` remains the doctrine map, not the owner for these repeatable moves.
- Old flat docs-root paths are allowed only as provenance or legacy mappings in
  `config/memo_mechanics.json` and mechanic legacy indexes.
- Generated companions, examples, quests, scripts, and tests must point at the
  mechanic-owned source docs.
- `aoa-memo` still does not claim proof, route implementation, role rights,
  runtime writeback, or retention execution.

## Alternatives Considered

- Keep `docs/adoption/`, `docs/writeback/`, and `docs/retention/` as thematic
  docs districts. Rejected because it flattens actual mechanics into
  documentation folders.
- Move all related schemas, examples, generated files, scripts, and tests into
  mechanic-local artifact homes immediately. Deferred because many of those
  artifacts are still shared repo-wide contracts; this change first establishes
  the owner mechanic and validator.

## Validation

The mechanic route is checked by:

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/release_check.py
```
