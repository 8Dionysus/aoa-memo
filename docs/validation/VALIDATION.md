# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `docs/validation/AGENTS.md`

```bash
python scripts/root-topology/validate_validator_topology.py
python -m pytest -q tests/root-topology/test_validator_topology.py tests/root-topology/test_validation_lanes.py
python scripts/ci_gate.py --mode source-fast
```
### Preserved route from `docs/decisions/AGENTS.md`

```bash
python scripts/root-topology/build_decision_indexes.py --check
python -m pytest -q tests
python scripts/release/release_check.py
```

### Preserved route from `docs/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
python scripts/agents/validate_semantic_agents.py
```

<!-- Preserved on-demand procedure from `.agents/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `.agents/AGENTS.md`

```bash
python .agents/spark/scripts/validate_spark_lane.py
python -m unittest discover -s .agents/spark/tests -p 'test*.py'
python -m pytest -q tests/root-topology/test_topology_spine.py
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `.agents/spark/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `.agents/spark/AGENTS.md`

```bash
python .agents/spark/scripts/validate_spark_lane.py
python -m unittest discover -s .agents/spark/tests -p 'test*.py'
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `config/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `config/AGENTS.md`

```bash
python scripts/mechanics/validate_mechanic_artifact_topology.py
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
```
```bash
python scripts/memory/validate_memo.py --profile schema
python scripts/memory/validate_memo.py --profile memory-context
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```
```bash
python scripts/root-topology/validate_validator_topology.py
python -m pytest -q tests/root-topology/test_validation_lanes.py tests/root-topology/test_validator_topology.py tests/root-topology/test_ci_gate.py tests/root-topology/test_release_check.py
```

<!-- Preserved on-demand procedure from `config/agents/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `config/agents/AGENTS.md`

```bash
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
```

<!-- Preserved on-demand procedure from `config/mechanics/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `config/mechanics/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `config/memory-ports/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `config/memory-ports/AGENTS.md`

```bash
python scripts/memory/build_memo_port_vocabulary.py --check
python scripts/memory/validate_local_memo_port.py --path examples/memory-ports/example-port
```

<!-- Preserved on-demand procedure from `config/root-topology/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `config/root-topology/AGENTS.md`

```bash
python scripts/mechanics/validate_mechanic_artifact_topology.py
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
```

<!-- Preserved on-demand procedure from `docs/boundaries/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `docs/boundaries/AGENTS.md`

```bash
python scripts/memory/validate_memo.py --profile schema
python scripts/memory/validate_memo.py --profile runtime-boundary
python scripts/memory/validate_memory_operations.py
python scripts/root-topology/validate_docs_districts.py
```

<!-- Preserved on-demand procedure from `docs/memory/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `docs/memory/AGENTS.md`

```bash
python scripts/memory/validate_memo.py --profile schema
python scripts/memory/validate_memo.py --profile memory-context
python scripts/memory/validate_memory_operations.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_local_memo_port.py --path examples/memory-ports/example-port
python scripts/memory/build_memory_operational_readouts.py --write --live
python scripts/memory/build_memory_operational_readouts.py --check --live
python scripts/memory/validate_abyss_machine_memory_object_bundle.py
```

<!-- Preserved on-demand procedure from `docs/posture/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `docs/posture/AGENTS.md`

```bash
python scripts/memory/validate_memo.py --profile schema
python scripts/memory/validate_memo.py --profile memory-context
python scripts/memory/validate_memory_operations.py
python scripts/memory/validate_lifecycle_audit_examples.py
```

<!-- Preserved on-demand procedure from `docs/root/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `docs/root/AGENTS.md`

```bash
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `docs/testing/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `docs/testing/AGENTS.md`

```bash
python -m pytest -q tests/root-topology/test_test_topology.py
python -m pytest -q tests/root-topology/test_validation_lanes.py
python -m pytest -q tests/root-topology/test_validator_topology.py
python scripts/ci_gate.py --mode source-fast
```

<!-- Preserved on-demand procedure from `examples/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `examples/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
python scripts/memory/validate_lifecycle_audit_examples.py
```
```bash
python scripts/memory/generate_memory_object_surfaces.py
```

