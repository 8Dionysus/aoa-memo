# Changelog

All notable changes to `aoa-memo` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

### Added

- Add a registry-backed `.agents/spark/` Codex Spark lane with memo-specific
  scenarios, result and handoff packet homes, schemas, validator, tests,
  release-gate wiring, and decision record.
- Add `MEMORY_INDEX.md` as a compact root memory-canon map for object kinds,
  support objects, recall modes, temperature vocabulary, source families, and
  generated companions.
- Extend the mechanic artifact inventory and readiness matrix to recognize
  part-local technical homes, and move Agon runnable artifacts into its
  functioning `parts/` lanes with part-local validation.
- Move antifragility failure-lesson, shared-lesson, recovery-pattern, native
  pattern, and local regression artifacts into their functioning `parts/`
  homes with part-local validation.
- Move operational-gate deployment, office incident, service revision, and
  post-release boundary artifacts into functioning `parts/` homes with
  part-local validation.
- Move the remaining shape-guard, readiness-boundary, recurrence-support,
  lineage-harvest, and Questbook package-level artifacts into functioning
  `parts/` homes so the mechanic artifact inventory has no package-scope
  residue.
- Add part-local adoption and retention contract tests so those mechanics can
  validate boundary, revision/retention, scar/routing, office marker,
  cross-repo/governance, and post-release artifacts at their owning parts.
- Add a package-local retention regression boundary so retention docs,
  schemas, examples, and stronger-owner stop-lines are tested inside
  `mechanics/retention/`.
- Add readiness artifact-test coverage so a mechanic with package-local
  config, examples, generated companions, manifests, schemas, or scripts
  cannot be marked OS Abyss ready without a package-local regression test.
- Add readiness local-test-route coverage so mechanic packages with
  package-local tests must name their local pytest command in validation
  surfaces.
- Add physical `parts/` contracts for memo mechanics so each active row in
  `PARTS.md` has a `README.md`, `CONTRACT.md`, and `VALIDATION.md` node.
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
- Add a builder-backed quest projection check for `generated/quest_catalog`
  and `generated/quest_dispatch` surfaces so root quest companions are
  reproducible from source quest files.
- Add `mechanics/questbook/` as the memo mechanic for public memory-layer
  obligations, with lane-first `quests/` source placement, source-contract
  docs, validator, generated projection builder, tests, AGENTS mesh coverage,
  generated mechanics coverage, and decision record.
- Add `mechanics/questbook/parts/quest-read-model-projections/` so root-published quest
  generated read models have an explicit mechanic-owned part contract and
  validator coverage.
- Add the `mechanics/` atlas plus `adoption`, `writeback`, and `retention`
  memo mechanic packages with package cards, owner maps, provenance bridges,
  legacy indexes, source-backed generated mechanics index, validators, tests,
  and decision record.
- Add mechanic docs/legacy subroute cards plus
  `mechanics/ARTIFACT_TOPOLOGY.md` so active package docs, legacy provenance,
  and mechanic-adjacent root technical artifacts have separate machine-checked
  routes.
- Add `scripts/validate_mechanic_artifact_topology.py` to make root
  technical-district placement a direct release-gate validator rather than
  only a pytest regression.
- Add `config/root_technical_districts.json` as an exact allowlist for root
  technical artifacts so remaining root schemas, examples, generated outputs,
  scripts, tests, manifests, and config files are machine-auditable.
- Extend the root technical contract with schema-family ownership so every
  root `schemas/` file names its public contract role, owner surface, source
  refs, and validators.
- Extend the root technical contract with example-family ownership so every
  root `examples/` file names its public example role, owner surface, source
  refs, and validators.
- Extend the root technical contract with config-family ownership and an
  explicit reserved-empty root manifests policy, so root `config/` and
  `manifests/` are also machine-owned rather than only allowlisted.
- Add a builder-backed package-local mechanic artifact inventory at
  `generated/mechanic_artifacts.min.json`, with builder, validator, release
  gate coverage, and tests so mechanic-local schemas, examples, config,
  generated outputs, scripts, tests, and manifests stay inspectable.
- Add `scripts/validate_memo_mechanic_parts.py` to keep mechanic `PARTS.md`
  files operation-shaped, with Active Parts tables, source links, interface
  sections, release gate coverage, and regression tests.
- Add `generated/memo_mechanic_readiness.min.json` with builder, validator,
  release gate coverage, root technical family contracts, and regression tests
  so every memo mechanic package has a machine-checkable OS Abyss readiness
  surface.
- Add `generated/memo_mechanic_landing_logs.min.json` with builder,
  validator, release gate coverage, root technical family contracts, and
  regression tests so every memo mechanic package has a machine-checkable
  landing receipt surface.
- Extend `config/root_technical_districts.json` with root generated-family
  contracts so every root `generated/` output names its owner surface, source
  refs, validators, and builders when generator-backed or projected.
- Extend the same root technical contract with script-family ownership so every
  root `scripts/` file names its role, owner surface, and release/test coverage
  refs.
- Extend the root technical contract with test-family ownership so every root
  `tests/` file and public fixture names its role, owner surface, and protected
  refs.

### Changed

