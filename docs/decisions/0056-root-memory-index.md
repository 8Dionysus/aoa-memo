# Root Memory Index

- Decision ID: AOA-MEM-D-0056

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-19
- Surface classes: root/topology, memory doctrine, generated/readout
- Mechanic parents: none
- Guard families: docs route, generated/read-model, memory surface
- Memory object classes: none
- Posture: active rationale

## Context

The root document pass aligned `aoa-memo` with the mature root shapes in
`Agents-of-Abyss`, `aoa-techniques`, and `aoa-skills`: a compact README, a
charter, a design surface, agent route cards, a direction surface, and a
root-level index for the repo's primary public canon.

Before this change, `README.md` and docs maps carried too much memory-canon
orientation pressure. They needed to explain object kinds, support objects,
recall modes, temperature vocabulary, source families, generated companions,
and routing stop-lines while still staying readable as entrypoints.

## Decision

Add `MEMORY_INDEX.md` as the compact root memory-canon map.

`MEMORY_INDEX.md` may name object kinds, support objects, recall modes,
temperature vocabulary, source families, and generated companions. It routes
to stronger authored docs, schemas, examples, mechanics, generated companions,
validators, and sibling-owner repositories instead of replacing them.

Keep `README.md` as the public front door, `CHARTER.md` as the authority
boundary, `DESIGN.md` as system form, `DESIGN.AGENTS.md` as agent-surface
form, `AGENTS.md` as route law, `ROADMAP.md` as direction, and
`QUESTBOOK.md` as a compact obligation index.

## Alternatives

- Keep canon routing inside `README.md`. Rejected because the README would
  keep growing into a doctrine map instead of staying a public entrypoint.
- Put the canon map under `docs/`. Rejected because memory-object and recall
  vocabulary are root-level orientation for this repository, similar to a
  public index surface in sibling repos.
- Treat generated registry output as the index. Rejected because generated
  companions summarize and route; they do not own public doctrine or root
  orientation.

## Consequences

- Root entrypoints must route to `MEMORY_INDEX.md` when memory-canon shape is
  involved.
- `MEMORY_INDEX.md` must stay compact and link-driven.
- Generated registry and topology tests should recognize the index as a core
  public surface without promoting it over stronger doctrine.
- Contribution guidance should route executable validation through `AGENTS.md`
  and nearest local cards instead of copying large command batteries into
  every civic root document.

## Affected Surfaces

- `MEMORY_INDEX.md`
- `README.md`
- `AGENTS.md`
- `CHARTER.md`
- `DESIGN.md`
- `DESIGN.AGENTS.md`
- `ROADMAP.md`
- `CONTRIBUTING.md`
- `QUESTBOOK.md`
- `SECURITY.md`
- `docs/README.md`
- `docs/ROOT_SURFACE_LAW.md`
- `generated/memo_registry.min.json`
- `tests/test_topology_spine.py`

## Validation

Validate this decision through:

```bash
python scripts/validate_memo.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python -m pytest -q tests/test_topology_spine.py
python scripts/release_check.py
```
