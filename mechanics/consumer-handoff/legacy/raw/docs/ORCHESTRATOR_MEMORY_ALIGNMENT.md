# Orchestrator Memory Alignment

## Purpose

This note defines how orchestrator-facing quest families align with `aoa-memo` without turning memo into class identity or live quest ownership.

Orchestrator class identity lives in `aoa-agents`.
`aoa-memo` only defines recall posture, inspect/capsule/expand expectations, and writeback boundaries for those classes.

## Router

The `router` class should stay inspect-first and capsule-second.

It may consume:

- inspect surfaces such as `generated/memory_object_catalog.min.json`
- capsule surfaces such as `generated/memory_object_capsules.json`
- bounded recall contracts that keep routing grounded without full expansion first

Router memory alignment stays entrypoint-shaped.
It does not turn memo into routing policy.

## Review

The `review` class should preserve:

- residual-risk notes
- closure notes
- provenance continuity around why a route closed, returned, or stopped

Review memory alignment stays recurrence-shaped.
It does not turn memo into the owner of closure verdicts.

## Bounded execution

The `bounded_execution` class should preserve:

- step-local recall
- handoff continuity
- the smallest useful recall pack before the next bounded step opens

Bounded execution memory alignment stays continuity-shaped.
It does not turn memo into runtime state or silent planning.

## Boundary rule

Memo stores evidence, provenance, recall posture, and recurrence.
Quests may point at memo surfaces, but they must not redefine orchestrator identity or make memo the owner of active quest state.
