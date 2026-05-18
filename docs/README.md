# Documentation Map

This is the map for the `docs/` district of `aoa-memo`.

Use the root [README](../README.md) as the public front door and this file when
you are already inside `docs/` and need the right memory-layer surface.

Editing under `docs/` starts with [AGENTS](AGENTS.md), then the placement rules
in [ROOT_SURFACE_LAW](ROOT_SURFACE_LAW.md). For agent-facing topology, add
[DESIGN.AGENTS](../DESIGN.AGENTS.md).

## Start Here

For the shortest repo overview, read:

1. [README](../README.md)
2. [CHARTER](../CHARTER.md)
3. [DESIGN](../DESIGN.md)
4. [BOUNDARIES](BOUNDARIES.md)
5. [MEMORY_MODEL](MEMORY_MODEL.md)

For current direction, add [ROADMAP](../ROADMAP.md). For agent-surface shape,
add [DESIGN.AGENTS](../DESIGN.AGENTS.md).

## Root Docs

| Surface | Owns |
|---|---|
| [AGENTS](AGENTS.md) | docs-local route card |
| [README](README.md) | this district map |
| [ROOT_SURFACE_LAW](ROOT_SURFACE_LAW.md) | root and docs-root placement law |
| [BOUNDARIES](BOUNDARIES.md) | repository owner split and route-away rules |
| [MEMORY_MODEL](MEMORY_MODEL.md) | conceptual model for memory functions, temperature, scope, trust, and object canon |
| [MEMORY_OBJECT_PROFILES](MEMORY_OBJECT_PROFILES.md) | per-kind memory object posture |
| [MEMORY_TRUST_POSTURE](MEMORY_TRUST_POSTURE.md) | confidence, authority, freshness, salience, freeze, and current recall posture |
| [MEMORY_TEMPERATURES](MEMORY_TEMPERATURES.md) | hot, warm, cool, cold, frozen, and core-band guidance |
| [LIFECYCLE](LIFECYCLE.md) | confirmation, freeze, supersession, retraction, archive, and current recall |
| [NARRATIVE_CORE_CONTRACT](NARRATIVE_CORE_CONTRACT.md) | authored/core memory versus derived memory split |
| [PROVENANCE_THREADS](PROVENANCE_THREADS.md) | provenance thread shape and walk-back posture |
| [OPERATIONAL_BOUNDARY](OPERATIONAL_BOUNDARY.md) | v1-facing boundary as doctrine plus compact public surfaces |
| [MEMORY_READINESS_BOUNDARY](MEMORY_READINESS_BOUNDARY.md) | high-pressure memory readiness stop-lines |
| [RELEASING](RELEASING.md) | release route |

## Current Surface Families

`docs/` is still partly flat. Treat this map as the topology spine for
remaining flat doctrine, while validated districts and mechanics move one owner
family at a time.

Antifragility, Agon, Titan, adoption, governance, shape-guard, checkpoint,
consumer-handoff, operational-gate, recurrence-support, lineage-harvest,
writeback, and retention are now memo mechanics under
[`mechanics/`](../mechanics/README.md), not docs subdirectories.
In path terms, `mechanics/agon/docs/` owns the former flat and transitional
`AGON_*` docs and `mechanics/titan/docs/` owns the former flat and
transitional `TITAN_*` docs.

| Family | Current flat surfaces |
|---|---|
| Core doctrine | `BOUNDARIES`, `MEMORY_MODEL`, `MEMORY_OBJECT_PROFILES`, `MEMORY_TRUST_POSTURE`, `MEMORY_TEMPERATURES`, `LIFECYCLE`, `NARRATIVE_CORE_CONTRACT`, `PROVENANCE_THREADS`, `OPERATIONAL_BOUNDARY` |
| Recall and writeback | [recurrence-support mechanic](../mechanics/recurrence-support/README.md), [writeback mechanic](../mechanics/writeback/README.md) |
| Neighbor handoffs | [consumer-handoff mechanic](../mechanics/consumer-handoff/README.md), [adoption mechanic](../mechanics/adoption/README.md) |
| Checkpoint carry | [checkpoint mechanic](../mechanics/checkpoint/README.md) plus inquiry checkpoint, approval, health, improvement thread, checkpoint-to-memory schema, examples, generated refs, and tests |
| Operational gates | [operational-gate mechanic](../mechanics/operational-gate/README.md) plus deployment incident, office incident, service revision, and post-release boundary schemas, examples, and tests |
| Recurrence support | [recurrence-support mechanic](../mechanics/recurrence-support/README.md) plus witness trace, checkpoint consumer refs, return recall, reviewed closeout quest, schemas, examples, generated refs, and tests |
| Lineage harvest | [lineage-harvest mechanic](../mechanics/lineage-harvest/README.md) plus pattern-lineage schema, example, generated recall surfaces, and tests |
| Antifragility | [antifragility mechanic](../mechanics/antifragility/README.md) plus matching schemas, examples, generated object surfaces, and tests |
| Adoption, authority, and shape guard | [adoption mechanic](../mechanics/adoption/README.md), [governance mechanic](../mechanics/governance/README.md), [shape-guard mechanic](../mechanics/shape-guard/README.md), [retention mechanic](../mechanics/retention/README.md) |
| Agon memo seams | [agon mechanic](../mechanics/agon/README.md) plus matching config, schemas, generated registries, examples, tests, quests, and manifests |
| Titan memory seams | [titan mechanic](../mechanics/titan/README.md) plus matching schemas, examples, and tests |
| Decision rationale | [decisions](decisions/README.md) |

