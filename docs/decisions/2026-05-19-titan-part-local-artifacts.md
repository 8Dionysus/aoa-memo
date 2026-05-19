# Titan Part-Local Artifacts

## Context

Titan was already a memo mechanic with functioning parts, but its runnable
schemas, examples, and tests still lived directly under `mechanics/titan/`.
That kept the package usable, yet it made the active parts less operational
than Agon and left future Titan additions with an ambiguous artifact home.

`mechanics/ARTIFACT_TOPOLOGY.md` says that once a mechanic has functioning
parts, single-mechanic artifacts should move to the nearest part-local home.

## Decision

Titan schemas, examples, and tests now live under the part that owns their
memory operation:

- `parts/core-memory-posture/` owns recall, writeback, and remembrance record
  artifacts.
- `parts/closeout-and-digest-posture/` owns bridge, closeout, console, and
  digest candidate artifacts.
- `parts/specialized-policy/` owns audit-memory candidate artifacts.

The package-level Titan directory remains the route card, owner map,
provenance, roadmap, and source-doc home. It does not keep active artifact
aliases.

## Alternatives

Keeping artifacts at `mechanics/titan/{schemas,examples,tests}` would preserve
the previous package-local shape, but it would make parts descriptive rather
than functional.

Moving Titan docs into parts was rejected for this slice. The docs still work
as the shared source family map for the Titan mechanic; only runnable contract
artifacts needed the narrower owner.

## Consequences

Future Titan artifact additions should start in `mechanics/titan/parts/<part>/`
unless they become shared across multiple parts or mechanics.

The artifact inventory and readiness matrix must continue to recognize
part-local artifact ownership and part-local pytest routes.

This does not move Titan role authority, proof, runtime storage, routing
behavior, private retention, or source-owner doctrine into `aoa-memo`.

## Affected Surfaces

- `mechanics/titan/parts/*/{schemas,examples,tests}/`
- `mechanics/titan/AGENTS.md`
- `mechanics/titan/docs/AGENTS.md`
- `mechanics/titan/docs/README.md`
- `mechanics/titan/LANDING_LOG.md`
- `mechanics/titan/PROVENANCE.md`
- `mechanics/ARTIFACT_TOPOLOGY.md`
- `generated/mechanic_artifacts.min.json`
- `generated/memo_mechanic_readiness.min.json`

## Verification Route

```bash
python -m pytest -q mechanics/titan/parts/core-memory-posture/tests mechanics/titan/parts/closeout-and-digest-posture/tests mechanics/titan/parts/specialized-policy/tests
python scripts/validate_mechanic_artifact_inventory.py
python scripts/validate_memo_mechanic_readiness.py
python scripts/release_check.py
```
