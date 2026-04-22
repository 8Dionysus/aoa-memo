# aoa-memo

`aoa-memo` is the memory and recall layer of the AoA ecosystem.

It exists to make memory explicit, reviewable, and bounded. Memory matters here, but memory is not proof.

> Current release: `v0.2.2`. See [CHANGELOG](CHANGELOG.md) for release notes.

## Start here

Use the shortest route by need:

- role, boundaries, and conceptual model: [CHARTER](CHARTER.md), [docs/BOUNDARIES](docs/BOUNDARIES.md), and [docs/MEMORY_MODEL](docs/MEMORY_MODEL.md)
- object canon, trust posture, and lifecycle: [docs/MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md), [docs/MEMORY_TRUST_POSTURE](docs/MEMORY_TRUST_POSTURE.md), [docs/MEMORY_TEMPERATURES](docs/MEMORY_TEMPERATURES.md), [docs/LIFECYCLE](docs/LIFECYCLE.md), and [docs/NARRATIVE_CORE_CONTRACT](docs/NARRATIVE_CORE_CONTRACT.md)
- Titan Memory Loom, bearer-recall posture, and remembrance source-ref policy: [docs/TITAN_MEMORY_LOOM_POSTURE.md](docs/TITAN_MEMORY_LOOM_POSTURE.md), [docs/TITAN_PERSONALITY_MEMORY_POLICY.md](docs/TITAN_PERSONALITY_MEMORY_POLICY.md), [docs/TITAN_RECALL_CANDIDATE_POLICY.md](docs/TITAN_RECALL_CANDIDATE_POLICY.md), [docs/TITAN_REMEMBRANCE_SOURCE_REF_POLICY.md](docs/TITAN_REMEMBRANCE_SOURCE_REF_POLICY.md), `schemas/titan_remembrance_record.schema.json`, and `examples/titan_remembrance_record.example.json`
- antifragility failure-lesson seam: [docs/FAILURE_LESSON_MEMORY.md](docs/FAILURE_LESSON_MEMORY.md), [docs/FAILURE_LESSON_RECALL.md](docs/FAILURE_LESSON_RECALL.md), [docs/DRIFT_REVIEW_LESSON_MEMORY.md](docs/DRIFT_REVIEW_LESSON_MEMORY.md), `schemas/failure_lesson_memory_v1.json`, `examples/failure_lesson_memory.example.json`, `examples/failure_lesson_memory.lineage.example.json`, `examples/failure_lesson_memory.rollout.example.json`, and `examples/failure_lesson_memory.drift_review.example.json`
- antifragility recovery-pattern seam: [docs/RECOVERY_PATTERN_MEMORY.md](docs/RECOVERY_PATTERN_MEMORY.md), [docs/RECOVERY_PATTERN_RECALL.md](docs/RECOVERY_PATTERN_RECALL.md), [docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md](docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md), `schemas/recovery_pattern_memory_v1.json`, `examples/recovery_pattern_memory.example.json`, `examples/recovery_pattern_memory.lineage.example.json`, `examples/recovery_pattern_memory.rollout.example.json`, `examples/recovery_pattern_memory.rollback_followthrough.example.json`, `examples/recovery_pattern_memory.component_refresh.example.json`, and `examples/pattern.antifragility-stress-recovery-window.example.json`
- writeback, recurrence, and neighboring-layer seams: [docs/WITNESS_TRACE_CONTRACT](docs/WITNESS_TRACE_CONTRACT.md), [docs/WRITEBACK_TEMPERATURE_POLICY](docs/WRITEBACK_TEMPERATURE_POLICY.md), [docs/QUEST_CHRONICLE_WRITEBACK](docs/QUEST_CHRONICLE_WRITEBACK.md), `schemas/quest_chronicle.schema.json`, `examples/quest_chronicle.example.json`, [docs/RUNTIME_WRITEBACK_SEAM](docs/RUNTIME_WRITEBACK_SEAM.md), [docs/GROWTH_REFINERY_WRITEBACK](docs/GROWTH_REFINERY_WRITEBACK.md), [docs/SELF_AGENCY_CONTINUITY_WRITEBACK](docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md), `examples/provenance_thread.self-agency-continuity.example.json`, [docs/RECURRENCE_MEMORY_SUPPORT_SURFACES](docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md), [docs/AGENT_MEMORY_POSTURE_SEAM](docs/AGENT_MEMORY_POSTURE_SEAM.md), and [docs/PLAYBOOK_MEMORY_SCOPES](docs/PLAYBOOK_MEMORY_SCOPES.md)
- memory readiness boundary for future durable-consequence, delta, retention, and recall pressure: [docs/MEMORY_READINESS_BOUNDARY](docs/MEMORY_READINESS_BOUNDARY.md)
- Wave 1 memory gate / retention / writeback boundary contract: [docs/MEMORY_READINESS_BOUNDARY](docs/MEMORY_READINESS_BOUNDARY.md), `schemas/memory_readiness_boundary_contract.schema.json`, and `examples/memory_readiness_boundary_contract.example.json`
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

