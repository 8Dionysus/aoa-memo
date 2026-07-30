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

## `codex_owner_orientation_v0`

The first concrete pack is an operator-invoked, D0/R1 Codex orientation
consumer. Its owner-authored profile, C11 policy, SDK compatibility pin,
memo-bundle schema, packet builder, and executable checks live under
`parts/orchestrator-recall-alignment/`.

The flow is deliberately split:

1. `aoa-sdk` admits exact C07, C11, model/prompt/provider, C18, and C19 pins
   and selects only confirmed, current `reviewed_corpus` cards.
2. `aoa-memo` validates the exact SDK plan schema and emits owner-valid C08
   and C09 inside a content-addressed delivery bundle.
3. `abyss-stack` may return that already-admitted bundle to the explicit
   caller and issue C20, but may not rerank, reselect, persist content, or
   manufacture memo-owned semantics.

`bounded` stops after inspect plus capsule. `high-fidelity` may add expand
inside its separate item/token budget. `off` and `fresh-start` produce no
memory. Every mode preserves visible omissions, lifecycle replacements and
contradictions, the strongest source route, and a verified no-memory
walkback. Raw `.aoa`, private ledgers, proactive delivery, exact tool
parameters, permission changes, memory writes, promotion, and effects are
forbidden.

## Ordinary Codex participation

`AOA-MEM-D-0083` keeps ordinary-session participation inside the existing
`aoa-memo` skill family:

```text
prompt-visible aoa-memo
  -> fast orient: one read-only brief, optional one bounded reviewed search
  -> current owner-source verification or silence
  -> deep recall only when exact memory meaning becomes material
```

The H0 hook is a separate observation contour, not a delivery contour. It
records coarse opportunities and completed `aoa_memo` tool-result stages while
leaving whether the session noticed, used, rejected, or benefited from memory
unknown. It does not inject a cue or packet and cannot substitute for
fresh-session selection tests or outcome review.

The memo-owned fragment is composed into native Codex hook configuration by
`abyss-stack`. It does not modify or depend on `aoa-session-memory`; the two
standalone hook families may coexist only through neutral configuration
composition. A later route-only cue is H2 and needs a separate policy. Direct
memory-packet injection is outside this contract.

## Boundary rule

Memo stores evidence, provenance, recall posture, and recurrence.
Quests may point at memo surfaces, but they must not redefine orchestrator identity or make memo the owner of active quest state.
