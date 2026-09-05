# Changelog

All notable changes to `aoa-memo` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

### Added

- Add decisions `AOA-MEM-D-0086` and `AOA-MEM-D-0087`: inherited
  `AGENTS.md` cards retain semantic delta, routing, and stop-lines while exact
  focused procedure moves to one same-directory `VALIDATION.md` per owner
  card; recursive route aggregates are rejected.
- Add decisions `AOA-MEM-D-0088` and `AOA-MEM-D-0089`: delegated validation
  routes must name their exact owner, while a same-directory `VALIDATION.md`
  is topology metadata only beside a tracked `AGENTS.md`, never ordinary
  doctrine, quest, manifest, or technical payload.
- Add decision `AOA-MEM-D-0085` and owner-authored MCP capability contours for
  reviewed durable-memory reads and candidate-only handoff preparation. The
  read/candidate identities remain disjoint and grant no direct durable write,
  proof, admission, or effect authority.
- Land the reviewed claim that a direct KAG → Memo → Evals chain preserves
  proof and memory-owner boundaries, with the exact reviewed intake and
  landing receipt retained in the corpus.
- Land the bounded role-first external-actor responsibility claim, with the
  obligation → incarnation → pause/wake → filtered-return contour, exact
  reviewed intake refs, and explicit separation from runtime, live stats,
  owner acceptance, and recurring-pattern promotion.
- Repair the pre-correction external-actor landing receipt as a machine-
  readable rejected historical attempt, add its lifecycle audit event, and
  guard the corpus against multiple active `landed` receipts for one object.

- Add decision `AOA-MEM-D-0082`, making reviewed public explicit pull the R1
  admitted core while keeping proactive, private, and agent-local runtime
  contours disabled until separate evidence and authority gates pass.
- Add decisions `AOA-MEM-D-0077` through `AOA-MEM-D-0081` for selective
  owner-orientation shadow/canary contracts, outcome-qualified proposal-only
  utility, allowlisted mechanical lifecycle, walkable distributed erasure,
  and isolated agent-local promotion without shared-truth authority.
- Add decision `AOA-MEM-D-0083`, a two-speed participation spine for ordinary
  Codex sessions: bounded brief-first recall, correct silence and sibling
  handoff, an independent content-minimized H0 hook fragment, and explicit
  whole-session receipt retention that never runs as an implicit hook effect.
- Add one manually admitted `aoa-memo` owner bundle with internal `recall`,
  `review`, and `evolve` modes under the canonical `skills/` home.

### Changed

- Add bounded local changed-path feedback to the existing `ci_gate.py`: mapped
  owner tests are deduplicated from the root topology, test inventory, and
  mechanic part tests, while runner/config/fixture/environment and unknown
  paths fail closed to the existing release lane. Optional `--lf` remains
  retry feedback only and cannot become release admission.
- Skip expensive retired mechanics-path regex searches when the literal path
  is absent. Keep the exact boundary checks, provenance exceptions, and full
  tracked-file coverage; focused regression covers those distinctions.

- Split the repository-wide and mechanic-package validation aggregates into
  owner-local on-demand companions, preserving focused commands while avoiding
  unrelated procedure preload.
- Treat `aoa-kag://` evidence references as symbolic owner refs in reviewed
  intake validation while continuing to require packet-local candidate and
  receipt references for landing authorization.

- Route current dispatch boundaries, mechanic owner maps, operational readouts,
  and memo consumer guidance through the canonical `aoa-sdk` control plane
  while preserving dated `aoa-routing` provenance and release history.
- Compact the owner skill's global description while retaining existing-artifact
  selection, the package-first gate, and the first-writeback coexistence
  boundary.
- Replace 25 copied shared skill projections with one exact generated
  `.agents/skills/aoa-memo` projection and remove the foreign companion-script
  regression that treated a copied workflow helper as memo-owned truth.

## [0.5.0] - 2026-07-13

### Summary

