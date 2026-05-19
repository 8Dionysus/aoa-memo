# CHARTER

## Mission

`aoa-memo` is the explicit memory and recall layer of the AoA ecosystem.

Its job is to make memory objects, provenance threads, temporal posture, and recall surfaces explicit, reviewable, and bounded.

The repository exists so that AoA and ToS can remember without turning memory into hidden prompt residue, proof by vibes, or an unowned fog of context.

## Authority Boundary

This charter answers what `aoa-memo` may claim about the memory layer.

Operational editing routes live in [AGENTS](AGENTS.md). The memory-layer system
form lives in [DESIGN](DESIGN.md). The public memory canon map lives in
[MEMORY_INDEX](MEMORY_INDEX.md). Detailed doctrine lives in
[MEMORY_MODEL](docs/memory/MEMORY_MODEL.md), [BOUNDARIES](docs/boundaries/BOUNDARIES.md), and the
nearest mechanic package when a repeatable memo operation owns the surface.

This charter gives those routes their repository boundary; it does not replace
them.

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
- memo-side mechanics that preserve repeatable memory movement without taking
  stronger owner authority

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

## Memory Discipline

A memory claim is healthy when a reader can identify the object kind, time
posture, source route, provenance confidence, lifecycle state, and stronger
owner boundary without relying on private context.

Generated catalogs, capsules, indexes, and read models are companions. They may
route, compress, or expose memory for machines, but authored docs, schemas,
examples, mechanics, and validators keep authority.

Mechanics may prepare, gate, preserve, and route memory movement. They do not
turn candidate recall into proof, runtime action, role rights, route dispatch,
KAG substrate, playbook choreography, source-owner consent, or current truth.

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

This repository is in contract hardening.

The immediate goal is to harden doctrine, object canon, recall contracts, and bounded writeback/export seams without turning the repository into runtime infrastructure or a graph platform.

## Editing posture

Prefer the smallest reviewable change that makes memory clearer.

Before changing root posture, memory-canon boundaries, generated-companion
routes, or owner split, check:

1. this charter for repository authority
2. [DESIGN](DESIGN.md) for the system form being preserved
3. [MEMORY_INDEX](MEMORY_INDEX.md) for the current public memory map
4. [MEMORY_MODEL](docs/memory/MEMORY_MODEL.md) for conceptual shape
5. [BOUNDARIES](docs/boundaries/BOUNDARIES.md) for route-away rules
6. [ROOT_SURFACE_LAW](docs/root/ROOT_SURFACE_LAW.md) for root and docs-root placement
7. [mechanics](mechanics/README.md) when the change concerns repeatable memory movement
8. generated surfaces, builders, validators, and tests before claiming parity

A good change usually improves one or more of these questions:

- what happened?
- when did it happen?
- where did it come from?
- how stale or current is it?
- how should it be recalled?
- what stronger source should be checked next?

A bad change usually makes memory more absolute, less temporal, less reviewable, or more authoritative than it can honestly support.
