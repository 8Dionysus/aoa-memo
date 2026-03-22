# Narrative Core Contract

This document records the first-wave contract between authored/core memory and derived memory surfaces.

It exists to keep `aoa-memo` explicit, reviewable, and source-disciplined while still allowing downstream retrieval and KAG work.

## Core rule

Write the memory event once.
Derive downstream surfaces later.

`aoa-memo` owns explicit, reviewable memory surfaces.
It does not become a hidden graph platform, embedding empire, or substitute for Tree of Sophia.

## Core memory surfaces

The authored/core memory layer should stay small, readable, and reviewable.
At the current public baseline, core memory surfaces follow the shipped `memory_object.schema.json` taxonomy.

At the current baseline, core memory includes:

- `anchor`
- `state_capsule`
- `episode`
- `claim`
- `decision`
- `pattern`
- `bridge`
- `audit_event`

These objects should remain the surfaces a human can inspect directly when asking what happened, why it matters, and what stronger source to inspect next.

## Supporting memory structures

Some memory-layer structures are first-class and important without currently being part of the shipped memory-object kind taxonomy.

At the current public baseline, supporting structures include:

- `provenance_thread`
- `recall_contract`

This keeps the machine-readable taxonomy aligned with the repo's current public surfaces.
`provenance_thread` may still be promoted later, but this round does not reopen that baseline.

## Derived memory surfaces

Derived memory may exist for retrieval, lift preparation, and downstream consumers, but it stays downstream of the authored/core layer.

Examples:

- chunk-oriented recall views
- graph-facing relation candidates
- embedding indexes
- retrieval caches
- KAG lift candidates
- framework adapters

These surfaces may accelerate recall.
They do not become the source of truth for memory meaning.

## Ownership split

- `aoa-memo` owns the explicit memory object and its provenance posture
- `aoa-kag` owns normalized derived substrate and graph-ready projections
- `abyss-stack` owns runtime stores, jobs, and storage topology
- `Tree-of-Sophia` owns source-authored texts, concepts, and lineage architecture

## Required handoff rules

Any handoff from core memory into derived memory should preserve:

- source refs
- provenance thread linkage where available
- temporal posture
- review state
- bounded statement of what was derived

Any return path from derived memory back into AoA should point back toward stronger authored surfaces rather than pretending the derived surface is final truth.

## Anti-goals

Avoid turning `aoa-memo` into:

- a proof layer
- a routing layer
- a live runtime state store
- a source replacement for ToS
- a silent graph platform
