# MEMORY OBJECT PROFILES

## Purpose

This document hardens the object canon of `aoa-memo`.

The base `memory_object` schema remains the shared envelope for all memory objects.
The profile layer adds per-kind contracts so the canon is not only named in doctrine but also machine-checkable by kind.

## Core rule

Use the schemas in two layers:

- `schemas/memory-objects/memory_object.schema.json` for the shared field families
- `schemas/memory-objects/memory_object_profile.schema.json` or a per-kind schema when validating a concrete memory object kind

This keeps the canon small while making each first-class kind explicit enough for downstream consumers to rely on.

## Why profiles exist

Without profiles, the repo can only say that a memory object exists.
It cannot say enough about what makes an `anchor` distinct from a `state_capsule`, or a `pattern` distinct from a `claim`.

Profiles make the current baseline more honest by saying:

- which posture is expected for each kind
- which fields are required for that kind to remain reviewable
- which kinds are still working-state exports versus durable memory
- where the next hardening pass should focus without moving policy into neighboring repos

## Profile entrypoint

The profile entrypoint is:

- `schemas/memory-objects/memory_object_profile.schema.json`

It selects the correct per-kind profile for:

- `anchor`
- `state_capsule`
- `episode`
- `claim`
- `decision`
- `pattern`
- `bridge`
- `audit_event`

## Per-kind posture

### `anchor`

Use for intentionally stable reference memory.

Profile posture:

- stable operating axis or doctrine seam
- temperature should stay `frozen` or other stable posture
- lifecycle should remain explicitly stabilized rather than raw
- should point toward a stronger source surface for inspection

### `state_capsule`

Use for exported working-state memory, not the live scratchpad itself.

Profile posture:

- must preserve `observed_at`
- should stay `hot` or `warm`
- should remain in captured or early review posture unless explicitly consolidated later
- should preserve the route or source surface that explains the capsule

### `episode`

Use for durable event memory.

Profile posture:

- must preserve `observed_at`
- should remain close to what happened
- should keep provenance visible even when later claims are derived from it

### `claim`

Use for consolidated memory-layer statements.

Profile posture:

- should not remain raw `captured` memory
- should preserve a route back to sources and episodes
- should stay distinct from proof and timeless truth

### `decision`

Use for explicit choices that should survive recall.

Profile posture:

- must point to the source or artifact that explains the choice
- should preserve scope and current review posture
- should remain distinct from generic notes or implicit preference drift

### `pattern`

Use for repeated procedural-experience memory.

Profile posture:

- should point back to more than one episode
- should remain memory about repeated experience, not a replacement for `aoa-techniques`
- should stay reviewable as observed regularity rather than universal law

### `bridge`

Use for outward-facing connection memory.

Profile posture:

- must preserve at least one outward bridge surface
- should remain candidate-oriented when the downstream lift is not finished
- should preserve provenance and stronger source routes

### `audit_event`

Use for lifecycle or governance changes that should remain inspectable as first-class memory objects.

Profile posture:

- must preserve `observed_at`
- must remain attached to a provenance thread
- should record meaningful change, not shadow-note noise

## Coverage matrix

The current profile-hardening pass uses these canonical schema/example pairs:

- `anchor` -> `schemas/memory-objects/anchor.schema.json` -> `examples/memory-objects/anchor.example.json`
- `state_capsule` -> `schemas/memory-objects/state_capsule.schema.json` -> `examples/memory-objects/state_capsule.example.json`
- `episode` -> `schemas/memory-objects/episode.schema.json` -> `examples/memory-objects/episode.example.json`
- `claim` -> `schemas/memory-objects/claim.schema.json` -> `examples/memory-objects/claim.example.json`
- `decision` -> `schemas/memory-objects/decision.schema.json` -> `mechanics/checkpoint/parts/approval-and-health-records/examples/checkpoint_approval_record.example.json`
- `pattern` -> `schemas/memory-objects/pattern.schema.json` -> `examples/memory-objects/pattern.example.json`
- `bridge` -> `schemas/memory-objects/bridge.schema.json` -> `memo/objects/bridges/2026/tos-lineage-kag-candidate/object.json` with `mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/bridge.kag-lift.example.json` retained as a teaching fixture
- `audit_event` -> `schemas/memory-objects/audit_event.schema.json` -> `examples/lifecycle/audit_event.supersession.example.json`

## Object Population Plan

Future corpus growth should fill real reviewed objects in this order so memory
does not become a fluent claim layer without events, audit, and route anchors.

| Object kind | First stable slots to fill | Why first | Usual source lanes |
|---|---|---|---|
| `episode` | first live end-to-end intake; first reviewed `.aoa` distillation; first host-memory export; first consumer recall run | events come before claims and give later memory evidence | local ports, `.aoa`, runtime, playbooks |
| `audit_event` | reviewed intake landing; lifecycle transition; access-plane drift; generated read-model drift; candidate rejection or quarantine | audit events let memory admit review, correction, and time | every lane |
| `state_capsule` | current `aoa-memo` organ readiness; port status snapshot; MCP/read-model currentness; host runtime health; consumer drift snapshot | state capsules make a moment inspectable without pretending to be timeless truth | memo, `abyss-stack`, host, SDK, routing |
| `decision` | foundation route placement; access-plane currentness route; consumer path alignment; lifecycle wave choice | decisions preserve why a route was chosen and what it rejected | memo, stack, agents, routing |
| `anchor` | memory organ boundary; reviewed corpus authority; access-plane boundary; center-route memory | anchors reduce repeated re-argument when later events need the same boundary | center route, memo doctrine, MCP boundary |
| `claim` | corpus density claim; recall currentness claim; port maturity claim; lifecycle readiness claim | claims consolidate repeated episodes while staying provenance-linked | stats, review, evals, memo doctrine |
| `pattern` | local port flow recurrence; stale path recurrence; consumer overread recurrence; reviewed closeout recurrence | patterns catch stable repetition without becoming proof or policy | playbooks, evals, `.aoa`, stats |
| `bridge` | ToS lineage to KAG candidate; MCP to reviewed corpus; agent posture to memory object; playbook run to recall object | bridges keep downstream handoff source-linked and weaker than downstream owner truth | ToS, KAG, stack, agents, playbooks |

## Boundary note

Profile schemas do not assign role rights, routing behavior, runtime storage policy, or eval verdict logic.

They only harden the memo-side shape of the current canon so neighboring repos can consume it without guessing.

## Next hardening pass

After the per-kind profile and trust/lifecycle layers are stable, the next contract-hardening pass should sharpen:

- object-facing generated recall surfaces built from the canon
