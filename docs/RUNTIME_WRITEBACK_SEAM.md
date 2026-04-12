# RUNTIME WRITEBACK SEAM

## Purpose

This document defines the runtime-to-memo writeback seam for `aoa-memo`.

It does not turn `aoa-memo` into a runtime store or a hidden orchestration layer.
It defines the bounded contract that a future runtime may use when exporting selected state into the memo canon.

## Source Seed

Source seed ref:

- `seed_expansion/seed.aoa.agents-runtime-pack.v0.md#aoa-seed-r3-runtime-writeback-to-memo`

## Core Rule

Keep live scratchpad in runtime.

`aoa-memo` should receive only bounded exports or reviewed writeback candidates.
It should not become the main live state store for a running route.

## Boundary Split

- `aoa-agents` keeps role memory posture, memory rights, and writeback boundaries
- `aoa-playbooks` keeps checkpoint-shaped scenario meaning
- `aoa-memo` keeps object canon, lifecycle, writeback classes, and review rules
- `aoa-kag` keeps derived substrate and downstream lift work
- `abyss-stack` keeps runtime stores, checkpoint workers, and writeback plumbing

## Mapping To Preserve

- run scratchpad stays runtime-local
- checkpoint export becomes `state_capsule`
- approval and transition records become `decision`
- execution and review traces become `episode` and `audit_event`
- `distillation_pack` yields candidates for `claim`, `pattern`, and `bridge` after review

This is a mapping contract, not a promotion shortcut.

## Checkpoint To Memory Contract

The first structural surface for this seam is schema-backed and code-free:

- `schemas/checkpoint-to-memory-contract.schema.json`
- `examples/checkpoint_to_memory_contract.example.json`

The compact downstream read surface derived from that contract is:

- `generated/runtime_writeback_targets.min.json`
- `generated/runtime_writeback_intake.min.json`
- `generated/runtime_writeback_governance.min.json`

The checkpoint artifact remains `inquiry_checkpoint`.
It is not a new memory-object kind.
It stays a route artifact until a bounded export is written into the current memo canon.
Return-specific relaunch metadata stays inside `inquiry_checkpoint` as route-scoped structure and does not create a new writeback class.

The governance surface is intentionally narrow.
It checks only that the runtime writeback target map and the runtime writeback intake map remain aligned as one release-facing seam.
It does not become a governance verdict over the whole memo corpus.

Growth-refinery writeback remains a memo-side adjunct on top of this seam.
When reviewed lineage evidence warrants a durable memory object, reuse existing
`failure_lesson_memory_v1` and `recovery_pattern_memory_v1` surfaces rather
than introducing a new writeback family.

Shared-root Codex rollout follow-through reuses that same boundary.
Checked-in rollout history, drift windows, rollback windows, and derived
summaries may justify a bounded failure lesson or recovery pattern, but they do
not create a rollout-specific memo kind or move rollout authority into
`aoa-memo`.

## Trace And Restart Reuse

Reuse existing public surfaces where possible:

- `WitnessTrace` remains the reviewable trace export when a run needs step-level visibility
- `inquiry_checkpoint` remains the pause and relaunch container for long-horizon routes

This seam maps selected results from those surfaces into memo objects.
It does not replace those surfaces with a new hidden format.

## Distillation Posture

`distillation_pack` does not write settled truth directly.

Its output should be treated as:

- `claim` candidate
- `pattern` candidate
- `bridge` candidate

Those candidates still need provenance, temporal posture, and review before they become durable memo surfaces.

## Reference Scenarios

Use these as the primary reference scenarios for the seam:

- `AOA-P-0008 long-horizon-model-tier-orchestra`
- `AOA-P-0009 restartable-inquiry-loop`

The current checkpoint and witness examples remain useful memo-side precedents.
They do not move scenario ownership into this repository.

## What This Seam Does Not Do

This seam does not authorize:

- runtime scratchpad as durable memory canon
- direct freeze or promotion policy inside `aoa-agents`
- silent writeback that skips review posture
- a new memory-object family for runtime traces
- runtime implementation code inside `aoa-memo`

## Minimal Landing Slice

This landing slice stays intentionally small:

- one human-readable seam note
- one checkpoint-to-memory contract surface
- one schema-backed example
- no runtime database or worker implementation
- no direct canon promotion automation
- no changes to role rights owned by `aoa-agents`
