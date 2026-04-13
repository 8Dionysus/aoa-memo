# ROADMAP

## Direction

Build `aoa-memo` as the explicit memory and recall layer of AoA: small, reviewable, provenance-aware, routeable, and KAG-ready, without turning the repository into a runtime database, a routing monolith, or a graph platform.

## Current stage

`aoa-memo` is in contract hardening.

The repository has already named its role, object canon, schemas, doctrine-facing generated surfaces, object-facing generated surfaces, lifecycle posture, temperature posture, runtime writeback seam, and first bridge/export and guardrail handoff surfaces.
Object canon, trust/lifecycle posture, and the separate object-facing generated family are now in place.
The active next slice is neighbor adoption so adjacent repos can consume the sharpened memo contracts without moving routing, role policy, graph normalization, or verdict logic into this repository.
The first router-first adoption package formalizes additive inspect -> capsule -> expand consumption across the doctrine and object-facing recall families without changing memo ownership.
The first recurrence-support landing makes checkpoint relaunch anchors and return-ready working recall explicit without changing memo ownership.
The first downstream eval adoption wave is now explicitly narrowed to recall precision, provenance fidelity, and staleness so `aoa-evals` can pilot memo proof without pretending to cover every guardrail focus at once.
The current KAG-facing adoption slice now publishes `generated/kag_export.min.json` as one source-owned memo export for `aoa-kag` readiness without widening the live federation spine or `aoa-routing` ABI.
The pre-Agon readiness holding map in `docs/PRE_AGON_MEMORY_READINESS.md` now
maps future scar, delta, retention, and recall pressure back to existing memo
objects without planting Agon, creating a live ledger, changing schemas, or
moving proof, graph lift, navigation, role authority, or runtime retention into
`aoa-memo`.

The current `v0.2.1` release line also already carries:
- checkpoint recall follow-through and lineage-aware growth-refinery writeback surfaces through `docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md`, `docs/GROWTH_REFINERY_WRITEBACK.md`, and `docs/QUEST_CHRONICLE_WRITEBACK.md`
- runtime writeback landing, intake, and governance surfaces through `generated/runtime_writeback_targets.min.json`, `generated/runtime_writeback_intake.min.json`, `generated/runtime_writeback_governance.min.json`, and `docs/RUNTIME_WRITEBACK_SEAM.md`
- rollout, rollback-followthrough, component-refresh, and self-agency continuity support through `examples/recovery_pattern_memory.rollback_followthrough.example.json`, `examples/recovery_pattern_memory.component_refresh.example.json`, `docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md`, and `examples/provenance_thread.self-agency-continuity.example.json`
- Phase Alpha writeback routing and owner-local live receipt publication through `generated/phase_alpha_writeback_map.min.json` and `scripts/publish_live_receipts.py`
- pre-Agon memory readiness through `docs/PRE_AGON_MEMORY_READINESS.md`

The near-term risk is roadmap drift: checkpoint recall, runtime writeback,
growth-refinery writeback, and continuity writeback are already shipped
memory-layer surfaces and should stay visible here without turning memory into
proof, routing, or live runtime authority.

## Current contract-hardening waves

Within the current contract-hardening stage, the cleanest wave order is:

1. **Object canon hardening**
   Add per-kind memory-object profiles, first-class example coverage for every shipped kind, and validator coverage for the full canon.
2. **Trust and lifecycle hardening**
   Tighten ordinal-versus-descriptive trust posture, freeze criteria, contradiction posture, and current-entrypoint semantics without collapsing memory into proof.
3. **Object-facing generated surfaces**
   Publish a separate generated family for actual memory objects and profile-backed example bundles without breaking doctrine-first catalogs.
4. **Neighbor adoption**
   Let `aoa-routing`, `aoa-agents`, `aoa-kag`, and `aoa-evals` consume the sharpened memo contracts without moving their logic into this repository.

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
- `generated/memory_object_catalog.json`
- `generated/memory_object_catalog.min.json`
- `generated/memory_object_capsules.json`
- `generated/memory_object_sections.full.json`

**Exit criteria:**

- doctrine and curated memory objects are discoverable without loading the whole repository
- inspect and expand flows are feasible
- routeable doctrine and object surfaces exist without copying neighboring meaning into `aoa-memo`

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

- `docs/AGENT_MEMORY_POSTURE_SEAM.md`
- `docs/PLAYBOOK_MEMORY_SCOPES.md`
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

- `docs/KAG_TOS_BRIDGE_CONTRACT.md`
- `docs/KAG_SOURCE_EXPORT.md`
- `schemas/memory_chunk_face.schema.json`
- `schemas/memory_graph_face.schema.json`
- chunk-face contract for memory inspection
- graph-face contract for downstream associative lifts
- `generated/kag_export.min.json`
- ToS node and fragment bridge guidance
- `kag_lift_status` and related bridge fields
- examples of chunk-face and graph-face export
- examples of episode -> claim -> bridge -> KAG lift flow

**Exit criteria:**

- `aoa-kag` can consume memory exports cleanly
- `aoa-kag` can validate the published source-owned memo donor export without activating it in the live federation spine yet
- ToS relations stay explicit and source-aware
- the memory layer remains source-preserving rather than graph-theatrical

### `v0.8` Evaluation and guardrails

**Goal:** make memory quality testable.

**Deliverables:**

- `docs/MEMORY_EVAL_GUARDRAILS.md`
- `schemas/memory_eval_guardrail_pack.schema.json`
- `examples/memory_eval_guardrail_pack.example.json`
- memory-focused eval ideas for `aoa-evals`
- first narrow downstream diagnostic pilot for recall precision, provenance fidelity, and staleness
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

- `docs/OPERATIONAL_BOUNDARY.md`
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
4. provenance, lifecycle, and temperature hardening
5. cross-repo integration notes
6. bridge/export and guardrail surfaces
7. operational boundary freeze

## Cross-repo dependencies

### `aoa-routing`

Already consumes the live `memo` kind, compact memo catalogs, router-ready doctrine recall contracts, and the current parallel object-facing recall family.

Future routing work should keep those memo-facing hints additive, source-owned, and bounded rather than turning `aoa-routing` into memo authority.
The current memo-side adoption package now makes the capsule step explicit between inspect and full expansion for both doctrine and object-facing semantic or lineage recall.

### `aoa-agents`

Needs explicit memory posture fields for read scopes, write scopes, promotion rights, freeze rights, and handoff expectations.

### `aoa-kag`

Needs memory exports that are graph-ready but still source- and provenance-aware.
The current next move is publish-only plus consumer readiness, not live federation activation.

### `aoa-evals`

Needs bounded checks for recall precision, provenance fidelity, and stale-memory behavior.
The first adoption wave should stay diagnostic and triad-scoped before the rest of the guardrail focuses are pulled into downstream proof bundles.

### `abyss-stack`

Needs to own live stores, background consolidation jobs, retention, and backup posture.
Future Agon retention checks should keep their durable memo evidence bounded to
`episode` or `audit_event` plus lifecycle and recall posture, while live
retention workers stay in `abyss-stack`.

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
- how agent, playbook, KAG, and eval consumers should touch memo without taking ownership from their source repos
- where memory stops and other layers begin
- what the next implementation milestones are
