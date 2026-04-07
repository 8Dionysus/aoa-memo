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

Do not create one for every failed run.

## What it should carry

A healthy failure lesson memory object includes:

- the owner repo and bounded surface
- the stressor family
- source receipt references
- optional adaptation references
- a concise lesson summary
- a recommended posture for later recall
- trust signals
- temperature and salience suitable for recall
- optional expiry or supersession

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
