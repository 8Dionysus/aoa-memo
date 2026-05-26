# Writeback Curated Object Examples

- Decision ID: AOA-MEM-D-0041

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-writeback-curated-object-examples.md
- Surface classes: local port/writeback, mechanic package
- Mechanic parents: writeback
- Guard families: local port/writeback
- Memory object classes: local_candidate
- Posture: active rationale

## Context

The root `examples/` lane now has positive family contracts for shared memory
object, lifecycle, recall, and support examples. The self-agency continuity
decision and state-capsule examples were still physically stored in root
`examples/`, even though their family owner was the writeback mechanic and
`examples/AGENTS.md` already routed self-agency examples to the writeback
mechanic.

Those two examples are still curated memory-object inputs for the root
object-facing generated family. The question is where the authored examples
should live when the object is public and shared enough for generated recall,
but the owner boundary is mechanic-local.

## Decision

Move the self-agency continuity decision and state-capsule examples into
`mechanics/writeback/parts/growth-and-continuity/examples/`, while keeping
`examples/memory_object_surface_manifest.json` as the root manifest that
selects curated object-surface inputs.

The root manifest may reference mechanic-local public examples when a mechanic
owns the authored object boundary. Generated object-facing surfaces still
belong in root `generated/` because they are repo-wide recall companions, not
single-package artifacts.

## Alternatives

- Keep the examples in root `examples/` and rely on the root example family
  owner to explain writeback ownership. This preserved paths, but left a
  mechanic-owned artifact in a root district.
- Move the examples and remove them from the object-surface manifest. This
  would clean root placement, but it would make continuity recall less visible
  to object-facing consumers.
- Move the entire object-surface manifest under writeback. This would overfit
  a repo-wide generated family to one mechanic.

## Consequences

- Root `examples/` no longer carries writeback-owned self-agency object
  examples.
- The object-facing generated catalog, capsules, and section surfaces now show
  `mechanics/writeback/parts/growth-and-continuity/examples/...` as the source
  path for those objects.
- Future curated object examples can live under a mechanic package when the
  owner boundary is mechanic-local, as long as the root manifest and generated
  family stay deterministic and validated.
- This does not create proof, runtime continuity, route authority, role
  authority, playbook choreography, or owner acceptance.

## Affected Surfaces

- `mechanics/writeback/parts/growth-and-continuity/examples/decision.self-agency-reanchor-window.example.json`
- `mechanics/writeback/parts/growth-and-continuity/examples/state_capsule.self-agency-continuity-relay.example.json`
- `examples/memory_object_surface_manifest.json`
- `generated/memory_object_catalog.json`
- `generated/memory_object_catalog.min.json`
- `generated/memory_object_capsules.json`
- `generated/memory_object_sections.full.json`
- `config/root_technical_districts.json`
- `scripts/validate_memo.py`
- `mechanics/writeback/parts/growth-and-continuity/tests/test_self_agency_continuity_writeback.py`
- `mechanics/writeback/AGENTS.md`
- `mechanics/writeback/LANDING_LOG.md`

## Verification

Use:

```bash
python scripts/generate_memory_object_surfaces.py
python scripts/validate_memo.py
python scripts/validate_memory_object_surfaces.py
python scripts/validate_mechanic_artifact_topology.py
python scripts/build_mechanic_artifact_inventory.py --check
python scripts/validate_mechanic_artifact_inventory.py
python -m pytest -q mechanics/writeback/parts/growth-and-continuity/tests/test_self_agency_continuity_writeback.py tests/test_mechanic_artifact_topology.py tests/test_mechanic_artifact_inventory.py
python scripts/release_check.py
```
