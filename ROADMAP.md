# aoa-memo Roadmap

This roadmap tracks current direction for `aoa-memo` as the public memory and
recall layer of AoA.

Use it when the question is "what repo-level direction should shape the next
change?", not "which memory object, mechanic part, or generated companion
should I open?"

## Authority

Root [ROADMAP](ROADMAP.md) owns repo-level direction, memory-layer horizons,
current contract-hardening pressure, cross-repo handoff pressure, root
source-of-truth pressure, and concrete future triggers that belong to this
repository.

It does not own memory object semantics by itself, generated registry truth,
mechanic-local roadmaps, checked mechanic landings, release history, quest
state, proof verdicts, runtime implementation, route dispatch, role policy, or
sibling-repository implementation direction.

Use the stronger surface when the change is narrower:

- repository boundary: [CHARTER](CHARTER.md)
- memory canon map: [MEMORY_INDEX](MEMORY_INDEX.md)
- memory model: [MEMORY_MODEL](docs/memory/MEMORY_MODEL.md)
- root and docs placement: [ROOT_SURFACE_LAW](docs/root/ROOT_SURFACE_LAW.md)
- mechanic-local future pressure: `mechanics/<slug>/ROADMAP.md`
- checked mechanic landings: `mechanics/<slug>/LANDING_LOG.md`
- durable obligations: [QUESTBOOK](QUESTBOOK.md) and [quests](quests/)
- released repository history: [CHANGELOG](CHANGELOG.md)

## Update Rule

Update this roadmap only when a change moves repo-level direction, memory
canon posture, root source-of-truth posture, cross-repo handoff posture,
mechanics-to-memory interface, or a concrete future trigger for this
repository.

Do not update it for a local mechanic landing, generated refresh, release
note, quest lifecycle move, package-local artifact relocation, or validator
maintenance unless that local change alters repo-level direction.

## Direction

Build `aoa-memo` as the explicit memory and recall layer of AoA: small, reviewable, provenance-aware, routeable, and KAG-ready, without turning the repository into a runtime database, a routing monolith, or a graph platform.

## Current stage

`aoa-memo` is in contract hardening.

The repository has already named its role, object canon, schemas, doctrine-facing generated surfaces, object-facing generated surfaces, lifecycle posture, temperature posture, runtime writeback seam, and first bridge/export and guardrail handoff surfaces.
Object canon, trust/lifecycle posture, and the separate object-facing generated family are now in place.
The active next slice is neighbor adoption so adjacent repos can consume the sharpened memo contracts without moving routing, role policy, graph normalization, or verdict logic into this repository.
The first router-first adoption package formalizes additive inspect -> capsule -> expand consumption across the doctrine and object-facing recall families without changing memo ownership.
The first checkpoint mechanic landing makes checkpoint relaunch anchors,
carry packets, approval and health records, and checkpoint-to-memory mappings
explicit without changing execution, runtime, role, proof, route, or source
ownership.
The first lineage-harvest landing makes pattern-lineage memory candidates and
federation harvest stop-lines explicit without granting memo proof, KAG
promotion, ToS canon, stats certification, runtime truth, or source-owner
consent.
The first downstream eval adoption pass is now explicitly narrowed to recall precision, provenance fidelity, and staleness so `aoa-evals` can pilot memo proof without pretending to cover every guardrail focus at once.
The current KAG-facing adoption slice now publishes `mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json` as one source-owned memo export for `aoa-kag` readiness without widening the live federation spine or `aoa-routing` ABI.
Governance authority-boundary artifacts now live at their owning parts:
`mechanics/governance/parts/governance-boundary/`,
`mechanics/governance/parts/federation-boundary/`,
`mechanics/governance/parts/install-and-certification-boundary/`, and
`mechanics/governance/parts/precedent-and-stay-order/`, keeping governance
memory operational without making `aoa-memo` a council, release, proof, or
runtime authority.
The memory readiness boundary map in `mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md` now
maps future durable-consequence, delta, retention, and recall pressure back to
existing memo objects without planting a future protocol, creating a live
ledger, changing schemas, or moving proof, graph lift, navigation, role
authority, or runtime retention into `aoa-memo`.

