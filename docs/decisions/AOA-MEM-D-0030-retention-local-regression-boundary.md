# Retention Local Regression Boundary

- Decision ID: AOA-MEM-D-0030

## Status

Accepted on 2026-05-18.

Amended on 2026-05-19 by the retention part-local artifact move. The original
package-local test was split into part-local routes.

## Index Metadata

- Original date: 2026-05-18
- Surface classes: lifecycle/retention, mechanic package, boundary/runtime/sibling
- Mechanic parents: retention
- Guard families: lifecycle/retention, sibling and boundary
- Memory object classes: none
- Posture: active rationale

## Context

The retention mechanic already owned active docs, schemas, and examples under
`mechanics/retention/`, but its package-local artifact inventory had zero
tests. Its route card pointed to the governance-boundary contract
regression, which validates one retention-adjacent contract but does not protect
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
- The governance-boundary contract test remains useful but is no longer the only
  retention validation named by the package route card.
- The mechanic artifact inventory and readiness surfaces must include the new
  retention test.
- `aoa-memo` still does not claim retention execution, runtime scheduling,
  proof, private trace retention, role authority, or stronger policy authority.

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
