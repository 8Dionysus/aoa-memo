# Mechanic Readiness Artifact Test Coverage

- Decision ID: AOA-MEM-D-0018

## Index Metadata

- Original date: 2026-05-18
- Surface classes: mechanic package, validation guard
- Mechanic parents: none
- Guard families: mechanic topology
- Memory object classes: none
- Posture: active rationale

## Context

Memo mechanics now own package-local schemas, examples, generated companions,
scripts, config, manifests, and tests when those artifacts only make sense
inside one mechanic boundary.

The artifact inventory made those local artifacts inspectable, and the
readiness matrix made mechanic package shape checkable. A gap remained:
a mechanic could grow local non-test artifacts and still appear OS Abyss ready
without any package-local regression test proving that the local contract had a
bounded executable check.

## Decision

`generated/memo_mechanic_readiness.min.json` now includes an
`artifact-test-coverage` check.

A mechanic with package-local config, examples, generated companions,
manifests, schemas, or scripts must also have at least one package-local test.
Mechanics with test-only artifact surfaces remain valid when the test is the
local operation surface, such as a validator or shape-guard regression.

## Alternatives Considered

- Keep this as documentation guidance only. Rejected because artifact coverage
  drift should fail validation, not rely on a reader noticing a paragraph.
- Add a new standalone root validator. Rejected for now because readiness
  already joins package cards, source maps, owner routes, stop-lines, and the
  artifact inventory.
- Require one test per artifact district. Deferred because the current repo
  needs a package-level regression floor first; finer per-district coverage can
  grow after real package pressure proves it useful.

## Consequences

- A mechanic can no longer be reported as OS Abyss ready while local non-test
  artifacts have no local test surface.
- The readiness payload exposes artifact counts, non-test counts, and test
  counts for each package.
- Future package-local artifact moves must keep the test boundary local or
  deliberately justify a stronger readiness model.

## Affected Surfaces

- `scripts/mechanic_readiness_common.py`
- `generated/memo_mechanic_readiness.min.json`
- `tests/test_memo_mechanic_readiness.py`
- `mechanics/ARTIFACT_TOPOLOGY.md`

## Verification Route

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