The current `v0.2.3` release line also already carries:
- checkpoint recall follow-through and lineage-aware growth-refinery writeback surfaces through `mechanics/checkpoint/docs/CHECKPOINT_MEMORY_BOUNDARY.md`, `mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md`, `mechanics/writeback/docs/GROWTH_REFINERY_WRITEBACK.md`, and `mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md`
- pattern-lineage harvest memory through `mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md`, `mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/schemas/pattern_lineage_memory_entry_v1.json`, and `mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/examples/pattern_lineage_memory_entry.example.json`
- runtime writeback landing, intake, and governance surfaces through `mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json`, `mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json`, `mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json`, and `mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md`
- rollout, rollback-followthrough, component-refresh, and self-agency continuity support through `mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.rollback_followthrough.example.json`, `mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.component_refresh.example.json`, `mechanics/writeback/docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md`, `mechanics/writeback/parts/growth-and-continuity/examples/provenance_thread.self-agency-continuity.example.json`, `mechanics/writeback/parts/growth-and-continuity/examples/decision.self-agency-reanchor-window.example.json`, and `mechanics/writeback/parts/growth-and-continuity/examples/state_capsule.self-agency-continuity-relay.example.json`
- Phase Alpha writeback routing and owner-local live receipt publication through `mechanics/writeback/parts/growth-and-continuity/generated/phase_alpha_writeback_map.min.json` and `mechanics/writeback/parts/receipt-publication-regression/scripts/publish_live_receipts.py`
- memory readiness boundary through `mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md`
- Questbook read-model projection placement through `mechanics/questbook/parts/quest-read-model-projections/README.md`,
  keeping `generated/quests/quest_catalog.min*.json` and
  `generated/quests/quest_dispatch.min*.json` root-published while the Questbook
  mechanic owns the builder, validation, and stop-lines

The near-term risk is roadmap drift: checkpoint recall, runtime writeback,
growth-refinery writeback, and continuity writeback are already shipped
memory-layer surfaces and should stay visible here without turning memory into
proof, routing, or live runtime authority.

The current topology hardening path starts with the source-authored route spine
in `DESIGN.md`, `DESIGN.AGENTS.md`, `docs/README.md`,
`docs/root/ROOT_SURFACE_LAW.md`, and `docs/decisions/`. This precedes any thematic
docs or mechanics migration so antifragility, Agon, Titan, adoption,
governance, checkpoint, consumer handoff, operational gate, recurrence
support, lineage harvest, readiness boundary, retention, and writeback
surfaces are moved only with owner maps, link updates, legacy bridges, and
validation.
The maintained Spark fast-loop lane now lives under `.agents/spark/` rather
than root `Spark/`, aligning agent-lane placement with the new topology spine
without treating the lane as root civic law.

The first generated AGENTS mesh is now the active topology hardening layer:
`config/agents/agents_mesh.json` records current route-card contracts and
`generated/agents/agents_mesh.min.json` is rebuilt from that source. Future docs or
mechanics migrations should add any new local route cards through this mesh
before landing.

The Agon and Titan migration is now mechanic-shaped rather than docs-district
shaped: `mechanics/agon/` and `mechanics/titan/` own the former flat and
transitional docs surfaces through package cards, owner maps, provenance
bridges, legacy indexes, generated mechanics coverage, and validators.

The antifragility migration is now mechanic-shaped as well:
`mechanics/antifragility/` owns failure-lesson and recovery-pattern memory
docs through package cards, owner maps, provenance bridge, legacy index,
generated mechanics coverage, examples, generated object surfaces, and tests.

The governance migration is now mechanic-shaped:
`mechanics/governance/` owns governance, federation, installation,
certification, precedent, and stay-order authority-boundary memory through
package cards, owner maps, provenance bridge, legacy index, generated mechanics
coverage, and tests. General via-negativa pruning now belongs to
`mechanics/shape-guard/` so governance stays an authority-boundary operation
rather than a topic bucket.

The mechanics topology follows the `Agents-of-Abyss` pattern:
`mechanics/antifragility/`, `mechanics/agon/`, `mechanics/titan/`,
`mechanics/adoption/`, `mechanics/governance/`, `mechanics/shape-guard/`,
`mechanics/checkpoint/`, `mechanics/readiness-boundary/`,
`mechanics/consumer-handoff/`,
`mechanics/operational-gate/`, `mechanics/recurrence-support/`,
`mechanics/lineage-harvest/`, `mechanics/writeback/`, and
`mechanics/retention/` own the former flat or transitional owner families as
memo-side mechanics. Each package has a route card, package card, operation,
direction, parts map, owner map, provenance
bridge, landing log, roadmap, and legacy index. The source-backed
`config/mechanics/memo_mechanics.json` and `generated/mechanics/memo_mechanics.min.json` keep the
shape machine-checkable. `generated/mechanics/memo_mechanic_landing_logs.min.json` now
makes dated landing receipts, release validation, and stop-lines inspectable,
and `generated/mechanics/memo_mechanic_readiness.min.json` adds the OS Abyss readiness
matrix over package cards, owner maps, parts, local artifacts, stop-lines, and
validation routes.

The operational-gate migration now owns deployment incident gates, office
incident gates, service revision ledger posture, and post-release memory
boundaries as one admission operation. Its schemas, examples, and tests now
live in `mechanics/operational-gate/` so the admission mechanic carries its own
contract surface.

The checkpoint migration now owns inquiry checkpoint, checkpoint-to-memory,
approval, health, improvement-thread, and phase-alpha checkpoint examples as
one checkpoint memory operation. Those technical artifacts now live under the
nearest functioning `mechanics/checkpoint/parts/<part>/` home so carry,
mapping, record preservation, and boundary regression can be checked as real
parts. Recurrence-support consumes checkpoint artifacts for route return, and
writeback consumes the checkpoint-to-memory contract for generated runtime
writeback companions.

