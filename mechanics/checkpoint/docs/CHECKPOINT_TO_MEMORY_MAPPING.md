# Checkpoint To Memory Mapping

Checkpoint-to-memory mapping explains how checkpoint artifacts become ordinary
memo objects without creating a checkpoint-only object family.

## Mapping Contract

The source contract is
`mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json` and
its schema is
`mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json`.

## Mapping Rules

- checkpoint export -> `state_capsule`
- approval record -> `decision`
- transition record -> `decision`
- execution trace -> `episode`
- review trace -> `audit_event`
- distillation claim candidate -> `claim`
- distillation pattern candidate -> `pattern`
- distillation bridge candidate -> `bridge`

Candidate mappings require review before writeback.

## Consumers

`mechanics/writeback/` consumes this contract to generate runtime writeback
companions. `mechanics/recurrence-support/` consumes checkpoint refs for
relaunch support. Neither consumer becomes the checkpoint owner.
