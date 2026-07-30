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

The baseline rule is:

**authored/core memory stays in `aoa-memo`; derived memory stays downstream**

`aoa-memo` should own the explicit and reviewable memory object.
Chunk-facing views, graph-facing views, embedding indexes, and other retrieval-oriented derivatives may exist, but they remain downstream of the core object rather than replacing it.

See [NARRATIVE_CORE_CONTRACT](NARRATIVE_CORE_CONTRACT.md) for the compact ownership split and required handoff fields.

## Active-organ contract spine

An active memory organ participates in agent life by carrying bounded evidence,
recall, lifecycle, and erasure posture. Participation does not make memory an
action authority. `aoa-memo` may produce a silence decision or a bounded
observation; routing, tool selection, and external effects remain outside this
owner.

The strict memo-owned v1 ABI lives in
`schemas/support-objects/active_organ_memo_contracts_v1.schema.json`. It owns:

- evidence envelopes, candidate packets, and quarantine packets
- reviewed-memory wrappers, provenance threads, and lifecycle transitions
- recall packets, intervention decisions, and memory-influence policy envelopes
- disposable memory-projection manifests with exact source-generation posture
- erase requests, distributed erase manifests, per-owner work items, and
  completion-or-residue receipts

The stable IDs and local dependency direction are:

| ID | Contract | Requires | Produces |
|---|---|---|---|
| `C01` | `MemoryEvidenceEnvelope` | stronger owner source or bounded observation | evidence for intake |
| `C02` | `MemoryCandidatePacket` | `C01` plus derivation, risk, tenant, expiry, and taint posture | proposal only |
| `C03` | `MemoryQuarantinePacket` | candidate or guarded intake plus monotonic taint | isolated, non-recallable packet |
| `C04` | `ReviewedMemoryObject` | accepted `C06` transition | versioned reviewed-memory reference |
| `C05` | `ProvenanceThread` | evidence and transition refs | content-minimized lineage |
| `C06` | `MemoryLifecycleTransition` | expected version plus operator decision or accepted mechanical policy | belief commit and audit refs |
| `C08` | `RecallPacket` | SDK-owned `C07` intent plus reviewed object and projection pins | silence or cited bounded memory |
| `C09` | `InterventionDecision` | `C08`, exact trigger/anchor/taint refs, and `C11` | silence or bounded observation |
| `C11` | `MemoryInfluencePolicyEnvelope` | operator-approved policy tuple | effect ceiling for SDK and stack |
| `C12` | `MemoryProjectionManifest` | canonical objects, exact source generation, builder and optional owner-extension pins | disposable recall-eligibility posture only |
| `C14` | `MemoryEraseRequest` | exact operator decision and ER0-ER9 scope | approved work request |
| `C15` | `DistributedMemoryEraseManifest` | `C14`, owner set, surfaces, descendants, and exceptions | global pending or closure posture |
| `C16` | `PerOwnerEraseWorkItem` | `C15` | owner-bounded physical work request |
| `C17` | `EraseCompletionOrResidueReceipt` | completed `C16` attempt and recovery probe | owner-local result, never global completion |

Every object in this family pins its schema, source, generation, policy,
version, idempotency key, and content digest. Unknown fields and versions fail
closed. The public example suite includes one accepted payload and one
executable rejection case for every contract type.

Version `1.0.0` is immutable after landing. A semantic field change, relaxed
enum, authority change, or new effect class requires a new schema file and an
explicit migration; consumers must continue to pin the old `$id` and digest
until their owner-local conformance tests accept the new version. Additive
owner-local fields do not travel as unvalidated inline data: `C16` and `C17`
carry a pinned `owner_extension` schema, payload reference, version, and
digest; C12 uses the same pin for graph or runtime projection extensions. A
generated mirror is compatibility evidence, never semantic
authority.

The family preserves five hard boundaries:

1. A candidate is not reviewed memory. Promotion requires an accepted,
   version-advancing lifecycle transition.
2. Semantic transitions require the operator decision; mechanical transitions
   require an accepted policy. Both emit commit and audit receipt references.
3. Recall is evidence for a consumer decision, never permission to act.
   `action_use` stays `forbidden`, and silence is a valid result.
4. Private-corpus admission remains disabled unless an explicit private-corpus
   decision reference is present.
5. A projection is disposable and has no acceptance authority. Only an exact
   current source generation may be recall-eligible; stale, pending, and
   invalidated projections fail closed until an owner receipt and rebuild.
6. Erasure is distributed work, not a local delete claim. Global completion
   requires ER0-ER9 exactly once, per-surface owner work and receipts,
   schema-pinned owner extensions, positive controls, content-minimized
   negative recovery, required race/rebuild probes, and no unreported residue.
   Recovery covers exact, lexical, dense, graph, paraphrase, restore, and
   owner-native routes. An approved retention exception stays visible but
   blocks plain-complete private-memory deployment. `abyss-machine` work items
   may target only host-owned roots and never stack or project roots.

This schema family is a source contract, not a live memory store. Runtime
storage, lifecycle jobs, backup, and restore stay with `abyss-stack`;
host-local resources stay with `abyss-machine`; consumer dispatch and
control-plane policy stay with `aoa-sdk`; derived retrieval and graph
projections stay with `aoa-kag`; measurement and verdict authority stay with
`aoa-stats` and `aoa-evals`.

Outcome-qualified episodic utility remains outside reviewed semantic state.
`aoa-stats` may aggregate compatible C10 facts, `aoa-evals` owns the evidence
verdict, and `aoa-memo` may emit only a bounded policy proposal. Pending
delayed outcomes freeze positive adjustment; access count is not an input;
rare critical evidence keeps an explicit preservation floor. No score may
promote, delete, retract, change ownership, expand a tenant or permission, or
approve its own policy.

