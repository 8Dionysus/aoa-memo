# AUDIT EVENTS

## Purpose

This document defines `audit_event` objects in `aoa-memo`.

An audit event is a first-class memory object that records an important lifecycle or governance change.

The point is not bureaucracy.
The point is to keep memory-layer changes visible.

## Why audit events exist

If a claim changes state silently, later readers are forced to guess.

Audit events make it easier to answer:

- when did this change happen?
- what kind of change was it?
- which memory object did it affect?
- what thread or source context was involved?
- should current recall prefer a newer object, or stop using the old one entirely?

## What an audit event is for

Use `audit_event` when a memory-layer change is important enough that it should remain inspectable as its own object.

Good uses include:

- confirmation
- freeze
- supersession
- retraction
- archive transition
- access-class change
- provenance correction

## What an audit event is not

An audit event is not:

- a generic note
- a substitute for the object's own lifecycle field
- proof that the new state is universally correct
- a full incident report system

The object being changed still needs its own lifecycle fields.
The audit event is the visible trace of change.

## Relationship to lifecycle fields

A good memory-layer change has two faces:

1. the current state on the memory object
2. the audit event that explains a meaningful change in that state

This keeps current recall simple while preserving historical honesty.

## Suggested audit-event posture

An `audit_event` should usually include:

- `kind: audit_event`
- a summary of what changed
- provenance refs
- a review state, often `confirmed`
- bridges or route refs when the change affects current recall entrypoints

It may also mention the affected object in:

- `summary`
- `payload_ref`
- provenance-thread links
- surrounding provenance-thread timeline entries

## Supersession events

A supersession audit event says:

- an older object should no longer be the preferred current object
- a newer object now takes that role
- the older object remains part of history

A supersession event should be paired with:

- `review_state: superseded` on the older object
- `superseded_by` on the older object
- `supersedes` on the newer object when relevant

## Retraction events

A retraction audit event says:

- the object should no longer be used as an active memory surface in its prior form
- the object remains as historical trace, but active recall should not treat it as current memory-layer meaning

Retraction is stronger than supersession.

## Freeze events

A freeze audit event is useful when a surface becomes intentionally stable, especially at doctrine, constitutional, or source-boundary seams.

Freezing should be rare enough to mean something.

## Provenance correction events

Use this when the main change is not the claim content itself but the trace that supports it.

This helps keep provenance repairs visible instead of silently rewriting the chain.

## Anti-patterns

Treat these as warning signs:

- changing major lifecycle state with no audit event
- writing audit events for trivial noise
- using audit events as a shadow note system
- assuming the audit event replaces the object's own lifecycle fields

## One-line doctrine

An audit event is memory admitting that it changed, and leaving a footprint.
