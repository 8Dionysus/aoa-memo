# Root Technical District Atlas

- Decision ID: AOA-MEM-D-0058

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-19
- Legacy path: docs/decisions/2026-05-19-root-technical-district-atlas.md
- Surface classes: root/topology, generated/readout
- Mechanic parents: none
- Guard families: root technical district, generated/read-model
- Memory object classes: none
- Posture: active rationale

## Context

Root `config/`, `examples/`, `generated/`, `manifests/`, `schemas/`,
`scripts/`, and `tests/` already had exact allowlist and family contracts in
`config/root_technical_districts.json`.

That contract was correct but dense. A human or agent trying to answer "what
does this root folder do, what is above it, and where does local material go"
had to read a long source map before seeing the route shape.

## Decision

Add `generated/root_technical_districts.min.json` as a compact generated atlas
for root technical districts.

The atlas is built from `config/root_technical_districts.json` and names:

- district path and route card
- root role and common use
- family ids
- allowed-file count
- local mechanic/part routing path
- narrow check command

The exact allowlist remains in `config/root_technical_districts.json`.
`mechanics/ARTIFACT_TOPOLOGY.md` remains the placement law.

## Consequences

- Root folders can be inspected through a small machine-readable map before
  opening the full contract.
- README and AGENTS cards can point to the atlas instead of duplicating the
  entire allowlist.
- The atlas is generated, so root district changes now require builder,
  validator, and release-gate parity.
- The change clarifies placement positively through role and route rather than
  adding another broad prohibition layer.

## Validation

This decision is validated through:

```bash
python scripts/validate_mechanic_artifact_topology.py
python scripts/build_root_technical_districts_index.py --check
python scripts/validate_root_technical_districts_index.py
python -m pytest -q tests/test_root_technical_districts_index.py
python scripts/release_check.py
```
