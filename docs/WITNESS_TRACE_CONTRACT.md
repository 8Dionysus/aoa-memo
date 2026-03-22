# Witness Trace Contract

This document defines the current witness trace export contract for the witness/compost pilot wave.

It does not introduce a new memory-object kind.
It defines the public trace artifact that a scenario route may preserve before selected parts of that route are written back into the current memo taxonomy.

## Core rule

`WitnessTrace` is a trace export contract, not a memory object.

The witness may later write back into:

- `episode`
- `decision`
- `provenance_thread`
- `audit_event`

The trace itself remains the reviewable source artifact for that route.

## Contract objects

### `WitnessTrace`

Run-level witness record with:

- run identity
- goal
- bounded status
- time window
- step sequence
- human-readable summary output
- provenance and review notes

### `WitnessStep`

Step-level witness record with:

- ordered index
- step kind
- intent
- tool visibility when present
- observation
- state delta when an external effect occurred
- review flags or failure notes

### `TraceSummary`

Compact human-readable output that should answer:

- what the run was trying to do
- what it did
- where risk or review flags appeared
- what survived as the main result
- what a human should inspect next

## Required posture

The contract should preserve:

- run-level identity and goal
- bounded step sequence
- tool visibility
- state-delta visibility for external effects
- redaction-first handling
- failure-path preservation
- human-readable summary output

It should not preserve raw secret-bearing payloads or hidden chain-of-thought dumps.

## Writeback mapping

When a witness route writes back into memo-layer objects, use the current canon:

- trace event -> `episode`
- explicit gate or approval outcome -> `decision` when present
- accumulated route history -> `provenance_thread`
- failure or lifecycle transition -> `audit_event` where appropriate

The trace contract does not authorize a new memory-object family.
