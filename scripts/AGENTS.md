# AGENTS.md

This file applies to helper and validator scripts under `scripts/`.

## Role of this directory

`scripts/` is the operational seam for `aoa-memo`.
It validates the memory layer, regenerates the object-facing surface family, and checks that examples, schemas, registry surfaces, and recall contracts stay aligned.

These scripts should remain small, reviewable, and honest about what they validate.
Do not turn them into hidden runtime infrastructure.

## Conditional route scope

- Above: root `AGENTS.md`, source docs, schemas, examples, config maps, and
  generated contracts decide what scripts may validate or build.
- Here: root scripts own shared validators, builders, and release-oriented
  checks.
- Below: mechanic-owned generators and validators belong under the owning
  package or part when the logic is local to one mechanic.

## Main script families

Keep the current split clear:

- `memory/validate_memo.py` is a profiled memory-contract validator; release
  lanes call `--profile schema`, `--profile memory-context`,
  `--profile runtime-boundary`, `--profile handoff-boundary`, or
  `--profile eval-boundary` instead of the historical broad gate
- `memory/validate_memo_corpus.py` checks the reviewed `memo/` corpus shape,
  object bundles, source refs, and local-port separation
- `memory/validate_memory_surfaces.py` checks the doctrine family under `generated/memory/` plus router-facing recall contracts
- `memory/generate_memory_object_surfaces.py` rebuilds the object-facing family
  from curated examples into `generated/memory-objects/`; source loading,
  shared projection helpers, and item rendering live in separate
  `memory_object_surface_*` modules
- `memory/validate_memory_object_surfaces.py` checks manifest coverage, determinism, lifecycle integrity, and object-facing recall contracts
- `memory/validate_lifecycle_audit_examples.py` checks lifecycle, provenance-thread, and audit-event example integrity
- `memory/build_memory_operational_readouts.py` rebuilds access-plane
  currentness, source-lane intake wave, and workspace memo-port status readouts
  while keeping `abyss-stack` and `8Dionysus` as stronger owners; live access
  probes, source-wave projection, and workspace-port projection live in
  separate `memory_operational_*` modules
- `mechanics/validate_mechanic_artifact_topology.py` keeps single-mechanic schemas,
  examples, config inputs, generated outputs, scripts, tests, and manifests out
  of root technical districts, and checks that root `generated/` outputs belong
  to explicit generated-family contracts; its family-contract implementation
  lives in `mechanics/mechanic_artifact_family_contracts.py` and shared root
  topology helpers live in `mechanics/mechanic_artifact_topology_common.py`
- `mechanics/build_mechanic_artifact_inventory.py` and
  `mechanics/validate_mechanic_artifact_inventory.py` keep
  `generated/mechanics/mechanic_artifacts.min.json` aligned with package-local and
  part-local mechanic artifact homes
- `root-topology/build_root_technical_districts_index.py` and
  `root-topology/validate_root_technical_districts_index.py` keep
  `generated/root-topology/root_technical_districts.min.json` aligned with the root
  technical district contract in `config/root-topology/root_technical_districts.json`
- `root-topology/build_decision_indexes.py` keeps
  `docs/decisions/indexes/` aligned with canonical decision IDs and decision
  `Index Metadata`; parsing, rendering, and contract validation are split into
  `decision_index_*` helpers
- quest projection building belongs to `mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py`
- `memory/validate_nested_agents.py` checks that local guidance files stay present and explicit
- `agents/validate_agents_mesh.py`, `agents/build_agents_mesh_index.py`, and `agents/validate_agents_mesh_index.py` keep the source-backed AGENTS mesh aligned with current route cards
- `root-topology/validate_docs_districts.py` keeps retired docs districts and moved flat docs
  from drifting back into active docs-root sprawl
- `root-topology/validate_validator_topology.py` keeps validator layers,
  command lane metadata, source-fast boundaries, release composition, and
  route-away declarations aligned with `docs/validation/VALIDATOR_TOPOLOGY.md`;
  shared constants, path refs, and helper checks live in
  `root-topology/validator_topology_common.py`
- `mechanics/validate_memo_mechanic_parts.py` keeps package `PARTS.md` files in the
  operation-first Active Parts plus Interface shape and requires physical
  `parts/<part>/README.md`, `CONTRACT.md`, and `VALIDATION.md` nodes
- `mechanics/build_memo_mechanic_cards.py` and `mechanics/validate_memo_mechanic_cards.py` keep a
  compact generated route-card index aligned with package README mechanic cards
- `mechanics/build_memo_mechanic_owner_routes.py` and
  `mechanics/validate_memo_mechanic_owner_routes.py` keep a compact generated
  owner-route matrix aligned with package `OWNER_MAP.md` files and card refs
- `mechanics/build_memo_mechanic_landing_logs.py` and
  `mechanics/validate_memo_mechanic_landing_logs.py` keep a compact generated landing
  receipt index aligned with package `LANDING_LOG.md` files, validation
  routes, and stop-lines
- `mechanics/build_memo_mechanic_readiness.py` and
  `mechanics/validate_memo_mechanic_readiness.py` keep a compact readiness matrix for
  every mechanic package, tying package cards, owner maps, stop-lines,
  validation routes, and package-local or part-local artifacts together; the
  readiness helper stack is split into constants, build, and validation modules
- `config/root-topology/root_technical_districts.json` groups every root script into a
  `script_families` contract so root scripts stay release-oriented, covered,
  and owned rather than merely allowed by path
- `config/validation_lanes.json`, `validation_lanes.py`, `ci_gate.py`, and
  `release/release_check.py` keep validation command authority in one manifest
  while Python remains orchestration, not doctrine
- `release/validate_local_stats_port.py` is a thin boundary adapter to the pinned
  `aoa-stats` validator; memo-local statistical meaning stays under `stats/`
- `docs/validation/validator_inventory.json` records validation-like
  entrypoints, lane-backed generated checks, compatibility wrappers, and manual
  validators so root scripts do not become unlabeled historical gates

Mechanic-owned generators and validators live under the owning package, for
example `mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py`,
`mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_targets.py`, and
`mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_memo_prebindings.py`.

## Editing posture

When editing scripts here:

- preserve small, direct validator logic over framework sprawl
- keep error messages specific and reviewable
- do not silently widen repository ownership from memory semantics into routing, proof, or runtime policy
- keep generator behavior deterministic
- keep KAG export generation source-owned and bridge-focused rather than widening into a graph substrate pack
- avoid adding hidden network calls, secret handling, or environment-specific assumptions

If a validator starts depending on a new contract, update the matching nested `AGENTS.md`, examples, schemas, and generated surfaces together.

When validating recall contracts with a compact intermediate step, keep
`capsule_surface` checks explicit and local-ref-based. Validators here should
confirm family alignment without turning capsules into routing policy.

## Validation

After changing scripts, run the affected entrypoints directly. For broad script
verification, use lane ids rather than copying the full lane sequence into this
route card:
For validation lane orchestration changes, also run:
For generator changes, use the declared source builder and nearest `VALIDATION.md` route.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
