# Recurrence Memory Support Surfaces

## Purpose

This document defines how `aoa-memo` supports the AoA recurrence principle without becoming the router, the runtime body, or the authority layer for actor rights.

The memo layer can help a route return.
It cannot decide whether return is permitted, which tier owns the next move, or how many retries a runtime may spend.

## Boundary Rule

`aoa-memo` may publish reviewable surfaces that help a route recover its last valid axis.

It must not:

- become the live scratchpad store
- become the dispatch layer
- become the role-rights layer
- create a new `return_memory` family that duplicates the current canon

Within the federation:

- `Agents-of-Abyss` owns recurrence as doctrine
- `aoa-agents` owns return as a handoff and transition move
- `aoa-playbooks` owns scenario-level return posture
- `abyss-stack` owns runtime rebuild policy and return-event logging
- `aoa-memo` owns the reviewable traces and anchors those layers may use

## Memo-Side Surfaces That Already Support Recurrence

### 1. `inquiry_checkpoint`

This is the primary pause-and-relaunch artifact.

It already holds the route question, evidence refs, contradiction refs, resolved decisions, open questions, witness refs, memory deltas, canon deltas, restart count, and review posture.

For recurrence, this remains the main relaunch pack.
It stays a route artifact, not a durable memory-object kind.

### 2. Working recall contracts

The existing working recall family already matches checkpoint continuity and relaunch use:

- doctrine-first working recall
- object-facing working recall

These remain the default memo-side entrypoints when a route needs compact re-entry anchors.

### 3. `state_capsule`

A return should not rehydrate from hidden scratchpad residue when a bounded exported working-state surface exists.

`state_capsule` is the right memo-side landing for a reviewable export of working state.

### 4. `decision`

An explicit return, reroute, or re-entry gate should survive as a first-class decision when it matters beyond one ephemeral run.

This does not mean every retry becomes durable memory.
It means the meaningful governed return events already have a memo-side home.

### 5. `episode` and `audit_event`

Drift, failure, review transitions, supersession, and restart-significant observations should survive as episodes or audit events when they affect later recall posture.

### 6. `anchor`

A route often needs one deliberately stable reference point during recovery.
The current object canon already has `anchor`.
Use it for stabilized reference points.
Do not invent a separate return-only object family.

### 7. `provenance_thread`

When recovery needs a bounded backward walk, the provenance thread is the right memo-side chain.
It keeps recurrence reviewable without turning memo into a graph runtime.

### 8. `checkpoint_to_memory_contract`

The current writeback seam already covers the return pathway:

- checkpoint export -> `state_capsule`
- transition record -> `decision`
- execution trace -> `episode`
- review trace -> `audit_event`

No new writeback class is required for this landing.

## Minimal Landing

### A. Add optional `return_pack` to `inquiry_checkpoint`

The checkpoint may carry compact relaunch metadata:

- which anchors remain valid
- which refs should be used for re-entry
- what bounded re-entry note should guide the next pass

This keeps recurrence-specific support inside the existing relaunch artifact instead of inventing a separate object family.

### B. Add optional return-support fields to recall contracts

The recall contract model stays mode-based.
It does not gain a new recall mode called `return`.

Instead, a working recall contract may declare whether it supports checkpoint continuity and which kinds make good return anchors.

That keeps return subordinate to current recall semantics rather than turning it into a new memory taxonomy.

### C. Keep generated surfaces unchanged

The current object catalog and object sections are already suitable for return-oriented inspection when the following kinds are present:

- `state_capsule`
- `decision`
- `episode`
- `audit_event`
- `anchor`

This landing does not require a new generated family.

## Consumer Rules

### `aoa-agents`

May consume memo-side descriptors for checkpoint, anchor, state export, and decision posture.
Must keep actor rights, retry rules, and role policy outside `aoa-memo`.

### `aoa-playbooks`

May ask for working recall with checkpoint continuity.
Must keep scenario choreography outside `aoa-memo`.

### `abyss-stack`

May export bounded runtime state into the current memo canon through the writeback seam.
May consume checkpoint and anchor refs as relaunch aids.
Must keep live stores, retry loops, and rebuild mechanics outside `aoa-memo`.

### `aoa-routing`

May point back to memo contracts and public object surfaces.
Must not reinterpret memo truth or checkpoint semantics.

## Anti-Patterns

Treat these as boundary failures:

- adding a new `return_memory` object kind
- storing raw runtime scratchpad as return canon
- letting a checkpoint field silently grant role rights
- using memo to decide dispatch or tier escalation
- replacing a stable source surface with memo summary when stronger authority exists

## One-Line Rule

`aoa-memo` supports recurrence by publishing bounded relaunch anchors and reviewable traces, not by becoming the router, the runtime body, or the policy owner.
