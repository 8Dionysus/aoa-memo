# aoa-memo

`aoa-memo` is the memory and recall layer of the AoA ecosystem.

It exists to make memory explicit, reviewable, and bounded. Memory matters here, but memory is not proof.

> Current release: `v0.2.3`. See [CHANGELOG](CHANGELOG.md) for release notes.

## Start here

Use the shortest route by need:

- role, boundaries, and conceptual model: [CHARTER](CHARTER.md), [DESIGN](DESIGN.md), [docs/BOUNDARIES](docs/BOUNDARIES.md), and [docs/MEMORY_MODEL](docs/MEMORY_MODEL.md)
- docs topology, root placement, and decision rationale: [docs/README](docs/README.md), [docs/ROOT_SURFACE_LAW](docs/ROOT_SURFACE_LAW.md), and [docs/decisions](docs/decisions/README.md)
- agent-facing route shape: [AGENTS](AGENTS.md), [DESIGN.AGENTS](DESIGN.AGENTS.md), and the nearest nested `AGENTS.md`
- machine-checkable route-card coverage: `config/agents_mesh.json`,
  `generated/agents_mesh.min.json`, `scripts/validate_agents_mesh.py`, and
  `scripts/validate_agents_mesh_index.py`
- object canon, trust posture, and lifecycle: [docs/MEMORY_OBJECT_PROFILES](docs/MEMORY_OBJECT_PROFILES.md), [docs/MEMORY_TRUST_POSTURE](docs/MEMORY_TRUST_POSTURE.md), [docs/MEMORY_TEMPERATURES](docs/MEMORY_TEMPERATURES.md), [docs/LIFECYCLE](docs/LIFECYCLE.md), and [docs/NARRATIVE_CORE_CONTRACT](docs/NARRATIVE_CORE_CONTRACT.md)
- Titan Memory Loom, bearer-recall posture, and remembrance source-ref policy: [mechanics/titan/docs/TITAN_MEMORY_LOOM_POSTURE.md](mechanics/titan/docs/TITAN_MEMORY_LOOM_POSTURE.md), [mechanics/titan/docs/TITAN_PERSONALITY_MEMORY_POLICY.md](mechanics/titan/docs/TITAN_PERSONALITY_MEMORY_POLICY.md), [mechanics/titan/docs/TITAN_RECALL_CANDIDATE_POLICY.md](mechanics/titan/docs/TITAN_RECALL_CANDIDATE_POLICY.md), [mechanics/titan/docs/TITAN_REMEMBRANCE_SOURCE_REF_POLICY.md](mechanics/titan/docs/TITAN_REMEMBRANCE_SOURCE_REF_POLICY.md), `schemas/titan_remembrance_record.schema.json`, and `examples/titan_remembrance_record.example.json`
- antifragility failure-lesson seam: [mechanics/antifragility/docs/FAILURE_LESSON_MEMORY.md](mechanics/antifragility/docs/FAILURE_LESSON_MEMORY.md), [mechanics/antifragility/docs/FAILURE_LESSON_RECALL.md](mechanics/antifragility/docs/FAILURE_LESSON_RECALL.md), [mechanics/antifragility/docs/DRIFT_REVIEW_LESSON_MEMORY.md](mechanics/antifragility/docs/DRIFT_REVIEW_LESSON_MEMORY.md), `schemas/failure_lesson_memory_v1.json`, `examples/failure_lesson_memory.example.json`, `examples/failure_lesson_memory.lineage.example.json`, `examples/failure_lesson_memory.rollout.example.json`, and `examples/failure_lesson_memory.drift_review.example.json`
- antifragility recovery-pattern seam: [mechanics/antifragility/docs/RECOVERY_PATTERN_MEMORY.md](mechanics/antifragility/docs/RECOVERY_PATTERN_MEMORY.md), [mechanics/antifragility/docs/RECOVERY_PATTERN_RECALL.md](mechanics/antifragility/docs/RECOVERY_PATTERN_RECALL.md), [mechanics/antifragility/docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md](mechanics/antifragility/docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md), `schemas/recovery_pattern_memory_v1.json`, `examples/recovery_pattern_memory.example.json`, `examples/recovery_pattern_memory.lineage.example.json`, `examples/recovery_pattern_memory.rollout.example.json`, `examples/recovery_pattern_memory.rollback_followthrough.example.json`, `examples/recovery_pattern_memory.component_refresh.example.json`, and `examples/pattern.antifragility-stress-recovery-window.example.json`
- writeback, recurrence, and neighboring-layer seams: [docs/WITNESS_TRACE_CONTRACT](docs/WITNESS_TRACE_CONTRACT.md), [mechanics/writeback/WRITEBACK_TEMPERATURE_POLICY](mechanics/writeback/docs/WRITEBACK_TEMPERATURE_POLICY.md), [mechanics/writeback/QUEST_CHRONICLE_WRITEBACK](mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md), `schemas/quest_chronicle.schema.json`, `examples/quest_chronicle.example.json`, [mechanics/writeback/RUNTIME_WRITEBACK_SEAM](mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md), [mechanics/writeback/GROWTH_REFINERY_WRITEBACK](mechanics/writeback/docs/GROWTH_REFINERY_WRITEBACK.md), [mechanics/writeback/SELF_AGENCY_CONTINUITY_WRITEBACK](mechanics/writeback/docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md), `examples/provenance_thread.self-agency-continuity.example.json`, [docs/RECURRENCE_MEMORY_SUPPORT_SURFACES](docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md), [docs/AGENT_MEMORY_POSTURE_SEAM](docs/AGENT_MEMORY_POSTURE_SEAM.md), and [docs/PLAYBOOK_MEMORY_SCOPES](docs/PLAYBOOK_MEMORY_SCOPES.md)
- memory readiness boundary for future durable-consequence, delta, retention, and recall pressure: [docs/MEMORY_READINESS_BOUNDARY](docs/MEMORY_READINESS_BOUNDARY.md)
- Wave 1 memory gate / retention / writeback boundary contract: [docs/MEMORY_READINESS_BOUNDARY](docs/MEMORY_READINESS_BOUNDARY.md), `schemas/memory_readiness_boundary_contract.schema.json`, and `examples/memory_readiness_boundary_contract.example.json`
- bridge, export, and guardrail surfaces: [docs/KAG_TOS_BRIDGE_CONTRACT](docs/KAG_TOS_BRIDGE_CONTRACT.md), [docs/KAG_SOURCE_EXPORT](docs/KAG_SOURCE_EXPORT.md), [docs/MEMORY_EVAL_GUARDRAILS](docs/MEMORY_EVAL_GUARDRAILS.md), [docs/OPERATIONAL_BOUNDARY](docs/OPERATIONAL_BOUNDARY.md), and [mechanics/adoption/ROUTING_MEMORY_ADOPTION](mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md)
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
- failure-lesson doctrine and contract surfaces: [antifragility/FAILURE_LESSON_MEMORY](mechanics/antifragility/docs/FAILURE_LESSON_MEMORY.md), [antifragility/FAILURE_LESSON_RECALL](mechanics/antifragility/docs/FAILURE_LESSON_RECALL.md), [antifragility/DRIFT_REVIEW_LESSON_MEMORY](mechanics/antifragility/docs/DRIFT_REVIEW_LESSON_MEMORY.md), `schemas/failure_lesson_memory_v1.json`, `examples/failure_lesson_memory.example.json`, `examples/failure_lesson_memory.lineage.example.json`, `examples/failure_lesson_memory.rollout.example.json`, and `examples/failure_lesson_memory.drift_review.example.json`
- recovery-pattern doctrine, adjunct contract, and native pattern surfaces: [antifragility/RECOVERY_PATTERN_MEMORY](mechanics/antifragility/docs/RECOVERY_PATTERN_MEMORY.md), [antifragility/RECOVERY_PATTERN_RECALL](mechanics/antifragility/docs/RECOVERY_PATTERN_RECALL.md), [antifragility/ROLLBACK_FOLLOWTHROUGH_PATTERN](mechanics/antifragility/docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md), `schemas/recovery_pattern_memory_v1.json`, `examples/recovery_pattern_memory.example.json`, `examples/recovery_pattern_memory.lineage.example.json`, `examples/recovery_pattern_memory.rollout.example.json`, `examples/recovery_pattern_memory.rollback_followthrough.example.json`, `examples/recovery_pattern_memory.component_refresh.example.json`, and `examples/pattern.antifragility-stress-recovery-window.example.json`
- governance authority-boundary memory and shape guard pruning:
  [mechanics/governance](mechanics/governance/README.md),
  [governance/GOVERNANCE_MEMORY_BOUNDARIES](mechanics/governance/docs/GOVERNANCE_MEMORY_BOUNDARIES.md),
  [governance/FEDERATION_MEMORY_BOUNDARIES](mechanics/governance/docs/FEDERATION_MEMORY_BOUNDARIES.md),
  [mechanics/shape-guard](mechanics/shape-guard/README.md), and
  [shape-guard/VIA_NEGATIVA_CHECKLIST](mechanics/shape-guard/docs/VIA_NEGATIVA_CHECKLIST.md)