The readiness-boundary migration now owns the memory readiness boundary doc,
contract schema, example, and regression test as one admission-boundary
operation. It gates durable-consequence, delta, retention, recall,
contradiction, bridge-candidate, and service-trace pressure into existing
memo objects and stronger owner routes without becoming proof, runtime
retention, KAG substrate, route dispatch, role authority, live ledger, or a
new object-family author.

The recurrence-support migration now owns recurrence support, witness trace,
and reviewed closeout recall landing surfaces as one route-return support
operation. Witness trace contracts live in `mechanics/recurrence-support/`;
shared recall contracts remain root-owned only when they are cross-mechanic.
Questbook now owns memo obligation mechanics: root `QUESTBOOK.md` is the compact
index, root `quests/` is the lane-first item store, and generated quest
companions are builder-backed projections whose owner routes must point back
into real memo docs or mechanic docs instead of inventing shadow homes.

The lineage-harvest migration now owns pattern-lineage memory as one
cross-repo recurring-signal gate. The pattern-lineage schema, example, and test
now live under `mechanics/lineage-harvest/`.

The current mechanics hardening layer adds `docs/AGENTS.md` and
`legacy/AGENTS.md` subroutes for each memo mechanic plus
`mechanics/ARTIFACT_TOPOLOGY.md`. This keeps active docs, legacy provenance,
and mechanic-local artifacts separate after the schema, example, generated,
script, test, manifest, questbook, and hook relocation.
The readiness matrix closes the next layer by proving every current package is
not only present but structurally ready for OS Abyss consumption.

## Current contract-hardening order

Within the current contract-hardening stage, the cleanest slice order is:

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
- `docs/memory/MEMORY_MODEL.md`
- `docs/boundaries/BOUNDARIES.md`
- `ROADMAP.md`
- initial glossary of core memory terms

**Exit criteria:**

- the role of `aoa-memo` can be explained without code
- neighboring layers can tell what memory owns and what it does not own
- the object canon is named even if schemas are not final yet

### `v0.2` Object canon and schemas

**Goal:** turn doctrine into a machine-checkable memory shape.

**Deliverables:**

- `schemas/memory-objects/memory_object.schema.json`
- `schemas/support-objects/provenance_thread.schema.json`
- `schemas/recall-posture/recall_contract.schema.json`
- `examples/` or `fixtures/` for core object kinds
- `scripts/memory/validate_memo.py`

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

- `generated/memory/memo_registry.min.json`
- `generated/memory/memory_catalog.json`
- `generated/memory/memory_catalog.min.json`
- `generated/memory/memory_capsules.json`
- `generated/memory/memory_sections.full.json`
- `generated/memory-objects/memory_object_catalog.json`
- `generated/memory-objects/memory_object_catalog.min.json`
- `generated/memory-objects/memory_object_capsules.json`
- `generated/memory-objects/memory_object_sections.full.json`

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
- `docs/posture/MEMORY_TEMPERATURES.md`
- `mechanics/writeback/docs/WRITEBACK_TEMPERATURE_POLICY.md`
- `schemas/recall-posture/decay_policy.schema.json`
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

- `mechanics/consumer-handoff/docs/AGENT_MEMORY_POSTURE_SEAM.md`
- `mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md`
- cross-repo contract notes for `aoa-agents` memory posture
- `mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json`
- `mechanics/checkpoint/parts/checkpoint-carry-contract/examples/inquiry_checkpoint.example.json`
- suggested fields for read, write, promotion, and freeze rights
- playbook-facing guidance for required memory scopes and recall modes

**Exit criteria:**

- agents are not assumed to have magical rights
- scenario design can say what memory it needs
- `aoa-memo` stays object-centric while `aoa-agents` and `aoa-playbooks` own policy and composition

### `v0.7` KAG bridge and ToS bridge

**Goal:** make memory KAG-oriented and ToS-connected without making the memory layer itself a substrate engine.

**Deliverables:**

- `mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md`
- `mechanics/consumer-handoff/docs/KAG_SOURCE_EXPORT.md`
- `mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/schemas/memory_chunk_face.schema.json`
- `mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/schemas/memory_graph_face.schema.json`
- chunk-face contract for memory inspection
- graph-face contract for downstream associative lifts
- `mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json`
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

- `mechanics/consumer-handoff/docs/MEMORY_EVAL_GUARDRAILS.md`
- `mechanics/consumer-handoff/parts/eval-guardrail-handoff/schemas/memory_eval_guardrail_pack.schema.json`
- `mechanics/consumer-handoff/parts/eval-guardrail-handoff/examples/memory_eval_guardrail_pack.example.json`
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

- `docs/boundaries/OPERATIONAL_BOUNDARY.md`
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
The first adoption pass should stay diagnostic and triad-scoped before the rest of the guardrail focuses are pulled into downstream proof bundles.

### `abyss-stack`

Needs to own live stores, background consolidation jobs, retention, and backup posture.
Future retention checks should keep their durable memo evidence bounded to
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
