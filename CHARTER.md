# CHARTER

## Mission

`aoa-memo` is the explicit memory and recall layer of the AoA ecosystem.

Its job is to make memory objects, provenance threads, temporal posture, and recall surfaces explicit, reviewable, and bounded.

The repository exists so that AoA and ToS can remember without turning memory into hidden prompt residue, proof by vibes, or an unowned fog of context.

## Why this layer exists

AoA and ToS need a memory layer that is:

- explicit rather than hidden in prompts or agent folklore
- temporal rather than pretending to be timeless truth
- source-aware rather than free-floating summary
- reviewable rather than magical
- routeable rather than swollen
- compatible with downstream KAG lifts without becoming a graph platform itself

## Core rules

1. **Memory is not proof.** A memory object may preserve a past event, interpretation, or judgment. It does not automatically make that content authoritative, current, or sufficient.
2. **Events come before claims.** Capture what happened first. Consolidated claims come later.
3. **Provenance should stay visible where possible.** A useful memory object tells a reader where it came from and what stronger source should be inspected next.
4. **Temperature is not truth.** Hot memory is current, not necessarily reliable. Frozen memory is stable, not necessarily universal.
5. **Trust is multi-axial.** Confidence, authority, freshness, and salience should not be collapsed into one vague score.
6. **Graph lifts are downstream.** `aoa-memo` may define graph-ready faces and bridges, but `aoa-kag` owns normalized derived substrate work.
7. **Live runtime state belongs outside this repository.** Runtime stores, consolidation workers, storage layout, backup, and lifecycle jobs belong in `abyss-stack` and adjacent runtime systems.
8. **Role rights belong outside this repository.** Read, write, promotion, freeze, and handoff rights belong in `aoa-agents`.
9. **Routing belongs outside this repository.** `aoa-memo` may expose routeable surfaces, but `aoa-routing` owns dispatch logic.
10. **Source-authored knowledge world material belongs outside this repository.** `Tree-of-Sophia` owns source-authored texts, concepts, and lineage architecture.

## What this repository owns

`aoa-memo` is the source of truth for memory-layer meaning about:

- memory classes and memory-object kinds
- provenance threads
- temporal posture at the memory layer
- salience and memory-temperature posture
- recall and retrieval-oriented memory contracts
- public, reviewable memory registries, catalogs, capsules, and section surfaces
- schemas, validation rules, and examples for explicit memory objects

## What this repository does not own

`aoa-memo` should not become the primary home for:

- reusable techniques
- bounded execution workflows
- proof doctrine or verdict logic
- routing logic as such
- agent role contracts and persona boundaries
- scenario recipes and playbook composition
- infrastructure implementation details
- a hidden graph platform that quietly replaces neighboring layers
- generic notes with no memory contract

## Relationship to neighboring layers

- **`Agents-of-Abyss`** names the ecosystem, layer map, and federation rules.
- **`Tree-of-Sophia`** owns the living knowledge architecture and source-authored knowledge world.
- **`aoa-techniques`** owns reusable practice.
- **`aoa-skills`** owns bounded execution workflows.
- **`aoa-evals`** owns portable proof surfaces for bounded claims.
- **`aoa-routing`** owns navigation and dispatch.
- **`aoa-agents`** owns role contracts, handoff posture, and memory posture rights.
- **`aoa-playbooks`** owns recurring scenario composition.
- **`aoa-kag`** owns derived knowledge substrate and normalized graph-ready lifts.
- **`abyss-stack`** owns runtime, deployment, storage, lifecycle, and infra glue.

## Success criteria

`aoa-memo` is succeeding when:

- memory objects are explicit, small, and reviewable
- provenance and temporal posture are visible
- memory can route a reader toward stronger sources
- memory surfaces are compact enough for smaller models and deterministic tools
- neighboring repositories do not have to re-argue what memory is
- memory growth increases clarity rather than swelling the stack into context fog

## Current phase

This repository is in bootstrap.

The immediate goal is to establish doctrine, boundaries, the conceptual model, and the first routeable memory surfaces before adding heavier schema work or runtime integration.

## Editing posture

Prefer the smallest reviewable change that makes memory clearer.

A good change usually improves one or more of these questions:

- what happened?
- when did it happen?
- where did it come from?
- how stale or current is it?
- how should it be recalled?
- what stronger source should be checked next?

A bad change usually makes memory more absolute, less temporal, less reviewable, or more authoritative than it can honestly support.
