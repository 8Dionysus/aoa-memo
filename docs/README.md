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
[root/ROOT_SURFACE_LAW](root/ROOT_SURFACE_LAW.md). Workspace release tooling
may enter through the thin [RELEASING](RELEASING.md) compatibility pointer.

## Districts

| District | Owns | Validation owner |
|---|---|---|
| [memory](memory/AGENTS.md) | memory model, object profiles, operation cycle, living topology, local memo ports, and narrative/core memory split | `memory/AGENTS.md` |
| [boundaries](boundaries/AGENTS.md) | repository owner split, operational boundary posture, and write-path guardrails | `boundaries/AGENTS.md` |
| [posture](posture/AGENTS.md) | trust, lifecycle, temperature, provenance, operation modes, and audit-event posture | `posture/AGENTS.md` |
| [root](root/AGENTS.md) | root placement law, release route, and preserved root reference | `root/AGENTS.md` |
| [decisions](decisions/AGENTS.md) | durable rationale for structural and route-law choices | decision-specific review plus release gate |
| [validation](validation/AGENTS.md) | validator boundary layers, command authority, validator inventory, route-away declarations, and release/nightly composition law | `validation/AGENTS.md` and `config/validation_lanes.json` |
| [testing](testing/AGENTS.md) | test topology, test inventory, and release-gate regression map | `testing/AGENTS.md` |

## Source Families

| Family | Current home | First route |
|---|---|---|
| Memory canon, object canon, and operation cycle | `docs/memory/` | [MEMORY_MODEL](memory/MEMORY_MODEL.md), [MEMORY_OPERATION_CYCLE](memory/MEMORY_OPERATION_CYCLE.md), then [MEMORY_OBJECT_PROFILES](memory/MEMORY_OBJECT_PROFILES.md) |
| Living memory topology and local ports | `docs/memory/` | [LIVING_MEMORY_TOPOLOGY](memory/LIVING_MEMORY_TOPOLOGY.md), then [LOCAL_MEMO_PORT_STANDARD](memory/LOCAL_MEMO_PORT_STANDARD.md) and [MEMO_PORT_INDEXING_VOCABULARY](memory/MEMO_PORT_INDEXING_VOCABULARY.md) |
| Boundary and operational posture | `docs/boundaries/` | [BOUNDARIES](boundaries/BOUNDARIES.md), [OPERATIONAL_BOUNDARY](boundaries/OPERATIONAL_BOUNDARY.md), then [MEMORY_WRITE_PATH_GUARDRAILS](boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md) |
| Lifecycle, trust, temperature, provenance, operation modes | `docs/posture/` | [MEMORY_TRUST_POSTURE](posture/MEMORY_TRUST_POSTURE.md), [LIFECYCLE](posture/LIFECYCLE.md), [MEMORY_TEMPERATURES](posture/MEMORY_TEMPERATURES.md), [MEMORY_OPERATION_MODES](posture/MEMORY_OPERATION_MODES.md), [PROVENANCE_THREADS](posture/PROVENANCE_THREADS.md) |
| Root law and release route | `docs/root/` plus thin `docs/RELEASING.md` compatibility pointer | [ROOT_SURFACE_LAW](root/ROOT_SURFACE_LAW.md), [RELEASING](root/RELEASING.md), [AGENTS_ROOT_REFERENCE](root/AGENTS_ROOT_REFERENCE.md) |
| Structural rationale | `docs/decisions/` | [decisions/README](decisions/README.md) |
| Validator topology | `docs/validation/` | [VALIDATOR_TOPOLOGY](validation/VALIDATOR_TOPOLOGY.md), [COMMAND_AUTHORITY](validation/COMMAND_AUTHORITY.md), [validator_inventory](validation/validator_inventory.json), then [validation_lanes](../config/validation_lanes.json) |
| Test topology | `docs/testing/` | [TEST_TOPOLOGY](testing/TEST_TOPOLOGY.md), then [test_inventory](testing/test_inventory.json) |

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
| Is this safe to write into memory? | [MEMORY_WRITE_PATH_GUARDRAILS](boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md), then [operational guard](../mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md) |
| What kind of memory object is it? | [MEMORY_INDEX](../MEMORY_INDEX.md), then [MEMORY_MODEL](memory/MEMORY_MODEL.md) and [MEMORY_OBJECT_PROFILES](memory/MEMORY_OBJECT_PROFILES.md) |
| What is the operational memory cycle? | [MEMORY_OPERATION_CYCLE](memory/MEMORY_OPERATION_CYCLE.md) |
| Which read/write mode applies? | [MEMORY_OPERATION_MODES](posture/MEMORY_OPERATION_MODES.md), then [memory operation modes example](../examples/recall/memory_operation_modes.example.json) |
| How does local project memory connect? | [LIVING_MEMORY_TOPOLOGY](memory/LIVING_MEMORY_TOPOLOGY.md), then [LOCAL_MEMO_PORT_STANDARD](memory/LOCAL_MEMO_PORT_STANDARD.md) and [MEMO_PORT_INDEXING_VOCABULARY](memory/MEMO_PORT_INDEXING_VOCABULARY.md) |
| Is this proof or verdict logic? | [BOUNDARIES](boundaries/BOUNDARIES.md), then route to `aoa-evals` |
| Is this routing behavior? | [ROUTING_MEMORY_ADOPTION](../mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md), then route to `aoa-routing` |
| Is this a role right or actor policy? | [AGENT_MEMORY_POSTURE_SEAM](../mechanics/consumer-handoff/docs/AGENT_MEMORY_POSTURE_SEAM.md), then route to `aoa-agents` |
| Is this a graph lift or retrieval substrate? | [KAG_SOURCE_EXPORT](../mechanics/consumer-handoff/docs/KAG_SOURCE_EXPORT.md), then route to `aoa-kag` |
| Is this a recurring cross-repo pattern or federation harvest candidate? | [PATTERN_LINEAGE_MEMORY](../mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md), then route stronger claims to source owners |
| Is this live runtime storage or retention? | [RUNTIME_WRITEBACK_SEAM](../mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md), then route to `abyss-stack` |
| Is this stale, duplicate, superseded, or ready to archive? | [CONSOLIDATION_FORGETTING_OPERATION](../mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md) |
| Where should a new root or docs-root file live? | [ROOT_SURFACE_LAW](root/ROOT_SURFACE_LAW.md) |
| Why was a structural route chosen? | [decisions](decisions/README.md) |

