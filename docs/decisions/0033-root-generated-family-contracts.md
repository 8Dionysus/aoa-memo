# Decision: Root Generated Outputs Use Family Contracts

- Decision ID: AOA-MEM-D-0033

## Status

Accepted on 2026-05-18.

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-root-generated-family-contracts.md
- Surface classes: root/topology, generated/readout, validation guard
- Mechanic parents: none
- Guard families: root technical district, generated/read-model
- Memory object classes: none
- Posture: active rationale

## Context

`config/root_technical_districts.json` already made root technical artifacts
explicit. That prevented unlisted files from drifting back into root
`generated/`, but it still treated root generated outputs as a flat allowlist.

That was not enough for the mechanics refactor. Root `generated/` contains
different kinds of public companions: source-authored registry metadata,
checked-in doctrine reader surfaces, generator-backed object and route-card
families, package-local artifact inventory, and Questbook projections.

Without a machine-readable family contract, a new root generated output could
be allowed without naming its owner surface, source refs, builder, or validator.

## Decision

Extend `config/root_technical_districts.json` to schema version
`aoa_memo_root_technical_districts_v2` and add `generated_families`.

Each root generated output must now belong to exactly one family that names:

- `id`
- `source_kind`
- `owner_surface`
- `source_refs`
- `outputs`
- `validators`
- `builders` when the family is generator-backed or a projection

Extend `scripts/validate_mechanic_artifact_topology.py` so the release gate
checks this family contract in addition to the root technical allowlist.

## Tradeoffs

Keeping this in `config/root_technical_districts.json` makes the root technical
contract larger, but it keeps placement and generated-family ownership in one
auditable source map instead of splitting generated authority into a second
partial config.

The contract does not make generated outputs source truth. It only names how
each root generated output stays owned, sourced, rebuilt, or validated.

## Consequences

- Root generated outputs cannot be added as anonymous files.
- Source-authored, checked-in-derived, generator-backed, and projection
  surfaces remain distinguishable.
- Mechanic-owned generated outputs continue to live in package-local
  `mechanics/<slug>/generated/` homes.
- The release gate now detects both missing generated-family contracts and
  generated-family contracts that cover files outside the root generated
  allowlist.

## Affected Surfaces

- `config/root_technical_districts.json`
- `scripts/validate_mechanic_artifact_topology.py`
- `tests/test_mechanic_artifact_topology.py`
- `generated/AGENTS.md`
- `mechanics/ARTIFACT_TOPOLOGY.md`
- `config/AGENTS.md`

## Validation

```bash
python scripts/validate_mechanic_artifact_topology.py
python -m pytest -q tests/test_mechanic_artifact_topology.py
python scripts/release_check.py
```
