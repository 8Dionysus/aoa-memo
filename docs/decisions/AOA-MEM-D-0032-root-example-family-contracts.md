# Decision: Root Examples Use Family Contracts

- Decision ID: AOA-MEM-D-0032

## Status

Accepted on 2026-05-18.

## Index Metadata

- Original date: 2026-05-18
- Surface classes: root/topology, validation guard
- Mechanic parents: none
- Guard families: root technical district
- Memory object classes: none
- Posture: active rationale

## Context

`config/root_technical_districts.json` already made root examples exact by
path. That prevented mechanic-local examples from drifting back into root
`examples/`, but the remaining public examples still had only a flat allowlist.

Root `examples/` contains several different roles: base memory-object examples,
lifecycle/audit examples, Phase Alpha thread examples, recall contracts,
support contracts, the memory-object surface manifest, and self-agency
continuity relay examples. They are public and shared, but they should not
become one anonymous example bucket.

Without a machine-readable family contract, a future root example could be
allowed without naming its owner surface, source refs, or validators.

## Decision

Extend `config/root_technical_districts.json` to schema version
`aoa_memo_root_technical_districts_v6` and add `example_families`.

Each root example must now belong to exactly one family that names:

- `id`
- `role`
- `owner_surface`
- `examples`
- `source_refs`
- `validators`

Extend `scripts/validate_mechanic_artifact_topology.py` so the release gate
checks example-family coverage against the root examples allowlist.

## Tradeoffs

This makes the root technical contract larger, but it keeps public example
ownership in the same auditable map as schema, generated, script, and test
ownership.

The contract does not move shared examples under one mechanic. Root examples
remain root-owned when they teach public memory-object shape, lifecycle/audit
posture, recall contracts, support contracts, generated-surface manifests, or
cross-family continuity. Examples that serve only one memo mechanic still
belong under `mechanics/<slug>/examples/`.

## Consequences

- New root examples cannot land without a named family, owner surface, source
  refs, and validators.
- Public shared examples stay distinct from package-local mechanic examples.
- Root lifecycle, recall, and generated-object examples keep their validator
  coverage visible from the root technical contract.
- The release gate now detects missing example-family contracts and family
  contracts that cover files outside the root examples allowlist.

## Affected Surfaces

- `config/root_technical_districts.json`
- `scripts/validate_mechanic_artifact_topology.py`
- `tests/test_mechanic_artifact_topology.py`
- `config/AGENTS.md`
- `examples/AGENTS.md`
- `mechanics/ARTIFACT_TOPOLOGY.md`

## Validation

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
