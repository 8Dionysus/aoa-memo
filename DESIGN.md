# aoa-memo System Design

## Role

`DESIGN.md` describes the system form of `aoa-memo`.

It is not the charter, roadmap, memory model, generated registry, or agent
instruction file.

It answers one question:

What shape should the memory and recall layer preserve while it grows as an
AoA organ?

## Design Thesis

`aoa-memo` is the explicit memory and recall layer of AoA.

It keeps memory object meaning source-authored, temporal, provenance-aware,
and reviewable while giving neighboring repositories enough public surfaces to
inspect, recall, lift, evaluate, route, and govern memory without absorbing it.

The memory object owns the trace.
Neighboring layers own their stronger work.
Generated surfaces help orientation.
Runtime stores remain outside this repository.

## Design as Appearance

The repository should appear as a memory atlas with a clear public front door:

- compact entry surfaces for humans and agents
- durable doctrine for memory meaning and boundaries
- explicit object, trust, lifecycle, and temperature contracts
- schema-backed examples that teach how memory stays reviewable
- generated companions for inspect, capsule, and expand flows
- local route cards that keep editing inside the nearest owner surface

A reader should be able to ask: what does this repo remember, how is it
bounded, what can be recalled, what source explains it, what changed over time,
and which neighboring owner takes the next stronger claim?

## Design as Anatomy

`aoa-memo` is composed of different source classes:

- root public entry and authority surfaces
- doctrine docs under `docs/`
- memo-side mechanics under `mechanics/`
- schema-backed memory and support contracts under `schemas/`
- public-safe examples under `examples/`
- generated memory companions under `generated/`
- builder, validator, and publication helpers under `scripts/`
- recurrence manifests, quests, and agent-facing companion surfaces

Each class supports the others. No class should silently steal another class's
authority.

## Design as Operation

A good memory-layer operation has:

- an entry route
- a named source surface
- one bounded memory question
- visible provenance or source refs
- explicit temporal and lifecycle posture
- a validation path
- a return route to stronger neighboring owners when memory is not enough

Memory grows well when every new surface makes recall, provenance, or boundary
honesty clearer than before.

## Design as Aim

The long aim is a memory layer that can support OS Abyss continuity without
becoming hidden context fog.

The repository should support:

- explicit memory objects instead of prompt residue
- compact recall surfaces for smaller models and deterministic tools
- provenance threads that let a reader walk backward
- lifecycle and temperature posture that make time visible
- bounded writeback and chronicle seams
- KAG-ready and eval-ready handoffs without becoming KAG or proof
- runtime consumption without becoming the runtime body

The layer succeeds when remembering increases reviewability instead of
inflating authority.

## Design Principles

### 1. Memory before mythology

The memory layer may preserve meaningful continuity, recurrence, and growth
signals. It must still answer what happened, when, from where, and with what
review posture.

### 2. Events before claims

Episodes and traces are the durable raw layer. Consolidated claims come later
and should remain connected to their evidence path.

### 3. Provenance before fluency

A smooth summary is weaker than a rough memory object with a source route.
Generated capsules may compress memory, but they must keep a path back to
authored surfaces.

### 4. Time stays visible

Temperature, freshness, lifecycle, supersession, retraction, and current recall
posture exist because memory changes over time. Current usefulness is not truth.

### 5. Memory is not proof

Memory can preserve an eval outcome, a judgment, or a review trace. It does not
become verdict logic. Proof belongs in `aoa-evals`.

### 6. Recall is not routing sovereignty

`aoa-memo` may expose routeable recall surfaces. Dispatch logic and route
compression policy belong in `aoa-routing`.

### 7. Graph faces are not graph ownership

`aoa-memo` may publish graph-ready faces and source-owned donor exports.
Normalized substrate formation belongs in `aoa-kag`.

### 8. Runtime remains outside

Live stores, retention workers, consolidation jobs, backup, restore, and secret
handling belong in runtime owners such as `abyss-stack`.

### 9. Agent rights stay outside

Read, write, promotion, freeze, and handoff rights belong in `aoa-agents`.
`aoa-memo` defines the memory object that those rights apply to.

### 10. Topology should reduce recall cost

New docs, districts, schemas, and generated companions should make it easier to
find the right memory surface. If a surface only preserves a session wave or
landing receipt, it needs a bounded home rather than a root-level spotlight.

## Good Design Feels Like

- a public reader can distinguish memory from proof
- an agent can find the nearest route card
- a memory object can find its provenance
- a generated file can find its source
- a stale object can find its current recall posture
- a bridge can find its downstream owner
- a repeatable adoption, governance, shape-guard, consumer-handoff, writeback,
  or retention move can find its mechanic, owner map, and legacy bridge
- a mechanic-adjacent artifact can tell whether it belongs in a root technical
  district or a package-local home
- a future contributor can find why the topology exists

## Bad Design Smells Like

- flat docs sprawl with no route map
- repeatable mechanics hidden as ordinary docs folders
- memory objects that read like workflows or verdicts
- generated files cited as source truth
- writeback surfaces pretending to be live ledgers
- Antifragility, Agon, Titan, adoption, governance, shape-guard,
  consumer-handoff, writeback, or retention notes without a local owner lane
- runtime language pretending this repo stores live memory
- role rights hidden inside memory schemas
- KAG exports widening into graph platform behavior

## Relationship to Other Root Surfaces

[README](README.md) introduces. [CHARTER](CHARTER.md) authorizes.
[ROADMAP](ROADMAP.md) points direction. [BOUNDARIES](docs/BOUNDARIES.md)
separates owner truth. [MEMORY_MODEL](docs/MEMORY_MODEL.md) defines the memory
conceptual model. [ROOT_SURFACE_LAW](docs/ROOT_SURFACE_LAW.md) governs root and
docs-root placement. [AGENTS](AGENTS.md) routes agents. [DESIGN.AGENTS](DESIGN.AGENTS.md)
holds the design form of the agent-facing layer. `DESIGN.md` holds the system
form of the memory layer.

## Use by Agents

Agents should consult this file when a change alters:

- repository shape
- root surfaces
- docs topology
- source versus generated authority
- memory-object and support-surface boundaries
- writeback, chronicle, recurrence, or bridge posture
- agent-facing layer design
- neighboring owner handoffs

This file does not override local owner truth. It tells agents what kind of
shape they are preserving.
