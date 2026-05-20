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

## Contract Surface

The part-local schema is:

- `mechanics/retention/parts/consolidation-and-forgetting/schemas/memory_consolidation_forgetting_operation_v1.json`

The examples are:

- `mechanics/retention/parts/consolidation-and-forgetting/examples/memory_consolidation_forgetting.supersede.example.json`
- `mechanics/retention/parts/consolidation-and-forgetting/examples/memory_consolidation_forgetting.archive.example.json`

## Stop-lines

This operation changes memo-side recall posture. It does not delete source
truth, erase provenance, decide stronger owner policy, or hide a retraction.
