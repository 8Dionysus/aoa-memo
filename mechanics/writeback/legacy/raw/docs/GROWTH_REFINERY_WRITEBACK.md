# GROWTH REFINERY WRITEBACK

## Purpose

Growth refinery may write back to `aoa-memo` only when durable memory will help
future reviewed handling of a similar owner-fit or repair situation.

This surface is memo-side support.
It does not become lineage truth, proof doctrine, or owner authority.
It is also the bounded home for prune-aware writeback when drop, supersession,
merge, or seed-no-value outcomes repeat often enough to deserve memory.

## Reuse Existing Memo Kinds

Do not introduce a growth-refinery-only memory family.

Use existing memo kinds instead:

- `failure_lesson_memory_v1` when the main value is a cautionary memory
- `recovery_pattern_memory_v1` when the main value is a reusable bounded
  repair or reanchor pattern

Prune-aware mapping stays inside those existing kinds:

- repeated drop, wrong-owner, or weak-owner supersession belongs in
  `failure_lesson_memory_v1` when the main value is caution
- repeated reanchor, merge, or proof-first rescue belongs in
  `recovery_pattern_memory_v1` when the main value is a bounded reusable move

## Write Back Failure Lessons When

- a candidate repeatedly lands in the wrong owner
- a candidate or staged seed repeatedly drops for the same bounded reason
- supersession or merge repeatedly happens because the first owner-fit guess
  was too weak or duplicated a stronger owner surface
- seed staging repeatedly adds no value compared with direct owner landing
- a repair widened scope or violated boundaries
- the same handoff failed more than once

## Write Back Recovery Patterns When

- the same reanchor move fixes owner fit more than once
- the same merge pattern preserves truth while reducing duplicate owner surfaces
- the same proof-first rule prevents repeated thin-evidence landings
- a thin-evidence object became stable through repeated review or proof
- a bounded repair move worked more than once without widening authority

## Strongest Available Lineage Refs

When reviewed lineage evidence exists, preserve the strongest available chain in
`lineage_refs`:

- `cluster_ref`
- `candidate_ref`
- `seed_ref`
- `object_ref`

Earlier refs may remain populated even when later refs are still `null`.
Memo should stay honest about which parts of the chain are not landed yet.

## Optional Lineage Context

When bounded owner-fit context will help later recall, preserve it under
`lineage_context`:

- `owner_hypothesis`
- `owner_shape`
- `nearest_wrong_target`
- `status_posture`
- `supersedes`
- `merged_into`
- `drop_reason`

This context helps memory explain why a lesson mattered.
It does not override owner-local receipts, seed truth, landed object truth, or
proof.

## Negative Rules

Do not use memo writeback here to:

- mint `candidate_ref`, `seed_ref`, or `object_ref`
- replace owner-local receipts or proof bundles
- invent a new recurring-runner authority inside `aoa-memo`
- treat memory as the canonical home of growth-refinery state
- let prune writeback become the first record of drop, merge, or supersession truth
- let memory decide whether a candidate should be dropped, merged, or superseded

## Do Not Recall From Memo Alone

Do not use lineage-aware memo recall as first authority when the linked
owner receipt, seed lineage entry, eval report, or stats summary is available
to inspect directly.

If the surviving chain is still `early` or `thin-evidence`, memo may preserve
bounded context, but landing, repair, and promotion decisions still belong to
the stronger owner and proof surfaces.

## Canonical Neighbors

- `docs/RUNTIME_WRITEBACK_SEAM.md` owns the runtime-to-memo boundary
- `docs/FAILURE_LESSON_MEMORY.md` owns failure-lesson doctrine
- `docs/RECOVERY_PATTERN_MEMORY.md` owns recovery-pattern doctrine
