# Playbook Memory Scopes

## Purpose

This document defines memo-side guidance that `aoa-playbooks` may cite when a scenario needs bounded memory access.

It keeps memory requirements explicit without moving scenario composition into `aoa-memo`.

## Core Rule

Playbooks should ask memo for bounded recall modes and explicit scopes.

They should not assume a blank check to the whole memory layer.

## Required Inputs

A playbook-to-memo request should name:

- the active repo, project, workspace, or ecosystem scope
- whether the need is `working`, `episodic`, `semantic`, `procedural`, `lineage`, or `source_route`
- whether checkpoint continuity is required
- whether the playbook needs inspect surfaces only or full section expansion
- which stronger source should be preferred when memo is ambiguous

## Recommended Recall Modes

Use the current recall modes like this:

- `working` for relaunch, checkpoint recovery, or active state capsules
- `episodic` for event traces, approvals, failures, and audits
- `semantic` for doctrine, stable claims, and cross-session project memory
- `procedural` for repeated success or failure patterns
- `lineage` for ToS or bridge-heavy memory walks
- `source_route` when the playbook needs the strongest next source rather than memory-only answers

The default memo-side entrypoint for relaunch and checkpoint use is `examples/recall_contract.working.json`.
Return-oriented relaunch should prefer working recall plus explicit checkpoint continuity over widening the whole memo scope.

## Recommended Memory Scopes

Playbooks should request the smallest useful scope first:

- `thread` or `session` for local relaunch work
- `project` for repo-bounded doctrine, claims, and patterns
- `workspace` for neighboring-repo coordination
- `ecosystem` only when the scenario truly crosses AoA-wide surfaces
- `ToS node / lineage` only when the playbook explicitly needs source-linked knowledge-world relations

Scope expansion should be explicit and reviewable.

## Checkpoint And Writeback Use

Use the current memo canon like this:

- `inquiry_checkpoint` for pause and relaunch continuity
- `state_capsule` for bounded exported working state
- `episode` for what happened during the scenario
- `decision` for explicit gates or approvals
- `audit_event` for lifecycle transitions
- `provenance_thread` for the bounded backward-walk chain

When a playbook requests return, it should ask for checkpoint anchors and exported state surfaces, not a new memory family.

This guidance helps playbooks ask for memory.
It does not move playbook choreography into `aoa-memo`.

For the current working-memory recall entrypoint, see `examples/recall_contract.working.json`.

## What This Guidance Does Not Do

This guidance does not:

- define scenario bundles
- define execution choreography
- authorize promotion or freeze policy
- replace `aoa-playbooks`
- replace runtime checkpoint workers or storage