## Claim Routes

| Question | Route |
|---|---|
| Does this belong in memory at all? | [CHARTER](../CHARTER.md), then [BOUNDARIES](BOUNDARIES.md) |
| What kind of memory object is it? | [MEMORY_MODEL](MEMORY_MODEL.md), then [MEMORY_OBJECT_PROFILES](MEMORY_OBJECT_PROFILES.md) |
| Is this proof or verdict logic? | [BOUNDARIES](BOUNDARIES.md), then route to `aoa-evals` |
| Is this routing behavior? | [ROUTING_MEMORY_ADOPTION](../mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md), then route to `aoa-routing` |
| Is this a role right or actor policy? | [consumer-handoff/AGENT_MEMORY_POSTURE_SEAM](../mechanics/consumer-handoff/docs/AGENT_MEMORY_POSTURE_SEAM.md), then route to `aoa-agents` |
| Is this a graph lift or retrieval substrate? | [consumer-handoff/KAG_SOURCE_EXPORT](../mechanics/consumer-handoff/docs/KAG_SOURCE_EXPORT.md), then route to `aoa-kag` |
| Is this a recurring cross-repo pattern or federation harvest candidate? | [lineage-harvest/PATTERN_LINEAGE_MEMORY](../mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md), then route stronger claims to `Agents-of-Abyss`, source owners, `aoa-evals`, `aoa-stats`, `aoa-kag`, or `Tree-of-Sophia` |
| Is this live runtime storage or retention? | [RUNTIME_WRITEBACK_SEAM](../mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md), then route to `abyss-stack` |
| Where should a new root or docs-root file live? | [ROOT_SURFACE_LAW](ROOT_SURFACE_LAW.md) |
| Why was a structural route chosen? | [decisions](decisions/README.md) |

## Change Routes

| Change | First route |
|---|---|
| Memory doctrine | [BOUNDARIES](BOUNDARIES.md), [MEMORY_MODEL](MEMORY_MODEL.md), and the target doc |
| Object canon or lifecycle | [MEMORY_OBJECT_PROFILES](MEMORY_OBJECT_PROFILES.md), [MEMORY_TRUST_POSTURE](MEMORY_TRUST_POSTURE.md), [LIFECYCLE](LIFECYCLE.md) |
| Generated parity | source doc or manifest, builder, generated output, validator, and test together |
| Docs placement | [ROOT_SURFACE_LAW](ROOT_SURFACE_LAW.md) |
| Antifragility mechanic | [mechanics/antifragility/AGENTS](../mechanics/antifragility/AGENTS.md), then [mechanics/antifragility/README](../mechanics/antifragility/README.md) |
| Agon memo mechanic | [mechanics/agon/AGENTS](../mechanics/agon/AGENTS.md), then [mechanics/agon/README](../mechanics/agon/README.md) |
| Titan memo mechanic | [mechanics/titan/AGENTS](../mechanics/titan/AGENTS.md), then [mechanics/titan/README](../mechanics/titan/README.md) |
| Adoption mechanic | [mechanics/adoption/AGENTS](../mechanics/adoption/AGENTS.md), then [mechanics/adoption/README](../mechanics/adoption/README.md) |
| Governance mechanic | [mechanics/governance/AGENTS](../mechanics/governance/AGENTS.md), then [mechanics/governance/README](../mechanics/governance/README.md) |
| Shape-guard mechanic | [mechanics/shape-guard/AGENTS](../mechanics/shape-guard/AGENTS.md), then [mechanics/shape-guard/README](../mechanics/shape-guard/README.md) |
| Checkpoint mechanic | [mechanics/checkpoint/AGENTS](../mechanics/checkpoint/AGENTS.md), then [mechanics/checkpoint/README](../mechanics/checkpoint/README.md) |
| Consumer-handoff mechanic | [mechanics/consumer-handoff/AGENTS](../mechanics/consumer-handoff/AGENTS.md), then [mechanics/consumer-handoff/README](../mechanics/consumer-handoff/README.md) |
| Operational-gate mechanic | [mechanics/operational-gate/AGENTS](../mechanics/operational-gate/AGENTS.md), then [mechanics/operational-gate/README](../mechanics/operational-gate/README.md) |
| Recurrence-support mechanic | [mechanics/recurrence-support/AGENTS](../mechanics/recurrence-support/AGENTS.md), then [mechanics/recurrence-support/README](../mechanics/recurrence-support/README.md) |
| Lineage-harvest mechanic | [mechanics/lineage-harvest/AGENTS](../mechanics/lineage-harvest/AGENTS.md), then [mechanics/lineage-harvest/README](../mechanics/lineage-harvest/README.md) |
| Writeback mechanic | [mechanics/writeback/AGENTS](../mechanics/writeback/AGENTS.md), then [mechanics/writeback/README](../mechanics/writeback/README.md) |
| Retention mechanic | [mechanics/retention/AGENTS](../mechanics/retention/AGENTS.md), then [mechanics/retention/README](../mechanics/retention/README.md) |
| Mechanic artifact placement | [mechanics/ARTIFACT_TOPOLOGY](../mechanics/ARTIFACT_TOPOLOGY.md) |
| Agent-facing shape | [DESIGN.AGENTS](../DESIGN.AGENTS.md), root [AGENTS](../AGENTS.md), and nearest local `AGENTS.md` |
| Decision rationale | [decisions/AGENTS](decisions/AGENTS.md), then [decisions/README](decisions/README.md) |
| Public release path | [RELEASING](RELEASING.md), then [CHANGELOG](../CHANGELOG.md) |

