# AGENTS.md

This file applies to checked-in artifacts under `generated/`.

## Important split

`generated/` contains shared memo surface classes:

- `memory/memo_registry.min.json` is the compact machine-readable registry surface for the layer
- the doctrine family lives under `memory/` as `memory_catalog.json`, `memory_catalog.min.json`, `memory_capsules.json`, and `memory_sections.full.json`
- the operational readout family lives under `memory/` as
  `access_plane_currentness.min.json`, `source_intake_wave.min.json`, and
  `workspace_memo_port_status.min.json`
- the object family lives under `memory-objects/` as `memory_object_catalog.json`, `memory_object_catalog.min.json`, `memory_object_capsules.json`, and `memory_object_sections.full.json`
- `agents/agents_mesh.min.json` is the compact companion mirror for current AGENTS route-card coverage
- `root-topology/root_technical_districts.min.json` is the compact atlas for root technical
  district purpose, route cards, family ids, and local routing
- `mechanics/mechanic_artifacts.min.json` is the compact generated inventory of
  package-local mechanic artifact homes
- `mechanics/memo_mechanic_cards.min.json` is the compact generated mirror of current
  mechanic README route cards
- `mechanics/memo_mechanic_owner_routes.min.json` is the compact generated owner-route
  matrix for current mechanic packages
- `mechanics/memo_mechanic_landing_logs.min.json` is the compact generated landing
  receipt index for current mechanic packages
- `mechanics/memo_mechanic_readiness.min.json` is the compact generated readiness matrix
  for current mechanic packages
- `quests/quest_catalog.min*.json` and `quests/quest_dispatch.min*.json` are compact public quest projections from `quests/memo/<state>/AOA-MEM-Q-*.yaml`

Do not treat every file here as the same kind of artifact.

Mechanic-owned generated artifacts do not live in root `generated/`. They belong
under the owning package or the nearest functioning part, for example
`mechanics/consumer-handoff/parts/kag-source-export/generated/`,
`mechanics/writeback/parts/runtime-and-temperature/generated/`, or
`mechanics/agon/parts/bridge-and-evidence-seams/generated/`.

## Route Stack

- Above: source docs, schemas, examples, config maps, quest sources, and
  mechanic package cards own meaning.
- Here: root `generated/` holds compact shared companions for inspection,
  recall, route-card coverage, mechanics readiness, and quest projections.
- Below: package-local generated artifacts stay under the owning mechanic or
  part. Do not copy them into root for convenience.

## Source and derivation map

Keep this split explicit:

- `generated/memory/memo_registry.min.json` is a source-authored registry contract validated by `scripts/memory/validate_memo.py`
- the doctrine family is a checked-in router-facing memo surface family validated by `scripts/memory/validate_memory_surfaces.py`
- the operational readout family is rebuilt by
  `scripts/memory/build_memory_operational_readouts.py` from memo generated
  surfaces plus read-only `8Dionysus` workspace-map and `abyss-stack` MCP
  inputs, and checked by the same builder in `--check` mode
- the object family is generator-backed and is rebuilt by `scripts/memory/generate_memory_object_surfaces.py`, checked by `scripts/memory/validate_memory_object_surfaces.py`, and wrapped for OS Abyss ABI/provenance plus durable subject-store trust gating by `docs/memory/artifact-bundles/memory_object_readmodels.bundle.json`
- the quest projection family is rebuilt by `mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py` from lane-first quest sources, governed by `mechanics/questbook/parts/quest-read-model-projections/`, and checked by `scripts/memory/validate_memo.py`
- `mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json` is rebuilt by `mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py` and checked by `scripts/memory/validate_memo.py`
- `mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json` is generator-backed, rebuilt by `mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py`, and checked by `scripts/memory/validate_memo.py`
- `generated/agents/agents_mesh.min.json` is rebuilt by `scripts/agents/build_agents_mesh_index.py` from `config/agents/agents_mesh.json` and checked by `scripts/agents/validate_agents_mesh_index.py`
- `generated/root-topology/root_technical_districts.min.json` is rebuilt by
  `scripts/root-topology/build_root_technical_districts_index.py` from
  `config/root-topology/root_technical_districts.json` and checked by
  `scripts/root-topology/validate_root_technical_districts_index.py`
- `generated/mechanics/mechanic_artifacts.min.json` is rebuilt by
  `scripts/mechanics/build_mechanic_artifact_inventory.py` from tracked package-local
  artifact homes and checked by `scripts/mechanics/validate_mechanic_artifact_inventory.py`
- `generated/mechanics/memo_mechanic_cards.min.json` is rebuilt by
  `scripts/mechanics/build_memo_mechanic_cards.py` from package README mechanic cards
  and checked by `scripts/mechanics/validate_memo_mechanic_cards.py`
