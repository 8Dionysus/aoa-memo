# Mechanic Owner Route Matrix

- Decision ID: AOA-MEM-D-0015

## Index Metadata

- Original date: 2026-05-18
- Surface classes: generated/readout, mechanic package
- Mechanic parents: none
- Guard families: mechanic topology, generated/read-model
- Memory object classes: none
- Posture: active rationale

## Context

The memo mechanics tree now has package cards, readiness checks, artifact
inventory, and route-card generation. Each package also has an `OWNER_MAP.md`
that names what `aoa-memo` may preserve and which stronger owner owns proof,
runtime, routing, role authority, KAG substrate, playbook choreography, stats,
source doctrine, or owner acceptance.

Agents-of-Abyss uses an owner-request queue because the center can write
request packets for owner-local landings. `aoa-memo` needs a weaker surface:
it should make stronger-owner routes inspectable for OS Abyss, but it should
not imply a request was filed, accepted, or landed.

## Decision

Add `generated/memo_mechanic_owner_routes.min.json` as a generated
owner-route matrix built from package `OWNER_MAP.md` files and README mechanic
cards.

The matrix is an inspection and validation companion. It is not an
owner-request queue, owner acceptance receipt, proof surface, runtime
authority, route dispatch, role grant, KAG truth, playbook choreography, stats
truth, or source doctrine.

## Alternatives

- Copy the Agents-of-Abyss owner-request queue shape directly. This would give
  stable request IDs, but it would overclaim memo authority before owner-local
  request packets exist.
- Keep owner routing only in package `OWNER_MAP.md` files. This preserves
  simple Markdown, but OS Abyss consumers would need to scan every package to
  answer a cross-mechanic routing question.
- Fold owner-route data into the readiness matrix. That would blur readiness
  with route lookup and make both surfaces harder to inspect.

## Consequences

- OS Abyss can inspect all memo mechanic owner routes from one compact
  generated surface.
- Release validation fails when a package card names a stronger owner that its
  `OWNER_MAP.md` does not cover.
- Package `OWNER_MAP.md` files remain the authored source for route ownership.
- If future work needs actual owner-local request packets, it should add a
  separate request protocol rather than promoting this matrix.

## Affected Surfaces

- `generated/memo_mechanic_owner_routes.min.json`
- `scripts/build_memo_mechanic_owner_routes.py`
- `scripts/validate_memo_mechanic_owner_routes.py`
- `scripts/memo_mechanic_owner_routes_common.py`
- `tests/test_memo_mechanic_owner_routes.py`
- `generated/memo_mechanic_readiness.min.json`
- `scripts/mechanic_readiness_common.py`
- `config/root_technical_districts.json`
- `scripts/release_check.py`
- `mechanics/README.md`
- `mechanics/ARTIFACT_TOPOLOGY.md`
- `mechanics/AGENTS.md`

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
