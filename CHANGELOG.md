# Changelog

All notable changes to `aoa-memo` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

### Added

- Add a source-authored topology spine with `DESIGN.md`, `DESIGN.AGENTS.md`,
  `docs/README.md`, `docs/ROOT_SURFACE_LAW.md`, and `docs/decisions/` so
  future docs, agent-lane, and placement cleanup can route through explicit
  owner surfaces before moving flat memory docs.
- Add a source-backed AGENTS mesh with `config/agents_mesh.json`,
  `generated/agents_mesh.min.json`, mesh validators, and regression tests so
  current route-card coverage is machine-checkable before docs districts move.
- Add top-level route cards for `manifests/` and `quests/`.
- Add `mechanics/agon/` and `mechanics/titan/` memo mechanic packages with
  package cards, owner maps, provenance bridges, legacy indexes,
  source-backed generated mechanics index coverage, validators, tests, and
  decision record.
- Add `mechanics/antifragility/` as a memo mechanic package for
  failure-lesson and recovery-pattern memory, with package cards, owner map,
  provenance bridge, legacy index, AGENTS mesh coverage, generated mechanics
  coverage, validators, tests, and decision record.
- Add `mechanics/governance/` as a memo mechanic package for governance,
  federation, installation, certification, precedent, and stay-order
  authority-boundary memory, with package cards, owner map, provenance bridge,
  legacy index, AGENTS mesh coverage, generated mechanics coverage,
  validators, tests, and decision record.
- Add `mechanics/shape-guard/` as the memo mechanic for via-negativa
  memory-shape pruning, with operation-first package metadata, owner map,
  provenance bridge, legacy index, AGENTS mesh coverage, generated mechanics
  coverage, validators, tests, and decision record.
- Add `mechanics/consumer-handoff/` as the memo mechanic for bounded
  downstream handoff surfaces across agents, playbooks, evals, KAG/ToS bridge,
  KAG export, and orchestrator recall alignment, with owner map, provenance
  bridge, legacy index, AGENTS mesh coverage, generated mechanics coverage,
  validators, tests, and decision record.
- Add `mechanics/operational-gate/` as the memo mechanic for operational
  memory admission across deployment incidents, office/service incident gates,
  service revision ledger entries, and post-release memory boundaries, with
  owner map, provenance bridge, legacy index, AGENTS mesh coverage, generated
  mechanics coverage, validators, tests, and decision record.
- Add `mechanics/recurrence-support/` as the memo mechanic for bounded
  relaunch anchors, witness trace exports, and reviewed closeout recall
  landings, with owner map, provenance bridge, legacy index, AGENTS mesh
  coverage, generated mechanics coverage, validators, tests, and decision
  record.
- Add `mechanics/lineage-harvest/` as the memo mechanic for pattern-lineage
  memory candidates, federation harvest gates, and downstream dossier
  boundaries, with owner map, provenance bridge, legacy index, AGENTS mesh
  coverage, generated mechanics coverage, doctrine recall coverage,
  validators, tests, and decision record.
- Add `mechanics/checkpoint/` as the memo mechanic for checkpoint gates, carry
  packets, approval and health records, improvement threads, and
  checkpoint-to-memory mappings, with owner map, provenance bridge, legacy
  index, AGENTS mesh coverage, generated mechanics coverage, package-local
  artifacts, validators, tests, and decision record.
- Add `mechanics/readiness-boundary/` as the memo mechanic for high-pressure
  memory readiness admission boundaries, with owner map, provenance bridge,
  legacy index, AGENTS mesh coverage, generated mechanics coverage,
  package-local schema/example/test artifacts, validators, tests, and decision
  record.
- Add the `mechanics/` atlas plus `adoption`, `writeback`, and `retention`
  memo mechanic packages with package cards, owner maps, provenance bridges,
  legacy indexes, source-backed generated mechanics index, validators, tests,
  and decision record.
- Add mechanic docs/legacy subroute cards plus
  `mechanics/ARTIFACT_TOPOLOGY.md` so active package docs, legacy provenance,
  and mechanic-adjacent root technical artifacts have separate machine-checked
  routes.

### Changed

- Move the maintained Spark fast-loop lane from root `Spark/` to
  `.agents/spark/`, with `.agents/AGENTS.md` as the agent-facing district
  route card.
- Move transitional Agon docs-district surfaces into `mechanics/agon/docs/`
  and update recurrence manifest refs to the new mechanic paths.
- Move transitional Titan docs-district surfaces into `mechanics/titan/docs/`
  and update Titan source refs in README, examples, and tests.
- Move flat adoption, writeback, and retention docs-root surfaces into
  `mechanics/<slug>/docs/` and update source refs across docs, examples,
  generated companions, quests, scripts, and tests.
- Move flat antifragility docs-root surfaces into
  `mechanics/antifragility/docs/` and update README, registry, examples,
  generated object surfaces, writeback refs, scripts, and tests.
