# MEMORY MODEL

## Purpose

This document defines the conceptual model for memory in `aoa-memo`.

The goal is to make memory explicit, temporal, provenance-aware, and compatible with downstream KAG work without confusing memory with proof, routing, role policy, or source-authored knowledge.

## Design posture

A useful memory system for AoA and ToS should do more than store text.

It should make it possible to answer:

- what happened?
- what was later inferred from that event?
- how current or stale is this memory?
- what stronger source should be checked next?
- what can be recalled cheaply, and what requires deeper inspection?
- how can downstream graph lifts happen without making the memory layer itself a graph engine?

## Core vs derived memory

The first-wave rule is:

**authored/core memory stays in `aoa-memo`; derived memory stays downstream**

`aoa-memo` should own the explicit and reviewable memory object.
Chunk-facing views, graph-facing views, embedding indexes, and other retrieval-oriented derivatives may exist, but they remain downstream of the core object rather than replacing it.

See [NARRATIVE_CORE_CONTRACT](NARRATIVE_CORE_CONTRACT.md) for the compact ownership split and required handoff fields.

## Why this model is layered

The old split between short-term and long-term memory is too coarse for AoA.

AoA and ToS need memory that can distinguish:

- live task state from durable event memory
- raw episodes from consolidated claims
- source authority from model confidence
- current usefulness from historical significance
- local recall surfaces from downstream associative or graph-ready lifts

For that reason, `aoa-memo` uses four axes:

1. **function**: what kind of remembering is happening
2. **temperature**: how active and recallable the memory is right now
3. **scope**: where the memory is allowed to matter
4. **trust posture**: how the memory should be interpreted

## Axis 1: memory functions

### Working memory

Working memory holds current task state, open loops, assumptions, temporary hypotheses, and local progress.

This memory is usually hot and highly mutable.

Important rule: live working memory belongs primarily in runtime systems. `aoa-memo` may define exported **state capsules** or public summaries of that state, but it should not become the main live state store.

### Episodic memory

Episodic memory records that something happened.

Examples:

- an agent run occurred
- a source was inspected
- a handoff happened
- a decision point was reached
- a failure or success occurred
- a ToS interpretation event happened

Episodes are the most important durable raw layer because they preserve the trace that later claims can be built from.

Episodes should be treated as close to immutable.

### Semantic memory

Semantic memory stores consolidated, reusable statements derived from episodes and authoritative sources.

Examples:

- a stable project constraint
- a user preference that has been observed more than once
- a settled project fact with provenance
- a durable interpretation claim tied to sources

Semantic memory should never pretend to be timeless truth. It still needs provenance, time, and review posture.

### Procedural-experience memory

This is memory about what worked, failed, or repeated under certain conditions.

Examples:

- a skill run pattern that often succeeds under condition X
- a common failure mode for a routing choice
- a useful handoff format discovered in practice

This is not the same as a reusable technique or a skill definition.

`aoa-techniques` owns reusable practice. `aoa-skills` owns bounded execution workflows. `aoa-memo` may remember experience about them.

### Associative memory

Associative memory expresses bridges and relations that help recall fan outward.

Examples:

- this episode relates to that ToS node
- this decision is linked to a prior lineage
- this claim shares concepts with another project surface

Associative memory is where KAG orientation begins, but the normalized derived substrate still belongs in `aoa-kag`.

### Audit memory

Audit memory records review, supersession, retraction, access changes, and lifecycle events.

This layer protects the honesty of the memory system.

It makes it possible to say not only what was remembered, but also how that memory changed over time.

## Axis 2: temperature

Temperature describes recall posture, not truth.

A hot memory object may be extremely useful and still be wrong.
A frozen object may be stable and still be narrow in scope.

### Hot

- currently active
- cheap to read and write
- likely to change quickly
- usually session- or task-adjacent

### Warm

- active project memory
- often recalled by default
- stable enough for reuse, but still likely to move

### Cool

- consolidated and cross-session
- not needed on every task
- often summary-first before deeper expansion

### Cold

- archival or rarely needed
- usually retrieved only by explicit request, trace-back, or audit needs

### Frozen

- intentionally stabilized
- usually human-reviewed or tied to an authoritative source boundary
- may serve as an anchor or stable reference point

## Axis 3: scope

Scope tells us where a memory object is allowed to matter.

Common scopes include:

- **thread**: one conversation or task thread
- **session**: one working session or run window
- **user**: persistent user-level memory
- **agent**: role-specific or actor-specific memory context
- **project**: one repo, initiative, or bounded effort
- **workspace**: a cluster of related repos or services
- **ecosystem**: AoA-wide memory surfaces
- **ToS node / lineage**: memory tied to specific knowledge-world structures

A memory object may have more than one scope, but scope expansion should be explicit rather than accidental.

## Axis 4: trust posture

Trust should not be compressed into a single magic number.

The model distinguishes at least these dimensions:

### Confidence

How plausible or well-supported the memory object appears from the current evidence.

### Authority

How strong the source is.

Examples:

- human-reviewed source
- direct source extract
- agent-derived summary
- inferred pattern

### Freshness

How current the memory is for the question being asked.

Freshness can decay even when the original episode remains historically true.

### Salience

How worth recalling the memory is right now.

Salience is about relevance pressure, not truth.

## Object canon

The memory layer should use a small set of explicit object kinds.

### `anchor`

A stabilized reference point.

Used for constitutional, source-authoritative, or otherwise intentionally stable memory surfaces.

### `state_capsule`

A compact exported view of working state.

This is not the live runtime state itself. It is the public, reviewable capsule that other layers may inspect.

### `episode`

An event record.