## Change Routes

| Change | First route |
|---|---|
| Memory canon map | [MEMORY_INDEX](../MEMORY_INDEX.md), then the stronger source doc it points to |
| Memory doctrine | [BOUNDARIES](boundaries/BOUNDARIES.md), [MEMORY_MODEL](memory/MEMORY_MODEL.md), and the target district `AGENTS.md` |
| Memory operation cycle or local memo ports | [MEMORY_OPERATION_CYCLE](memory/MEMORY_OPERATION_CYCLE.md), [LIVING_MEMORY_TOPOLOGY](memory/LIVING_MEMORY_TOPOLOGY.md), [LOCAL_MEMO_PORT_STANDARD](memory/LOCAL_MEMO_PORT_STANDARD.md), [MEMO_PORT_INDEXING_VOCABULARY](memory/MEMO_PORT_INDEXING_VOCABULARY.md), then [memory/AGENTS](memory/AGENTS.md) |
| Write-path safety | [MEMORY_WRITE_PATH_GUARDRAILS](boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md), [operational gate write path](../mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md), then [boundaries/AGENTS](boundaries/AGENTS.md) |
| Memory operation modes | [MEMORY_OPERATION_MODES](posture/MEMORY_OPERATION_MODES.md), [mode schema](../schemas/recall-posture/memory_operation_mode.schema.json), then [posture/AGENTS](posture/AGENTS.md) |
| Object canon or lifecycle | [MEMORY_OBJECT_PROFILES](memory/MEMORY_OBJECT_PROFILES.md), [MEMORY_TRUST_POSTURE](posture/MEMORY_TRUST_POSTURE.md), [LIFECYCLE](posture/LIFECYCLE.md) |
| Generated parity | source doc or manifest, builder, generated output, validator, and test together |
| Docs placement | [ROOT_SURFACE_LAW](root/ROOT_SURFACE_LAW.md) |
| Validation layers, command authority, validator inventory, lane hardness, or release/nightly composition | [validation/VALIDATOR_TOPOLOGY](validation/VALIDATOR_TOPOLOGY.md), [validation/COMMAND_AUTHORITY](validation/COMMAND_AUTHORITY.md), [validator_inventory](validation/validator_inventory.json), then [validation_lanes](../config/validation_lanes.json) |
| Test inventory or test topology | [testing/TEST_TOPOLOGY](testing/TEST_TOPOLOGY.md), then [test_inventory](testing/test_inventory.json) |
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
