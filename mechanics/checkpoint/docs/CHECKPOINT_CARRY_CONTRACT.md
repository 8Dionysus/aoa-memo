# Checkpoint Carry Contract

Checkpoint carry lets a long-horizon route pause without losing the bounded
facts needed for later review.

The carry surface is a memory aid. It is not runtime state and not permission
to resume.

## Carry Inputs

- `inquiry_checkpoint` exports
- return packs
- memory delta refs
- canon delta refs
- source refs
- reviewed closeout refs
- owner-local handoff refs
- runtime checkpoint refs by reference only

## Carry Outputs

- a bounded `state_capsule`, `decision`, `episode`, `audit_event`, or
  `provenance_thread` candidate
- explicit reentry refs for later recall
- owner-routed next claims
- review state and current recall posture

## Return Boundary

`mechanics/recurrence-support/` uses checkpoint carry for route return, but it
does not own the checkpoint artifact. `mechanics/checkpoint/` owns the
checkpoint artifact and mapping; recurrence-support owns the relaunch support
operation that consumes it.

## Runtime Boundary

Runtime checkpoint state belongs in `abyss-stack`. Memo may cite runtime
checkpoint refs, but it must not copy live scratchpad state or pretend a worker
exists here.
