# Decision: Keep mechanical lifecycle allowlisted and recoverable

- Decision ID: AOA-MEM-D-0079

## Status

Accepted on 2026-07-29 for source-local Phase 10 contracts and reference-lab
evaluation. Runtime admission, deployed workers, policy activation, and
landing remain deferred.

## Index Metadata

- Original date: 2026-07-29
- Surface classes: lifecycle/retention, boundary/runtime/sibling
- Mechanic parents: retention
- Guard families: lifecycle/retention, memory surface, sibling and boundary
- Memory object classes: decision, audit_event
- Posture: active allowlisted-mechanical rationale

## Context

The active-organ contract spine already defines C06
`MemoryLifecycleTransition`: semantic transitions require an operator
decision, mechanical transitions require an accepted policy, both compare an
expected prior version, advance a version, and name belief-commit and audit
receipts. The existing retention mechanic also distinguishes demotion,
deduplication, supersession, retraction, archive, freeze, split, and
merge-review.

Those contracts do not yet make the Phase 10 automation boundary executable.
A trigger, age, score, queue retry, or model suggestion must not silently turn
into semantic authority. At the same time, projection invalidation, rebuild,
explicit ephemeral expiry, and other disposable maintenance need a precise
idempotent path that does not consume the sole operator's attention for every
safe retry.

## Decision

Add a C06-compatible Phase 10 owner extension under the retention mechanic.
It pins the immutable active-organ v1 base schema and records, for every
mechanical plan:

- exact policy id, version, digest, and decision;
- operation and forgetting taxonomy classes;
- subject owner, tenant, namespace, version, state, semantic digest, and
  source generation;
- preconditions and expected prior version;
- exact effect scope;
- idempotency key, deadline, bounded attempts, backoff, and cancellation;
- rollback or forward-repair posture;
- required belief-commit and audit receipt refs;
- an explicit reference-lab-only execution ceiling.

Only these operation classes enter the Phase 10 mechanical allowlist:

- `projection_invalidation`;
- `projection_rebuild`;
- `compaction`;
- `explicit_ephemeral_ttl`;
- `queue_cancellation`;
- `owner_approved_archive_deadline`;
- `cache_expiry`;
- `generation_rollover`;
- `obsolete_derived_artifact_removal`.

The class is not admitted by name alone:

- projection work requires a disposable projection and exact source
  generation;
- TTL requires an explicitly ephemeral subject and a reached fixed deadline;
- archive deadline requires an exact prior owner approval;
- ordinary deletion is limited to an obsolete derived artifact and cannot
  target canonical semantic content;
- all classes forbid cross-tenant movement, physical privacy erasure,
  source-owner replacement, permission change, and semantic-content mutation.

The forgetting taxonomy remains explicit. Projection maintenance, queue
cancellation, and generation rollover are `not_forgetting`; compaction is
`compression`; fixed TTL and cache expiry are `expiry`; an approved archive
deadline is `archive`; obsolete derived removal is `ordinary_deletion`.
Decay, demotion, merge, supersession, retraction, quarantine, privacy erasure,
and model unlearning retain their distinct meanings and cannot be reported as
one of these mechanical effects by analogy.

AI may emit only proposal-only records for:

- conflict;
- merge or split;
- narrowed applicability;
- supersession;
- retraction;
- archive without a prior exact owner-approved deadline;
- temperature or salience change;
- retention change.

Such a proposal carries evidence, a bounded diff, and solo-operator attention
posture. It fixes `apply_allowed=false`. Work beyond the configured open-review
budget becomes explicitly deferred; it is neither accepted nor dropped.

A reference transaction may commit canonical version and lifecycle state
before a projection owner completes invalidation or rebuild. If descendant
work fails, the canonical commit remains valid, affected projection admission
fails closed, and the result is `partial/pending_repair`. Partial progress is
never success. Exact replay after acknowledgement loss creates no second
effect. A stale expected version, reordered event chain, expired deadline,
cancelled work item, conflicting transition, or reused idempotency key with a
different payload fails closed.

`aoa-memo` owns plan and proposal meaning. `aoa-sdk` remains the future
control-plane admission owner and may coordinate only exact owner-pinned
envelopes. `abyss-stack` owns future durable workers and storage transactions.
`aoa-kag` owns projection invalidation and rebuild receipts. `abyss-machine`
owns host-local physical work. `aoa-evals` owns the Phase 10 failure-injection
verdict.

This decision authorizes contracts, validators, deterministic reference
simulation, adversarial evaluation, and disposable lab artifacts. It does not
authorize live lifecycle policy, a scheduler, canonical private storage,
runtime execution, privacy erasure, deployment, or landing.

## Alternatives

- Extend the immutable active-organ v1 schema in place. Rejected because the
  landed v1 contract requires a new schema for semantic or authority changes.
- Let the model choose which lifecycle transition is mechanical. Rejected
  because classification by analogy is hidden semantic authority.
- Roll back every canonical commit when a projection owner is unavailable.
  Rejected because projection completion governs recall admission, not the
  validity of an already accepted canonical transition.
- Treat partial descendant work as success and repair later. Rejected because
  it exposes mixed belief state and makes residue invisible.
- Route every safe retry to the operator. Rejected because it spends the
  solo-operator attention budget on deterministic replay rather than semantic
  judgment.

## Consequences

- Safe maintenance can be tested without widening semantic authority.
- Each operation has an exact owner, policy, version, deadline, compensation,
  and audit trail.
- Canonical and projection state can recover independently while recall stays
  fail closed.
- Semantic work remains visible as proposals and consumes a bounded,
  inspectable solo-operator queue.
- A green reference lab remains weaker than durable stack storage,
  multi-process crash recovery, natural workload precision, and runtime
  deployment.

## Affected Surfaces

- `mechanics/retention/parts/consolidation-and-forgetting/`
- `mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md`
- `docs/memory/MEMORY_MODEL.md`
- `aoa-evals` active-organ offline replay bundle
- `aoa-kag` projection-health contracts
- future `aoa-sdk` lifecycle admission and `abyss-stack` runtime workers

## Verification

Phase 10 must prove:

- all nine exact mechanical classes validate and no extra class is admitted;
- semantic proposals cannot execute;
- exact duplicate delivery creates no second effect;
- a stale retry and conflicting transition fail before commit;
- crash before commit is safely retryable;
- crash after commit but before acknowledgement does not double-commit;
- projection failure after canonical commit becomes fail-closed partial work
  and can be repaired forward;
- reordered events, missed deadlines, and cancellation fail closed;
- concurrent readers observe either the prior committed version or the new
  committed version with descendants invalidated, never mixed active state;
- provenance, semantic digest, tenant, namespace, and authority ceilings
  survive every path;
- backlog beyond the solo-operator attention budget remains deferred rather
  than silently accepted or discarded.
