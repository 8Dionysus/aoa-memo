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

The examples are:

- `mechanics/retention/parts/consolidation-and-forgetting/examples/memory_consolidation_forgetting.supersede.example.json`
- `mechanics/retention/parts/consolidation-and-forgetting/examples/memory_consolidation_forgetting.archive.example.json`

## Stop-lines

This operation changes memo-side recall posture. It does not delete source
truth, erase provenance, decide stronger owner policy, or hide a retraction.
