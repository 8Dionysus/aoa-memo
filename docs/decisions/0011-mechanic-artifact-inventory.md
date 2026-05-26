# Mechanic Artifact Inventory

- Decision ID: AOA-MEM-D-0011

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-mechanic-artifact-inventory.md
- Surface classes: mechanic package
- Mechanic parents: none
- Guard families: mechanic topology
- Memory object classes: none
- Posture: active rationale

## Context

The root technical districts now have an exact allowlist, and single-mechanic
artifacts have moved under their owning packages.

That closes the root-sprawl problem, but it creates the next topology risk:
package-local `schemas/`, `examples/`, `config/`, `generated/`, `scripts/`,
`tests/`, and `manifests/` can become hard to audit if the only source of
truth is scattered filesystem placement.

`PARTS.md` should name functioning parts and contracts. It should not become a
raw file inventory.

## Decision

Add `generated/mechanic_artifacts.min.json` as a compact generated inventory of
tracked package-local mechanic artifacts.

The inventory is generated from the current package list in
`config/memo_mechanics.json` and the tracked files under
`mechanics/<slug>/{config,examples,generated,manifests,schemas,scripts,tests}/`.

It is checked by:

```bash
python scripts/build_mechanic_artifact_inventory.py --check
python scripts/validate_mechanic_artifact_inventory.py
```

The release gate runs both commands.

## Consequences

- Agents can inspect package-local artifact ownership without guessing from
  raw paths.
- Package cards and `PARTS.md` stay semantic instead of turning into file
  dumps.
- New package-local artifact files must keep the generated inventory current.
- The generated inventory does not author mechanic truth; source remains in
  package docs, package-local artifacts, `config/memo_mechanics.json`, and
  `mechanics/ARTIFACT_TOPOLOGY.md`.

## Boundaries

- The inventory does not make package-local generated files source truth.
- The inventory does not move artifacts into part-local homes by itself.
- The inventory does not replace the root technical district allowlist.
