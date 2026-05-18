# Checkpoint Provenance

Checkpoint surfaces previously lived across root examples, recurrence-support,
and writeback. The split was workable while checkpoint was only a support
detail, but OS Abyss uses checkpoints as a repeatable memory operation.

## Active Placement

- `mechanics/checkpoint/docs/` owns checkpoint mechanic doctrine.
- `mechanics/checkpoint/schemas/` owns checkpoint-specific support schemas.
- `mechanics/checkpoint/examples/` owns checkpoint-specific examples.
- `mechanics/checkpoint/tests/` owns checkpoint mechanic regression tests.

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

## Boundary Note

Recurrence-support still consumes checkpoint surfaces for route return.
Writeback still consumes checkpoint-to-memory mapping for runtime writeback
companions. Neither consumer owns the checkpoint artifact itself.
