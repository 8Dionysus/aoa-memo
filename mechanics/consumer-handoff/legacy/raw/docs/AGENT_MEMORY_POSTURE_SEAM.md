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
- `scope_classes`
- `access.access_class`
- `access.read_scopes`
- `access.write_scopes`
- `access.promotion_scopes`
- `lifecycle.review_state`
- `lifecycle.current_recall.status`
- `lifecycle.promotion_state`
- `trust.temperature`
- `trust.authority_kind`
- `trust.authority`
- `provenance.provenance_thread_id`
- `bridges.route_capsule_ref`

These fields let agent contracts talk about memory posture without hard-coding role policy inside `aoa-memo`.

`scope` remains the concrete namespaced object identifier list such as `thread:contract-hardening` or `repo:aoa-memo`.
`scope_classes` is the derived class list that agent-side contracts may compare against `allowed_recall_scopes` or governed self-checkpoint `memory_scope` without parsing object-local identifiers.

## Consumer Contract

When `aoa-agents` consumes memo surfaces, it should be able to answer:

- what object kind is being touched
- which scope identifiers the object applies to
- which scope classes those identifiers reduce to
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
- scope classes
- access class
- read scopes
- write scopes
- promotion scopes when present
- lifecycle review state
- current recall status
- trust temperature
- authority kind
- provenance thread id when present
- route capsule ref or stronger source refs for deeper inspection

These are memo-side descriptors, not grants.

For compact object-first inspection, the current memo-side public surface is:

- `generated/memory_object_catalog.min.json` for inspect
- `generated/memory_object_sections.full.json` for expansion

The doctrine family remains separate and continues to answer layer-meaning questions rather than object-level posture lookup.

## What This Seam Does Not Do

This seam does not:

- assign rights to a role
- define actor policy
- authorize freeze or promotion by presence of a field alone
- create a hidden agent runtime inside `aoa-memo`
- replace `aoa-agents` memory posture doctrine
