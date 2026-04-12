# FAILURE LESSON MEMORY

## Purpose

Wave 2 adds one bounded memory object family for reviewed failure lessons.

This object family exists so the system can remember:

- a stress pattern that has happened before
- what posture helped
- what should be avoided next time

It does **not** replace source-owned receipts or bounded eval proof.

## When to create one

A `failure_lesson_memory_v1` object is appropriate when at least one of the following is true:

- a stressor family repeats
- a single event is severe enough to deserve recall
- a reviewed adaptation cites the event and changes future handling
- operators repeatedly need the same cautionary context
- a checked-in rollout or drift window keeps teaching the same bounded caution

Do not create one for every failed run.

## What it should carry

A healthy failure lesson memory object includes:

- the owner repo and bounded surface
- the stressor family
- source receipt references
- checked-in rollout, drift, or rollback refs when rollout history is the source
- optional adaptation references
- strongest available lineage refs when reviewed owner-chain evidence exists
- a concise lesson summary
- a recommended posture for later recall
- trust signals
- temperature and salience suitable for recall
- optional expiry or supersession

When lineage-aware writeback is warranted, keep `lineage_refs` scoped to the
strongest reviewed chain available at the time of writeback:

- `cluster_ref`
- `candidate_ref`
- `seed_ref`
- `object_ref`

Optional `lineage_context` may preserve bounded owner-fit clues such as
`owner_hypothesis`, `owner_shape`, `nearest_wrong_target`, `status_posture`,
`supersedes`, `merged_into`, and `drop_reason`.
That context is memory support only. It does not become final lineage truth.

## Review posture

Preferred review states:

- `draft`
- `reviewed`
- `superseded`

Prefer `reviewed` before the object becomes a strong recall candidate.

## Boundary reminder

Failure lesson memory is useful because it is portable context.
It remains memory, not proof.

The object may help answer:

- have we seen this pattern before
- what posture helped
- what should we inspect first

The object should not claim:

- that the current run definitely matches past runs
- that the owner repo is healthy now
- that a mutation is safe by itself

For the narrower shared-root campaign-cadence seam, use
`docs/DRIFT_REVIEW_LESSON_MEMORY.md` plus
`examples/failure_lesson_memory.drift_review.example.json`.
