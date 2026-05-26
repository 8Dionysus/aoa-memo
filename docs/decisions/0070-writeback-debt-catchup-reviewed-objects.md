# Decision: Writeback debt catchup lands reviewed objects

- Decision ID: AOA-MEM-D-0070

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-25
- Surface classes: reviewed corpus, local port/writeback, mechanic package
- Mechanic parents: writeback
- Guard families: reviewed corpus/intake, local port/writeback
- Memory object classes: local_candidate
- Posture: active rationale

## Context

The workspace writeback debt readout showed `aoa-memo` had landed work after
the last explicit writeback marker. The relevant landed work was not generic
progress: it added the distributed memory-organ foundation and the operational
readout family for access-plane currentness, source-intake wave coverage, and
workspace memo-port status.

Because `aoa-memo` owns the reviewed memory corpus, the right catchup path is
not a local `repo/memo/` candidate. The source decisions are already accepted
in this repository, and the durable memory layer should remember them as
reviewed corpus objects.

## Decision

Add reviewed decision objects for:

- `memo.decision.2026-05-25.distributed-memory-organ-foundation`
- `memo.decision.2026-05-25.memory-operational-readouts`

This decision record is the explicit writeback marker for the catchup. The
objects are the durable reviewed memory. The generated memory-object read
models remain derived companions.

## Consequences

- The reviewed corpus gains real post-May-22 decision memory for the memory
  organ foundation and operational readout slices.
- The catchup avoids creating fake local-port packets inside `aoa-memo`.
- Future agents can recall these decisions from object read models instead of
  replaying only PR summaries or session context.
- The writeback debt readout can treat this file as the current route-only
  marker while `aoa-memo` continues to own durable memory through
  `memo/objects/`.

## Verification

Use:

```bash
python scripts/memory/validate_memo_corpus.py
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memory_object_surfaces.py
python scripts/release/release_check.py
```
