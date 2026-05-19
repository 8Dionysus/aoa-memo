# Documentation Map

This is the map for the `docs/` district of `aoa-memo`.

Use the root [README](../README.md) as the public front door. Use this file
after entering `docs/` to choose the right memory-layer district, source
surface, and validator.

Editing under `docs/` starts with [AGENTS](AGENTS.md), then the placement rules
in [root/ROOT_SURFACE_LAW](root/ROOT_SURFACE_LAW.md). For agent-facing topology,
also read [DESIGN.AGENTS](../DESIGN.AGENTS.md).

## Start Here

For the shortest repo overview, read:

1. [README](../README.md)
2. [CHARTER](../CHARTER.md)
3. [DESIGN](../DESIGN.md)
4. [MEMORY_INDEX](../MEMORY_INDEX.md)
5. [boundaries/BOUNDARIES](boundaries/BOUNDARIES.md)
6. [memory/MEMORY_MODEL](memory/MEMORY_MODEL.md)

For current direction, add [ROADMAP](../ROADMAP.md). For release and root
placement work, add [root/RELEASING](root/RELEASING.md) and
[root/ROOT_SURFACE_LAW](root/ROOT_SURFACE_LAW.md).

## Districts

| District | Owns | Validator |
|---|---|---|
| [memory](memory/AGENTS.md) | memory model, object profiles, and narrative/core memory split | `python scripts/memory/validate_memo.py` |
| [boundaries](boundaries/AGENTS.md) | repository owner split and operational boundary posture | `python scripts/memory/validate_memo.py` |
| [posture](posture/AGENTS.md) | trust, lifecycle, temperature, provenance, and audit-event posture | `python scripts/memory/validate_lifecycle_audit_examples.py` |
| [root](root/AGENTS.md) | root placement law, release route, and preserved root reference | `python scripts/root-topology/validate_docs_districts.py` |
| [decisions](decisions/AGENTS.md) | durable rationale for structural and route-law choices | decision-specific review plus release gate |

## Source Families

| Family | Current home | First route |
|---|---|---|
| Memory canon and object canon | `docs/memory/` | [MEMORY_MODEL](memory/MEMORY_MODEL.md), then [MEMORY_OBJECT_PROFILES](memory/MEMORY_OBJECT_PROFILES.md) |
| Boundary and operational posture | `docs/boundaries/` | [BOUNDARIES](boundaries/BOUNDARIES.md), then [OPERATIONAL_BOUNDARY](boundaries/OPERATIONAL_BOUNDARY.md) |
| Lifecycle, trust, temperature, provenance | `docs/posture/` | [MEMORY_TRUST_POSTURE](posture/MEMORY_TRUST_POSTURE.md), [LIFECYCLE](posture/LIFECYCLE.md), [MEMORY_TEMPERATURES](posture/MEMORY_TEMPERATURES.md), [PROVENANCE_THREADS](posture/PROVENANCE_THREADS.md) |
| Root law and release route | `docs/root/` | [ROOT_SURFACE_LAW](root/ROOT_SURFACE_LAW.md), [RELEASING](root/RELEASING.md), [AGENTS_ROOT_REFERENCE](root/AGENTS_ROOT_REFERENCE.md) |
| Structural rationale | `docs/decisions/` | [decisions/README](decisions/README.md) |

Mechanic docs live with their mechanics, not in `docs/`:
[mechanics/agon](../mechanics/agon/README.md),
[mechanics/titan](../mechanics/titan/README.md),
[mechanics/adoption](../mechanics/adoption/README.md),
[mechanics/governance](../mechanics/governance/README.md),
[mechanics/shape-guard](../mechanics/shape-guard/README.md),
[mechanics/checkpoint](../mechanics/checkpoint/README.md),
[mechanics/readiness-boundary](../mechanics/readiness-boundary/README.md),
[mechanics/consumer-handoff](../mechanics/consumer-handoff/README.md),
[mechanics/operational-gate](../mechanics/operational-gate/README.md),
[mechanics/recurrence-support](../mechanics/recurrence-support/README.md),
[mechanics/lineage-harvest](../mechanics/lineage-harvest/README.md),
[mechanics/questbook](../mechanics/questbook/README.md),
[mechanics/writeback](../mechanics/writeback/README.md),
[mechanics/retention](../mechanics/retention/README.md), and
[mechanics/antifragility](../mechanics/antifragility/README.md).

## Claim Routes

