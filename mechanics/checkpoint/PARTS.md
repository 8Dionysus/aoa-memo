# Checkpoint Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Checkpoint memory boundary | [CHECKPOINT_MEMORY_BOUNDARY](./docs/CHECKPOINT_MEMORY_BOUNDARY.md) | names what memo may preserve and what routes away |
| Checkpoint carry contract | [CHECKPOINT_CARRY_CONTRACT](./docs/CHECKPOINT_CARRY_CONTRACT.md) | keeps pause, return, and carry refs bounded and reviewable |
| Approval and health records | [CHECKPOINT_APPROVAL_HEALTH_MEMORY](./docs/CHECKPOINT_APPROVAL_HEALTH_MEMORY.md) | maps approval, health, improvement, and checkpoint review examples into existing memory objects |
| Checkpoint-to-memory mapping | [CHECKPOINT_TO_MEMORY_MAPPING](./docs/CHECKPOINT_TO_MEMORY_MAPPING.md) | maps checkpoint artifacts into existing object kinds without creating checkpoint-only memory |

## Part-Local Technical Contracts

Checkpoint schemas, examples, and regression tests live with the nearest
functioning part because those parts define the active checkpoint operation:

| Contract | Artifact Surface |
|---|---|
| Inquiry checkpoint | `mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json`, `mechanics/checkpoint/parts/checkpoint-carry-contract/examples/inquiry_checkpoint.example.json`, `mechanics/checkpoint/parts/checkpoint-carry-contract/examples/inquiry_checkpoint.return.example.json` |
| Checkpoint to memory contract | `mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json`, `mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json` |
| Approval and health examples | `mechanics/checkpoint/parts/approval-and-health-records/examples/checkpoint_approval_record.example.json`, `mechanics/checkpoint/parts/approval-and-health-records/examples/checkpoint_health_check.example.json` |
| Improvement thread | `mechanics/checkpoint/parts/approval-and-health-records/examples/checkpoint_improvement_thread.example.json` |
| Phase Alpha checkpoint examples | `mechanics/checkpoint/parts/approval-and-health-records/examples/decision.phase-alpha-self-agent-checkpoint.example.json`, `mechanics/checkpoint/parts/approval-and-health-records/examples/audit_event.phase-alpha-self-agent-checkpoint.example.json` |
| Boundary regression | `mechanics/checkpoint/parts/checkpoint-memory-boundary/tests/test_checkpoint_mechanic.py` |

## Interface

Inputs are checkpoint refs, approval records, health records, improvement
threads, return packs, reviewed closeout refs, runtime checkpoint refs, and
owner-local carry signals.

Outputs are bounded checkpoint memory surfaces, existing-object mappings,
provenance threads, and owner-routed next claims. Stronger owners decide
checkpoint execution, route return, role authority, scenario acceptance, proof,
and runtime state.
