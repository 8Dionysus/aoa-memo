# Memory Eval Guardrails

## Purpose

This document defines memo-side guardrail targets that `aoa-evals` may turn into bounded proof surfaces.

It keeps memory quality discussable without moving verdict logic into `aoa-memo`.

## Boundary Rule

`aoa-memo` names the memory failure modes and machine-readable case surfaces to hand off.

`aoa-evals` still owns:

- scoring
- pass/fail logic
- evidence weighting
- verdict language

## Guardrail Cases

The current guardrail set keeps these risks explicit:

- recall precision
- provenance fidelity
- staleness handling
- contradiction handling
- permission leakage
- over-promotion
- hallucinated memory merges

These are memory quality risks, not verdicts by themselves.

## First Downstream Pilot

The first downstream pilot in `aoa-evals` should stay intentionally narrow.

It covers only:

- recall precision
- provenance fidelity
- staleness

That pilot is a bounded adoption wave, not the whole guardrail program.
It does not yet absorb contradiction handling, permission leakage, over-promotion, or hallucinated memory merge checks into the first proof bundle.

## Machine-readable Handoff Surface

The current schema-backed guardrail handoff surface is:

- `schemas/memory_eval_guardrail_pack.schema.json`
- `examples/memory_eval_guardrail_pack.example.json`

Each case should preserve:

- the bounded focus area
- the input refs
- the expected behavior
- the failure signals that should become visible if posture drifts

## What Success Looks Like

A good downstream eval pack should make it possible to tell:

- whether memo returns the smallest relevant surface first
- whether provenance survives recall and expansion
- whether stale or superseded memory is handled honestly
- whether current recall posture stays visible
- whether contradictions stay visible
- whether role rights are inferred incorrectly from memo fields
- whether promotion posture drifts beyond reviewable evidence
- whether separate traces are hallucinated into one false memory object

## What This Surface Does Not Do

This surface does not:

- publish verdict logic
- replace `aoa-evals`
- define consumer-specific thresholds
- force one universal score for memory quality
- turn memory examples into proof by themselves
