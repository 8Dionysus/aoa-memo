# Decision: Root Technical Districts Use An Exact Allowlist

## Status

Accepted on 2026-05-18.

## Context

The mechanics refactor moved many single-mechanic schemas, examples, generated
outputs, scripts, tests, manifests, and config seeds into `mechanics/<slug>/`.
The release gate already blocked known mechanic-owned file prefixes from
returning to root technical districts.

That was still a negative check. It could prove that known old families did not
come back, but it did not prove that every remaining root artifact was
deliberately root-owned.

## Decision

Add `config/root_technical_districts.json` as the exact source map for
remaining root technical artifacts under `config/`, `examples/`, `generated/`,
`manifests/`, `schemas/`, `scripts/`, and `tests/`.

Extend `scripts/validate_mechanic_artifact_topology.py` so it checks both:

- the positive allowlist of root-owned files
- the existing denylist for known single-mechanic artifact families

## Consequences

- New root technical artifacts must be explicitly justified as repo-wide or
  shared, or moved into a mechanic package.
- Route cards stay as the `AGENTS.md` exception and do not need to appear in
  the artifact allowlist.
- The root technical districts become auditable as a current-state contract,
  not only as historical cleanup.

## Validation

```bash
python scripts/validate_mechanic_artifact_topology.py
python scripts/release_check.py
```
