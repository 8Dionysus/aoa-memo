# Changelog

All notable changes to `aoa-memo` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

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
- `docs/ROUTING_MEMORY_ADOPTION.md` to formalize router-facing inspect -> capsule -> expand memo consumption without moving routing policy into `aoa-memo`
- schema-backed chunk-face, graph-face, and eval-guardrail handoff surfaces with bounded examples
- bridge-lift provenance examples and validation coverage for new bridge/export and guardrail surfaces

### Changed

- roadmap and doctrine-facing generated surfaces now record that `aoa-routing` already consumes the live `memo` kind and router-ready recall contracts
- router-facing doctrine recall contracts and object-facing semantic or lineage recall contracts now publish an additive `capsule_surface` between inspect and expand

### Included in this release

- doctrine-facing memory families under `generated/memory_catalog.json`, `generated/memory_catalog.min.json`, `generated/memory_capsules.json`, and `generated/memory_sections.full.json`
- object-facing memory families under `generated/memory_object_catalog.json`, `generated/memory_object_catalog.min.json`, `generated/memory_object_capsules.json`, and `generated/memory_object_sections.full.json`
- bounded source-owned export and writeback support seams under `generated/kag_export.min.json`, `generated/runtime_writeback_targets.min.json`, and `generated/runtime_writeback_intake.min.json`

### Validation

- `python scripts/generate_memory_object_surfaces.py`
- `python scripts/generate_kag_export.py`
- `python scripts/validate_memo.py`
- `python scripts/validate_memory_surfaces.py`
- `python scripts/validate_memory_object_surfaces.py`
- `python scripts/validate_lifecycle_audit_examples.py`

### Notes

- this release is a repository release of memory contracts and derived memory surfaces, not a claim that memory should replace source truth or proof
