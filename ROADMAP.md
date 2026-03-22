# ROADMAP

## Direction

Build `aoa-memo` as the explicit memory and recall layer of AoA: small, reviewable, provenance-aware, routeable, and KAG-ready, without turning the repository into a runtime database, a routing monolith, or a graph platform.

## Current stage

`aoa-memo` is in bootstrap.

The repository has already named its role at the ecosystem level, but it still needs the doctrine, object canon, schemas, generated surfaces, and cross-repo contracts that will make the memory layer real and usable.

## North star

By `v1.0`, `aoa-memo` should make it possible to say:

- memory objects are explicit and bounded
- episodes, claims, patterns, anchors, and audit events are distinguished clearly
- provenance and temporal posture survive recall
- temperature, salience, confidence, and authority are not collapsed into one foggy signal
- `aoa-routing` can route into memo surfaces without copying their meaning
- `aoa-kag` can lift memory surfaces downstream without treating `aoa-memo` as a graph engine
- `aoa-agents` can govern memory rights without those rights being hidden inside the memory layer
- live storage and lifecycle machinery remain outside this repository

## Non-goals

This roadmap does **not** aim to turn `aoa-memo` into:

- a live memory database
- a generic note attic
- a graph platform
- a prompt archive
- a proof layer
- a routing engine
- a substitute for `Tree-of-Sophia`

## Guiding principles

- memory is not proof
- events come before claims
- provenance should stay visible
- temperature is not truth
- source repositories keep authored meaning
- graph lifts are downstream
- small public surfaces beat swollen universal objects

## Milestone sequence

### `v0.1` Doctrine baseline

**Goal:** establish the layer so its boundaries stop drifting.

**Deliverables:**

- `CHARTER.md`
- `docs/MEMORY_MODEL.md`
- `docs/BOUNDARIES.md`
- `ROADMAP.md`
- initial glossary of core memory terms

**Exit criteria:**

- the role of `aoa-memo` can be explained without code
- neighboring layers can tell what memory owns and what it does not own
- the object canon is named even if schemas are not final yet

### `v0.2` Object canon and schemas

**Goal:** turn doctrine into a machine-checkable memory shape.

**Deliverables:**

- `schemas/memory_object.schema.json`
- `schemas/provenance_thread.schema.json`
- `schemas/recall_contract.schema.json`
- `examples/` or `fixtures/` for core object kinds
- `scripts/validate_memo.py`

**Recommended first-class kinds:**

- `anchor`
- `state_capsule`
- `episode`
- `claim`
- `decision`
- `pattern`
- `bridge`
- `provenance_thread`
- `audit_event`

**Exit criteria:**

- core objects can be validated consistently
- examples make the doctrine concrete
- field families for identity, provenance, time, trust, lifecycle, and access are stable enough for downstream work

### `v0.3` Generated public surfaces

**Goal:** publish compact memory surfaces that tools and smaller models can inspect deterministically.

**Deliverables:**

- `generated/memo_registry.min.json`
- `generated/memory_catalog.json`
- `generated/memory_catalog.min.json`
- `generated/memory_capsules.json`
- `generated/memory_sections.full.json`

**Exit criteria:**

- memory objects are discoverable without loading the whole repository
- inspect and expand flows are feasible
- routeable surfaces exist without copying neighboring meaning into `aoa-memo`

### `v0.4` Provenance and lifecycle

**Goal:** make memory traceable and honest over time.

**Deliverables:**

- first-class provenance-thread docs and examples
- lifecycle docs covering confirmation, freeze, supersession, and retraction
- explicit `valid_from` / `valid_to` and supersession rules
- audit-event examples

**Exit criteria:**

- any nontrivial memory object can point back toward its trace
- stale memory can be recognized instead of silently lingering
- superseded or retracted memory remains inspectable as history

### `v0.5` Temperature and consolidation

**Goal:** separate current usefulness from truth and create a memory-quality pipeline.

**Deliverables:**

