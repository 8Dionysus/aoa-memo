# Numbered Decision Paths

- Decision ID: AOA-MEM-D-0072

## Status

Accepted on 2026-05-26.

Superseded in part on 2026-05-26 by
[AOA-MEM-D-0073 Numbered Decision Route Completion](AOA-MEM-D-0073-numbered-decision-route-completion.md):
the transitional date-path compatibility metadata and generated read models are
retired from the active repository surface.

Superseded in path format on 2026-05-26 by
[AOA-MEM-D-0074 Full Canonical ID Decision Filenames](AOA-MEM-D-0074-full-canonical-id-decision-filenames.md):
source filenames now carry the complete `AOA-MEM-D-####` prefix, not only the
numeric portion.

## Index Metadata

- Original date: 2026-05-26
- Surface classes: root/topology, generated/readout, validation guard, legacy/provenance
- Mechanic parents: none
- Guard families: decision index/read-model, docs route, generated/read-model, release/tooling
- Memory object classes: decision
- Posture: accepted addressing migration

## Context

AOA-MEM-D-0071 introduced canonical decision IDs, source-owned index metadata,
generated lookup indexes, and a temporary compatibility bridge. That made the
decision lane ready for a path migration without renaming files before the
lookup contract existed.

Keeping the date-named files live after that hardening would make the canonical
ID lane weaker than intended: agents could inspect by number, but the source
surface would still teach date paths as the active route.

## Decision

Make short numbered decision paths the active source format for this migration
slice. A later decision replaces that transitional path format with full
canonical-ID filenames.

Each existing decision note now carries:

- `Original date`, used by generated date indexes after the filename no longer
  starts with a date.

## Alternatives

Leaving the date-named files active would preserve compatibility but keep the
decision lane in a permanent transition state.

Creating date-named stub files would make old links resolve directly, but it
would also create duplicate source surfaces and invite agents to edit the wrong
file.

## Consequences

Agents should route by canonical decision ID or numbered path first. Old
date-path references are historical references, not repository lookup routes.

For this slice, the builder validated filename prefixes against `Decision ID`
numbers and could require the then-current path mode from the index contract.

## Affected Surfaces

- `docs/decisions/*.md`
- `docs/decisions/AGENTS.md`
- `docs/decisions/README.md`
- `docs/decisions/TEMPLATE.md`
- `docs/decisions/indexes/*`
- `scripts/root-topology/decision_index_common.py`
- `tests/root-topology/test_topology_spine.py`

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
