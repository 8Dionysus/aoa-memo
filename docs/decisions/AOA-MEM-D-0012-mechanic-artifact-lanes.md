# Mechanic Artifact Lanes

- Decision ID: AOA-MEM-D-0012

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-18
- Surface classes: mechanic package
- Mechanic parents: none
- Guard families: mechanic topology
- Memory object classes: none
- Posture: active rationale

## Context

The mechanics refactor first moved active docs into package lanes while many
schemas, examples, config seeds, generated companions, scripts, tests, and
manifests stayed in root technical districts.

That was useful as a transition, but it left a misleading topology: artifacts
that only made sense inside Agon, Titan, checkpoint, writeback, consumer
handoff, governance, retention, operational gates, recurrence support, lineage
harvest, antifragility, shape guard, or adoption looked root-owned because
their files were still under root `schemas/`, `examples/`, `generated/`,
`scripts/`, `tests/`, `config/`, and `manifests/`.

## Decision

Move single-mechanic technical artifacts into mechanic-local lanes:

- `mechanics/<slug>/schemas/`
- `mechanics/<slug>/examples/`
- `mechanics/<slug>/config/`
- `mechanics/<slug>/generated/`
- `mechanics/<slug>/scripts/`
- `mechanics/<slug>/tests/`
- `mechanics/<slug>/manifests/`

Keep root technical districts for shared memory-object canon, shared recall
contracts, repo-wide validators, release gates, source maps, and
cross-mechanic regression tests.

Root `manifests/` is now reserved for shared recurrence manifests. Active Agon
recurrence manifests and hook bindings first moved under
`mechanics/agon/manifests/`; once physical parts exist, single-part Agon
manifests move onward to the nearest `mechanics/agon/parts/<part>/manifests/`
home.

## Consequences

- The owning mechanic now carries its own runnable contract surface, not only
  its docs.
- Root validators must discover package-local schemas and examples instead of
  assuming a flat repository.
- Generated companions that serve one mechanic are generated and checked in the
  owning package.
- Root route cards describe shared technical districts and point to
  mechanic-local artifact lanes instead of retaining active aliases.

## Validation

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
