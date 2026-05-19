# Antifragility Part-Local Artifacts

## Status

Accepted on 2026-05-19.

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

Expected verification:

- `python -m pytest -q mechanics/antifragility/parts/failure-lesson-memory/tests mechanics/antifragility/parts/recovery-pattern-memory/tests tests/test_experience_wave3_seed_contracts.py tests/test_memo_validators.py tests/test_roadmap_parity.py mechanics/writeback/parts/growth-and-continuity/tests/test_growth_refinery_writeback.py mechanics/writeback/parts/receipt-publication-regression/tests/test_publish_live_receipts.py`
- `python mechanics/writeback/parts/growth-and-continuity/scripts/generate_growth_refinery_writeback_lanes.py --check`
- `python scripts/generate_memory_object_surfaces.py`
- `python scripts/build_mechanic_artifact_inventory.py --check`
- `python scripts/validate_mechanic_artifact_inventory.py`
- `python scripts/build_memo_mechanic_readiness.py --check`
- `python scripts/validate_memo_mechanic_readiness.py`
- `python scripts/validate_memo_mechanic_parts.py`
- `python scripts/validate_memo.py`
- `python scripts/release_check.py`
