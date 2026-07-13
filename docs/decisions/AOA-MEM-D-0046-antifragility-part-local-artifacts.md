# Antifragility Part-Local Artifacts

- Decision ID: AOA-MEM-D-0046

## Status

Accepted on 2026-05-19.

## Index Metadata

- Original date: 2026-05-19
- Surface classes: mechanic package, mechanic part
- Mechanic parents: antifragility
- Guard families: mechanic topology, part and payload
- Memory object classes: none
- Posture: active rationale

## Context

Antifragility already had functioning parts for failure lesson memory and
recovery pattern memory. Its schemas, examples, native pattern source, and
local regressions still lived at the package level under
`mechanics/antifragility/{schemas,examples,tests}`.

That made the part names correct but left the executable contracts one layer
above the operations that own them. For OS Abyss, the part must be the working
unit: future agents need to inspect the operation, schema, examples, and local
test together without guessing which package-level files belong to which
function.

## Decision

Move antifragility technical artifacts to the nearest functioning part:

- failure lesson schema, shared lesson schema, failure lesson examples,
  shared lesson example, drift-review example, and failure lesson regression
  under `mechanics/antifragility/parts/failure-lesson-memory/`
- recovery pattern schema, recovery examples, rollback-followthrough and
  component-refresh examples, native antifragility stress/recovery pattern
  example, and recovery pattern regression under
  `mechanics/antifragility/parts/recovery-pattern-memory/`

Keep `shared_lesson_memory` under `failure-lesson-memory` because it is a
lesson-memory support contract, not a third antifragility operation. Keep the
native `pattern.antifragility-stress-recovery-window.example.json` under
`recovery-pattern-memory` because it feeds recovery-pattern memory object
surfaces without becoming a separate router, proof, or rollback authority.

## Alternatives

Leaving artifacts under package-level `schemas/`, `examples/`, and `tests/`
would preserve shorter paths but keep `parts/` descriptive instead of
functional.

Creating a third `shared-lesson-memory` part for one support schema/example
would make the topology look busier while blurring the operation-first split:
the object supports failure lessons rather than owning an independent
antifragility workflow.

Moving the native pattern example into root `examples/` would make the
generated object surface easy to find but would detach it from the
recovery-pattern operation that owns its recall posture.

## Consequences

The antifragility artifact inventory should now report all antifragility
schemas, examples, and tests as `scope: part`. Package-level artifact homes are
provenance only, not active routes.

Writeback growth-lane generation, memory-object surface generation, root
technical protection refs, validators, and regression tests must use the
part-local paths.

The move keeps `aoa-memo` below stronger owners. It does not grant proof
verdicts, current-health truth, rollback authorization, route dispatch, stats
truth, source-owner acceptance, playbook choreography, role authority, or
runtime repair.

## Affected Surfaces

- `mechanics/antifragility/PARTS.md`
- `mechanics/antifragility/PROVENANCE.md`
- `mechanics/antifragility/parts/*`
- `mechanics/antifragility/AGENTS.md`
- `mechanics/antifragility/docs/AGENTS.md`
- `mechanics/antifragility/docs/README.md`
- `mechanics/writeback/parts/growth-and-continuity/`
- `examples/memory_object_surface_manifest.json`
- `generated/memory_object_*.json`
- `generated/mechanic_artifacts.min.json`
- `generated/memo_mechanic_readiness.min.json`

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