- writeback, intake, runtime support, and landing governance surfaces: `generated/runtime_writeback_targets.min.json`, `generated/runtime_writeback_intake.min.json`, `generated/runtime_writeback_governance.min.json`, [mechanics/writeback/RUNTIME_WRITEBACK_SEAM](mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md), [mechanics/writeback/GROWTH_REFINERY_WRITEBACK](mechanics/writeback/docs/GROWTH_REFINERY_WRITEBACK.md), [mechanics/writeback/QUEST_CHRONICLE_WRITEBACK](mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md), `schemas/quest_chronicle.schema.json`, and `examples/quest_chronicle.example.json`
- memory readiness boundary: [docs/MEMORY_READINESS_BOUNDARY](docs/MEMORY_READINESS_BOUNDARY.md)
- Titan receipt memory, recall candidates, remembrance source refs, bridge digest, and closeout memory posture: [mechanics/titan/docs/TITAN_MEMORY_POSTURE.md](mechanics/titan/docs/TITAN_MEMORY_POSTURE.md), [mechanics/titan/docs/TITAN_MEMORY_LOOM_POSTURE.md](mechanics/titan/docs/TITAN_MEMORY_LOOM_POSTURE.md), [mechanics/titan/docs/TITAN_REMEMBRANCE_SOURCE_REF_POLICY.md](mechanics/titan/docs/TITAN_REMEMBRANCE_SOURCE_REF_POLICY.md), [mechanics/titan/docs/TITAN_BRIDGE_MEMORY_POSTURE.md](mechanics/titan/docs/TITAN_BRIDGE_MEMORY_POSTURE.md), [mechanics/titan/docs/TITAN_CONSOLE_MEMORY_DIGEST.md](mechanics/titan/docs/TITAN_CONSOLE_MEMORY_DIGEST.md), [mechanics/titan/docs/TITAN_CLOSEOUT_MEMORY_POSTURE.md](mechanics/titan/docs/TITAN_CLOSEOUT_MEMORY_POSTURE.md), `schemas/titan_remembrance_record.schema.json`, and `examples/titan_remembrance_record.example.json`
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

