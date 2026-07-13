# Release Tool Compatibility Entrypoints

- Decision ID: AOA-MEM-D-0068

## Status

Accepted on 2026-05-24.

## Index Metadata

- Original date: 2026-05-24
- Surface classes: validation guard, release/tooling
- Mechanic parents: none
- Guard families: release/tooling
- Memory object classes: none
- Posture: active rationale

## Context

The active `aoa-memo` release procedure had moved into `docs/root/RELEASING.md`
and the release gate had moved into `scripts/release/release_check.py` as part
of the root semantic topology work. That topology is still correct: release
procedure belongs with root law, and release validation belongs in the
release-script district.

The workspace release publisher still probes the legacy public paths
`docs/RELEASING.md` and `scripts/release_check.py` during preflight. Without
those entrypoints, the repository can be locally green while the workspace
release route refuses to publish.

## Decision

Add thin compatibility entrypoints:

- `docs/RELEASING.md` points to `docs/root/RELEASING.md` and carries no
  independent release policy.
- `scripts/release_check.py` delegates to `scripts/release/release_check.py`.

The active route remains `docs/root/RELEASING.md` and
`scripts/release/release_check.py`. The compatibility files exist only so the
workspace release auditor and publisher can keep using stable public probes.

## Alternatives

Updating only the workspace release tool was rejected for this release because
`aoa-memo` still needs to be publishable from the current shared release plane.

Publishing manually through GitHub was rejected because the repository release
procedure names the shared AoA release publisher as the owner route.

Duplicating the full release procedure into `docs/RELEASING.md` was rejected
because it would create two release-policy surfaces.

## Consequences

- `docs/` root now permits one extra flat file, but only as a release-tool
  compatibility pointer.
- The root technical district contract includes `scripts/release_check.py` as
  part of the release gate family.
- Future release-tool updates may remove the compatibility need, but until
  then the thin entrypoints should remain in sync with the active route.

## Affected Surfaces

- `docs/RELEASING.md`
- `docs/root/RELEASING.md`
- `docs/root/ROOT_SURFACE_LAW.md`
- `docs/README.md`
- `scripts/release_check.py`
- `scripts/release/release_check.py`
- `config/root-topology/root_technical_districts.json`
- `generated/root-topology/root_technical_districts.min.json`
- `scripts/root-topology/validate_docs_districts.py`
- `CHANGELOG.md`

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
