# Decision: Agent-local promotion is not shared truth

- Decision ID: AOA-MEM-D-0081

## Status

Accepted on 2026-07-29 for source-local Phase 12 contracts and isolated
evaluation. Runtime deployment, live private ingestion, semantic auto-write,
and landing remain deferred.

## Index Metadata

- Original date: 2026-07-29
- Surface classes: consumer handoff, local port/writeback
- Mechanic parents: consumer-handoff
- Guard families: memory surface, sibling and boundary
- Memory object classes: episode, pattern, decision
- Posture: active agent-local federation rationale

## Context

Agent-local episodic and procedural memory can reduce blast radius and shorten
the local learning loop, but it also creates duplication, fragmented policy,
private-to-shared leakage risk, and a promotion-review burden. Treating a
local case as shared memory merely because it helped one agent would bypass
the reviewed `aoa-memo` ledger and turn local reward into ecosystem truth.

## Decision

An agent-local namespace may nominate a content-minimized promotion candidate.
It may not write the shared ledger.

The candidate pins the exact `aoa-agents` namespace contract, generation,
agent, tenant, local case digest, evidence, outcomes, target scope, duplicate
checks, and conflict checks. Cross-tenant nomination is forbidden. Raw local
payload is absent from the promotion envelope.

An operator-reviewed admission receipt may yield only:

- a proposed `aoa-memo` candidate;
- duplicate/no-write;
- conflict quarantine;
- rejection; or
- deferral.

Even an approved admission leaves the shared ledger unchanged and performs no
semantic transition. Shared truth appears only through the ordinary
`aoa-memo` candidate, review, and lifecycle path after this handoff.

Duplicate or subsumed material produces no candidate. Unresolved conflict is
quarantined. Local rollback and expiry never mutate an already reviewed shared
object. Consumer-specific policy and control-plane admission remain with
`aoa-sdk`; role and namespace rights remain with `aoa-agents`; runtime
isolation remains with `abyss-stack`; proof remains with `aoa-evals`.

## Alternatives

- Allow local agents to publish directly after a successful outcome. Rejected
  because one local reward loop is not shared semantic review.
- Merge all local stores before deduplication. Rejected because it enlarges the
  privacy and contamination blast radius.
- Reject all local learning. Rejected because bounded local episodic and
  procedural cases may produce benefit without becoming shared truth.
- Let `aoa-memo` own agent role rights. Rejected because actor posture belongs
  to `aoa-agents`.

## Consequences

- Shared truth cannot appear silently from a local namespace.
- Promotion burden is explicit and measurable.
- Duplicate and conflict outcomes are typed instead of hidden in reviewer
  prose.
- Local namespace rollback remains independent from shared semantic
  lifecycle.
- Phase 12 can compare the benefit and coordination cost of the D contour
  without deploying private memory.

## Affected Surfaces

- `mechanics/consumer-handoff/parts/orchestrator-recall-alignment/`
- `docs/memory/MEMORY_MODEL.md`
- `aoa-agents` agent-local namespace posture
- `aoa-sdk` consumer-specific namespace plan
- `abyss-stack` namespace runtime boundary
- `aoa-evals` Phase 12 federation lab

## Verification

Phase 12 must prove:

- exact agent and tenant isolation;
- bounded local ranking adaptation with outcome evidence;
- no direct shared write;
- duplicate/no-write and conflict-quarantine behavior;
- local expiry and rollback;
- namespace disable without shared-organ failure;
- consumer-zero removal;
- portable behavior across the declared agent/model identities;
- promotion burden remains below measured benefit and inside the
  solo-operator review budget.
