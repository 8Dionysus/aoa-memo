# Root Semantic Topology

- Decision ID: AOA-MEM-D-0057

## Status

Accepted on 2026-05-19.

## Index Metadata

- Original date: 2026-05-19
- Legacy path: docs/decisions/2026-05-19-root-semantic-topology.md
- Surface classes: root/topology
- Mechanic parents: none
- Guard families: root technical district
- Memory object classes: none
- Posture: active rationale

## Context

`aoa-memo` had already moved many mechanic-owned artifacts into mechanics and
parts, but the root districts still read like file buckets. `docs/`,
`schemas/`, `examples`, `generated`, `scripts`, `tests`, and `config` exposed
long flat lists where meaning had to be inferred from filenames.

That shape was too weak for OS Abyss use. A future agent needs to know which
family a file belongs to, which surface owns the source truth, which companion
is generated, and which validator proves the route is still current.

## Decision

Make the active root districts semantic and family-shaped:

- `docs/` is split into `memory/`, `boundaries/`, `posture/`, `root/`, and
  `decisions/`.
- `schemas/` is split into memory-object, recall-posture, support-object, and
  generated-surface contracts.
- `examples/` is split into memory objects, lifecycle, Phase Alpha, recall,
  support objects, and generated-surface manifests.
- `generated/` is split into memory, memory-object, AGENTS, mechanics,
  Questbook, and root-topology companions.
- `scripts/` is split into memory, AGENTS, mechanics, root-topology, and
  release entrypoints.
- `tests/` is split into memory, AGENTS, mechanics, and root-topology
  regression districts.
- `config/` is split into AGENTS mesh, mechanics, and root-topology source
  maps.

Every new district gets a nearest `AGENTS.md`. The source-backed AGENTS mesh
names those cards. The root technical district contract keeps exact allowed
technical files, while `validate_docs_districts.py` keeps docs-root topology
from sliding back into a flat shelf.

## Alternatives

Leaving the root districts flat would preserve short paths, but it would keep
the semantic work in human memory instead of the repository shape.

Moving everything into mechanics was rejected because several families are
repo-wide: memory canon, support contracts, generated companions, AGENTS mesh,
release gates, and cross-mechanic regression surfaces.

Creating only documentation indexes was rejected because the topology must be
machine-checkable through validators and generated companions, not only
explained in prose.

## Consequences

- File location now carries meaning: family, source, generated status, owner
  route, and validation route are visible from the path and nearest AGENTS card.
- Old flat root files in technical districts are release-gate failures unless
  added intentionally to the family contract.
- Docs-root additions must enter a semantic district or a mechanic package.
- Generated companions must continue to mirror their source families after
  every topology change.
- Historical changelog entries and raw legacy/source vocabulary may preserve
  old names when they are provenance rather than active topology.

## Affected Surfaces

- `docs/{memory,boundaries,posture,root,decisions}/`
- `schemas/{memory-objects,recall-posture,support-objects,generated-surfaces}/`
- `examples/{memory-objects,lifecycle,phase-alpha,recall,support-objects,generated-surfaces}/`
- `generated/{memory,memory-objects,agents,mechanics,quests,root-topology}/`
- `scripts/{memory,agents,mechanics,root-topology,release}/`
- `tests/{memory,agents,mechanics,root-topology}/`
- `config/{agents,mechanics,root-topology}/`
- `config/agents/agents_mesh.json`
- `config/root-topology/root_technical_districts.json`
- `generated/agents/agents_mesh.min.json`
- `generated/root-topology/root_technical_districts.min.json`
- `README.md`
- `MEMORY_INDEX.md`
- `AGENTS.md`
- `docs/README.md`
- `docs/root/ROOT_SURFACE_LAW.md`
- `CHANGELOG.md`

## Verification

Use:

```bash
python scripts/root-topology/validate_docs_districts.py
python scripts/mechanics/validate_mechanic_artifact_topology.py
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/agents/validate_semantic_agents.py
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memory_object_surfaces.py
python -m pytest -q
python scripts/release/release_check.py
```