Agent-local episodic and procedural memory is an optional leaf below this
shared model. `aoa-agents` owns the exact agent/tenant namespace posture;
`aoa-memo` accepts only a content-minimized reviewed-promotion nomination.
Duplicate or subsumed material yields no write, unresolved conflict stays
quarantined, and even an approved admission produces only a proposed memo
candidate. Shared truth still requires the ordinary C02 review and C06
lifecycle path. Local expiry, rollback, or namespace disable cannot mutate an
already reviewed shared object.

Mechanical lifecycle work is narrower than semantic forgetting. The
Phase 10 C06 extension admits exactly projection invalidation, projection
rebuild, compaction, explicit ephemeral TTL, queue cancellation, an
owner-approved archive deadline, cache expiry, generation rollover, and
obsolete derived-artifact removal. Each plan pins accepted policy, expected
version, source generation, owner and scope, deadline, bounded retry,
cancellation, compensation, and distinct commit and audit receipts. Exact
replay creates no second effect; stale, conflicting, reordered, expired, or
cancelled work fails closed.

Conflict, merge or split, narrowed applicability, supersession, retraction,
archive without an exact prior approval, temperature or salience change, and
retention change remain proposal-only for the sole operator. Overflow beyond
the review budget is explicitly deferred. A projection failure after canonical
commit leaves that commit valid but affected recall invalidated and the result
`partial_pending_repair`; it cannot be reported as success.

Decay, demotion, compression, merge, supersession, retraction, quarantine,
expiry, ordinary deletion, privacy erasure, and model unlearning remain
different operations. Projection maintenance, queue cancellation, and
generation rollover are not forgetting. Privacy erasure and model unlearning
are outside the Phase 10 mechanical extension and require their stronger
owners and closure evidence.

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
The current public contract treats this as an ordinal `0..1` memo-side posture signal.

### Authority

How strong the source is.

Examples:

- human-reviewed source
- direct source extract
- agent-derived summary
- inferred pattern

The current public contract splits authority into:

- `authority_kind` for the stable machine-readable category
- `authority` for bounded human-readable explanation

### Freshness

How current the memory is for the question being asked.

Freshness can decay even when the original episode remains historically true.
The current public contract treats this as an ordinal `0..1` posture signal.

### Salience

How worth recalling the memory is right now.

Salience is about relevance pressure, not truth.
The current public contract treats this as an ordinal `0..1` posture signal.
When more detail is needed, `salience_components` may break that pressure into `novelty`, `impact`, `recurrence`, and `risk`.

See [MEMORY_TRUST_POSTURE](MEMORY_TRUST_POSTURE.md) for the contract that fixes ordinal versus categorical versus descriptive trust fields.

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
- `authority_kind`
- `authority`
- `freshness`
- `salience`
- `temperature`

### Lifecycle

- `review_state`
- `current_recall`
- `freeze_basis`
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

Current recall posture should remain explicit as well:

- `preferred`
- `allowed`
- `historical`
- `withdrawn`

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

## Witness trace export

The witness/compost pilot adds a public witness trace contract.

That contract is not a new memory-object kind.
It is the bounded route artifact that may later write selected pieces into the current object canon.

Use the current canon like this:

- whole witnessed run -> `episode`
- explicit gate or approval outcome -> `decision` when present
- route history across the run -> `provenance_thread`
- failure or lifecycle transition -> `audit_event`

See [WITNESS_TRACE_CONTRACT](../mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md) for the compact trace-export contract and required summary posture.

## Recall modes

The memory layer should support bounded recall modes rather than one giant generic retrieval call.

### `working`

Return current or recent state capsules.

Concrete entrypoint: `examples/recall/recall_contract.working.json`

### `episodic`

Return event memory with provenance emphasis.

### `semantic`

Return consolidated claims with explicit temporal posture.

### `procedural`

Return patterns about what worked, failed, or repeated.

### `lineage`

Return bridges tied to ToS nodes, concepts, fragments, or longer chains of relation.

Concrete entrypoints:

- `examples/recall/recall_contract.lineage.json`
- `examples/recall/recall_contract.router.lineage.json`

### `source_route`

Return the strongest next source-owned surfaces to inspect when memory alone is not enough.

## KAG orientation

`aoa-memo` should be KAG-oriented without becoming `aoa-kag`.

The guiding rule is:

**write the event once, derive downstream surfaces later**

See [KAG_TOS_BRIDGE_CONTRACT](../mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md) for the current chunk-face, graph-face, and ToS-bridge handoff surfaces.

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

See [AGENT_MEMORY_POSTURE_SEAM](../mechanics/consumer-handoff/docs/AGENT_MEMORY_POSTURE_SEAM.md) for the memo-side fields that those rights may apply to without moving rights policy into `aoa-memo`.

### `aoa-sdk`

Owns how a model or human is routed toward the smallest next source surface.

### `aoa-kag`

Owns derived knowledge substrate, graph-ready normalization, and downstream retrieval adapters.

### `aoa-evals`

Owns checks for recall precision, provenance fidelity, staleness handling, contradiction handling, and leakage.

See [MEMORY_EVAL_GUARDRAILS](../mechanics/consumer-handoff/docs/MEMORY_EVAL_GUARDRAILS.md) for the memo-side handoff surface that keeps these risks explicit.

### `aoa-playbooks`

Owns scenario-level memory requirements and composition rules.

See [PLAYBOOK_MEMORY_SCOPES](../mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md) for the memo-side guidance on scopes and recall modes that playbooks may request.

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
