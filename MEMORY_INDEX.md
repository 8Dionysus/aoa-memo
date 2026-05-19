# MEMORY_INDEX

This file is the repository-wide map of public memory surfaces.

Use it when the question is "what memory objects, recall modes, source docs,
or generated companions exist here?" It is an index, not the full memory model.

## Authority

`MEMORY_INDEX.md` owns the compact public map of:

- memory object kinds
- support objects
- recall modes
- memory temperature vocabulary
- source doctrine families
- generated memory companions

It does not own object semantics, schema fields, lifecycle policy, generated
truth, proof verdicts, runtime retention, route dispatch, role rights, or KAG
substrate meaning.

Use the stronger surface when the question is narrower:

- repository boundary: [CHARTER](CHARTER.md)
- system form: [DESIGN](DESIGN.md)
- memory model: [MEMORY_MODEL](docs/MEMORY_MODEL.md)
- per-kind posture: [MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md)
- trust posture: [MEMORY_TRUST_POSTURE](docs/MEMORY_TRUST_POSTURE.md)
- temperature and freshness: [MEMORY_TEMPERATURES](docs/MEMORY_TEMPERATURES.md)
- lifecycle: [LIFECYCLE](docs/LIFECYCLE.md)
- provenance thread shape: [PROVENANCE_THREADS](docs/PROVENANCE_THREADS.md)
- mechanics atlas: [mechanics](mechanics/README.md)
- generated registry: [memo_registry.min.json](generated/memo_registry.min.json)

Generated companions route and compress. Authored docs, schemas, examples,
mechanic packages, validators, and owner repositories keep authority.

## Memory Object Kinds

| Kind | Use for | First source |
|---|---|---|
| `anchor` | stable reference points that other memory can attach to | [MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md) |
| `state_capsule` | bounded state snapshots with explicit scope and time | [MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md) |
| `episode` | what happened, when, and under what source refs | [MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md) |
| `claim` | consolidated statement with provenance and lifecycle posture | [MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md) |
| `decision` | bounded choice, rationale, and consequence memory | [MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md) |
| `pattern` | recurring signal or reusable memory candidate | [MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md) |
| `bridge` | source-linked handoff toward another owner layer | [MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md) |
| `audit_event` | review, validation, correction, retention, or supersession trace | [MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md) |

Memory objects are explicit recall material. They are not proof, route
authority, runtime state, role rights, or source-authored knowledge.

## Support Objects

| Object | Use for | First source |
|---|---|---|
| `provenance_thread` | walk-back paths, source refs, and lineage support | [PROVENANCE_THREADS](docs/PROVENANCE_THREADS.md) |
| `recall_contract` | inspect, capsule, expand, and mode/scoping expectations | [MEMORY_MODEL](docs/MEMORY_MODEL.md) and [examples](examples/AGENTS.md) |
| `inquiry_checkpoint` | checkpoint carry memory at the memo boundary | [checkpoint mechanic](mechanics/checkpoint/README.md) |
| `witness_trace` | reviewed route-return and closeout recall support | [recurrence-support mechanic](mechanics/recurrence-support/README.md) |
| `quest_chronicle` | quest witness and writeback support | [writeback mechanic](mechanics/writeback/README.md) |

Support objects help memory stay reviewable. They do not create a new object
family unless the memory model, schema, examples, and validators say so.

## Recall Modes

| Mode | Use for | First source |
|---|---|---|
| `working` | immediate bounded continuation and checkpoint-aware return | [PLAYBOOK_MEMORY_SCOPES](mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md) |
| `episodic` | event-like recall with time and source context | [MEMORY_MODEL](docs/MEMORY_MODEL.md) |
| `semantic` | concept-like recall through compact surfaces | [ROUTING_MEMORY_ADOPTION](mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md) |
| `procedural` | process-shaped recall without becoming execution authority | [MEMORY_MODEL](docs/MEMORY_MODEL.md) |
| `lineage` | provenance, recurrence, and pattern-lineage recall | [PATTERN_LINEAGE_MEMORY](mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md) |
| `source_route` | route to stronger owner surfaces rather than local overclaim | [BOUNDARIES](docs/BOUNDARIES.md) |

Recall defaults to inspect first, capsule second, expand only when needed.

## Temperature Scale

| Temperature | Meaning | First source |
|---|---|---|
| `hot` | current and actively useful, not necessarily proven | [MEMORY_TEMPERATURES](docs/MEMORY_TEMPERATURES.md) |
| `warm` | still useful, but less immediate | [MEMORY_TEMPERATURES](docs/MEMORY_TEMPERATURES.md) |
| `cool` | available background memory | [MEMORY_TEMPERATURES](docs/MEMORY_TEMPERATURES.md) |
| `cold` | low-current-use retained memory | [MEMORY_TEMPERATURES](docs/MEMORY_TEMPERATURES.md) |
| `frozen` | stable historical memory with explicit lifecycle posture | [MEMORY_TEMPERATURES](docs/MEMORY_TEMPERATURES.md) |

Temperature is current-use posture. It is not truth, proof, authority, or
freshness by itself.

## Source Families

| Family | First route |
|---|---|
| Repository authority and boundaries | [CHARTER](CHARTER.md), [BOUNDARIES](docs/BOUNDARIES.md) |
| Memory model and object canon | [MEMORY_MODEL](docs/MEMORY_MODEL.md), [MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md) |
| Trust, lifecycle, temperature, and provenance | [MEMORY_TRUST_POSTURE](docs/MEMORY_TRUST_POSTURE.md), [LIFECYCLE](docs/LIFECYCLE.md), [MEMORY_TEMPERATURES](docs/MEMORY_TEMPERATURES.md), [PROVENANCE_THREADS](docs/PROVENANCE_THREADS.md) |
| Operational boundary | [OPERATIONAL_BOUNDARY](docs/OPERATIONAL_BOUNDARY.md) |
| Memo mechanics | [mechanics](mechanics/README.md) |
| Root and docs placement | [ROOT_SURFACE_LAW](docs/ROOT_SURFACE_LAW.md) |
| Public obligations | [QUESTBOOK](QUESTBOOK.md), [quests](quests/README.md), [questbook mechanic](mechanics/questbook/README.md) |

## Generated Companions

| Surface | Role |
|---|---|
| [memo_registry.min.json](generated/memo_registry.min.json) | compact layer registry and validation command map |
| [memory_catalog.min.json](generated/memory_catalog.min.json) | compact doctrine inspect surface |
| [memory_capsules.json](generated/memory_capsules.json) | capsule hydration surface for doctrine recall |
| [memory_sections.full.json](generated/memory_sections.full.json) | expanded doctrine sections |
| [memory_object_catalog.min.json](generated/memory_object_catalog.min.json) | compact object-facing inspect surface |
| [memory_object_capsules.json](generated/memory_object_capsules.json) | capsule hydration surface for object recall |
| [memory_object_sections.full.json](generated/memory_object_sections.full.json) | expanded object-facing sections |
| [memo_mechanics.min.json](generated/memo_mechanics.min.json) | compact mechanic package index |
| [memo_mechanic_readiness.min.json](generated/memo_mechanic_readiness.min.json) | OS Abyss readiness matrix for memo mechanics |
| [quest_catalog.min.json](generated/quest_catalog.min.json) | generated quest catalog projection |
| [quest_dispatch.min.json](generated/quest_dispatch.min.json) | generated quest dispatch projection |
| [kag_export.min.json](mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json) | source-owned memo donor export for `aoa-kag` readiness |

## Notes

- `MEMORY_INDEX.md` is the map; [MEMORY_MODEL](docs/MEMORY_MODEL.md) is the
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