- Compact the root README Memo Mechanics section so detailed mechanic routing
  stays in AGENTS/mechanic atlas surfaces rather than root public overview.
- Rename active root cross-mechanic contract families and part-local
  governance/post-release regressions from migration-era staging labels to
  current operation-owner language.
- Normalize active root doctrine and roadmap wording toward baseline, pass,
  slice, and stage language while leaving source-owned Agon and lineage refs
  intact.
- Upgrade the moved Spark lane from two guidance files into a functional
  one-scenario `done-or-handoff` fast loop for bounded memory-layer work.
- Align root README, CHARTER, ROADMAP, docs map, design surfaces,
  CONTRIBUTING, CODE_OF_CONDUCT, QUESTBOOK, and SECURITY around explicit
  root-doc authority, memory-canon routing, public-safety posture, and
  AGENTS-owned validation routes.
- Compact the root README current-contour section so GitHub renders short
  route labels instead of long monospaced path blocks.
- Replace wide mechanics atlas tables with wrapping lists so GitHub renders
  the mechanic card contract and compass without cramped code-cell breaks.
- Move mechanics atlas command runbook details into `mechanics/AGENTS.md` so
  `mechanics/README.md` stays a human-readable atlas.
- Add functional Route Stack guidance across mechanics and root technical
  district `AGENTS.md` files, and keep README/index surfaces map-oriented.
- Harden mechanic part naming by keeping package mechanic slugs stable while
  renaming weak surface-family part slugs into operation/read-model route
  names for lineage-harvest, Questbook, recurrence-support, and Titan.
- Move governance schemas, examples, and local regressions into nearest
  functioning `parts/` homes, with federation, install/certification,
  precedent, lineage, and cross-mechanic contract refs updated to the part-local
  surfaces.
- Move consumer-handoff schemas, examples, generated KAG export, generator,
  playbook regression, and downstream feed tests into nearest functioning
  `parts/` homes, with validators and generated references updated to the
  part-local surfaces.
- Move checkpoint inquiry, mapping, approval/health/improvement, Phase Alpha,
  and boundary regression artifacts into nearest functioning `parts/` homes,
  with recurrence, consumer-handoff, and writeback refs updated to the
  part-local checkpoint surfaces.
- Move writeback schemas, examples, generated companions, scripts, tests, and
  receipt fixtures into nearest functioning `parts/` homes, with the
  operational-contract regression registered as a root cross-mechanic test
  family.
- Move Titan runnable schemas, examples, and tests into nearest functioning
  `parts/` homes, split digest/closeout candidate coverage into a part-local
  regression test, and tighten readiness local-test-route detection around
  runnable pytest arguments.
- Move adoption and retention schemas, examples, and local tests into nearest
  functioning `parts/` homes, and remove the stale retention validation
  dependency on governance tests from the retention route.
- Move the downstream feed regression into
  the consumer-handoff mechanic regression lane, move the tracked writeback receipt
  fixture into `mechanics/writeback/parts/receipt-publication-regression/tests/fixtures/`,
  and narrow the remaining
  root test-family contract to the cross-mechanic candidate-contract regression.
- Move self-agency continuity object examples from root `examples/` into
  `mechanics/writeback/parts/growth-and-continuity/examples/` while keeping
  them in the root object-surface manifest and generated object-facing family.
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
- Move flat root quest sources into lane-first lifecycle directories under
  `quests/`, move the quest projection builder into
  `mechanics/questbook/parts/quest-read-model-projections/scripts/`, and give Agon follow-through Markdown notes
  an explicit memo quest source contract.
- Close the compact witness trace quest through recurrence-support, route the
  chronicle quest to writeback, and require current quest `owner_surface` and
  `anchor_ref` values to resolve into real memo docs or mechanic docs.
- Extend the AGENTS mesh and memo mechanics validator to include Agon/Titan
  and antifragility/governance/shape-guard/consumer-handoff/operational-gate/
  recurrence-support/lineage-harvest/questbook mechanics and mechanic docs/legacy
  subroutes.
- Normalize governance and lineage-harvest `PARTS.md` into the shared Active
  Parts plus Interface shape.

## [0.2.3] - 2026-04-23

### Summary

- this patch expands memo surfaces across Agon prebindings, verdict-delta scar
  bridges, scar candidate intake, mechanical-trial intakes, retention rank,
  schools/lineages, KAG/Sophian evidence, and Wave XV epistemic memory
- Titan memory loom, remembrance provenance, and recall/source-anchor contracts
  land beside Experience memory readiness, release gates, adoption contracts,
  governance/runtime memory boundaries, revision ledgers, retention markers,
  and post-release datetime validation
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

- memo review follow-ups, contract drift, operational and governance-boundary gates, remembrance
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
- bounded source-owned export and writeback support seams under `mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json`, `mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json`, and `mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json`

### Validation

- `python scripts/generate_memory_object_surfaces.py`
- `python mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py`
- `python scripts/validate_memo.py`
- `python scripts/validate_memory_surfaces.py`
- `python scripts/validate_memory_object_surfaces.py`
- `python scripts/validate_lifecycle_audit_examples.py`

### Notes

- this release is a repository release of memory contracts and derived memory surfaces, not a claim that memory should replace source truth or proof
