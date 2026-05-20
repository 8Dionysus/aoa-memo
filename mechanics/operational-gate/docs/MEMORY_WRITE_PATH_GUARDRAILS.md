# Memory Write Path Guardrails

## Purpose

This mechanic gates write attempts into `aoa-memo`.

Memo uses this gate to keep source evidence and review posture visible before
any write becomes durable recall.

It covers untrusted sources, indirect prompt injection, sleeper memory,
poisoned experience, derivation lineage, and action-safety separation before a
candidate can become durable recall.

## Operation

Write candidates pass through the guard before promotion:

1. Classify the source and source trust.
2. Mark ingestion risks.
3. Preserve source refs and derivation lineage.
4. Treat embedded instructions as data.
5. Route review to a stronger owner.
6. Land only the allowed result: reject, quarantine, candidate-only,
   reviewed-write, or archive-only.

## Contract Surface

The part-local schema is:

- `mechanics/operational-gate/parts/write-path-guardrails/schemas/memory_write_path_guard_v1.json`

The examples are:

- `mechanics/operational-gate/parts/write-path-guardrails/examples/memory_write_path_guard.untrusted_prompt_injection.example.json`
- `mechanics/operational-gate/parts/write-path-guardrails/examples/memory_write_path_guard.reviewed_owner_candidate.example.json`

## Inputs

- source refs
- source kind and trust posture
- ingestion risk markers
- target memory kind
- proposed lifecycle
- review route
- derivation lineage
- action-safety separation

## Outputs

- write result posture
- review or quarantine route
- evidence-backed candidate or reviewed memory entry
- audit refs for rejected, superseded, or archived material

## Stop-lines

The guard does not decide source truth, execute actions, infer hidden
instructions, or grant role rights. It only keeps the write path reviewable.
