# aoa-memo

`aoa-memo` is the memory and recall layer of the AoA ecosystem.

A memory object here is explicit, temporal, source-aware, and reviewable. It is
not proof, not route sovereignty, not runtime state, not role authority, and not
source-authored knowledge.

Use this README as the public front door. When work becomes doctrinal,
mechanic-local, generated, schema-backed, quest-bound, or agent-facing, follow
the linked owner surface instead of expanding this page.

> Current release: `v0.4.0`. See [CHANGELOG](CHANGELOG.md) for release notes.

## What This Repository Does

| Function | Surface |
|---|---|
| Repository authority boundary | [CHARTER](CHARTER.md) |
| Memory-layer system form | [DESIGN](DESIGN.md) |
| Agent-facing guidance form | [DESIGN.AGENTS](DESIGN.AGENTS.md) |
| Public memory canon map | [MEMORY_INDEX](MEMORY_INDEX.md) |
| Reviewed memory object corpus | [memo](memo/README.md) |
| Memory model, operation cycle, and object posture | [MEMORY_MODEL](docs/memory/MEMORY_MODEL.md), [MEMORY_OPERATION_CYCLE](docs/memory/MEMORY_OPERATION_CYCLE.md), [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| Living memory topology and local ports | [LIVING_MEMORY_TOPOLOGY](docs/memory/LIVING_MEMORY_TOPOLOGY.md), [LOCAL_MEMO_PORT_STANDARD](docs/memory/LOCAL_MEMO_PORT_STANDARD.md), [MEMO_PORT_INDEXING_VOCABULARY](docs/memory/MEMO_PORT_INDEXING_VOCABULARY.md) |
| Trust, temperature, lifecycle, operation modes, and provenance posture | [MEMORY_TRUST_POSTURE](docs/posture/MEMORY_TRUST_POSTURE.md), [MEMORY_TEMPERATURES](docs/posture/MEMORY_TEMPERATURES.md), [LIFECYCLE](docs/posture/LIFECYCLE.md), [MEMORY_OPERATION_MODES](docs/posture/MEMORY_OPERATION_MODES.md), [PROVENANCE_THREADS](docs/posture/PROVENANCE_THREADS.md) |
| Root and docs placement law | [ROOT_SURFACE_LAW](docs/root/ROOT_SURFACE_LAW.md) |
| Documentation map | [docs](docs/README.md) |
| Memo-side mechanics | [mechanics](mechanics/README.md) |
| Agent route law and local checks | [AGENTS](AGENTS.md) |
| Direction and obligations | [ROADMAP](ROADMAP.md), [QUESTBOOK](QUESTBOOK.md) |

This repository is strongest when it makes memory inspectable and bounded. It
is weakest when it tries to become proof, routing, runtime, role policy, graph
substrate, playbook choreography, or the source meaning of neighboring layers.

## Start Here

Read only the surface that matches the job.

| Need | Route |
|---|---|
| Shortest honest overview | this README -> [CHARTER](CHARTER.md) -> [DESIGN](DESIGN.md) -> [MEMORY_INDEX](MEMORY_INDEX.md) |
| Memory object canon | [MEMORY_INDEX](MEMORY_INDEX.md) -> [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| Reviewed memory object corpus | [memo](memo/README.md) -> [OBJECT_SHAPE](memo/OBJECT_SHAPE.md) |
| Reviewed intake landing | [memo](memo/README.md) -> [memo AGENTS](memo/AGENTS.md) -> [land_reviewed_memo_intake](scripts/memory/land_reviewed_memo_intake.py) |
| Memory doctrine | [MEMORY_MODEL](docs/memory/MEMORY_MODEL.md), [BOUNDARIES](docs/boundaries/BOUNDARIES.md), then the target doctrine file |
| Memory operation cycle | [MEMORY_OPERATION_CYCLE](docs/memory/MEMORY_OPERATION_CYCLE.md) |
| Write-path safety | [MEMORY_WRITE_PATH_GUARDRAILS](docs/boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md), then [operational gate guardrails](mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md) |
| Operation modes | [MEMORY_OPERATION_MODES](docs/posture/MEMORY_OPERATION_MODES.md), then [operation mode example](examples/recall/memory_operation_modes.example.json) |
| Local project memory ports | [LIVING_MEMORY_TOPOLOGY](docs/memory/LIVING_MEMORY_TOPOLOGY.md), then [LOCAL_MEMO_PORT_STANDARD](docs/memory/LOCAL_MEMO_PORT_STANDARD.md) and [MEMO_PORT_INDEXING_VOCABULARY](docs/memory/MEMO_PORT_INDEXING_VOCABULARY.md) |
| Memory readiness pressure | [MEMORY_READINESS_BOUNDARY](mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md) |
| Memo mechanic work | [mechanics](mechanics/README.md), then the nearest mechanic `AGENTS.md` |
| Consumer handoff | [consumer-handoff](mechanics/consumer-handoff/README.md), [PLAYBOOK_MEMORY_SCOPES](mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md), [KAG_SOURCE_EXPORT](mechanics/consumer-handoff/docs/KAG_SOURCE_EXPORT.md), or [MEMORY_EVAL_GUARDRAILS](mechanics/consumer-handoff/docs/MEMORY_EVAL_GUARDRAILS.md) |
| Router-facing recall adoption | [ROUTING_MEMORY_ADOPTION](mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md) |
| Self-agency continuity writeback | [SELF_AGENCY_CONTINUITY_WRITEBACK](mechanics/writeback/docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md) |
| Root or docs-root placement | [ROOT_SURFACE_LAW](docs/root/ROOT_SURFACE_LAW.md) |
| Current direction | [ROADMAP](ROADMAP.md) |
| Agent editing route | [AGENTS](AGENTS.md), then the nearest nested `AGENTS.md` |

## Memory Check

Before adding, trusting, or publishing a memo claim, ask the narrowest owner.

| Claim question | Check |
|---|---|
| May `aoa-memo` say this at all? | [CHARTER](CHARTER.md), then [BOUNDARIES](docs/boundaries/BOUNDARIES.md) |
| May this source write into memory? | [MEMORY_WRITE_PATH_GUARDRAILS](docs/boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md) and [MEMORY_WRITE_PATH_GUARDRAILS](mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md) |
| What memory object kind is this? | [MEMORY_INDEX](MEMORY_INDEX.md), then [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| What part of the memory cycle is this? | [MEMORY_OPERATION_CYCLE](docs/memory/MEMORY_OPERATION_CYCLE.md) |
| What read/write posture should this task use? | [MEMORY_OPERATION_MODES](docs/posture/MEMORY_OPERATION_MODES.md) |
| Is this proof, verdict logic, or scoring? | [BOUNDARIES](docs/boundaries/BOUNDARIES.md), then route to `aoa-evals` |
| Is this dispatch or route policy? | [ROUTING_MEMORY_ADOPTION](mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md), then route to `aoa-routing` |
| Is this role, persona, or handoff right? | [AGENT_MEMORY_POSTURE_SEAM](mechanics/consumer-handoff/docs/AGENT_MEMORY_POSTURE_SEAM.md), then route to `aoa-agents` |
| Is this playbook memory scope? | [PLAYBOOK_MEMORY_SCOPES](mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md), then route choreography to `aoa-playbooks` |
| Is this KAG or ToS handoff? | [KAG_SOURCE_EXPORT](mechanics/consumer-handoff/docs/KAG_SOURCE_EXPORT.md) and [KAG_TOS_BRIDGE_CONTRACT](mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md) |
| Is this live runtime retention or storage? | [RUNTIME_WRITEBACK_SEAM](mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md), then route to `abyss-stack` |
| Is this duplicate, superseded, stale, unsafe, or ready to archive? | [CONSOLIDATION_FORGETTING_OPERATION](mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md) |
| Is this current enough to recall? | [MEMORY_TRUST_POSTURE](docs/posture/MEMORY_TRUST_POSTURE.md), [MEMORY_TEMPERATURES](docs/posture/MEMORY_TEMPERATURES.md), and [LIFECYCLE](docs/posture/LIFECYCLE.md) |

## Current Contour

`aoa-memo` is in contract hardening.

The released `v0.4.0` contour is routed through these compact entrypoints:

- Authority and canon:
  [charter](CHARTER.md), [design](DESIGN.md), [memory index](MEMORY_INDEX.md),
  [memory model](docs/memory/MEMORY_MODEL.md), and
  [object profiles](docs/memory/MEMORY_OBJECT_PROFILES.md).
- Reviewed memory corpus:
  [memo](memo/README.md), [object shape](memo/OBJECT_SHAPE.md), and the first
  reviewed corpus decision bundle under
  [memo/objects/decisions/2026/reviewed-corpus-district](memo/objects/decisions/2026/reviewed-corpus-district/MEMO.md).
  Reviewed local-port exports with `allowed_result: reviewed_write` land
  through `scripts/memory/land_reviewed_memo_intake.py`.
- Trust, lifecycle, temperature, provenance, and operational boundary:
  [trust posture](docs/posture/MEMORY_TRUST_POSTURE.md),
  [lifecycle](docs/posture/LIFECYCLE.md),
  [temperatures](docs/posture/MEMORY_TEMPERATURES.md),
  [operation modes](docs/posture/MEMORY_OPERATION_MODES.md),
  [provenance threads](docs/posture/PROVENANCE_THREADS.md), and
  [operational boundary](docs/boundaries/OPERATIONAL_BOUNDARY.md).
- Memory operations and local growth:
  [operation cycle](docs/memory/MEMORY_OPERATION_CYCLE.md),
  [living memory topology](docs/memory/LIVING_MEMORY_TOPOLOGY.md),
  [local memo port standard](docs/memory/LOCAL_MEMO_PORT_STANDARD.md),
  [memo port indexing vocabulary](docs/memory/MEMO_PORT_INDEXING_VOCABULARY.md),
  [write-path boundary](docs/boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md),
  [write-path guard mechanic](mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md), and
  [consolidation/forgetting](mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md).
- Checkpoint and return recall:
  [checkpoint boundary](mechanics/checkpoint/docs/CHECKPOINT_MEMORY_BOUNDARY.md),
  [recurrence support](mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md),
  and [carry contract](mechanics/checkpoint/docs/CHECKPOINT_CARRY_CONTRACT.md).
- Consumer adoption and handoff:
  [routing adoption](mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md),
  [playbook memory scopes](mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md),
  [KAG export](mechanics/consumer-handoff/docs/KAG_SOURCE_EXPORT.md), and
  [eval guardrails](mechanics/consumer-handoff/docs/MEMORY_EVAL_GUARDRAILS.md).
- Writeback, chronicle, runtime, and continuity:
  [growth-refinery writeback](mechanics/writeback/docs/GROWTH_REFINERY_WRITEBACK.md),
  [quest chronicle](mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md),
  [self-agency continuity](mechanics/writeback/docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md),
  [runtime seam](mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md),
  [runtime targets](mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json),
  [runtime intake](mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json),
  [runtime governance](mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json),
  [receipt publication](mechanics/writeback/parts/receipt-publication-regression/scripts/publish_live_receipts.py),
  [continuity example](mechanics/writeback/parts/growth-and-continuity/examples/provenance_thread.self-agency-continuity.example.json), and
  [Phase Alpha map](mechanics/writeback/parts/growth-and-continuity/generated/phase_alpha_writeback_map.min.json).
- Antifragility and lineage:
  [antifragility mechanic](mechanics/antifragility/README.md),
  [rollback follow-through](mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.rollback_followthrough.example.json),
  [component refresh](mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.component_refresh.example.json),
  [pattern-lineage memory](mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md),
  [pattern-lineage schema](mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/schemas/pattern_lineage_memory_entry_v1.json), and
  [pattern-lineage example](mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/examples/pattern_lineage_memory_entry.example.json).
- Readiness and Questbook:
  [memory readiness boundary](mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md),
  [Questbook projections](mechanics/questbook/parts/quest-read-model-projections/README.md),
  [quest catalog](generated/quests/quest_catalog.min.json), and
  [quest dispatch](generated/quests/quest_dispatch.min.json).

Detailed mechanic futures live in `mechanics/<slug>/ROADMAP.md`. Detailed
release history lives in [CHANGELOG](CHANGELOG.md). Durable obligations live in
[QUESTBOOK](QUESTBOOK.md) and [quests](quests/README.md).

## Memo Mechanics

[mechanics](mechanics/README.md) is the atlas for repeatable memo-side
movement around memory canon, source families, technical artifacts, owner
handoffs, legacy bridges, and validation.

Current mechanic entries: [adoption](mechanics/adoption/README.md),
[agon](mechanics/agon/README.md),
[antifragility](mechanics/antifragility/README.md),
[checkpoint](mechanics/checkpoint/README.md),
[consumer-handoff](mechanics/consumer-handoff/README.md),
[governance](mechanics/governance/README.md),
[lineage-harvest](mechanics/lineage-harvest/README.md),
[operational-gate](mechanics/operational-gate/README.md),
[questbook](mechanics/questbook/README.md),
[readiness-boundary](mechanics/readiness-boundary/README.md),
[recurrence-support](mechanics/recurrence-support/README.md),
[retention](mechanics/retention/README.md),
[shape-guard](mechanics/shape-guard/README.md),
[titan](mechanics/titan/README.md), and
[writeback](mechanics/writeback/README.md).

Use root [AGENTS](AGENTS.md) for mechanic-change routing, then follow
`mechanics/AGENTS.md` and the target `mechanics/<slug>/AGENTS.md` before
editing. The root README only points to the mechanics atlas; it should not
duplicate the agent route matrix.

## Technical Districts

For machine-readable orientation, use
[root_technical_districts.min.json](generated/root-topology/root_technical_districts.min.json).
The exact allowlist and family contracts live in
[config/root-topology/root_technical_districts.json](config/root-topology/root_technical_districts.json).

| District | Use for |
|---|---|
| [docs](docs/README.md) | memory doctrine, route maps, boundary docs, release route, and [docs/decisions](docs/decisions/README.md) |
| [memo](memo/README.md) | reviewed memory object corpus, support lanes, and reviewed intake receipts |
| [mechanics](mechanics/README.md) | repeatable memo operations and package-local artifacts |
| [schemas](schemas/AGENTS.md) | memory and support-object contracts |
| [examples](examples/AGENTS.md) | public-safe memory examples and recall contracts |
| [generated](generated/AGENTS.md) | compact generated companions |
| [scripts](scripts/AGENTS.md) | validators, builders, and publication helpers |
| [tests](tests/AGENTS.md) | regression surfaces |
| [config](config/AGENTS.md) | source config for route cards, mechanics, and technical districts |
| [manifests](manifests/AGENTS.md) | reserved manifest posture and future recurrence surfaces |
| [quests](quests/AGENTS.md) | lane-first quest item store backing root Questbook |
| [.agents](.agents/AGENTS.md) | agent-facing companion lanes |

District gates narrow local handling. They do not replace source docs,
mechanic packages, validators, or sibling-owner repositories.

## Machine Companions

| Surface | Role |
|---|---|
| [memo_registry.min.json](generated/memory/memo_registry.min.json) | compact layer registry and validation command map |
| [memory_catalog.min.json](generated/memory/memory_catalog.min.json) | doctrine inspect surface |
| [memory_capsules.json](generated/memory/memory_capsules.json) | doctrine capsule hydration surface |
| [memory_sections.full.json](generated/memory/memory_sections.full.json) | expanded doctrine sections |
| [access_plane_currentness.min.json](generated/memory/access_plane_currentness.min.json) | MCP access-plane currentness readout |
| [source_intake_wave.min.json](generated/memory/source_intake_wave.min.json) | first source-lane intake wave readout |
| [workspace_memo_port_status.min.json](generated/memory/workspace_memo_port_status.min.json) | memo-side workspace port status readout from `8Dionysus` |
| [memory_object_catalog.min.json](generated/memory-objects/memory_object_catalog.min.json) | object-facing inspect surface over reviewed corpus objects and teaching fixtures |
| [memory_object_capsules.json](generated/memory-objects/memory_object_capsules.json) | object-facing capsule hydration surface with `source_kind` |
| [memory_object_sections.full.json](generated/memory-objects/memory_object_sections.full.json) | expanded object-facing sections with source paths back to corpus or fixtures |
| [agents_mesh.min.json](generated/agents/agents_mesh.min.json) | AGENTS mesh coverage companion |
| [root_technical_districts.min.json](generated/root-topology/root_technical_districts.min.json) | compact root technical district atlas |
| [memo_mechanics.min.json](generated/mechanics/memo_mechanics.min.json) | compact mechanic package index |
| [memo_mechanic_readiness.min.json](generated/mechanics/memo_mechanic_readiness.min.json) | OS Abyss readiness matrix for memo mechanics |
| [mechanic_artifacts.min.json](generated/mechanics/mechanic_artifacts.min.json) | mechanic-local artifact inventory |

Generated files are companions, not authority. Source docs, schemas, examples,
mechanic packages, config, builders, validators, and owner repositories keep
meaning.

## Validate

Executable validation routes live in [AGENTS](AGENTS.md#verify) and the
nearest `AGENTS.md`. Generated families should be rebuilt from their
owning source surfaces before broad validation.

## Working Rule

Grow the memory layer by making the next recall route clearer.

Add docs, schemas, examples, mechanics, generated companions, quests, tests, and
agent cards only where they make memory more explicit, provenance-aware,
temporally honest, and bounded. When detail belongs to proof, routing, runtime,
roles, playbooks, KAG, ToS, a mechanic roadmap, a changelog, a quest, a
decision record, or a generated companion, route it there.

## License

Apache-2.0
