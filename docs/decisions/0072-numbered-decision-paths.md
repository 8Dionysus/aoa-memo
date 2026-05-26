# Numbered Decision Paths

- Decision ID: AOA-MEM-D-0072

## Status

Accepted on 2026-05-26.

## Index Metadata

- Original date: 2026-05-26
- Legacy path: none
- Surface classes: root/topology, generated/readout, validation guard, legacy/provenance
- Mechanic parents: none
- Guard families: decision index/read-model, docs route, generated/read-model, release/tooling
- Memory object classes: decision
- Posture: accepted addressing migration

## Context

AOA-MEM-D-0071 introduced canonical decision IDs, source-owned index metadata,
generated lookup indexes, and a dual-addressing alias map. That made the
decision lane ready for a path migration without losing date-path provenance.

Keeping the date-named files live after that hardening would make the canonical
ID lane weaker than intended: agents could inspect by number, but the source
surface would still teach date paths as the active route.

## Decision

Make numbered decision paths the active source format:

- `docs/decisions/0001-*.md`
- `docs/decisions/0002-*.md`
- `docs/decisions/####-*.md`

Each existing decision note now carries:

- `Original date`, used by generated date indexes after the filename no longer
  starts with a date;
- `Legacy path`, used by the generated alias map to route old date-path refs to
  the current numbered file.

The generated alias map now treats date-named paths as legacy aliases, not live
files. New decisions that never had a date-named path use `Legacy path: none`.

## Alternatives

Leaving the date-named files active would preserve compatibility but keep the
decision lane in a permanent transition state.

Creating date-named stub files would make old links resolve directly, but it
would also create duplicate source surfaces and invite agents to edit the wrong
file.

## Consequences

Agents should route by canonical decision ID or numbered path first. Old
date-path references remain recoverable through generated alias/read-model
surfaces.

The builder now validates numbered filename prefixes against `Decision ID`
numbers and can require `numbered_canonical` mode from the index contract.

## Affected Surfaces

- `docs/decisions/*.md`
- `docs/decisions/AGENTS.md`
- `docs/decisions/README.md`
- `docs/decisions/TEMPLATE.md`
- `docs/decisions/indexes/*`
- `scripts/root-topology/decision_index_common.py`
- `tests/root-topology/test_topology_spine.py`

## Verification

Use:

```bash
python scripts/root-topology/build_decision_indexes.py --check
python -m pytest -q tests/root-topology/test_topology_spine.py
python scripts/release/release_check.py
```
