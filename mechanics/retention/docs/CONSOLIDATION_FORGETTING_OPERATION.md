# Consolidation And Forgetting Operation

## Purpose

This mechanic owns the memo-side operation for demotion, deduplication,
supersession, retraction, archive, and freeze.

The existing lifecycle, temperature, TTL, half-life, retire-after, and audit
fields already describe memory state. This document defines the repeatable
operation that changes that state.

## Operation

1. Detect a trigger: expiry, contradiction, duplicate cluster, owner
   supersession, source withdrawal, safety retraction, or low recall value.
2. Gather target memory ids, source refs, and current lifecycle posture.
3. Choose the operation: demote, deduplicate, supersede, retract, archive,
   freeze, split, or merge-review.
4. Record retention fields and review route.
5. Emit output refs and audit-event refs.
6. Regenerate read models when active recall posture changes.

## Regular Pressures

| Pressure | Trigger | Expected output |
|---|---|---|
| demote | salience drops or recall pressure weakens | lower temperature or less preferred current recall |
| deduplicate | repeated candidates point to the same memory question | one preferred object with preserved provenance refs |
| supersede | newer route decision or stronger source correction replaces current use | old object marked historical or withdrawn from preferred recall |
| retract | source withdrawal, unsafe overread, malformed memory, poisoned input, or private material | withdrawn current recall plus audit walkback |
| archive | cooled history, completed run, or replaced state snapshot | historical recall posture |
| freeze | stable doctrine, reviewed boundary, or durable route law | explicit freeze basis |
| split | one object carries multiple memory questions | narrower objects plus original-object audit posture |
| merge-review | several traces may describe one memory but need review | merge candidate, not a hallucinated combined object |

## Contract Surface

The part-local schema is:

- `mechanics/retention/parts/consolidation-and-forgetting/schemas/memory_consolidation_forgetting_operation_v1.json`

The Phase 10 active-organ extension is additive to the immutable C06 base
contract:

- `mechanics/retention/parts/consolidation-and-forgetting/schemas/active_organ_mechanical_lifecycle_plan_v0.schema.json`
- `mechanics/retention/parts/consolidation-and-forgetting/schemas/active_organ_semantic_lifecycle_proposal_v0.schema.json`
- `mechanics/retention/parts/consolidation-and-forgetting/schemas/active_organ_lifecycle_execution_receipt_v0.schema.json`
- `mechanics/retention/parts/consolidation-and-forgetting/scripts/active_organ_lifecycle.py`

Only nine exact mechanical classes may use that plan: projection invalidation,
projection rebuild, compaction, explicit ephemeral TTL, queue cancellation,
an owner-approved archive deadline, cache expiry, generation rollover, and
obsolete derived-artifact removal. Admission requires the class-specific
precondition plus accepted policy, exact owner and scope pins, expected
version, deadline, bounded retry, cancellation, compensation, and distinct
commit and audit refs.

Conflict, merge or split, narrowed applicability, supersession, retraction,
archive without a prior exact approval, temperature or salience change, and
retention change remain semantic proposals. A proposal cannot apply or approve
itself. When the sole-operator attention budget is full, it is deferred rather
than silently accepted or discarded.

The forgetting taxonomy remains explicit: decay, demotion, compression, merge,
supersession, retraction, quarantine, expiry, ordinary deletion, privacy
erasure, and model unlearning are not interchangeable. Projection maintenance,
queue cancellation, and generation rollover are not forgetting. Phase 10
does not perform privacy erasure or model unlearning.

The examples are:

- `mechanics/retention/parts/consolidation-and-forgetting/examples/memory_consolidation_forgetting.supersede.example.json`
- `mechanics/retention/parts/consolidation-and-forgetting/examples/memory_consolidation_forgetting.archive.example.json`

## Stop-lines

This operation changes memo-side recall posture. It does not delete source
truth, erase provenance, decide stronger owner policy, or hide a retraction.
Reference receipts do not prove a durable runtime worker. A projection failure
after canonical commit remains visible as `partial_pending_repair`, blocks
affected recall, and requires compensation or forward repair; partial work is
never success.
