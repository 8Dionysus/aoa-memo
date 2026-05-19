# Consumer Handoff Part-Local Artifacts

## Context

Consumer-handoff already had functioning parts, but its active schemas,
examples, generated KAG export, generator, and local regression tests still
lived at the package level.

That made `parts/` descriptive rather than operational for the surfaces that
neighboring owners actually consume.

## Decision

Move consumer-handoff technical artifacts to the nearest functioning part:

- bridge object chain, chunk face, and graph face under
  `parts/kag-tos-bridge-handoff/`
- source-owned KAG donor export, generator, and bridge-record source contract
  under `parts/kag-source-export/`
- eval guardrail pack schema and example under `parts/eval-guardrail-handoff/`
- playbook memory-scope regression under `parts/playbook-scope-handoff/`
- consumer feed and mechanic regression tests under
  `parts/downstream-feed-regression/`

Keep package docs as the authored handoff doctrine and keep generated root
companions as derived inspection surfaces.

## Alternatives

Leaving artifacts under package-level `schemas/`, `examples/`, `generated/`,
`scripts/`, and `tests/` would preserve shorter paths but leave the active
parts without the contracts they operate.

Moving everything into a generic package-local artifact directory would reduce
root sprawl but would still hide ownership from the part topology.

## Consequences

Consumer-handoff parts are now executable owner nodes: each runnable artifact
has a part-local home, and downstream validators point at the owning part.

The move keeps `aoa-memo` below stronger owners. It does not grant role policy,
playbook choreography, eval verdicts, KAG graph truth, ToS source meaning,
route dispatch, or runtime execution.

## Affected Surfaces

- `mechanics/consumer-handoff/PARTS.md`
- `mechanics/consumer-handoff/PROVENANCE.md`
- `mechanics/consumer-handoff/parts/*`
- `mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md`
- `mechanics/consumer-handoff/docs/MEMORY_EVAL_GUARDRAILS.md`
- `scripts/validate_memo.py`
- `generated/memo_registry.min.json`
- `generated/mechanic_artifacts.min.json`
- `generated/memo_mechanic_readiness.min.json`
- object-surface generated family

## Verification Route

Expected verification:

- `python mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py`
- `python scripts/generate_memory_object_surfaces.py`
- `python scripts/build_mechanic_artifact_inventory.py`
- `python scripts/build_memo_mechanic_landing_logs.py`
- `python scripts/build_memo_mechanic_readiness.py`
- `python scripts/build_agents_mesh_index.py`
- `python -m pytest -q mechanics/consumer-handoff/parts/downstream-feed-regression/tests mechanics/consumer-handoff/parts/playbook-scope-handoff/tests tests/test_memo_validators.py tests/test_cross_mechanic_candidate_contracts.py tests/test_roadmap_parity.py`
- `python scripts/release_check.py`
