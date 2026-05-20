# Memory Write Path Guardrails

## Purpose

This boundary names the write path that protects `aoa-memo` from poisoned,
untrusted, or action-bearing memory.

`aoa-memo` may receive candidates from agents, runtime exports, web research,
operator notes, and sibling repositories. Those inputs are useful only when
their trust posture, derivation lineage, review route, and action-safety split
are explicit.

## Core Rule

Untrusted text is data before it is memory.

Any input that may contain indirect instructions, source spoofing, sleeper
memory, poisoned experience, private leakage, or executable action pressure
enters as a reviewed candidate or quarantine record. It may become durable
memory only after an owner route and evidence-backed review make that promotion
visible.

## Write Path

1. Capture source refs and source trust.
2. Mark ingestion risks before summarizing.
3. Preserve derivation lineage for generated or agent-authored candidates.
4. Separate action text from executable action.
5. Route review to the stronger owner.
6. Land only candidate, reviewed, archived, or rejected posture.

The operational contract lives in
`mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md`.

## Boundary Fields

Every guarded write needs:

- source kind and source refs
- ingestion risk markers
- target memory kind
- proposed lifecycle
- review route
- derivation lineage when any summary or model output rewrites source text
- action-safety separation
- allowed write result

## Stop-lines

This boundary does not decide truth, execute actions, grant role rights, or
promote memory without review. Those decisions stay with source owners,
`aoa-evals`, `aoa-agents`, `abyss-stack`, `aoa-kag`, or the human operator
route that owns the stronger claim.
