# Decision: Questbook Uses A Lane-First Root Store

- Decision ID: AOA-MEM-D-0026

## Index Metadata

- Original date: 2026-05-18
- Surface classes: mechanic package, quest/lane
- Mechanic parents: questbook
- Guard families: quest/read-model
- Memory object classes: none
- Posture: active rationale

## Context

`aoa-memo` already had root `QUESTBOOK.md`, flat `quests/AOA-MEM-Q-*.yaml`
files, generated quest catalog and dispatch projections, and several
Agon-specific follow-through Markdown notes in root `quests/`.

`Agents-of-Abyss` uses a clearer pattern: `mechanics/questbook/` owns quest
law and quest read-model projections, while root `quests/` remains a public item store with
lane-first lifecycle placement.

## Decision

Adopt the same model in `aoa-memo`.

Questbook law, source contracts, validation, and the generated projection
builder live under `mechanics/questbook/`. Root `QUESTBOOK.md` remains the
compact public index. Root `quests/` remains the public item store, now shaped
as `quests/<lane>/<state>/<quest-id>`.

## Alternatives

- Move Agon follow-through notes into `mechanics/agon/quests/`. This made the
  item store look cleaner but diverged from the Questbook pattern.
- Keep all quest files flat under root `quests/`. This preserved old paths but
  left lifecycle and lane ownership weak.
- Convert every quest source to generated-only surfaces. This would invert
  authority by making projections feel source-like.

## Consequences

- `quests/` is not treated as generic root technical debt.
- Quest source files can remain public and durable while still naming owner
  lanes and lifecycle states.
- Generated quest surfaces remain builder-backed projections.
- Future quest growth should extend `mechanics/questbook/` before adding new
  root quest shapes.

## Affected Surfaces

- `mechanics/questbook/`
- `QUESTBOOK.md`
- `quests/`
- `mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py`
- `generated/quest_catalog*.json`
- `generated/quest_dispatch*.json`
- `scripts/validate_memo.py`
- `scripts/release_check.py`
- `config/memo_mechanics.json`
- `config/agents_mesh.json`

## Verification Route

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
