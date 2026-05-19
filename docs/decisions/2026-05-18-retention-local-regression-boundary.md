# Retention Local Regression Boundary

## Status

Accepted on 2026-05-18.

Amended on 2026-05-19 by the retention part-local artifact move. The original
package-local test was split into part-local routes.

## Context

The retention mechanic already owned active docs, schemas, and examples under
`mechanics/retention/`, but its package-local artifact inventory had zero
tests. Its route card pointed to the cross-mechanic Wave 4 governance seed
regression, which validates one retention-adjacent seed but does not protect
the retention package boundary itself.

That left retention weaker than the other mechanic packages: ready in the
generated readiness matrix, but not locally guarded against doc, schema,
example, or stop-line drift.

## Decision

Add part-local retention tests as the retention regression boundary.

The test validates active doc registration, old flat path absence, stronger
owner stop-lines, package-local schema/example discoverability, schema validity,
example validity, and required-field rejection.

## Consequences

- Retention now has a local test lane for the surfaces it owns directly.
- The cross-mechanic Wave 4 test remains useful but is no longer the only
  retention validation named by the package route card.
- The mechanic artifact inventory and readiness surfaces must include the new
  retention test.
- `aoa-memo` still does not claim retention execution, runtime scheduling,
  proof, private trace retention, role authority, or stronger policy authority.

## Verification

Expected verification:

- `python -m pytest -q mechanics/retention/parts/cross-repo-and-governance-retention/tests mechanics/retention/parts/office-markers/tests mechanics/retention/parts/post-release-retention/tests`
- `python scripts/build_mechanic_artifact_inventory.py --check`
- `python scripts/validate_mechanic_artifact_inventory.py`
- `python scripts/build_memo_mechanic_readiness.py --check`
- `python scripts/validate_memo_mechanic_readiness.py`
- `python scripts/release_check.py`
