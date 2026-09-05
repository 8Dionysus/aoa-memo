# Retire Spark Lane and Legacy Mechanic Subtrees

- Decision ID: AOA-MEM-D-0090

## Status

Accepted on 2026-09-04.

## Index Metadata

- Original date: 2026-09-04
- Surface classes: root/topology, legacy/provenance, mechanic package, validation guard
- Mechanic parents: adoption, agon, antifragility, checkpoint, consumer-handoff, governance, lineage-harvest, operational-gate, questbook, readiness-boundary, recurrence-support, retention, shape-guard, titan, writeback
- Guard families: root technical district, AGENTS/mesh, mechanic topology, release/tooling
- Memory object classes: none
- Posture: accepted retirement; historical recovery remains pinned in Git

## Context

The maintained memo owner routes and functioning mechanic parts supersede the
repository-local Spark lane and the former `mechanics/*/legacy/` staging trees.
Keeping those scaffolds in the active tree makes retired validator, test, and
route obligations look current and leaves broken links after the active owners
have taken over.

## Decision

Retire these tracked subtrees from the active tree:

- `.agents/spark`
- `mechanics/adoption/legacy`
- `mechanics/agon/legacy`
- `mechanics/antifragility/legacy`
- `mechanics/checkpoint/legacy`
- `mechanics/consumer-handoff/legacy`
- `mechanics/governance/legacy`
- `mechanics/lineage-harvest/legacy`
- `mechanics/operational-gate/legacy`
- `mechanics/questbook/legacy`
- `mechanics/readiness-boundary/legacy`
- `mechanics/recurrence-support/legacy`
- `mechanics/retention/legacy`
- `mechanics/shape-guard/legacy`
- `mechanics/titan/legacy`
- `mechanics/writeback/legacy`

The complete pre-retirement source remains recoverable from the immutable
baseline commit [`dff1f7447cfe90e711ec720ef5d8062dfc400cf4`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4):

- [`.agents/spark`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/.agents/spark)
- [`mechanics/adoption/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/adoption/legacy)
- [`mechanics/agon/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/agon/legacy)
- [`mechanics/antifragility/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/antifragility/legacy)
- [`mechanics/checkpoint/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/checkpoint/legacy)
- [`mechanics/consumer-handoff/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/consumer-handoff/legacy)
- [`mechanics/governance/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/governance/legacy)
- [`mechanics/lineage-harvest/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/lineage-harvest/legacy)
- [`mechanics/operational-gate/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/operational-gate/legacy)
- [`mechanics/questbook/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/questbook/legacy)
- [`mechanics/readiness-boundary/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/readiness-boundary/legacy)
- [`mechanics/recurrence-support/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/recurrence-support/legacy)
- [`mechanics/retention/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/retention/legacy)
- [`mechanics/shape-guard/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/shape-guard/legacy)
- [`mechanics/titan/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/titan/legacy)
- [`mechanics/writeback/legacy`](https://github.com/8Dionysus/aoa-memo/tree/dff1f7447cfe90e711ec720ef5d8062dfc400cf4/mechanics/writeback/legacy)

Historical provenance points to these pinned commit paths only. Current
references route to each package's active `README.md`, `PROVENANCE.md`, docs,
and functioning parts. No archive directory, service, role, runtime, or
memory-object history is introduced.

## Consequences

- Retired scaffolding no longer participates in active AGENTS, topology,
  validator, test, release, or generated mesh contracts.
- Existing active mechanic docs and parts remain the source for current work.
- Historical recovery is explicit and immutable through the baseline commit;
  Git history remains the recovery mechanism.
- This is a structural/provenance change, not proof, runtime, role, or owner
  acceptance evidence.

## Alternatives

- Keep the retired trees under a new archive directory. Rejected because it
  would create a second active-looking owner surface and duplicate recovery.
- Keep the Spark lane and legacy trees but mark them inactive. Rejected because
  inactive scaffolding still retains validator and test obligations.

## Affected Surfaces

- `.agents/` route metadata and mesh
- mechanic package READMEs and provenance bridges
- `config/agents/agents_mesh.json`
- `config/validation_lanes.json`
- generated topology and mechanic companions
- root-topology, agent-mesh, mechanic, and test inventories

## Verification

Run focused AGENTS mesh, root-topology, mechanic-topology, generated-parity,
and repository validation after rebuilding generated companions. Confirm that
all retired paths are absent, active owner routes remain present, and the
baseline commit links resolve without treating historical material as current
source.
