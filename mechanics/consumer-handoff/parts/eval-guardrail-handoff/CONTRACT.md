# Eval guardrail handoff Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/consumer-handoff/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and historical placement is recorded in `../../PROVENANCE.md`.

## Source Surfaces

- [MEMORY_EVAL_GUARDRAILS](../../docs/MEMORY_EVAL_GUARDRAILS.md)
- `schemas/memory_eval_guardrail_pack.schema.json`
- `examples/memory_eval_guardrail_pack.example.json`

## Contract

names memory quality risk cases for downstream proof owners

## Artifact Contract

The part owns the memo-side guardrail handoff pack and schema. It may name
failure modes and input refs for downstream eval adoption, but scoring,
thresholds, pass/fail logic, and proof verdicts stay with `aoa-evals`.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
