# Agent Memory Posture Seam

## Purpose

This document defines the memo-side contract note that `aoa-agents` may rely on when reading from or writing toward `aoa-memo`.

It makes the shape of memory posture explicit without moving role policy into this repository.

## Boundary Rule

`aoa-memo` names the memory objects, scopes, lifecycle states, temperatures, and handoff fields that a right would apply to.

`aoa-agents` still owns:

- who receives a right
- when the right is granted
- what approvals are required
- how handoff posture is enforced

## What Memo Publishes

The memo layer may publish the following posture fields for agent-side consumption:

- object `kind`
- `scope`
- `access.access_class`
- `access.read_scopes`
- `access.write_scopes`
- `access.promotion_scopes`
- `lifecycle.review_state`
- `lifecycle.promotion_state`
- `trust.temperature`
- `trust.authority`
- `provenance.provenance_thread_id`
- `bridges.route_capsule_ref`

These fields let agent contracts talk about memory posture without hard-coding role policy inside `aoa-memo`.

## Consumer Contract

When `aoa-agents` consumes memo surfaces, it should be able to answer:

- what object kind is being touched
- which scope the object applies to
- what review or freeze posture the object already has
- whether the object is a raw event, a reviewed claim, a bridge candidate, or an audit trail
- which stronger source should be opened next if memory alone is insufficient

When an agent writes back into memo, the write should preserve:

- source refs
- provenance thread linkage where available
- explicit scope
- explicit review state
- policy decisions as outward refs rather than hidden role logic

## What Stays In `aoa-agents`

The following still belong in `aoa-agents` rather than here:

- read, write, promotion, and freeze rights
- actor identity and persona doctrine
- handoff and delegation posture
- policy-specific approval rules
- private or runtime-only memory posture

## Minimal Handoff Fields

The smallest useful memo-side handoff surface for agent consumers should include:

- source memory id
- object kind
- scope
- access class
- read scopes
- write scopes
- promotion scopes when present
- lifecycle review state
- trust temperature
- provenance thread id when present
- route capsule ref or stronger source refs for deeper inspection

These are memo-side descriptors, not grants.

## What This Seam Does Not Do

This seam does not:

- assign rights to a role
- define actor policy
- authorize freeze or promotion by presence of a field alone
- create a hidden agent runtime inside `aoa-memo`
- replace `aoa-agents` memory posture doctrine
