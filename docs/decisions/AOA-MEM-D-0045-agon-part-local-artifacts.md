# Agon Part-Local Artifacts

- Decision ID: AOA-MEM-D-0045

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-19
- Surface classes: mechanic package, mechanic part
- Mechanic parents: agon
- Guard families: mechanic topology, part and payload
- Memory object classes: none
- Posture: active rationale

## Context

The physical `parts/` layer made each active mechanic part reviewable, but
Agon still carried its runnable technical artifacts at package level:
`config/`, `examples/`, `generated/`, `schemas/`, `scripts/`, `tests/`, and
`manifests/`.

That was better than root sprawl, but weaker than the OS Abyss mechanics shape
used by `Agents-of-Abyss`, `aoa-skills`, and `aoa-techniques`, where parts can
own their own runnable companions when a sub-operation has enough technical
weight.

## Decision

Move Agon single-part technical artifacts into the nearest functioning part:

- `parts/prebinding-and-candidate-intake/` owns memo prebindings and
  retention-rank candidate intake companions.
- `parts/bridge-and-evidence-seams/` owns epistemic, KAG, SLC, Sophian, VDS,
  and mechanical-trial memo bridge companions.
- `parts/stage-landing-and-stop-lines/` owns stage recurrence manifests and hook
  bindings.

Extend `generated/mechanic_artifacts.min.json` so the inventory recognizes both
package-local and part-local homes. Extend readiness so part-local test
directories count as local mechanic validation routes.

## Consequences

- Agon parts are now runnable owner units, not only contract headings.
- Package-level Agon technical homes stop acting as a second owner layer for
  sub-operations that already have parts.
- Future artifact moves can use the same inventory/readiness contract rather
  than adding special-case validators.
- The change does not grant Agon proof, runtime, role authority, KAG truth,
  source doctrine, or owner acceptance inside `aoa-memo`.

## Validation

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
