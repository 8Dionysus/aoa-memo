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

`docs/` is still mostly flat. Treat this map as the topology spine for the
remaining flat docs while validated districts move out one owner family at a
time.

The first moved districts are the [Agon Memo District](agon/README.md) and the
[Titan Memo District](titan/README.md): `docs/agon/` owns the former flat
`AGON_*` memo docs, and `docs/titan/` owns the former flat `TITAN_*` memo docs.

| Family | Current flat surfaces |
|---|---|
| Core doctrine | `BOUNDARIES`, `MEMORY_MODEL`, `MEMORY_OBJECT_PROFILES`, `MEMORY_TRUST_POSTURE`, `MEMORY_TEMPERATURES`, `LIFECYCLE`, `NARRATIVE_CORE_CONTRACT`, `PROVENANCE_THREADS`, `OPERATIONAL_BOUNDARY` |
| Recall and writeback | `WITNESS_TRACE_CONTRACT`, `WRITEBACK_TEMPERATURE_POLICY`, `QUEST_CHRONICLE_WRITEBACK`, `RUNTIME_WRITEBACK_SEAM`, `GROWTH_REFINERY_WRITEBACK`, `RECURRENCE_MEMORY_SUPPORT_SURFACES`, `REVIEWED_CLOSEOUT_RECALL_LANDING` |
| Neighbor seams | `AGENT_MEMORY_POSTURE_SEAM`, `PLAYBOOK_MEMORY_SCOPES`, `ROUTING_MEMORY_ADOPTION`, `KAG_TOS_BRIDGE_CONTRACT`, `KAG_SOURCE_EXPORT`, `MEMORY_EVAL_GUARDRAILS` |
| Antifragility | `FAILURE_LESSON_MEMORY`, `FAILURE_LESSON_RECALL`, `DRIFT_REVIEW_LESSON_MEMORY`, `RECOVERY_PATTERN_MEMORY`, `RECOVERY_PATTERN_RECALL`, `ROLLBACK_FOLLOWTHROUGH_PATTERN` |
| Adoption and governance | `ADOPTION_*`, `GOVERNANCE_*`, `FEDERATION_*`, `INSTALLATION_MEMORY_BOUNDARIES`, `CERTIFICATION_MEMORY_BOUNDARIES`, `CROSS_REPO_RETENTION_MEMORY` |
| Agon memo seams | [agon](agon/README.md) district plus matching config, schemas, generated registries, examples, tests, quests, and manifests |
| Titan memory seams | [titan](titan/README.md) district plus matching schemas, examples, and tests |
| Decision rationale | [decisions](decisions/README.md) |

## Claim Routes

| Question | Route |
|---|---|
| Does this belong in memory at all? | [CHARTER](../CHARTER.md), then [BOUNDARIES](BOUNDARIES.md) |
| What kind of memory object is it? | [MEMORY_MODEL](MEMORY_MODEL.md), then [MEMORY_OBJECT_PROFILES](MEMORY_OBJECT_PROFILES.md) |
| Is this proof or verdict logic? | [BOUNDARIES](BOUNDARIES.md), then route to `aoa-evals` |
| Is this routing behavior? | [ROUTING_MEMORY_ADOPTION](ROUTING_MEMORY_ADOPTION.md), then route to `aoa-routing` |
| Is this a role right or actor policy? | [AGENT_MEMORY_POSTURE_SEAM](AGENT_MEMORY_POSTURE_SEAM.md), then route to `aoa-agents` |
| Is this a graph lift or retrieval substrate? | [KAG_SOURCE_EXPORT](KAG_SOURCE_EXPORT.md), then route to `aoa-kag` |
| Is this live runtime storage or retention? | [RUNTIME_WRITEBACK_SEAM](RUNTIME_WRITEBACK_SEAM.md), then route to `abyss-stack` |
| Where should a new root or docs-root file live? | [ROOT_SURFACE_LAW](ROOT_SURFACE_LAW.md) |
| Why was a structural route chosen? | [decisions](decisions/README.md) |

## Change Routes

| Change | First route |
|---|---|
| Memory doctrine | [BOUNDARIES](BOUNDARIES.md), [MEMORY_MODEL](MEMORY_MODEL.md), and the target doc |
| Object canon or lifecycle | [MEMORY_OBJECT_PROFILES](MEMORY_OBJECT_PROFILES.md), [MEMORY_TRUST_POSTURE](MEMORY_TRUST_POSTURE.md), [LIFECYCLE](LIFECYCLE.md) |
| Generated parity | source doc or manifest, builder, generated output, validator, and test together |
| Docs placement | [ROOT_SURFACE_LAW](ROOT_SURFACE_LAW.md) |
| Agon memo docs | [agon/AGENTS](agon/AGENTS.md), then [agon/README](agon/README.md) |
| Titan memo docs | [titan/AGENTS](titan/AGENTS.md), then [titan/README](titan/README.md) |
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
| [agon](agon/README.md) | Agon memo docs district |
| [titan](titan/README.md) | Titan memo docs district |
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
- Prefer `scripts/validate_docs_districts.py` when a thematic docs family moves
  out of the flat docs root.
- Generated surfaces summarize memory doctrine and object examples. They do not
  replace authored docs, schemas, examples, or validators.
