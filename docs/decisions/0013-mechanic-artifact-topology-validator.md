# Decision: Mechanic Artifact Topology Gets A Release Gate

- Decision ID: AOA-MEM-D-0013

## Status

Accepted on 2026-05-18.

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-mechanic-artifact-topology-validator.md
- Surface classes: mechanic package, validation guard
- Mechanic parents: none
- Guard families: mechanic topology
- Memory object classes: none
- Posture: active rationale

## Context

`aoa-memo` moved many mechanic-owned schemas, examples, config seeds,
generated outputs, scripts, and tests out of root technical districts and into
their owning `mechanics/<slug>/` packages.

That placement was documented in `mechanics/ARTIFACT_TOPOLOGY.md` and covered
by a pytest regression, but the rule was not yet an explicit release-gate
validator. That left the topology easy to miss during non-pytest validation
passes.

## Decision

Add `scripts/validate_mechanic_artifact_topology.py` as the direct validator
for root technical district placement.

The validator keeps known single-mechanic artifact families out of root
`config/`, `examples/`, `generated/`, `schemas/`, `scripts/`, and `tests/`, and
keeps root `manifests/` reserved for shared manifests only.

Wire the validator into `scripts/release_check.py` and route cards so future
mechanic topology changes run it explicitly.

## Consequences

- Root technical districts remain available for public, shared, repo-wide
  memory-object contracts and release validators.
- Single-mechanic artifacts must stay with their owning package unless a
  stronger source-of-truth decision changes the topology.
- Release validation now catches root artifact drift before pytest is the only
  backstop.

## Validation

```bash
python scripts/validate_mechanic_artifact_topology.py
python -m pytest -q tests/test_mechanic_artifact_topology.py
python scripts/release_check.py
```