## Thematic Migration Rule

Do not move flat docs into thematic subdirectories just because they look
crowded.

A migration should happen only when it has:

- an owner family
- a source map
- updated links
- validator or test coverage
- a decision record when the route will matter later

Until then, this README is the map and the flat files remain active surfaces.

## Adjacent Routes

| Route | Use |
|---|---|
| [schemas](../schemas/AGENTS.md) | memory and support-object contracts |
| [examples](../examples/AGENTS.md) | public-safe examples and manifests |
| [generated](../generated/AGENTS.md) | compact generated companions |
| [scripts](../scripts/AGENTS.md) | builders, validators, and publication helpers |
| [tests](../tests/AGENTS.md) | regression surfaces |
| [config](../config/AGENTS.md) | seed and build inputs |
| [mechanics/antifragility](../mechanics/antifragility/README.md) | Antifragility memo mechanic |
| [mechanics/agon](../mechanics/agon/README.md) | Agon memo mechanic |
| [mechanics/titan](../mechanics/titan/README.md) | Titan memo mechanic |
| [mechanics/governance](../mechanics/governance/README.md) | Governance memo mechanic |
| [mechanics/shape-guard](../mechanics/shape-guard/README.md) | Shape guard memo mechanic |
| [mechanics/checkpoint](../mechanics/checkpoint/README.md) | Checkpoint memo mechanic |
| [mechanics/consumer-handoff](../mechanics/consumer-handoff/README.md) | Consumer handoff memo mechanic |
| [mechanics/operational-gate](../mechanics/operational-gate/README.md) | Operational gate memo mechanic |
| [mechanics/recurrence-support](../mechanics/recurrence-support/README.md) | Recurrence support memo mechanic |
| [mechanics/lineage-harvest](../mechanics/lineage-harvest/README.md) | Lineage harvest memo mechanic |
| [mechanics](../mechanics/README.md) | Antifragility, Agon, Titan, adoption, governance, shape-guard, checkpoint, consumer-handoff, operational-gate, recurrence-support, lineage-harvest, writeback, and retention memo mechanics |
| [manifests](../manifests/AGENTS.md) | recurrence manifests and hook bindings |
| [quests](../quests/AGENTS.md) | quest files backing `QUESTBOOK.md` |
| [.agents](../.agents/AGENTS.md) | agent-facing companion lanes |
| [QUESTBOOK](../QUESTBOOK.md) | active memory-layer obligation index |

## Notes

- Prefer this map when a flat `docs/*.md` surface is hard to classify.
- Prefer [ROOT_SURFACE_LAW](ROOT_SURFACE_LAW.md) before adding, moving, or
  deleting root or docs-root surfaces.
- Prefer [decisions](decisions/README.md) when future contributors will need to
  know why a topology route exists.
- Prefer `config/agents_mesh.json` and `generated/agents_mesh.min.json` when a
  docs migration adds or changes local route cards.
- Prefer `scripts/validate_docs_districts.py` when checking that retired docs
  districts and flat moved docs have not reappeared.
- Prefer `scripts/validate_memo_mechanics.py` when antifragility, Agon, Titan,
  adoption, governance, shape-guard, checkpoint, consumer-handoff,
  operational-gate, recurrence-support, lineage-harvest, writeback, or
  retention mechanics move.
- Generated surfaces summarize memory doctrine and object examples. They do not
  replace authored docs, schemas, examples, or validators.
