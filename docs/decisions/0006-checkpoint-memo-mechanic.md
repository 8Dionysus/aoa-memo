# 2026-05-18 Checkpoint Memo Mechanic

- Decision ID: AOA-MEM-D-0006

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-checkpoint-memo-mechanic.md
- Surface classes: mechanic package
- Mechanic parents: checkpoint
- Guard families: mechanic topology
- Memory object classes: none
- Posture: active rationale

## Context

Checkpoint surfaces were present in `aoa-memo`, but their ownership was split
across root examples, recurrence-support, and writeback.

That split hid the operation:

- recurrence-support consumed checkpoint continuity for route return
- writeback consumed checkpoint-to-memory mapping for runtime writeback
- root examples preserved checkpoint approval, health, and improvement traces

As OS Abyss begins using `aoa-memo` actively, checkpoint memory is not just a
topic. It is a repeatable memory-layer operation with inputs, outputs, owner
split, stop-lines, validation, and consumers.

## Decision

Create `mechanics/checkpoint/` as the owner of memo-side checkpoint memory.

The checkpoint mechanic owns checkpoint-specific docs, schemas, examples, and
tests, including:

- `inquiry_checkpoint`
- `checkpoint_to_memory_contract`
- checkpoint approval and health examples
- checkpoint improvement provenance
- phase-alpha self-agent checkpoint examples

Recurrence-support remains the route-return support mechanic that consumes
checkpoint refs. Writeback remains the generic writeback mechanic that consumes
checkpoint-to-memory mapping for generated runtime writeback companions.

## Alternatives Considered

- Keep checkpoint under recurrence-support. Rejected because recurrence-support
  owns relaunch support, not the checkpoint artifact and mapping operation.
- Keep checkpoint-to-memory under writeback. Rejected because the contract is
  checkpoint-specific; writeback is a consumer of the mapping.
- Leave root examples as shared canon. Rejected because these examples are
  checkpoint-owned artifacts, not general memory-object canon.

## Consequences

- The mechanics map gains a checkpoint package and generated index coverage.
- Root technical districts lose checkpoint-owned examples and schemas.
- Recurrence-support and writeback now name checkpoint as an owner rather than
  silently owning checkpoint artifacts.
- Validators and tests must keep checkpoint artifacts in the checkpoint package
  while allowing recurrence-support/writeback consumer refs.

## Boundaries

`aoa-memo` still does not own checkpoint execution, runtime stores, actor
rights, route dispatch, playbook acceptance, proof, or source-owner acceptance.

Checkpoint artifacts map into existing memory object kinds. This decision does
not create `checkpoint_memory`.
