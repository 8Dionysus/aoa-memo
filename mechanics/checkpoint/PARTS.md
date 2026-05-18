# Checkpoint Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Checkpoint memory boundary | [CHECKPOINT_MEMORY_BOUNDARY](./docs/CHECKPOINT_MEMORY_BOUNDARY.md) | names what memo may preserve and what routes away |
| Checkpoint carry contract | [CHECKPOINT_CARRY_CONTRACT](./docs/CHECKPOINT_CARRY_CONTRACT.md) | keeps pause, return, and carry refs bounded and reviewable |
| Approval and health records | [CHECKPOINT_APPROVAL_HEALTH_MEMORY](./docs/CHECKPOINT_APPROVAL_HEALTH_MEMORY.md) | maps approval and health examples into existing memory objects |
| Checkpoint-to-memory mapping | [CHECKPOINT_TO_MEMORY_MAPPING](./docs/CHECKPOINT_TO_MEMORY_MAPPING.md) | maps checkpoint artifacts into existing object kinds without creating checkpoint-only memory |

## Mechanic-Local Technical Contracts

The checkpoint schemas and examples live with the package because they define
the checkpoint mechanic:

| Contract | Artifact Surface |
|---|---|
| Inquiry checkpoint | `mechanics/checkpoint/schemas/inquiry_checkpoint.schema.json`, `mechanics/checkpoint/examples/inquiry_checkpoint.example.json`, `mechanics/checkpoint/examples/inquiry_checkpoint.return.example.json` |
| Checkpoint to memory contract | `mechanics/checkpoint/schemas/checkpoint-to-memory-contract.schema.json`, `mechanics/checkpoint/examples/checkpoint_to_memory_contract.example.json` |
| Approval and health examples | `mechanics/checkpoint/examples/checkpoint_approval_record.example.json`, `mechanics/checkpoint/examples/checkpoint_health_check.example.json` |
| Improvement thread | `mechanics/checkpoint/examples/checkpoint_improvement_thread.example.json` |
| Phase Alpha checkpoint examples | `mechanics/checkpoint/examples/decision.phase-alpha-self-agent-checkpoint.example.json`, `mechanics/checkpoint/examples/audit_event.phase-alpha-self-agent-checkpoint.example.json` |

## Interface

Inputs are checkpoint refs, approval records, health records, improvement
threads, return packs, reviewed closeout refs, runtime checkpoint refs, and
owner-local carry signals.

Outputs are bounded checkpoint memory surfaces, existing-object mappings,
provenance threads, and owner-routed next claims. Stronger owners decide
checkpoint execution, route return, role authority, scenario acceptance, proof,
and runtime state.
