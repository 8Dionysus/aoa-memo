# PROVENANCE THREADS

## Purpose

This document defines how provenance threads work in `aoa-memo`.

A provenance thread is the smallest explicit structure that ties memory objects, source references, and time-ordered changes into one reviewable chain.

The point is simple: memory should not float free.

## What a provenance thread is

A provenance thread is a bounded trace that links:

- source references
- memory objects created from those sources
- lifecycle events that changed the status of those objects
- time-ordered notes about how the memory changed

A provenance thread is not a universal graph.
It is a reviewable local chain.

## Why provenance threads exist

Without provenance threads, memory objects are easy to read but hard to trust.

The thread gives a reader a way to answer:

- where did this object come from?
- which other memory objects were part of the same trace?
- what changed over time?
- when did a claim become confirmed, frozen, superseded, or retracted?
- which object still carries the preferred current recall posture when a contradiction or replacement exists?
- which stronger source should be opened next?

## Core rules

1. **A provenance thread should stay local and reviewable.** It is a chain, not a hidden graph platform.
2. **Source refs come first.** The thread should point back to source-owned surfaces whenever possible.
3. **Lifecycle events belong in the thread.** Confirmation, supersession, freeze, and retraction should be visible in time order.
4. **The thread should survive claim changes.** When a claim is superseded or retracted, the thread remains as history.
5. **Current recall posture should stay walkable.** If one object remains preferred and another becomes historical or withdrawn, the thread should make that shift inspectable.
6. **The thread should not pretend to prove correctness.** Provenance helps readers inspect the trace. It does not turn memory into proof.

## What a thread should link

A useful provenance thread may link any mix of:

- `episode` objects
- `claim` objects
- `decision` objects
- `pattern` objects
- `bridge` objects
- `audit_event` objects
- source refs pointing to docs, generated surfaces, or neighboring repos

The thread does not need to include every object in the ecosystem.
It only needs to include the chain that matters for a bounded memory question.

## Recommended thread anatomy

A provenance thread should usually include:

- `id`
- `title`
- `summary`
- `status`
- `source_refs`
- `memory_object_ids`
- `timeline`

The `timeline` should be the most human-legible part of the thread.
Each event should say:

- when it happened
- what action occurred
- which actor or surface was involved when known
- which memory object changed when relevant

If the thread includes a contradiction set or a current-entrypoint shift, the timeline should make that change inspectable.

## Relationship to memory objects

### Episodes

Episodes usually begin a thread because they preserve that something happened.

### Claims

Claims often sit in the middle of a thread.
They should stay connected to the episodes and sources that justify their existence.

### Audit events

Audit events make the thread honest over time.
They show when a claim was confirmed, frozen, superseded, or retracted.

### Bridges

Bridges may sit inside a provenance thread when the memory trace needs to point toward ToS, KAG, or another source-owned seam.

## Relationship to KAG and ToS

A provenance thread may point outward to ToS fragments, concepts, lineages, or KAG-ready objects.

But the provenance thread itself remains a memory-layer trace.
It should not become the normalized graph substrate.

That downstream work still belongs in `aoa-kag` and related systems.

At the current public baseline, `provenance_thread` remains a schema-backed support surface.
It does not become its own generated family in the doctrine-versus-object surface split.

## Improvement logs and checkpoint routes

A provenance thread is also the right current home for a bounded self-agent improvement log.

In that route, the thread can tie together:

- the approval record as a `decision`
- the rollback marker as a referenced artifact
- the post-change health result as an `episode` or `audit_event`
- the time-ordered improvement notes that tell the next reviewer what changed and why

That keeps the improvement log as a backward-walk chain instead of turning it into a new hidden memory subsystem.

## Thread status

Recommended statuses are:

- `active`
- `frozen`
- `archived`

`active` means the thread may still receive lifecycle additions.
`frozen` means the thread is intentionally stabilized.
`archived` means it remains as history and is not expected to change.

## Anti-patterns

Treat these as warning signs:

- a provenance thread that hides its source refs
- a provenance thread that tries to encode all relations in the repo
- a provenance thread used as a substitute for current truth
- a provenance thread that omits lifecycle changes after supersession or retraction

## One-line doctrine

A provenance thread is the memory-layer chain that lets a reader walk backward without guessing.
