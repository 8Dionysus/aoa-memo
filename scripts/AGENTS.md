# AGENTS.md

This file applies to helper and validator scripts under `scripts/`.

## Role of this directory

`scripts/` is the operational seam for `aoa-memo`.
It validates the memory layer, regenerates the object-facing surface family, and checks that examples, schemas, registry surfaces, and recall contracts stay aligned.

These scripts should remain small, reviewable, and honest about what they validate.
Do not turn them into hidden runtime infrastructure.

## Route Stack

- Above: root `AGENTS.md`, source docs, schemas, examples, config maps, and
  generated contracts decide what scripts may validate or build.
- Here: root scripts own shared validators, builders, and release-oriented
  checks.
- Below: mechanic-owned generators and validators belong under the owning
  package or part when the logic is local to one mechanic.

## Main script families

Keep the current split clear:

- `memory/validate_memo.py` is the canonical memory-layer validator and now also checks nested guidance surfaces
- `memory/validate_memo_corpus.py` checks the reviewed `memo/` corpus shape,
  object bundles, source refs, and local-port separation
- `memory/validate_memory_surfaces.py` checks the doctrine family under `generated/memory/` plus router-facing recall contracts
- `memory/generate_memory_object_surfaces.py` rebuilds the object-facing family from curated examples into `generated/memory-objects/`
- `memory/validate_memory_object_surfaces.py` checks manifest coverage, determinism, lifecycle integrity, and object-facing recall contracts
- `memory/validate_lifecycle_audit_examples.py` checks lifecycle, provenance-thread, and audit-event example integrity
- `mechanics/validate_mechanic_artifact_topology.py` keeps single-mechanic schemas,
  examples, config inputs, generated outputs, scripts, tests, and manifests out
  of root technical districts, and checks that root `generated/` outputs belong
  to explicit generated-family contracts
- `mechanics/build_mechanic_artifact_inventory.py` and
  `mechanics/validate_mechanic_artifact_inventory.py` keep
  `generated/mechanics/mechanic_artifacts.min.json` aligned with package-local and
  part-local mechanic artifact homes
- `root-topology/build_root_technical_districts_index.py` and
  `root-topology/validate_root_technical_districts_index.py` keep
  `generated/root-topology/root_technical_districts.min.json` aligned with the root
  technical district contract in `config/root-topology/root_technical_districts.json`
- quest projection building belongs to `mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py`
- `memory/validate_nested_agents.py` checks that local guidance files stay present and explicit
- `agents/validate_agents_mesh.py`, `agents/build_agents_mesh_index.py`, and `agents/validate_agents_mesh_index.py` keep the source-backed AGENTS mesh aligned with current route cards
- `root-topology/validate_docs_districts.py` keeps retired docs districts and moved flat docs
  from drifting back into active docs-root sprawl
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
  validation routes, and package-local or part-local artifacts together
- `config/root-topology/root_technical_districts.json` groups every root script into a
  `script_families` contract so root scripts stay release-oriented, covered,
  and owned rather than merely allowed by path

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

After changing scripts, run the affected entrypoints directly. The common sequence is:

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memo_corpus.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
python scripts/memory/validate_lifecycle_audit_examples.py
python scripts/mechanics/validate_mechanic_artifact_topology.py
python scripts/mechanics/build_mechanic_artifact_inventory.py --check
python scripts/mechanics/validate_mechanic_artifact_inventory.py
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/agents/validate_semantic_agents.py
python scripts/root-topology/validate_docs_districts.py
python scripts/mechanics/validate_memo_mechanic_parts.py
python scripts/mechanics/build_memo_mechanic_cards.py --check
python scripts/mechanics/validate_memo_mechanic_cards.py
python scripts/mechanics/build_memo_mechanic_owner_routes.py --check
python scripts/mechanics/validate_memo_mechanic_owner_routes.py
python scripts/mechanics/build_memo_mechanic_landing_logs.py --check
python scripts/mechanics/validate_memo_mechanic_landing_logs.py
python scripts/mechanics/build_memo_mechanic_readiness.py --check
python scripts/mechanics/validate_memo_mechanic_readiness.py
```

If generator logic changed, also run:

```bash
python scripts/memory/generate_memory_object_surfaces.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py
python mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_targets.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_intake.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_growth_refinery_writeback_lanes.py
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_phase_alpha_writeback_map.py
```
