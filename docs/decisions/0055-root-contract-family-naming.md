# Root Contract Family Naming

- Decision ID: AOA-MEM-D-0055

## Status

Accepted on 2026-05-19.

## Index Metadata

- Original date: 2026-05-19
- Surface classes: root/topology, validation guard
- Mechanic parents: none
- Guard families: root technical district
- Memory object classes: none
- Posture: active rationale

## Context

Root `tests/` and `config/root_technical_districts.json` still named two
active cross-mechanic regression families after their migration-era staging
posture.

The tests no longer protect migration stages. They protect current
operation-first contract surfaces that now live in mechanic packages and
functioning parts. Keeping staging names in root technical districts made the
current topology look like a historical staging layer.

## Decision

Rename active root cross-mechanic regression families by what they protect now:

- `cross_mechanic_operational_contracts`
- `cross_mechanic_candidate_contracts`

Rename matching test files, test classes, validation routes, package references,
and generated companions to the same current owner-language. Also rename the
part-local governance-boundary and post-release-boundary regressions away from
staging labels.

Normalize active root doctrine and roadmap wording where it used the same
staging vocabulary generically. Do not rename source-owned Agon landing stages,
lineage source references, raw legacy snapshots, or historical changelog entries
when those labels are provenance rather than current root topology.

## Consequences

- Root tests describe current contract responsibility rather than migration
  history.
- Historical `legacy/` and source-owner staging references remain
  provenance when they are real source labels.
- Generated mechanic artifact, landing-log, readiness, and AGENTS mesh
  companions must be rebuilt after naming changes.
- This does not move contract ownership, grant proof authority, or remove
  source refs that still belong to stronger owners.

## Verification

- `python -m pytest -q tests/test_cross_mechanic_operational_contracts.py tests/test_cross_mechanic_candidate_contracts.py mechanics/governance/parts/governance-boundary/tests/test_governance_boundary_contracts.py mechanics/operational-gate/parts/post-release-boundaries/tests/test_post_release_boundary_contracts.py`
- `python scripts/validate_mechanic_artifact_topology.py`
- `python scripts/validate_mechanic_artifact_inventory.py`
- `python scripts/validate_memo_mechanic_landing_logs.py`
- `python scripts/validate_memo_mechanic_readiness.py`
- `python scripts/validate_agents_mesh.py`
- `python scripts/release_check.py`
