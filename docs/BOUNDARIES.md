# BOUNDARIES

## Purpose

This document defines what belongs in `aoa-memo`, what should stay in neighboring AoA or ToS repositories, and how memory-layer surfaces may connect outward without swallowing the stack.

## Source-of-truth rule

`aoa-memo` is the source of truth for **explicit memory-layer meaning**.

It is not the source of truth for authored knowledge, execution, proof, routing, agent roles, scenario composition, or runtime infrastructure.

## What belongs here

`aoa-memo` should hold public, reviewable objects and docs that clarify memory-layer meaning, such as:

- memory-object kinds and their field families
- provenance-thread structure
- temporal posture and validity-window doctrine
- salience and memory-temperature doctrine
- recall contracts and recall-mode docs
- generated memory registries, catalogs, sections, and capsules
- memory-object examples and validation surfaces
- docs explaining promotion, supersession, retraction, and freeze posture

This repository is the right place for memory **about** work, not necessarily the work itself.

## What should stay outside

### `Tree-of-Sophia`

Keep the following outside `aoa-memo` and in `Tree-of-Sophia`:

- source-authored texts and fragments
- key terms, theses, and semantic fields as canonical knowledge artifacts
- lineage maps and intellectual inheritance structure
- time-and-place framing for civilizational knowledge nodes

`aoa-memo` may point to ToS nodes. It should not replace the ToS knowledge world.

### `aoa-techniques`

Keep reusable practice and method doctrine there:

- techniques
- heuristics
- reusable operating patterns
- practice-oriented abstractions

A memory object may say a technique was used or failed. The technique itself belongs elsewhere.

### `aoa-skills`

Keep bounded execution meaning there:

- workflows
- task bundles
- execution recipes
- do-this-next structures

A memory object may preserve what happened in an execution. The execution contract stays outside.

### `aoa-evals`

Keep portable proof surfaces there:

- eval bundles
- verdict logic
- bounded proof methods
- pass/fail or evidence-oriented criteria

Memory may preserve an eval outcome. That does not make the memory object the proof surface itself.

### `aoa-routing`

Keep dispatch logic there:

- pick / inspect / expand routing logic
- next-object navigation logic
- route compression for smaller models
- deterministic dispatch heuristics

`aoa-memo` may expose routeable surfaces, but it should not silently become the router.

### `aoa-agents`

Keep role and memory rights there:

- read rights
- write rights
- promotion rights
- freeze rights
- handoff posture
- persona or role doctrine

`aoa-memo` may define what a right would apply to. It should not define who has that right.

### `aoa-playbooks`

Keep recurring scenario composition there:

- scenario bundles
- repeated situation doctrine
- handoff and execution choreography

Memory objects may be used by playbooks. They do not become playbooks by proximity.

### `aoa-kag`

Keep derived knowledge substrate work there:

- normalized node and edge lifts
- graph-oriented derivation
- retrieval substrate adapters
- framework-facing graph-ready structures

`aoa-memo` may define graph-ready faces and bridges. It should not grow into the downstream graph substrate.

### `abyss-stack`

Keep runtime and operational machinery there:

- live storage backends
- consolidation workers
- lifecycle jobs
- deployment surfaces
- backup and restore posture
- runtime memory plumbing

The repository `aoa-memo` should remain inspectable doctrine plus compact surfaces, not runtime state.

## Safe outward links

The memory layer may safely link outward through:

- `source_refs`
- `episode_refs`
- `provenance_thread_id`
- `tos_refs`
- `skill_refs`
- `eval_refs`
- route capsule references
- canonical repository links

These links should make stronger sources easier to inspect, not harder.

## Anti-patterns

Treat the following as warning signs:

- a memory object that looks like a workflow spec
- a memory object that acts like a verdict with no evidence path
- a memory doc that rewrites ToS node meaning instead of linking to it
- a memory registry that becomes a hidden graph engine
- a memory field that implies authority, permanence, or role rights without saying so explicitly
- public memory objects that smuggle runtime secrets or private notes

## Boundary test

A proposed addition probably belongs in `aoa-memo` if it answers all or most of these:

- Is it explicit memory-layer meaning?
- Does it preserve event, claim, provenance, temporal posture, salience, or recall behavior?
- Is it reviewable as a public object or contract?
- Would storing it here avoid hidden context fog?
- Does it still point toward stronger canonical sources when needed?

A proposed addition probably belongs elsewhere if it is mainly:

- authored knowledge
- technique
- workflow
- proof
- routing
- role policy
- runtime implementation

## Doctrine in one line

`aoa-memo` remembers. It does not pretend to be the whole organism.