## Route by need

- doctrine and object reader surfaces: `generated/memory_catalog.json`, `generated/memory_catalog.min.json`, `generated/memory_capsules.json`, `generated/memory_sections.full.json`, `generated/memory_object_catalog.json`, `generated/memory_object_catalog.min.json`, `generated/memory_object_capsules.json`, and `generated/memory_object_sections.full.json`
- recall contracts and memory-object examples: `examples/recall_contract.*.json`, `examples/core_memory_contract.example.json`, `examples/checkpoint_to_memory_contract.example.json`, and `examples/memory_object_surface_manifest.json`
- failure-lesson doctrine and contract surfaces: [docs/FAILURE_LESSON_MEMORY](docs/FAILURE_LESSON_MEMORY.md), [docs/FAILURE_LESSON_RECALL](docs/FAILURE_LESSON_RECALL.md), [docs/DRIFT_REVIEW_LESSON_MEMORY](docs/DRIFT_REVIEW_LESSON_MEMORY.md), `schemas/failure_lesson_memory_v1.json`, `examples/failure_lesson_memory.example.json`, `examples/failure_lesson_memory.lineage.example.json`, `examples/failure_lesson_memory.rollout.example.json`, and `examples/failure_lesson_memory.drift_review.example.json`
- recovery-pattern doctrine, adjunct contract, and native pattern surfaces: [docs/RECOVERY_PATTERN_MEMORY](docs/RECOVERY_PATTERN_MEMORY.md), [docs/RECOVERY_PATTERN_RECALL](docs/RECOVERY_PATTERN_RECALL.md), [docs/ROLLBACK_FOLLOWTHROUGH_PATTERN](docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md), `schemas/recovery_pattern_memory_v1.json`, `examples/recovery_pattern_memory.example.json`, `examples/recovery_pattern_memory.lineage.example.json`, `examples/recovery_pattern_memory.rollout.example.json`, `examples/recovery_pattern_memory.rollback_followthrough.example.json`, `examples/recovery_pattern_memory.component_refresh.example.json`, and `examples/pattern.antifragility-stress-recovery-window.example.json`
- via negativa pruning checklist: [docs/VIA_NEGATIVA_CHECKLIST](docs/VIA_NEGATIVA_CHECKLIST.md)
- writeback, intake, runtime support, and landing governance surfaces: `generated/runtime_writeback_targets.min.json`, `generated/runtime_writeback_intake.min.json`, `generated/runtime_writeback_governance.min.json`, [docs/RUNTIME_WRITEBACK_SEAM](docs/RUNTIME_WRITEBACK_SEAM.md), [docs/GROWTH_REFINERY_WRITEBACK](docs/GROWTH_REFINERY_WRITEBACK.md), [docs/QUEST_CHRONICLE_WRITEBACK](docs/QUEST_CHRONICLE_WRITEBACK.md), `schemas/quest_chronicle.schema.json`, and `examples/quest_chronicle.example.json`
- memory readiness boundary: [docs/MEMORY_READINESS_BOUNDARY](docs/MEMORY_READINESS_BOUNDARY.md)
- Titan receipt memory, recall candidates, remembrance source refs, bridge digest, and closeout memory posture: [docs/TITAN_MEMORY_POSTURE.md](docs/TITAN_MEMORY_POSTURE.md), [docs/TITAN_MEMORY_LOOM_POSTURE.md](docs/TITAN_MEMORY_LOOM_POSTURE.md), [docs/TITAN_REMEMBRANCE_SOURCE_REF_POLICY.md](docs/TITAN_REMEMBRANCE_SOURCE_REF_POLICY.md), [docs/TITAN_BRIDGE_MEMORY_POSTURE.md](docs/TITAN_BRIDGE_MEMORY_POSTURE.md), [docs/TITAN_CONSOLE_MEMORY_DIGEST.md](docs/TITAN_CONSOLE_MEMORY_DIGEST.md), [docs/TITAN_CLOSEOUT_MEMORY_POSTURE.md](docs/TITAN_CLOSEOUT_MEMORY_POSTURE.md), `schemas/titan_remembrance_record.schema.json`, and `examples/titan_remembrance_record.example.json`
- owner-local live receipt publication for closeout/stats integration: `scripts/publish_live_receipts.py` and `.aoa/live_receipts/memo-writeback-receipts.jsonl`
- bridge, export, and guardrail surfaces: `generated/kag_export.min.json`, [docs/KAG_SOURCE_EXPORT](docs/KAG_SOURCE_EXPORT.md), [docs/KAG_TOS_BRIDGE_CONTRACT](docs/KAG_TOS_BRIDGE_CONTRACT.md), and [docs/MEMORY_EVAL_GUARDRAILS](docs/MEMORY_EVAL_GUARDRAILS.md)
- schemas and local validation: `schemas/`, `python scripts/validate_memo.py`, `python scripts/validate_memory_surfaces.py`, `python scripts/validate_memory_object_surfaces.py`, `python scripts/validate_lifecycle_audit_examples.py`, and `python -m pytest -q tests`

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

