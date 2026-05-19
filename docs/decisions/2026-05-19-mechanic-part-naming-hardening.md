# Mechanic Part Naming Hardening

## Status

Accepted on 2026-05-19.

## Context

After the mechanics were materialized as physical `parts/`, several part names
still described a surface family or bucket rather than the operation the part
performs. That weakened the OS Abyss rule that a part is a functioning node:
it should tell future agents what work is owned there, not merely where files
or generated artifacts happen to live.

The package-level mechanic names are already stable operation boundaries and
should not churn. The weak layer is only the local part name where a label
still says "generated", "public index", "support surfaces", "core", or
"specialized policy" without naming the memo action.

## Decision

Keep mechanic package slugs stable and rename only the weak part slugs:

- `lineage-harvest/parts/generated-companions` becomes
  `lineage-harvest/parts/lineage-inspection-projections`.
- `questbook/parts/public-index` becomes
  `questbook/parts/obligation-index`.
- `questbook/parts/generated-views` becomes
  `questbook/parts/quest-read-model-projections`.
- `recurrence-support/parts/recurrence-support-surfaces` becomes
  `recurrence-support/parts/route-return-anchors`.
- `titan/parts/core-memory-posture` becomes
  `titan/parts/recall-and-remembrance-posture`.
- `titan/parts/specialized-policy` becomes
  `titan/parts/audit-personality-and-swarm-policy`.

`generated companions` remains the generic repo term for generated mirror
artifacts. The lineage-harvest part name is narrower: it names the part that
keeps lineage inspection projections legible without making those projections
source truth.

## Alternatives

Renaming package-level mechanics was rejected because those slugs are already
usable route anchors and changing them would create broad churn without better
ownership.

Leaving the weak part names in place was rejected because it would preserve a
storage-first shape inside an operation-first mechanic topology.

Using one shared "generated companions" part name across mechanics was rejected
because generated mirrors are artifacts, not a universal operation. Each part
must name the specific memo work it performs.

## Consequences

Part route cards, local contracts, validators, tests, readiness reports, AGENTS
mesh refs, and generated indexes must use the new part slugs. Historical
decision records may keep their old filenames, but active links should point at
the current part paths.

This change does not move proof, runtime execution, route dispatch, role
rights, owner acceptance, private memory, source doctrine, or stronger-owner
authority into `aoa-memo`.

## Affected Surfaces

- `mechanics/lineage-harvest/parts/lineage-inspection-projections/`
- `mechanics/questbook/parts/obligation-index/`
- `mechanics/questbook/parts/quest-read-model-projections/`
- `mechanics/recurrence-support/parts/route-return-anchors/`
- `mechanics/titan/parts/recall-and-remembrance-posture/`
- `mechanics/titan/parts/audit-personality-and-swarm-policy/`
- generated mechanic artifact, readiness, landing-log, and AGENTS mesh indexes
- Questbook source-contract validation and release gate paths

## Verification

Expected verification:

- `python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py`
- `python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check`
- `python scripts/validate_memo_mechanic_parts.py`
- `python scripts/build_mechanic_artifact_inventory.py --check`
- `python scripts/validate_mechanic_artifact_inventory.py`
- `python scripts/build_agents_mesh_index.py --check`
- `python scripts/validate_agents_mesh_index.py`
- `python scripts/build_memo_mechanic_landing_logs.py --check`
- `python scripts/validate_memo_mechanic_landing_logs.py`
- `python scripts/build_memo_mechanic_readiness.py --check`
- `python scripts/validate_memo_mechanic_readiness.py`
- `python scripts/release_check.py`