- establish the distributed memory-organ foundation and its operational
  readouts, reviewed writeback objects, access-plane intake, and reproducible
  workspace memo-port status without moving runtime or proof authority into
  `aoa-memo`
- complete the canonical `AOA-MEM-D-####` decision lane with full-ID source
  filenames and generated lookup indexes, retiring the numbered compatibility
  paths from the active surface
- refactor validation, builder, and test topology into explicit owner lanes,
  focused validator profiles, bounded test homes, and command-authority
  manifests while deactivating legacy validation surfaces
- add the memo-local eval port, artifact identities, OS Abyss and subject-store
  trust gates, the local KAG provider/index family, and the owner-local stats
  port so downstream consumers receive fail-closed, provenance-bearing memory
  read models
- harden reviewed intake, operation-mode, Spark-schema, decision-surface, and
  generated-route handling so malformed or nonlocal evidence fails as a
  reported contract error rather than becoming accepted memory or a traceback

### Added

- Add the owner-local `stats/` port with a source-backed reviewed-memory-object
  count contract and reference packet; memo corpus meaning remains here while
  `aoa-stats` owns the shared statistical grammar, cross-owner composition,
  and the validator delegated to by the release lane.
- Add an explicit `aoa_local_memo_receipt_v2` branch for local memo receipts
  using `checked_by`, while keeping legacy `aoa_local_memo_receipt_v1`
  `reviewed_by` receipts readable under the same schema file.
- Distribute the memory-organ foundation layout across existing memory,
  topology, object-profile, lifecycle, retention, consumer-handoff, and
  Questbook surfaces so future memory events have stable intake lanes, object
  slots, recall-pack grammar, lifecycle pressures, quality lenses, port-status
  fields, and activation quests without adding a separate foundation document.
- Add operational readouts for access-plane currentness, source-lane intake
  wave coverage, and workspace memo-port status so distant agents can inspect
  the memo route while `abyss-stack` and `8Dionysus` keep their stronger owner
  boundaries.
- Add reviewed decision objects for the distributed memory-organ foundation and
  operational readout slices, with an explicit writeback debt catchup marker so
  these landed changes become recallable corpus memory rather than only PR or
  decision-doc history.
- Land the `abyss-stack` OS access-plane MCP services reviewed-intake packet as
  a reviewed decision object so the memory corpus records the memory/eval/host
  MCP owner split without moving runtime, proof, or host authority into memo.
- Land the `abyss-stack` `aoa-memo-mcp` workspace-port-discovery intake packet
  as a reviewed decision object so map-discovered full ports become recallable
  corpus memory rather than only access-plane implementation detail.
- Add canonical `AOA-MEM-D-####` IDs, decision-note index metadata, generated
  decision lookup indexes, and full canonical-ID decision filenames so agents
  can find decision rationale without reading a hand-maintained omnibus index.
- Complete the decision-lane path migration by retiring date-path compatibility
  metadata, short numbered filenames, and generated compatibility read models;
  full `AOA-MEM-D-####` filenames are now the only active decision source route.
- Add validator topology and lane metadata with
  `docs/validation/VALIDATOR_TOPOLOGY.md`, `config/validation_lanes.json`,
  `scripts/validation_lanes.py`, `scripts/ci_gate.py`, and
  `scripts/root-topology/validate_validator_topology.py` so validators are
  grouped by boundary layer instead of accumulating as historical release
  scripts.
- Add `docs/testing/` and focused regressions so test inventory, release-check
  command authority, CI lane selection, and validator topology stay aligned.
- Split the historical broad `scripts/memory/validate_memo.py` release use into
  focused profiles for schema, memory context, runtime boundary, handoff
  boundary, and eval boundary checks, so release lanes no longer run one
  unprofiled memory validator across multiple authority layers.
- Move those profile implementations into `scripts/memory/validators/` modules
  and keep `validate_memo.py` as a thin compatibility CLI, with topology tests
  preventing the memo validator from growing back into a monolith.