<!-- Preserved on-demand procedure from `examples/generated-surfaces/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `examples/generated-surfaces/AGENTS.md`

```bash
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memory_object_surfaces.py
```

<!-- Preserved on-demand procedure from `examples/lifecycle/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `examples/lifecycle/AGENTS.md`

```bash
python scripts/memory/validate_lifecycle_audit_examples.py
python scripts/memory/validate_memo.py
```

<!-- Preserved on-demand procedure from `examples/memory-objects/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `examples/memory-objects/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_object_surfaces.py
```

<!-- Preserved on-demand procedure from `examples/memory-ports/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `examples/memory-ports/AGENTS.md`

```bash
python scripts/memory/validate_local_memo_port.py --path examples/memory-ports/example-port
python scripts/memory/build_local_memo_port_index.py --path examples/memory-ports/example-port --check
```

<!-- Preserved on-demand procedure from `examples/phase-alpha/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `examples/phase-alpha/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_object_surfaces.py
```

<!-- Preserved on-demand procedure from `examples/recall/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `examples/recall/AGENTS.md`

```bash
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
python scripts/memory/validate_memory_operations.py
```

<!-- Preserved on-demand procedure from `examples/support-objects/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `examples/support-objects/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
```

<!-- Preserved on-demand procedure from `generated/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `generated/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
python scripts/memory/validate_abyss_machine_memory_object_bundle.py
python scripts/memory/build_memory_operational_readouts.py --check
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
python scripts/mechanics/validate_mechanic_artifact_inventory.py
python scripts/mechanics/validate_memo_mechanic_cards.py
python scripts/mechanics/validate_memo_mechanic_owner_routes.py
python scripts/mechanics/validate_memo_mechanic_landing_logs.py
python scripts/mechanics/validate_memo_mechanic_readiness.py
```
```bash
python scripts/memory/generate_memory_object_surfaces.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py
python mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py
```

<!-- Preserved on-demand procedure from `generated/agents/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `generated/agents/AGENTS.md`

```bash
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
```

<!-- Preserved on-demand procedure from `generated/mechanics/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `generated/mechanics/AGENTS.md`

```bash
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/mechanics/validate_memo_mechanic_readiness.py
```

<!-- Preserved on-demand procedure from `generated/memory-objects/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `generated/memory-objects/AGENTS.md`

```bash
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memory_object_surfaces.py
```

<!-- Preserved on-demand procedure from `generated/memory/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `generated/memory/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/build_memory_operational_readouts.py --check
```

<!-- Preserved on-demand procedure from `generated/quests/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `generated/quests/AGENTS.md`

```bash
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
```

<!-- Preserved on-demand procedure from `generated/root-topology/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `generated/root-topology/AGENTS.md`

```bash
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
```

