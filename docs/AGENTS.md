# AGENTS.md

## Guidance for `docs/`

`docs/` explains memory models, boundaries, lifecycle, trust posture, writeback, recall, KAG bridge, and neighboring-layer seams.

Docs may define doctrine for memo surfaces, but they must preserve the boundary: memory is not proof, not execution, not routing authority, and not runtime infrastructure.

Keep provenance, temporal relevance, salience, temperature, and recall pressure explicit. Avoid making durable-consequence claims without matching schemas, examples, and validators.

When docs change proof, routing, KAG, role, or playbook seams, name the downstream owner repo and what remains outside memo authority.

## Route Stack

- Above: root `AGENTS.md` chooses the route mode; `docs/README.md` maps the
  docs district.
- Here: root docs own memory doctrine, boundaries, lifecycle, trust,
  temperature, provenance, and root-surface placement.
- Below: `docs/decisions/` owns decision rationale, `docs/validation/` owns
  validator topology and lane hardness, and `docs/testing/` owns test topology
  plus test inventory. Mechanic doctrine lives under `mechanics/<slug>/docs/`
  once a mechanic owns the surface.

## Migration Posture

- Do not move flat docs into thematic subdirectories because the directory
  looks crowded.
- A docs migration needs an owner family, source map, updated links, validator
  or test coverage, and a decision record when the route matters later.
- Use `ROOT_SURFACE_LAW.md` before adding, moving, deleting, or rewriting a
  root or docs-root surface.
- When a mechanic owns the surface, route to the nearest
  `mechanics/<slug>/AGENTS.md` before changing active docs.
- When validation layers, lane ownership, or release/nightly composition change,
  route to `docs/validation/AGENTS.md` and `config/validation_lanes.json`.
- When test inventory changes, route to `docs/testing/AGENTS.md`.

Verify with:

```bash
python scripts/memory/validate_memo.py
python scripts/agents/validate_semantic_agents.py
```