- Split the former broad memory validator regression file into layer-owned
  tests for schema contracts, memory-context boundaries, runtime degradation,
  Questbook projections, handoffs, eval guardrails, and generated read-model
  contracts, with test topology enforcing the split.
- Split the runtime degradation regression surface again into runtime
  writeback contracts and live receipt degradation tests so runtime writeback
  semantics and receipt replay/fault cases stay separately reviewable.
- Split the mechanic artifact topology validator into a thin CLI, shared
  topology helpers, and a reusable family-contract engine so root technical
  district checks no longer live in one bulky validator file.
- Split validator-topology helper constants and path checks out of
  `validate_validator_topology.py` so the validator topology gate also stays
  below the repo's bulky-file threshold.
- Exclude legacy raw test snapshots from active test inventory and pytest
  collection, rename preserved legacy `test*.py` snapshots into inert
  `.snapshot` files, and cap active test files at 300 lines so historical
  tests cannot silently re-enter gates or grow back into bulky hidden
  architecture.
- Remove legacy mechanic folders from active AGENTS mesh and mechanic readiness
  package-surface checks so legacy stays provenance only, not a required route
  card or readiness bridge.
- Retire the old Titan remembrance single-`source_ref` schema branch from the
  active recall/remembrance part, preserving its v0 example only as an inert
  legacy snapshot.
- Tighten the root README into a compact front door and route detailed memory,
  mechanics, generated, and technical inventories to their owning surfaces.
- Add the OS Abyss memory-object artifact bundle trust gate to the public
  validation lane, including subject-store materialization and fail-closed
  consumer verdict coverage for generated memo surfaces.
- Align root surface law with the memo-local `evals/` technical district while
  keeping proof doctrine and verdict authority in `aoa-evals`.

### Changed

- Centralize runnable validation commands in the lane manifest, nearest
  `AGENTS.md` or `VALIDATION.md`, and the active release procedure; decisions,
  changelog history, landing logs, reviewed memory objects, and route maps now
  retain owner routes and outcomes instead of copied command catalogs.
- Refresh the release-closeout workspace memo-port readout from the landed
  owner map so publication carries current route evidence instead of the
  pre-merge workspace snapshot.

### Fixed

- Pin repo-local KAG source-index validation to the portable shared generator
  and refresh the repository-owned index from the current memo source tree.
- Record the roadmap alignment that keeps mechanic `legacy/` material as
  indexed provenance outside the active AGENTS mesh while active mechanic
  doctrine stays in `docs/AGENTS.md`.
- Reject local memo source/evidence refs that become blank after trimming so
  reviewed intake cannot preserve whitespace-only provenance.
- Reject symbolic or otherwise invalid reviewed-intake receipt `candidate_ref`
  values during corpus landing input validation, and refresh the imported
  workspace memo-port status so `aoa-memo` remains a route-only reviewed corpus
  owner instead of a broken local port.
- Report invalid Draft 2020-12 Spark registry schemas through the Spark lane
  validator problem list instead of allowing schema drift to raise a traceback.
- Report non-file and non-JSON operation mode refs as memory-operation
  validation errors instead of letting JSON loading raise a traceback.
- Require `checked_by` on `aoa_local_memo_receipt_v2` packets so reviewed
  intake cannot rely on v2 receipts without checker provenance.
- Preserve sibling script imports when `validate_memo.py` is imported by file
  location, so the schema profile can still load `validate_nested_agents.py`.

### Validation

- the active repo-level release gate and its workspace-compatibility wrapper
  completed successfully through the release routes owned by
  `docs/root/RELEASING.md` and `scripts/release/`
- federation preflight completed through the workspace release owner using the
  dependency revisions pinned by this repository's validation workflow
- GitHub `Repo Validation` completed successfully on the landed release commit
- a landed-main live access-plane verification recorded six passing probes,
  one explicitly routed known gap, and no failed probes; the checked-in
  access-plane readout remains the contract-only release artifact, while the
  imported workspace map separately preserves the current Tree-of-Sophia
  memory-route issue instead of flattening it into a green memo claim