- `generated/mechanics/memo_mechanic_owner_routes.min.json` is rebuilt by
  `scripts/mechanics/build_memo_mechanic_owner_routes.py` from package `OWNER_MAP.md`
  files plus mechanic card owner refs, and checked by
  `scripts/mechanics/validate_memo_mechanic_owner_routes.py`
- `generated/mechanics/memo_mechanic_landing_logs.min.json` is rebuilt by
  `scripts/mechanics/build_memo_mechanic_landing_logs.py` from package `LANDING_LOG.md`
  receipts, and checked by `scripts/mechanics/validate_memo_mechanic_landing_logs.py`
- `generated/mechanics/memo_mechanic_readiness.min.json` is rebuilt by
  `scripts/mechanics/build_memo_mechanic_readiness.py` from package cards, source maps,
  landing logs, and the artifact inventory, then checked by
  `scripts/mechanics/validate_memo_mechanic_readiness.py`

`config/root-topology/root_technical_districts.json` is the machine-readable source for the
root generated family contract. Every root generated output must appear in
exactly one `generated_families` entry with its owner surface, source refs,
outputs, validators, and builders when the output is generator-backed or a
projection.

The object family is derived from reviewed corpus bundles under `memo/objects/`
plus curated teaching fixtures in
`examples/generated-surfaces/memory_object_surface_manifest.json` and the
referenced memory-object examples. Generated rows use `source_kind` to keep
reviewed corpus objects distinct from teaching fixtures.

## Editing posture

For `memo_registry.min.json`:

- edit carefully because it is canonical memory-layer registry metadata
- preserve stable ids, schema refs, doc refs, and validation command listings unless semantics truly changed

For the doctrine family:

- keep `memory_catalog.json`, `memory_catalog.min.json`, `memory_capsules.json`, and `memory_sections.full.json` aligned as one readable family
- preserve stable surface ids and source paths unless the underlying doctrine changed
- do not turn router-facing surfaces into workflow policy or proof verdicts

For the operational readout family:

- Do not hand-edit `access_plane_currentness.min.json`,
  `source_intake_wave.min.json`, or `workspace_memo_port_status.min.json`
- regenerate them with `python scripts/memory/build_memory_operational_readouts.py --write --live` in the workspace
- keep `8Dionysus` as workspace-map owner and `abyss-stack` as MCP runtime owner
- keep known gaps routed instead of inflating MCP output into memory truth

For the object family:

- Do not hand-edit `memory_object_catalog.json`, `memory_object_catalog.min.json`, `memory_object_capsules.json`, or `memory_object_sections.full.json`
- regenerate the family from reviewed corpus bundles plus curated examples
- keep `source_kind` visible so generated read models do not confuse fixtures
  with reviewed memory truth
- keep object-facing exports deterministic and reviewable
- keep `docs/memory/artifact-bundles/memory_object_readmodels.bundle.json`
  aligned when the public subject set, `artifact_identity`, or consumer
  expectation changes; release/export consumers must use the durable registry,
  materialized subject-store, and trust-gate path before treating the family as
  recall support

For mechanic-owned generated outputs:

- Do not hand-edit package-local generated files from root
- update the owning mechanic source artifacts first
- run the owning package generator, then the root validator that consumes it
- do not copy mechanic generated files back into root `generated/`

For `agents_mesh.min.json`:

- Do not hand-edit it
- update `config/agents/agents_mesh.json` and the affected local `AGENTS.md` cards first
- rebuild it with `python scripts/agents/build_agents_mesh_index.py`
- keep it a route-card coverage companion, not source memory doctrine

For `root_technical_districts.min.json`:

- Do not hand-edit it
- update `config/root-topology/root_technical_districts.json` and the affected root district
  `AGENTS.md` first
- rebuild it with `python scripts/root-topology/build_root_technical_districts_index.py`
- keep it a compact atlas for root district routing, not the exact allowlist

For the quest projection family:

- Do not hand-edit `generated/quests/quest_catalog.min*.json` or `generated/quests/quest_dispatch.min*.json`
- update `quests/memo/<state>/AOA-MEM-Q-*.yaml`, `QUESTBOOK.md`, and the owning mechanic docs first
- rebuild with `python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py`
- keep `owner_surface` and `anchor_ref` routed to real memo docs or mechanics docs
- keep the read-model projection placement contract in `mechanics/questbook/parts/quest-read-model-projections/`

## Validation

When this directory changes, run the matching checks:

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
python scripts/memory/validate_abyss_machine_memory_object_bundle.py
python scripts/memory/build_memory_operational_readouts.py --check
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
python scripts/mechanics/validate_mechanic_artifact_inventory.py
python scripts/mechanics/validate_memo_mechanic_cards.py
python scripts/mechanics/validate_memo_mechanic_owner_routes.py
python scripts/mechanics/validate_memo_mechanic_landing_logs.py
python scripts/mechanics/validate_memo_mechanic_readiness.py
```

If the object family or mechanic-generated outputs changed, also run the
matching generator:

```bash
python scripts/memory/generate_memory_object_surfaces.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py
python mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py
```