This is the primary durable raw memory object.

### `claim`

A consolidated statement derived from episodes and or authoritative sources.

Claims must remain temporal and provenance-aware.

### `decision`

An explicit choice, including context, rationale, and scope.

Decisions are important enough to warrant first-class treatment rather than hiding inside generic summary text.

### `pattern`

A repeated procedural-experience memory.

This records observed regularity. It does not define canonical practice.

### `bridge`

A memory object that primarily exists to connect surfaces, such as linking an episode to a ToS fragment, a concept cluster, or a KAG lift candidate.

### `provenance_thread`

A first-class structure linking related memory objects, source refs, and lifecycle steps across time.

### `audit_event`

A lifecycle or governance event such as confirmation, supersession, freeze, retraction, or access-class change.

## Suggested object fields

The exact schema can evolve, but a durable memory object should usually be able to express these families of fields:

### Identity

- `id`
- `kind`
- `scope`
- `owner_refs`

### Content

- `title`
- `summary`
- `payload_ref` or bounded payload

### Provenance

- `source_refs`
- `episode_refs`
- `provenance_thread_id`

### Time

- `created_at`
- `observed_at`
- `valid_from`
- `valid_to`

### Trust posture

- `confidence`
- `authority`
- `freshness`
- `salience`
- `temperature`

### Lifecycle

- `review_state`
- `supersedes`
- `superseded_by`
- `retention_class`

### Access and bridges

- `access_class`
- `read_scopes`
- `write_scopes`
- `tos_refs`
- `skill_refs`
- `eval_refs`
- `kag_lift_status`
- `route_capsule_ref`

## Lifecycle model

Memory should pass through explicit lifecycle states rather than mutating silently.

A useful default sequence is:

`captured -> proposed -> confirmed -> frozen -> superseded -> retracted -> archived`

Not every object will use every state, but the state machine should make it obvious whether a memory object is raw, stabilized, outdated, or withdrawn.

## Two-speed memory pipeline

AoA memory should run at two speeds.

### Online path

Fast path for current work:

- capture state capsules
- record episodes
- attach basic provenance
- keep the write path cheap

### Offline path

Slower path for durable memory quality:

- deduplicate
- consolidate episodes into claims or patterns
- update salience and freshness posture
- propose freeze candidates
- create bridge objects for downstream KAG work
- record audit events

This split lets the system stay responsive without letting the long-term layer become sludge.

## Checkpoint route writeback

The self-agent checkpoint route should write back into the current memory taxonomy without inventing a new mythic object family.

Use the current object canon like this:

- `approval_record` -> `decision`
- `rollback_marker` -> explicit referenced artifact or bounded state marker
- `health_check` -> `episode` or `audit_event`
- `improvement_log` -> `provenance_thread`

This keeps checkpoint history reviewable while preserving the current rule:

**write the event once, derive downstream surfaces later**

## Recall modes

The memory layer should support bounded recall modes rather than one giant generic retrieval call.

### `working`

Return current or recent state capsules.

### `episodic`

Return event memory with provenance emphasis.

### `semantic`

Return consolidated claims with explicit temporal posture.

### `procedural`

Return patterns about what worked, failed, or repeated.

### `lineage`

Return bridges tied to ToS nodes, concepts, fragments, or longer chains of relation.

### `source_route`

Return the strongest next source-owned surfaces to inspect when memory alone is not enough.

## KAG orientation

`aoa-memo` should be KAG-oriented without becoming `aoa-kag`.

The guiding rule is:

**write the event once, derive downstream surfaces later**

Each memory object should be able to expose two compatible faces:

### Chunk face

For bounded inspection and retrieval:

- capsule text
- section refs
- source spans or fragment refs
- compact summaries
- recall metadata

### Graph face

For downstream associative and KAG lifts:

- entity refs
- concept refs
- relation candidates
- provenance thread ids
- time windows
- ToS refs and lineage bridges

`aoa-memo` may define and export these faces.
`aoa-kag` owns normalization, substrate formation, and downstream framework adapters.

## Relationship to the rest of AoA and ToS

### `aoa-agents`

Owns who can read, write, promote, freeze, or hand off memory.

### `aoa-routing`

Owns how a model or human is routed toward the smallest next source surface.

### `aoa-kag`

Owns derived knowledge substrate, graph-ready normalization, and downstream retrieval adapters.

### `aoa-evals`

Owns checks for recall precision, provenance fidelity, staleness handling, contradiction handling, and leakage.

### `aoa-playbooks`

Owns scenario-level memory requirements and composition rules.

### `abyss-stack`

Owns runtime stores, lifecycle jobs, security posture, backup, and restore.

### `Tree-of-Sophia`

Owns source-authored texts, concepts, semantic layers, and lineage architecture. `aoa-memo` remembers interactions with that world. It does not replace the world.

## Non-goals

This memory model is not trying to define:

- one giant universal memory score
- a hidden proof system
- a routing engine
- a full graph platform
- runtime deployment or storage topology
- a substitute for ToS source architecture

## Example pattern

A useful way to think about the system is:

- a **ToS fragment** lives in `Tree-of-Sophia`
- an **interpretation event** becomes an `episode` in `aoa-memo`
- a repeated interpretation becomes a `claim` or `pattern`
- a cross-link to concept and lineage becomes a `bridge`
- a normalized associative lift becomes downstream `aoa-kag` substrate

The same pattern can hold for self-agent checkpoint work:

- an approval gate becomes a `decision`
- a post-change health result becomes an `episode`
- the full improvement log becomes a `provenance_thread`

That keeps source, memory, and derived knowledge distinct while still allowing them to connect.
