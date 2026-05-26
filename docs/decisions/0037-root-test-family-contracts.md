# Decision: Root Tests Use Family Contracts

- Decision ID: AOA-MEM-D-0037

## Status

Accepted on 2026-05-18.

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-root-test-family-contracts.md
- Surface classes: root/topology, validation guard
- Mechanic parents: none
- Guard families: root technical district
- Memory object classes: none
- Posture: active rationale

## Context

`config/root_technical_districts.json` already made root tests exact by path.
That prevented mechanic-local tests from drifting back into root `tests/`, but
it still did not say why a remaining root regression belonged in root or which
surface it protected.

Root `tests/` now covers route-card mesh parity, docs topology, mechanics
indexes, generated-surface contracts, memory-object validation, downstream
feed seams, and agent companion skill behavior. Those are repo-wide and
cross-mechanic invariants, not one flat test pile.

Without a machine-readable family contract, a future test or fixture could be
accepted into root by allowlist only, without naming the owner surface or the
protected contract.

## Decision

Extend `config/root_technical_districts.json` to schema version
`aoa_memo_root_technical_districts_v4` and add `test_families`.

Each root test file or public fixture must now belong to exactly one family
that names:

- `id`
- `role`
- `owner_surface`
- `tests`
- `protects`

Extend `scripts/validate_mechanic_artifact_topology.py` so the release gate
checks test-family coverage against the root tests allowlist.

## Tradeoffs

This makes the root technical contract larger, but it keeps root placement,
generated ownership, script ownership, and regression ownership in one
auditable map.

The contract does not move package-local mechanic tests into root. It only
keeps repo-wide regression coverage explicit when the protected surface spans
root docs, generated companions, route cards, or multiple mechanics.

## Consequences

- New root tests cannot land without a named family and protected refs.
- Public fixtures in root `tests/fixtures/` are treated as regression
  artifacts, not loose data.
- Package-local mechanic tests continue to live under
  `mechanics/<slug>/tests/` when they only serve one package.
- The release gate now detects missing test-family contracts and family
  contracts that cover files outside the root tests allowlist.

## Affected Surfaces

- `config/root_technical_districts.json`
- `scripts/validate_mechanic_artifact_topology.py`
- `tests/test_mechanic_artifact_topology.py`
- `config/AGENTS.md`
- `tests/AGENTS.md`
- `mechanics/ARTIFACT_TOPOLOGY.md`

## Validation

```bash
python -m json.tool config/root_technical_districts.json >/dev/null
python scripts/validate_mechanic_artifact_topology.py
python -m pytest -q tests/test_mechanic_artifact_topology.py
python scripts/release_check.py
```