## Topology spine

The first topology hardening surface is now source-authored rather than
generated:

- [DESIGN](DESIGN.md) names the memory-layer system form
- [DESIGN.AGENTS](DESIGN.AGENTS.md) names the agent-facing guidance form
- [docs/README](docs/README.md) maps the current docs district
- [docs/ROOT_SURFACE_LAW](docs/ROOT_SURFACE_LAW.md) governs root and docs-root placement
- [docs/decisions](docs/decisions/README.md) preserves durable rationale
- [.agents/spark](.agents/spark/AGENTS.md) is the maintained fast-loop Spark lane
- `config/agents_mesh.json` and `generated/agents_mesh.min.json` make current
  route-card coverage machine-checkable
- [mechanics](mechanics/README.md) owns memo-side antifragility, Agon, Titan,
  adoption, governance, shape-guard, writeback, and retention mechanics with
  package cards, owner maps, legacy bridges, and
  `generated/memo_mechanics.min.json`
- [mechanics/antifragility](mechanics/antifragility/README.md) is the active
  home for former flat failure-lesson and recovery-pattern surfaces
- [mechanics/agon](mechanics/agon/README.md) is the active home for former
  flat and transitional Agon memory surfaces
- [mechanics/titan](mechanics/titan/README.md) is the active home for former
  flat and transitional Titan memory posture surfaces
- [mechanics/adoption](mechanics/adoption/README.md),
  [mechanics/governance](mechanics/governance/README.md),
  [mechanics/shape-guard](mechanics/shape-guard/README.md),
  [mechanics/writeback](mechanics/writeback/README.md), and
  [mechanics/retention](mechanics/retention/README.md) are the active homes for
  the former flat adoption/governance/shape-guard/writeback/retention
  docs-root families

This spine does not move flat docs by itself. It exists so later mechanic,
rollback, or AGENTS-mesh work can land through named owner routes
instead of cosmetic cleanup.

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
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python scripts/validate_docs_districts.py
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

The current topology pass adds the memory-layer design and docs-route spine.
Antifragility, Agon, Titan, adoption, governance, shape-guard, writeback, and
retention docs now live under `mechanics/` as memo mechanics with owner maps,
validation, and legacy route maps. Other flat `docs/*.md` surfaces remain active until
their validated district or mechanic routes replace them.

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
