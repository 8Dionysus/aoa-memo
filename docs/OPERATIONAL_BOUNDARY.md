# Operational Boundary

## Purpose

This document fixes the v1-facing boundary of `aoa-memo` as doctrine plus compact public surfaces.

It makes the repository stable enough for neighboring repos to consume without turning `aoa-memo` into runtime memory infrastructure.

## Stable Public Boundary

The stable public boundary of this repository consists of:

- doctrine docs that define memory meaning, provenance, lifecycle, temperature, writeback, bridges, guardrails, and boundaries
- schema-backed memory and contract surfaces
- a doctrine generated family for layer-meaning inspect and expand surfaces
- an object generated family for curated memory-object inspect and expand surfaces
- reviewed examples that show how the layer is meant to be used

These are the public review surfaces a consumer should rely on.
`provenance_thread`, `witness_trace`, `inquiry_checkpoint`, and checkpoint contracts remain explicit support surfaces in this boundary, not a separate generated family.
`inquiry_checkpoint` may carry bounded `return_pack` metadata for relaunch, but it remains a route artifact rather than a new durable memory-object family.

## Consumer Contracts

### `aoa-routing`

Consume compact generated surfaces and recall contracts.
Use the doctrine family for layer meaning and the object family for object-first inspect/expand.
Keep dispatch logic and route compression policy outside this repository.

### `aoa-agents`

Consume object kind, scope, lifecycle, access posture, provenance linkage, and route refs.
Use the object family when the task is posture lookup over curated memory objects, and the doctrine family when the task is layer interpretation.
Keep rights policy, handoff posture, and actor doctrine outside this repository.

### `aoa-kag`

Consume bridge objects, chunk faces, graph faces, and provenance-aware exports.
Keep normalized substrate formation and framework adapters outside this repository.

### `abyss-stack`

Consume writeback seams and schema-backed export contracts.
Runtime may consume checkpoint return-pack refs as relaunch aids, but retry policy and rebuild mechanics remain outside this repository.
Keep live stores, background jobs, retention, backups, and restore posture outside this repository.

## What Runtime Owns

Runtime and operations remain outside `aoa-memo`, including:

- live state stores
- checkpoint workers
- consolidation jobs
- background lift jobs
- retention machinery
- secret handling
- deployment posture

## What This Boundary Freezes

This boundary freezes these layer rules:

- memory is not proof
- events come before claims
- authored/core memory remains inspectable
- graph lifts stay downstream
- role rights stay outside the memory layer
- runtime storage and jobs stay outside the repository
- cross-repo consumers rely on explicit public surfaces rather than hidden prompt residue

## What It Does Not Freeze

This boundary does not freeze:

- specific runtime implementation choices
- downstream graph normalization details
- role policy in `aoa-agents`
- scenario choreography in `aoa-playbooks`
- verdict logic in `aoa-evals`
- authored knowledge structure in Tree of Sophia

## One-line Rule

`aoa-memo` is the stable memory-layer boundary that neighboring repos may build on without guessing, but it is still not the runtime body.
