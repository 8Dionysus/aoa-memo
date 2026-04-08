# RECOVERY PATTERN MEMORY

## Purpose

Wave 4 adds one bounded memory adjunct for reviewed recovery patterns that
survived an ordered stress window.

This adjunct exists so the system can remember:

- which stressor family repeated
- what bounded recovery posture held across the window
- which route or recall cues remained safe to surface afterward

It does **not** replace source-owned receipts, bounded eval proof, or derived
stats summaries.

## When to create one

A `recovery_pattern_memory_v1` object is appropriate when at least one of the
following is true:

- an ordered stress window has more than one reviewed event
- a bounded longitudinal eval confirms the recovery claim
- derived stats still expose explicit evidence or suppression posture
- routing and operator review benefit from one reusable bounded recall object

Do not create one from a single anecdote, from stats-only inference, or from a
route hint without stronger upstream evidence.

## What it should carry

A healthy recovery pattern memory object includes:

- the stressor family and ordered window scope
- source receipt references
- linked eval report references
- linked stats summary references
- optional route hint references
- one concise recovery summary
- one explicit recall posture
- trust signals
- a native pattern-object reference when the lesson is promoted into the memo
  object family

## Review posture

Preferred review states:

- `draft`
- `reviewed`
- `superseded`

Prefer `reviewed` before the object becomes a durable recall aid or a routing
adjunct.

## Boundary reminder

Recovery pattern memory is useful because it preserves reviewed repeated-window
context.
It remains memory, not proof.

The object may help answer:

- have we seen bounded recovery across this stressor family before
- which stronger sources should be inspected first
- which posture helped the system recover without widening scope

The object should not claim:

- that the current run is healthy by itself
- that memo now owns route or eval authority
- that a recovery route is safe without checking linked receipts and proof
