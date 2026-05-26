# Mechanic Readiness Matrix

- Decision ID: AOA-MEM-D-0020

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-mechanic-readiness-matrix.md
- Surface classes: generated/readout, mechanic package, validation guard
- Mechanic parents: none
- Guard families: mechanic topology, generated/read-model
- Memory object classes: none
- Posture: active rationale

## Context

The mechanics tree now holds memo-side operations for antifragility, Agon,
Titan, adoption, governance, shape guard, checkpoint, readiness boundary,
consumer handoff, operational gate, recurrence support, lineage harvest,
Questbook, writeback, and retention.

Existing validators proved package shape, docs placement, parts-table shape,
and artifact ownership. They did not expose one compact machine surface that
answered whether every package was ready for OS Abyss use as a mechanic:
package card, owner split, stop-lines, validation route, legacy bridge, and
package-local artifacts together.

## Decision

Add `generated/memo_mechanic_readiness.min.json` as a generated companion built
from `config/memo_mechanics.json`, package-local route surfaces, and
`generated/mechanic_artifacts.min.json`.

The source truth remains the mechanic package surfaces. The readiness matrix is
a compact audit surface and release-gate target, not a new mechanic authority.

## Alternatives

- Keep readiness implicit in package files and tests. This preserves fewer
  generated files but makes OS Abyss consumption depend on scattered Markdown
  reads.
- Extend `generated/memo_mechanics.min.json` with every readiness detail. This
  would overload the package index and blur route orientation with operational
  readiness.
- Put readiness inside `mechanics/README.md`. This is human-readable, but not
  deterministic enough for release gates.

## Consequences

- Every mechanic package now has a machine-checkable readiness result.
- Release validation fails when a package card, owner map, parts map,
  provenance bridge, landing log, validation route, or stronger-owner stop-line
  stops satisfying the readiness contract.
- Root generated, script, and test technical districts must include the new
  builder, validator, generated output, and regression test in their family
  contracts.
- The matrix must stay downstream-readable without claiming proof, runtime,
  routing, role, KAG, source-owner, or playbook authority.

## Affected Surfaces

- `generated/memo_mechanic_readiness.min.json`
- `scripts/build_memo_mechanic_readiness.py`
- `scripts/validate_memo_mechanic_readiness.py`
- `scripts/mechanic_readiness_common.py`
- `tests/test_memo_mechanic_readiness.py`
- `config/root_technical_districts.json`
- `scripts/release_check.py`
- `mechanics/README.md`
- `mechanics/ARTIFACT_TOPOLOGY.md`

## Verification

Use:

```bash
python scripts/build_memo_mechanic_readiness.py --check
python scripts/validate_memo_mechanic_readiness.py
python scripts/validate_mechanic_artifact_topology.py
python -m pytest -q tests/test_memo_mechanic_readiness.py tests/test_mechanic_artifact_topology.py
python scripts/release_check.py
```
