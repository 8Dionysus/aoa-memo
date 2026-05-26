# Decision: Root Scripts Use Family Contracts

- Decision ID: AOA-MEM-D-0035

## Status

Accepted on 2026-05-18.

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-root-script-family-contracts.md
- Surface classes: root/topology, validation guard
- Mechanic parents: none
- Guard families: root technical district
- Memory object classes: none
- Posture: active rationale

## Context

`config/root_technical_districts.json` made root scripts exact by path, but an
exact path list still does not say why a script belongs in root or how it is
covered.

Root `scripts/` contains several different roles: the release orchestrator,
repo-wide validators, generated-surface builders, imported helper modules, and
AGENTS/docs shape validators. Without a machine-readable role map, a future
script could become root-owned only by appearing in the allowlist.

## Decision

Extend `config/root_technical_districts.json` to schema version
`aoa_memo_root_technical_districts_v3` and add `script_families`.

Each root script must now belong to exactly one family that names:

- `id`
- `role`
- `owner_surface`
- `scripts`
- `covered_by`

Extend `scripts/validate_mechanic_artifact_topology.py` so the release gate
checks script-family coverage against the root scripts allowlist.

Also run `scripts/validate_semantic_agents.py` directly from
`scripts/release_check.py` so semantic AGENTS guidance is a release-gate check,
not only a pytest-loaded helper.

## Tradeoffs

This keeps root script ownership in the same root technical contract as
generated ownership. The config becomes larger, but the alternative would split
script role truth into prose and leave the allowlist as the only machine check.

The contract does not make root scripts runtime infrastructure. Root scripts
remain small validators, builders, helpers, and release checks for public
memo-layer surfaces.

## Consequences

- New root scripts cannot land without a named family and coverage refs.
- Imported helper modules stay visible as helper members of a covered family.
- Mechanic-owned builders and validators continue to live under
  `mechanics/<slug>/scripts/`.
- Semantic AGENTS guidance is checked directly by `scripts/release_check.py`.

## Affected Surfaces

- `config/root_technical_districts.json`
- `scripts/validate_mechanic_artifact_topology.py`
- `scripts/release_check.py`
- `tests/test_mechanic_artifact_topology.py`
- `AGENTS.md`
- `config/AGENTS.md`
- `scripts/AGENTS.md`
- `mechanics/ARTIFACT_TOPOLOGY.md`

## Validation

```bash
python scripts/validate_mechanic_artifact_topology.py
python scripts/validate_semantic_agents.py
python -m pytest -q tests/test_mechanic_artifact_topology.py tests/test_validate_semantic_agents.py
python scripts/release_check.py
```
