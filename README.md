# aoa-memo

`aoa-memo` is the memory and recall layer of the AoA ecosystem. It makes memory
explicit, temporal, source-aware, reviewable, and safe to route through without
turning memory into proof, runtime state, role authority, dispatch logic, or
source-authored knowledge.

Use this README as the public front door. When work becomes doctrinal,
mechanic-local, corpus-backed, generated, schema-backed, quest-bound, or
agent-facing, follow the linked owner surface instead of expanding this page.

> Current release: `v0.4.0`. See [CHANGELOG](CHANGELOG.md) for release notes.

## What This Repository Does

| Function | Surface |
|---|---|
| Repository authority boundary | [CHARTER](CHARTER.md) |
| Memory-layer system form | [DESIGN](DESIGN.md) |
| Agent-facing guidance form | [DESIGN.AGENTS](DESIGN.AGENTS.md) |
| Public memory canon map | [MEMORY_INDEX](MEMORY_INDEX.md) |
| Reviewed memory object corpus | [memo](memo/README.md) |
| Documentation and boundary map | [docs](docs/README.md), [BOUNDARIES](docs/boundaries/BOUNDARIES.md) |
| Memo-side mechanics | [mechanics](mechanics/README.md) |
| Direction and obligations | [ROADMAP](ROADMAP.md), [QUESTBOOK](QUESTBOOK.md), [quests](quests/README.md) |
| Agent route law and local checks | [AGENTS](AGENTS.md), then the nearest nested `AGENTS.md` |

This repository is strongest when it makes recall inspectable and bounded. It
is weakest when it tries to become proof, routing, runtime, role policy, graph
substrate, playbook choreography, or sibling source meaning.

## Start Here

Read only what matches the job.

| Need | Route |
|---|---|
| Shortest honest overview | this README -> [CHARTER](CHARTER.md) -> [DESIGN](DESIGN.md) -> [MEMORY_INDEX](MEMORY_INDEX.md) |
| Decide whether something belongs here | [CHARTER](CHARTER.md) -> [BOUNDARIES](docs/boundaries/BOUNDARIES.md) |
| Memory object canon | [MEMORY_INDEX](MEMORY_INDEX.md) -> [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| Reviewed durable memory | [memo](memo/README.md) -> [OBJECT_SHAPE](memo/OBJECT_SHAPE.md) |
| Memory doctrine or operation posture | [docs](docs/README.md), then the owning `docs/<district>/AGENTS.md` |
| Local memo ports and intake | [LIVING_MEMORY_TOPOLOGY](docs/memory/LIVING_MEMORY_TOPOLOGY.md) -> [LOCAL_MEMO_PORT_STANDARD](docs/memory/LOCAL_MEMO_PORT_STANDARD.md) |
| Root or docs-root placement | [ROOT_SURFACE_LAW](docs/root/ROOT_SURFACE_LAW.md) |
| Generated companions | [MEMORY_INDEX](MEMORY_INDEX.md#generated-companions), source surface, builder, generated output, validator |
| Memo mechanic work | [mechanics](mechanics/README.md), then the owning mechanic `AGENTS.md` and `PARTS.md` |
| Current direction | [ROADMAP](ROADMAP.md) |
| Decision rationale | [docs/decisions](docs/decisions/README.md) |
| Agent editing route | [AGENTS](AGENTS.md), then the nearest `AGENTS.md` route card |

## Memory Check

Before adding, trusting, or publishing a memo claim, open the smallest owner
that can answer it.

| Question | Owner route |
|---|---|
| May `aoa-memo` say this? | [CHARTER](CHARTER.md), then [BOUNDARIES](docs/boundaries/BOUNDARIES.md) |
| Is this write path allowed? | [MEMORY_WRITE_PATH_GUARDRAILS](docs/boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md) |
| What object kind or recall mode is this? | [MEMORY_INDEX](MEMORY_INDEX.md), then [MEMORY_MODEL](docs/memory/MEMORY_MODEL.md) |
| What read/write posture applies? | [MEMORY_OPERATION_MODES](docs/posture/MEMORY_OPERATION_MODES.md) |
| Is this current enough to recall? | [MEMORY_TRUST_POSTURE](docs/posture/MEMORY_TRUST_POSTURE.md), [MEMORY_TEMPERATURES](docs/posture/MEMORY_TEMPERATURES.md), and [LIFECYCLE](docs/posture/LIFECYCLE.md) |
| Is this proof, route, role, playbook, KAG, or runtime authority? | [BOUNDARIES](docs/boundaries/BOUNDARIES.md), then route to the stronger owner |

Required public handoff anchors:
[MEMORY_READINESS_BOUNDARY](mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md),
[ROUTING_MEMORY_ADOPTION](mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md),
[PLAYBOOK_MEMORY_SCOPES](mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md),
[SELF_AGENCY_CONTINUITY_WRITEBACK](mechanics/writeback/docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md), and
[QUEST_CHRONICLE_WRITEBACK](mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md).

## Current Contour

`aoa-memo` is in contract hardening.

`aoa-memo` currently carries reviewed memory-object bundles under `memo/`,
memory doctrine under `docs/`, repeatable memo operations under `mechanics/`,
schemas and examples for public memory contracts, generated read models, and
quest records for durable memory-layer obligations.

The detailed surface map lives in [MEMORY_INDEX](MEMORY_INDEX.md),
[docs](docs/README.md), [mechanics](mechanics/README.md), and generated indexes.
The root README should not become that inventory.

## Core Districts

| District | Use for |
|---|---|
| [docs](docs/README.md) | memory doctrine, boundaries, posture, validation topology, test topology, decisions, and root law |
| [memo](memo/README.md) | reviewed memory object corpus, support lanes, and intake receipts |
| [mechanics](mechanics/README.md) | repeatable memo operations and package-local artifacts |
| [schemas](schemas/AGENTS.md) | memory and support-object contracts |
| [examples](examples/AGENTS.md) | public-safe memory examples and recall contracts |
| [generated](generated/AGENTS.md) | compact derived companions tied back to source inputs |
| [scripts](scripts/AGENTS.md) and [tests](tests/AGENTS.md) | deterministic builders, validators, and regression surfaces |
| [config](config/AGENTS.md) | source config for route cards, validation lanes, mechanics, and root topology |
| [manifests](manifests/AGENTS.md), [quests](quests/AGENTS.md), [.agents](.agents/AGENTS.md) | recurrence posture, quest store, and agent-facing companion lanes |

Mechanic entrypoints: [adoption](mechanics/adoption/README.md),
[agon](mechanics/agon/README.md), [antifragility](mechanics/antifragility/README.md),
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
[titan](mechanics/titan/README.md), and [writeback](mechanics/writeback/README.md).

Generated files are companions, not authority. Source docs, schemas, examples,
mechanic packages, corpus bundles, config, builders, validators, tests, and
owner repositories keep meaning.

## Validate

Executable validation routes live in [AGENTS](AGENTS.md#verify) and the nearest
`AGENTS.md`. Use [docs/validation](docs/validation/VALIDATOR_TOPOLOGY.md)
for lane meaning and command authority.

For the frozen release gate, run:

```bash
python scripts/release/release_check.py
```

## Working Rule

Grow the memory layer by making the next recall route clearer.

Add docs, corpus objects, schemas, examples, mechanics, generated companions,
quests, tests, and agent cards only where they make memory more explicit,
provenance-aware, temporally honest, and bounded. Route detail to the owning
mechanic, memory index, docs map, decision record, quest, generated companion,
changelog, roadmap, route card, or sibling owner instead of making this README
carry it.

## License

Apache-2.0