### Notes

- this release was reconstructed from the complete first-parent history and
  tree diff from `v0.4.0` through `698d823`, not from the previous
  `[Unreleased]` prose alone: the reconciled span contains 61 first-parent
  changes across 404 paths, with 60,928 insertions and 11,985 deletions
- every first-parent change in that span is listed below; the release-prep
  change itself is represented by this dated section, the `v0.5.0` version
  alignment, validation evidence, and publication metadata
- this release changes the reviewed memory owner only; evaluation truth stays
  in `aoa-evals`, routing in `aoa-routing`, shared KAG and statistical grammar
  in `aoa-kag` and `aoa-stats`, runtime/storage in `abyss-stack`, and role or
  playbook authority in their owning repositories

### Included in this release

- `ca456e8` - Land memory organ foundation routes
- `b8eea5c` - Land memory operational readouts (#222)
- `c90c605` - Land memo writeback catchup objects (#223)
- `81cb36f` - Land abyss-stack access-plane memory intake (#224)
- `d315627` - Land memo MCP workspace port discovery intake (#225)
- `be3e7a5` - Refresh workspace memo port status readout (#226)
- `4d7e843` - Sync workspace memo port status after aoa-agents marker (#227)
- `ae5e4e6` - Sync workspace memo port status after aoa-agents formation marker (#228)
- `38f8d8f` - Sync workspace memo port status after aoa-agents assistant civil marker (#229)
- `c7cb869` - Sync workspace memo port status after aoa-agents Codex refresh marker (#230)
- `7b7efa4` - Sync workspace memo port status after aoa-agents adoption boundary marker (#231)
- `2544a49` - Add canonical decision indexes (#232)
- `0a83502` - Use numbered decision paths (#233)
- `36fe6e5` - Complete numbered decision route migration (#234)
- `f4a822e` - Use full decision IDs in memo decision filenames (#235)
- `0a1dc6e` - Refactor memo validation topology
- `ffaf5f8` - Split memo validator profiles into modules
- `660ff56` - Split memo validator tests by boundary (#238)
- `d2aa7da` - Split remaining bulky validation surfaces (#239)
- `147a224` - Refine memo validator and test topology (#240)
- `acdef7d` - Refactor memo builder topology (#241)
- `895a9db` - Tighten memo test topology gates (#242)
- `5c53b7e` - Deactivate legacy validation surfaces (#243)
- `477c251` - Slim root README route surface (#244)
- `fdce572` - Keep README validation route command-free (#245)
- `efb7e0d` - Detect unmodeled decision lane surfaces (#246)
- `6b85a83` - Validate modeled decision surface contract entries (#247)
- `8055b6c` - Add local eval port (#248)
- `5f87c4f` - Refresh KAG source export route (#249)
- `e3f39a4` - Align KAG export ToS donor ref
- `82823cb` - Align evals root surface law (#251)
- `bd5b017` - Align roadmap with legacy deactivation (#252)
- `e3f1283` - Load memo validators through private package (#253)
- `74ac0bc` - Derive memo decision index test expectations (#254)
- `845c227` - Harden memory operational readouts
- `bc3771d` - Reject nonlocal reviewed intake refs (#256)
- `b7bdedb` - Require reviewed intake receipt coverage (#257)
- `7677032` - Version local memo receipt checked-by contract (#258)
- `bb169ea` - Validate memory intake operation mode refs
- `fdb157c` - Validate Spark registry against schema
- `f2ae15a` - Cover operational contract part paths
- `3139924` - Handle invalid Spark registry schemas (#262)
- `ec5993b` - Handle non-JSON operation mode refs (#263)
- `f69ca51` - Require checked_by on v2 receipts (#264)
- `ff22991` - Guard reviewed intake receipt candidate refs (#265)
- `568b73e` - Reject blank trimmed memo refs (#266)
- `13ba7b6` - Preserve validate_memo sibling imports (#267)
- `9747615` - Add roadmap legacy changelog note
- `dc1530d` - [codex] Add artifact identity to memory object surfaces (#269)
- `04c1b66` - Add OS Abyss trust gate for memory readmodels (#270)
- `8b2fc02` - Require subject-store trust gate for memory readmodels (#271)
- `79951a2` - Add memo KAG provider home (#272)
- `19b1e26` - Add repo-local KAG indexes (#274)
- `e11bc3b` - Enforce repo-local KAG index parity (#275)
- `d317041` - Pin deterministic repo-local KAG index gate (#276)
- `5e2104b` - Add repository KAG index family (#277)
- `166c8a7` - Reground stress recovery eval provenance (#279)
- `6eacb49` - Add the owner-local stats port (#280)
- `cfd98d6` - Publish canonical repository KAG indexes (#278)
- `40565fd` - Centralize validation command ownership (#281)
- `698d823` - Align memo KAG topology and artifact admission (#282)

## [0.4.0] - 2026-05-24

### Summary

- this release promotes `aoa-memo` from a broad memory-document surface into a
  contract-hardened memory organ with reviewed corpus bundles, reviewed intake
  landing, corpus-backed object read models, local memo-port contracts, and
  consumer-handoff/MCP access boundaries
- memo mechanics are reorganized into operation-shaped packages and physical
  `parts/` lanes, with generated mechanic indexes, readiness matrices,
  landing logs, root technical districts, AGENTS mesh coverage, validators, and
  tests keeping the topology inspectable
- portable skill/session-growth support, Titan/Agon follow-through, workspace
  retargeting, dry-run and self-repair guards, and release-compatible anchors
  are included while memory remains weaker than proof, routing, runtime state,
  role authority, and source-authored knowledge

### Added

- Add root `memo/` as the reviewed memory corpus district with object bundles,
  corpus support and intake lanes, a validator, tests, AGENTS mesh coverage,
  root-surface law, decision record, and release-gate wiring.
- Add reviewed intake landing so `reviewed_write` exports from local memo ports
  can become checked `memo/objects/` bundles with copied intake packets,
  schema-backed landing receipts, validator coverage, and regression tests.
- Back object-facing generated read models with reviewed corpus objects while
  preserving teaching fixtures and marking each generated row with
  `source_kind`.
- Promote the KAG donor bridge into the reviewed corpus so the source-owned
  memo export and object-facing read models route `aoa-kag` to
  `source_kind: reviewed_corpus` rather than a teaching fixture row.
- Clarify the `aoa_memo` MCP access plane as brief/search/status/validation,
  local packet preparation, and dry-run landing-plan support rather than
  durable reviewed memory authority.
- Add portable AoA skill foundation and session-growth support in the memo
  repo, including GitHub landing posture, traceability metadata, readiness
  guard refreshes, dry-run preview validation, malformed-shape preservation,
  and refreshed `aoa-summon`, self-diagnose, and automation-opportunity skill
  exports.
- Add semantic root districts for docs, config, schemas, examples, generated,
  scripts, and tests, with nearest `AGENTS.md` cards so each source family has
  a readable home, route, and validator.
- Add release-compatible public entrypoints for the workspace release auditor
  while keeping the active release procedure routed through `docs/root/` and
  the release gate through `scripts/release/`.
- Add `generated/root-topology/root_technical_districts.min.json` with builder, validator,
  release-gate coverage, and tests so root technical districts have a compact
  machine-readable atlas of role, route card, family ids, and local routing.
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
  `docs/README.md`, `docs/root/ROOT_SURFACE_LAW.md`, and `docs/decisions/` so
  future docs, agent-lane, and placement cleanup can route through explicit
  owner surfaces before moving flat memory docs.
- Add a source-backed AGENTS mesh with `config/agents/agents_mesh.json`,
  `generated/agents/agents_mesh.min.json`, mesh validators, and regression tests so
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
- Add a builder-backed quest projection check for `generated/quests/quest_catalog`
  and `generated/quests/quest_dispatch` surfaces so root quest companions are
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
- Add `scripts/mechanics/validate_mechanic_artifact_topology.py` to make root
  technical-district placement a direct release-gate validator rather than
  only a pytest regression.
- Add `config/root-topology/root_technical_districts.json` as an exact allowlist for root
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
  `generated/mechanics/mechanic_artifacts.min.json`, with builder, validator, release
  gate coverage, and tests so mechanic-local schemas, examples, config,
  generated outputs, scripts, tests, and manifests stay inspectable.
- Add `scripts/mechanics/validate_memo_mechanic_parts.py` to keep mechanic `PARTS.md`
  files operation-shaped, with Active Parts tables, source links, interface
  sections, release gate coverage, and regression tests.
- Add `generated/mechanics/memo_mechanic_readiness.min.json` with builder, validator,
  release gate coverage, root technical family contracts, and regression tests
  so every memo mechanic package has a machine-checkable OS Abyss readiness
  surface.
- Add `generated/mechanics/memo_mechanic_landing_logs.min.json` with builder,
  validator, release gate coverage, root technical family contracts, and
  regression tests so every memo mechanic package has a machine-checkable
  landing receipt surface.
- Extend `config/root-topology/root_technical_districts.json` with root generated-family
  contracts so every root `generated/` output names its owner surface, source
  refs, validators, and builders when generator-backed or projected.
- Extend the same root technical contract with script-family ownership so every
  root `scripts/` file names its role, owner surface, and release/test coverage
  refs.
- Extend the root technical contract with test-family ownership so every root
  `tests/` file and public fixture names its role, owner surface, and protected
  refs.

### Changed

- Re-ground the reviewed stress-recovery memory pattern on the current
  `aoa-evals/evals/comparison/longitudinal-window/` report path and rebuild its
  generated memory-object projections without changing recall authority.
- Tighten the reviewed memory consumer-handoff spine so downstream consumers
  retrieve reviewed object/read-model context while local memo ports, `.aoa`
  session evidence, reviewed intake, and `aoa_memo` MCP landing-plan dry runs
  keep separate authority boundaries.
- Retarget memo workspace paths to `/srv/AbyssOS`, land AoA v0.4.0 closeout
  follow-through, and preserve that route through the release-visible memory
  surfaces.
- Plant the Titan sixteenth-stage memory seed, require Titan audit owner-route
  hints, and align Titan audit examples with the route-hint schema.
- Harden portable skill exports, dry-run helper step shapes, malformed preview
  handling, donor-harvest self-repair handoff, and current audit follow-ups so
  agent-facing support remains bounded and traceable.
- Audit root AGENTS authority boundaries by keeping root route modes and
  executable validation commands in `AGENTS.md`, trimming adjacent README,
  CHARTER, and `DESIGN.AGENTS.md` duplicates, repairing stale legacy
  route-card script paths and stale Agon docs companion maps, clarifying Titan
  closeout wording, and adding mesh validation for neighboring-doc boundaries
  plus stale flat root script commands in `AGENTS.md`.
- Rename active memo-side `wave` and `seed` surfaces to stage/source naming
  while preserving legacy snapshots and source-owned upstream refs literally.
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

### Validation

- Historical run evidence remains in Git and CI history. Current executable
  routes live in `config/validation_lanes.json`, the nearest `AGENTS.md`, and
  the active release procedure.

### Notes

- the release body intentionally stays large: it preserves the accumulated
  `Unreleased` detail and adds a commit-by-commit reconciliation for the
  feature/history span through `b3e334e`
- the v0.4.0 release-preparation change itself is represented above by the
  release-compatible entrypoint, version, validation, and changelog bullets
- this release publishes memory, recall, writeback, topology, and release-gate
  contracts only; proof remains in `aoa-evals`, routing in `aoa-routing`, live
  runtime/storage in `abyss-stack`, role authority in `aoa-agents`, playbook
  choreography in `aoa-playbooks`, and source-authored meaning in its owning
  repositories

### Included in this release

- `6841ed8` - [codex] Plant Titan sixteenth wave seed
- `6de9427` - Add semantic AGENTS validation
- `fde9ff5` - Slim root AGENTS route card (#125)
- `625565b` - chore: retarget memo workspace paths to AbyssOS
- `2864e18` - Land AoA v0.4.0 memo closeout follow-through (#127)
- `6e808da` - Install portable AoA skill foundation
- `d771198` - Roll out session-growth skills and GitHub landing (#129)
- `6949078` - [codex] harden portable skills and traceability (#130)
- `50723dd` - Refresh session growth refs and readiness guard (#131)
- `1868baa` - Guard dry run preview step shape (#132)
- `e4c84b4` - Preserve dry run helper malformed shapes (#133)
- `e30542b` - Refresh shared AoA skill pack (#134)
- `75f49ec` - Require titan audit owner route hint (#135)
- `38bdb9c` - Address current aoa-memo audit findings
- `4d30734` - Refresh shared AoA skill pack (#137)
- `da316da` - Align Titan audit memory example with route hint schema
- `9680414` - Refresh aoa-summon skill export (#139)
- `63d41fa` - Refresh self-diagnose skill export
- `07f041d` - Add memo topology spine and move Spark lane
- `c258b09` - Add source-backed AGENTS mesh
- `bd3979c` - Move Agon docs into district
- `d7cbb21` - Move Titan docs into district
- `6cba5c6` - Move adoption writeback retention into memo mechanics
- `2aea796` - Add memo mechanics subroutes and artifact topology
- `3e61940` - Land Agon and Titan memo mechanics (#147)
- `32d1e9c` - Land antifragility memo mechanic (#148)
- `85921ae` - Land governance memo mechanic (#149)
- `9965c60` - Gate donor harvest self-repair handoff (#150)
- `f525232` - Add operation-first memo shape guard
- `c544ef6` - Add consumer handoff memo mechanic
- `4df2de7` - Add operational gate memo mechanic
- `eaed3d4` - Add recurrence support memo mechanic (#154)
- `34c7fdf` - Add lineage harvest memo mechanic
- `2bcd5d1` - Refresh automation opportunity skill contracts (#156)
- `25be2df` - Refactor mechanic artifact topology (#157)
- `4fec12f` - Add checkpoint memo mechanic (#158)
- `a0f6127` - Add readiness boundary memo mechanic (#159)
- `56303e8` - Add quest owner route projections (#160)
- `29f0d7d` - Add questbook lane-first mechanic
- `03b0be3` - Add root technical district allowlist
- `404a402` - Add mechanic artifact inventory
- `6af3ffd` - Validate memo mechanic parts shape
- `e5d4e6e` - Add root generated family contracts
- `132177a` - Add root script family contracts
- `a0fb807` - Add root test family contracts
- `e7371a2` - Add root schema family contracts
- `cd252d9` - Add root example family contracts
- `676d2b2` - Add root config manifest contracts
- `caca2d9` - Add mechanic readiness matrix
- `5133513` - Add mechanic route card index (#172)
- `2a1ebbb` - Add mechanic owner route matrix (#173)
- `68e34c9` - Add mechanic landing log index (#174)
- `e9dd653` - Move writeback self-agency examples (#175)
- `d638096` - Add questbook generated views part (#176)
- `bf0eacd` - Localize downstream feed tests (#177)
- `ce1d493` - Add retention local regression boundary (#178)
- `79dfec0` - Add mechanic readiness artifact test coverage (#179)
- `b79e03b` - Require local test routes for mechanics (#180)
- `2d536e3` - Materialize functional memo mechanic parts
- `27a2431` - Fix memo Codex review followups
- `00b86c0` - Move Agon artifacts into mechanic parts
- `15b5104` - Require runnable readiness test routes
- `d98d4c8` - Move Titan artifacts into mechanic parts
- `497c8ba` - Move adoption and retention artifacts into parts (#186)
- `51a8516` - Require runnable test modules for readiness
- `a84798d` - Move writeback artifacts into mechanic parts (#188)
- `1b9ebb8` - Move checkpoint artifacts into mechanic parts (#189)
- `eced8f2` - Move consumer handoff artifacts into parts (#190)
- `c7617e1` - Move governance artifacts into parts (#191)
- `f4998c5` - Move antifragility artifacts into parts (#192)
- `644271b` - Move operational gate artifacts into parts (#193)
- `6c9c07d` - Move remaining mechanic artifacts into parts (#194)
- `97217d3` - Restore mechanic legacy raw snapshots (#195)
- `e310e29` - Harden memo mechanic part naming (#196)
- `91d7214` - Fix mechanics atlas rendering (#197)
- `3f949fa` - Move mechanics runbook into AGENTS (#198)
- `fc2ea31` - Make AGENTS route cards functional (#199)
- `8f9041a` - Align root documents with memory index (#200)
- `d420146` - Compact README current contour (#201)
- `9d1232f` - Build registry-backed memo Spark lane (#202)
- `7d1df9c` - Compact root memo mechanics README
- `79bf26a` - Harden root contract family naming
- `e704b66` - Rename active memo stage source surfaces (#205)
- `b8c1f75` - Add root technical district atlas (#206)
- `1ab6ea2` - Refactor root semantic topology (#207)
- `97f1969` - Harden AGENTS authority boundaries (#208)
- `4d01950` - Calibrate memory operations plane
- `93cfc22` - Align local memo port standard (#210)
- `647e88a` - Add memo port v2 contracts (#211)
- `a786b58` - Route memo port index commands to AGENTS (#212)
- `b3ca1f4` - Harden local memo receipt checks (#213)
- `2553225` - Refresh memory route AGENTS mesh (#214)
- `1e78f42` - Add reviewed intake landing layer (#215)
- `ecc1a55` - Land abyss-stack memory pilot
- `4844182` - Harden reviewed intake landing refs (#217)
- `d3883e4` - Grow reviewed memory consumer spine (#218)
- `b3e334e` - Land reviewed memory consumer handoff spine

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

- Historical run evidence remains in Git and CI history. Current executable
  routes live in `config/validation_lanes.json`, the nearest `AGENTS.md`, and
  the active release procedure.

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

- Historical run evidence remains in Git and CI history. Current executable
  routes live in `config/validation_lanes.json`, the nearest `AGENTS.md`, and
  the active release procedure.

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

- Historical run evidence remains in Git and CI history. Current executable
  routes live in `config/validation_lanes.json`, the nearest `AGENTS.md`, and
  the active release procedure.

### Notes

- detailed checkpoint recall, rollout-memory writeback, and growth-refinery
  changes for this patch remain enumerated below under `Added` and `Changed`

## [0.2.0] - 2026-04-10

### Summary

- this release adds runtime writeback landing gates, live receipt publishing, scope classes, capsule-backed recall, and checkpoint-growth memo surfaces
- memo schemas, JSONL publication boundaries, and writeback references are hardened across the live writeback loop
- `aoa-memo` remains the bounded memory and recall layer rather than source or proof authority

### Validation

- Historical run evidence remains in Git and CI history. Current executable
  routes live in `config/validation_lanes.json`, the nearest `AGENTS.md`, and
  the active release procedure.

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

- Historical run evidence remains in Git and CI history. Current executable
  routes live in `config/validation_lanes.json`, the nearest `AGENTS.md`, and
  the active release procedure.

### Notes

- this release is a repository release of memory contracts and derived memory surfaces, not a claim that memory should replace source truth or proof
