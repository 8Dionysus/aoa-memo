# LIFECYCLE

## Purpose

This document defines how memory objects change over time in `aoa-memo`.

The memory layer should not mutate silently.
A reader should be able to tell whether a memory object is raw, proposed, confirmed, frozen, superseded, retracted, or simply left behind.

## Why lifecycle matters

A memory system without lifecycle posture becomes a fog of claims.

It becomes hard to tell:

- which objects are still provisional
- which objects were reviewed
- which objects were replaced
- which objects should no longer be used for current recall
- which history still matters even after replacement

Lifecycle gives memory temporal honesty.

## Default lifecycle states

Recommended default states are:

- `captured`
- `proposed`
- `confirmed`
- `frozen`
- `superseded`
- `retracted`
- `archived`

Not every object needs every state.
But state transitions should be explicit rather than inferred from vibes.

## State meanings

### `captured`

The object has been recorded, usually close to an event or observation.
It should be treated as raw memory, not settled meaning.

Typical examples:

- a fresh episode
- a first state capsule
- a just-recorded pattern candidate

### `proposed`

The object is formed enough to be reviewed or reused cautiously, but it has not yet been confirmed.

Typical examples:

- a claim inferred from one or more episodes
- a draft decision summary
- a pattern candidate waiting for more evidence

### `confirmed`

The object has passed a bounded review threshold for its scope.

Confirmed does not mean timeless or universal truth.
It means the object is currently acceptable memory-layer meaning for the scope it names.

### `frozen`

The object has been intentionally stabilized.

Frozen objects are usually:

- human-reviewed
- tied to a source-authoritative boundary
- used as stable anchors or durable doctrine references

Frozen still does not mean universal truth.
It means the layer intends stability unless a later change explicitly reopens or supersedes the object.

### `superseded`

The object has been replaced by a newer object for current use.

A superseded object remains important as history.
It should still be inspectable, and it should point to the object that replaced it.

### `retracted`

The object should no longer be used as an active memory surface.

Retraction is stronger than supersession.
Use it when the memory object is no longer trustworthy for active recall in its prior form.

The object remains in history, but it should clearly signal that it has been withdrawn.

### `archived`

The object remains stored as history and is not part of normal current recall.

Archiving may follow supersession, retraction, or simple historical cooling.

## Transition posture

Useful default transitions are:

- `captured -> proposed`
- `proposed -> confirmed`
- `confirmed -> frozen`
- `confirmed -> superseded`
- `confirmed -> retracted`
- `superseded -> archived`
- `retracted -> archived`

Some objects may move directly from `captured` to `confirmed` when the source authority is unusually strong.
That shortcut should be used carefully and explicitly.

## Supersession

Supersession means:

- the old object remains part of the historical trace
- a newer object is preferred for current recall
- the relation between old and new should be explicit

When supersession happens, the old object should usually record:

- `review_state: superseded`
- `superseded_by`
- optional `supersedes` history when relevant

And the newer object should usually record the older object in `supersedes`.

## Retraction

Retraction means the object should no longer be used as an active source of memory-layer meaning.

Use retraction when:

- the claim is no longer defensible even as scoped memory
- the memory object was malformed or misleading
- the memory trace was later found to be too weak for active use

Retraction should usually be accompanied by an `audit_event` and a provenance-thread timeline entry.

## Freeze posture

Freezing should be harder than confirmation.

A useful freeze rule is that at least one of these should hold:

- the object is tied to a stable doctrine or constitutional seam
- the object was reviewed by a human curator
- the object is anchored to a source-owned boundary that should not drift casually

The current public contract records this in `freeze_basis.qualifies_by`.

## Current recall posture

Lifecycle state alone is not always enough for downstream recall.

The current public contract therefore keeps `lifecycle.current_recall` explicit.

Use these statuses:

- `preferred` for the current best surface in ordinary recall for the scoped question
- `allowed` for a surface that may be returned normally but is not the main entrypoint
- `historical` for a surface kept visible mainly for trace-back and comparison
- `withdrawn` for a surface that should not be returned as normal current memory-layer meaning

This keeps "what happened to the object" separate from "how recall should treat it now".

## Contradiction visibility

Contradiction is not identical to supersession.

Use `lifecycle.current_recall.contradiction_refs` when a memory object should remain visibly in tension with another object instead of being flattened silently.

This helps consumers distinguish:

- a better replacement
- a withdrawn contradiction
- a still-open tension that should remain inspectable

## Audit events and lifecycle

Lifecycle should not rely on silent field edits alone.

Important lifecycle changes should also appear as `audit_event` objects.
That gives the memory layer a second face:

- the object's current state
- the audit trail that explains how it reached that state

## Anti-patterns

Treat these as warnings:

- changing `review_state` with no visible audit trail for important objects
- replacing a claim without `superseded_by`
- retracting an object without saying why or from which thread
- leaving current recall posture implicit when replacement or withdrawal already happened
- freezing objects too casually until frozen means almost nothing

## One-line doctrine

Lifecycle is how memory admits that time happened.
