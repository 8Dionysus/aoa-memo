# Lineage Harvest Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Pattern-lineage memory gate | [PATTERN_LINEAGE_MEMORY](./docs/PATTERN_LINEAGE_MEMORY.md) | gates cross-repo recurring signals into reviewed pattern-lineage memory candidates without federation authority |
| Adjacent mechanic interfaces | [governance](../governance/README.md), [writeback](../writeback/README.md), [retention](../retention/README.md), [adoption](../adoption/README.md), [consumer-handoff](../consumer-handoff/README.md), [operational-gate](../operational-gate/README.md), [recurrence-support](../recurrence-support/README.md) | routes stronger adjacent memory operations without absorbing their authority |
| Lineage inspection projections | `generated/memo_mechanics.min.json`, `generated/agents_mesh.min.json`, `generated/memo_registry.min.json`, `generated/memory_catalog*.json`, `generated/memory_capsules.json`, `generated/memory_sections.full.json` | exposes compact mirrors while keeping lineage-harvest source truth in package docs and artifacts |

## Part-Local Artifacts

These artifacts live with the pattern-lineage-memory-gate part because they
define that public support contract and regression boundary.

| Artifact | Role |
|---|---|
| `mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/schemas/pattern_lineage_memory_entry_v1.json` | public schema for pattern-lineage memory entry examples |
| `mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/examples/pattern_lineage_memory_entry.example.json` | public-safe example for the pattern-lineage memory entry contract |
| `mechanics/governance/parts/federation-boundary/examples/federation_memory_gate_decision.example.json` | adjacent governance gate example that names `pattern_lineage_memory` as a memory kind |
| `tests/test_experience_wave3_seed_contracts.py` | validates the federation-harvest seed schemas and examples as public contracts |
| `mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/tests/test_lineage_harvest_mechanic.py` | protects the package boundary, active path, mechanic-local artifact placement, and stronger-owner stop-lines |

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

## Lineage inspection projections

- `generated/memo_mechanics.min.json` indexes this package from
  `config/memo_mechanics.json`.
- `generated/agents_mesh.min.json` indexes this package's route cards from
  `config/agents_mesh.json`.
- `generated/memo_registry.min.json` routes core docs to the active
  `mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md` path.
- `generated/memory_catalog*.json`, `generated/memory_capsules.json`, and
  `generated/memory_sections.full.json` expose the `AOA-M-0015` inspect,
  capsule, and expand surfaces for this mechanic.

Lineage inspection projections are mirrors. They do not author lineage-harvest truth.

## Interface

Inputs are cross-repo recurring owner-local signals, federation-harvest gates,
reviewed source refs, and adjacent mechanic signals that may justify a
pattern-lineage memory candidate.

Outputs are bounded lineage candidate memory, schema-backed examples,
provenance-aware review posture, and stronger-owner next routes. This mechanic
does not approve federation, promote KAG, write ToS canon, certify stats,
execute runtime watches, or adopt source-owner truth.