<!-- Preserved on-demand procedure from `manifests/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `manifests/AGENTS.md`

```bash
python mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_memo_prebindings.py
python -m pytest -q mechanics/agon/parts/stage-landing-and-stop-lines/tests
python scripts/memory/validate_memo.py
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/AGENTS.md`

```bash
  python scripts/mechanics/validate_mechanic_artifact_topology.py
  python scripts/mechanics/build_mechanic_artifact_inventory.py --check
  python scripts/mechanics/validate_mechanic_artifact_inventory.py
  ```
```bash
  python scripts/mechanics/validate_mechanic_artifact_topology.py
  python scripts/mechanics/build_mechanic_artifact_inventory.py --check
  python scripts/mechanics/validate_mechanic_artifact_inventory.py
  python scripts/mechanics/build_memo_mechanic_landing_logs.py --check
  python scripts/mechanics/validate_memo_mechanic_landing_logs.py
  python scripts/mechanics/build_memo_mechanic_readiness.py --check
  python scripts/mechanics/validate_memo_mechanic_readiness.py
  python scripts/mechanics/validate_memo_mechanics.py
  ```
```bash
  python scripts/mechanics/validate_memo_mechanic_parts.py
  ```
```bash
  python scripts/mechanics/build_memo_mechanic_cards.py --check
  python scripts/mechanics/validate_memo_mechanic_cards.py
  ```
```bash
  python scripts/mechanics/build_memo_mechanic_owner_routes.py --check
  python scripts/mechanics/validate_memo_mechanic_owner_routes.py
  ```
```bash
  python scripts/mechanics/build_memo_mechanic_landing_logs.py --check
  python scripts/mechanics/validate_memo_mechanic_landing_logs.py
  ```
```bash
  python scripts/mechanics/build_memo_mechanic_readiness.py --check
  python scripts/mechanics/validate_memo_mechanic_readiness.py
  ```
```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/validate_memo_mechanic_parts.py
python scripts/mechanics/build_memo_mechanic_cards.py --check
python scripts/mechanics/validate_memo_mechanic_cards.py
python scripts/mechanics/build_memo_mechanic_owner_routes.py --check
python scripts/mechanics/validate_memo_mechanic_owner_routes.py
python scripts/mechanics/build_memo_mechanic_landing_logs.py --check
python scripts/mechanics/validate_memo_mechanic_landing_logs.py
python scripts/mechanics/build_memo_mechanic_readiness.py --check
python scripts/mechanics/validate_memo_mechanic_readiness.py
python scripts/mechanics/validate_mechanic_artifact_topology.py
python scripts/mechanics/build_mechanic_artifact_inventory.py --check
python scripts/mechanics/validate_mechanic_artifact_inventory.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/adoption/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/adoption/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/adoption/parts/adoption-boundary/tests mechanics/adoption/parts/revision-and-retention-pressure/tests mechanics/adoption/parts/scar-and-routing-adoption/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/adoption/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/adoption/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/adoption/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/adoption/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/adoption/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/adoption/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/agon/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/agon/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_memo_prebindings.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_epistemic_memo_bridge.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_kag_memo_evidence_package_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_mechanical_trial_memo_intakes.py
python mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_retention_rank_memo_bridge.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_slc_memo_bridge_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_sophian_memo_evidence_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_vds_memo_bridge.py
python -m pytest -q mechanics/agon/parts/prebinding-and-candidate-intake/tests mechanics/agon/parts/bridge-and-evidence-seams/tests mechanics/agon/parts/stage-landing-and-stop-lines/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/agon/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/agon/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_memo_prebindings.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_epistemic_memo_bridge.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_kag_memo_evidence_package_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_mechanical_trial_memo_intakes.py
python mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_retention_rank_memo_bridge.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_slc_memo_bridge_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_sophian_memo_evidence_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_vds_memo_bridge.py
python -m pytest -q mechanics/agon/parts/prebinding-and-candidate-intake/tests mechanics/agon/parts/bridge-and-evidence-seams/tests mechanics/agon/parts/stage-landing-and-stop-lines/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/agon/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/agon/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/agon/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/agon/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/antifragility/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/antifragility/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/antifragility/parts/failure-lesson-memory/tests mechanics/antifragility/parts/recovery-pattern-memory/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/antifragility/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/antifragility/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/antifragility/parts/failure-lesson-memory/tests mechanics/antifragility/parts/recovery-pattern-memory/tests
```

<!-- Preserved on-demand procedure from `mechanics/antifragility/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/antifragility/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/antifragility/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/antifragility/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/checkpoint/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/checkpoint/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/checkpoint/parts/checkpoint-memory-boundary/tests/test_checkpoint_mechanic.py tests/memory/test_memo_schema_contracts.py tests/memory/test_memo_memory_context_boundaries.py mechanics/consumer-handoff/parts/downstream-feed-regression/tests tests/mechanics/test_memo_mechanics.py tests/agents/test_agents_mesh.py tests/root-topology/test_mechanic_artifact_topology.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/checkpoint/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/checkpoint/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/checkpoint/parts/checkpoint-memory-boundary/tests/test_checkpoint_mechanic.py tests/memory/test_memo_schema_contracts.py tests/memory/test_memo_memory_context_boundaries.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/checkpoint/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/checkpoint/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/checkpoint/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/checkpoint/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/consumer-handoff/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/consumer-handoff/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_surfaces.py
python -m pytest -q mechanics/consumer-handoff/parts/downstream-feed-regression/tests mechanics/consumer-handoff/parts/mcp-organ-access/tests mechanics/consumer-handoff/parts/mcp-owner-evidence-review/tests mechanics/consumer-handoff/parts/orchestrator-recall-alignment/tests mechanics/consumer-handoff/parts/playbook-scope-handoff/tests tests/memory/test_memo_handoff_boundaries.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/consumer-handoff/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/consumer-handoff/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_surfaces.py
python -m pytest -q mechanics/consumer-handoff/parts/downstream-feed-regression/tests mechanics/consumer-handoff/parts/playbook-scope-handoff/tests/test_playbook_memory_scopes.py tests/memory/test_memo_handoff_boundaries.py
```

<!-- Preserved on-demand procedure from `mechanics/consumer-handoff/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/consumer-handoff/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/consumer-handoff/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/consumer-handoff/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/governance/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/governance/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/governance/parts/governance-boundary/tests tests/mechanics/test_memo_mechanics.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/governance/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/governance/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/governance/parts/governance-boundary/tests tests/mechanics/test_memo_mechanics.py
```

<!-- Preserved on-demand procedure from `mechanics/governance/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/governance/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/governance/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/governance/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/lineage-harvest/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/lineage-harvest/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/lineage-harvest/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/lineage-harvest/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/memory/validate_memo.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/lineage-harvest/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/lineage-harvest/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/lineage-harvest/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/lineage-harvest/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/operational-gate/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/operational-gate/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_operations.py
python -m pytest -q mechanics/operational-gate/parts/deployment-incident-gate/tests mechanics/operational-gate/parts/write-path-guardrails/tests mechanics/operational-gate/parts/post-release-boundaries/tests tests/mechanics/test_memo_mechanics.py tests/agents/test_agents_mesh.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/operational-gate/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/operational-gate/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/operational-gate/parts/deployment-incident-gate/tests mechanics/operational-gate/parts/post-release-boundaries/tests
```

<!-- Preserved on-demand procedure from `mechanics/operational-gate/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/operational-gate/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/operational-gate/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/operational-gate/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/questbook/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/questbook/AGENTS.md`

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/questbook/parts/source-contract/tests tests/memory/test_memo_questbook_boundaries.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/questbook/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/questbook/docs/AGENTS.md`

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python scripts/mechanics/validate_memo_mechanics.py
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/questbook/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/questbook/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/questbook/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/questbook/parts/AGENTS.md`

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/memory/validate_memo.py
```