- Move flat governance docs-root surfaces into `mechanics/governance/docs/`
  and update README, docs maps, route law, validators, generated mechanics
  coverage, AGENTS mesh, and tests.
- Move `VIA_NEGATIVA_CHECKLIST.md` from governance into
  `mechanics/shape-guard/docs/` and require every memo mechanic card to name
  its repeatable operation.
- Move flat consumer-handoff docs-root surfaces into
  `mechanics/consumer-handoff/docs/` and update README, docs maps, route law,
  quests, examples, generated companions, validators, and tests to the new
  active paths.
- Move flat operational-gate docs-root surfaces into
  `mechanics/operational-gate/docs/` and expand the deployment incident and
  post-release boundary docs from placeholder notes into evidence/owner-route
  admission contracts.
- Move flat recurrence-support docs-root surfaces into
  `mechanics/recurrence-support/docs/` and update README, docs maps, route
  law, quests, examples, generated companions, validators, and tests to the
  new active paths.
- Move the flat pattern-lineage docs-root surface into
  `mechanics/lineage-harvest/docs/` and update README, docs maps, route law,
  generated companions, validators, and tests to the new active path.
- Move checkpoint-specific schemas and examples into
  `mechanics/checkpoint/` and update recurrence-support/writeback consumers,
  generated companions, validators, and tests to the new artifact owner path.
- Move the flat readiness boundary doc plus its schema, example, and
  regression test into `mechanics/readiness-boundary/` and update README,
  docs maps, route law, registry refs, generated object surfaces, validators,
  and tests to the new artifact owner path.
- Extend the AGENTS mesh and memo mechanics validator to include Agon/Titan
  and antifragility/governance/shape-guard/consumer-handoff/operational-gate/
  recurrence-support/lineage-harvest mechanics and mechanic docs/legacy
  subroutes.

## [0.2.3] - 2026-04-23

### Summary

- this patch expands memo surfaces across Agon prebindings, verdict-delta scar
  bridges, scar candidate intake, mechanical-trial intakes, retention rank,
  schools/lineages, KAG/Sophian evidence, and Wave XV epistemic memory
- Titan memory loom, remembrance provenance, and recall/source-anchor contracts
  land beside Experience memory readiness, release gates, adoption contracts,
  governance/runtime memory boundaries, revision ledgers, retention markers,
  and wave5 datetime validation
- `aoa-memo` remains the bounded recall and writeback layer; memory stays
  explicit, provenance-aware, and weaker than proof or source truth

### Added

- Agon memo prebindings, scar bridges, scar candidate intakes, mechanical
  trial intakes, retention-rank candidate boundaries, schools/lineages,
  KAG/Sophian evidence packages, and epistemic memo surfaces
- Titan memory loom posture, Titan bridge/closeout/operator-console memory
  posture, remembrance provenance contracts, source-ref policy, recall
  candidate policy, and personality memory policy
- Experience memory readiness boundaries, release memory gates, adoption
  forgetting/revision/retention/scar-writeback contracts, governance runtime
  memory boundaries, installation/service memory boundaries, office incident
  gates, post-release retention watch, and sovereign-office memory surfaces

### Changed

- memo review follow-ups, contract drift, wave2 and wave4 gates, remembrance
  source anchors, post-merge contract guards, generated memo registry version,
  and RFC3339 datetime validation were tightened

### Validation

- `python scripts/release_check.py`

### Notes

- this patch adds recall/writeback and provenance surfaces only; proof remains
  in `aoa-evals`, routing in `aoa-routing`, and runtime records in
  `abyss-stack`

## [0.2.2] - 2026-04-19

### Summary

- this patch adds live receipt publishing, A2A return provenance, and
  self-agency continuity objects across the memo layer
- recall landing, writeback lanes, KAG export provenance, and
  reviewed-candidate adoption are tightened for the current memory wave
- `aoa-memo` remains the bounded recall and writeback layer rather than proof
  or routing authority

### Added

- live receipt publishing and hydration validation, A2A child-return
  provenance fixtures, memory-readiness pressure cases, and growth-refinery
  live writeback lanes
- self-agency continuity objects and KAG export provenance relations across
  memo-facing surfaces

### Changed

- recall landing, reviewed candidate memo receipts, memory-scope package
  validation, and CI/protection surfaces are tightened around the active
  writeback loop

### Validation

- `python scripts/release_check.py`

### Notes

- this patch extends bounded recall and provenance-aware writeback without
  turning `aoa-memo` into an eval, routing, or runtime authority layer

## [0.2.1] - 2026-04-12

### Summary

- this patch extends checkpoint recall and rollout-memory writeback through the
  current continuity wave
- growth-refinery writeback handling is tightened without widening `aoa-memo`
  beyond bounded recall
