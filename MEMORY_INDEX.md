# MEMORY_INDEX

This file is the repository-wide map of public memory surfaces.

Use it when the question is "what memory objects, recall modes, source docs,
or generated companions exist here?" It is an index, not the full memory model.

## Authority

`MEMORY_INDEX.md` owns the compact public map of:

- memory object kinds
- support objects
- recall modes
- memory operation modes
- memory temperature vocabulary
- source doctrine families
- reviewed memory corpus route
- generated memory companions

It does not own object semantics, schema fields, lifecycle policy, generated
truth, proof verdicts, runtime retention, route dispatch, role rights, or KAG
substrate meaning.

Use the stronger surface when the question is narrower:

- repository boundary: [CHARTER](CHARTER.md)
- system form: [DESIGN](DESIGN.md)
- memory model: [MEMORY_MODEL](docs/memory/MEMORY_MODEL.md)
- operation cycle: [MEMORY_OPERATION_CYCLE](docs/memory/MEMORY_OPERATION_CYCLE.md)
- per-kind posture: [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md)
- living topology: [LIVING_MEMORY_TOPOLOGY](docs/memory/LIVING_MEMORY_TOPOLOGY.md)
- local memo ports: [LOCAL_MEMO_PORT_STANDARD](docs/memory/LOCAL_MEMO_PORT_STANDARD.md)
- memo port indexing vocabulary: [MEMO_PORT_INDEXING_VOCABULARY](docs/memory/MEMO_PORT_INDEXING_VOCABULARY.md)
- reviewed corpus: [memo](memo/README.md), [OBJECT_SHAPE](memo/OBJECT_SHAPE.md)
- trust posture: [MEMORY_TRUST_POSTURE](docs/posture/MEMORY_TRUST_POSTURE.md)
- operation modes: [MEMORY_OPERATION_MODES](docs/posture/MEMORY_OPERATION_MODES.md)
- temperature and freshness: [MEMORY_TEMPERATURES](docs/posture/MEMORY_TEMPERATURES.md)
- lifecycle: [LIFECYCLE](docs/posture/LIFECYCLE.md)
- provenance thread shape: [PROVENANCE_THREADS](docs/posture/PROVENANCE_THREADS.md)
- mechanics atlas: [mechanics](mechanics/README.md)
- generated registry: [memo_registry.min.json](generated/memory/memo_registry.min.json)

Generated companions route and compress. Authored docs, schemas, examples,
mechanic packages, validators, and owner repositories keep authority.

## Memory Object Kinds

