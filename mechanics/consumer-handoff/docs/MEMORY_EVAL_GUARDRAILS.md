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
- temporal reasoning
- knowledge update
- abstention
- selective forgetting
- poisoning

These are memory quality risks, not verdicts by themselves.

## Quality Harness Plan

`aoa-memo` should hand off cases by lens. `aoa-evals` decides scoring,
thresholds, reports, and verdict language.

| Lens | Stable question | Required evidence | Failure signal | Downstream owner |
|---|---|---|---|---|
| recall precision | did the consumer get the smallest relevant surface first? | inspect row, capsule, optional expand trace | full expansion or irrelevant object becomes default | `aoa-evals`, `aoa-sdk` |
| provenance fidelity | did source refs survive capture, review, corpus, and recall? | candidate refs, intake packet, object refs, generated row | compact recall hides source or stronger owner | `aoa-evals`, source repo |
| staleness handling | did cooled, superseded, retracted, or archived posture remain visible? | lifecycle fields, current recall status, audit event | old memory reads as current | `aoa-evals`, retention mechanic |
| contradiction handling | did unresolved tension remain explicit? | contradiction refs, replacement refs, audit walkback | summary invents a clean resolution | `aoa-evals`, source owners |
| permission leakage | did access or memory posture get misread as role rights? | access fields, agent boundary refs | memo grants or implies actor rights | `aoa-agents`, `aoa-evals` |
| over-promotion | did candidate, allowed, or bridge-ready memory become settled truth? | review state, promotion state, KAG lift status | candidate is treated as confirmed or lifted | `aoa-evals`, `aoa-kag`, source owner |
| hallucinated merge | did separate traces get fused without review? | provenance threads, merge-review records | consumer narrates one object from separate evidence | `aoa-evals`, memo review |
| abstention | did the consumer route outward when memo was not enough? | stronger owner stop-line and escalation note | memo answer replaces source truth | source owner, router, review |
| selective forgetting | did archive or retirement affect active recall without erasing history? | archive operation, audit event, historical recall path | archived memory keeps winning active recall | `aoa-evals`, retention mechanic |
| poisoning | did untrusted or injected experience stay candidate/quarantine until review? | write-path guard record, candidate state, review receipt | action-bearing text becomes durable memory | operational gate, `aoa-evals` |

The stable harness order is:

1. select one real object or candidate from each active source lane;
2. read inspect, capsule, and expand surfaces separately;
3. check the lenses above without producing a universal memory score;
4. write bounded eval reports in `aoa-evals`;
5. turn only review-accepted findings into memo candidates or lifecycle changes.

## Machine-readable Handoff Surface

The current schema-backed guardrail handoff surface is:

- `mechanics/consumer-handoff/parts/eval-guardrail-handoff/schemas/memory_eval_guardrail_pack.schema.json`
- `mechanics/consumer-handoff/parts/eval-guardrail-handoff/examples/memory_eval_guardrail_pack.example.json`

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
