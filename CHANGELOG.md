# Changelog

All notable changes to `aoa-memo` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

## [0.2.0] - 2026-04-10

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
