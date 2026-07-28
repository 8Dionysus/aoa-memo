# Orchestrator Memory Alignment

## Purpose

This note defines how orchestrator-facing quest families align with `aoa-memo` without turning memo into class identity or live quest ownership.

Orchestrator class identity lives in `aoa-agents`.
`aoa-memo` only defines recall posture, inspect/capsule/expand expectations, and writeback boundaries for those classes.

## Router

The `router` class should stay inspect-first and capsule-second.

It may consume:

- inspect surfaces such as `generated/memory-objects/memory_object_catalog.min.json`
- capsule surfaces such as `generated/memory-objects/memory_object_capsules.json`
- bounded recall contracts that keep routing grounded without full expansion first

Router memory alignment stays entrypoint-shaped.
It does not turn memo into routing policy.

Router recall packs use this route:

| Step | Surface | Output |
|---|---|---|
| inspect | `generated/memory-objects/memory_object_catalog.min.json` filtered by repo, kind, `source_kind`, and recall posture | bounded object ids and owner refs |
| capsule | `generated/memory-objects/memory_object_capsules.json` for matched ids | short source-linked memory context |
| expand | object section or source doc only when route ambiguity remains | route evidence, not dispatch policy |
| stronger owner | `aoa-sdk` for dispatch and the source repo for meaning | next owner route |

## Review

The `review` class should preserve:

- residual-risk notes
- closure notes
- provenance continuity around why a route closed, returned, or stopped

Review memory alignment stays recurrence-shaped.
It does not turn memo into the owner of closure verdicts.

Review recall packs use this route:

| Step | Surface | Output |
|---|---|---|
| inspect | object catalog rows, intake receipts, audit events, and lifecycle posture | closure and residual-risk candidates |
| capsule | object capsules with current recall and provenance posture | review context without full corpus expansion |
| expand | object bundle, audit walkback, provenance thread, or eval report | evidence for close, return, or stop |
| stronger owner | `aoa-evals` for verdicts and source repo for acceptance | review result or memo candidate |

## Bounded execution

The `bounded_execution` class should preserve:

- step-local recall
- handoff continuity
- the smallest useful recall pack before the next bounded step opens

Bounded execution memory alignment stays continuity-shaped.
It does not turn memo into runtime state or silent planning.

Bounded-execution recall packs use this route:

| Step | Surface | Output |
|---|---|---|
| inspect | object catalog row and recall contract | smallest relevant memory reference |
| capsule | capsule with source refs and current recall posture | step-local context |
| expand | full object or source route only if the step cannot proceed safely | bounded evidence |
| stronger owner | `aoa-agents` for rights, `aoa-playbooks` for scenario, runtime owner for action | next bounded route |

## Pack Card

Each concrete pack should name:

- `pack_id`
- `consumer_class`
- `memory_question`
- `inspect_surface`
- `capsule_surface`
- `expand_surface`
- `required_object_refs`
- `allowed_source_kinds`
- `lifecycle_filters`
- `stronger_owner_stop_lines`
- `writeback_candidate_route`

## Boundary rule

Memo stores evidence, provenance, recall posture, and recurrence.
Quests may point at memo surfaces, but they must not redefine orchestrator identity or make memo the owner of active quest state.