<!-- Preserved on-demand procedure from `mechanics/readiness-boundary/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/readiness-boundary/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/readiness-boundary/parts/memory-readiness-boundary/tests/test_readiness_boundary_mechanic.py tests/memory/test_memo_memory_context_boundaries.py tests/root-topology/test_current_direction_routes.py tests/root-topology/test_mechanic_artifact_topology.py tests/mechanics/test_memo_mechanics.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/readiness-boundary/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/readiness-boundary/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/readiness-boundary/parts/memory-readiness-boundary/tests/test_readiness_boundary_mechanic.py
```

<!-- Preserved on-demand procedure from `mechanics/readiness-boundary/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/readiness-boundary/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/readiness-boundary/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/readiness-boundary/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/recurrence-support/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/recurrence-support/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/recurrence-support/parts/witness-trace-contract/tests/test_recurrence_support_mechanic.py tests/mechanics/test_memo_mechanics.py tests/agents/test_agents_mesh.py tests/memory/test_memo_memory_context_boundaries.py mechanics/consumer-handoff/parts/playbook-scope-handoff/tests/test_playbook_memory_scopes.py tests/root-topology/test_roadmap_parity.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/recurrence-support/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/recurrence-support/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/recurrence-support/parts/witness-trace-contract/tests/test_recurrence_support_mechanic.py tests/memory/test_memo_memory_context_boundaries.py mechanics/consumer-handoff/parts/playbook-scope-handoff/tests/test_playbook_memory_scopes.py tests/root-topology/test_roadmap_parity.py
```

<!-- Preserved on-demand procedure from `mechanics/recurrence-support/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/recurrence-support/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
```

<!-- Preserved on-demand procedure from `mechanics/recurrence-support/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/recurrence-support/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/retention/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/retention/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/memory/validate_memory_operations.py
python -m pytest -q mechanics/retention/parts/consolidation-and-forgetting/tests mechanics/retention/parts/cross-repo-and-governance-retention/tests mechanics/retention/parts/office-markers/tests mechanics/retention/parts/post-release-retention/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/retention/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/retention/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/retention/parts/cross-repo-and-governance-retention/tests mechanics/retention/parts/office-markers/tests mechanics/retention/parts/post-release-retention/tests
```

