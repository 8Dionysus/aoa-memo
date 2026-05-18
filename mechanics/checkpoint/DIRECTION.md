# Checkpoint Direction

Checkpoint memory is the bounded pause, review, and carry surface for OS
Abyss. It should make checkpoint artifacts recallable without letting memory
pretend that a checkpoint executed, passed proof, or granted authority.

## Current Direction

- Keep checkpoint artifacts under `mechanics/checkpoint/` when they are
  checkpoint-specific rather than shared public memory canon.
- Keep `inquiry_checkpoint` as a support artifact, not a new memory-object
  family.
- Keep checkpoint-to-memory mapping explicit: checkpoint exports map into
  existing memory objects, then stronger owners decide execution, proof,
  routing, and acceptance.
- Keep recurrence-support as the route-return consumer and writeback as the
  generic writeback consumer.

## Stop Lines

- No runtime checkpoint store in `aoa-memo`.
- No hidden checkpoint worker or retry loop.
- No checkpoint authority for agents, routes, playbooks, or source owners.
- No checkpoint proof verdict.
- No `checkpoint_memory` object family.