- doctrine for `hot`, `warm`, `cool`, `cold`, `frozen`
- `docs/MEMORY_TEMPERATURES.md`
- `docs/WRITEBACK_TEMPERATURE_POLICY.md`
- `schemas/decay_policy.schema.json`
- distinction docs for `confidence`, `authority`, `freshness`, `salience`
- online capture vs offline consolidation model
- examples of promotion and demotion flows

**Exit criteria:**

- memory can age without becoming incoherent
- capture stays cheap while long-term memory stays reviewable
- the repository has a shared language for salience and staleness

### `v0.6` Agents and playbooks integration

**Goal:** connect memory surfaces to actor contracts and scenario requirements without moving ownership.

**Deliverables:**

- cross-repo contract notes for `aoa-agents` memory posture
- `schemas/inquiry_checkpoint.schema.json`
- `examples/inquiry_checkpoint.example.json`
- suggested fields for read, write, promotion, and freeze rights
- playbook-facing guidance for required memory scopes and recall modes

**Exit criteria:**

- agents are not assumed to have magical rights
- scenario design can say what memory it needs
- `aoa-memo` stays object-centric while `aoa-agents` and `aoa-playbooks` own policy and composition

### `v0.7` KAG bridge and ToS bridge

**Goal:** make memory KAG-oriented and ToS-connected without making the memory layer itself a substrate engine.

**Deliverables:**

- chunk-face contract for memory inspection
- graph-face contract for downstream associative lifts
- ToS node and fragment bridge guidance
- `kag_lift_status` and related bridge fields
- examples of episode -> claim -> bridge -> KAG lift flow

**Exit criteria:**

- `aoa-kag` can consume memory exports cleanly
- ToS relations stay explicit and source-aware
- the memory layer remains source-preserving rather than graph-theatrical

### `v0.8` Evaluation and guardrails

**Goal:** make memory quality testable.

**Deliverables:**

- memory-focused eval ideas for `aoa-evals`
- tests for recall precision and provenance fidelity
- tests for staleness handling and contradiction handling
- tests for permission leakage and over-promotion
- tests for hallucinated memory merges

**Exit criteria:**

- memory quality is discussable in bounded checks, not just taste
- regressions in memory posture become visible

### `v1.0` Operational memory fabric boundary

**Goal:** finish the repository as the doctrine and surface layer, not the runtime body.

**Deliverables:**

- stable doctrine and schemas
- stable compact public surfaces
- clear cross-repo contracts
- validated examples
- documented handoff to runtime and downstream consumers

**Exit criteria:**

- `aoa-memo` is small but real
- neighboring repositories can build on it without guessing
- the runtime body can evolve in `abyss-stack` without turning the memory layer into infra soup

## Immediate execution order

The cleanest first pull request sequence is:

1. doctrine files
2. schemas and examples
3. generated surfaces and validation
4. provenance and lifecycle hardening
5. cross-repo integration notes

## Cross-repo dependencies

### `aoa-routing`

Needs a future `memo` kind that can ingest compact memo catalogs and route to source-owned memo capsules and sections.

### `aoa-agents`

Needs explicit memory posture fields for read scopes, write scopes, promotion rights, freeze rights, and handoff expectations.

### `aoa-kag`

Needs memory exports that are graph-ready but still source- and provenance-aware.

### `aoa-evals`

Needs bounded checks for recall precision, provenance fidelity, and stale-memory behavior.

### `abyss-stack`

Needs to own live stores, background consolidation jobs, retention, and backup posture.

### `Tree-of-Sophia`

Needs explicit refs and bridge contracts rather than duplication of source-authored material inside memory objects.

## Open design questions

These questions should stay visible while the layer is still young:

1. Which trust fields should be ordinal, and which should remain descriptive?
2. What should qualify an object for `frozen` state?
3. How much user-level memory should ever be public by default?
4. Which memory surfaces should be generated, and which should remain hand-authored?
5. At what point should retention policy move from doctrine to runtime implementation?

## Definition of done for the current pass

The current pass is done when a contributor can open the repository and understand:

- what memory means here
- which object kinds exist
- how temperature and trust posture work
- where memory stops and other layers begin
- what the next implementation milestones are