<!-- Preserved on-demand procedure from `mechanics/retention/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/retention/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/retention/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/retention/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/shape-guard/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/shape-guard/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/shape-guard/parts/via-negativa-checklist/tests/test_shape_guard_mechanic.py tests/mechanics/test_memo_mechanics.py tests/agents/test_agents_mesh.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/shape-guard/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/shape-guard/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/shape-guard/parts/via-negativa-checklist/tests/test_shape_guard_mechanic.py tests/mechanics/test_memo_mechanics.py
```

<!-- Preserved on-demand procedure from `mechanics/shape-guard/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/shape-guard/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/shape-guard/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/shape-guard/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/titan/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/titan/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/titan/parts/recall-and-remembrance-posture/tests mechanics/titan/parts/audit-personality-and-swarm-policy/tests
python -m pytest -q mechanics/titan/parts/recall-and-remembrance-posture/tests mechanics/titan/parts/closeout-and-digest-posture/tests mechanics/titan/parts/audit-personality-and-swarm-policy/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/titan/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/titan/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/titan/parts/recall-and-remembrance-posture/tests mechanics/titan/parts/closeout-and-digest-posture/tests mechanics/titan/parts/audit-personality-and-swarm-policy/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/titan/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/titan/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/titan/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/titan/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/writeback/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/writeback/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/memory/generate_memory_object_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_targets.py --check
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_intake.py --check
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py --check
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_growth_refinery_writeback_lanes.py --check
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_phase_alpha_writeback_map.py --check
python -m pytest -q mechanics/writeback/parts/runtime-and-temperature/tests mechanics/writeback/parts/quest-and-chronicle/tests mechanics/writeback/parts/revision-ledgers/tests mechanics/writeback/parts/rollback-and-recovery/tests mechanics/writeback/parts/growth-and-continuity/tests mechanics/writeback/parts/receipt-publication-regression/tests mechanics/consumer-handoff/parts/downstream-feed-regression/tests tests/mechanics/test_cross_mechanic_operational_contracts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/writeback/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/writeback/docs/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/writeback/legacy/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/writeback/legacy/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

<!-- Preserved on-demand procedure from `mechanics/writeback/parts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `mechanics/writeback/parts/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `memo/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `memo/AGENTS.md`

```text
memo/objects/<kind-dir>/<year>/<slug>/
  object.json
  MEMO.md
```
```bash
python scripts/memory/validate_memo_corpus.py
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/agents/validate_agents_mesh.py
python scripts/root-topology/validate_root_technical_districts_index.py
python -m pytest -q tests/memory/test_memo_corpus.py tests/memory/test_reviewed_intake_landing.py tests/agents/test_agents_mesh.py tests/root-topology/test_root_technical_districts_index.py
```

<!-- Preserved on-demand procedure from `quests/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `quests/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `schemas/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `schemas/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
python scripts/memory/validate_lifecycle_audit_examples.py
```
```bash
python scripts/memory/generate_memory_object_surfaces.py
```

<!-- Preserved on-demand procedure from `schemas/generated-surfaces/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `schemas/generated-surfaces/AGENTS.md`

```bash
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memory_object_surfaces.py
```

<!-- Preserved on-demand procedure from `schemas/memory-objects/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `schemas/memory-objects/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_object_surfaces.py
```

<!-- Preserved on-demand procedure from `schemas/recall-posture/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `schemas/recall-posture/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_operations.py
python scripts/memory/validate_memory_surfaces.py
```

<!-- Preserved on-demand procedure from `schemas/support-objects/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `schemas/support-objects/AGENTS.md`

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memo_corpus.py
```

<!-- Preserved on-demand procedure from `scripts/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `scripts/AGENTS.md`

```bash
python scripts/root-topology/validate_validator_topology.py
python scripts/ci_gate.py --mode source-fast
python scripts/ci_gate.py --mode generated
python scripts/ci_gate.py --mode memory
python scripts/ci_gate.py --mode tests
```
```bash
python -m pytest -q tests/root-topology/test_validation_lanes.py tests/root-topology/test_validator_topology.py tests/root-topology/test_ci_gate.py tests/root-topology/test_release_check.py
```
```bash
python scripts/memory/generate_memory_object_surfaces.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py
python mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_targets.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_intake.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_growth_refinery_writeback_lanes.py
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_phase_alpha_writeback_map.py
```

<!-- Preserved on-demand procedure from `scripts/agents/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `scripts/agents/AGENTS.md`