| Kind | Use for | First source |
|---|---|---|
| `anchor` | stable reference points that other memory can attach to | [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| `state_capsule` | bounded state snapshots with explicit scope and time | [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| `episode` | what happened, when, and under what source refs | [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| `claim` | consolidated statement with provenance and lifecycle posture | [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| `decision` | bounded choice, rationale, and consequence memory | [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| `pattern` | recurring signal or reusable memory candidate | [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| `bridge` | source-linked handoff toward another owner layer | [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| `audit_event` | review, validation, correction, retention, or supersession trace | [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |

Memory objects are explicit recall material. They are not proof, route
authority, runtime state, role rights, or source-authored knowledge.

## Support Objects

| Object | Use for | First source |
|---|---|---|
| `provenance_thread` | walk-back paths, source refs, and lineage support | [PROVENANCE_THREADS](docs/posture/PROVENANCE_THREADS.md) |
| `recall_contract` | inspect, capsule, expand, and mode/scoping expectations | [MEMORY_MODEL](docs/memory/MEMORY_MODEL.md) and [examples](examples/AGENTS.md) |
| `reviewed_intake_landing_receipt` | receipt that links accepted local-port export to copied intake packet and landed object bundle | [OBJECT_SHAPE](memo/OBJECT_SHAPE.md) |
| `inquiry_checkpoint` | checkpoint carry memory at the memo boundary | [checkpoint mechanic](mechanics/checkpoint/README.md) |
| `witness_trace` | reviewed route-return and closeout recall support | [recurrence-support mechanic](mechanics/recurrence-support/README.md) |
| `quest_chronicle` | quest witness and writeback support | [writeback mechanic](mechanics/writeback/README.md) |

Support objects help memory stay reviewable. They do not create a new object
family unless the memory model, schema, examples, and validators say so.

## Recall Modes

| Mode | Use for | First source |
|---|---|---|
| `working` | immediate bounded continuation and checkpoint-aware return | [PLAYBOOK_MEMORY_SCOPES](mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md) |
| `episodic` | event-like recall with time and source context | [MEMORY_MODEL](docs/memory/MEMORY_MODEL.md) |
| `semantic` | concept-like recall through compact surfaces | [ROUTING_MEMORY_ADOPTION](mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md) |
| `procedural` | process-shaped recall without becoming execution authority | [MEMORY_MODEL](docs/memory/MEMORY_MODEL.md) |
| `lineage` | provenance, recurrence, and pattern-lineage recall | [PATTERN_LINEAGE_MEMORY](mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md) |
| `source_route` | route to stronger owner surfaces rather than local overclaim | [BOUNDARIES](docs/boundaries/BOUNDARIES.md) |

Recall defaults to inspect first, capsule second, expand only when needed.

## Operation Modes

| Mode | Use for | First source |
|---|---|---|
| `read_only` | inspect source docs and generated read models | [MEMORY_OPERATION_MODES](docs/posture/MEMORY_OPERATION_MODES.md) |
| `write_candidate_only` | capture source-linked candidates for review | [MEMORY_WRITE_PATH_GUARDRAILS](docs/boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md) |
| `generate_without_read` | produce output without reading or mutating memory | [MEMORY_OPERATION_MODES](docs/posture/MEMORY_OPERATION_MODES.md) |
| `read_write_under_review` | read memo and emit reviewed writeback candidates | [MEMORY_OPERATION_CYCLE](docs/memory/MEMORY_OPERATION_CYCLE.md) |
| `frozen_read_mostly` | inspect stable surfaces and change only through owner approval | [MEMORY_OPERATION_MODES](docs/posture/MEMORY_OPERATION_MODES.md) |

Operation modes describe task posture. They are not role rights.

## Temperature Scale

| Temperature | Meaning | First source |
|---|---|---|
| `hot` | current and actively useful, not necessarily proven | [MEMORY_TEMPERATURES](docs/posture/MEMORY_TEMPERATURES.md) |
| `warm` | still useful, but less immediate | [MEMORY_TEMPERATURES](docs/posture/MEMORY_TEMPERATURES.md) |
| `cool` | available background memory | [MEMORY_TEMPERATURES](docs/posture/MEMORY_TEMPERATURES.md) |
| `cold` | low-current-use retained memory | [MEMORY_TEMPERATURES](docs/posture/MEMORY_TEMPERATURES.md) |
| `frozen` | stable historical memory with explicit lifecycle posture | [MEMORY_TEMPERATURES](docs/posture/MEMORY_TEMPERATURES.md) |

Temperature is current-use posture. It is not truth, proof, authority, or
freshness by itself.

## Source Families

| Family | First route |
|---|---|
| Repository authority and boundaries | [CHARTER](CHARTER.md), [BOUNDARIES](docs/boundaries/BOUNDARIES.md) |
| Reviewed memory corpus | [memo](memo/README.md), [OBJECT_SHAPE](memo/OBJECT_SHAPE.md) |
| Memory model, object canon, and operation cycle | [MEMORY_MODEL](docs/memory/MEMORY_MODEL.md), [MEMORY_OPERATION_CYCLE](docs/memory/MEMORY_OPERATION_CYCLE.md), [MEMORY_OBJECT_PROFILES](docs/memory/MEMORY_OBJECT_PROFILES.md) |
| Living topology and local memo ports | [LIVING_MEMORY_TOPOLOGY](docs/memory/LIVING_MEMORY_TOPOLOGY.md), [LOCAL_MEMO_PORT_STANDARD](docs/memory/LOCAL_MEMO_PORT_STANDARD.md), [MEMO_PORT_INDEXING_VOCABULARY](docs/memory/MEMO_PORT_INDEXING_VOCABULARY.md) |
| Trust, lifecycle, temperature, operation modes, and provenance | [MEMORY_TRUST_POSTURE](docs/posture/MEMORY_TRUST_POSTURE.md), [LIFECYCLE](docs/posture/LIFECYCLE.md), [MEMORY_TEMPERATURES](docs/posture/MEMORY_TEMPERATURES.md), [MEMORY_OPERATION_MODES](docs/posture/MEMORY_OPERATION_MODES.md), [PROVENANCE_THREADS](docs/posture/PROVENANCE_THREADS.md) |
| Operational boundary and write-path guardrails | [OPERATIONAL_BOUNDARY](docs/boundaries/OPERATIONAL_BOUNDARY.md), [MEMORY_WRITE_PATH_GUARDRAILS](docs/boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md), [operational gate write path](mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md) |
| Memo mechanics | [mechanics](mechanics/README.md) |
| Root and docs placement | [ROOT_SURFACE_LAW](docs/root/ROOT_SURFACE_LAW.md) |
| Public obligations | [QUESTBOOK](QUESTBOOK.md), [quests](quests/README.md), [questbook mechanic](mechanics/questbook/README.md) |

## Generated Companions

| Surface | Role |
|---|---|
| [memo_registry.min.json](generated/memory/memo_registry.min.json) | compact layer registry and validation command map |
| [memory_catalog.min.json](generated/memory/memory_catalog.min.json) | compact doctrine inspect surface |
| [memory_capsules.json](generated/memory/memory_capsules.json) | capsule hydration surface for doctrine recall |
| [memory_sections.full.json](generated/memory/memory_sections.full.json) | expanded doctrine sections |
| [access_plane_currentness.min.json](generated/memory/access_plane_currentness.min.json) | operational currentness readout for the `aoa_memo` access plane |
| [source_intake_wave.min.json](generated/memory/source_intake_wave.min.json) | first source-lane intake wave readout across real reviewed/export pressure |
| [workspace_memo_port_status.min.json](generated/memory/workspace_memo_port_status.min.json) | memo-side projection of workspace memo-port status from the `8Dionysus` map |
| [memory_object_catalog.min.json](generated/memory-objects/memory_object_catalog.min.json) | compact object-facing inspect surface over reviewed corpus objects and teaching fixtures |
| [memory_object_capsules.json](generated/memory-objects/memory_object_capsules.json) | capsule hydration surface for object recall, with `source_kind` |
| [memory_object_sections.full.json](generated/memory-objects/memory_object_sections.full.json) | expanded object-facing sections with source paths back to corpus or fixtures |
| [memo_port_vocabulary.min.json](generated/memory/memo_port_vocabulary.min.json) | compact vocabulary for local memo port packet indexing |
| [memo_mechanics.min.json](generated/mechanics/memo_mechanics.min.json) | compact mechanic package index |
| [memo_mechanic_readiness.min.json](generated/mechanics/memo_mechanic_readiness.min.json) | OS Abyss readiness matrix for memo mechanics |
| [quest_catalog.min.json](generated/quests/quest_catalog.min.json) | generated quest catalog projection |
| [quest_dispatch.min.json](generated/quests/quest_dispatch.min.json) | generated quest dispatch projection |
| [kag_export.min.json](mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json) | source-owned memo donor export for `aoa-kag` readiness |

## Notes

- `MEMORY_INDEX.md` is the map; [MEMORY_MODEL](docs/memory/MEMORY_MODEL.md) is the
  conceptual contract.
- [schemas](schemas/AGENTS.md) and [examples](examples/AGENTS.md) make the
  object shape concrete.
- [scripts](scripts/AGENTS.md) and [tests](tests/AGENTS.md) keep generated
  companions and examples honest.
- When memory needs proof, route to `aoa-evals`.
- When memory needs runtime retention, route to `abyss-stack`.
- When memory needs role rights, route to `aoa-agents`.
- When memory needs dispatch, route to `aoa-routing`.
- When memory needs graph substrate meaning, route to `aoa-kag` and stronger
  source owners.
