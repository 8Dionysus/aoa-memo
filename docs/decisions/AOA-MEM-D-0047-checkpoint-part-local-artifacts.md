# Checkpoint Part-Local Artifacts

- Decision ID: AOA-MEM-D-0047

## Status

Accepted on 2026-05-19.

## Index Metadata

- Original date: 2026-05-19
- Surface classes: mechanic package, mechanic part
- Mechanic parents: checkpoint
- Guard families: mechanic topology, part and payload
- Memory object classes: none
- Posture: active rationale

## Context

Checkpoint already had functioning `parts/` nodes, but its technical contract
was still parked at the package level. The inquiry checkpoint schema and
examples, checkpoint-to-memory schema and example, approval/health/improvement
examples, Phase Alpha checkpoint examples, and checkpoint regression test lived
under `mechanics/checkpoint/{schemas,examples,tests}`.

That kept checkpoint usable but not cleanly shaped for OS Abyss. The carry
packet, writeback mapping, approval/health record preservation, and package
boundary regression are different operations with different consumer routes.
Keeping them in one package bucket made the parts descriptive instead of fully
functional.

## Decision

Move checkpoint technical artifacts to the nearest functioning part:

- `inquiry_checkpoint` schema and examples under
  `mechanics/checkpoint/parts/checkpoint-carry-contract/`
- checkpoint-to-memory schema and example under
  `mechanics/checkpoint/parts/checkpoint-to-memory-mapping/`
- approval, health, improvement-thread, and checkpoint review examples under
  `mechanics/checkpoint/parts/approval-and-health-records/`
- the package boundary regression under
  `mechanics/checkpoint/parts/checkpoint-memory-boundary/tests/`

Keep recurrence-support and writeback as consumers of checkpoint artifacts, not
owners. Their refs point to the part-local surfaces, while checkpoint remains
the source owner for the checkpoint artifact and mapping.

## Consequences

- The checkpoint artifact inventory now reports checkpoint artifacts as
  `scope: part`, not package-owned.
- Writeback runtime target and intake generation read the part-local
  checkpoint-to-memory contract.
- Recurrence-support and consumer-handoff tests assert the new part-local
  checkpoint paths.
- The old package-level `mechanics/checkpoint/schemas`,
  `mechanics/checkpoint/examples`, and `mechanics/checkpoint/tests` paths are
  provenance only, not active homes.
- `aoa-memo` still does not execute checkpoints, own runtime state, grant role
  rights, dispatch return routes, prove checkpoint success, choreograph
  playbooks, or accept source-owner outcomes.

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
