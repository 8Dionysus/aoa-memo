# Decision: Root Config and Manifest Control Plane Is Explicit

- Decision ID: AOA-MEM-D-0031

## Status

Accepted on 2026-05-18.

## Index Metadata

- Original date: 2026-05-18
- Surface classes: root/topology
- Mechanic parents: none
- Guard families: root technical district
- Memory object classes: none
- Posture: active rationale

## Context

`config/root_technical_districts.json` already made root `config/` and
`manifests/` exact by path. That prevented unlisted files from drifting into
the root control plane, but it still left two gaps:

- root config files were allowlisted without a machine-readable source-map
  family
- root manifests were empty by convention rather than by an explicit reserved
  policy

Root `config/` now contains three repo-wide source maps: AGENTS mesh, memo
mechanics, and root technical districts. Root `manifests/` is intentionally
empty until a shared recurrence manifest exists.

## Decision

Extend `config/root_technical_districts.json` to schema version
`aoa_memo_root_technical_districts_v7`.

Add `config_families`. Each root config file must now belong to exactly one
family that names:

- `id`
- `role`
- `owner_surface`
- `configs`
- `source_refs`
- `validators`

Add `manifest_policy` with `id` `root_manifests_reserved`. It must name the
reserved shared-manifest role, owner surface, source refs, validators, and an
`allowed_files` list that matches the root `manifests.allowed_files` district.

Extend `scripts/validate_mechanic_artifact_topology.py` so the release gate
checks config-family coverage and manifest-policy consistency.

## Tradeoffs

This adds another layer to the root technical contract, but it closes the last
root technical districts named by the mechanics refactor without moving
repo-wide source maps into package-local homes.

The manifest policy is not a fake active manifest family. It records that root
`manifests/` is currently reserved-empty and that mechanic-local manifests
belong under their owning mechanic.

## Consequences

- New root config files cannot land without a named source-map family.
- Root manifest files cannot appear without updating both the district
  allowlist and the manifest policy.
- The release gate now detects anonymous root config drift and manifest policy
  drift.
- Config and manifests remain control-plane support, not memory truth.

## Affected Surfaces

- `config/root_technical_districts.json`
- `scripts/validate_mechanic_artifact_topology.py`
- `tests/test_mechanic_artifact_topology.py`
- `config/AGENTS.md`
- `manifests/AGENTS.md`
- `mechanics/ARTIFACT_TOPOLOGY.md`

## Validation

```bash
python -m json.tool config/root_technical_districts.json >/dev/null
python scripts/validate_mechanic_artifact_topology.py
python -m pytest -q tests/test_mechanic_artifact_topology.py
python scripts/release_check.py
```
