# Checkpoint Provenance

Checkpoint surfaces previously lived across root examples, recurrence-support,
and writeback. The split was workable while checkpoint was only a support
detail, but OS Abyss uses checkpoints as a repeatable memory operation.

## Active Placement

- `mechanics/checkpoint/docs/` owns checkpoint mechanic doctrine.
- `mechanics/checkpoint/parts/checkpoint-carry-contract/` owns
  `inquiry_checkpoint` schemas and examples.
- `mechanics/checkpoint/parts/checkpoint-to-memory-mapping/` owns the
  checkpoint-to-memory schema and example consumed by writeback.
- `mechanics/checkpoint/parts/approval-and-health-records/` owns approval,
  health, improvement, and checkpoint review memory-object examples.
- `mechanics/checkpoint/parts/checkpoint-memory-boundary/tests/` owns the
  package boundary regression.

## Former Placement

Former active paths now route here:

- `examples/checkpoint_approval_record.example.json`
- `examples/checkpoint_health_check.example.json`
- `examples/checkpoint_improvement_thread.example.json`
- `examples/decision.phase-alpha-self-agent-checkpoint.example.json`
- `examples/audit_event.phase-alpha-self-agent-checkpoint.example.json`
- `mechanics/recurrence-support/schemas/inquiry_checkpoint.schema.json`
- `mechanics/recurrence-support/examples/inquiry_checkpoint.example.json`
- `mechanics/recurrence-support/examples/inquiry_checkpoint.return.example.json`
- `mechanics/writeback/schemas/checkpoint-to-memory-contract.schema.json`
- `mechanics/writeback/examples/checkpoint_to_memory_contract.example.json`
- `mechanics/checkpoint/schemas/inquiry_checkpoint.schema.json`
- `mechanics/checkpoint/schemas/checkpoint-to-memory-contract.schema.json`
- `mechanics/checkpoint/examples/inquiry_checkpoint.example.json`
- `mechanics/checkpoint/examples/inquiry_checkpoint.return.example.json`
- `mechanics/checkpoint/examples/checkpoint_to_memory_contract.example.json`
- `mechanics/checkpoint/examples/checkpoint_approval_record.example.json`
- `mechanics/checkpoint/examples/checkpoint_health_check.example.json`
- `mechanics/checkpoint/examples/checkpoint_improvement_thread.example.json`
- `mechanics/checkpoint/examples/decision.phase-alpha-self-agent-checkpoint.example.json`
- `mechanics/checkpoint/examples/audit_event.phase-alpha-self-agent-checkpoint.example.json`
- `mechanics/checkpoint/tests/test_checkpoint_mechanic.py`

## Boundary Note

Recurrence-support still consumes checkpoint surfaces for route return.
Writeback still consumes checkpoint-to-memory mapping for runtime writeback
companions. Neither consumer owns the checkpoint artifact itself.
