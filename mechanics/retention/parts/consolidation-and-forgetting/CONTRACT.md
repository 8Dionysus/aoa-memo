# Consolidation and forgetting Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/retention/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and historical placement is recorded in `../../PROVENANCE.md`.

## Source Surfaces

- [CONSOLIDATION_FORGETTING_OPERATION](../../docs/CONSOLIDATION_FORGETTING_OPERATION.md)
- `schemas/memory_consolidation_forgetting_operation_v1.json`
- `schemas/active_organ_mechanical_lifecycle_plan_v0.schema.json`
- `schemas/active_organ_semantic_lifecycle_proposal_v0.schema.json`
- `schemas/active_organ_lifecycle_execution_receipt_v0.schema.json`
- `schemas/active_organ_erasure_recovery_probe_v0.schema.json`
- `schemas/active_organ_memo_erasure_owner_extension_v0.schema.json`
- `scripts/active_organ_lifecycle.py`
- `scripts/distributed_erasure.py`
- `examples/memory_consolidation_forgetting.supersede.example.json`
- `examples/memory_consolidation_forgetting.archive.example.json`

## Contract

keeps demotion, deduplication, supersession, retraction, archive, and freeze as explicit reviewed memory operations

## Artifact Contract

This part owns the schema and examples for lifecycle-changing memory
operations. Every operation keeps target memory ids, trigger, lifecycle
transition, retention fields, review route, output refs, and audit refs
inspectable.

The active-organ mechanical extension is pinned to the immutable C06 base
schema and [AOA-MEM-D-0079](../../../../docs/decisions/AOA-MEM-D-0079-mechanical-lifecycle-is-allowlisted-and-recoverable.md).
It admits only projection invalidation, projection rebuild, compaction,
explicit ephemeral TTL, queue cancellation, an owner-approved archive
deadline, cache expiry, generation rollover, and obsolete derived-artifact
removal. Each plan pins policy, owner, tenant, namespace, semantic digest,
source generation, expected version, exact effect scope, deadline, retry,
cancellation, compensation, commit receipt, and audit receipt.

Conflict, merge or split, narrowed applicability, supersession, retraction,
archive without a prior exact owner-approved deadline, temperature or salience
change, and retention change are proposal-only. They carry
`apply_allowed=false`, stay pending sole-operator review, and become deferred
rather than accepted or dropped when the attention budget is full.

An exact replay cannot create a second effect. Stale, conflicting, reordered,
expired, cancelled, or idempotency-mismatched work fails closed. If a
descendant projection fails after canonical commit, the canonical transition
remains valid, projection recall remains invalidated, and the receipt stays
`partial_pending_repair` until an audited repair.

## Distributed erasure closure

[AOA-MEM-D-0080](../../../../docs/decisions/AOA-MEM-D-0080-distributed-erasure-requires-walkable-owner-closure.md)
fixes ER0-ER9 as an exact surface set. C14 authorizes scope, C15 composes the
only global closure posture, C16 carries one owner-bounded work item, and C17
reports one owner-local result. Neither C16 nor C17 may claim global
completion.

Every surface must resolve through its C15 row, C16 work item, schema- and
digest-pinned owner extension, C17 receipt, and a content-minimized recovery
probe. The probe records a digest-only canary, proves the detector caught the
positive control before erasure, covers the surface's declared exact,
lexical, dense, graph, paraphrase, restore, or owner-native query routes, and
finds zero material afterward. ER2-ER8 additionally require a race/rebuild
attempt that does not restore the subject.

The surface manifest covers canonical objects, summaries and Markdown read
models; authorized raw evidence; local memo ports and lexical postings;
embeddings, graph and KAG projections; runtime stores, caches and nervous
indexes; exports and backup/restore descendants; host-local surfaces;
experiment replay copies; training datasets and model-checkpoint or unlearning
obligations; and a content-minimized ER9 tombstone. Residue and retention
exceptions remain explicit. Even an approved exception blocks plain-complete
private-memory deployment.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.

It also must not collapse decay, demotion, compression, merge, supersession,
retraction, quarantine, expiry, ordinary deletion, privacy erasure, or model
unlearning into a generic deletion result. Phase 10 performs neither privacy
erasure nor model unlearning. Phase 11 models only public-safe reference
closure; it authorizes no live deletion, raw-session mutation, backup purge,
physical erasure, or model unlearning.
