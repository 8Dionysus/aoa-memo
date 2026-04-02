# aoa-memo

`aoa-memo` is the memory and recall layer of the AoA ecosystem.

It exists to make memory explicit, reviewable, and bounded. Memory matters here, but memory is not proof.

## Start here

Use the shortest route by need:

- role, boundaries, and conceptual model: [CHARTER](CHARTER.md), [docs/BOUNDARIES](docs/BOUNDARIES.md), and [docs/MEMORY_MODEL](docs/MEMORY_MODEL.md)
- object canon, trust posture, and lifecycle: [docs/MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md), [docs/MEMORY_TRUST_POSTURE](docs/MEMORY_TRUST_POSTURE.md), [docs/MEMORY_TEMPERATURES](docs/MEMORY_TEMPERATURES.md), [docs/LIFECYCLE](docs/LIFECYCLE.md), and [docs/NARRATIVE_CORE_CONTRACT](docs/NARRATIVE_CORE_CONTRACT.md)
- writeback, recurrence, and neighboring-layer seams: [docs/WITNESS_TRACE_CONTRACT](docs/WITNESS_TRACE_CONTRACT.md), [docs/WRITEBACK_TEMPERATURE_POLICY](docs/WRITEBACK_TEMPERATURE_POLICY.md), [docs/QUEST_CHRONICLE_WRITEBACK](docs/QUEST_CHRONICLE_WRITEBACK.md), [docs/RUNTIME_WRITEBACK_SEAM](docs/RUNTIME_WRITEBACK_SEAM.md), [docs/RECURRENCE_MEMORY_SUPPORT_SURFACES](docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md), [docs/AGENT_MEMORY_POSTURE_SEAM](docs/AGENT_MEMORY_POSTURE_SEAM.md), and [docs/PLAYBOOK_MEMORY_SCOPES](docs/PLAYBOOK_MEMORY_SCOPES.md)
- bridge, export, and guardrail surfaces: [docs/KAG_TOS_BRIDGE_CONTRACT](docs/KAG_TOS_BRIDGE_CONTRACT.md), [docs/KAG_SOURCE_EXPORT](docs/KAG_SOURCE_EXPORT.md), [docs/MEMORY_EVAL_GUARDRAILS](docs/MEMORY_EVAL_GUARDRAILS.md), [docs/OPERATIONAL_BOUNDARY](docs/OPERATIONAL_BOUNDARY.md), and [docs/ROUTING_MEMORY_ADOPTION](docs/ROUTING_MEMORY_ADOPTION.md)
- current direction: [ROADMAP](ROADMAP.md)

## Public recall entrypoints

For concrete recall contracts, start with:

- `examples/recall_contract.working.json`
- `examples/recall_contract.semantic.json`
- `examples/recall_contract.lineage.json`
- `examples/recall_contract.router.semantic.json`
- `examples/recall_contract.router.lineage.json`
- `examples/recall_contract.object.working.json`
- `examples/recall_contract.object.semantic.json`
- `examples/recall_contract.object.lineage.json`
- `examples/recall_contract.object.working.return.json`

The doctrine-first and router-facing recall contracts remain stable. The object-facing family is the parallel entrypoint over curated memory objects, and it follows the same `inspect -> capsule -> expand` join rule.

If you are editing inside `schemas/`, `examples/`, `generated/`, or `scripts/`, also follow the nested `AGENTS.md` in that directory.

## What `aoa-memo` owns

This repository is the source of truth for:

- memory objects and recall surfaces
- provenance threads and trace-bearing memory support surfaces
- temporal relevance, salience, and temperature posture
- memory-oriented retrieval contracts
- the boundary between memory, proof, execution, and routing

## What it does not own

Do not treat this repository as the main home for:

- reusable techniques in `aoa-techniques`
- bounded skill workflows in `aoa-skills`
- eval bundles or verdict logic in `aoa-evals`
- navigation and dispatch logic in `aoa-routing`
- role contracts in `aoa-agents`
- scenario composition in `aoa-playbooks`
- derived knowledge substrate semantics in `aoa-kag`

Memory is valuable. It is not the same thing as source meaning, workflow meaning, or proof.

## Current public surfaces

The committed machine-readable surfaces group into four families:

- root registry: `generated/memo_registry.min.json`
- doctrine family: `generated/memory_catalog.json`, `generated/memory_catalog.min.json`, `generated/memory_capsules.json`, and `generated/memory_sections.full.json`
- object family: `generated/memory_object_catalog.json`, `generated/memory_object_catalog.min.json`, `generated/memory_object_capsules.json`, and `generated/memory_object_sections.full.json`
- source-owned memo donor export: `generated/kag_export.min.json`

`provenance_thread`, `witness_trace`, `inquiry_checkpoint`, and checkpoint-to-memory contract surfaces remain support seams in this split, not a third generated memory-object family.

## Go here when...

- you need the ecosystem center and layer map: [`Agents-of-Abyss`](https://github.com/8Dionysus/Agents-of-Abyss)
- you need the smallest next object or dispatch hint: [`aoa-routing`](https://github.com/8Dionysus/aoa-routing)
- you need source-owned practice, execution, or proof meaning: [`aoa-techniques`](https://github.com/8Dionysus/aoa-techniques), [`aoa-skills`](https://github.com/8Dionysus/aoa-skills), or [`aoa-evals`](https://github.com/8Dionysus/aoa-evals)
- you need explicit role contracts and handoff posture: [`aoa-agents`](https://github.com/8Dionysus/aoa-agents)

## Build and validate

The canonical validator is:

```bash
python scripts/validate_memo.py
```

For the full local validation pass, run:

```bash
python scripts/generate_memory_object_surfaces.py
python scripts/generate_kag_export.py
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_memory_object_surfaces.py
python scripts/validate_lifecycle_audit_examples.py
```

`validate_memo.py` also checks the local guidance surfaces in `schemas/`, `examples/`, `generated/`, and `scripts/`.

## Current contour

`aoa-memo` is in contract hardening. The public baseline now includes doctrine surfaces, object-facing surfaces, a narrow source-owned memo KAG export, writeback seams, bridge/export contracts, and memo-side guardrail handoff surfaces without turning the repository into runtime infrastructure or a graph platform.

The current downstream guardrail pilot stays intentionally narrow: recall precision, provenance fidelity, and staleness. That keeps the memo layer explicit and reviewable without pretending it is already full proof doctrine.

## License

Apache-2.0
