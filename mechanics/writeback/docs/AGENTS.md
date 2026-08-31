# AGENTS.md

## Applies To

This card applies to `mechanics/writeback/docs/`.

## Role

This directory owns active mechanic-owned doctrine and support notes for the
writeback mechanic.

It is not runtime storage, a live receipt ledger, a generated companion home,
or owner-local implementation.

## Conditional route scope

- Above: the package `AGENTS.md`, `README.md`, `PARTS.md`, and `OWNER_MAP.md`
  set the operation and stronger-owner split.
- Here: `docs/README.md` maps the source family; individual docs own active
  mechanic doctrine and support notes.
- Adjacent: package or part artifact homes own schemas, examples, config,
  generated outputs, scripts, tests, manifests, and quests. Use
  `mechanics/ARTIFACT_TOPOLOGY.md` before moving root technical artifacts.
- Below: no nested active law is expected here; legacy context routes through
  `../PROVENANCE.md` and `../legacy/`.

## Conditional source route
When this task touches the path, consult root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/ARTIFACT_TOPOLOGY.md`,
`../AGENTS.md`, `../README.md`, `../PARTS.md`, `../OWNER_MAP.md`, and
`../PROVENANCE.md`.

## Boundaries

- Keep writeback source-linked, candidate-only where appropriate, and weaker
  than runtime or owner acceptance.
- Do not claim a live writeback occurred.
- Do not add root technical artifacts here; use the artifact topology rule
  before moving schemas, examples, generated outputs, scripts, or tests.
- Do not preserve old flat `docs/*.md` aliases.

## Validation
## Closeout

Report active writeback docs changed, generated companions affected or not
affected, and which stronger owner remains responsible for live behavior.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
