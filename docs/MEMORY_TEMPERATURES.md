# MEMORY TEMPERATURES

## Purpose

This document makes the temperature axis in `aoa-memo` more operational.

The goal is not to replace the broader memory model.
The goal is to say:

- what each public temperature means in practice
- how memory moves between temperatures
- what should decay, demote, freeze, or retire
- how a constitutional `core` band fits without breaking the existing public scale

## Core rule

The public temperature scale remains:

- `hot`
- `warm`
- `cool`
- `cold`
- `frozen`

This document adds one important overlay:

- `core` is a constitutional or retention **band**, not a replacement temperature

`core` marks memory that must stay available as a stable operating axis.
It does not replace the temperature field in `memory_object.schema.json`.

## Why this split exists

AoA needs two different questions to stay separate:

1. how active is this memory right now?
2. does this memory belong to the constitutional core?

If those questions are collapsed, the layer becomes confusing.
A highly active item is not automatically constitutional.
A constitutional item is not automatically `hot`.

## The public temperatures

### `hot`

Use for:

- current task state
- active constraints
- near-term open loops
- session-adjacent decisions not yet consolidated

Default posture:

- cheap to read
- cheap to write
- expected to change quickly
- expected to demote unless it stays salient

### `warm`

Use for:

- active project memory
- repeated decisions
- recurring errors or patterns
- current multi-session context that still moves

Default posture:

- often recalled by default for related work
- stable enough for reuse
- still reviewable and promotable

### `cool`

Use for:

- consolidated cross-session memory
- stable summaries of episodes and decisions
- patterns that survived more than one local cycle

Default posture:

- summary-first retrieval
- explicit promotion or demotion gates
- not automatically loaded on every task

### `cold`

Use for:

- durable but rarely needed memory
- reviewable historical context
- long-tail provenance or decision history

Default posture:

- explicit retrieval or audit access
- low default recall pressure
- retirement remains possible

### `frozen`

Use for:

- intentionally stabilized reference memory
- human-reviewed anchors
- source-backed reference objects with low expected churn

Default posture:

- read-mostly
- strong review requirement before change
- should behave like a stable reference, not a live scratchpad

## The `core` overlay

`core` marks memory that the system should preserve as a stable operating axis.

Typical `core` candidates:

- constitutional constraints
- project identity
- role law
- stable safety or approval boundaries
- writeback rules that must not disappear between sessions

Typical non-`core` items:

- one-off session notes
- narrow task tactics
- unstable hypotheses
- unresolved contradictions

`core` is best represented through:

- `retention_class`
- `access.read_scopes`
- explicit write and promotion rights
- stable references such as `anchor` and `decision`

## Salience gate

Temperature should not move by similarity alone.

Promotion and demotion should consider:

- `novelty`
- `impact`
- `recurrence`
- `risk`

These are salience components, not truth scores.

They help answer:

- should this item stay active?
- should it consolidate?
- should it be demoted?
- should it be rescued from retirement?

## Promotion and demotion posture

Preferred movement shape:

- `hot -> warm` when a task-local item survives one session and still matters
- `warm -> cool` when the item becomes reusable across runs
- `cool -> cold` when the item remains valuable but low-pressure
- `cold -> frozen` only after explicit stabilization or human review

Possible reverse movements:

- `cold -> cool` when a long-tail memory becomes active again
- `cool -> warm` when a stable summary becomes operational again

Do not assume monotonic promotion.
Reactivation and demotion are normal.

## Decay and retirement posture

Memory should be able to age out honestly.

Useful decay controls include:

- `review_after`
- `ttl_days`
- `half_life_days`
- `demotion_target`
- `retire_after`
- `manual_veto`

Retirement is not deletion.
It is the decision that the memory should stop competing for ordinary recall.

## Boundaries to preserve

- temperature is not truth
- `core` is not a new temperature enum
- `frozen` is not a synonym for source-of-truth in every case
- memory decay is not permission to erase provenance
- writeback rules remain separate from ToS canon law

## Practical use

When a new memory object is created, ask:

1. what temperature should it start at?
2. is it `core` or merely active?
3. who may read it by default?
4. who may promote, demote, freeze, or retire it?
5. what review or decay signal moves it next?