For a read-only current-state validation pass, run:

```bash
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_memory_object_surfaces.py
python scripts/validate_lifecycle_audit_examples.py
python -m pytest -q tests
```

`validate_memo.py` also checks the local guidance surfaces in `schemas/`, `examples/`, `generated/`, and `scripts/`.

If you changed generator-backed surfaces, regenerate only the touched families first:

```bash
python scripts/generate_memory_object_surfaces.py
python scripts/generate_kag_export.py
python scripts/generate_runtime_writeback_targets.py
python scripts/generate_runtime_writeback_intake.py
python scripts/generate_runtime_writeback_governance.py
python scripts/generate_phase_alpha_writeback_map.py
```

Then rerun the read-only validation pass above and inspect `git status -sb` before opening a PR.

## Current contour

`aoa-memo` is in contract hardening. The public baseline now includes doctrine surfaces, object-facing surfaces, a narrow source-owned memo KAG export, writeback seams, bridge/export contracts, and memo-side guardrail handoff surfaces without turning the repository into runtime infrastructure or a graph platform.

The current downstream guardrail pilot stays intentionally narrow: recall precision, provenance fidelity, and staleness. That keeps the memo layer explicit and reviewable without pretending it is already full proof doctrine.

High-pressure memory readiness now has an owner-local boundary map. Future
durable-consequence, delta, retention, and recall pressure should route through
existing memo objects first and then out to `aoa-evals`, `aoa-kag`,
`aoa-routing`, `aoa-agents`, or `abyss-stack` when proof, graph lift,
navigation, role authority, or runtime retention is the real owner concern.

Antifragility wave two stays inside that boundary. Failure lessons are bounded
memory context for later recall and operator posture, not a new proof family
and not a live runtime writeback lane.

Antifragility wave four extends that same posture to reviewed recovery
patterns. Memo can preserve repeated-window recovery context and native
`pattern` recall surfaces, but it still stays downstream from source-owned
receipts, eval proof, and derived stats summaries.

## License

Apache-2.0
