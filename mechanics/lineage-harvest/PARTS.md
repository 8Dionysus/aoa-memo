# Lineage Harvest Parts

## Active docs

| Surface | Role |
|---|---|
| [PATTERN_LINEAGE_MEMORY](../../mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md) | active source doc for pattern-lineage memory flow, gates, inputs, outputs, and invariants |

## Root technical contracts

These artifacts remain in root technical districts because they are public
support contracts and release-gate companions, not private package-local lore.

| Artifact | Role |
|---|---|
| `schemas/pattern_lineage_memory_entry_v1.json` | public schema for pattern-lineage memory entry examples |
| `examples/pattern_lineage_memory_entry.example.json` | public-safe example for the pattern-lineage memory entry contract |
| `examples/federation_memory_gate_decision.example.json` | adjacent governance gate example that names `pattern_lineage_memory` as a memory kind |
| `tests/test_experience_wave3_seed_contracts.py` | validates the federation-harvest seed schemas and examples as public contracts |
| `tests/test_lineage_harvest_mechanic.py` | protects the package boundary, active path, root technical artifact placement, and stronger-owner stop-lines |

## Adjacent mechanic interfaces

| Neighbor mechanic | Interface |
|---|---|
| [governance](../governance/README.md) | owns authority-boundary memory for federation decisions and forgetting law |
| [writeback](../writeback/README.md) | owns harvest-to-memory return lanes and runtime-to-memo writeback posture |
| [retention](../retention/README.md) | owns retention evidence and cross-repo retention outcomes |
| [adoption](../adoption/README.md) | owns owner-local adoption memory after federation harvest approval |
| [consumer-handoff](../consumer-handoff/README.md) | owns KAG, ToS, eval, playbook, agent, and orchestrator handoff surfaces |
| [operational-gate](../operational-gate/README.md) | owns operational incident admission into durable memo |
| [recurrence-support](../recurrence-support/README.md) | owns route-return anchors, witness trace exports, and reviewed closeout recall landings |

## Generated companions

- `generated/memo_mechanics.min.json` indexes this package from
  `config/memo_mechanics.json`.
- `generated/agents_mesh.min.json` indexes this package's route cards from
  `config/agents_mesh.json`.
- `generated/memo_registry.min.json` routes core docs to the active
  `mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md` path.
- `generated/memory_catalog*.json`, `generated/memory_capsules.json`, and
  `generated/memory_sections.full.json` expose the `AOA-M-0015` inspect,
  capsule, and expand surfaces for this mechanic.

Generated companions are mirrors. They do not author lineage-harvest truth.