| Question | Route |
|---|---|
| Does this belong in memory at all? | [CHARTER](../CHARTER.md), then [BOUNDARIES](boundaries/BOUNDARIES.md) |
| What kind of memory object is it? | [MEMORY_INDEX](../MEMORY_INDEX.md), then [MEMORY_MODEL](memory/MEMORY_MODEL.md) and [MEMORY_OBJECT_PROFILES](memory/MEMORY_OBJECT_PROFILES.md) |
| Is this proof or verdict logic? | [BOUNDARIES](boundaries/BOUNDARIES.md), then route to `aoa-evals` |
| Is this routing behavior? | [ROUTING_MEMORY_ADOPTION](../mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md), then route to `aoa-routing` |
| Is this a role right or actor policy? | [AGENT_MEMORY_POSTURE_SEAM](../mechanics/consumer-handoff/docs/AGENT_MEMORY_POSTURE_SEAM.md), then route to `aoa-agents` |
| Is this a graph lift or retrieval substrate? | [KAG_SOURCE_EXPORT](../mechanics/consumer-handoff/docs/KAG_SOURCE_EXPORT.md), then route to `aoa-kag` |
| Is this a recurring cross-repo pattern or federation harvest candidate? | [PATTERN_LINEAGE_MEMORY](../mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md), then route stronger claims to source owners |
| Is this live runtime storage or retention? | [RUNTIME_WRITEBACK_SEAM](../mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md), then route to `abyss-stack` |
| Where should a new root or docs-root file live? | [ROOT_SURFACE_LAW](root/ROOT_SURFACE_LAW.md) |
| Why was a structural route chosen? | [decisions](decisions/README.md) |

## Change Routes

| Change | First route |
|---|---|
| Memory canon map | [MEMORY_INDEX](../MEMORY_INDEX.md), then the stronger source doc it points to |
| Memory doctrine | [BOUNDARIES](boundaries/BOUNDARIES.md), [MEMORY_MODEL](memory/MEMORY_MODEL.md), and the target district `AGENTS.md` |
| Object canon or lifecycle | [MEMORY_OBJECT_PROFILES](memory/MEMORY_OBJECT_PROFILES.md), [MEMORY_TRUST_POSTURE](posture/MEMORY_TRUST_POSTURE.md), [LIFECYCLE](posture/LIFECYCLE.md) |
| Generated parity | source doc or manifest, builder, generated output, validator, and test together |
| Docs placement | [ROOT_SURFACE_LAW](root/ROOT_SURFACE_LAW.md) |
| Mechanic docs | [mechanics](../mechanics/README.md), then the target mechanic `AGENTS.md` |
| Mechanic artifact placement | [mechanics/ARTIFACT_TOPOLOGY](../mechanics/ARTIFACT_TOPOLOGY.md) |
| Agent-facing shape | [DESIGN.AGENTS](../DESIGN.AGENTS.md), root [AGENTS](../AGENTS.md), and nearest local `AGENTS.md` |
| Decision rationale | [decisions/AGENTS](decisions/AGENTS.md), then [decisions/README](decisions/README.md) |
| Public release path | [root/RELEASING](root/RELEASING.md), then [CHANGELOG](../CHANGELOG.md) |

## Topology Rule

`docs/` is no longer a flat doctrine shelf. New current docs must enter the
nearest semantic district, and single-mechanic docs must enter the owning
mechanic package.

`scripts/root-topology/validate_docs_districts.py` checks that retired flat
docs and retired docs subdistricts do not return. The root technical district
atlas covers technical root homes; this docs map covers authored documentation
families.

## Adjacent Routes

| Route | Use |
|---|---|
| [schemas](../schemas/AGENTS.md) | memory, recall, support-object, and generated-surface contracts |
| [examples](../examples/AGENTS.md) | public-safe examples and manifests |
| [generated](../generated/AGENTS.md) | compact generated companions |
| [scripts](../scripts/AGENTS.md) | builders, validators, and publication helpers |
| [tests](../tests/AGENTS.md) | regression surfaces |
| [config](../config/AGENTS.md) | source maps and build inputs |
| [mechanics](../mechanics/README.md) | repeatable memo operations and their local docs |
| [manifests](../manifests/AGENTS.md) | reserved recurrence manifests |
| [quests](../quests/AGENTS.md) | quest files backing `QUESTBOOK.md` |
| [.agents](../.agents/AGENTS.md) | agent-facing companion lanes |
| [QUESTBOOK](../QUESTBOOK.md) | active memory-layer obligation index |

## Notes

- Prefer the nearest district `AGENTS.md` before editing a docs file.
- Prefer [ROOT_SURFACE_LAW](root/ROOT_SURFACE_LAW.md) before adding, moving, or
  deleting root or docs-root surfaces.
- Prefer [decisions](decisions/README.md) when future contributors need to know
  why a topology route exists.
- Prefer `config/agents/agents_mesh.json` and
  `generated/agents/agents_mesh.min.json` when a docs migration adds or changes
  local route cards.
- Prefer `scripts/root-topology/validate_docs_districts.py` when checking docs
  placement.
