# Add Source-Backed AGENTS Mesh for Route Cards

Date: 2026-05-18

## Context

`aoa-memo` now has a topology spine and local route cards across the main
repository districts. The agent-facing design named a later
`config/agents_mesh.json` and `generated/agents_mesh.min.json`, but the current
route cards were still checked by several partial validators rather than one
source-backed mesh.

The next topology step is to make the current card set machine-checkable before
moving thematic docs. That gives later Agon, Titan, adoption, writeback, and
retention migrations a stable way to prove their local route cards are present.

## Decision

Add `config/agents_mesh.json` as the source of truth for current AGENTS route
cards, and generate `generated/agents_mesh.min.json` from it.

The mesh validator checks:

- every registered card exists
- registered cards keep a level-1 heading, enough local guidance, and required
  memory-layer snippets
- no unregistered `AGENTS.md` cards are present
- tracked top-level directories have local `AGENTS.md` route cards
- the generated mesh mirror is reproducible from source

Add missing top-level route cards for `manifests/` and `quests/` instead of
exempting them, because both directories already hold durable public surfaces.
Ignore `.deps/` dependency checkouts because their `AGENTS.md` cards belong to
sibling repositories, not to the local `aoa-memo` mesh.

## Alternatives Considered

1. Keep only the existing semantic and nested AGENTS validators.
   This would preserve current checks but leave no single route-card map for
   later district migrations.
2. Copy the stricter canonical-heading mesh from `aoa-techniques`.
   That would overfit `aoa-memo` to a sibling repository and force noisy
   rewrite of existing cards before the docs districts move.
3. Add a source-backed mesh that validates the current card form.
   This keeps the repo's own route language while making the card set
   reproducible.

## Consequences

- Future route-card additions must update `config/agents_mesh.json`, rebuild
  `generated/agents_mesh.min.json`, and pass the mesh validators.
- `generated/agents_mesh.min.json` is a companion mirror only. It does not
  replace root `AGENTS.md`, local cards, source docs, schemas, examples, or
  validators.
- Later Agon, Titan, adoption, writeback, and retention districts can add their
  own cards through this mesh rather than relying on flat-doc memory.
- CI dependency checkouts under `.deps/` do not become route-card migration
  pressure for this repository.

## Affected Surfaces

- `config/agents_mesh.json`
- `generated/agents_mesh.min.json`
- `scripts/agents_mesh_common.py`
- `scripts/build_agents_mesh_index.py`
- `scripts/validate_agents_mesh.py`
- `scripts/validate_agents_mesh_index.py`
- `manifests/AGENTS.md`
- `quests/AGENTS.md`
- `tests/test_agents_mesh.py`

## Verification

```bash
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python scripts/release_check.py
```
