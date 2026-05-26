# 2026-05-18: Land Agon and Titan as Memo Mechanics

- Decision ID: AOA-MEM-D-0004

## Index Metadata

- Surface classes: mechanic package
- Mechanic parents: agon, titan
- Guard families: mechanic topology
- Memory object classes: none
- Posture: active rationale

## Context

Agon and Titan were first moved out of flat docs-root placement into local
docs districts. That made the surface easier to inspect, but it kept both
families shaped like documentation districts even though they already had
repeatable mechanic traits: inputs, outputs, owner splits, stop-lines,
companion artifacts, validation, and legacy routing.

`Agents-of-Abyss` uses mechanic packages for this kind of owner-bounded work.
`aoa-memo` had already adopted that shape for adoption, writeback, and
retention.

## Decision

Move Agon and Titan from transitional docs districts into active memo mechanic
packages:

- `mechanics/agon/docs/`
- `mechanics/titan/docs/`

Each package gets a route card, mechanic card, direction, parts map, owner map,
provenance bridge, landing log, roadmap, docs subroute, and legacy route.
`config/memo_mechanics.json`, generated mechanics index coverage, AGENTS mesh
coverage, docs-district retirement checks, tests, and release validation become
the machine-checkable companion surface.

## Alternatives

- Keep Agon and Titan as docs districts. This preserved a clean folder, but it
  hid the owner split and mechanic contract that future work needs.
- Move only links while leaving the topology unchanged. This would reduce
  immediate churn, but it would keep Agon/Titan unlike the already landed
  memo mechanics.

## Consequences

- Active Agon and Titan source docs now route through `mechanics/<slug>/`.
- `docs/agon/` and `docs/titan/` are retired paths; any future reference to
  them must be provenance or decision history, not an active route.
- Companion artifacts were later moved into mechanic-local artifact lanes by
  [2026-05-18-mechanic-artifact-lanes](2026-05-18-mechanic-artifact-lanes.md).
- Stronger owner claims still route away: Agon source mechanics to
  `Agents-of-Abyss`, Titan role authority to `aoa-agents`, proof to
  `aoa-evals`, runtime to `abyss-stack`, graph lift to `aoa-kag`, and authored
  Sophian canon to `Tree-of-Sophia`.

## Affected Surfaces

- `mechanics/agon/`
- `mechanics/titan/`
- `config/memo_mechanics.json`
- `config/agents_mesh.json`
- `generated/memo_mechanics.min.json`
- `generated/agents_mesh.min.json`
- `scripts/validate_docs_districts.py`
- `scripts/validate_memo_mechanics.py`
- `tests/test_docs_districts.py`
- `tests/test_agents_mesh.py`

## Verification Route

```bash
python scripts/validate_docs_districts.py
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python scripts/release_check.py
```
