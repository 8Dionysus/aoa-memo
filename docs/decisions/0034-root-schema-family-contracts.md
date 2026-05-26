# Decision: Root Schemas Use Family Contracts

- Decision ID: AOA-MEM-D-0034

## Status

Accepted on 2026-05-18.

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-root-schema-family-contracts.md
- Surface classes: root/topology, validation guard
- Mechanic parents: none
- Guard families: root technical district
- Memory object classes: none
- Posture: active rationale

## Context

`config/root_technical_districts.json` already made root schemas exact by path.
That stopped mechanic-local schemas from silently returning to root
`schemas/`, but the remaining public schema canon still had only a flat
allowlist.

Root `schemas/` contains different contract roles: memory-object canon,
recall/posture contracts, shared support-object contracts, and generated
object-surface contracts. Those are repo-wide public contracts, but they should
not blur into one generic schema bucket.

Without a machine-readable family contract, a future root schema could be
allowed without naming its owner surface, source refs, or validators.

## Decision

Extend `config/root_technical_districts.json` to schema version
`aoa_memo_root_technical_districts_v5` and add `schema_families`.

Each root schema must now belong to exactly one family that names:

- `id`
- `role`
- `owner_surface`
- `schemas`
- `source_refs`
- `validators`

Extend `scripts/validate_mechanic_artifact_topology.py` so the release gate
checks schema-family coverage against the root schemas allowlist.

## Tradeoffs

This keeps public schema ownership in the same technical district contract as
generated, script, and test ownership. The config grows, but the alternative
would leave root schemas exact by path while hiding the stronger contract role
in prose.

The contract does not move public memory-object canon under a mechanic. Root
schemas remain root-owned when they define shared memory objects, recall or
posture contracts, support objects, or generated-surface contracts. Schemas
that serve only one memo mechanic still belong under `mechanics/<slug>/schemas/`.

## Consequences

- New root schemas cannot land without a named family, owner surface, source
  refs, and validators.
- Public schema roles stay distinct from package-local mechanic schemas.
- Generated object-surface schemas remain tied to their manifest and generated
  family.
- The release gate now detects missing schema-family contracts and family
  contracts that cover files outside the root schemas allowlist.

## Affected Surfaces

- `config/root_technical_districts.json`
- `scripts/validate_mechanic_artifact_topology.py`
- `tests/test_mechanic_artifact_topology.py`
- `config/AGENTS.md`
- `schemas/AGENTS.md`
- `mechanics/ARTIFACT_TOPOLOGY.md`

## Validation

```bash
python -m json.tool config/root_technical_districts.json >/dev/null
python scripts/validate_mechanic_artifact_topology.py
python -m pytest -q tests/test_mechanic_artifact_topology.py
python scripts/release_check.py
```