- the release remains a memory-layer refinement over `v0.2.0`

### Added

- checkpoint recall follow-through quest capture and lineage-aware growth
  refinery writeback surfaces.
- rollout memory writeback examples, campaign cadence memo examples, and
  self-agency continuity writeback support.

### Changed

- growth-refinery memo writeback and review-badge handling are tightened around
  the current continuity-oriented writeback loop.

### Validation

- `python scripts/release_check.py`

### Notes

- detailed checkpoint recall, rollout-memory writeback, and growth-refinery
  changes for this patch remain enumerated below under `Added` and `Changed`

## [0.2.0] - 2026-04-10

### Summary

- this release adds runtime writeback landing gates, live receipt publishing, scope classes, capsule-backed recall, and checkpoint-growth memo surfaces
- memo schemas, JSONL publication boundaries, and writeback references are hardened across the live writeback loop
- `aoa-memo` remains the bounded memory and recall layer rather than source or proof authority

### Validation

- `python scripts/release_check.py`

### Notes

- detailed writeback, recall, generated-surface, and contributor-surface coverage for this release remains enumerated below under `Added`, `Changed`, and `Included in this release`

### Added

- runtime writeback landing gate, live receipt publisher, and workspace
  checkpoint-growth memo writeback surfaces
- scope classes for memory-object surfaces, capsule-backed working-return
  recall, fourth-wave recovery patterns, and antifragility failure-lesson
  contracts
- checkpoint closeout bridge install plus repo-local project-foundation and
  session-harvest follow-through surfaces

### Changed

- hardened memo schemas, nullable datetime validation, JSONL publication
  boundaries, and writeback refs across the live writeback loop
- aligned docs and AGENTS guidance with next-wave continuity posture and
  bounded recall routing

### Included in this release

- memo writeback, recall, and recovery surfaces across `docs/`, `generated/`,
  `schemas/`, `examples/`, and `scripts/`, including Phase Alpha writeback
  corpus, scope classes, capsule-backed recall, failure-lesson contracts, and
  live publication support
- repo-local quest, follow-through, and contributor surfaces under `.agents/`,
  `.github/`, `CHARTER.md`, `QUESTBOOK.md`, `quests/`, `AGENTS.md`,
  `README.md`, `CONTRIBUTING.md`, and `tests/`, including orchestrator memory
  quests, quest-harvest installs, and validation-route alignment

## [0.1.0] - 2026-04-01

First public baseline release of `aoa-memo` as the explicit memory and recall layer in the AoA public surface.

This changelog entry uses the release-prep merge date.

### Summary

- first public baseline release of `aoa-memo` as the memory and recall layer for AoA
- the public baseline now includes doctrine-facing memory surfaces, object-facing memory surfaces, a bounded source-owned memo export seam, and writeback / guardrail contracts
- the release keeps memory explicit and reviewable without collapsing memory into proof, routing, or execution ownership

### Added

- community-docs baseline established for this repository
- `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `CONTRIBUTING.md`
- memo-side contract docs for `aoa-agents`, `aoa-playbooks`, KAG/ToS bridge exports, eval guardrails, and the operational boundary
- `mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md` to formalize router-facing inspect -> capsule -> expand memo consumption without moving routing policy into `aoa-memo`
- schema-backed chunk-face, graph-face, and eval-guardrail handoff surfaces with bounded examples
- bridge-lift provenance examples and validation coverage for new bridge/export and guardrail surfaces

### Changed

- roadmap and doctrine-facing generated surfaces now record that `aoa-routing` already consumes the live `memo` kind and router-ready recall contracts
- router-facing doctrine recall contracts and object-facing semantic or lineage recall contracts now publish an additive `capsule_surface` between inspect and expand

### Included in this release

- doctrine-facing memory families under `generated/memory_catalog.json`, `generated/memory_catalog.min.json`, `generated/memory_capsules.json`, and `generated/memory_sections.full.json`
- object-facing memory families under `generated/memory_object_catalog.json`, `generated/memory_object_catalog.min.json`, `generated/memory_object_capsules.json`, and `generated/memory_object_sections.full.json`
- bounded source-owned export and writeback support seams under `mechanics/consumer-handoff/generated/kag_export.min.json`, `mechanics/writeback/generated/runtime_writeback_targets.min.json`, and `mechanics/writeback/generated/runtime_writeback_intake.min.json`

### Validation

- `python scripts/generate_memory_object_surfaces.py`
- `python mechanics/consumer-handoff/scripts/generate_kag_export.py`
- `python scripts/validate_memo.py`
- `python scripts/validate_memory_surfaces.py`
- `python scripts/validate_memory_object_surfaces.py`
- `python scripts/validate_lifecycle_audit_examples.py`

### Notes

- this release is a repository release of memory contracts and derived memory surfaces, not a claim that memory should replace source truth or proof
