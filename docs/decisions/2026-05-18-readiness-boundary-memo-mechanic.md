# 2026-05-18 Readiness Boundary Memo Mechanic

## Status

Accepted.

## Context

The memory readiness boundary started as a flat docs-root surface with a root
schema, root example, and root test.

That shape hid the operation:

- the doc mapped high-pressure memory inputs to existing object kinds
- the contract separated memory gate, retention boundary, and writeback
  boundary
- the test protected the boundary but lived outside the mechanic tree

As `aoa-memo` prepares for active OS Abyss use, this is not only core doctrine.
It is a repeatable memory-layer operation that admits or refuses readiness
pressure before proof, runtime retention, graph lift, route dispatch, role
authority, scenario meaning, or source acceptance can be claimed.

## Decision

Create `mechanics/readiness-boundary/` as the owner of memo-side readiness
boundary memory.

The readiness-boundary mechanic owns:

- `MEMORY_READINESS_BOUNDARY.md`
- `memory_readiness_boundary_contract.schema.json`
- `memory_readiness_boundary_contract.example.json`
- readiness-boundary regression tests

Root memory doctrine still owns the memory object canon. Readiness-boundary
owns the pressure admission operation around future durable consequences,
deltas, retention pressure, contradictions, bridge candidates, and service
traces.

## Alternatives Considered

- Keep the doc flat under `docs/`. Rejected because the schema, example, and
  test are mechanic-owned technical artifacts and should sit with the
  operation.
- Merge the surface into `shape-guard`. Rejected because shape-guard prunes
  object/mechanic inflation, while readiness-boundary admits or refuses
  high-pressure memory inputs.
- Merge the surface into `operational-gate` or `retention`. Rejected because
  readiness-boundary spans retention, writeback, contradiction, bridge, and
  service pressure without owning any one stronger outcome.

## Consequences

- The mechanics map gains a readiness-boundary package and generated index
  coverage.
- Root `docs/`, `schemas/`, `examples/`, and `tests/` lose a
  mechanic-owned readiness contract.
- Validators and object-surface generators must use package-local readiness
  refs.
- The package keeps current object-kind reuse visible and blocks new object
  families until stronger owner evidence exists.

## Boundaries

`aoa-memo` still does not own proof, runtime retention, live ledgers, route
dispatch, role authority, graph substrate, scenario acceptance, or source-owner
acceptance.