```bash
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python -m pytest -q tests/agents
```

<!-- Preserved on-demand procedure from `scripts/mechanics/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `scripts/mechanics/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/validate_memo_mechanic_parts.py
python -m pytest -q tests/mechanics
```

<!-- Preserved on-demand procedure from `scripts/memory/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `scripts/memory/AGENTS.md`

```bash
python scripts/memory/validate_memo.py --profile schema
python scripts/memory/validate_memo.py --profile memory-context
python scripts/memory/validate_memo.py --profile runtime-boundary
python scripts/memory/validate_memo.py --profile handoff-boundary
python scripts/memory/validate_memo.py --profile eval-boundary
python scripts/memory/validate_memo_corpus.py
python scripts/memory/validate_memory_operations.py
python scripts/memory/validate_local_memo_port.py --path examples/memory-ports/example-port
python -m pytest -q tests/memory
```

<!-- Preserved on-demand procedure from `scripts/memory/validators/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `scripts/memory/validators/AGENTS.md`

```bash
python scripts/memory/validate_memo.py --profile all
python scripts/root-topology/validate_validator_topology.py
python -m pytest -q tests/memory/test_memo_schema_contracts.py tests/memory/test_memo_runtime_writeback_boundaries.py tests/memory/test_memo_live_receipt_boundaries.py tests/root-topology/test_validator_topology.py
```

<!-- Preserved on-demand procedure from `scripts/release/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `scripts/release/AGENTS.md`

```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `scripts/root-topology/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `scripts/root-topology/AGENTS.md`

```bash
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
python -m pytest -q tests/root-topology
```

<!-- Preserved on-demand procedure from `stats/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `stats/AGENTS.md`

```bash
find memo/objects -name object.json -type f | sort
```
```bash
python scripts/release/validate_local_stats_port.py
```

<!-- Preserved on-demand procedure from `tests/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `tests/AGENTS.md`

```bash
python scripts/ci_gate.py --mode tests
```
```bash
python -m pytest -q tests/root-topology/test_test_topology.py tests/root-topology/test_validation_lanes.py tests/root-topology/test_validator_topology.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `tests/agents/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `tests/agents/AGENTS.md`

```bash
python -m pytest -q tests/agents
```

<!-- Preserved on-demand procedure from `tests/mechanics/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `tests/mechanics/AGENTS.md`

```bash
python -m pytest -q tests/mechanics
```

<!-- Preserved on-demand procedure from `tests/memory/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `tests/memory/AGENTS.md`

```bash
python -m pytest -q tests/memory
python -m pytest -q tests/memory/test_memo_schema_contracts.py tests/memory/test_memo_memory_context_boundaries.py
python -m pytest -q tests/memory/test_memo_runtime_writeback_boundaries.py tests/memory/test_memo_live_receipt_boundaries.py tests/memory/test_memo_handoff_boundaries.py tests/memory/test_memo_eval_guardrails.py
python -m pytest -q tests/memory/test_reviewed_intake_landing.py
python scripts/memory/validate_memo_corpus.py
python scripts/memory/validate_memory_operations.py
```

<!-- Preserved on-demand procedure from `tests/root-topology/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure

### Preserved route from `tests/root-topology/AGENTS.md`

```bash
python -m pytest -q tests/root-topology
```

## Preserved inline procedure from `AGENTS.md`

```text
Use `python scripts/release/release_check.py` for the frozen release gate.
```

## Preserved inline procedure from `evals/AGENTS.md`

```text
| validation | `python ../aoa-evals/scripts/validate_local_eval_port.py --target-root .` |
```

## Preserved inline procedure from `generated/AGENTS.md`

```text
- regenerate them with `python scripts/memory/build_memory_operational_readouts.py --write --live` in the workspace
- rebuild it with `python scripts/agents/build_agents_mesh_index.py`
- rebuild it with `python scripts/root-topology/build_root_technical_districts_index.py`
- rebuild with `python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py`
```

## Preserved inline procedure from `scripts/memory/AGENTS.md`

```text
- Landing usage: run `python scripts/memory/land_reviewed_memo_intake.py
```
